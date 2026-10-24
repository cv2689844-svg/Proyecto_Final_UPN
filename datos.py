# ============================================================
# datos.py
# Persistencia: guardar y cargar la informacion en archivos de texto
# Cada linea del archivo es una fila; los campos se separan con '|'
# ============================================================

NOMBRE_PRODUCTOS = "productos.txt"
NOMBRE_PEDIDOS = "pedidos.txt"
NOMBRE_MERMAS = "mermas.txt"
NOMBRE_REPORTE = "reporte_facturacion.txt"


def guardar_tabla(nombre, tabla):
  # Escribe una lista 2D en un archivo: una fila por linea
  archivo = open(nombre, "w", encoding="utf-8")

  for fila in tabla:
    campos = []
    for campo in fila:
      campos.append(str(campo))
    archivo.write("|".join(campos) + "\n")

  archivo.close()


def leer_lineas(nombre):
  # Retorna las lineas utiles del archivo (sin vacias ni comentarios #)
  lineas = []

  try:
    archivo = open(nombre, "r", encoding="utf-8")
  except FileNotFoundError:
    return lineas   # si el archivo no existe, la tabla queda vacia

  for linea in archivo:
    linea = linea.strip()
    if linea != "" and not linea.startswith("#"):
      lineas.append(linea)

  archivo.close()
  return lineas


def cargar_productos(nombre=NOMBRE_PRODUCTOS):
  # Fila: codigo | nombre | lote | vencimiento | precio | stock | mal estado
  productos = []

  for linea in leer_lineas(nombre):
    campos = linea.split("|")

    if len(campos) == 7:
      try:
        fila = [int(campos[0]), campos[1], campos[2], campos[3],
                float(campos[4]), int(campos[5]), int(campos[6])]
        productos.append(fila)
      except ValueError:
        pass   # linea danada: se ignora para que el programa no se caiga

  return productos


def cargar_pedidos(nombre=NOMBRE_PEDIDOS):
  # Fila: numero | cliente | vendedor | codigo producto | cantidad | total | estado
  pedidos = []

  for linea in leer_lineas(nombre):
    campos = linea.split("|")

    if len(campos) == 7:
      try:
        fila = [int(campos[0]), campos[1], campos[2], int(campos[3]),
                int(campos[4]), float(campos[5]), campos[6]]
        pedidos.append(fila)
      except ValueError:
        pass

  return pedidos


def cargar_mermas(nombre=NOMBRE_MERMAS):
  # Fila: codigo producto | cantidad en mal estado | motivo
  mermas = []

  for linea in leer_lineas(nombre):
    campos = linea.split("|")

    if len(campos) == 3:
      try:
        fila = [int(campos[0]), int(campos[1]), campos[2]]
        mermas.append(fila)
      except ValueError:
        pass

  return mermas


def guardar_todo(productos, pedidos, mermas):
  # Guarda las tres tablas (se llama despues de cada operacion)
  guardar_tabla(NOMBRE_PRODUCTOS, productos)
  guardar_tabla(NOMBRE_PEDIDOS, pedidos)
  guardar_tabla(NOMBRE_MERMAS, mermas)


def exportar_reporte(lineas):
  # Guarda el reporte de facturacion en un archivo de texto
  archivo = open(NOMBRE_REPORTE, "w", encoding="utf-8")
  archivo.write("REPORTE DE PRODUCTOS EN MAL ESTADO PARA FACTURACION\n")

  for linea in lineas:
    archivo.write(linea + "\n")

  archivo.close()
