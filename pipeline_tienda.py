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
archivo_fuente = os.path.join(ruta_dimensiones, "DIM_TIENDA.csv")

TABLA = "DimTienda"
COLUMNA_ID = "TiendaID"
COLUMNAS_DIM = ["TiendaID", "NombreTienda", "Ciudad", "Region", "FechaApertura"]

tiendas = leer_archivo_csv(archivo_fuente, separador=";")

columnas_texto = ["TiendaID", "NombreTienda", "Ciudad", "Region"]
tiendas = eliminar_espacios(tiendas, columnas_texto)
tiendas = eliminar_duplicados(tiendas, ["TiendaID"])

tiendas = tiendas[COLUMNAS_DIM]

nuevos, actualizados = upsert_dimension_en_db(tiendas, TABLA, COLUMNA_ID)

print(f"DimTienda -> {nuevos} tiendas nuevas insertadas, {actualizados} actualizadas.")
