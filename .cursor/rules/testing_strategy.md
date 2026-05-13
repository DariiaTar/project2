# Testing Strategy — SportBook UA

## Tools & Commands

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner |
| `pytest-cov` | Coverage measurement |
| `pytest-asyncio` | Async test support |
| `unittest.mock.MagicMock` | Mock SQLAlchemy sessions and repos |

```bash
# Run all unit tests with HTML coverage report
pytest tests/unit/ --cov=src --cov-report=html:htmlcov --cov-report=xml:coverage.xml --junitxml=junit.xml

# Quick coverage check
pytest tests/unit/ --cov=src --cov-report=term-missing -q

# Run a specific test class
pytest tests/unit/test_booking_service.py::TestCreateBooking -v
```

---

## Coverage Targets

| Metric | Target | Current |
|--------|--------|---------|
| Line coverage | ≥ 70% | ~73% |
| Total tests | ≥ 200 | 344 |

Coverage exclusions (configured in `sonar-project.properties`):
- `src/config/**` — framework wiring, not testable in isolation
- `src/main.py` — FastAPI app factory
- `src/dto/**` — Pydantic schema declarations

---

## Test Structure

```
tests/
├── unit/                         # Fast, isolated, no real DB
│   ├── test_auth_service.py      # AuthService unit tests
│   ├── test_booking_service.py   # BookingService unit tests
│   ├── test_location_service.py  # LocationService + SlotService
│   ├── test_price_calculation.py # Price calculation edge cases
│   ├── test_pricing_strategy.py  # Strategy pattern tests
│   ├── test_observer.py          # Observer pattern tests
│   ├── test_in_memory_repositories.py  # In-Memory repo tests
│   ├── test_repositories.py      # SQL repo tests (mocked DB)
│   ├── test_dto_validation.py    # Pydantic DTO validation
│   └── test_models.py            # ORM model tests
└── integration/
    └── test_api.py               # FastAPI TestClient + SQLite
```

---

## Unit Test Conventions

### Mocking the Database Layer

For service tests: mock all three repositories on the service instance.

```python
from unittest.mock import MagicMock
from src.services.booking_service import BookingService

def make_booking_service():
    db = MagicMock()
    service = BookingService(db)
    service.booking_repo = MagicMock()
    service.slot_repo = MagicMock()
    service.location_repo = MagicMock()
    return service
```

### Using In-Memory Repositories

For repository-layer tests: use `InMemory*` implementations — no mocking needed.

```python
from src.repositories.in_memory import InMemoryBookingRepository

def test_create_booking_assigns_id():
    repo = InMemoryBookingRepository()
    booking = repo.create(user_id=1, slot_id=1, total_price=300.0)
    assert booking.id == 1
```

### Testing Pricing Strategies

```python
from src.services.pricing_strategy import PeakHourPricingStrategy, DynamicPricingContext

def test_peak_hour_markup():
    strategy = PeakHourPricingStrategy()
    start = datetime(2026, 5, 11, 19, 0)   # Monday 19:00 — peak
    end   = datetime(2026, 5, 11, 20, 0)
    result = strategy.calculate(300.0, start, end)
    assert result == pytest.approx(375.0)   # 300 × 1.25
```

### Testing Observers

```python
from src.services.booking_observer import LoggingObserver, BookingNotifier

def test_observer_receives_event():
    notifier = BookingNotifier()
    obs = LoggingObserver()
    notifier.subscribe(obs)
    notifier.notify_booking_created(1, 2, 3, 300.0)
    assert obs.events[0]["event"] == "created"
```

---

## What to Test in Each Category

### Happy Path
- Normal inputs produce correct outputs.
- Status transitions succeed (PENDING_PAYMENT → CONFIRMED).

### Error Cases
- `404` when entity not found.
- `400` when slot is already booked.
- `403` when user accesses another user's booking.
- `400` when cancelling an already-cancelled booking.

### Edge Cases
- Zero-price location, zero-duration slot.
- Booking by admin vs. regular user.
- Subscribing the same observer twice (idempotent).
- Empty repository returns empty list, not `None`.

---

## CI Coverage Reports

The CI pipeline (`ci.yml`) generates:
1. `coverage.xml` — for SonarCloud ingestion.
2. `htmlcov/` — human-readable HTML; download from GitHub Actions artifacts.
3. `junit.xml` — JUnit XML for SonarCloud test report ingestion.

All three artifacts are uploaded via `actions/upload-artifact@v4` and retained for 7 days.
