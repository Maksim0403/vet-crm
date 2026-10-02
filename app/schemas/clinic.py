from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    pet_id: int
    scheduled_at: datetime
    reason: str


class AppointmentOut(AppointmentCreate):
    id: int
    status: str

    model_config = ConfigDict(from_attributes=True)


class MedicalRecordCreate(BaseModel):
    pet_id: int
    visit_date: date
    diagnosis: str
    treatment: str


class MedicalRecordOut(MedicalRecordCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
