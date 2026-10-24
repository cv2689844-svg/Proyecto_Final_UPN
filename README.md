# Proyecto Final UPN - Droguerías Unidas del Perú S.A.C.

Sistema de consola en Python para la **gestión de pedidos y el control de stock**.
Resuelve dos problemas: (1) el seguimiento del estado de los pedidos y
(2) el registro de productos en mal estado para que no se facturen.

**Integrantes:** Ventura Mozo Cristian David (N00184343) · Pascual Llajaruna Bryan Wilmer (N00481499)
**Docente:** Delgado Chavarri Anthony Hans · UPN Trujillo 2026

## Requisitos
Python 3.10 o superior. No necesita instalar paquetes (solo biblioteca estándar).

## Ejecución
```bash
python main.py      # abre el menú
python pruebas.py   # ejecuta las 19 pruebas automáticas
```

## Estructura
| Archivo | Responsabilidad |
|---|---|
| `main.py` | Menú y coordinación del flujo (único módulo que interactúa con el usuario) |
| `inventario.py` | Productos, búsqueda, productos en mal estado y reporte para facturación |
| `pedidos.py` | Registro de pedidos, estados (REGISTRADO → EN PREPARACION → DESPACHADO → ENTREGADO) y consultas |
| `datos.py` | Persistencia en archivos de texto (`productos.txt`, `pedidos.txt`, `mermas.txt`) |
| `utilidades.py` | Cadenas, validaciones y recursividad |
| `pruebas.py` | Pruebas con `unittest` (CP-01 a CP-19) |

## Regla central
`stock disponible = stock total - unidades en mal estado`.
Si de 500 jarabes hay 30 en mal estado, solo se pueden pedir y facturar 470.

> Los datos de `productos.txt` son de ejemplo; reemplazarlos por el catálogo real.

## Flujo de trabajo Git
Ramas `feature/inventario`, `feature/pedidos` y `feature/reportes-menu`, integradas a `main` con merge.
