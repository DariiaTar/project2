from sqlalchemy.orm import Session
from typing import Optional, List
from src.models.location import Location, LocationImage, LocationCategory


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, location_id: int) -> Optional[Location]:
        return self.db.query(Location).filter(Location.id == location_id).first()

    def get_all(self, skip: int = 0, limit: int = 100,
                category: Optional[LocationCategory] = None,
                active_only: bool = True) -> List[Location]:
        query = self.db.query(Location)
        if active_only:
            query = query.filter(Location.is_active.is_(True))
        if category:
            query = query.filter(Location.category == category)
        return query.offset(skip).limit(limit).all()

    def create(self, **kwargs) -> Location:
        location = Location(**kwargs)
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def update(self, location: Location, **kwargs) -> Location:
        for key, value in kwargs.items():
            if value is not None:
                setattr(location, key, value)
        self.db.commit()
        self.db.refresh(location)
        return location

    def delete(self, location: Location) -> None:
        self.db.delete(location)
        self.db.commit()

    def add_image(self, location_id: int, image_url: str, is_primary: bool = False) -> LocationImage:
        if is_primary:
            self.db.query(LocationImage).filter(
                LocationImage.location_id == location_id
            ).update({"is_primary": False})
        image = LocationImage(location_id=location_id, image_url=image_url, is_primary=is_primary)
        self.db.add(image)
        self.db.commit()
        self.db.refresh(image)
        return image

    def delete_image(self, image_id: int) -> None:
        image = self.db.query(LocationImage).filter(LocationImage.id == image_id).first()
        if image:
            self.db.delete(image)
            self.db.commit()
