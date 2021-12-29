# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.property_category import PropertyCategory  # noqa
from app.models.amenity import Amenity  # noqa
from app.models.property import Property  # noqa
from app.models.property_amenity import PropertyAmenity  # noqa
from app.models.favorite import Favorite  # noqa
