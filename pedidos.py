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



def actualizar_estado(pedidos, id_pedido, nuevo_estado):
    """Cambia el estado de un pedido respetando el orden del flujo.

    Solo se permite avanzar al estado inmediatamente siguiente
    (REGISTRADO -> EN PREPARACION -> DESPACHADO -> ENTREGADO).
    Retorna (exito, mensaje).
    """
    posicion = buscar_pedido(pedidos, id_pedido)
    if posicion == -1:
        return False, "Pedido no encontrado."
    nuevo = validar_estado(nuevo_estado)
    if nuevo is None:
        return False, "Estado no válido. Use: " + ", ".join(ESTADOS) + "."
    actual = pedidos[posicion][ESTADO]
    indice_actual = ESTADOS.index(actual)
    if indice_actual == len(ESTADOS) - 1:
        return False, "El pedido ya fue entregado; no admite más cambios."
    if ESTADOS.index(nuevo) != indice_actual + 1:
        return False, (f"No se puede pasar de {actual} a {nuevo}. "
                       f"El siguiente estado es {ESTADOS[indice_actual + 1]}.")
    pedidos[posicion][ESTADO] = nuevo
    return True, f"Pedido N° {id_pedido:04d} actualizado a {nuevo}."



def buscar_pedidos_por_cliente(pedidos, texto):
    """Búsqueda parcial: retorna los pedidos cuyo cliente contiene el texto."""
    texto = normalizar_texto(texto)
    encontrados = []
    if texto == "":
        return encontrados
    for pedido in pedidos:
        if texto in pedido[CLIENTE]:
            encontrados.append(pedido)
    return encontrados


def linea_avance(estado):
    """Retorna una línea que marca las etapas cumplidas del pedido."""
    cumplidas = ESTADOS.index(estado)
    etapas = []
    for i in range(len(ESTADOS)):
        marca = "X" if i <= cumplidas else " "
        etapas.append(f"[{marca}] {ESTADOS[i]}")
    return " -> ".join(etapas)


def mostrar_pedido(pedido):
    """Imprime el detalle de un pedido y su línea de avance (sin retorno)."""
    mostrar_titulo(f"PEDIDO N° {pedido[ID]:04d}")
    print(f"Cliente : {pedido[CLIENTE]}")
    print(f"Vendedor: {pedido[VENDEDOR]}")
    print(f"Producto: {pedido[PRODUCTO]}  x {pedido[CANTIDAD]} und.")
    print(f"Total   : S/ {pedido[TOTAL]:.2f}")
    print(f"Estado  : {pedido[ESTADO]}")
    print(linea_avance(pedido[ESTADO]))
