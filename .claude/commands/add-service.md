# Skill: Add Service

Scaffold a new service class following SportBook UA architecture conventions.

## Usage
```
/add-service <ServiceName> [brief description of responsibility]
```
Example: `/add-service ReviewService manages user reviews for locations`

## Steps

1. **Create `src/services/<snake_name>.py`** with:
   - A class `<ServiceName>` that receives `db: Session` in `__init__`.
   - Constructor instantiates all required repositories:
     ```python
     self.repo = <Entity>Repository(db)
     ```
   - Each public method raises `HTTPException` (with Ukrainian message) for domain errors.
   - No raw SQL; no direct SQLAlchemy queries — only repository calls.

2. **Register a FastAPI dependency** in `src/config/dependencies.py`:
   ```python
   def get_<snake_name>(db: Session = Depends(get_db)) -> <ServiceName>:
       return <ServiceName>(db)
   ```

3. **Create a controller** `src/controllers/<snake_name>_controller.py`:
   - `APIRouter` with prefix and tags.
   - Inject the service via `Depends(get_<snake_name>)`.
   - Return DTOs, never raw ORM objects.

4. **Mount the router** in `src/main.py`:
   ```python
   from src.controllers.<snake_name>_controller import router as <snake_name>_router
   app.include_router(<snake_name>_router)
   ```

5. **Run `/create-unit-tests <ServiceName>`** to generate the test file.

## Constraints
- Service must NOT import from `src/controllers/` or `src/repositories/` SQL classes directly — only interfaces.
- Layer order: Controller → Service → Repository → Model. Never skip or reverse.
- All user-facing exception messages must be in Ukrainian.
