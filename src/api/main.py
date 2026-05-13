import os
import shutil

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.generation.answer_generation import generate_answer
from src.embeddings.index_documents import index_pdf


UPLOAD_DIR = "data/raw"

app = FastAPI(
    title="DocMind AI",
    description="API RAG para responder perguntas com base em documentos",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str
    n_results: int = 1
    document_id: str | None = None


@app.get("/")
def home():
    return {
        "message": "DocMind AI API online",
        "description": "Sistema RAG para perguntas e respostas sobre documentos"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Apenas arquivos PDF são permitidos."
        }

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = index_pdf(file_path)

    return {
        "message": "PDF enviado e indexado com sucesso",
        "file_name": file.filename,
        "document_id": result["document_id"],
        "chunks_indexed": result["chunks_indexed"]
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    result = generate_answer(
        question=request.question,
        n_results=request.n_results,
        document_id=request.document_id
    )

    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": result["sources"],
        "model": result["model"],
        "document_id": result["document_id"]
    }