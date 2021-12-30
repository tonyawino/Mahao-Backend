import datetime
import uuid
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

from app.core.storage import upload_file
from app.schemas.geometry import Geometry

from app.recommend import gorse

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
    properties = crud.property.get_multi(db, skip=skip, limit=limit, user_id=current_user.id)
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


@router.get("/favorites/", response_model=List[schemas.Property])
def read_favorite_properties(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve favorite properties by logged in user.
    """
    properties = crud.property.get_favorite_by_owner(
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
        latitude: float = Body(..., example="43.21"),
        longitude: float = Body(..., example="43.21"),
        is_enabled: bool = Body(True),
        is_verified: bool = Body(False),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new property.
    """
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

    gorse.insert_item(schemas.GorseItem(Categories=crud.property.get_categories(property),
                                        IsHidden=(not property.is_enabled),
                                        Comment=f"Created by {current_user.id}",
                                        ItemId=property.id,
                                        Labels=crud.property.get_labels(property),
                                        Timestamp=property.created_at))
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
        latitude: float = Body(..., example="43.21"),
        longitude: float = Body(..., example="43.21"),
        is_enabled: bool = Body(True),
        is_verified: bool = Body(False),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a property.
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
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

    gorse.update_item(id, schemas.GorseItem(Categories=crud.property.get_categories(property),
                                            IsHidden=(not property.is_enabled),
                                            Comment=f"Updated by {current_user.id}",
                                            ItemId=property.id,
                                            Labels=crud.property.get_labels(property),
                                            Timestamp=property.last_updated))
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
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
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
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    property = crud.property.remove(db=db, id=id)
    gorse.remove_item(id)
    return property


@router.post("/{id}/modify_property_amenities", response_model=List[schemas.PropertyAmenity])
def modify_property_amenities(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        amenities: schemas.PropertyAmenityModify,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Modify property amenities to property by the property ID, with those being added and removed.
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    amenities_return: List[schemas.PropertyAmenity] = list()
    if amenities.added:
        for amenity_id in amenities.added:
            amenity = crud.property_amenity.get_by_property_id_and_amenity_id(db=db,
                                                                              property_id=id,
                                                                              amenity_id=amenity_id)
            if not amenity:
                actual_amenity = crud.amenity.get(db=db, id=amenity_id)
                if not actual_amenity:
                    raise HTTPException(status_code=404,
                                        detail=f"Some amenities to create not found with id {amenity_id}")

                amenity = crud.property_amenity.create(db=db,
                                                       obj_in=schemas.PropertyAmenityCreate(property_id=id,
                                                                                            amenity_id=amenity_id))
                gorse.add_category_to_item(id, amenity_id)
            amenities_return.append(amenity)

    if amenities.removed:
        for amenity_id in amenities.removed:
            amenity = crud.property_amenity.get_by_property_id_and_amenity_id(db=db,
                                                                              property_id=id,
                                                                              amenity_id=amenity_id)
            if not amenity:
                raise HTTPException(status_code=404,
                                    detail=f"Some property amenities to delete not found with key {amenity_id}")

            amenity = crud.property_amenity.delete_by_property_id_and_amenity_id(db=db,
                                                                                 property_id=id,
                                                                                 amenity_id=amenity_id)
            gorse.remove_category_from_item(id, amenity_id)

    return amenities_return


@router.post("/{id}/add_favorite", response_model=schemas.Favorite)
def add_favorite(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Make the property a favorite for the user
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    favorite = crud.favorite.get_by_property_id_and_user_id(db=db,
                                                            property_id=id,
                                                            user_id=current_user.id)

    if favorite:
        raise HTTPException(status_code=404, detail=f"The favorite already exists")

    favorite = crud.favorite.create(db=db, obj_in=schemas.FavoriteCreate(property_id=id,
                                                                         user_id=current_user.id))

    gorse.insert_feedback([schemas.GorseFeedback(Comment=f"Created by {current_user.id}",
                                                 FeedbackType="favorite",
                                                 ItemId=id,
                                                 UserId=current_user.id,
                                                 Timestamp=favorite.created_at)])
    return favorite


@router.post("/{id}/remove_favorite", response_model=schemas.Favorite)
def remove_favorite(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove the property from the favorite by the user
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    favorite = crud.favorite.get_by_property_id_and_user_id(db=db,
                                                            property_id=id,
                                                            user_id=current_user.id)

    if not favorite:
        raise HTTPException(status_code=404, detail=f"The favorite does not exist")

    favorite = crud.favorite.delete_by_property_id_and_user_id(db=db,
                                                               property_id=id,
                                                               user_id=current_user.id)

    gorse.remove_feedback(user_id=current_user.id, item_id=id, feedback_type="favorite")
    return favorite


@router.post("/{id}/add_feedback", response_model=schemas.Feedback)
def add_feedback(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        feedback: schemas.FeedbackIn,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add feedback to the property by logged in user
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    feedback_out = crud.feedback.create(db=db, obj_in=schemas.FeedbackCreate(**jsonable_encoder(feedback),
                                                                             property_id=id,
                                                                             user_id=current_user.id))

    gorse.insert_feedback([schemas.GorseFeedback(Comment=f"Created by {current_user.id}",
                                                 FeedbackType=feedback_out.feedback_type.lower(),
                                                 ItemId=feedback_out.property_id,
                                                 UserId=feedback_out.user_id,
                                                 Timestamp=feedback_out.created_at)])
    return feedback_out


@router.post("/{id}/add_property_photos", response_model=List[schemas.PropertyPhoto])
def add_property_photos(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        photos: List[UploadFile] = File(...),
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add photos to the property
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    photo_res = list()
    for photo in photos:
        url = upload_file(photo, str(uuid.uuid4()), "property_photo")
        property_photo = crud.property_photo.create(db=db,
                                                    obj_in=schemas.PropertyPhotoCreate(photo=url,
                                                                                       property_id=id,
                                                                                       user_id=current_user.id))
        photo_res.append(property_photo)
    return photo_res


@router.post("/{id}/remove_property_photo", response_model=schemas.PropertyPhoto)
def remove_property_photo(
        *,
        db: Session = Depends(deps.get_db),
        id: int,
        property_photo: schemas.PropertyPhotoRemove,
        current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add photo to the property
    """
    property = crud.property.get(db=db, id=id, user_id=current_user.id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if not crud.user.is_superuser(current_user) and (property.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")

    property_photo = crud.property_photo.get(db=db, id=property_photo.id)

    if not property_photo or (id != property_photo.property_id):
        raise HTTPException(status_code=404, detail=f"The property_photo does not exist")
    property_photo = crud.property_photo.remove(db=db, id=property_photo.id)
    return property_photo
