from typing import Optional, List

import starlette.status
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator


class PropertyFilter(BaseModel):
    q: Optional[str] = Field(None, title="Query string")
    min_bed: Optional[int] = Field(None, title="Minimum number of bedrooms")
    max_bed: Optional[int] = Field(None, title="Maximum number of bedrooms")
    min_bath: Optional[int] = Field(None, title="Minimum number of bathrooms")
    max_bath: Optional[int] = Field(None, title="Maximum number of bathrooms")
    min_price: Optional[float] = Field(None, title="Minimum rent per month")
    max_price: Optional[float] = Field(None, title="Maximum rent per month")
    location: Optional[str] = Field(None,
                                            title="Coordinates of location to search in an array with latitude and "
                                                  "longitude respectively", example="[43.21, 42.12]")
    is_verified: Optional[bool] = Field(None, title="Whether the properties are verified or not")
    is_enabled: Optional[bool] = Field(True, title="Whether the properties are enabled or not")
    categories: Optional[str] = Field(None, title="Comma separated List of categories to filter", example="[2, 5, 12]")
    amenities: Optional[str] = Field(None, title="Comma separated List of amenities to filter", example="[21, 15, 2]")

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
                if len(vals) != 2:
                    raise HTTPException(detail=f"Coordinates should be floats in the form lat,lng",
                                        status_code=starlette.status.HTTP_400_BAD_REQUEST)
                v = ",".join(vals)
                return v
            else:
                raise HTTPException(detail=f"Coordinates should be floats in the form lat,lng",
                                    status_code=starlette.status.HTTP_400_BAD_REQUEST)

