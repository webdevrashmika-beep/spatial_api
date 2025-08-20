from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from geoalchemy2 import functions as geofunc
from sqlalchemy import select
from app.api.deps import get_db
from app.schemas.point import PointCreate, PointUpdate, PointOut, PointsBulkCreate
from app.crud.crud_point import point as point_crud
from app.models.point import Point as PointModel
from app.models.polygon import Polygon as PolygonModel
from geoalchemy2.shape import to_shape

router = APIRouter(prefix="/points", tags=["points"])

@router.post("/", response_model=PointOut)
def create_point(payload: PointCreate, db: Session = Depends(get_db)):
    obj = point_crud.create(db, payload)
    return {"id": obj.id, "geometry": point_crud.to_geojson(obj)}

@router.post("/bulk", response_model=List[PointOut])
def create_points_bulk(payload: PointsBulkCreate, db: Session = Depends(get_db)):
    objs = point_crud.create_bulk(db, payload.items)
    return [{"id": o.id, "geometry": point_crud.to_geojson(o)} for o in objs]

@router.get("/{point_id}", response_model=PointOut)
def get_point(point_id: int, db: Session = Depends(get_db)):
    obj = point_crud.get(db, point_id)
    if not obj:
        raise HTTPException(404, "Point not found")
    return {"id": obj.id, "geometry": point_crud.to_geojson(obj)}

@router.get("/", response_model=List[PointOut])
def list_points(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = point_crud.get_multi(db, skip=skip, limit=limit)
    return [{"id": o.id, "geometry": point_crud.to_geojson(o)} for o in objs]

@router.patch("/{point_id}", response_model=PointOut)
def update_point(point_id: int, payload: PointUpdate, db: Session = Depends(get_db)):
    obj = point_crud.get(db, point_id)
    if not obj:
        raise HTTPException(404, "Point not found")
    obj = point_crud.update(db, obj, payload)
    return {"id": obj.id, "geometry": point_crud.to_geojson(obj)}

@router.delete("/{point_id}", status_code=204)
def delete_point(point_id: int, db: Session = Depends(get_db)):
    obj = point_crud.remove(db, point_id)
    if not obj:
        raise HTTPException(404, "Point not found")
    return

# --- Spatial query: points within polygon ---
@router.get("/within_polygon/{polygon_id}", response_model=List[PointOut])
def points_within_polygon(polygon_id: int, db: Session = Depends(get_db)):
    poly = db.get(PolygonModel, polygon_id)
    if not poly:
        raise HTTPException(404, "Polygon not found")
    stmt = select(PointModel).where(geofunc.ST_Within(PointModel.geom, poly.geom))
    objs = db.execute(stmt).scalars().all()
    return [{"id": o.id, "geometry": point_crud.to_geojson(o)} for o in objs]
