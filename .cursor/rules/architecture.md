# Architecture Guide — SportBook UA

## Overview

SportBook UA follows a **Layered (N-Tier) Architecture** with strict dependency direction:

```
HTTP Request
     ↓
[Controllers]  — src/controllers/
     ↓
[Services]     — src/services/
     ↓
[Repositories] — src/repositories/
     ↓
[Models]       — src/models/
     ↓
[Database]     — PostgreSQL (prod) / SQLite (tests)
```

Each layer depends only on the layer directly below it.

---

## Layers

### Controllers (`src/controllers/`)
- FastAPI routers; receive HTTP requests, call services, return responses.
- Must not contain business logic.
- May only import from `src/services/` and `src/dto/`.

### Services (`src/services/`)
- All business logic lives here.
- Orchestrate repositories; raise `HTTPException` for domain errors.
- Key services:
  - `AuthService` — registration, login, JWT lifecycle.
  - `BookingService` — booking creation/cancellation/payment + GoF patterns.
  - `SlotService` — slot CRUD.
  - `LocationService` — location CRUD.

### GoF Patterns in Services

**Strategy** (`src/services/pricing_strategy.py`):
```
IPricingStrategy (ABC)
├── StandardPricingStrategy     — base_price × duration
├── PeakHourPricingStrategy     — +25% for 18:00–22:00
└── WeekendPricingStrategy      — +50% on Sat/Sun

DynamicPricingContext           — holds and delegates to the active strategy
```
Inject via `BookingService(db, pricing_strategy=PeakHourPricingStrategy())`.
Or swap at runtime: `booking_service.set_pricing_strategy(WeekendPricingStrategy())`.

**Observer** (`src/services/booking_observer.py`):
```
IBookingObserver (ABC)
├── LoggingObserver             — records events in memory
└── EmailNotificationObserver   — records notification payloads

BookingNotifier                 — maintains observer list; dispatches events
```
Subscribe via `booking_service.add_observer(LoggingObserver())`.
BookingService fires events on: create, cancel, pay.

### Repositories (`src/repositories/`)
- Data-access only. Never contain business logic.
- All repositories implement an abstract interface from `interfaces.py`:
  - `IUserRepository` → `UserRepository` (SQLAlchemy) + `InMemoryUserRepository`
  - `ILocationRepository` → `LocationRepository` + `InMemoryLocationRepository`
  - `ISlotRepository` → `SlotRepository` + `InMemorySlotRepository`
  - `IBookingRepository` → `BookingRepository` + `InMemoryBookingRepository`

**In-Memory implementations** (`src/repositories/in_memory.py`) are pure Python dict-based stores.
They are used in unit tests to eliminate database dependencies.

### Models (`src/models/`)
SQLAlchemy ORM models. No business logic.

| Model    | Key fields                              |
|----------|-----------------------------------------|
| User     | email, hashed_password, role, is_active |
| Location | name, category, price_per_hour, is_active|
| Slot     | location_id, start_time, end_time, status|
| Booking  | user_id, slot_id, total_price, status   |

### DTOs (`src/dto/`)
Pydantic schemas used as input/output contracts between layers.
Services return DTOs; controllers never return raw ORM objects.

---

## Dependency Injection

FastAPI `Depends()` is used for:
- `get_db()` — injects SQLAlchemy session per request.
- `get_current_user()` — decodes JWT and returns current `User`.
- `require_admin()` — verifies `UserRole.ADMIN`.

---

## Configuration (`src/config/`)

- `settings.py` — `AppSettings` Singleton; reads from environment variables.
- `database.py` — SQLAlchemy engine and session factory.
- `dependencies.py` — FastAPI dependency functions.

---

## Testing Architecture

- **Unit tests** — mock all repositories with `MagicMock` OR use `InMemory*` implementations.
- **Integration tests** — use FastAPI `TestClient` with SQLite in-memory database.
- Never use a real PostgreSQL connection in tests.
