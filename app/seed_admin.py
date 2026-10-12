import sys

from app.db.bootstrap import create_admin
from app.db.session import Base, SessionLocal, engine


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python -m app.seed_admin <email> <password>")

    email, password = sys.argv[1:]
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        create_admin(db, email, password)
    finally:
        db.close()

    print(f"Admin user is ready: {email}")


if __name__ == "__main__":
    main()
