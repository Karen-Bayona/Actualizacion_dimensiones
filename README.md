# Pipelines de carga y actualización - Laura Franco y Karen Bayona

## Requisitos

- Python 3.10+
- Dependencias:
  ```
  pip install pandas python-dotenv
  ```

## Esquema en estrella

- **DimFecha** — calendario (no se actualiza por pipeline; se carga una sola vez).
- **DimCliente** — `ClienteID, NombreCliente, Genero, RangoEdad, Ciudad, SegmentoCliente`
- **DimTienda** — `TiendaID, NombreTienda, Ciudad, Region, FechaApertura`
- **DimProducto** — `ProductoID, NombreProducto, MarcaProducto, NombreCategoria, NombreProveedor, PaisProveedor, PrecioListado` (desnormalizada, no copo de nieve)
- **VentasFact** — hechos de venta, con FK a las cuatro dimensiones.

## Cómo ejecutar

Desde la raíz del proyecto (`proyecto_final/`):

```bash
python pipeline_cliente.py
python pipeline_tienda.py
python pipeline_producto.py
python pipeline_erp.py        
```

Cada pipeline imprime en consola cuántos registros insertó y cuántos actualizó, por ejemplo:

```
DimCliente -> 2 clientes nuevos insertados, 78 actualizados.
```

## Paso a paso: cómo ejecutarlo (primera vez)

1. **Descomprimir el proyecto** y abrir una terminal dentro de la carpeta `proyecto_final/` (la que contiene `.env`, `pipeline_erp.py`, `utils/`, etc.).

2. **Instalar dependencias** (solo la primera vez):
   ```bash
   pip install pandas python-dotenv
   ```

3. **Ejecutar `pipeline_cliente.py`**:
   ```bash
   python pipeline_cliente.py
   ```
   Debe imprimir algo como:
   ```
   DimCliente -> 0 clientes nuevos insertados, 80 actualizados.
   ```

4. **Ejecutar `pipeline_tienda.py`**:
   ```bash
   python pipeline_tienda.py
   ```
   Debe imprimir:
   ```
   DimTienda -> 0 tiendas nuevas insertadas, 5 actualizadas.
   ```

5. **Ejecutar `pipeline_producto.py`**:
   ```bash
   python pipeline_producto.py
   ```
   Debe imprimir:
   ```
   DimProducto -> 0 productos nuevos insertados, 38 actualizados.
   ```
