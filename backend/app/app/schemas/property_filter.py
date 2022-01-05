from typing import Optional, List

import starlette.status
from fastapi import HTTPException, Query
from pydantic import BaseModel, Field, validator

class PropertyFilter(BaseModel):
    q: Optional[str] = Query(None, title="Query string")
    min_bed: Optional[int] = Query(None, title="Minimum number of bedrooms")
    max_bed: Optional[int] = Query(None, title="Maximum number of bedrooms")
    min_bath: Optional[int] = Query(None, title="Minimum number of bathrooms")
    max_bath: Optional[int] = Query(None, title="Maximum number of bathrooms")
    min_price: Optional[float] = Query(None, title="Minimum rent per month")
    max_price: Optional[float] = Query(None, title="Maximum rent per month")
    location: Optional[str] = Query(None, title="Coordinates of location to search in an array with latitude, "
                                                  "longitude, and radius in KM respectively", example="[43.21, 42.12, 1]")
    is_verified: Optional[bool] = Query(None, title="Whether the properties are verified or not")
    is_enabled: Optional[bool] = Query(True, title="Whether the properties are enabled or not")
    categories: Optional[str] = Query(None, title="Comma separated List of categories to filter", example="[2, 5, 12]")
    amenities: Optional[str] = Query(None, title="Comma separated List of amenities to filter", example="[21, 15]")

    @validator('categories', 'amenities')
    def comma_separated_list_of_ints(cls, v):
        if v:
            v = v.replace(' ', '')
            if "," in v:
                # Remove trailing commas
                vals = [x for x in v.split(',') if x != '']
                for val in vals:
                    try:
                        value = int(val)
                    except Exception:
                        raise HTTPException(detail=f"{v} Must only contain comma separated integers",
                                            status_code=starlette.status.HTTP_400_BAD_REQUEST)
                v = ",".join(vals)
            else:
                try:
                    v = int(v)
                except Exception:
                    raise HTTPException(detail=f"{v} Must only contain comma separated integers",
                                        status_code=starlette.status.HTTP_400_BAD_REQUEST)

        return v


    @validator('location')
    def comma_separated_list_of_two_floats(cls, v):
        if v:
            v = v.replace(' ', '')
            if "," in v:
                # Remove trailing commas
                vals = [x for x in v.split(',') if x != '']
                for val in vals:
                    try:
                        value = float(val)
                    except Exception as e:
                        raise HTTPException(detail=f"{v} Must only contain comma separated floats",
                                            status_code=starlette.status.HTTP_400_BAD_REQUEST)
                if len(vals) != 3:
                    raise HTTPException(detail=f"Coordinates should be floats in the form lat,lng,radius",
                                        status_code=starlette.status.HTTP_400_BAD_REQUEST)

                if not float(vals[0]) >= -90 and float(vals[0]) <= 90:
                    raise HTTPException(status_code=starlette.status.HTTP_400_BAD_REQUEST,
                                        detail="Latitude must be between -90 and 90 degrees inclusive")
                if not float(vals[1]) >= -180 and float(vals[1]) <= 180:
                    raise HTTPException(status_code=404, detail="Longitude must be between -180 and 180 degrees inclusive")
                if float(vals[2]) < 0:
                    raise HTTPException(status_code=404, detail="Radius must be greater than 0")

                v = ",".join(vals)
                return v
            else:
                raise HTTPException(detail=f"Coordinates should be floats in the form lat,lng,radius",
                                    status_code=starlette.status.HTTP_400_BAD_REQUEST)

