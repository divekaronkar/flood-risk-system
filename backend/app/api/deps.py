from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        subject: str | None = payload.get("sub")
        if subject is None:
            raise HTTPException(status_code=401, detail="Token missing subject")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token signature: {str(e)}")

    user_id = int(subject)
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=401, detail=f"User ID {user_id} not found in database. Please log out and register again.")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user


def require_role(*roles: str):
    def _inner(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles and not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return current_user

    return _inner

