from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_user

router = APIRouter()

@router.get("/me")
def me(
    current_user = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }