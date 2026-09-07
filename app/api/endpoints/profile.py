from fastapi import APIRouter, HTTPException, status
from app.schemas.profile import UserProfileRequest, UserProfileResponse

router = APIRouter()

@router.post("/profile", response_model=UserProfileResponse, status_code=status.HTTP_200_OK, summary="Submit user profile matrix")
async def process_user_profile(profile: UserProfileRequest):
    """
    Validates user traits, background, skills, and target region.
    """
    try:
        return UserProfileResponse(
            status="success",
            message="User profile matrix validated successfully.",
            profile=profile
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to process user profile: {str(e)}"
        )
