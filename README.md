# TP integrador — AyED C2 2026

Repositorio del grupo. Partir de este esqueleto. No borrar la estructura de `src/` ni de `docs/`.

## Integrantes

| Nombre | Mail | GitHub |
| Rivas Thomas| thomasrivas100@gmail.com | thomasrivas593  |


**Tema elegido:**  Recetario 

## Cómo ejecutar

Desde la raíz del repo, con Python 3.10 o superior:

```text
python -m src.main
```

En Windows, si `python` no anda: `py -3 -m src.main`.

Solo biblioteca estándar. No hay `requirements.txt` a propósito.

## Entregas

Cada vencimiento se marca con un tag. Ver `GIT.md`.

| Tag | Vence |
| --- | --- |
| `preentrega` (opcional, solo repo) | domingo 30-ago-2026 23:59 |
| `entrega-1` | domingo 06-sep-2026 23:59 |
| `entrega-2` | domingo 20-sep-2026 23:59 |
| `entrega-3` | domingo 04-oct-2026 23:59 |
| `entrega-4` | domingo 01-nov-2026 23:59 |
| `entrega-5` | domingo 15-nov-2026 23:59 |
| `entrega-6` | domingo 22-nov-2026 23:59 |

Defensa oral (reemplaza el 2do parcial): 25 y 27-nov-2026.

La cátedra corrige el **tag**, no el último commit suelto de `main`.

El grupo se avisa por mail a diego.ambrossio@unab.edu.ar **y** angel.bianco@unab.edu.ar. Ver `GIT.md`.


Gestor de catálogo por consola con las 10 operaciones del menú:

Listar catálogo: recorre las recetas cargadas mediante el iterador propio de la ListaEnlazada.

Ver detalle: muestra la ficha técnica individual de una receta por ID, validando IDs inexistentes sin interrumpir la ejecución.

Buscar: búsqueda lineal por nombre y búsqueda binaria (ordenando previamente el catálogo por nombre).

Ordenar: ordenamiento del catálogo por nombre o tiempo de preparación utilizando algoritmos propios (Selección, Inserción y Shell Sort).

Operación recursiva: desglose en profundidad de una receta compuesta y todas sus subrecetas asociadas (data/subrecetas.txt).

Colección principal y ABM persistente: gestión de un Menú Semanal mediante colección con tope máximo de 6 elementos, y altas, bajas y modificaciones persistentes sobre el catálogo (.txt y .bin con actualización directa vía seek).

Historial (Pila): registro LIFO de las acciones realizadas durante la sesión con opción de deshacer, capturando PilaVaciaError.

Cola de preparación: gestión FIFO de recetas en espera de preparación, capturando ColaVaciaError.

Persistencia en archivos: carga y guardado en texto simple (.txt) y en binario de registros de longitud fija con cabecera (struct), validando integridad y lanzando ArchivoInvalidoError ante archivos corruptos o truncados.

Salir: finalización limpia del programa.