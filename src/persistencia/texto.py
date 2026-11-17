import csv
from pathlib import Path
from src.dominio.receta import Receta
from src.excepciones import ArchivoInvalidoError

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_CSV = DATA / "recetas.csv"
RUTA_TXT = DATA / "recetas.txt"
RUTA_SUBRECETAS = DATA / "relaciones_subrecetas.csv"
ENCABEZADOS_RECETAS = ["id", "nombre", "tiempo_min", "dificultad", "categoria"]


def cargar_texto(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo: {ruta}")

    filas = []
    with ruta.open("r", encoding="utf-8") as archivo:
        primera = archivo.readline().strip()
        if not primera:
            raise ArchivoInvalidoError("El archivo de texto está vacío o no tiene encabezado.")
        encabezado = [col.strip() for col in primera.split(",")]
        if encabezado != ENCABEZADOS_RECETAS:
            raise ArchivoInvalidoError(
                f"Encabezado inválido: se esperaba {ENCABEZADOS_RECETAS} y se recibió {encabezado}."
            )

        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue
            valores = [v.strip() for v in linea.split(",")]
            if len(valores) != len(encabezado):
                raise ArchivoInvalidoError(
                    f"Línea con {len(valores)} campos (se esperaban {len(encabezado)}): {linea}"
                )
            filas.append(dict(zip(encabezado, valores)))
    return filas


def guardar_texto(ruta, filas, encabezados=ENCABEZADOS_RECETAS):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as archivo:
        archivo.write(",".join(encabezados) + "\n")
        for fila in filas:
            campos = [str(fila[clave]).replace(",", " ").strip() for clave in encabezados]
            archivo.write(",".join(campos) + "\n")


def filas_desde_recetas(recetas):
    filas = []
    for r in recetas:
        filas.append({
            "id": r.id,
            "nombre": r.nombre,
            "tiempo_min": r.tiempo_min,
            "dificultad": r.dificultad,
            "categoria": r.categoria,
        })
    return filas


def armar_recetas_desde_txt(ruta=RUTA_TXT):
    recetas = []
    for fila in cargar_texto(ruta):
        try:
            receta = Receta(
                id_receta=int(fila["id"]),
                nombre=fila["nombre"],
                tiempo_min=int(fila["tiempo_min"]),
                dificultad=fila["dificultad"],
                categoria=fila["categoria"],
            )
        except (ValueError, KeyError) as e:
            raise ArchivoInvalidoError(f"Registro malformado en el archivo de texto: {e}")
        recetas.append(receta)
    return recetas


def cargar_recetas(ruta=None):
    if ruta is not None:
        return armar_recetas_desde_txt(ruta)

    if RUTA_TXT.exists():
        return armar_recetas_desde_txt(RUTA_TXT)

    recetas = []
    if RUTA_CSV.exists():
        with RUTA_CSV.open(mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                recetas.append(
                    Receta(
                        id_receta=int(fila["id"]),
                        nombre=fila["nombre"],
                        tiempo_min=int(fila["tiempo_min"]),
                        dificultad=fila["dificultad"],
                        categoria=fila["categoria"],
                    )
                )
        guardar_texto(RUTA_TXT, filas_desde_recetas(recetas), ENCABEZADOS_RECETAS)
    return recetas


def cargar_relaciones_subrecetas(ruta=RUTA_SUBRECETAS):
    ruta = Path(ruta)
    relaciones = []
    if ruta.exists():
        with ruta.open(mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                relaciones.append((fila["receta_id"], fila["subreceta_id"]))
    else:
        relaciones.append(("10", "3"))
        relaciones.append(("10", "4"))
    return relaciones