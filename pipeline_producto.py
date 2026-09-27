import os
from dotenv import load_dotenv

from utils.reglas import (
    leer_archivo_csv,
    eliminar_duplicados,
    eliminar_espacios,
)
from db_utils.load import upsert_dimension_en_db

load_dotenv()

ruta_dimensiones = os.getenv("RUTA_DIMENSIONES", "csvs_dimensiones")
archivo_fuente = os.path.join(ruta_dimensiones, "DIM_PRODUCTO.csv")

TABLA = "DimProducto"
COLUMNA_ID = "ProductoID"
COLUMNAS_DIM = [
    "ProductoID",
    "NombreProducto",
    "MarcaProducto",
    "NombreCategoria",
    "NombreProveedor",
    "PaisProveedor",
    "PrecioListado",
]

productos = leer_archivo_csv(archivo_fuente, separador=";")

columnas_texto = ["ProductoID", "NombreProducto", "MarcaProducto", "NombreCategoria", "NombreProveedor", "PaisProveedor"]
productos = eliminar_espacios(productos, columnas_texto)
productos = eliminar_duplicados(productos, ["ProductoID"])


productos["PrecioListado"] = (
    productos["PrecioListado"].astype(str).str.replace(",", ".", regex=False).astype(float)
)

productos = productos[COLUMNAS_DIM]

nuevos, actualizados = upsert_dimension_en_db(productos, TABLA, COLUMNA_ID)

print(f"DimProducto -> {nuevos} productos nuevos insertados, {actualizados} actualizados.")
