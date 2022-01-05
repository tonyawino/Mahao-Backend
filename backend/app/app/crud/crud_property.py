from typing import List, Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import cast
from shapely.geometry import Point
from geoalchemy2 import func, WKTElement, Geography
from geoalchemy2.shape import from_shape
from geoalchemy2.types import Geography

from app.crud.base import CRUDBase
from app.models.property import Property
from app.models.favorite import Favorite
from app import schemas

from app.models import PropertyCategory

from app.models import PropertyAmenity


class CRUDProperty(CRUDBase[Property, schemas.PropertyCreate, schemas.PropertyUpdate]):

    def get(self, db: Session, id: Any, user_id: int) -> Optional[Property]:
        query = db.query(Property).filter(Property.id == id)
        query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == user_id)))
        return query.first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100, user_id: int,
            options: Optional[List[str]] = None,
            filters: Optional[schemas.PropertyFilter] = None,
            sort: Optional[str] = "-time",
            sort_latitude: Optional[float] = None,
            sort_longitude: Optional[float] = None
    ) -> List[Property]:
        query = db.query(Property)
        # If a list of IDs is given, filter by them
        if options and (len(options) > 0):
            query = query.filter(Property.id.in_(options))

        if filters:
            # TODO: Actual filtering by Query using SQLAlchemy-Searchable If filtering by query, perform full
            if filters.q:
                # Remove extra spaces
                text = filters.q.replace('  ', ' ')
                search_text = ''
                for word in text.split(' '):
                    search_text = search_text.join('|').join(word)
                query = query.filter(Property.__ts_vector__.match(filters.q))

            # If filtering by minimum number of beds
            if filters.min_bed is not None:
                query = query.filter(Property.num_bed >= filters.min_bed)
            # If filtering by maximum number of beds
            if filters.max_bed is not None:
                query = query.filter(Property.num_bed <= filters.max_bed)

            # If filtering by minimum number of bathrooms
            if filters.min_bath is not None:
                query = query.filter(Property.num_bath >= filters.min_bath)
            # If filtering by maximum number of bathrooms
            if filters.max_bath is not None:
                query = query.filter(Property.num_bath <= filters.max_bath)

            # If filtering by minimum price
            if filters.min_price is not None:
                query = query.filter(Property.price >= filters.min_price)
            # If filtering by maximum price
            if filters.max_price is not None:
                query = query.filter(Property.price <= filters.max_price)

            if filters.location:
                parts = filters.location.split(",")
                lat, lng, radius = tuple([float(part) for part in parts])
                query = query.filter(func.ST_DWithin(cast(Property.location, Geography), cast(from_shape(Point(lng, lat)), Geography), radius*1000))

            # If filtering by verified status
            if filters.is_verified is not None:
                query = query.filter(Property.is_verified == filters.is_verified)

            # If filtering by enabled status
            if filters.is_enabled is not None:
                query = query.filter(Property.is_enabled == filters.is_enabled)

            # If filtering by categories
            if filters.categories:
                if not isinstance(filters.categories, int):
                    categories = [num for num in filters.categories.split(",")]
                else:
                    categories = [filters.categories]
                if len(categories) > 0:
                    query = query.filter(Property.property_category_id.in_(categories))

            # If filtering by amenities
            if filters.amenities:
                if not isinstance(filters.amenities, int):
                    amenities = [num for num in filters.amenities.split(",")]
                else:
                    amenities = [filters.amenities]
                if len(amenities) > 0:
                    query = query.join(PropertyAmenity, (Property.id == PropertyAmenity.property_id))\
                        .filter(PropertyAmenity.amenity_id.in_(amenities))

        # Sort by appropriate field in ascending or descending order
        if sort:
            if sort == "time":
                query = query.order_by(Property.created_at)
            elif sort == "-time":
                query = query.order_by(Property.created_at.desc())
            elif sort == "price":
                query = query.order_by(Property.price)
            elif sort == "-price":
                query = query.order_by(Property.price.desc())
            elif sort == "distance" and sort_latitude is not None and sort_longitude is not None:
                query = query.order_by(func.ST_Distance(cast(Property.location, Geography),
                                                        cast(from_shape(Point(sort_longitude, sort_latitude)), Geography)))
            elif sort == "-distance" and sort_latitude is not None and sort_longitude is not None:
                query = query.order_by(func.ST_Distance(cast(Property.location, Geography),
                                                        cast(from_shape(Point(sort_longitude, sort_latitude)), Geography)).desc())
        query = query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == user_id)))
        return query.offset(skip).limit(limit).all()

    def create_with_owner(
            self, db: Session, *, obj_in: schemas.PropertyCreate, owner_id: int
    ) -> Property:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        query = db.query(Property).filter(Property.owner_id == owner_id)
        query.outerjoin(Favorite, ((Property.id == Favorite.property_id) & (Favorite.user_id == owner_id)))
        return query.offset(skip).limit(limit).all()

    def get_favorite_by_owner(
            self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Property]:
        query = db.query(Property).join(Favorite,
                                        ((Property.id == Favorite.property_id) & (Favorite.user_id == owner_id)))
        return query.offset(skip).limit(limit).all()

    def get_labels(self, property: Property) -> List[str]:
        labels = [f"num_bed:{property.num_bed}", f"num_bath:{property.num_bath}",
                  f"location:{property.location_name}", f"price:{property.price}",
                  f"category:{property.property_category_id}", f"user:{property.owner_id}",
                  f"verified:{property.is_verified}"]

        for amenity in property.property_amenities:
            labels.append(f"amenity:{amenity.id}")
        return labels

    def get_categories(self, property: Property) -> List[str]:
        return [amenity.id for amenity in property.property_amenities]


property = CRUDProperty(Property)
