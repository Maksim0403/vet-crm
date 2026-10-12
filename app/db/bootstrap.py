from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User, UserRole


def create_admin(db: Session, email: str, password: str) -> None:
    admin = db.query(User).filter(User.email == email).first()
    if admin is None:
        admin = User(email=email, hashed_password=hash_password(password), role=UserRole.admin)
        db.add(admin)
    else:
        admin.hashed_password = hash_password(password)
        admin.role = UserRole.admin
    db.commit()
