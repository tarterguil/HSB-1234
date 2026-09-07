from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.schemas.profile import UserProfileRequest

class StoryGenerationRequest(BaseModel):
    user_profile: UserProfileRequest
    custom_instructions: Optional[str] = Field(default=None, description="Optional custom guidance for the director model")

class DirectorOutputSchema(BaseModel):
    personality_fit_analysis: str
    key_strengths: List[str]
    regional_job_strategy: str
    selected_trajectories: List[str]

class ScenarioStepSchema(BaseModel):
    step_number: int
    title: str
    description: str
    skills_required: List[str]
    workplace_challenge: str

class ScenarioOutputSchema(BaseModel):
    day_in_the_life_title: str
    scenes: List[ScenarioStepSchema]

class VisualCardSchema(BaseModel):
    title: str
    description: str
    pros: List[str]
    cons: List[str]
    alternative_paths: List[str]
    infographic_prompt: str
    map_location_hub: str

class VisualOutputSchema(BaseModel):
    visual_cards: List[VisualCardSchema]

class StoryGenerationResponse(BaseModel):
    task_id: str
    status: str
    current_step: str
    director_output: Optional[DirectorOutputSchema] = None
    scenario_output: Optional[ScenarioOutputSchema] = None
    visual_output: Optional[VisualOutputSchema] = None
    errors: List[str] = Field(default_factory=list)
