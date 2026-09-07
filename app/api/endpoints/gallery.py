import logging
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import datetime

from app.db.session import get_db
from app.db.models import Story

router = APIRouter()
logger = logging.getLogger(__name__)

class StorySaveRequest(BaseModel):
    user_name: str
    target_field: str
    region: str
    story_data: Dict[str, Any]

class StoryGalleryResponse(BaseModel):
    id: int
    user_name: str
    target_field: str
    region: str
    story_data: Dict[str, Any]
    created_at: datetime.datetime

    class Config:
        from_attributes = True

@router.post("/save", response_model=StoryGalleryResponse, status_code=status.HTTP_201_CREATED, summary="Save a story to the gallery")
def save_story(request: StorySaveRequest, db: Session = Depends(get_db)):
    try:
        new_story = Story(
            user_name=request.user_name,
            target_field=request.target_field,
            region=request.region,
            story_data=request.story_data
        )
        db.add(new_story)
        db.commit()
        db.refresh(new_story)
        return new_story
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to save story: {e}")
        raise HTTPException(status_code=500, detail="Failed to save story to database.")

@router.get("/", response_model=List[StoryGalleryResponse], summary="Get all public stories")
def get_gallery(db: Session = Depends(get_db)):
    try:
        # Fetch stories, order by newest first
        stories = db.query(Story).order_by(Story.created_at.desc()).limit(20).all()
        return stories
    except Exception as e:
        logger.error(f"Failed to fetch gallery: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch gallery.")
