from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.property_category import PropertyCategory
from app.schemas.property_category import PropertyCategoryCreate, PropertyCategoryUpdate


class CRUDPropertyCategory(CRUDBase[PropertyCategory, PropertyCategoryCreate, PropertyCategoryUpdate]):
    def get_by_title(self, db: Session, *, title: str) -> Optional[PropertyCategory]:
        return db.query(PropertyCategory).filter(PropertyCategory.title == title).first()

    def create(
        self, db: Session, *, obj_in: PropertyCategoryCreate
    ) -> PropertyCategory:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PropertyCategory, obj_in: Union[PropertyCategoryUpdate, Dict[str, Any]]
    ) -> PropertyCategory:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


property_category = CRUDPropertyCategory(PropertyCategory)
