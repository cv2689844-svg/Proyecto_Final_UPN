"""Pruebas automáticas (unittest). Ejecutar con: python pruebas.py"""

import os
import tempfile
import unittest

import datos
import inventario as inv
import pedidos as ped
import utilidades as util


def datos_base():
    """Crea productos de ejemplo: 500 jarabes y 1000 paracetamoles."""
    return [["JAR-001", "JARABE PARA LA TOS", 12.5, 500, 0],
            ["PAR-002", "PARACETAMOL 500 MG", 1.2, 1000, 0]]


class PruebasInventario(unittest.TestCase):
    def setUp(self):
        self.productos = datos_base()
        self.mermas = []

    def test_cp01_registrar_producto_valido(self):
        ok, _ = inv.registrar_producto(self.productos, "AMO-004", "Amoxicilina", "32.00", 150)
        self.assertTrue(ok)
        self.assertEqual(self.productos[-1], ["AMO-004", "AMOXICILINA", 32.0, 150, 0])

    def test_cp02_codigo_duplicado(self):
        ok, _ = inv.registrar_producto(self.productos, "JAR-001", "Otro", "5", 10)
        self.assertFalse(ok)
        self.assertEqual(len(self.productos), 2)

    def test_cp03_precio_no_numerico(self):
        ok, _ = inv.registrar_producto(self.productos, "X-1", "Otro", "abc", 10)
        self.assertFalse(ok)
        self.assertEqual(len(self.productos), 2)

    def test_cp04_busqueda_parcial(self):
        encontrados = inv.buscar_por_nombre(self.productos, "jarabe")
        self.assertEqual([p[0] for p in encontrados], ["JAR-001"])

    def test_cp05_treinta_en_mal_estado(self):
        ok, _ = inv.registrar_mal_estado(self.productos, self.mermas, "JAR-001", 30, "frasco roto")
        self.assertTrue(ok)
        self.assertEqual(inv.stock_disponible(self.productos[0]), 470)
        self.assertEqual(len(self.mermas), 1)

    def test_cp06_mal_estado_mayor_al_stock(self):
        ok, _ = inv.registrar_mal_estado(self.productos, self.mermas, "JAR-001", 600, "x")
        self.assertFalse(ok)
        self.assertEqual(self.productos[0][inv.MAL], 0)
        self.assertEqual(self.mermas, [])

    def test_cp07_reporte_facturacion(self):
        inv.registrar_mal_estado(self.productos, self.mermas, "JAR-001", 30, "vencido")
        lineas = inv.lineas_reporte_facturacion(self.productos, self.mermas)
        self.assertEqual(len(lineas), 1)
        self.assertIn("JAR-001", lineas[0])


class PruebasPedidos(unittest.TestCase):
    def setUp(self):
        self.productos = datos_base()
        self.lista = []

    def test_cp08_crear_pedido_valido(self):
        ok, _ = ped.crear_pedido(self.lista, self.productos, "Farmacia Salud", "Ana", "JAR-001", 100)
        self.assertTrue(ok)
        self.assertEqual(self.lista[0][ped.TOTAL], 1250.00)
        self.assertEqual(self.productos[0][inv.STOCK], 400)
        self.assertEqual(self.lista[0][ped.ESTADO], "REGISTRADO")

    def test_cp09_pedido_excede_unidades_aptas(self):
        inv.registrar_mal_estado(self.productos, [], "JAR-001", 30, "roto")
        ok, _ = ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "JAR-001", 480)
        self.assertFalse(ok)
        ok, _ = ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "JAR-001", 470)
        self.assertTrue(ok)

    def test_cp10_producto_inexistente(self):
        ok, _ = ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "XXX-999", 1)
        self.assertFalse(ok)
        self.assertEqual(self.lista, [])

    def test_cp11_avanzar_estado_en_orden(self):
        ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "JAR-001", 5)
        ok, _ = ped.actualizar_estado(self.lista, 1, "en preparacion")
        self.assertTrue(ok)
        self.assertEqual(self.lista[0][ped.ESTADO], "EN PREPARACION")

    def test_cp12_rechazar_salto_de_estado(self):
        ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "JAR-001", 5)
        ok, _ = ped.actualizar_estado(self.lista, 1, "ENTREGADO")
        self.assertFalse(ok)
        self.assertEqual(self.lista[0][ped.ESTADO], "REGISTRADO")

    def test_cp13_estado_inexistente(self):
        ped.crear_pedido(self.lista, self.productos, "Cliente", "Ana", "JAR-001", 5)
        ok, mensaje = ped.actualizar_estado(self.lista, 1, "PERDIDO")
        self.assertFalse(ok)
        self.assertIn("no válido", mensaje)

    def test_cp14_pedido_inexistente(self):
        self.assertEqual(ped.buscar_pedido(self.lista, 99), -1)

    def test_cp15_buscar_por_cliente(self):
        ped.crear_pedido(self.lista, self.productos, "Farmacia Salud Vida", "Ana", "JAR-001", 5)
        ped.crear_pedido(self.lista, self.productos, "Botica Central", "Ana", "PAR-002", 5)
        self.assertEqual(len(ped.buscar_pedidos_por_cliente(self.lista, "salud")), 1)

    def test_cp16_total_recursivo_igual_a_iterativo(self):
        self.lista = [[1, "A", "V", "JAR-001", 1, 12.5, "REGISTRADO"],
                      [2, "B", "V", "JAR-001", 3, 37.5, "REGISTRADO"],
                      [3, "C", "V", "PAR-002", 10, 12.0, "REGISTRADO"]]
        self.assertEqual(ped.total_pedidos_recursivo(self.lista), 62.0)
        self.assertEqual(ped.total_pedidos_recursivo(self.lista),
                         ped.total_pedidos_iterativo(self.lista))


class PruebasArchivosYCadenas(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.original = datos.CARPETA
        datos.CARPETA = self.carpeta.name

    def tearDown(self):
        datos.CARPETA = self.original
        self.carpeta.cleanup()

    def test_cp17_persistencia(self):
        productos = datos_base()
        lista = [[1, "CLIENTE", "ANA", "JAR-001", 5, 62.5, "REGISTRADO"]]
        mermas = [["JAR-001", 3, "ROTO", "2026-10-21"]]
        datos.guardar_todo(productos, lista, mermas)
        self.assertEqual(datos.cargar_todo(), (productos, lista, mermas))

    def test_cp18_lineas_danadas(self):
        with open(os.path.join(self.carpeta.name, "productos.txt"), "w", encoding="utf-8") as f:
            f.write("JAR-001|JARABE|12.5|500|0\n")
            f.write("PAR-002|INCOMPLETA|1.2\n")
            f.write("IBU-003|TEXTO|abc|10|0\n")
        self.assertEqual(datos.cargar_productos(), [["JAR-001", "JARABE", 12.5, 500, 0]])

    def test_cp19_manejo_de_cadenas(self):
        self.assertEqual(util.normalizar_texto("  jarabe   tos "), "JARABE TOS")
        self.assertEqual(util.convertir_precio("S/ 12,50"), 12.5)
        self.assertEqual(util.segmentar_linea("a | b|  C "), ["a", "b", "C"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
