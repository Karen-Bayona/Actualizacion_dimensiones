import sqlite3
import pandas as pd
import os
from dotenv import load_dotenv


RUTA_DB = os.getenv("RUTA_DB", "instance")

conn = sqlite3.connect(f'{RUTA_DB}/datacaos_estrella.db')

def _siguiente_numero_venta(con):
    actual = con.execute(
        "SELECT MAX(CAST(SUBSTR(VentaID, 2) AS INTEGER)) FROM VentasFact"
    ).fetchone()[0]
    return actual or 0



def preparar_datos_para_carga(df):
    """
    Prepara los datos para la carga en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a preparar.

    Returns:
        pd.DataFrame: DataFrame preparado para la carga.
    """
    # Aquí puedes agregar cualquier transformación adicional que necesites
    df = df.copy()
    df["FechaID"] = pd.to_datetime(df["Fecha"], format="%Y-%m-%d").dt.strftime("%Y%m%d").astype(int)

    # Genera los consecutivos de VentaID basados en el último número en la base de datos
    siguiente = _siguiente_numero_venta(conn)
    df["VentaID"] = [f"V{str(siguiente + i + 1).zfill(6)}" for i in range(len(df))]

    df = df[["VentaID", "FechaID", "TiendaID", "ProductoID", "ClienteID","Unidades", "PrecioUnitario", "Descuento", "ValorVenta"]]

    return df


def cargar_datos_en_db(df):
    """
    Carga los datos en la base de datos.

    Args:
        df (pd.DataFrame): DataFrame con los datos a cargar.
    """
    df.to_sql("VentasFact", conn, if_exists="append", index=False)
    conn.commit()
    return len(df)


def obtener_ids_existentes(tabla, columna_id):
    """
    Consulta los IDs que ya existen en una tabla de dimensión.

    Args:
        tabla (str): Nombre de la tabla de dimensión (ej. 'DimCliente').
        columna_id (str): Nombre de la columna clave (ej. 'ClienteID').

    Returns:
        set: Conjunto de IDs ya presentes en la tabla.
    """
    cur = conn.execute(f"SELECT {columna_id} FROM {tabla}")
    return {fila[0] for fila in cur.fetchall()}


def upsert_dimension_en_db(df, tabla, columna_id):
    """
    Actualiza una tabla de dimensión a partir de un DataFrame que trae los
    atributos reales de la dimensión (ej. DIM_CLIENTE.csv). Inserta los
    registros nuevos y actualiza los existentes cuyos atributos cambiaron
    (estrategia SCD Tipo 1: se sobrescribe el valor anterior).

    Args:
        df (pd.DataFrame): DataFrame con TODAS las columnas de la tabla
            de dimensión, incluyendo la columna clave.
        tabla (str): Nombre de la tabla de dimensión destino.
        columna_id (str): Nombre de la columna clave de esa dimensión.

    Returns:
        tuple(int, int): (registros nuevos insertados, registros actualizados).
    """
    ids_existentes = obtener_ids_existentes(tabla, columna_id)

    columnas = list(df.columns)
    otras_columnas = [c for c in columnas if c != columna_id]
    placeholders = ", ".join(f":{c}" for c in columnas)
    set_clause = ", ".join(f"{c} = excluded.{c}" for c in otras_columnas)

    sql = f"""
        INSERT INTO {tabla} ({', '.join(columnas)})
        VALUES ({placeholders})
        ON CONFLICT({columna_id}) DO UPDATE SET {set_clause}
    """

    registros = df.to_dict(orient="records")
    conn.executemany(sql, registros)
    conn.commit()

    nuevos = sum(1 for r in registros if r[columna_id] not in ids_existentes)
    actualizados = len(registros) - nuevos
    return nuevos, actualizados
