from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User, UserRole


def ensure_admin(db: Session) -> None:
    admin = db.query(User).filter(User.email == settings.admin_email).first()
    if admin is None:
        db.add(
            User(
                email=settings.admin_email,
                hashed_password=hash_password(settings.admin_password),
                role=UserRole.admin,
            )
        )
        db.commit()
