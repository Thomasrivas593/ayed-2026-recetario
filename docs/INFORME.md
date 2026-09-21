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
| ListaEnlazada |  |  |
| Pila |  |  |
| Cola |  |  |

Dónde se usa cada uno en el dominio.

## 5. Complejidad (E4)

| Operación | Tiempo | Espacio | Por qué |
| --- | --- | --- | --- |
|  |  |  |  |

Mediciones (`time.perf_counter`):

| Operación | n | segundos |
| --- | --- | --- |
|  |  |  |

## 6. Persistencia (E5)

- Layout del registro binario (campos, `struct`, anchos):
- Header:
- Cómo se actualiza un registro por posición:

## 7. Reparto de trabajo (E6)

| Integrante | Qué hizo | Qué puede defender |
| --- | --- | --- |
|  |  |  |
