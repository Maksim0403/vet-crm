from fastapi import FastAPI

from app.db.session import Base, engine
from app.models import clinic, patient  # noqa: F401 — потрібно для реєстрації моделей

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}
