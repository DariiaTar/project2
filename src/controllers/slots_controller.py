from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.config.database import get_db
from src.config.dependencies import require_admin
from src.services.booking_service import SlotService
from src.dto.booking_dto import SlotCreateDTO, SlotResponseDTO
from src.models.user import User

router = APIRouter()


@router.get("/location/{location_id}", response_model=List[SlotResponseDTO], summary="Всі слоти локації")
def get_slots(location_id: int, db: Session = Depends(get_db)):
    return SlotService(db).get_by_location(location_id)


@router.get("/location/{location_id}/available", response_model=List[SlotResponseDTO], summary="Доступні слоти")
def get_available_slots(location_id: int, db: Session = Depends(get_db)):
    return SlotService(db).get_available(location_id)


@router.post("/", response_model=SlotResponseDTO, summary="Створити слот (адмін)")
def create_slot(
    data: SlotCreateDTO,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return SlotService(db).create(data)


@router.delete("/{slot_id}", summary="Видалити слот (адмін)")
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    SlotService(db).delete(slot_id)
    return {"message": "Слот видалено"}
