import requests
import os
from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize Supabase client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase : Client = create_client(url, key)

# API key for OpenWeather
weather_api_key = os.getenv("OPENWEATHER_KEY")

class Location(BaseModel):
    latitude: float
    longitude: float

@app.post("/api/get-crops")
async def get_crops(location: Location):
    # Get climate data from OpenWeather API
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={weather_api_key}&units=metric"
    response = requests.get(weather_url)
    weather_data = response.json()

    if response.status_code != 200:
        return {"error": "Failed to fetch weather data"}
    
    temperature = weather_data['main']['temp']
    rainfall = weather_data.get('rain', {}).get('1h', 0)

    # Get crops from supabase
    crops_data = supabase.table('crop_climate').select('crop_id,t_min,t_max,rain_min,rain_max').execute()
    crops = crops_data.data

    suitable_crops = []

    # Filter crops based on climate data
    for crop in crops:
        if (
            crop['t_min'] <= temperature <= crop['t_max']
        ):
            suitable_crops.append(crop['crop_id'])
    
    return {"suitable_crops": suitable_crops}

    