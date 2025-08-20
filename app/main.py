from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.endpoints.points import router as points_router
from app.api.endpoints.polygons import router as polygons_router

app = FastAPI(title=settings.PROJECT_NAME)

# Create tables if not using Alembic (simple dev)
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(points_router)
app.include_router(polygons_router)
