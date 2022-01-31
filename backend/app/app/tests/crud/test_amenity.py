from sqlalchemy.orm import Session

from app import crud
from app.schemas.amenity import AmenityCreate, AmenityUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_amenity(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = AmenityCreate(title=title, description=description)
    item = crud.amenity.create(db=db, obj_in=item_in)
    assert item.title == title
    assert item.description == description


def test_get_amenity(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = AmenityCreate(title=title, description=description)
    item = crud.amenity.create(db=db, obj_in=item_in)
    stored_item = crud.amenity.get(db=db, id=item.id)
    assert stored_item
    assert item.id == stored_item.id
    assert item.title == stored_item.title
    assert item.description == stored_item.description


def test_update_amenity(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = AmenityCreate(title=title, description=description)
    item = crud.amenity.create(db=db, obj_in=item_in)
    description2 = random_lower_string()
    item_update = AmenityUpdate(title=title, description=description2)
    item2 = crud.amenity.update(db=db, db_obj=item, obj_in=item_update)
    assert item.id == item2.id
    assert item.title == item2.title
    assert item2.description == description2


def test_delete_amenity(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    item_in = AmenityCreate(title=title, description=description)
    item = crud.amenity.create(db=db, obj_in=item_in)
    item2 = crud.amenity.remove(db=db, id=item.id)
    item3 = crud.amenity.get(db=db, id=item.id)
    assert item3 is None
    assert item2.id == item.id
    assert item2.title == title
    assert item2.description == description
