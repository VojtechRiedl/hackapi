from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional


from .. import crud

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("/", summary="Get all topics")
def get_topics(path: str | None = "" ,db: Session = Depends(get_db)):
    return crud.get_topics(db, f"/{path}")

