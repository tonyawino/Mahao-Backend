from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.storage import upload_file

router = APIRouter()


@router.get("/", response_model=List[schemas.PropertyCategory])
def read_property_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve property categories.
    """
    items = crud.property_category.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=schemas.PropertyCategory)
def create_property_category(
    *,
    db: Session = Depends(deps.get_db),
    title: str = Form(...),
    description: str = Form(...),
    icon: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new property category.
    """
    property_category_in = schemas.PropertyCategoryCreate(title=title, description=description)
    property_category = crud.property_category.get_by_title(db, title=property_category_in.title)
    if property_category:
        raise HTTPException(
            status_code=400,
            detail="The property category with this title already exists in the system",
        )
    property_category = crud.property_category.create(db=db, obj_in=property_category_in)
    if not icon:
        return property_category

    property_category_in.icon = upload_file(icon, property_category.id, "property_category")
    property_category = crud.item.update(db=db, db_obj=property_category,
                                         obj_in=property_category_in)
    return property_category


@router.put("/{id}", response_model=schemas.PropertyCategory)
def update_property_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    icon: Optional[UploadFile] = File(None),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a property category.
    """
    property_category = crud.property_category.get(db=db, id=id)
    if not property_category:
        raise HTTPException(status_code=404, detail="Property category not found")
    property_category_update = schemas.PropertyCategoryUpdate(title=title, description=description)
    if icon:
        url = upload_file(icon, property_category.id, "property_category")
        property_category_update.icon = url
    property_category = crud.item.update(db=db, db_obj=property_category,
                                         obj_in=property_category_update)
    return property_category


@router.get("/{id}", response_model=schemas.PropertyCategory)
def read_property_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get property category by ID.
    """
    property_category = crud.property_category.get(db=db, id=id)
    if not property_category:
        raise HTTPException(status_code=404, detail="Item not found")
    return property_category


@router.delete("/{id}", response_model=schemas.PropertyCategory)
def delete_property_category(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a property category.
    """
    property_category = crud.property_category.get(db=db, id=id)
    if not property_category:
        raise HTTPException(status_code=404, detail="Property category not found")
    property_category = crud.property_category.remove(db=db, id=id)
    return property_category
