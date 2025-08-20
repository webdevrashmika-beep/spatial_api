from sqlalchemy import Column, Integer
from geoalchemy2 import Geometry
from app.db.base import Base

class Polygon(Base):
    __tablename__ = "polygons"
    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry(geometry_type="POLYGON", srid=4326, spatial_index=True), nullable=False)
