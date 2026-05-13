# Domain Model — SportBook UA

```mermaid
classDiagram
    class User {
        +int id
        +string email
        +string full_name
        +string hashed_password
        +string phone
        +UserRole role
        +bool is_active
        +datetime created_at
    }

    class Location {
        +int id
        +string name
        +string description
        +LocationCategory category
        +string address
        +float price_per_hour
        +int capacity
        +bool is_active
        +datetime created_at
    }

    class LocationImage {
        +int id
        +int location_id
        +string image_url
        +bool is_primary
    }

    class Slot {
        +int id
        +int location_id
        +datetime start_time
        +datetime end_time
        +SlotStatus status
    }

    class Booking {
        +int id
        +int user_id
        +int slot_id
        +float total_price
        +BookingStatus status
        +string guest_name
        +string guest_email
        +string guest_phone
        +string notes
        +datetime created_at
    }

    class UserRole {
        <<enumeration>>
        USER
        ADMIN
    }

    class LocationCategory {
        <<enumeration>>
        TENNIS
        FOOTBALL
        POOL
        GYM
        OTHER
    }

    class SlotStatus {
        <<enumeration>>
        AVAILABLE
        BOOKED
    }

    class BookingStatus {
        <<enumeration>>
        PENDING_PAYMENT
        CONFIRMED
        CANCELLED
        COMPLETED
    }

    User "1" --> "0..*" Booking : creates
    Location "1" --> "0..*" Slot : has
    Location "1" --> "0..*" LocationImage : has
    Slot "1" --> "0..1" Booking : reserved by
    User --> UserRole
    Location --> LocationCategory
    Slot --> SlotStatus
    Booking --> BookingStatus
```

## Business Rules

1. A `Slot` can only have **one active** `Booking` at a time (1:0..1).
2. A `Slot` transitions: `AVAILABLE` → `BOOKED` on booking creation; `BOOKED` → `AVAILABLE` on cancellation.
3. A `Booking` starts as `PENDING_PAYMENT`; moves to `CONFIRMED` after payment; `CANCELLED` by user/admin.
4. An inactive `User` (`is_active = False`) cannot log in.
5. `total_price` is calculated via the active **PricingStrategy** at booking creation time.
6. Pricing strategies: Standard (base × hours), PeakHour (+25% for 18–22h), Weekend (+50% Sat/Sun).
