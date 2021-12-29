from .crud_property import property
from .crud_user import user
from .crud_property_category import property_category
from .crud_amenity import amenity
from .crud_property_amenity import property_amenity
from .crud_favorite import favorite
from .crud_feedback import feedback

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.models.item import Item
# from app.schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
