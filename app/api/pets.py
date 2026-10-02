from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.pet import Pet
from app.models.user import User
from app.schemas.pet import PetCreate, PetOut

router = APIRouter(prefix="/pets", tags=["pets"])


@router.get("/", response_model=list[PetOut])
def list_my_pets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Pet).filter(Pet.owner_id == current_user.id).all()


@router.post("/", response_model=PetOut)
def create_pet(
    payload: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pet = Pet(**payload.model_dump(), owner_id=current_user.id)
    db.add(pet)
    db.commit()
    db.refresh(pet)
    return pet


@router.get("/{pet_id}", response_model=PetOut)
def get_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    if pet.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your pet")
    return pet
