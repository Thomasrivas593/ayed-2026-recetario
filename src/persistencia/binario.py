import struct
from pathlib import Path
from src.dominio.receta import Receta
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError

RAIZ = Path(__file__).resolve().parents[2]
DATA = RAIZ / "data"
RUTA_BIN = DATA / "recetas.bin"

HEADER = struct.Struct("<4s 1s I")
FORMATO = struct.Struct("<I 35s H 12s 20s")
MAGIA = b"AYED"
TEMA_BIN = b"R"


def _a_bytes(texto, ancho):
    codificado = str(texto).encode("utf-8")[:ancho]
    while True:
        try:
            codificado.decode("utf-8")
            break
        except UnicodeDecodeError:
            codificado = codificado[:-1]
    return codificado.ljust(ancho, b"\x00")


def _a_texto(datos):
    return datos.rstrip(b"\x00").decode("utf-8")


def _receta_a_tupla(item):
    return (
        int(item.id),
        _a_bytes(item.nombre, 35),
        int(item.tiempo_min),
        _a_bytes(item.dificultad, 12),
        _a_bytes(item.categoria, 20),
    )


def _tupla_a_receta(t):
    return Receta(
        id_receta=t[0],
        nombre=_a_texto(t[1]),
        tiempo_min=t[2],
        dificultad=_a_texto(t[3]),
        categoria=_a_texto(t[4]),
    )


def guardar_binario(ruta, items):
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    lista = list(items)
    with ruta.open("wb") as archivo:
        archivo.write(HEADER.pack(MAGIA, TEMA_BIN, len(lista)))
        for item in lista:
            archivo.write(FORMATO.pack(*_receta_a_tupla(item)))


def cargar_binario(ruta):
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")

    with ruta.open("rb") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado: ni siquiera tiene header completo.")

        magia, tema, cantidad = HEADER.unpack(cabecera)
        if magia != MAGIA:
            raise ArchivoInvalidoError("Magia incorrecta: este archivo no es de este TP.")
        if tema != TEMA_BIN:
            raise ArchivoInvalidoError(f"Tema binario incorrecto ({tema!r}): se esperaba {TEMA_BIN!r}.")

        items = []
        for _ in range(cantidad):
            datos = archivo.read(FORMATO.size)
            if len(datos) < FORMATO.size:
                raise ArchivoInvalidoError(
                    "Binario truncado: el header dice más registros de los que hay."
                )
            items.append(_tupla_a_receta(FORMATO.unpack(datos)))
    return items


def posicion_del_id(items, id_buscado):
    objetivo = str(id_buscado).strip()
    for posicion, item in enumerate(items):
        if str(item.id).strip() == objetivo:
            return posicion
    raise ItemNoEncontradoError(f"No existe ninguna receta con ID '{id_buscado}'.")


def actualizar_registro(ruta, posicion, item):
    """Pisa un registro por posición (acceso directo). posicion es 0-based."""
    ruta = Path(ruta)
    if not ruta.exists():
        raise ArchivoInvalidoError(f"No existe el archivo binario: {ruta}")
    with ruta.open("r+b") as archivo:
        archivo.seek(HEADER.size + posicion * FORMATO.size)
        archivo.write(FORMATO.pack(*_receta_a_tupla(item)))


def alta_binario(ruta, item):
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado al intentar dar de alta.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        archivo.seek(0, 2)
        archivo.write(FORMATO.pack(*_receta_a_tupla(item)))
        archivo.seek(0)
        archivo.write(HEADER.pack(magia, tema, cantidad + 1))


def baja_binario(ruta, posicion):
    ruta = Path(ruta)
    with ruta.open("r+b") as archivo:
        cabecera = archivo.read(HEADER.size)
        if len(cabecera) < HEADER.size:
            raise ArchivoInvalidoError("Binario truncado al intentar dar de baja.")
        magia, tema, cantidad = HEADER.unpack(cabecera)
        registros = [archivo.read(FORMATO.size) for _ in range(cantidad)]
        del registros[posicion]
        archivo.seek(0)
        archivo.truncate()
        archivo.write(HEADER.pack(magia, tema, len(registros)))
        for datos in registros:
            archivo.write(datos)