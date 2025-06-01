from pydantic import BaseModel

class Coordinates(BaseModel):
    lat: float
    lng: float

    def __str__(self):
        return f"Coordinates(lat={self.lat}, lng={self.lng})"