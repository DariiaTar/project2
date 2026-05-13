# UML Діаграми — SportBook UA

## Domain Model (основні сутності)

```
User ──────────< Booking >────────── Slot >────────── Location
                                                          |
                                                    LocationImage
```

### Entities:
- **User**: id, email, full_name, role(admin/user/guest), is_active
- **Location**: id, name, category, address, price_per_hour, capacity
- **LocationImage**: id, location_id, image_url, is_primary
- **Slot**: id, location_id, start_time, end_time, status(available/booked/blocked)
- **Booking**: id, user_id, slot_id, status, total_price

## Use Case Діаграма

Актори: Гість, Користувач, Адміністратор

- Гість: переглядати локації, переглядати слоти, реєструватись
- Користувач: все що гість + бронювати слот, скасовувати бронювання, переглядати свої бронювання
- Адміністратор: все що користувач + управляти локаціями, слотами, бронюваннями, користувачами

## Архітектурна діаграма (Layered Architecture)

```
[React Frontend]
      ↕ HTTP/REST
[Controllers Layer]  ← HTTP handlers, request validation
      ↕
[Services Layer]     ← Business logic
      ↕
[Repositories Layer] ← Data access abstraction
      ↕
[Models Layer]       ← SQLAlchemy ORM
      ↕
[PostgreSQL Database]
```
