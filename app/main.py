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

    best_chunk = search(query_embedding)

    return QuestionResponse(answer=best_chunk)
