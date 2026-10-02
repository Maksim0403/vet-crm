from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text

from app.db.session import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    status = Column(String, default="planned", nullable=False)


class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    visit_date = Column(Date, nullable=False)
    diagnosis = Column(String, nullable=False)
    treatment = Column(Text, nullable=False)
