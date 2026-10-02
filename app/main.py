from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.api import admin, auth, clinic, home, pets
from app.core.config import settings
from app.db.bootstrap import ensure_admin
from app.db.migrations import upgrade_pet_owner_column
from app.db.session import Base, SessionLocal, engine
from app.models import clinic as clinic_models  # noqa: F401

Base.metadata.create_all(bind=engine)
upgrade_pet_owner_column(engine)
with SessionLocal() as db:
    ensure_admin(db)

app = FastAPI(debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(home.router)
app.include_router(pets.router)
app.include_router(admin.router)
app.include_router(clinic.router)


@app.get("/", include_in_schema=False)
def frontend():
    return FileResponse(Path(__file__).with_name("app.html"))


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    if settings.debug:
        raise exc
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


@app.get("/test-error")
def test_error():
    raise ValueError("Тестова помилка для перевірки обробки 500")
