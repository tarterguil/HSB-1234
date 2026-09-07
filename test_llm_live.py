import asyncio
from app.core.llm import LLMAdapterFactory, test_llm_connection

async def run_llm_tests():
    print("--- Testing OpenRouter & DeepSeek API Adapters Live ---")
    openrouter_client = LLMAdapterFactory.get_openrouter_client("google/gemini-2.5-flash")
    res_openrouter = await test_llm_connection(openrouter_client)
    res_openrouter_str = str(res_openrouter).encode('ascii', 'backslashreplace').decode('ascii')
    print(f"[OpenRouter (google/gemini-2.5-flash)] Result: {res_openrouter_str}")

    deepseek_client = LLMAdapterFactory.get_director_llm()
    res_deepseek = await test_llm_connection(deepseek_client)
    res_deepseek_str = str(res_deepseek).encode('ascii', 'backslashreplace').decode('ascii')
    print(f"[Director LLM Adapter] Result: {res_deepseek_str}")

if __name__ == "__main__":
    asyncio.run(run_llm_tests())
