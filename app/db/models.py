from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.types import JSON
from .session import Base

class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, index=True)
    target_field = Column(String, index=True)
    region = Column(String, index=True)
    story_data = Column(JSON) # Store the full output from LangGraph
    created_at = Column(DateTime(timezone=True), server_default=func.now())
