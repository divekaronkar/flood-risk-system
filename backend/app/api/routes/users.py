from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import require_admin, get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import UserPublic


router = APIRouter()


@router.get("", response_model=list[UserPublic])
def list_users(db: Session = Depends(get_db), _admin=Depends(require_admin)):
    users = db.scalars(select(User).order_by(User.id)).all()
    return [
        UserPublic(
            id=u.id,
            email=u.email,
            full_name=u.full_name,
            is_admin=u.is_admin,
            role=u.role,
            phone_number=u.phone_number
        )
        for u in users
    ]


@router.patch("/me", response_model=UserPublic)
def update_my_profile(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if "full_name" in payload:
        current_user.full_name = payload["full_name"]
    if "phone_number" in payload:
        current_user.phone_number = payload["phone_number"]
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return UserPublic(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        is_admin=current_user.is_admin,
        role=current_user.role,
        phone_number=current_user.phone_number
    )


@router.patch("/{user_id}/role")
def update_user_role(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db),
    _admin=Depends(require_admin),
):
    role = payload.get("role")
    if role not in {"admin", "analyst", "user"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    u = db.scalar(select(User).where(User.id == user_id))
    if u is None:
        raise HTTPException(status_code=404, detail="User not found")

    u.role = role
    u.is_admin = role == "admin"
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "role": u.role, "is_admin": u.is_admin}

