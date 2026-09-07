from typing import List, Optional
from pydantic import BaseModel, Field

class UserProfileRequest(BaseModel):
    name: str = Field(..., description="User full name or display name", example="Alex Rivera")
    academic_background: str = Field(..., description="Education background or current status", example="Computer Science Sophomore")
    skills: List[str] = Field(default_factory=list, description="Key skills and qualification matrix", example=["Python", "Data Analysis", "Communication"])
    personality_traits: List[str] = Field(default_factory=list, description="User traits or strengths", example=["Analytical", "Creative", "Detail-oriented"])
    preferred_working_style: Optional[str] = Field(default="Hybrid", description="Remote, On-site, or Hybrid", example="Hybrid")
    target_region: str = Field(..., description="Target geographic region or city hub", example="San Francisco, CA")
    target_field: Optional[str] = Field(default=None, description="Optional target industry or role interest", example="AI Engineering")

class UserProfileResponse(BaseModel):
    status: str = "success"
    message: str = "Profile processed successfully"
    profile: UserProfileRequest
