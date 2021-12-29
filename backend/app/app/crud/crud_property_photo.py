from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.property_photo import PropertyPhoto
from app.schemas.property_photo import PropertyPhotoCreate, PropertyPhotoUpdate


class CRUDPropertyPhoto(CRUDBase[PropertyPhoto, PropertyPhotoCreate, PropertyPhotoUpdate]):

    def create(
        self, db: Session, *, obj_in: PropertyPhotoCreate
    ) -> PropertyPhoto:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PropertyPhoto, obj_in: Union[PropertyPhotoUpdate, Dict[str, Any]]
    ) -> PropertyPhoto:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


property_photo = CRUDPropertyPhoto(PropertyPhoto)
