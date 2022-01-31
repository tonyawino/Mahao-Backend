from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.amenity import AmenityCreate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def create_random_amenity(db: Session) -> models.PropertyCategory:
    title = random_lower_string()
    description = random_lower_string()
    item_in = AmenityCreate(title=title, description=description)
    return crud.amenity.create(db=db, obj_in=item_in)
