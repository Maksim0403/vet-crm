from datetime import date, datetime

from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    pet_id: int
    scheduled_at: datetime
    reason: str


class AppointmentOut(AppointmentCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


class MedicalRecordCreate(BaseModel):
    pet_id: int
    visit_date: date
    diagnosis: str
    treatment: str


class MedicalRecordOut(MedicalRecordCreate):
    id: int

    class Config:
        from_attributes = True
