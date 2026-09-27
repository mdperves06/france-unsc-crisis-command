from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.schemas.auth import UserRegister, UserLogin, UserOut, TokenResponse, AuthStatus, PasswordChange
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()


def get_current_user_from_header(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Extract and validate Bearer token from Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    token = authorization.removeprefix("Bearer ").strip()
    user = auth_service.get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@router.post("/register", response_model=TokenResponse, summary="Register new user")
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        user = auth_service.register_user(db, data)
        from app.services.auth_service import _create_token
        token = _create_token({"sub": str(user.id), "email": user.email, "role": user.role})
        return TokenResponse(access_token=token, user=UserOut.model_validate(user))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse, summary="Login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:
        user, token = auth_service.login_user(db, data.email, data.password)
        return TokenResponse(access_token=token, user=UserOut.model_validate(user))
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.get("/me", response_model=UserOut, summary="Get current user profile")
def get_me(current_user=Depends(get_current_user_from_header)):
    return current_user


@router.get("/status", response_model=AuthStatus, summary="Check auth status")
def auth_status(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    if not authorization or not authorization.startswith("Bearer "):
        return AuthStatus(authenticated=False)
    token = authorization.removeprefix("Bearer ").strip()
    user = auth_service.get_current_user(db, token)
    if not user:
        return AuthStatus(authenticated=False)
    return AuthStatus(authenticated=True, user=UserOut.model_validate(user))


@router.post("/change-password", summary="Change password")
def change_password(
    data: PasswordChange,
    current_user=Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    try:
        auth_service.change_password(db, current_user, data.current_password, data.new_password)
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users", response_model=list[UserOut], summary="List all users (Admin only)")
def list_users(
    current_user=Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    from app.models.user import UserRole
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return auth_service.get_all_users(db)
