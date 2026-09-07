from fastapi import APIRouter
from app.core.config import settings
from app.core.llm import LLMAdapterFactory, test_llm_connection

router = APIRouter()

@router.get("/health", summary="Health check and LLM service status")
async def health_check():
    """
    Returns system status and configuration check.
    """
    has_deepseek_key = bool(settings.DEEPSEEK_API_KEY)
    has_openrouter_key = bool(settings.OPENROUTER_API_KEY)

    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_config": {
            "deepseek_configured": has_deepseek_key,
            "openrouter_configured": has_openrouter_key,
            "default_director_model": settings.DEFAULT_DIRECTOR_MODEL,
            "default_scenario_model": settings.DEFAULT_SCENARIO_MODEL,
            "default_visual_model": settings.DEFAULT_VISUAL_MODEL,
        }
    }

@router.get("/health/llm-test", summary="Test live LLM connectivity")
async def test_llm_connectivity():
    """
    Executes a lightweight connectivity ping to configured LLM adapters.
    """
    director_client = LLMAdapterFactory.get_director_llm()
    director_res = await test_llm_connection(director_client)
    
    return {
        "director_test": director_res
    }
