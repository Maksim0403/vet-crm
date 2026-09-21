from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.db.session import Base


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    type = Column(String, nullable=False)  # vaccination / feeding / grooming
    scheduled_at = Column(DateTime, nullable=False)
    is_done = Column(Boolean, default=False)
