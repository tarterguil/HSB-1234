import uuid
import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status, WebSocket, WebSocketDisconnect
from app.schemas.story import StoryGenerationRequest, StoryGenerationResponse
from app.graph.workflow import career_story_graph
from app.graph.state import CareerStoryState

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory task state store for Phase 1
tasks_db: Dict[str, Dict[str, Any]] = {}

@router.post("/generate-story", response_model=StoryGenerationResponse, status_code=status.HTTP_202_ACCEPTED, summary="Trigger career story generation pipeline")
async def generate_career_story(request: StoryGenerationRequest):
    """
    Executes the multi-agent LangGraph workflow for career pathfinding and story generation.
    """
    task_id = str(uuid.uuid4())
    
    initial_state: CareerStoryState = {
        "user_profile": request.user_profile.model_dump(),
        "custom_instructions": request.custom_instructions,
        "director_output": {},
        "scenario_output": {},
        "visual_output": {},
        "current_step": "started",
        "status": "in_progress",
        "errors": []
    }
    
    try:
        # Execute LangGraph DAG
        final_state = await career_story_graph.ainvoke(initial_state)
        
        response_data = StoryGenerationResponse(
            task_id=task_id,
            status=final_state.get("status", "completed"),
            current_step=final_state.get("current_step", "completed"),
            director_output=final_state.get("director_output"),
            scenario_output=final_state.get("scenario_output"),
            visual_output=final_state.get("visual_output"),
            errors=final_state.get("errors", [])
        )
        
        tasks_db[task_id] = response_data.model_dump()
        return response_data
        
    except Exception as e:
        logger.error(f"Story generation failed for task {task_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LangGraph execution error: {str(e)}"
        )

@router.get("/story-status/{task_id}", response_model=StoryGenerationResponse, summary="Poll status of story generation task")
async def get_story_status(task_id: str):
    """
    Returns current status and generated story results for a given task ID.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task ID '{task_id}' not found."
        )
    return tasks_db[task_id]

@router.websocket("/ws/generate-story")
async def websocket_generate_story(websocket: WebSocket):
    """
    WebSocket endpoint for real-time streaming updates during story generation.
    """
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        request = StoryGenerationRequest.model_validate(data)
        
        await websocket.send_json({"step": "init", "message": "Pipeline initialized"})
        
        initial_state: CareerStoryState = {
            "user_profile": request.user_profile.model_dump(),
            "custom_instructions": request.custom_instructions,
            "director_output": {},
            "scenario_output": {},
            "visual_output": {},
            "current_step": "started",
            "status": "in_progress",
            "errors": []
        }
        
        # Execute workflow
        final_state = await career_story_graph.ainvoke(initial_state)
        
        await websocket.send_json({
            "step": "completed",
            "payload": {
                "director_output": final_state.get("director_output"),
                "scenario_output": final_state.get("scenario_output"),
                "visual_output": final_state.get("visual_output")
            }
        })
        await websocket.close()
        
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected by client.")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_json({"step": "error", "message": str(e)})
        await websocket.close()
