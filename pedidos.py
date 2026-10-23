"""Pedidos: registro, seguimiento de estados y consultas."""

from utilidades import normalizar_texto, validar_estado, ESTADOS, mostrar_titulo
from inventario import buscar_por_codigo, stock_disponible, STOCK, PRECIO

# Posiciones de cada campo dentro de una fila de pedido.
ID, CLIENTE, VENDEDOR, PRODUCTO, CANTIDAD, TOTAL, ESTADO = range(7)


def siguiente_id(pedidos):
    """Retorna el número del próximo pedido (máximo actual + 1)."""
    mayor = 0
    for pedido in pedidos:
        if pedido[ID] > mayor:
            mayor = pedido[ID]
    return mayor + 1


def buscar_pedido(pedidos, id_pedido):
    """Busca un pedido por su número. Retorna su posición o -1."""
    for posicion in range(len(pedidos)):
        if pedidos[posicion][ID] == id_pedido:
            return posicion
    return -1


def crear_pedido(pedidos, productos, cliente, vendedor, codigo, cantidad):
    """Registra un pedido y descuenta las unidades del stock.

    Solo se pueden pedir unidades en buen estado. Retorna (exito, mensaje).
    """
    cliente = normalizar_texto(cliente).replace("|", "/")
    vendedor = normalizar_texto(vendedor).replace("|", "/")
    if cliente == "" or vendedor == "":
        return False, "El cliente y el vendedor son obligatorios."
    posicion = buscar_por_codigo(productos, codigo)
    if posicion == -1:
        return False, "Producto no encontrado."
    if cantidad is None or cantidad <= 0:
        return False, "La cantidad debe ser un número entero positivo."
    producto = productos[posicion]
    disponible = stock_disponible(producto)
    if cantidad > disponible:
        return False, (f"Stock insuficiente: solo hay {disponible} unidades "
                       f"aptas para la venta.")
    producto[STOCK] -= cantidad
    total = round(cantidad * producto[PRECIO], 2)
    numero = siguiente_id(pedidos)
    pedidos.append([numero, cliente, vendedor, producto[0], cantidad, total, ESTADOS[0]])
    return True, f"Pedido N° {numero:04d} registrado. Total: S/ {total:.2f}"
