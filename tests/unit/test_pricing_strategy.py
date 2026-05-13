"""Tests for GoF Strategy pattern — pricing strategies."""
import pytest
from datetime import datetime

from src.services.pricing_strategy import (
    StandardPricingStrategy,
    PeakHourPricingStrategy,
    WeekendPricingStrategy,
    DynamicPricingContext,
    IPricingStrategy,
)


# ── helpers ────────────────────────────────────────────────────────────────

def make_times(date_str: str, hour_start: int, hour_end: int):
    start = datetime.fromisoformat(f"{date_str}T{hour_start:02d}:00:00")
    end = datetime.fromisoformat(f"{date_str}T{hour_end:02d}:00:00")
    return start, end


WEEKDAY = "2026-05-11"   # Monday
SATURDAY = "2026-05-16"  # Saturday
SUNDAY = "2026-05-17"    # Sunday


# ── StandardPricingStrategy ───────────────────────────────────────────────

class TestStandardPricingStrategy:
    def setup_method(self):
        self.strategy = StandardPricingStrategy()

    def test_one_hour(self):
        s, e = make_times(WEEKDAY, 10, 11)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_two_hours(self):
        s, e = make_times(WEEKDAY, 10, 12)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(600.0)

    def test_half_hour(self):
        start = datetime.fromisoformat(f"{WEEKDAY}T10:00:00")
        end = datetime.fromisoformat(f"{WEEKDAY}T10:30:00")
        assert self.strategy.calculate(200.0, start, end) == pytest.approx(100.0)

    def test_three_hours(self):
        s, e = make_times(WEEKDAY, 9, 12)
        assert self.strategy.calculate(500.0, s, e) == pytest.approx(1500.0)

    def test_zero_price_per_hour(self):
        s, e = make_times(WEEKDAY, 10, 12)
        assert self.strategy.calculate(0.0, s, e) == pytest.approx(0.0)

    def test_fractional_price(self):
        s, e = make_times(WEEKDAY, 10, 11)
        assert self.strategy.calculate(99.99, s, e) == pytest.approx(99.99)

    def test_result_is_float(self):
        s, e = make_times(WEEKDAY, 10, 11)
        result = self.strategy.calculate(300, s, e)
        assert isinstance(result, float)

    def test_peak_hours_no_extra_charge(self):
        # Standard ignores time-of-day
        s, e = make_times(WEEKDAY, 19, 21)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(600.0)

    def test_weekend_no_extra_charge(self):
        s, e = make_times(SATURDAY, 10, 11)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_implements_interface(self):
        assert isinstance(self.strategy, IPricingStrategy)


# ── PeakHourPricingStrategy ───────────────────────────────────────────────

class TestPeakHourPricingStrategy:
    def setup_method(self):
        self.strategy = PeakHourPricingStrategy()

    def test_off_peak_no_markup(self):
        s, e = make_times(WEEKDAY, 10, 11)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_peak_hour_18_markup(self):
        s, e = make_times(WEEKDAY, 18, 19)
        result = self.strategy.calculate(300.0, s, e)
        assert result == pytest.approx(300.0 * 1.25)

    def test_peak_hour_19_markup(self):
        s, e = make_times(WEEKDAY, 19, 20)
        result = self.strategy.calculate(300.0, s, e)
        assert result == pytest.approx(300.0 * 1.25)

    def test_peak_hour_21_markup(self):
        s, e = make_times(WEEKDAY, 21, 22)
        result = self.strategy.calculate(300.0, s, e)
        assert result == pytest.approx(300.0 * 1.25)

    def test_hour_22_not_peak(self):
        s, e = make_times(WEEKDAY, 22, 23)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_hour_17_not_peak(self):
        s, e = make_times(WEEKDAY, 17, 18)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_peak_two_hours_markup(self):
        s, e = make_times(WEEKDAY, 19, 21)
        result = self.strategy.calculate(200.0, s, e)
        assert result == pytest.approx(400.0 * 1.25)

    def test_markup_constant_is_25_percent(self):
        assert PeakHourPricingStrategy.PEAK_MARKUP == 0.25

    def test_implements_interface(self):
        assert isinstance(self.strategy, IPricingStrategy)

    def test_early_morning_off_peak(self):
        s, e = make_times(WEEKDAY, 6, 7)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)


# ── WeekendPricingStrategy ────────────────────────────────────────────────

class TestWeekendPricingStrategy:
    def setup_method(self):
        self.strategy = WeekendPricingStrategy()

    def test_weekday_no_markup(self):
        s, e = make_times(WEEKDAY, 10, 11)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_saturday_markup(self):
        s, e = make_times(SATURDAY, 10, 11)
        result = self.strategy.calculate(300.0, s, e)
        assert result == pytest.approx(300.0 * 1.50)

    def test_sunday_markup(self):
        s, e = make_times(SUNDAY, 10, 11)
        result = self.strategy.calculate(300.0, s, e)
        assert result == pytest.approx(300.0 * 1.50)

    def test_friday_no_markup(self):
        friday = "2026-05-15"
        s, e = make_times(friday, 10, 11)
        assert self.strategy.calculate(300.0, s, e) == pytest.approx(300.0)

    def test_weekend_markup_constant(self):
        assert WeekendPricingStrategy.WEEKEND_MARKUP == 0.50

    def test_weekend_two_hours(self):
        s, e = make_times(SATURDAY, 10, 12)
        result = self.strategy.calculate(200.0, s, e)
        assert result == pytest.approx(400.0 * 1.50)

    def test_implements_interface(self):
        assert isinstance(self.strategy, IPricingStrategy)


# ── DynamicPricingContext ─────────────────────────────────────────────────

class TestDynamicPricingContext:
    def test_default_strategy_is_standard(self):
        ctx = DynamicPricingContext()
        assert isinstance(ctx.get_strategy(), StandardPricingStrategy)

    def test_custom_strategy_injected(self):
        strategy = PeakHourPricingStrategy()
        ctx = DynamicPricingContext(strategy)
        assert ctx.get_strategy() is strategy

    def test_set_strategy_replaces(self):
        ctx = DynamicPricingContext()
        new_strategy = WeekendPricingStrategy()
        ctx.set_strategy(new_strategy)
        assert ctx.get_strategy() is new_strategy

    def test_calculate_delegates_to_strategy(self):
        ctx = DynamicPricingContext(StandardPricingStrategy())
        s, e = make_times(WEEKDAY, 10, 11)
        assert ctx.calculate_price(300.0, s, e) == pytest.approx(300.0)

    def test_calculate_with_peak_strategy(self):
        ctx = DynamicPricingContext(PeakHourPricingStrategy())
        s, e = make_times(WEEKDAY, 19, 20)
        assert ctx.calculate_price(300.0, s, e) == pytest.approx(375.0)

    def test_calculate_with_weekend_strategy(self):
        ctx = DynamicPricingContext(WeekendPricingStrategy())
        s, e = make_times(SATURDAY, 10, 11)
        assert ctx.calculate_price(300.0, s, e) == pytest.approx(450.0)

    def test_strategy_swap_changes_result(self):
        ctx = DynamicPricingContext(StandardPricingStrategy())
        s, e = make_times(SATURDAY, 10, 11)
        price_standard = ctx.calculate_price(300.0, s, e)
        ctx.set_strategy(WeekendPricingStrategy())
        price_weekend = ctx.calculate_price(300.0, s, e)
        assert price_weekend > price_standard

    def test_none_strategy_defaults_to_standard(self):
        ctx = DynamicPricingContext(None)
        assert isinstance(ctx.get_strategy(), StandardPricingStrategy)
