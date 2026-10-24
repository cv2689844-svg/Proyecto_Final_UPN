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

def registrar_mal_estado(productos, mermas, codigo, cantidad, motivo):
    """Registra unidades en mal estado de un producto.

    Las unidades siguen en el almacén pero dejan de estar disponibles para
    la venta. Se guarda el motivo en la lista de mermas. Retorna (exito, mensaje).
    """
    posicion = buscar_por_codigo(productos, codigo)
    if posicion == -1:
        return False, "Producto no encontrado."
    if cantidad is None or cantidad <= 0:
        return False, "La cantidad debe ser un número entero positivo."
    producto = productos[posicion]
    disponible = stock_disponible(producto)
    if cantidad > disponible:
        return False, (f"Solo hay {disponible} unidades en buen estado; "
                       f"no se pueden reportar {cantidad}.")
    motivo = normalizar_texto(motivo).replace("|", "/")  # '|' es el separador
    if motivo == "":
        motivo = "SIN MOTIVO"
    producto[MAL] += cantidad
    mermas.append([producto[COD], cantidad, motivo, date.today().isoformat()])
    return True, (f"Se registraron {cantidad} unidades en mal estado de "
                  f"{producto[NOMBRE]}. Disponibles para facturar: "
                  f"{stock_disponible(producto)}.")



def lineas_reporte_facturacion(productos, mermas):
    """Arma el reporte de productos en mal estado para el área de facturación.

    Retorna una lista de líneas de texto (una por producto con mal estado).
    """
    lineas = []
    for producto in productos:
        if producto[MAL] > 0:
            motivos = []
            for merma in mermas:
                if merma[0] == producto[COD]:
                    motivos.append(merma[2])
            perdida = round(producto[MAL] * producto[PRECIO], 2)
            lineas.append(
                f"{producto[COD]} | {producto[NOMBRE]} | "
                f"Mal estado: {producto[MAL]} | "
                f"Facturables: {stock_disponible(producto)} | "
                f"Perdida estimada: S/ {perdida:.2f} | "
                f"Motivo: {'; '.join(motivos)}")
    return lineas


def mostrar_reporte(lineas):
    """Imprime el reporte de facturación en pantalla (sin retorno)."""
    mostrar_titulo("REPORTE PARA FACTURACION - PRODUCTOS EN MAL ESTADO")
    if len(lineas) == 0:
        print("No hay productos en mal estado registrados.")
    for linea in lineas:
        print(linea)

        
