from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.common import Coordinates

class PointCreate(BaseModel):
    coordinates: Coordinates = Field(..., description="[lon, lat]")

class PointUpdate(BaseModel):
    coordinates: Optional[Coordinates] = None

class PointOut(BaseModel):
    id: int
    geometry: dict  # GeoJSON

    class Config:
        from_attributes = True

class PointsBulkCreate(BaseModel):
    items: List[PointCreate]
