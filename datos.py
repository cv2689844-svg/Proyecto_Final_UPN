"""Persistencia: lectura y escritura de tablas en archivos de texto."""

import os

from utilidades import segmentar_linea

# Carpeta donde se guardan los archivos (la misma del programa).
CARPETA = os.path.dirname(os.path.abspath(__file__))
SEPARADOR = "|"


def _ruta(nombre):
    """Retorna la ruta completa de un archivo de datos."""
    return os.path.join(CARPETA, nombre)


def cargar_tabla(nombre, tipos):
    """Lee un archivo y retorna una lista bidimensional (una fila por línea).

    Si el archivo no existe retorna []. Las líneas vacías, los comentarios (#)
    y las líneas corruptas se ignoran para que el sistema no se caiga.
    """
    tabla = []
    ruta = _ruta(nombre)
    if not os.path.exists(ruta):
        return tabla
    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            if linea.strip() == "" or linea.startswith("#"):
                continue
            campos = segmentar_linea(linea)
            if len(campos) != len(tipos):
                continue
            try:
                fila = [tipo(campo) for tipo, campo in zip(tipos, campos)]
            except ValueError:
                continue
            tabla.append(fila)
    return tabla


def guardar_tabla(nombre, tabla, encabezado=""):
    """Escribe una lista bidimensional en un archivo, una fila por línea."""
    with open(_ruta(nombre), "w", encoding="utf-8") as archivo:
        if encabezado != "":
            archivo.write("# " + encabezado + "\n")
        for fila in tabla:
            archivo.write(SEPARADOR.join(str(campo) for campo in fila) + "\n")



# Archivos y tipos de cada campo.
ARCHIVO_PRODUCTOS = "productos.txt"
ARCHIVO_PEDIDOS = "pedidos.txt"
ARCHIVO_MERMAS = "mermas.txt"
ARCHIVO_REPORTE = "reporte_facturacion.txt"

TIPOS_PRODUCTOS = [str, str, float, int, int]
TIPOS_PEDIDOS = [int, str, str, str, int, float, str]
TIPOS_MERMAS = [str, int, str, str]


def cargar_productos():
    """Retorna la lista 2D de productos guardada en disco."""
    return cargar_tabla(ARCHIVO_PRODUCTOS, TIPOS_PRODUCTOS)


def cargar_pedidos():
    """Retorna la lista 2D de pedidos guardada en disco."""
    return cargar_tabla(ARCHIVO_PEDIDOS, TIPOS_PEDIDOS)


def cargar_mermas():
    """Retorna la lista 2D de productos en mal estado guardada en disco."""
    return cargar_tabla(ARCHIVO_MERMAS, TIPOS_MERMAS)


def cargar_todo():
    """Carga las tres tablas y las retorna como (productos, pedidos, mermas)."""
    return cargar_productos(), cargar_pedidos(), cargar_mermas()


def guardar_todo(productos, pedidos, mermas):
    """Guarda las tres tablas en sus archivos (sin retorno)."""
    guardar_tabla(ARCHIVO_PRODUCTOS, productos,
                  "codigo|nombre|precio|stock_total|mal_estado")
    guardar_tabla(ARCHIVO_PEDIDOS, pedidos,
                  "numero|cliente|vendedor|codigo|cantidad|total|estado")
    guardar_tabla(ARCHIVO_MERMAS, mermas,
                  "codigo|cantidad|motivo|fecha")


def exportar_reporte(lineas):
    """Escribe el reporte de facturación en un archivo de texto.

    Retorna la ruta del archivo generado.
    """
    ruta = _ruta(ARCHIVO_REPORTE)
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("REPORTE DE PRODUCTOS EN MAL ESTADO PARA FACTURACION\n")
        for linea in lineas:
            archivo.write(linea + "\n")
    return ruta
