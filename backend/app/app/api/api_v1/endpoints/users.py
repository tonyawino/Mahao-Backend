from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

from app.recommend import gorse

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
def create_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: schemas.UserCreate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.get_by_phone(db, phone=user_in.phone)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone already exists in the system",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )

    gorse.insert_user(schemas.GorseUser(Subscribe=list(),
                                        Comment=f"Created by {current_user.id}",
                                        UserId=user.id,
                                        Labels=[user.location]))
    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
        *,
        db: Session = Depends(deps.get_db),
        password: str = Body(None),
        first_name: str = Body(None),
        last_name: str = Body(None),
        phone: str = Body(None),
        location: str = Body(None),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if first_name is not None:
        user_in.first_name = first_name
    if last_name is not None:
        user_in.last_name = last_name
    if phone is not None:
        user = crud.user.get_by_phone(db, phone=user_in.phone)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this phone already exists in the system",
            )
        user_in.phone = phone
    if location is not None:
        user_in.location = location
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    gorse.update_user(user.id, schemas.GorseUser(Subscribe=list(),
                                                 Comment=f"Updated by {user.id}",
                                                 UserId=user.id,
                                                 Labels=[user.location]))
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.User)
def create_user_open(
        *,
        db: Session = Depends(deps.get_db),
        user_open: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_by_email(db, email=user_open.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.user.get_by_phone(db, phone=user_open.phone)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone already exists in the system",
        )
    user_in_raw = jsonable_encoder(user_open)
    del user_in_raw["is_active"]
    del user_in_raw["is_superuser"]
    del user_in_raw["is_verified"]
    user_in = schemas.UserCreate(**user_in_raw)
    user = crud.user.create(db, obj_in=user_in)

    gorse.insert_user(schemas.GorseUser(Subscribe=list(),
                                        Comment=f"Created by {user.id}",
                                        UserId=user.id,
                                        Labels=[user.location]))
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
        *,
        db: Session = Depends(deps.get_db),
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )

    if not crud.user.is_superuser(current_user) and (user.id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    user_other = crud.user.get_by_email(db, email=user_in.email)
    if user_other and user.id != user_other.id:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user_other = crud.user.get_by_phone(db, phone=user_in.phone)
    if user_other and user.id != user_other.id:
        raise HTTPException(
            status_code=400,
            detail="The user with this phone already exists in the system",
        )

    if not crud.user.is_superuser(current_user):
        user_in.is_verified = current_user.is_verified
    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    gorse.update_user(user.id, schemas.GorseUser(Subscribe=list(),
                                                 Comment=f"Updated by {current_user.id}",
                                                 UserId=user.id,
                                                 Labels=[user.location]))
    return user
