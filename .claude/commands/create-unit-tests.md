# Skill: Create Unit Tests

Generate a complete unit test file for a SportBook UA service or repository.

## Usage
```
/create-unit-tests <ServiceName|RepositoryName>
```
Example: `/create-unit-tests BookingService`

## Steps

1. **Identify the target** from the argument (e.g. `BookingService` → `src/services/booking_service.py`).
2. **Read the source file** to list every public method.
3. **Determine the test file path**: `tests/unit/test_<snake_case_name>.py`.
   - If the file already exists, append new test classes without removing existing ones.
4. **For each public method write:**
   - A `TestClassName` class named after the method group (e.g. `TestCreateBooking`).
   - A happy-path test: normal inputs produce expected output.
   - An error/edge-case test: invalid input raises `HTTPException` or returns expected value.
5. **Mock rules:**
   - Service tests: mock all repository attributes with `MagicMock()`. Never use a real DB.
   - Repository tests: use `InMemory*` implementations from `src/repositories/in_memory.py`.
6. **Imports required in every test file:**
   ```python
   import pytest
   from unittest.mock import MagicMock
   ```
7. **Run the tests after generating:**
   ```bash
   pytest tests/unit/test_<name>.py -v
   ```
   Fix any failures before reporting done.

## Constraints
- All error messages in assertions must match Ukrainian strings from the source.
- Do not import SQLAlchemy, `requests`, or `httpx` in test files.
- Every test function name must start with `test_`.
- Coverage target for the new file: ≥ 70 % of the target module's lines.
