from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.property_amenity import PropertyAmenity
from app.schemas.property_amenity import PropertyAmenityCreate, PropertyAmenityUpdate


class CRUDPropertyAmenity(CRUDBase[PropertyAmenity, PropertyAmenityCreate, PropertyAmenityUpdate]):
    def get_by_property_id_and_amenity_id(self, db: Session, *, property_id: int, amenity_id: int) -> Optional[
        PropertyAmenity]:
        return db.query(PropertyAmenity).filter(PropertyAmenity.property_id == property_id,
                                                PropertyAmenity.amenity_id == amenity_id).first()

    def delete_by_property_id_and_amenity_id(self, db: Session, *, property_id: int, amenity_id: int) -> Optional[
        PropertyAmenity]:
        obj = db.query(PropertyAmenity).filter(PropertyAmenity.property_id == property_id,
                                               PropertyAmenity.amenity_id == amenity_id).first()
        db.delete(obj)
        db.commit()
        return obj

    def create(
            self, db: Session, *, obj_in: PropertyAmenityCreate
    ) -> PropertyAmenity:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PropertyAmenity, obj_in: Union[PropertyAmenityUpdate, Dict[str, Any]]
    ) -> PropertyAmenity:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


property_amenity = CRUDPropertyAmenity(PropertyAmenity)
