from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.clinic import Appointment, MedicalRecord
from app.models.pet import Pet
from app.models.user import User
from app.schemas.clinic import (
    AppointmentCreate,
    AppointmentOut,
    MedicalRecordCreate,
    MedicalRecordOut,
)

router = APIRouter(prefix="/clinic", tags=["clinic"])


def owned_pet(db: Session, pet_id: int, user_id: int) -> Pet:
    pet = db.query(Pet).filter(Pet.id == pet_id, Pet.owner_id == user_id).first()
    if pet is None:
        raise HTTPException(status_code=403, detail="You can access only your patients")
    return pet


@router.post("/appointments", response_model=AppointmentOut)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_pet(db, payload.pet_id, current_user.id)
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


@router.get("/appointments", response_model=list[AppointmentOut])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Appointment)
        .join(Pet, Pet.id == Appointment.pet_id)
        .filter(Pet.owner_id == current_user.id)
        .order_by(Appointment.scheduled_at)
        .all()
    )


@router.post("/medical-records", response_model=MedicalRecordOut)
def create_medical_record(
    payload: MedicalRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_pet(db, payload.pet_id, current_user.id)
    record = MedicalRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/medical-records/{pet_id}", response_model=list[MedicalRecordOut])
def list_medical_records(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    owned_pet(db, pet_id, current_user.id)
    return (
        db.query(MedicalRecord)
        .filter(MedicalRecord.pet_id == pet_id)
        .order_by(MedicalRecord.visit_date.desc())
        .all()
    )
