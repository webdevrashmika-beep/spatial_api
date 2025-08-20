from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Polygon as ShpPolygon, mapping
from app.crud.base import CRUDBase
from app.models.polygon import Polygon as PolygonModel
from app.schemas.polygon import PolygonCreate, PolygonUpdate

class CRUDPolygon(CRUDBase[PolygonModel, PolygonCreate, PolygonUpdate]):
    def create(self, db: Session, obj_in: PolygonCreate) -> PolygonModel:
        shp = ShpPolygon(shell=obj_in.coordinates[0],
                         holes=obj_in.coordinates[1:] if len(obj_in.coordinates) > 1 else None)
        if not shp.is_valid:
            shp = shp.buffer(0)  # attempt fix
        db_obj = PolygonModel(geom=from_shape(shp, srid=4326))
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: PolygonModel, obj_in: PolygonUpdate) -> PolygonModel:
        if obj_in.coordinates is not None:
            shp = ShpPolygon(shell=obj_in.coordinates[0],
                             holes=obj_in.coordinates[1:] if len(obj_in.coordinates) > 1 else None)
            if not shp.is_valid:
                shp = shp.buffer(0)
            db_obj.geom = from_shape(shp, srid=4326)
        db.add(db_obj); db.commit(); db.refresh(db_obj)
        return db_obj

    def to_geojson(self, db_obj: PolygonModel) -> dict:
        shp = to_shape(db_obj.geom)  # shapely Polygon
        return mapping(shp)

polygon = CRUDPolygon(PolygonModel)
