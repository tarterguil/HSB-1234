import logging
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class LLMAdapterFactory:
    """
    Adapter factory for initializing LLM clients for DeepSeek and OpenRouter models.
    """

    @staticmethod
    def get_openrouter_client(model_name: str, temperature: float = 0.7) -> ChatOpenAI:
        """
        Returns a ChatOpenAI instance configured to route through OpenRouter.
        """
        if not settings.OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY is not set.")
        
        return ChatOpenAI(
            model=model_name,
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL,
            temperature=temperature,
            default_headers={
                "HTTP-Referer": "https://harness-ai-agentic.local",
                "X-Title": "HARNESS AI AGENTIC Pathfinder"
            }
        )

    @staticmethod
    def get_deepseek_direct_client(model_name: str = "deepseek-chat", temperature: float = 0.7) -> ChatOpenAI:
        """
        Returns a ChatOpenAI instance configured directly for DeepSeek API.
        """
        if not settings.DEEPSEEK_API_KEY:
            logger.warning("DEEPSEEK_API_KEY is not set.")

        return ChatOpenAI(
            model=model_name,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=temperature
        )

    @classmethod
    def get_director_llm(cls) -> ChatOpenAI:
        """
        Agent 1: Director Model Adapter.
        Primary: DeepSeek Chat (Direct or via OpenRouter fallback).
        """
        if settings.DEEPSEEK_API_KEY:
            try:
                return cls.get_deepseek_direct_client("deepseek-chat", temperature=0.6)
            except Exception as e:
                logger.warning(f"Direct DeepSeek setup error, falling back to OpenRouter: {e}")
        return cls.get_openrouter_client(settings.DEFAULT_DIRECTOR_MODEL, temperature=0.6)

    @classmethod
    def get_scenario_llm(cls) -> ChatOpenAI:
        """
        Agent 2: Scene & Scenario Breakdown Model Adapter.
        Primary: Gemini 2.5 / DeepSeek via OpenRouter.
        """
        return cls.get_openrouter_client(settings.DEFAULT_SCENARIO_MODEL, temperature=0.7)

    @classmethod
    def get_visual_llm(cls) -> ChatOpenAI:
        """
        Agent 3: Job Matching & Visual Creation Model Adapter.
        Primary: Qwen 3 / Qwen 2.5 72B via OpenRouter.
        """
        return cls.get_openrouter_client(settings.DEFAULT_VISUAL_MODEL, temperature=0.5)

async def test_llm_connection(client: ChatOpenAI) -> Dict[str, Any]:
    """
    Utility function to verify connectivity and key validity for an LLM client.
    """
    try:
        response = await client.ainvoke("Ping")
        return {"status": "ok", "response": response.content}
    except Exception as e:
        logger.error(f"LLM connectivity test failed: {e}")
        return {"status": "error", "error": str(e)}
