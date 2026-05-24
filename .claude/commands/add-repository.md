# Skill: Add Repository

Scaffold a complete repository for a new entity: interface, SQLAlchemy implementation, and in-memory implementation.

## Usage
```
/add-repository <EntityName>
```
Example: `/add-repository Review`

## Steps

1. **Define the interface** in `src/repositories/interfaces.py` — add an ABC:
   ```python
   class I<Entity>Repository(ABC):
       @abstractmethod
       def get_by_id(self, entity_id: int) -> Optional[<Entity>]: ...
       @abstractmethod
       def get_all(self) -> list[<Entity>]: ...
       @abstractmethod
       def create(self, **kwargs) -> <Entity>: ...
       @abstractmethod
       def delete(self, entity_id: int) -> None: ...
   ```

2. **Create the SQL implementation** in `src/repositories/<snake_entity>_repository.py`:
   ```python
   class <Entity>Repository(I<Entity>Repository):
       def __init__(self, db: Session): self.db = db
       # implement each interface method using self.db.query(...)
   ```

3. **Add the in-memory implementation** to `src/repositories/in_memory.py`:
   ```python
   class InMemory<Entity>Repository(I<Entity>Repository):
       def __init__(self): self._store: dict[int, <Entity>] = {}; self._next_id = 1
       # implement each method using self._store
   ```

4. **Verify Liskov Substitution**: the in-memory class must be a drop-in replacement:
   ```python
   repo: I<Entity>Repository = InMemory<Entity>Repository()
   ```

5. **Run `/create-unit-tests InMemory<Entity>Repository`** to generate tests.

## Constraints
- Repositories must never contain business logic or raise `HTTPException`.
- Return `None` (not raise) when an entity is not found in `get_by_id`.
- All implementations must inherit from the interface — no duck typing.
