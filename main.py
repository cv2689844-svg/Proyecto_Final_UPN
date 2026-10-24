"""Programa principal: menú de consola de Droguerías Unidas del Perú S.A.C."""

import datos
import inventario
import pedidos
from utilidades import (convertir_entero, mostrar_titulo, ESTADOS)

# Con más pedidos que esto se usa la versión iterativa (límite de recursión).
LIMITE_RECURSION = 500


def mostrar_menu():
    """Imprime las opciones del menú (sin retorno)."""
    mostrar_titulo("DROGUERIAS UNIDAS DEL PERU S.A.C. - PEDIDOS Y STOCK")
    print("1. Registrar producto")
    print("2. Ver inventario")
    print("3. Buscar producto por nombre")
    print("4. Registrar productos en mal estado")
    print("5. Reporte de mal estado para facturación")
    print("6. Registrar pedido")
    print("7. Actualizar estado de un pedido")
    print("8. Consultar pedidos")
    print("9. Total acumulado de pedidos")
    print("0. Salir")


def mostrar_resultado(exito, mensaje):
    """Imprime el resultado de una operación (sin retorno)."""
    marca = "[OK]" if exito else "[ERROR]"
    print(f"{marca} {mensaje}")


def leer_entero(mensaje, permitir_cero=False):
    """Pide un número entero. Retorna None si lo ingresado no es válido."""
    return convertir_entero(input(mensaje), permitir_cero)


def opcion_registrar_producto(productos):
    """Pide los datos de un producto nuevo y lo registra."""
    codigo = input("Código (ej. AMO-004): ")
    nombre = input("Nombre: ")
    precio = input("Precio (ej. 12.50): ")
    stock = leer_entero("Stock inicial: ", permitir_cero=True)
    mostrar_resultado(*inventario.registrar_producto(productos, codigo, nombre, precio, stock))


def opcion_ver_inventario(productos):
    """Muestra el inventario completo."""
    inventario.mostrar_inventario(productos)


def opcion_buscar_producto(productos):
    """Busca productos por parte del nombre y los muestra."""
    texto = input("Texto a buscar: ")
    encontrados = inventario.buscar_por_nombre(productos, texto)
    if len(encontrados) == 0:
        print("No se encontraron productos.")
    else:
        inventario.mostrar_inventario(encontrados)


def opcion_mal_estado(productos, mermas):
    """Registra unidades en mal estado de un producto."""
    codigo = input("Código del producto: ")
    cantidad = leer_entero("Cantidad en mal estado: ")
    motivo = input("Motivo (ej. frasco roto, vencido): ")
    mostrar_resultado(*inventario.registrar_mal_estado(productos, mermas, codigo, cantidad, motivo))


def opcion_reporte(productos, mermas):
    """Muestra el reporte para facturación y lo exporta a un archivo."""
    lineas = inventario.lineas_reporte_facturacion(productos, mermas)
    inventario.mostrar_reporte(lineas)
    ruta = datos.exportar_reporte(lineas)
    print(f"Reporte guardado en: {ruta}")


def opcion_crear_pedido(lista_pedidos, productos):
    """Pide los datos de un pedido y lo registra."""
    cliente = input("Cliente: ")
    vendedor = input("Vendedor: ")
    codigo = input("Código del producto: ")
    cantidad = leer_entero("Cantidad: ")
    mostrar_resultado(*pedidos.crear_pedido(lista_pedidos, productos, cliente,
                                            vendedor, codigo, cantidad))


def opcion_actualizar_estado(lista_pedidos):
    """Cambia el estado de un pedido."""
    numero = leer_entero("N° de pedido: ")
    print("Estados:", ", ".join(ESTADOS))
    nuevo = input("Nuevo estado: ")
    mostrar_resultado(*pedidos.actualizar_estado(lista_pedidos, numero, nuevo))


def opcion_consultar_pedido(lista_pedidos):
    """Consulta un pedido por número o por parte del nombre del cliente."""
    print("1. Por número de pedido")
    print("2. Por cliente")
    modo = input("Elija: ").strip()
    if modo == "1":
        posicion = pedidos.buscar_pedido(lista_pedidos, leer_entero("N° de pedido: "))
        if posicion == -1:
            print("[ERROR] Pedido no encontrado.")
        else:
            pedidos.mostrar_pedido(lista_pedidos[posicion])
    elif modo == "2":
        encontrados = pedidos.buscar_pedidos_por_cliente(lista_pedidos, input("Cliente: "))
        if len(encontrados) == 0:
            print("No se encontraron pedidos.")
        for pedido in encontrados:
            pedidos.mostrar_pedido(pedido)
    else:
        print("[ERROR] Opción no válida.")


def opcion_total_pedidos(lista_pedidos):
    """Muestra el total acumulado (recursivo hasta 500 pedidos)."""
    if len(lista_pedidos) <= LIMITE_RECURSION:
        total = pedidos.total_pedidos_recursivo(lista_pedidos)
        metodo = "recursivo"
    else:
        total = pedidos.total_pedidos_iterativo(lista_pedidos)
        metodo = "iterativo"
    print(f"Total acumulado de {len(lista_pedidos)} pedidos: S/ {total:.2f} ({metodo})")


def main():
    """Carga los datos, atiende el menú y guarda tras cada operación."""
    productos, lista_pedidos, mermas = datos.cargar_todo()
    mostrar_menu()
    while True:
        opcion = input("\nOpción (M = ver menú): ").strip().upper()
        if opcion == "M":
            mostrar_menu()
        elif opcion == "0":
            print("Hasta pronto.")
            break
        elif opcion == "1":
            opcion_registrar_producto(productos)
        elif opcion == "2":
            opcion_ver_inventario(productos)
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
            opcion_consultar_pedido(lista_pedidos)
        elif opcion == "9":
            opcion_total_pedidos(lista_pedidos)
        else:
            print("[ERROR] Opción no válida.")
        datos.guardar_todo(productos, lista_pedidos, mermas)


if __name__ == "__main__":
    main()
