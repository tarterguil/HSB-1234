import asyncio
import json
import httpx
from main import app
from app.graph.workflow import career_story_graph, extract_json_from_llm_response

def safe_print(title: str, obj: any):
    print(f"\n=== {title} ===")
    obj_str = str(obj) if not isinstance(obj, (dict, list)) else json.dumps(obj, indent=2)
    safe_str = obj_str.encode('ascii', 'backslashreplace').decode('ascii')
    print(safe_str)

async def test_phase2_multi_agent_pipeline():
    print("==================================================")
    print("   Testing Phase 2 Multi-Agent LangGraph Pipeline  ")
    print("==================================================")

    profile_payload = {
        "name": "Samantha Chen",
        "academic_background": "Bachelor of Science in Data Science & AI",
        "skills": ["Python", "TensorFlow", "FastAPI", "Cloud Infrastructure"],
        "personality_traits": ["Strategic", "Collaborative", "Analytical"],
        "preferred_working_style": "Hybrid",
        "target_region": "Seattle, WA",
        "target_field": "AI Career Pathfinder & Machine Learning Specialist"
    }

    initial_state = {
        "user_profile": profile_payload,
        "custom_instructions": "Emphasize scalable AI system deployment and visual infographic storytelling.",
        "director_output": {},
        "scenario_output": {},
        "visual_output": {},
        "current_step": "init",
        "status": "in_progress",
        "errors": []
    }

    print("\n[1] Executing LangGraph Multi-Agent Workflow (Director -> Scenario -> Visual)...")
    final_state = await career_story_graph.ainvoke(initial_state)

    safe_print("Director Output (Agent 1: DeepSeek)", final_state.get("director_output"))
    safe_print("Scenario Output (Agent 2: Gemini 2.5)", final_state.get("scenario_output"))
    safe_print("Visual Output (Agent 3: Qwen)", final_state.get("visual_output"))

    assert final_state.get("status") == "completed", "Graph failed to reach completed state!"
    assert "director_output" in final_state and final_state["director_output"], "Director output missing!"
    assert "scenario_output" in final_state and final_state["scenario_output"], "Scenario output missing!"
    assert "visual_output" in final_state and final_state["visual_output"], "Visual output missing!"

    print("\n[2] Testing JSON Helper Extractor...")
    sample_llm_markdown = '```json\n{\n  "test": "ok"\n}\n```'
    parsed = extract_json_from_llm_response(sample_llm_markdown)
    assert parsed.get("test") == "ok"
    print("JSON Helper Extractor passed.")

    print("\n[SUCCESS] Phase 2 Multi-Agent Orchestration Verification Passed!")

if __name__ == "__main__":
    asyncio.run(test_phase2_multi_agent_pipeline())
