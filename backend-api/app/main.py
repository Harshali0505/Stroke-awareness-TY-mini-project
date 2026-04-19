from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/dashboard")
def get_dashboard():
    path = os.path.join(BASE_DIR, "data", "dashboard_stats.json")
    with open(path) as f:
        return json.load(f)

@app.get("/analytics/{file_name}")
def get_analytics(file_name: str):
    path = os.path.join(BASE_DIR, "data", "analytics", f"{file_name}.json")
    
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(path) as f:
        return json.load(f)
