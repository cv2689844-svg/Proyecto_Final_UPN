# ============================================================
# inventario.py
# Productos, productos en mal estado y reporte para facturacion
# productos = lista 2D, cada fila es un producto:
#   [codigo, nombre, lote, vencimiento, precio, stock total, mal estado]
# mermas = lista 2D, cada fila: [codigo, cantidad en mal estado, motivo]
# ============================================================

from utilidades import limpiar_texto, mostrar_titulo, soles

# Posiciones de cada dato dentro de la fila de un producto
COD = 0
NOMBRE = 1
LOTE = 2
VENC = 3
PRECIO = 4
STOCK = 5
MAL = 6


def stock_disponible(producto):
  # Regla central: disponible = stock total - unidades en mal estado
  return producto[STOCK] - producto[MAL]


def buscar_por_codigo(productos, codigo):
  # Retorna la posicion del producto en la lista, o -1 si no existe
  for i in range(len(productos)):
    if productos[i][COD] == codigo:
      return i
  return -1


def siguiente_codigo(productos):
  # El codigo nuevo es el mayor codigo actual + 1
  mayor = 0
  for producto in productos:
    if producto[COD] > mayor:
      mayor = producto[COD]
  return mayor + 1


def registrar_producto(productos, nombre, lote, vencimiento, precio, stock):
  nombre = limpiar_texto(nombre)
  lote = limpiar_texto(lote)
  vencimiento = limpiar_texto(vencimiento)

  if nombre == "" or lote == "":
    print("[ERROR] El nombre y el lote son obligatorios.")
    return False

  for producto in productos:
    if producto[NOMBRE] == nombre and producto[LOTE] == lote:
      print("[ERROR] Ya existe ese producto con el mismo lote.")
      return False

  if precio <= 0:
    print("[ERROR] El precio debe ser mayor a 0.")
    return False

  if stock < 0:
    print("[ERROR] El stock no puede ser negativo.")
    return False

  codigo = siguiente_codigo(productos)
  productos.append([codigo, nombre, lote, vencimiento, precio, stock, 0])
  print(f"[OK] Producto N° {codigo} registrado: {nombre}")
  return True


def mostrar_inventario(productos):
  mostrar_titulo("INVENTARIO")

  if len(productos) == 0:
    print("No hay productos registrados.")
    return

  print(f"{'N°':<4}{'PRODUCTO':<22}{'LOTE':<10}{'VENC.':<8}"
        f"{'PRECIO':>9}{'TOTAL':>8}{'MAL':>6}{'DISPON.':>9}")
  print("-" * 76)

  for p in productos:
    print(f"{p[COD]:<4}{p[NOMBRE]:<22}{p[LOTE]:<10}{p[VENC]:<8}"
          f"{p[PRECIO]:>9.2f}{p[STOCK]:>8}{p[MAL]:>6}{stock_disponible(p):>9}")


def buscar_por_nombre(productos, texto):
  # Busqueda parcial: "ban" encuentra BANES 100 MG y BANES FORTE
  texto = limpiar_texto(texto)
  encontrados = []

  if texto == "":
    return encontrados

  for producto in productos:
    if texto in producto[NOMBRE]:
      encontrados.append(producto)

  return encontrados


def registrar_mal_estado(productos, mermas, codigo, cantidad, motivo):
  # Las unidades siguen en el almacen, pero ya no se pueden vender
  posicion = buscar_por_codigo(productos, codigo)

  if posicion == -1:
    print("[ERROR] Producto no encontrado.")
    return False

  if cantidad <= 0:
    print("[ERROR] La cantidad debe ser mayor a 0.")
    return False

  producto = productos[posicion]
  disponible = stock_disponible(producto)

  if cantidad > disponible:
    print(f"[ERROR] Solo hay {disponible} unidades en buen estado; "
          f"no se pueden reportar {cantidad}.")
    return False

  motivo = limpiar_texto(motivo)
  if motivo == "":
    motivo = "SIN MOTIVO"

  producto[MAL] += cantidad
  mermas.append([producto[COD], cantidad, motivo])

  print(f"[OK] Se registraron {cantidad} unidades en mal estado de "
        f"{producto[NOMBRE]}. Disponibles para facturar: "
        f"{stock_disponible(producto)}")
  return True


def lineas_reporte_facturacion(productos, mermas):
  # Arma una linea de texto por cada producto que tiene unidades en mal estado
  lineas = []

  for producto in productos:
    if producto[MAL] > 0:

      motivos = []
      for merma in mermas:
        if merma[0] == producto[COD]:
          motivos.append(merma[2])

      perdida = producto[MAL] * producto[PRECIO]

      linea = (f"N° {producto[COD]} | {producto[NOMBRE]} | "
               f"Lote {producto[LOTE]} | Vence {producto[VENC]} | "
               f"Mal estado: {producto[MAL]} | "
               f"Facturables: {stock_disponible(producto)} | "
               f"Perdida estimada: {soles(perdida)} | "
               f"Motivo: " + "; ".join(motivos))
      lineas.append(linea)

  return lineas


def mostrar_reporte(lineas):
  mostrar_titulo("REPORTE PARA FACTURACION - PRODUCTOS EN MAL ESTADO")

  if len(lineas) == 0:
    print("No hay productos en mal estado registrados.")

  for linea in lineas:
    print(linea)
