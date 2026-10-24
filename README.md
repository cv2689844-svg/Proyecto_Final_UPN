# Proyecto Final UPN - Droguerías Unidas del Perú S.A.C.

Sistema de consola en Python para la **gestión de pedidos y el control de stock**.
Resuelve dos problemas: (1) el seguimiento del estado de los pedidos y
(2) el registro de productos en mal estado para que no se facturen.

**Integrantes:** Ventura Mozo Cristian David (N00184343) · Pascual Llajaruna Bryan Wilmer (N00481499)
**Docente:** Delgado Chavarri Anthony Hans · UPN Trujillo 2026

## Ejecución
```bash
python main.py       # abre el menú
python pruebas.py    # ejecuta los 19 casos de prueba
```
Solo usa Python 3 (no hay que instalar paquetes).

## Archivos
| Archivo | Responsabilidad |
|---|---|
| `main.py` | Menú principal (único módulo que habla con el usuario) |
| `inventario.py` | Productos, productos en mal estado y reporte para facturación |
| `pedidos.py` | Pedidos y sus estados: REGISTRADO → EN PREPARACION → DESPACHADO → ENTREGADO |
| `datos.py` | Guardar y cargar la información en archivos de texto |
| `utilidades.py` | Validaciones (`leer_entero`, `leer_decimal`), textos y recursividad |
| `pruebas.py` | 19 casos de prueba (CP-01 a CP-19) |
| `productos.txt` | Catálogo de 25 productos con lote, vencimiento, precio y stock |

## Regla central
`stock disponible = stock total - unidades en mal estado`.
Ejemplo: ALERGINA tiene 290 unidades; si 30 están en mal estado, solo se pueden pedir y facturar 260.
