from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import crud, auth
from .models import Asset, AssetIn, User
from datetime import timedelta
from typing import List, Optional


app = FastAPI(title="API de Inventario de Activos")

# Incluir el router de autenticación
app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])



# Obtener todos los activos
@app.get("/assets", response_model=list[Asset])
def get_assets(token: str = Depends(auth.get_current_user),category: Optional[str] = None,
    location: Optional[str] = None,
    status: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,):
    # Aquí validamos el token antes de permitir el acceso
    if min_price and max_price and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="El precio mínimo no puede ser mayor que el precio máximo",
        )

    filters = {}

    if category:
        filters["category"] = category
    if status:
        filters["status"] = status
    if min_price:
        filters["min_price"] = min_price
    if max_price:
        filters["max_price"] = max_price
    if location:
        filters["location"] = location

    assets = crud.get_all_assets(filters)
    return assets
    

# Obtener un activo por ID
@app.get("/assets/{asset_id}", response_model=Asset)
def get_asset(asset_id: int, token: str = Depends(auth.get_current_user)):
    asset = crud.get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Activo no encontrado")
    return asset

# Crear un nuevo activo
@app.post("/assets", response_model=Asset)
def create_asset(asset: AssetIn, token: str = Depends(auth.get_current_user)):
    new_asset = crud.add_asset(asset)
    return new_asset

# Actualizar un activo existente
@app.put("/assets/{asset_id}", response_model=Asset)
def update_asset(asset_id: int, asset: AssetIn, token: str = Depends(auth.get_current_user)):
    existing_asset = crud.get_asset_by_id(asset_id)
    if not existing_asset:
        raise HTTPException(status_code=404, detail="Activo no encontrado")
    
    # Actualizar el activo con los nuevos datos
    updated_asset = crud.update_asset(asset_id, asset)
    return updated_asset

# Eliminar un activo
@app.delete("/assets/{asset_id}", response_model=Asset)
def delete_asset(asset_id: int, token: str = Depends(auth.get_current_user)):
    asset = crud.get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Activo no encontrado")
    
    # Eliminar el activo
    deleted_asset = crud.delete_asset(asset_id)
    return deleted_asset


@app.post("/users", response_model=dict)
def create_user(user: User):
    """Crea un nuevo usuario"""
    try:
        new_user = crud.add_user(user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{username}", response_model=dict)
def read_user(username: str):
    """Obtiene un usuario por username"""
    user = crud.get_user_by_username(username)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
