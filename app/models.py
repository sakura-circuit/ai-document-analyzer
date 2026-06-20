from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    characters: int


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    answer: str
    source_chunk: str
    confidence: float
