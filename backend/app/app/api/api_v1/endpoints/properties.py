import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Body
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.storage import upload_file
from app.schemas.geometry import Geometry

router = APIRouter()


@router.get("/", response_model=List[schemas.Property])
def read_properties(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve properties.
    """
    properties = crud.property.get_multi(db, skip=skip, limit=limit)
    return properties


@router.get("/me/", response_model=List[schemas.Property])
def read_my_properties(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve properties by logged in user.
    """
    properties = crud.property.get_multi_by_owner(
        db=db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return properties


@router.post("/", response_model=schemas.Property)
def create_property(
    *,
    db: Session = Depends(deps.get_db),
    feature_image: UploadFile = File(...),
    property_category_id: int = Body(...),
    title: str = Body(...),
    description: str = Body(...),
    num_bed: int = Body(..., title="Number of bedrooms", ge=0),
    num_bath: int = Body(..., title="Number of bathrooms", ge=0),
    location_name: Optional[str] = Body(None),
    price: float = Body(..., title="Rent per month", ge=100),
    location: List[float] = Body(..., title="Coordinates", description="Array with latitude and longitude respectively",
                               example="[43.21, 15.89]"),
    is_enabled: bool = Body(True),
    is_verified: bool = Body(False),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new property.
    """
    if len(location) < 2:
        raise HTTPException(status_code=404, detail="Coordinates are invalid")
    property_in = schemas.PropertyCreate(title=title, description=description,
                                         num_bed=num_bed, num_bath=num_bath,
                                         location_name=location_name, price=price,
                                         is_enabled=is_enabled, is_verified=is_verified,
                                         property_category_id=property_category_id)
    property_category = crud.property_category.get(db=db, id=property_in.property_category_id)
    if not property_category:
        raise HTTPException(status_code=404, detail="Property Category not found")
    property_in.feature_image = upload_file(feature_image, str(uuid.uuid4()), "property")
    property = crud.property.create_with_owner(db=db, obj_in=property_in, owner_id=current_user.id)

    return property


@router.put("/{id}", response_model=schemas.Property)
def update_property(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    feature_image: Optional[UploadFile] = File(None),
    property_category_id: int = Body(...),
    title: str = Body(...),
    description: str = Body(...),
    num_bed: int = Body(..., title="Number of bedrooms", ge=0),
    num_bath: int = Body(..., title="Number of bathrooms", ge=0),
    location_name: Optional[str] = Body(None),
    price: float = Body(..., title="Rent per month", ge=100),
    location: List[float] = Body(..., title="Coordinates",
                               description="Array with latitude and longitude respectively",
                               example="[43.21, 15.89]"),    is_enabled: bool = Body(True),
    is_verified: bool = Body(False),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a property.
    """
    if len(location) < 2:
        raise HTTPException(status_code=404, detail="Coordinates are invalid")
    property = crud.property.get(db=db, id=id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    property_in = schemas.PropertyCreate(title=title, description=description,
                                         num_bed=num_bed, num_bath=num_bath,
                                         location_name=location_name, price=price,
                                         is_enabled=is_enabled, is_verified=is_verified,
                                         property_category_id=property_category_id)
    if feature_image:
        url = upload_file(feature_image, id, "property")
        property_in.feature_image = url

    if not crud.user.is_superuser(current_user):
        property_in.is_verified = property.is_verified
    property = crud.property.update(db=db, db_obj=property, obj_in=property_in)
    return property


@router.get("/{id}", response_model=schemas.Property)
def read_property(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get property by ID.
    """
    property = crud.property.get(db=db, id=id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property


@router.delete("/{id}", response_model=schemas.PropertyInDB)
def delete_property(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a property.
    """
    property = crud.property.get(db=db, id=id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    property = crud.property.remove(db=db, id=id)
    return property
