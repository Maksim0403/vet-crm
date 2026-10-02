from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_admin
from app.models.user import User

router = APIRouter(tags=["home"])


@router.get("/user/home")
def user_home(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.email}", "role": current_user.role}


@router.get("/admin/home")
def admin_home(current_user: User = Depends(require_admin)):
    return {"message": f"Welcome to admin panel, {current_user.email}"}
