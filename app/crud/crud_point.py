from typing import List
from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import Point as ShpPoint, mapping
from app.crud.base import CRUDBase
from app.models.point import Point as PointModel
from app.schemas.point import PointCreate, PointUpdate

class CRUDPoint(CRUDBase[PointModel, PointCreate, PointUpdate]):
    def create(self, db: Session, obj_in: PointCreate) -> PointModel:
        shp = ShpPoint(obj_in.coordinates[0], obj_in.coordinates[1])
        db_obj = PointModel(geom=from_shape(shp, srid=4326))
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_bulk(self, db: Session, objs_in: List[PointCreate]) -> List[PointModel]:
        records = []
        for obj in objs_in:
            shp = ShpPoint(obj.coordinates[0], obj.coordinates[1])
            records.append(PointModel(geom=from_shape(shp, srid=4326)))
        db.add_all(records)
        db.commit()
        for r in records: db.refresh(r)
        return records

    def update(self, db: Session, db_obj: PointModel, obj_in: PointUpdate) -> PointModel:
        if obj_in.coordinates is not None:
            shp = ShpPoint(obj_in.coordinates[0], obj_in.coordinates[1])
            db_obj.geom = from_shape(shp, srid=4326)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def to_geojson(self, db_obj: PointModel) -> dict:
        shp = to_shape(db_obj.geom)  # shapely Point
        return mapping(shp)

point = CRUDPoint(PointModel)
