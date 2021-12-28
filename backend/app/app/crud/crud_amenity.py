from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.amenity import Amenity
from app.schemas.amenity import AmenityCreate, AmenityUpdate


class CRUDAmenity(CRUDBase[Amenity, AmenityCreate, AmenityUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Optional[Amenity]:
        return db.query(Amenity).filter(Amenity.title == title).first()

    def create(
        self, db: Session, *, obj_in: AmenityCreate
    ) -> Amenity:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Amenity, obj_in: Union[AmenityUpdate, Dict[str, Any]]
    ) -> Amenity:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


amenity = CRUDAmenity(Amenity)
