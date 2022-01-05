from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.storage import upload_file

router = APIRouter()


@router.get("/", response_model=List[schemas.Amenity])
def read_amenities(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve amenities.
    """
    items = crud.amenity.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.Amenity)
def create_amenity(
    *,
    db: Session = Depends(deps.get_db),
    title: str = Form(...),
    description: str = Form(...),
    icon: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new amenity.
    """
    amenity_in = schemas.AmenityCreate(title=title, description=description)
    amenity = crud.amenity.get_by_title(db, title=amenity_in.title)
    if amenity:
        raise HTTPException(
            status_code=400,
            detail="The amenity with this title already exists in the system",
        )
    amenity = crud.amenity.create(db=db, obj_in=amenity_in)
    if not icon:
        return amenity

    amenity_in.icon = upload_file(icon, amenity.id, "property_amenity")
    amenity = crud.item.update(db=db, db_obj=amenity, obj_in=amenity_in)
    return amenity


@router.put("/{id}", response_model=schemas.Amenity)
def update_amenity(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    icon: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an amenity.
    """
    amenity = crud.amenity.get(db=db, id=id)
    if not amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    amenity_update = schemas.AmenityUpdate(title=title, description=description)
    if icon:
        url = upload_file(icon, amenity.id, "property_amenity")
        amenity_update.icon = url
    amenity = crud.item.update(db=db, db_obj=amenity, obj_in=amenity_update)
    return amenity


@router.get("/{id}", response_model=schemas.Amenity)
def read_amenity(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get amenity by ID.
    """
    amenity = crud.amenity.get(db=db, id=id)
    if not amenity:
        raise HTTPException(status_code=404, detail="Item not found")
    return amenity


@router.delete("/{id}", response_model=schemas.Amenity)
def delete_amenity(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete an amenity.
    """
    amenity = crud.amenity.get(db=db, id=id)
    if not amenity:
        raise HTTPException(status_code=404, detail="Amenity not found")
    amenity = crud.amenity.remove(db=db, id=id)
    return amenity
