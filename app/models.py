from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

# Modelo que el cliente envía (sin fecha)
class AssetIn(BaseModel):
    name: str
    category: str
    location: str
    status: str        # Ejemplo: "activo", "inactivo"
    purchase_price: float

# Modelo de respuesta (incluye fecha de creación)
class Asset(AssetIn):
    id: int
    created_at: str
