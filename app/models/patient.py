from sqlalchemy import Column, ForeignKey, Integer, String

from app.db.session import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    owner_name = Column(String, nullable=True)
    clinic_id = Column(Integer, ForeignKey("clinics.id"))
