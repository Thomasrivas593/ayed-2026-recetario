import csv
from src.dominio.receta import Receta

def cargar_csv(ruta):
    filas = []
    with open(ruta, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            filas.append(fila)
    return filas


def guardar_csv(ruta, filas, encabezados):
    with open(ruta, mode="w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=encabezados)
        escritor.writeheader()
        escritor.writerows(filas)

def cargar_recetas(ruta="data/recetas.csv"):
    """Carga el CSV y transforma cada fila en un objeto Receta."""
    recetas = []
    with open(ruta, mode="r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            receta = Receta(
                id_receta=fila["id"],
                nombre=fila["nombre"],
                tiempo_min=fila["tiempo_min"],
                dificultad=fila["dificultad"],
                categoria=fila["categoria"]
            )
            recetas.append(receta)
    return recetas        