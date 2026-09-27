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
archivo_fuente = os.path.join(ruta_dimensiones, "DIM_CLIENTE.csv")

TABLA = "DimCliente"
COLUMNA_ID = "ClienteID"
COLUMNAS_DIM = ["ClienteID", "NombreCliente", "Genero", "RangoEdad", "Ciudad", "SegmentoCliente"]

clientes = leer_archivo_csv(archivo_fuente, separador=";")

columnas_texto = ["ClienteID", "NombreCliente", "Genero", "RangoEdad", "Ciudad", "SegmentoCliente"]
clientes = eliminar_espacios(clientes, columnas_texto)
clientes = eliminar_duplicados(clientes, ["ClienteID"])

clientes = clientes[COLUMNAS_DIM]

nuevos, actualizados = upsert_dimension_en_db(clientes, TABLA, COLUMNA_ID)

print(f"DimCliente -> {nuevos} clientes nuevos insertados, {actualizados} actualizados.")
