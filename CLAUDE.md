# SportBook UA — Claude Code Rules

## Architecture (strict layer order)

```
Controllers → Services → Repositories → Models → DB
```

- Controller imports only from `src/services/` and `src/dto/`
- Service imports only from `src/repositories/` interfaces
- Repository imports only from `src/models/`
- Never skip or reverse layers

## Mandatory patterns

**Repository**: every repository class implements an ABC from `src/repositories/interfaces.py`.
Use `InMemory*` implementations for unit tests — they are drop-in replacements (Liskov).

**Strategy**: swap pricing via `DynamicPricingContext.set_strategy()`. Never add `if/else` pricing logic inside services.

**Observer**: hook into booking events via `BookingService.add_observer()`.

**Singleton**: always `AppSettings.get_instance()`, never `AppSettings()`.

## Code rules

- No raw SQL anywhere. All DB access through repository methods only.
- Services never import SQLAlchemy directly.
- All `HTTPException` detail messages must be in Ukrainian.
- No hardcoded secrets — use `src/config/settings.py`.

## Testing rules

- Unit tests: mock repositories with `MagicMock` OR use `InMemory*` — never a real DB.
- Every new public method needs: one happy-path test + one error/edge-case test.
- Coverage target: ≥ 70% of `src/`.

```bash
# Run unit tests
pytest tests/unit/ --cov=src --cov-report=term-missing -q

# Full run with reports
pytest tests/unit/ --cov=src --cov-report=xml:coverage.xml --cov-report=html:htmlcov --junitxml=junit.xml
```

## Available commands

- `/create-unit-tests <ClassName>` — generate unit tests for a service or repository
- `/add-service <ServiceName>` — scaffold service + controller + dependency
- `/add-repository <EntityName>` — scaffold interface + SQL + in-memory implementations
- `/add-pricing-strategy <StrategyName>` — add a new IPricingStrategy with tests
