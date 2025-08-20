from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.common import PolygonCoords

class PolygonCreate(BaseModel):
    coordinates: PolygonCoords = Field(..., description="GeoJSON Polygon coordinates")

class PolygonUpdate(BaseModel):
    coordinates: Optional[PolygonCoords] = None

class PolygonOut(BaseModel):
    id: int
    geometry: dict  # GeoJSON

    class Config:
        from_attributes = True
