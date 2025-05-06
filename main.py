import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase : Client = create_client(url, key)

from app.api.all_crops import router as crops_router
from app.api.soil_categories import router as soils_router
from app.api.rotation_plan import router as rotation_router
from app.api.suggest_crops import router as climate_router

app.include_router(crops_router, prefix="/api")
app.include_router(soils_router, prefix="/api")
app.include_router(rotation_router, prefix="/api")
app.include_router(climate_router, prefix="/api")