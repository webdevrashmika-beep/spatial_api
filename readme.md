# 1) git clone
git clone  https://github.com/webdevrashmika-beep/spatial_api.git
# 2) start db
docker compose up -d

# 3) create venv & install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 4) copy env
cp .env.example .env

# 5) run
uvicorn app.main:app --reload

# 6) Swagger
 http://127.0.0.1:8000/docs

# 7) Example payloads
    - Create a point
        POST /points
        {
            "coordinates": [77.5946, 12.9716]
        }
    
    - Bulk points
        POST /points/bulk
        {
            "items": [
                {"coordinates": [77.58, 12.98]},
                {"coordinates": [72.88, 19.07]}
            ]
        }

    - Create a polygon
        POST /polygons
        {
            "coordinates": [
                [[77.5,13.0],[77.7,13.0],[77.7,12.9],[77.5,12.9],[77.5,13.0]]
            ]
        }   

