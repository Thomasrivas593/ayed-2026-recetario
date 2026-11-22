# Informe del TP

Completar y hacer crecer en cada entrega. No hace falta prosa larga: oraciones claras y tablas.

## 1. Grupo y tema

- Tema: recetario
- Por qué lo eligieron (5–8 líneas):

## 2. Modelo

Qué es un ítem del catálogo. Qué es mutable y qué no (E1). Cómo se relacionan catálogo, colección principal, pila y cola.
En este tema, cada item es una receta, representada por la entidad del mismo nombre 
```text
(pueden pegar un diagrama ASCII o una lista de clases)
```

## 3. Recursión (E2)

- Función: `desglosar_subrecetas(recetario, id_receta)`
- Caso base: Si la receta no contiene subrecetas asociadas (`not sub`), devuelve una lista con su propio identificador: `[id_receta]`
- Caso recursivo: [id_receta] + `desglosar_subrecetas(sub_id)`
- Traza de un ejemplo real del dataset:

* **Llamada 1:** `desglosar_subrecetas("10")`
  * Busca dependencias directas: `["3", "4"]`.
  * Devuelve: `["10"] + desglosar_subrecetas("3") + desglosar_subrecetas("4")`

* **Llamada 2:** `desglosar_subrecetas("3")`
  * No tiene subrecetas (caso base), devuelve: `["3"]`

* **Llamada 3:** `desglosar_subrecetas("4")`
  * No tiene subrecetas (caso base), devuelve: `["4"]`

* **Resultado final:**
  * `["10"] + ["3"] + ["4"] = ["10", "3", "4"]`

## 4. TADs (E3)

| TAD | Operaciones | Invariante |
| --- | --- | --- |
| ListaEnlazada |esta_vacia(), tamanio(), insertar_al_inicio(dato), insertar_al_final(dato), insertar_ordenado(dato, clave), eliminar(dato), buscar(dato), __iter__()  |  |
| Pila | apilar(dato), desapilar(), ver_tope(), esta_vacia() |  |
| Cola | encolar(dato), desencolar(), ver_frente(), esta_vacia() |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

## 5. Complejidad y Rendimiento (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
| Listar catálogo | $O(n)$ | $O(1)$ | Recorre los n elementos una vez (iterador). |
| Búsqueda lineal | $O(n)$ en el peor / $O(1)$ en el mejor | $O(1)$ | Recorre los n elementos secuencialmente. Toca cada elemento hasta encontrarlo o llegar al final. |
| Búsqueda binaria | $O(\log n)$ | $O(1)$ | Cada comparación descarta la mitad del rango de búsqueda  . |
| Ordenar por Selección | $O(n^2)$ siempre | $O(1)$ | Dos bucles anidados: realiza $\approx n^2/2$ comparaciones sin importar si ya está ordenado. |
| Ordenar por Inserción | $O(n)$ mejor / $O(n^2)$ peor y promedio | $O(1)$ | Si ya está ordenado, hace 1 comparación por elemento; si está al revés, desplaza todo. |
| Ordenar por Shell Sort | $O(n \log n)$ a $O(n^2)$ | $O(1)$ | Mejora la inserción al comparar elementos separados por una brecha, minimizando desplazamientos pesados (Algoritmo extra). |



Mediciones (`time.perf_counter`):


| Operación | n | segundos |
| --- | --- | --- |
| Búsqueda lineal (nombre) | 30 | 0.000012 s |
| Búsqueda lineal ($n \times 10$) | 300 | 0.000005 s |
| Búsqueda binaria (nombre) | 30 | 0.000005 s |
| Búsqueda binaria ($n \times 10$) | 300 |  0.000007 s |

## 6. Persistencia (E5)

- **Layout del registro binario (campos, `struct`, anchos):** Elegí `struct.Struct("<I 35s H 12s 20s")`, lo que da un tamaño fijo de **73 bytes** por receta:
  - `id` (`I`, 4 bytes): número entero para el ID.
  - `nombre` (`35s`, 35 bytes): texto en UTF-8 rellenado con `\x00` (elegí 35 bytes para que entren nombres largos como *"Panqueques con dulce de leche"* sin cortarse).
  - `tiempo_min` (`H`, 2 bytes): entero corto para los minutos de preparación.
  - `dificultad` (`12s`, 12 bytes): texto en UTF-8 rellenado con `\x00` (`baja`, `media`, `alta`).
  - `categoria` (`20s`, 20 bytes): texto en UTF-8 rellenado con `\x00` (`salsa`, `principal`, `acompanamiento`, etc.).
- **Header:** Uso `struct.Struct("<4s 1s I")` (**9 bytes** al principio del archivo) para validar el archivo antes de leer las recetas:
  - `magia` (`4s`, 4 bytes): texto fijo `AYED` para comprobar que el archivo lo generó mi programa.
  - `tema` (`1s`, 1 byte): letra `R` para indicar que pertenece al tema Recetario.
  - `cantidad` (`I`, 4 bytes): entero con el total de recetas guardadas.
- **Cómo se actualiza un registro por posición:** Como el header mide siempre 9 bytes y cada receta ocupa exactamente 73 bytes, puedo calcular en qué byte empieza cualquier registro (`0-based`) sin leer los anteriores ($O(1)$). Abro el archivo en modo `"r+b"`, salto directo con `seek(9 + posicion * 73)` y piso solo esos 73 bytes con `write()`. Para el alta agrego el registro al final (`seek(0, 2)`) y sumo 1 a la cantidad en el header; para la baja reescribo los registros que quedan para no dejar huecos vacíos en el medio.
## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
Rivas, hice todo el trabajo, me quedé solo en la 2da entrega, mi compañera dejó