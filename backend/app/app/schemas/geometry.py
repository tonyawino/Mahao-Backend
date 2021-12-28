from pydantic import BaseModel, validator
from typing import List


class Coordinates(BaseModel):
    """Check coordinates format."""

    latitude: float
    longitude: float


class Geometry(BaseModel):
    """Feature geometry type and coordinates."""

    type: str = "Point"
    coordinates: Coordinates

    @validator("coordinates")
    def convert_string(cls, coords: Coordinates) -> List[float]:
        """Convert dict into list.

        @validator works here as a converter and ensure the coordinates system of geojson
        features [(lon, lat) / (x, y)]
        The type validation it self is made by Coordinates base model.
        """
        lat, lng = coords.dict().values()
        return [lng, lat]
