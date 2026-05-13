from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime


class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List:
        pass

    @abstractmethod
    def create(self, email: str, full_name: str, hashed_password: str, **kwargs):
        pass

    @abstractmethod
    def update(self, user, **kwargs):
        pass

    @abstractmethod
    def delete(self, user) -> None:
        pass


class ILocationRepository(ABC):
    @abstractmethod
    def get_by_id(self, location_id: int):
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = False) -> List:
        pass

    @abstractmethod
    def create(self, name: str, category, address: str, price_per_hour: float, **kwargs):
        pass

    @abstractmethod
    def update(self, location, **kwargs):
        pass

    @abstractmethod
    def delete(self, location) -> None:
        pass


class ISlotRepository(ABC):
    @abstractmethod
    def get_by_id(self, slot_id: int):
        pass

    @abstractmethod
    def get_by_location(self, location_id: int, from_date: Optional[datetime] = None) -> List:
        pass

    @abstractmethod
    def get_available_by_location(self, location_id: int) -> List:
        pass

    @abstractmethod
    def create(self, location_id: int, start_time: datetime, end_time: datetime):
        pass

    @abstractmethod
    def update_status(self, slot, status):
        pass

    @abstractmethod
    def delete(self, slot) -> None:
        pass


class IBookingRepository(ABC):
    @abstractmethod
    def get_by_id(self, booking_id: int):
        pass

    @abstractmethod
    def get_by_user(self, user_id: int) -> List:
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List:
        pass

    @abstractmethod
    def create(self, user_id: int, slot_id: int, total_price: float, **kwargs):
        pass

    @abstractmethod
    def update_status(self, booking, status):
        pass
