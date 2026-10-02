import sys

from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.user import User, UserRole


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m app.seed_admin <email> <password>")

    email, password = sys.argv[1:]
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            user = User(email=email, hashed_password=hash_password(password), role=UserRole.admin)
            db.add(user)
        else:
            user.hashed_password = hash_password(password)
            user.role = UserRole.admin
        db.commit()
    finally:
        db.close()

    print(f"Admin user is ready: {email}")


if __name__ == "__main__":
    main()
