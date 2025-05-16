# 📦 Inventario de Activos API

API REST sencilla construida con [FastAPI](https://fastapi.tiangolo.com/) para gestionar un inventario de activos.  
Guarda los datos en un archivo JSON (`assets.json`).

---

## 🚀 Requisitos

- Python 3.8 o superior
- pip

---

## 🛠️ Crear y activar un entorno virtual

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

## Ejecutar api
uvicorn app.main:app --reload