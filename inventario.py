"""Inventario: productos, búsquedas, productos en mal estado y reporte."""

from datetime import date

from utilidades import (normalizar_texto, convertir_precio, mostrar_titulo)

# Posiciones de cada campo dentro de una fila de producto.
COD, NOMBRE, PRECIO, STOCK, MAL = 0, 1, 2, 3, 4


def stock_disponible(producto):
    """Retorna las unidades aptas para la venta: stock total - mal estado."""
    return producto[STOCK] - producto[MAL]


def buscar_por_codigo(productos, codigo):
    """Busca un producto por código exacto. Retorna su posición o -1."""
    codigo = normalizar_texto(codigo)
    for posicion in range(len(productos)):
        if productos[posicion][COD] == codigo:
            return posicion
    return -1


def registrar_producto(productos, codigo, nombre, precio_texto, stock):
    """Agrega un producto nuevo con 0 unidades en mal estado.

    Retorna (exito, mensaje).
    """
    codigo = normalizar_texto(codigo).replace("|", "/")
    nombre = normalizar_texto(nombre).replace("|", "/")
    if codigo == "" or nombre == "":
        return False, "El código y el nombre son obligatorios."
    if buscar_por_codigo(productos, codigo) != -1:
        return False, f"Ya existe un producto con el código {codigo}."
    precio = convertir_precio(precio_texto)
    if precio is None:
        return False, "El precio no es válido (use un número mayor a 0)."
    if stock is None or stock < 0:
        return False, "El stock debe ser un número entero (0 o más)."
    productos.append([codigo, nombre, precio, stock, 0])
    return True, f"Producto {codigo} registrado correctamente."


def mostrar_inventario(productos):
    """Imprime una tabla con el inventario (sin retorno)."""
    mostrar_titulo("INVENTARIO")
    if len(productos) == 0:
        print("No hay productos registrados.")
        return
    print(f"{'CODIGO':<9}{'PRODUCTO':<32}{'PRECIO':>8}{'TOTAL':>8}"
          f"{'MAL':>6}{'DISPON.':>9}")
    for p in productos:
        print(f"{p[COD]:<9}{p[NOMBRE]:<32}{p[PRECIO]:>8.2f}{p[STOCK]:>8}"
              f"{p[MAL]:>6}{stock_disponible(p):>9}")



def buscar_por_nombre(productos, texto):
    """Búsqueda parcial: retorna los productos cuyo nombre contiene el texto."""
    texto = normalizar_texto(texto)
    encontrados = []
    if texto == "":
        return encontrados
    for producto in productos:
        if texto in producto[NOMBRE]:
            encontrados.append(producto)
    return encontrados
