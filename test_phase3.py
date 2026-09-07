import asyncio
import httpx
from main import app

async def test_phase3_frontend_and_static_serving():
    print("==================================================")
    print("   Testing Phase 3 Web UI & Map Route Serving     ")
    print("==================================================")

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        # Test root endpoint returns index.html
        res = await client.get("/")
        print(f"[GET /] Status Code: {res.status_code}")
        assert res.status_code == 200
        assert "HARNESS AI AGENTIC" in res.text
        assert "wizard-section" in res.text
        assert "map-container" in res.text

        # Test static CSS file route
        res_css = await client.get("/static/css/style.css")
        print(f"[GET /static/css/style.css] Status Code: {res_css.status_code}")
        assert res_css.status_code == 200
        assert "--primary-gradient" in res_css.text

        # Test static JS file route
        res_js = await client.get("/static/js/app.js")
        print(f"[GET /static/js/app.js] Status Code: {res_js.status_code}")
        assert res_js.status_code == 200
        assert "initLeafletMap" in res_js.text

    print("\n[SUCCESS] Phase 3 Web UI & Map Integration Verification Passed!")

if __name__ == "__main__":
    asyncio.run(test_phase3_frontend_and_static_serving())
