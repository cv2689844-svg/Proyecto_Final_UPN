# ============================================================
# DROGUERIAS UNIDAS DEL PERU S.A.C.
# SISTEMA DE GESTION DE PEDIDOS Y CONTROL DE STOCK
# main.py: menu principal (es el unico modulo que habla con el usuario)
# ============================================================

import datos
import inventario
import pedidos
from utilidades import (leer_entero, leer_decimal, leer_texto,
                        mostrar_titulo, soles, ESTADOS)

# Con mas pedidos que este limite se usa el total iterativo,
# porque Python limita la profundidad de la recursividad
LIMITE_RECURSION = 500


def mostrar_menu():
  mostrar_titulo("DROGUERIAS UNIDAS DEL PERU S.A.C.")
  print("1. Registrar producto")
  print("2. Ver inventario")
  print("3. Buscar producto por nombre")
  print("4. Registrar productos en mal estado")
  print("5. Reporte de mal estado para facturacion")
  print("6. Registrar pedido")
  print("7. Actualizar estado de un pedido")
  print("8. Consultar pedidos")
  print("9. Total acumulado de pedidos")
  print("0. Salir")


def opcion_registrar_producto(productos):
  print("\n--- REGISTRAR PRODUCTO ---")
  nombre = leer_texto("Nombre del producto: ")
  lote = leer_texto("Lote: ")
  vencimiento = leer_texto("Vencimiento (ejemplo MAY-28): ")
  precio = leer_decimal("Precio unitario (S/): ", 0.01)
  stock = leer_entero("Stock inicial: ", 0)

  inventario.registrar_producto(productos, nombre, lote, vencimiento, precio, stock)


def opcion_buscar_producto(productos):
  texto = leer_texto("Texto a buscar en el nombre: ")
  encontrados = inventario.buscar_por_nombre(productos, texto)

  if len(encontrados) == 0:
    print("No se encontraron productos.")
  else:
    inventario.mostrar_inventario(encontrados)


def opcion_mal_estado(productos, mermas):
  print("\n--- REGISTRAR PRODUCTOS EN MAL ESTADO ---")
  codigo = leer_entero("N° del producto: ", 1)
  cantidad = leer_entero("Cantidad en mal estado: ", 1)
  motivo = input("Motivo (ejemplo: frasco roto, vencido): ")

  inventario.registrar_mal_estado(productos, mermas, codigo, cantidad, motivo)


def opcion_reporte(productos, mermas):
  lineas = inventario.lineas_reporte_facturacion(productos, mermas)
  inventario.mostrar_reporte(lineas)
  datos.exportar_reporte(lineas)
  print("Reporte guardado en:", datos.NOMBRE_REPORTE)


def opcion_crear_pedido(lista_pedidos, productos):
  print("\n--- REGISTRAR PEDIDO ---")
  cliente = leer_texto("Cliente: ")
  vendedor = leer_texto("Vendedor: ")
  codigo = leer_entero("N° del producto: ", 1)
  cantidad = leer_entero("Cantidad: ", 1)

  pedidos.crear_pedido(lista_pedidos, productos, cliente, vendedor, codigo, cantidad)


def opcion_actualizar_estado(lista_pedidos):
  print("\n--- ACTUALIZAR ESTADO ---")
  numero = leer_entero("N° de pedido: ", 1)
  print("Estados:", ", ".join(ESTADOS))
  nuevo_estado = input("Nuevo estado: ")

  pedidos.actualizar_estado(lista_pedidos, numero, nuevo_estado)


def opcion_consultar_pedido(lista_pedidos, productos):
  print("\n--- CONSULTAR PEDIDOS ---")
  print("1. Por numero de pedido")
  print("2. Por cliente")
  modo = input("Seleccione una opcion: ").strip()

  if modo == "1":
    numero = leer_entero("N° de pedido: ", 1)
    posicion = pedidos.buscar_pedido(lista_pedidos, numero)

    if posicion == -1:
      print("[ERROR] Pedido no encontrado.")
    else:
      pedidos.mostrar_pedido(lista_pedidos[posicion], productos)

  elif modo == "2":
    texto = leer_texto("Cliente (puede ser parte del nombre): ")
    encontrados = pedidos.buscar_pedidos_por_cliente(lista_pedidos, texto)

    if len(encontrados) == 0:
      print("No se encontraron pedidos.")

    for pedido in encontrados:
      pedidos.mostrar_pedido(pedido, productos)

  else:
    print("Opcion invalida.")


def opcion_total_pedidos(lista_pedidos):
  if len(lista_pedidos) <= LIMITE_RECURSION:
    total = pedidos.total_pedidos_recursivo(lista_pedidos)
    metodo = "calculo recursivo"
  else:
    total = pedidos.total_pedidos_iterativo(lista_pedidos)
    metodo = "calculo iterativo"

  print(f"Total acumulado de {len(lista_pedidos)} pedidos: {soles(total)} ({metodo})")


def menu():
  # Al iniciar se cargan los datos guardados en los archivos
  productos = datos.cargar_productos()
  lista_pedidos = datos.cargar_pedidos()
  mermas = datos.cargar_mermas()

  while True:
    mostrar_menu()
    opcion = input("Seleccione una opcion: ").strip()

    if opcion == "1":
      opcion_registrar_producto(productos)
    elif opcion == "2":
      inventario.mostrar_inventario(productos)
    elif opcion == "3":
      opcion_buscar_producto(productos)
    elif opcion == "4":
      opcion_mal_estado(productos, mermas)
    elif opcion == "5":
      opcion_reporte(productos, mermas)
    elif opcion == "6":
      opcion_crear_pedido(lista_pedidos, productos)
    elif opcion == "7":
      opcion_actualizar_estado(lista_pedidos)
    elif opcion == "8":
      opcion_consultar_pedido(lista_pedidos, productos)
    elif opcion == "9":
      opcion_total_pedidos(lista_pedidos)
    elif opcion == "0":
      print("Gracias por utilizar el sistema.")
      break
    else:
      print("Opcion invalida.")

    # Despues de cada operacion se guarda todo en los archivos
    datos.guardar_todo(productos, lista_pedidos, mermas)


menu()
