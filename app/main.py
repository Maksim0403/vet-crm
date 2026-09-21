from fastapi import FastAPI

from app.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}
