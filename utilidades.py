"""Utilidades del sistema: manejo de cadenas, validaciones y recursividad."""

import math

# Estados del pedido, en el orden del flujo (lista unidimensional).
ESTADOS = ["REGISTRADO", "EN PREPARACION", "DESPACHADO", "ENTREGADO"]


def normalizar_texto(texto):
    """Quita espacios sobrantes y pasa el texto a mayúsculas.

    Ejemplo: '  jarabe   tos ' -> 'JARABE TOS'. Retorna la cadena limpia.
    """
    return " ".join(texto.split()).upper()


def convertir_precio(texto):
    """Convierte un texto como 'S/ 12,50' en el número 12.5.

    Usa replace para quitar 'S/' y cambiar la coma por punto.
    Retorna None si el texto no es un precio válido (o es <= 0).
    """
    limpio = texto.upper().replace("S/", "").replace(" ", "").replace(",", ".")
    try:
        precio = float(limpio)
    except ValueError:
        return None
    if not math.isfinite(precio) or precio <= 0:
        return None
    return round(precio, 2)


def segmentar_linea(linea):
    """Separa una línea del archivo en campos usando '|' (split).

    Retorna una lista de campos sin espacios en los extremos.
    """
    return [campo.strip() for campo in linea.strip().split("|")]
