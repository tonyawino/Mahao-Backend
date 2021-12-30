from typing import List, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.property import Property
from app.models.favorite import Favorite
from app.schemas.property import PropertyCreate, PropertyUpdate


class CRUDProperty(CRUDBase[Property, PropertyCreate, PropertyUpdate]):

    def get(self, db: Session, id: Any, user_id: int) -> Optional[Property]:
        query = db.query(Property).filter(Property.id == id)
        query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == user_id)))
        return query.first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, user_id: int
    ) -> List[Property]:
        query = db.query(Property)
        query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == user_id)))
        return query.offset(skip).limit(limit).all()

    def create_with_owner(
            self, db: Session, *, obj_in: PropertyCreate, owner_id: int
    ) -> Property:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        query = db.query(Property).filter(Property.owner_id == owner_id)
        query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == owner_id)))
        return query.offset(skip).limit(limit).all()

    def get_favorite_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        query = db.query(Property).join(Favorite,
                                        ((Property.id == Favorite.property_id) & (Favorite.user_id == owner_id)))
        return query.offset(skip).limit(limit).all()

    def get_labels(self, property: Property) -> List[str]:
        labels = [f"num_bed:{property.num_bed}", f"num_bath:{property.num_bath}",
                  f"location:{property.location_name}", f"price:{property.price}",
                  f"category:{property.property_category_id}", f"user:{property.owner_id}",
                  f"verified:{property.is_verified}"]

        for amenity in property.property_amenities:
            labels.append(f"amenity:{amenity.id}")
        return labels

    def get_categories(self, property: Property) -> List[str]:
        return [amenity.id for amenity in property.property_amenities]


property = CRUDProperty(Property)
