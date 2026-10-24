# ============================================================
# pedidos.py
# Registro de pedidos, seguimiento de estados y consultas
# pedidos = lista 2D, cada fila es un pedido:
#   [numero, cliente, vendedor, codigo producto, cantidad, total, estado]
# ============================================================

from utilidades import limpiar_texto, mostrar_titulo, soles, sumar_recursivo, ESTADOS
from inventario import buscar_por_codigo, stock_disponible, NOMBRE, PRECIO, STOCK

# Posiciones de cada dato dentro de la fila de un pedido
NUMERO = 0
CLIENTE = 1
VENDEDOR = 2
PRODUCTO = 3
CANTIDAD = 4
TOTAL = 5
ESTADO = 6

IGV = 0.18


def siguiente_numero(pedidos):
  # El numero nuevo es el mayor numero actual + 1
  mayor = 0
  for pedido in pedidos:
    if pedido[NUMERO] > mayor:
      mayor = pedido[NUMERO]
  return mayor + 1


def buscar_pedido(pedidos, numero):
  # Retorna la posicion del pedido en la lista, o -1 si no existe
  for i in range(len(pedidos)):
    if pedidos[i][NUMERO] == numero:
      return i
  return -1


def crear_pedido(pedidos, productos, cliente, vendedor, codigo, cantidad):
  cliente = limpiar_texto(cliente)
  vendedor = limpiar_texto(vendedor)

  if cliente == "" or vendedor == "":
    print("[ERROR] El cliente y el vendedor son obligatorios.")
    return False

  posicion = buscar_por_codigo(productos, codigo)

  if posicion == -1:
    print("[ERROR] Producto no encontrado.")
    return False

  if cantidad <= 0:
    print("[ERROR] La cantidad debe ser mayor a 0.")
    return False

  producto = productos[posicion]
  disponible = stock_disponible(producto)

  # Solo se pueden pedir unidades en buen estado
  if cantidad > disponible:
    print(f"[ERROR] Stock insuficiente: solo hay {disponible} unidades "
          f"aptas para la venta.")
    return False

  producto[STOCK] -= cantidad
  total = round(cantidad * producto[PRECIO], 2)
  numero = siguiente_numero(pedidos)

  pedidos.append([numero, cliente, vendedor, codigo, cantidad, total, ESTADOS[0]])

  print(f"[OK] Pedido N° {numero:04d} registrado. Total: {soles(total)}")
  return True


def actualizar_estado(pedidos, numero, nuevo_estado):
  # Solo se puede avanzar al estado siguiente:
  # REGISTRADO -> EN PREPARACION -> DESPACHADO -> ENTREGADO
  posicion = buscar_pedido(pedidos, numero)

  if posicion == -1:
    print("[ERROR] Pedido no encontrado.")
    return False

  nuevo_estado = limpiar_texto(nuevo_estado)

  if nuevo_estado not in ESTADOS:
    print("[ERROR] Estado no valido. Use: " + ", ".join(ESTADOS))
    return False

  actual = pedidos[posicion][ESTADO]
  indice_actual = ESTADOS.index(actual)

  if indice_actual == len(ESTADOS) - 1:
    print("[ERROR] El pedido ya fue entregado; no admite mas cambios.")
    return False

  if ESTADOS.index(nuevo_estado) != indice_actual + 1:
    print(f"[ERROR] No se puede pasar de {actual} a {nuevo_estado}. "
          f"El siguiente estado es {ESTADOS[indice_actual + 1]}.")
    return False

  pedidos[posicion][ESTADO] = nuevo_estado
  print(f"[OK] Pedido N° {numero:04d} actualizado a {nuevo_estado}")
  return True


def buscar_pedidos_por_cliente(pedidos, texto):
  # Busqueda parcial por el nombre del cliente
  texto = limpiar_texto(texto)
  encontrados = []

  if texto == "":
    return encontrados

  for pedido in pedidos:
    if texto in pedido[CLIENTE]:
      encontrados.append(pedido)

  return encontrados


def linea_avance(estado):
  # Marca con X las etapas que el pedido ya cumplio
  cumplidas = ESTADOS.index(estado)
  texto = ""

  for i in range(len(ESTADOS)):
    if i <= cumplidas:
      marca = "X"
    else:
      marca = " "

    texto += f"[{marca}] {ESTADOS[i]}"
    if i < len(ESTADOS) - 1:
      texto += " -> "

  return texto


def mostrar_pedido(pedido, productos):
  posicion = buscar_por_codigo(productos, pedido[PRODUCTO])
  if posicion == -1:
    nombre_producto = "(producto no encontrado)"
  else:
    nombre_producto = productos[posicion][NOMBRE]

  # Mismo calculo que en registrar_venta de clase: base imponible e IGV
  total = pedido[TOTAL]
  base = total / (1 + IGV)
  igv = total - base

  mostrar_titulo(f"PEDIDO N° {pedido[NUMERO]:04d}")
  print("Cliente :", pedido[CLIENTE])
  print("Vendedor:", pedido[VENDEDOR])
  print("Producto:", nombre_producto, "- Cantidad:", pedido[CANTIDAD])
  print("----------------------")
  print("Base imponible:", soles(base))
  print("IGV (18%):     ", soles(igv))
  print("Total:         ", soles(total))
  print("----------------------")
  print("Estado:", pedido[ESTADO])
  print(linea_avance(pedido[ESTADO]))


def total_pedidos_recursivo(pedidos):
  # Total acumulado de los pedidos usando recursividad
  totales = []
  for pedido in pedidos:
    totales.append(pedido[TOTAL])

  return round(sumar_recursivo(totales), 2)


def total_pedidos_iterativo(pedidos):
  # Mismo total con un ciclo for (mas eficiente)
  suma = 0
  for pedido in pedidos:
    suma += pedido[TOTAL]

  return round(suma, 2)
