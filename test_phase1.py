import asyncio
import httpx

async def test_fastapi_and_graph():
    from main import app
    from app.graph.workflow import career_story_graph

    print("--- 1. Testing FastAPI Endpoints ---")
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Health endpoint
        res = await client.get("/api/v1/health")
        print(f"[Health] Status Code: {res.status_code}, Response: {res.json()}")
        assert res.status_code == 200

        # Profile endpoint
        profile_payload = {
            "name": "Jordan Lee",
            "academic_background": "Computer Engineering Graduate",
            "skills": ["Python", "Machine Learning", "System Design"],
            "personality_traits": ["Analytical", "Resourceful"],
            "preferred_working_style": "Hybrid",
            "target_region": "Austin, TX",
            "target_field": "AI Engineering"
        }
        res = await client.post("/api/v1/profile", json=profile_payload)
        print(f"[Profile] Status Code: {res.status_code}, Response: {res.json()}")
        assert res.status_code == 200

        # Story generation endpoint
        story_payload = {
            "user_profile": profile_payload,
            "custom_instructions": "Focus on high performance AI agent deployments"
        }
        res = await client.post("/api/v1/generate-story", json=story_payload)
        print(f"[Generate Story] Status Code: {res.status_code}")
        story_res = res.json()
        print(f"Task ID: {story_res.get('task_id')}")
        print(f"Status: {story_res.get('status')}")
        print(f"Director Output: {story_res.get('director_output')}")
        print(f"Scenario Output: {story_res.get('scenario_output')}")
        print(f"Visual Output: {story_res.get('visual_output')}")
        assert res.status_code == 202
        assert story_res.get("status") == "completed"

    print("\n--- 2. Testing LangGraph Graph Compiled State ---")
    initial_state = {
        "user_profile": profile_payload,
        "custom_instructions": "Direct graph test",
        "director_output": {},
        "scenario_output": {},
        "visual_output": {},
        "current_step": "init",
        "status": "in_progress",
        "errors": []
    }
    graph_res = await career_story_graph.ainvoke(initial_state)
    print(f"[LangGraph] Final State Status: {graph_res.get('status')}")
    assert graph_res.get("status") == "completed"

    print("\n[SUCCESS] Phase 1 Verification Passed Successfully!")

if __name__ == "__main__":
    asyncio.run(test_fastapi_and_graph())
