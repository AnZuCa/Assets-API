import json
from pathlib import Path
from .models import User, Asset, AssetIn
from datetime import datetime
from .auth import hash_password

USER_DB_FILE = Path(__file__).parent / "database" / "users.json"
ASSET_DB_FILE = Path(__file__).parent / "database" / "assets.json"

def read_user_db():
    if not USER_DB_FILE.exists():
        return []
    with USER_DB_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_user_db(data):
    with USER_DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def read_asset_db():
    if not ASSET_DB_FILE.exists():
        return []
    with ASSET_DB_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def write_asset_db(data):
    with ASSET_DB_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_user_by_username(username: str):
    users = read_user_db()
    for user in users:
        if user["username"] == username:
            return user
    return None

def add_user(user: User) -> dict:
    users = read_user_db()

    # Verificar si el username ya existe
    for existing_user in users:
        if existing_user["username"] == user.username:
            raise ValueError("El nombre de usuario ya está en uso")

    new_user = user.dict()
    new_user["password"] = hash_password(new_user["password"])
    users.append(new_user)
    write_user_db(users)
    return new_user

def get_all_assets(filters: dict) -> list:
    assets =  read_asset_db()
    if filters.get("name"):
        assets = [asset for asset in assets if filters["name"].lower() in asset["name"].lower()]
    
    if filters.get("category"):
        assets = [asset for asset in assets if filters["category"].lower() in asset["category"].lower()]
    
    if filters.get("status"):
        assets = [asset for asset in assets if filters["status"].lower() == asset["status"].lower()]

    if filters.get("min_price") is not None:
        assets = [asset for asset in assets if asset["purchase_price"] >= filters["min_price"]]
    
    if filters.get("max_price") is not None:
        assets = [asset for asset in assets if asset["purchase_price"] <= filters["max_price"]]
    
    return assets

def get_asset_by_id(asset_id: int) -> dict:
    assets = read_asset_db()
    for asset in assets:
        if asset["id"] == asset_id:
            return asset
    return None

def add_asset(asset: AssetIn) -> dict:
    assets = read_asset_db()

    # Calcular nuevo ID automáticamente (evita colisiones)
    new_id = max((a["id"] for a in assets), default=0) + 1

    new_asset = asset.dict()
    new_asset["id"] = new_id
    new_asset["created_at"] = datetime.utcnow().isoformat()

    assets.append(new_asset)
    write_asset_db(assets)
    return new_asset

def update_asset(asset_id: int, asset_data: dict) -> dict:
    """Actualiza un activo en la base de datos."""
    assets = read_asset_db()
    asset = get_asset_by_id(asset_id)
    if asset:
        for key, value in asset_data.items():
            if value is not None:
                asset[key] = value
        write_asset_db(assets)
        return asset
    return None

def delete_asset(asset_id: int) -> bool:
    """Elimina un activo de la base de datos."""
    assets = read_asset_db()
    asset = get_asset_by_id(asset_id)
    if asset:
        assets.remove(asset)
        write_asset_db(assets)
        return True
    return False
