from abc import ABC, abstractmethod
from datetime import datetime


class IPricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_price_per_hour: float, start_time: datetime, end_time: datetime) -> float:
        pass


class StandardPricingStrategy(IPricingStrategy):
    def calculate(self, base_price_per_hour: float, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        return base_price_per_hour * duration_hours


class PeakHourPricingStrategy(IPricingStrategy):
    PEAK_MARKUP = 0.25
    PEAK_START = 18
    PEAK_END = 22

    def calculate(self, base_price_per_hour: float, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        base = base_price_per_hour * duration_hours
        if self.PEAK_START <= start_time.hour < self.PEAK_END:
            return base * (1 + self.PEAK_MARKUP)
        return base


class WeekendPricingStrategy(IPricingStrategy):
    WEEKEND_MARKUP = 0.50

    def calculate(self, base_price_per_hour: float, start_time: datetime, end_time: datetime) -> float:
        duration_hours = (end_time - start_time).total_seconds() / 3600
        base = base_price_per_hour * duration_hours
        if start_time.weekday() >= 5:
            return base * (1 + self.WEEKEND_MARKUP)
        return base


class DynamicPricingContext:
    def __init__(self, strategy: IPricingStrategy = None):
        self._strategy = strategy or StandardPricingStrategy()

    def set_strategy(self, strategy: IPricingStrategy) -> None:
        self._strategy = strategy

    def get_strategy(self) -> IPricingStrategy:
        return self._strategy

    def calculate_price(self, base_price_per_hour: float, start_time: datetime, end_time: datetime) -> float:
        return self._strategy.calculate(base_price_per_hour, start_time, end_time)
