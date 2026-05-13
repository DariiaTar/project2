from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from src.models.slot import Slot, SlotStatus
from src.models.booking import Booking, BookingStatus


class SlotRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, slot_id: int) -> Optional[Slot]:
        return self.db.query(Slot).filter(Slot.id == slot_id).first()

    def get_by_location(self, location_id: int, from_date: Optional[datetime] = None) -> List[Slot]:
        query = self.db.query(Slot).filter(Slot.location_id == location_id)
        if from_date:
            query = query.filter(Slot.start_time >= from_date)
        return query.order_by(Slot.start_time).all()

    def get_available_by_location(self, location_id: int) -> List[Slot]:
        return self.db.query(Slot).filter(
            Slot.location_id == location_id,
            Slot.status == SlotStatus.AVAILABLE,
            Slot.start_time >= datetime.utcnow()
        ).order_by(Slot.start_time).all()

    def create(self, location_id: int, start_time: datetime, end_time: datetime) -> Slot:
        slot = Slot(location_id=location_id, start_time=start_time, end_time=end_time)
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def update_status(self, slot: Slot, status: SlotStatus) -> Slot:
        slot.status = status
        self.db.commit()
        self.db.refresh(slot)
        return slot

    def delete(self, slot: Slot) -> None:
        self.db.delete(slot)
        self.db.commit()


class BookingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, booking_id: int) -> Optional[Booking]:
        return self.db.query(Booking).filter(Booking.id == booking_id).first()

    def get_by_user(self, user_id: int) -> List[Booking]:
        return self.db.query(Booking).filter(Booking.user_id == user_id).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Booking]:
        return self.db.query(Booking).offset(skip).limit(limit).all()

    def create(self, user_id: int, slot_id: int, total_price: float, **kwargs) -> Booking:
        booking = Booking(user_id=user_id, slot_id=slot_id, total_price=total_price, **kwargs)
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        return booking

    def update_status(self, booking: Booking, status: BookingStatus) -> Booking:
        booking.status = status
        self.db.commit()
        self.db.refresh(booking)
        return booking
