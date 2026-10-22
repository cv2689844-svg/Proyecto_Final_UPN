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
