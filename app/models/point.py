from sqlalchemy import Column, Integer
from geoalchemy2 import Geometry
from app.db.base import Base

class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    # Store as geography(POINT, 4326) for WGS84 longitude/latitude
    geom = Column(Geometry(geometry_type="POINT", srid=4326, spatial_index=True), nullable=False)
