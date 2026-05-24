# Skill: Add Pricing Strategy

Add a new pricing strategy to the Strategy pattern in SportBook UA.

## Usage
```
/add-pricing-strategy <StrategyName> [description]
```
Example: `/add-pricing-strategy HolidayPricingStrategy adds 40% markup on public holidays`

## Steps

1. **Add the class** to `src/services/pricing_strategy.py`:
   ```python
   class <StrategyName>(IPricingStrategy):
       def calculate(self, base_price: float, start_time: datetime, end_time: datetime) -> float:
           duration_hours = (end_time - start_time).seconds / 3600
           # apply markup logic
           return base_price * duration_hours * <multiplier>
   ```

2. **Register in `DynamicPricingContext`** — add a docstring entry listing the new strategy.

3. **Write tests** in `tests/unit/test_pricing_strategy.py`:
   - A test for a time slot that triggers the markup.
   - A test for a time slot that does NOT trigger the markup (falls back to base price).
   - Use `pytest.approx()` for all float comparisons.

4. **Run tests:**
   ```bash
   pytest tests/unit/test_pricing_strategy.py -v
   ```

## Constraints
- Must inherit from `IPricingStrategy` (ABC in `pricing_strategy.py`).
- `calculate()` must return `float`, never mutate arguments.
- No database access, no HTTP calls inside a strategy.
