# ============================================================
# utilidades.py
# Funciones de apoyo: validar datos, limpiar textos y recursividad
# ============================================================

# Lista 1D con los estados del pedido, en el orden del flujo
ESTADOS = ["REGISTRADO", "EN PREPARACION", "DESPACHADO", "ENTREGADO"]


def leer_entero(mensaje, minimo=0):
  # Pide un numero entero y repite hasta que sea valido
  while True:
    try:
      valor = int(input(mensaje))

      if valor < minimo:
        print(f"Error: el valor minimo es {minimo}.")
      else:
        return valor

    except ValueError:
      print("Error: ingrese un numero entero valido.")


def leer_decimal(mensaje, minimo=0):
  # Pide un numero decimal (acepta coma o punto) y repite hasta que sea valido
  while True:
    try:
      entrada = input(mensaje).strip().replace(",", ".")
      valor = float(entrada)

      if valor < minimo:
        print(f"Error: el valor minimo es {minimo}.")
      else:
        return valor

    except ValueError:
      print("Error: ingrese un numero valido.")


def leer_texto(mensaje):
  # Pide un texto que no puede quedar vacio
  texto = input(mensaje).strip()

  while texto == "":
    print("Error: no puede estar vacio.")
    texto = input(mensaje).strip()

  return limpiar_texto(texto)


def limpiar_texto(texto):
  # Quita espacios de sobra, pasa a mayusculas y cambia '|' por '/'
  # porque '|' es el separador que se usa en los archivos
  texto = texto.strip().upper()
  texto = texto.replace("|", "/")
  palabras = texto.split()
  return " ".join(palabras)


def soles(monto):
  # Muestra un monto en soles, por ejemplo: S/ 1,250.00
  return f"S/ {monto:,.2f}"


def mostrar_titulo(titulo):
  print()
  print("=" * 70)
  print(titulo)
  print("=" * 70)


def sumar_recursivo(valores, indice=0):
  # Suma los elementos de una lista usando recursividad
  # Caso base: si ya se llego al final de la lista, la suma es 0
  if indice >= len(valores):
    return 0

  # Caso recursivo: valor actual + suma del resto de la lista
  return valores[indice] + sumar_recursivo(valores, indice + 1)
