from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.rag_service import RAGService

router = APIRouter(prefix="/research", tags=["Research & RAG Library"])

MAX_UPLOAD_BYTES = 20 * 1024 * 1024

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    topic: str = Form("General"),
    region: str = Form("Global"),
    db: Session = Depends(get_db)
):
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 20 MB)")
    doc = RAGService.process_and_store_document(
        db=db,
        filename=file.filename or "uploaded_doc.txt",
        file_bytes=content,
        title=title,
        topic=topic,
        region=region
    )
    return {"id": doc.id, "title": doc.title, "chunks": doc.chunks_count, "summary": doc.summary}

@router.get("/search")
def search_research(query: str = Query(..., min_length=2), limit: int = 10, db: Session = Depends(get_db)):
    return RAGService.search_library(db, query=query, limit=limit)
