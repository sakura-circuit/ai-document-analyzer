from app import config

from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from app.models import UploadResponse, QuestionRequest, QuestionResponse
from app.pdf_reader import extract_text

from app.chunker import split_text

from app.embedding_service import create_embeddings, create_query_embedding

from app.vector_store import store_document, search

from app.gemini_provider import answer_question

app = FastAPI()


# Root endpoint
@app.get("/")
def root():

    return {"project": "AI Document Analyzer", "status": "running"}


# Upload endpoint
@app.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:

        temp_file.write(await file.read())

        pdf_path = temp_file.name

    try:

        text = extract_text(pdf_path)

        chunks = split_text(text)

        for i, chunk in enumerate(chunks):
            print(f"\n=== CHUNK {i} ===")
            print(chunk[:200])

        embeddings = create_embeddings(chunks)

        store_document(chunks, embeddings)

        return UploadResponse(
            filename=file.filename or "unknown.pdf", characters=len(text)
        )

    finally:

        Path(pdf_path).unlink(missing_ok=True)


# Ask endpoint
@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    query_embedding = create_query_embedding(request.question)

    best_chunk, confidence = search(query_embedding)

    answer = answer_question(request.question, best_chunk)

    return QuestionResponse(
        answer=answer, source_chunk=best_chunk, confidence=round(confidence, 3)
    )
