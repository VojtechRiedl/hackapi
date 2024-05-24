from fastapi import APIRouter, Depends, HTTPException, Path
from ..database import get_db
from sqlalchemy.orm import Session

from .. import crud

router = APIRouter(prefix="/topics", tags=["Ideas"])

@router.get("/", summary="Get all topics")
def get_topics():
    return {"message": "Get all topics"}

@router.post("/add_topic", summary="Add a topic")
def add_topic(db: Session = Depends(get_db)):
    return {"message": "Add a topic"}