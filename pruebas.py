# ============================================================
# pruebas.py
# Pruebas del sistema: cada caso compara el resultado obtenido
# con el resultado esperado y muestra APROBADO o FALLO.
# Ejecutar con:  python pruebas.py
# (Los mensajes [OK] / [ERROR] que aparecen son los que veria el usuario)
# ============================================================

import os
import datos
import inventario
import pedidos
from utilidades import limpiar_texto, soles

resultados = []   # aqui se guarda APROBADO o FALLO de cada caso


def verificar(codigo, descripcion, condicion):
  if condicion:
    estado = "APROBADO"
  else:
    estado = "FALLO"

  resultados.append(estado)
  print(f"{codigo}  {descripcion:<52}{estado}\n")


def datos_base():
  # Productos de ejemplo (codigo, nombre, lote, vencimiento, precio, stock, mal)
  return [[1, "ALERGINA", "59419", "MAY-28", 13.30, 290, 0],
          [2, "ACTERIL", "58983", "ABR-28", 11.00, 1500, 0],
          [3, "BANES FORTE", "67380", "JUN-29", 13.22, 1800, 0]]


# ---------------- INVENTARIO ----------------

productos = datos_base()
ok = inventario.registrar_producto(productos, "Cefinex", "2604103", "Abr-29", 6.85, 3000)
verificar("CP-01", "Registrar producto valido", ok and len(productos) == 4 and productos[3][6] == 0)

productos = datos_base()
ok = inventario.registrar_producto(productos, "alergina", "59419", "May-28", 13.30, 10)
verificar("CP-02", "Rechazar producto y lote duplicados", ok == False and len(productos) == 3)

productos = datos_base()
ok = inventario.registrar_producto(productos, "Nuevo", "111", "Ene-30", 0, 10)
verificar("CP-03", "Rechazar precio no valido (0)", ok == False and len(productos) == 3)

productos = datos_base()
encontrados = inventario.buscar_por_nombre(productos, "ban")
verificar("CP-04", "Busqueda parcial por nombre ('ban')", len(encontrados) == 1 and encontrados[0][1] == "BANES FORTE")

productos = datos_base()
mermas = []
inventario.registrar_mal_estado(productos, mermas, 1, 30, "frasco roto")
verificar("CP-05", "30 en mal estado de 290 -> disponible 260",
          inventario.stock_disponible(productos[0]) == 260 and len(mermas) == 1)

productos = datos_base()
mermas = []
ok = inventario.registrar_mal_estado(productos, mermas, 1, 400, "vencido")
verificar("CP-06", "Rechazar mal estado mayor al stock (400 de 290)",
          ok == False and productos[0][6] == 0 and len(mermas) == 0)

productos = datos_base()
mermas = []
inventario.registrar_mal_estado(productos, mermas, 1, 30, "vencido")
lineas = inventario.lineas_reporte_facturacion(productos, mermas)
verificar("CP-07", "Reporte de facturacion solo con productos danados",
          len(lineas) == 1 and "ALERGINA" in lineas[0])

# ---------------- PEDIDOS ----------------

productos = datos_base()
lista = []
ok = pedidos.crear_pedido(lista, productos, "Farmacia Salud", "Ana", 1, 100)
verificar("CP-08", "Crear pedido valido (100 x 13.30 = 1330.00)",
          ok and lista[0][5] == 1330.00 and productos[0][5] == 190 and lista[0][6] == "REGISTRADO")

productos = datos_base()
lista = []
inventario.registrar_mal_estado(productos, [], 1, 30, "roto")
rechazado = pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 1, 270)
aceptado = pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 1, 260)
verificar("CP-09", "Pedir 270 se rechaza; pedir 260 se acepta", rechazado == False and aceptado == True)

productos = datos_base()
lista = []
ok = pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 99, 1)
verificar("CP-10", "Pedido de producto inexistente", ok == False and len(lista) == 0)

productos = datos_base()
lista = []
pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 1, 5)
ok = pedidos.actualizar_estado(lista, 1, "en preparacion")
verificar("CP-11", "Avanzar estado en orden", ok and lista[0][6] == "EN PREPARACION")

productos = datos_base()
lista = []
pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 1, 5)
ok = pedidos.actualizar_estado(lista, 1, "ENTREGADO")
verificar("CP-12", "Rechazar salto de estado", ok == False and lista[0][6] == "REGISTRADO")

productos = datos_base()
lista = []
pedidos.crear_pedido(lista, productos, "Cliente", "Ana", 1, 5)
ok = pedidos.actualizar_estado(lista, 1, "PERDIDO")
verificar("CP-13", "Rechazar estado inexistente", ok == False and lista[0][6] == "REGISTRADO")

lista = []
verificar("CP-14", "Consultar pedido inexistente (retorna -1)", pedidos.buscar_pedido(lista, 99) == -1)

productos = datos_base()
lista = []
pedidos.crear_pedido(lista, productos, "Farmacia Salud Vida", "Ana", 1, 5)
pedidos.crear_pedido(lista, productos, "Botica Central", "Ana", 2, 5)
encontrados = pedidos.buscar_pedidos_por_cliente(lista, "salud")
verificar("CP-15", "Buscar pedidos por parte del cliente", len(encontrados) == 1)

lista = [[1, "A", "V", 1, 1, 13.30, "REGISTRADO"],
         [2, "B", "V", 1, 3, 39.90, "REGISTRADO"],
         [3, "C", "V", 2, 10, 110.00, "REGISTRADO"]]
rec = pedidos.total_pedidos_recursivo(lista)
ite = pedidos.total_pedidos_iterativo(lista)
verificar("CP-16", "Total recursivo igual al iterativo (163.20)", rec == ite and rec == 163.20)

# ---------------- ARCHIVOS Y CADENAS ----------------

productos = datos_base()
lista = [[1, "CLIENTE", "ANA", 1, 5, 66.5, "REGISTRADO"]]
mermas = [[1, 3, "ROTO"]]
datos.guardar_tabla("prueba_productos.txt", productos)
datos.guardar_tabla("prueba_pedidos.txt", lista)
datos.guardar_tabla("prueba_mermas.txt", mermas)
igual = (datos.cargar_productos("prueba_productos.txt") == productos
         and datos.cargar_pedidos("prueba_pedidos.txt") == lista
         and datos.cargar_mermas("prueba_mermas.txt") == mermas)
verificar("CP-17", "Persistencia: guardar y volver a cargar", igual)

archivo = open("prueba_productos.txt", "w", encoding="utf-8")
archivo.write("1|ALERGINA|59419|MAY-28|13.30|290|0\n")
archivo.write("2|INCOMPLETA|123\n")
archivo.write("3|TEXTO|111|ENE-30|abc|10|0\n")
archivo.close()
cargados = datos.cargar_productos("prueba_productos.txt")
verificar("CP-18", "Archivo con lineas danadas (solo carga la valida)",
          len(cargados) == 1 and cargados[0][1] == "ALERGINA")

verificar("CP-19", "Manejo de cadenas (limpiar y soles)",
          limpiar_texto("  jarabe   tos ") == "JARABE TOS"
          and limpiar_texto("a|b") == "A/B"
          and soles(1234.5) == "S/ 1,234.50")

# Se borran los archivos temporales de las pruebas
for nombre in ["prueba_productos.txt", "prueba_pedidos.txt", "prueba_mermas.txt"]:
  if os.path.exists(nombre):
    os.remove(nombre)

print("=" * 60)
print(f"RESULTADO: {resultados.count('APROBADO')} de {len(resultados)} casos APROBADOS")
print("=" * 60)
