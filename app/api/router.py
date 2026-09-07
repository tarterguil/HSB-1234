from fastapi import APIRouter
from app.api.endpoints import health, profile, story, gallery

api_router = APIRouter()

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(profile.router, tags=["User Profile"])
api_router.include_router(story.router, tags=["Story Generation"])
api_router.include_router(gallery.router, prefix="/gallery", tags=["Gallery"])
