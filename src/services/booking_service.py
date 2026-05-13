from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.repositories.slot_repository import SlotRepository
from src.repositories.booking_repository import BookingRepository
from src.repositories.location_repository import LocationRepository
from src.models.slot import SlotStatus, Slot
from src.models.booking import BookingStatus
from src.dto.booking_dto import BookingCreateDTO, BookingResponseDTO, SlotCreateDTO, SlotResponseDTO, BookingAdminResponseDTO, BookingDetailsResponseDTO


class SlotService:
    def __init__(self, db: Session):
        self.slot_repo = SlotRepository(db)
        self.location_repo = LocationRepository(db)

    def get_by_location(self, location_id: int) -> List[SlotResponseDTO]:
        slots = self.slot_repo.get_by_location(location_id)
        return [SlotResponseDTO.from_orm(s) for s in slots]

    def get_available(self, location_id: int) -> List[SlotResponseDTO]:
        slots = self.slot_repo.get_available_by_location(location_id)
        return [SlotResponseDTO.from_orm(s) for s in slots]

    def create(self, data: SlotCreateDTO) -> SlotResponseDTO:
        location = self.location_repo.get_by_id(data.location_id)
        if not location:
            raise HTTPException(status_code=404, detail="Локацію не знайдено")
        slot = self.slot_repo.create(data.location_id, data.start_time, data.end_time)
        return SlotResponseDTO.from_orm(slot)

    def delete(self, slot_id: int) -> None:
        slot = self.slot_repo.get_by_id(slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Слот не знайдено")
        if slot.status == SlotStatus.BOOKED:
            raise HTTPException(status_code=400, detail="Не можна видалити заброньований слот")
        self.slot_repo.delete(slot)


class BookingService:
    def __init__(self, db: Session):
        self.booking_repo = BookingRepository(db)
        self.slot_repo = SlotRepository(db)
        self.location_repo = LocationRepository(db)

    def create_booking(self, user_id: int, data: BookingCreateDTO) -> BookingResponseDTO:
        slot = self.slot_repo.get_by_id(data.slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Слот не знайдено")
        if slot.status != SlotStatus.AVAILABLE:
            raise HTTPException(status_code=400, detail="Слот вже заброньований")

        location = self.location_repo.get_by_id(slot.location_id)
        duration_hours = (slot.end_time - slot.start_time).seconds / 3600
        total_price = location.price_per_hour * duration_hours

        booking = self.booking_repo.create(
            user_id=user_id,
            slot_id=data.slot_id,
            total_price=total_price,
            notes=data.notes,
            guest_name=data.guest_name,
            guest_email=data.guest_email,
            guest_phone=data.guest_phone,
        )
        self.slot_repo.update_status(slot, SlotStatus.BOOKED)
        return BookingResponseDTO.from_orm(booking)

    def get_user_bookings(self, user_id: int) -> List[BookingResponseDTO]:
        bookings = self.booking_repo.get_by_user(user_id)
        return [BookingResponseDTO.from_orm(b) for b in bookings]

    def get_all_bookings(self) -> List[BookingResponseDTO]:
        bookings = self.booking_repo.get_all()
        return [BookingResponseDTO.from_orm(b) for b in bookings]

    def get_all_bookings_admin(self) -> List[BookingAdminResponseDTO]:
        """Get all bookings with location and user details for admin panel"""
        bookings = self.booking_repo.get_all()
        admin_bookings = []
        for b in bookings:
            location = self.location_repo.get_by_id(b.slot.location_id)
            admin_booking = BookingAdminResponseDTO(
                id=b.id,
                slot_id=b.slot_id,
                user_id=b.user_id,
                user_full_name=b.user.full_name,
                user_phone=b.user.phone,
                location_id=b.slot.location_id,
                location_name=location.name,
                start_time=b.slot.start_time,
                end_time=b.slot.end_time,
                status=b.status,
                total_price=b.total_price,
                notes=b.notes,
                created_at=b.created_at,
            )
            admin_bookings.append(admin_booking)
        return admin_bookings

    def get_booking(self, booking_id: int, user_id: int = None, is_admin: bool = False) -> BookingDetailsResponseDTO:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронювання не знайдено")
        if not is_admin and booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Доступ заборонено")

        location = self.location_repo.get_by_id(booking.slot.location_id)
        return BookingDetailsResponseDTO(
            id=booking.id,
            slot_id=booking.slot_id,
            status=booking.status,
            total_price=booking.total_price,
            notes=booking.notes,
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            guest_phone=booking.guest_phone,
            created_at=booking.created_at,
            user_id=booking.user_id,
            user_full_name=booking.user.full_name,
            user_phone=booking.user.phone,
            location_id=booking.slot.location_id,
            location_name=location.name,
            location_address=location.address,
            start_time=booking.slot.start_time,
            end_time=booking.slot.end_time,
        )

    def pay_booking(self, booking_id: int, user_id: int = None, is_admin: bool = False) -> BookingDetailsResponseDTO:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронювання не знайдено")
        if not is_admin and booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Доступ заборонено")
        if booking.status != BookingStatus.PENDING_PAYMENT:
            raise HTTPException(status_code=400, detail="Бронювання не потребує оплати")

        updated = self.booking_repo.update_status(booking, BookingStatus.CONFIRMED)
        location = self.location_repo.get_by_id(updated.slot.location_id)
        return BookingDetailsResponseDTO(
            id=updated.id,
            slot_id=updated.slot_id,
            status=updated.status,
            total_price=updated.total_price,
            notes=updated.notes,
            guest_name=updated.guest_name,
            guest_email=updated.guest_email,
            guest_phone=updated.guest_phone,
            created_at=updated.created_at,
            user_id=updated.user_id,
            user_full_name=updated.user.full_name,
            user_phone=updated.user.phone,
            location_id=updated.slot.location_id,
            location_name=location.name,
            location_address=location.address,
            start_time=updated.slot.start_time,
            end_time=updated.slot.end_time,
        )

    def cancel_booking(self, booking_id: int, user_id: int, is_admin: bool = False) -> BookingResponseDTO:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронювання не знайдено")
        if not is_admin and booking.user_id != user_id:
            raise HTTPException(status_code=403, detail="Доступ заборонено")
        if booking.status == BookingStatus.CANCELLED:
            raise HTTPException(status_code=400, detail="Бронювання вже скасовано")

        updated = self.booking_repo.update_status(booking, BookingStatus.CANCELLED)
        self.slot_repo.update_status(booking.slot, SlotStatus.AVAILABLE)
        return BookingResponseDTO.from_orm(updated)

    def update_status(self, booking_id: int, status: BookingStatus) -> BookingResponseDTO:
        booking = self.booking_repo.get_by_id(booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронювання не знайдено")
        updated = self.booking_repo.update_status(booking, status)
        return BookingResponseDTO.from_orm(updated)
