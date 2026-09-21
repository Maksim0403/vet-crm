from sqlalchemy import Column, Date, Integer, String

from app.db.session import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    species = Column(String, nullable=True)
    breed = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    owner_name = Column(String, nullable=True)
