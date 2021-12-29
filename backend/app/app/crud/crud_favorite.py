from typing import List, Union, Dict, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate, FavoriteUpdate


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteUpdate]):
    def get_by_property_id_and_user_id(self, db: Session, *, property_id: int, user_id: int) -> Optional[
        Favorite]:
        return db.query(Favorite).filter(Favorite.property_id == property_id,
                                         Favorite.user_id == user_id).first()

    def delete_by_property_id_and_user_id(self, db: Session, *, property_id: int, user_id: int) -> Optional[
        Favorite]:
        obj = db.query(Favorite).filter(Favorite.property_id == property_id,
                                        Favorite.user_id == user_id).first()
        db.delete(obj)
        db.commit()
        return obj

    def create(
            self, db: Session, *, obj_in: FavoriteCreate
    ) -> Favorite:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Favorite, obj_in: Union[FavoriteUpdate, Dict[str, Any]]
    ) -> Favorite:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


favorite = CRUDFavorite(Favorite)
