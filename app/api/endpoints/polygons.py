from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from geoalchemy2 import functions as geofunc
from sqlalchemy import select
from app.api.deps import get_db
from app.schemas.polygon import PolygonCreate, PolygonUpdate, PolygonOut
from app.crud.crud_polygon import polygon as polygon_crud
from app.models.polygon import Polygon as PolygonModel
from app.models.point import Point as PointModel

router = APIRouter(prefix="/polygons", tags=["polygons"])

@router.post("/", response_model=PolygonOut)
def create_polygon(payload: PolygonCreate, db: Session = Depends(get_db)):
    obj = polygon_crud.create(db, payload)
    return {"id": obj.id, "geometry": polygon_crud.to_geojson(obj)}

@router.get("/{polygon_id}", response_model=PolygonOut)
def get_polygon(polygon_id: int, db: Session = Depends(get_db)):
    obj = polygon_crud.get(db, polygon_id)
    if not obj:
        raise HTTPException(404, "Polygon not found")
    return {"id": obj.id, "geometry": polygon_crud.to_geojson(obj)}

@router.get("/", response_model=List[PolygonOut])
def list_polygons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objs = polygon_crud.get_multi(db, skip=skip, limit=limit)
    return [{"id": o.id, "geometry": polygon_crud.to_geojson(o)} for o in objs]

@router.patch("/{polygon_id}", response_model=PolygonOut)
def update_polygon(polygon_id: int, payload: PolygonUpdate, db: Session = Depends(get_db)):
    obj = polygon_crud.get(db, polygon_id)
    if not obj:
        raise HTTPException(404, "Polygon not found")
    obj = polygon_crud.update(db, obj, payload)
    return {"id": obj.id, "geometry": polygon_crud.to_geojson(obj)}

@router.delete("/{polygon_id}", status_code=204)
def delete_polygon(polygon_id: int, db: Session = Depends(get_db)):
    obj = polygon_crud.remove(db, polygon_id)
    if not obj:
        raise HTTPException(404, "Polygon not found")
    return

# --- Spatial query: polygon contains a point ---
@router.get("/{polygon_id}/contains_point/{point_id}", response_model=bool)
def polygon_contains_point(polygon_id: int, point_id: int, db: Session = Depends(get_db)):
    poly = db.get(PolygonModel, polygon_id)
    pt = db.get(PointModel, point_id)
    if not poly or not pt:
        raise HTTPException(404, "Polygon or Point not found")
    exists = db.execute(
        select(geofunc.ST_Contains(poly.geom, pt.geom))
    ).scalar()
    return bool(exists)
