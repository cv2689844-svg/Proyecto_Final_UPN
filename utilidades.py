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



def convertir_entero(texto, permitir_cero=False):
    """Convierte un texto en entero positivo.

    Retorna None si tiene letras, decimales, signo negativo o está vacío.
    Con permitir_cero=True acepta también el 0.
    """
    texto = texto.strip()
    if not (texto.isascii() and texto.isdigit()):
        return None
    valor = int(texto)
    if valor == 0 and not permitir_cero:
        return None
    return valor


def validar_estado(texto):
    """Retorna el estado normalizado si existe en ESTADOS; si no, None."""
    estado = normalizar_texto(texto)
    if estado in ESTADOS:
        return estado
    return None


def mostrar_titulo(titulo):
    """Imprime un título con líneas decorativas (sin retorno)."""
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)

def sumar_recursivo(valores, indice=0):
    """Suma los elementos de una lista de forma recursiva.

    Caso base: si el índice llega al final de la lista, la suma es 0.
    Caso recursivo: valor actual + suma del resto de la lista.
    """
    if indice >= len(valores):
        return 0
    return valores[indice] + sumar_recursivo(valores, indice + 1)

