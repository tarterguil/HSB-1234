from typing import TypedDict, List, Dict, Any, Optional

class CareerStoryState(TypedDict):
    """
    LangGraph State dictionary structure passing data between multi-agent pipeline nodes.
    """
    user_profile: Dict[str, Any]
    custom_instructions: Optional[str]
    director_output: Dict[str, Any]
    scenario_output: Dict[str, Any]
    visual_output: Dict[str, Any]
    current_step: str
    status: str  # 'idle', 'director_processing', 'scenario_processing', 'visual_processing', 'completed', 'error'
    errors: List[str]
