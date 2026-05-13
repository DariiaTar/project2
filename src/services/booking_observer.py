from abc import ABC, abstractmethod
from typing import List


class IBookingObserver(ABC):
    @abstractmethod
    def on_booking_created(self, booking_id: int, user_id: int, slot_id: int, total_price: float) -> None:
        pass

    @abstractmethod
    def on_booking_cancelled(self, booking_id: int, user_id: int) -> None:
        pass

    @abstractmethod
    def on_booking_confirmed(self, booking_id: int, user_id: int) -> None:
        pass


class LoggingObserver(IBookingObserver):
    def __init__(self):
        self.events: List[dict] = []

    def on_booking_created(self, booking_id: int, user_id: int, slot_id: int, total_price: float) -> None:
        self.events.append({
            "event": "created",
            "booking_id": booking_id,
            "user_id": user_id,
            "slot_id": slot_id,
            "total_price": total_price,
        })

    def on_booking_cancelled(self, booking_id: int, user_id: int) -> None:
        self.events.append({
            "event": "cancelled",
            "booking_id": booking_id,
            "user_id": user_id,
        })

    def on_booking_confirmed(self, booking_id: int, user_id: int) -> None:
        self.events.append({
            "event": "confirmed",
            "booking_id": booking_id,
            "user_id": user_id,
        })


class EmailNotificationObserver(IBookingObserver):
    def __init__(self):
        self.sent_notifications: List[dict] = []

    def on_booking_created(self, booking_id: int, user_id: int, slot_id: int, total_price: float) -> None:
        self.sent_notifications.append({
            "type": "booking_confirmation",
            "booking_id": booking_id,
            "user_id": user_id,
            "total_price": total_price,
        })

    def on_booking_cancelled(self, booking_id: int, user_id: int) -> None:
        self.sent_notifications.append({
            "type": "booking_cancellation",
            "booking_id": booking_id,
            "user_id": user_id,
        })

    def on_booking_confirmed(self, booking_id: int, user_id: int) -> None:
        self.sent_notifications.append({
            "type": "payment_confirmed",
            "booking_id": booking_id,
            "user_id": user_id,
        })


class BookingNotifier:
    def __init__(self):
        self._observers: List[IBookingObserver] = []

    def subscribe(self, observer: IBookingObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: IBookingObserver) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def get_observers(self) -> List[IBookingObserver]:
        return list(self._observers)

    def notify_booking_created(self, booking_id: int, user_id: int, slot_id: int, total_price: float) -> None:
        for obs in self._observers:
            obs.on_booking_created(booking_id, user_id, slot_id, total_price)

    def notify_booking_cancelled(self, booking_id: int, user_id: int) -> None:
        for obs in self._observers:
            obs.on_booking_cancelled(booking_id, user_id)

    def notify_booking_confirmed(self, booking_id: int, user_id: int) -> None:
        for obs in self._observers:
            obs.on_booking_confirmed(booking_id, user_id)
