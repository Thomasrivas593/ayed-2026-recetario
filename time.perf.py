import time
from src.persistencia.texto import cargar_recetas
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_insercion

# 1. Cargar datos reales
datos_originales = cargar_recetas()
n_original = len(datos_originales)

# 2. Agrandar datos para la prueba (multiplicamos por 10)
datos_grandes = datos_originales * 10
n_grandes = len(datos_grandes)

# Tomamos el nombre de la primera receta para buscar algo que sabemos que existe
nombre_buscado = datos_originales[0].nombre.lower() if n_original > 0 else "prueba"

print("=== MIDIENDO TIEMPOS DE BÚSQUEDA ===")

# --- BÚSQUEDA LINEAL ---
inicio = time.perf_counter()
busqueda_lineal(datos_originales, nombre_buscado, lambda r: r.nombre.lower())
fin = time.perf_counter()
print(f"Lineal Original (n={n_original}):  {fin - inicio:.6f} s")

inicio = time.perf_counter()
busqueda_lineal(datos_grandes, nombre_buscado, lambda r: r.nombre.lower())
fin = time.perf_counter()
print(f"Lineal Agrandado (n={n_grandes}): {fin - inicio:.6f} s")

# --- BÚSQUEDA BINARIA ---
# Por regla, la binaria requiere que los datos estén ordenados primero
ordenar_insercion(datos_originales, lambda r: r.nombre.lower())
ordenar_insercion(datos_grandes, lambda r: r.nombre.lower())

inicio = time.perf_counter()
busqueda_binaria(datos_originales, nombre_buscado, lambda r: r.nombre.lower())
fin = time.perf_counter()
print(f"Binaria Original (n={n_original}):  {fin - inicio:.6f} s")

inicio = time.perf_counter()
busqueda_binaria(datos_grandes, nombre_buscado, lambda r: r.nombre.lower())
fin = time.perf_counter()
print(f"Binaria Agrandado (n={n_grandes}): {fin - inicio:.6f} s")