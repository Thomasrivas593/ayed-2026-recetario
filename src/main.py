from pathlib import Path
from src.config import TEMA
from src.dominio.recetario import Recetario
from src.persistencia.texto import cargar_recetas, cargar_relaciones_subrecetas

# --- IMPORTS AGREGADOS PARA LA ENTREGA 3 ---
from src.dominio.menu_semanal import MenuSemanal
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import ColeccionLlenaError, PilaVaciaError, ColaVaciaError

# --- IMPORTS AGREGADOS PARA LA ENTREGA 4 ---
from src.algoritmos.busqueda import busqueda_lineal, busqueda_binaria
from src.algoritmos.ordenamiento import ordenar_seleccion, ordenar_insercion, ordenar_shell

# --- IMPORTS AGREGADOS PARA LA ENTREGA 5 ---
from src.dominio.receta import Receta
from src.excepciones import ArchivoInvalidoError, ItemNoEncontradoError
from src.persistencia.texto import (
    RUTA_TXT,
    ENCABEZADOS_RECETAS,
    armar_recetas_desde_txt,
    guardar_texto,
    filas_desde_recetas,
)
from src.persistencia.binario import (
    RUTA_BIN,
    guardar_binario,
    cargar_binario,
    posicion_del_id,
    actualizar_registro,
    alta_binario,
    baja_binario,
)

TEMAS = {
    "pokedex": "Pokédex",
    "recetario": "Recetario",
    "musica": "Biblioteca musical",
}

def pendiente():
    print("Todavía no está implementado. Completar en la entrega que corresponde.")

def mostrar_menu():
    nombre = TEMAS.get(TEMA, TEMA or "(sin tema)")
    print()
    print(f"=== {nombre} — AyED C2 2026 ===")
    print("1. Listar catálogo")
    print("2. Ver detalle")
    print("3. Buscar")
    print("4. Ordenar")
    print("5. Operación recursiva")
    print("6. Colección principal (Menú)")
    print("7. Historial (pila)")
    print("8. Cola")
    print("9. Guardar / cargar archivos")
    print("0. Salir")

def listar_catalogo(recetas):
    """Muestra todas las recetas cargadas en formato tabla."""
    if not recetas:
        print("\n[!] No hay recetas en el catálogo.")
        return

    print("\n" + "=" * 78)
    print(f"{'ID':<6} {'Nombre':<32} {'Tiempo':<12} {'Dificultad':<14} {'Categoría'}")
    print("-" * 78)
    for r in recetas:
        print(f"{r.id:<6} {r.nombre:<32} {f'{r.tiempo_min} min':<12} {r.dificultad:<14} {r.categoria}")
    print("=" * 78)
    print(f"Total: {len(recetas)} recetas registradas.")

def ver_detalle(recetas):
    """Permite ingresar un ID y muestra la ficha individual."""
    id_buscado = input("Ingrese el ID de la receta: ").strip()
    encontrada = None
    for r in recetas:
        if str(r.id).strip().lower() == id_buscado.lower():
            encontrada = r
            break

    if encontrada:
        print("\n" + "-" * 40)
        print(f"FICHA TÉCNICA: {encontrada.nombre.upper()}")
        print("-" * 40)
        print(f"ID:          {encontrada.id}")
        print(f"Tiempo:      {encontrada.tiempo_min} minutos")
        print(f"Dificultad:  {encontrada.dificultad}")
        print(f"Categoría:   {encontrada.categoria}")
        print("-" * 40)
    else:
        print(f"\n[!] No se encontró ninguna receta con ID '{id_buscado}'.")

def operacion_recursiva(recetario):
    """Ejecuta la función recursiva del dominio requerida en E2."""
    id_receta = input("Ingrese el ID de la receta a desglosar: ").strip()
    receta = recetario.obtener_por_id(id_receta)
    if not receta:
        print(f"\n[!] La receta con ID '{id_receta}' no existe en el catálogo.")
        return

    desglose = recetario.desglosar_subrecetas(id_receta)
    print(f"\n--- Desglose Recursivo de Componentes para ID '{id_receta}' ---")
    print(f"Secuencia de IDs desglosados: {desglose}")
    print("Detalle de componentes:")
    for sub_id in desglose:
        item = recetario.obtener_por_id(sub_id)
        nombre = item.nombre if item else "(Subreceta base)"
        print(f" - [{sub_id}] {nombre}")
    print("----------------------------------------------------------")

def guardar_todo(recetario):
    """Mantiene sincronizados memoria, .txt y .bin."""
    guardar_texto(RUTA_TXT, filas_desde_recetas(recetario), ENCABEZADOS_RECETAS)
    guardar_binario(RUTA_BIN, recetario)

def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    # Inicializamos el dominio base
    recetario = Recetario(recetas=cargar_recetas())

    # Inicializamos las estructuras de la Entrega 3
    menu_coleccion = MenuSemanal(tope=6)
    historial = Pila()
    cola_preparacion = Cola()

    # Cargamos y asociamos las relaciones de subrecetas
    relaciones = cargar_relaciones_subrecetas()
    for id_receta, id_subreceta in relaciones:
        recetario.asociar_subreceta(id_receta, id_subreceta)

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        
        if opcion == "0":
            print("Chau.")
        
        elif opcion == "1":
            listar_catalogo(recetario)
            historial.apilar("El usuario listó el catálogo de recetas.")
        
        elif opcion == "2":
            ver_detalle(recetario)
            historial.apilar("El usuario consultó el detalle de una receta.")
            
        elif opcion == "5":
            operacion_recursiva(recetario)
            historial.apilar("El usuario ejecutó la operación recursiva.")
            
        # --- OPCIONES DE LA ENTREGA 3 Y ABM PERSISTENTE (ENTREGA 5) ---
        elif opcion == "6":
            print("\n--- Menú Semanal (Colección con Tope) ---")
            print("A. Agregar receta")
            print("B. Listar menú")
            print("C. Alta de receta en catálogo (persistente)")
            print("D. Modificar receta en catálogo (acceso directo)")
            print("E. Baja de receta en catálogo (persistente)")
            sub6 = input("Opción: ").strip().upper()
            
            if sub6 == "A":
                receta_nueva = input("Nombre de la receta a agregar: ").strip()
                try:
                    menu_coleccion.agregar(receta_nueva)
                    print(f"[OK] '{receta_nueva}' agregada al menú semanal.")
                    historial.apilar(f"Se agregó '{receta_nueva}' al menú semanal.")
                except ColeccionLlenaError as e:
                    print(f"[ERROR] {e}")
            elif sub6 == "B":
                print("\nListado actual del menú:")
                menu_coleccion.listar()
            elif sub6 == "C":
                try:
                    nuevo_id = int(input("ID numérico de la nueva receta: ").strip())
                    if recetario.obtener_por_id(nuevo_id):
                        print(f"[!] Ya existe una receta con ID {nuevo_id}.")
                        continue
                    nombre = input("Nombre: ").strip()
                    tiempo = int(input("Tiempo en minutos: ").strip())
                    dificultad = input("Dificultad (baja/media/alta): ").strip()
                    categoria = input("Categoría: ").strip()
                    if not nombre or not dificultad or not categoria:
                        print("[!] Ningún campo de texto puede estar vacío.")
                        continue

                    if not RUTA_BIN.exists():
                        guardar_binario(RUTA_BIN, recetario)

                    nueva = Receta(nuevo_id, nombre, tiempo, dificultad, categoria)
                    recetario.agregar_receta(nueva)
                    alta_binario(RUTA_BIN, nueva)
                    guardar_texto(RUTA_TXT, filas_desde_recetas(recetario), ENCABEZADOS_RECETAS)
                    historial.apilar(f"Alta persistente de receta ID {nuevo_id} ({nombre}).")
                    print(f"[OK] Receta '{nombre}' guardada en .txt y .bin.")
                except ValueError:
                    print("[ERROR] El ID y el tiempo deben ser números enteros.")
            elif sub6 == "D":
                try:
                    id_mod = input("ID de la receta a modificar: ").strip()
                    posicion = posicion_del_id(recetario, id_mod)
                    actual = recetario.obtener_por_id(id_mod)
                    print(f"Actual: {actual}")

                    nuevo_nombre = input(f"Nuevo nombre [{actual.nombre}]: ").strip() or actual.nombre
                    tiempo_str = input(f"Nuevo tiempo en min [{actual.tiempo_min}]: ").strip()
                    nuevo_tiempo = int(tiempo_str) if tiempo_str else actual.tiempo_min
                    nueva_dif = input(f"Nueva dificultad [{actual.dificultad}]: ").strip() or actual.dificultad
                    nueva_cat = input(f"Nueva categoría [{actual.categoria}]: ").strip() or actual.categoria

                    if not RUTA_BIN.exists():
                        guardar_binario(RUTA_BIN, recetario)

                    modificada = Receta(int(actual.id), nuevo_nombre, nuevo_tiempo, nueva_dif, nueva_cat)
                    recetario.obtener_todas()[posicion] = modificada
                    actualizar_registro(RUTA_BIN, posicion, modificada)
                    guardar_texto(RUTA_TXT, filas_desde_recetas(recetario), ENCABEZADOS_RECETAS)
                    historial.apilar(f"Modificación directa (seek pos {posicion}) de receta ID {id_mod}.")
                    print(f"[OK] Registro en posición {posicion} actualizado con acceso directo.")
                except ItemNoEncontradoError as e:
                    print(f"[ERROR] {e}")
                except ValueError:
                    print("[ERROR] El tiempo debe ser un número entero.")
            elif sub6 == "E":
                try:
                    id_baja = input("ID de la receta a eliminar: ").strip()
                    posicion = posicion_del_id(recetario, id_baja)
                    if not RUTA_BIN.exists():
                        guardar_binario(RUTA_BIN, recetario)
                    eliminada = recetario.obtener_todas().pop(posicion)
                    baja_binario(RUTA_BIN, posicion)
                    guardar_texto(RUTA_TXT, filas_desde_recetas(recetario), ENCABEZADOS_RECETAS)
                    historial.apilar(f"Baja persistente de receta ID {id_baja} ({eliminada.nombre}).")
                    print(f"[OK] Receta '{eliminada.nombre}' eliminada de memoria, .txt y .bin.")
                except ItemNoEncontradoError as e:
                    print(f"[ERROR] {e}")
            else:
                print("Opción inválida.")
                
        elif opcion == "7":
            print("\n--- Historial de Acciones (Pila) ---")
            try:
                accion_deshecha = historial.desapilar()
                print(f"[DESHECHO] Se eliminó del historial: '{accion_deshecha}'")
            except PilaVaciaError as e:
                print(f"[ERROR] {e}")
                
        elif opcion == "8":
            print("\n--- Cola de Preparación ---")
            print("A. Encolar receta para cocinar")
            print("B. Terminar preparación (desencolar)")
            sub_opcion = input("Elija una opción: ").strip().upper()
            
            if sub_opcion == "A":
                receta_encolar = input("Nombre de la receta: ").strip()
                cola_preparacion.encolar(receta_encolar)
                print(f"[OK] '{receta_encolar}' puesta en cola de preparación.")
                historial.apilar(f"Se encoló '{receta_encolar}' para preparación.")
            elif sub_opcion == "B":
                try:
                    receta_lista = cola_preparacion.desencolar()
                    print(f"[OK] ¡Preparación terminada! Salió: '{receta_lista}'")
                    historial.apilar(f"Se terminó de preparar '{receta_lista}'.")
                except ColaVaciaError as e:
                    print(f"[ERROR] {e}")
            else:
                print("Opción inválida.")
                
        # --- OPCIONES DE LA ENTREGA 4 ---
        elif opcion == "3":
            print("\n--- Buscar Receta ---")
            print("1. Por Nombre (Lineal)")
            print("2. Por Nombre (Binaria - requiere orden)")
            sub = input("> ").strip()
            
            lista_recetas = recetario.obtener_todas()
            clave_buscada = input("Ingrese el nombre a buscar: ").strip().lower()
            
            if sub == "1":
                resultado = busqueda_lineal(lista_recetas, clave_buscada, lambda r: r.nombre.lower())
                print(f"[ENCONTRADO] {resultado.nombre}" if resultado else "[!] No encontrado.")
            elif sub == "2":
                print("[!] Ordenando catálogo por nombre para usar búsqueda binaria...")
                ordenar_insercion(lista_recetas, lambda r: r.nombre.lower())
                guardar_todo(recetario)
                resultado = busqueda_binaria(lista_recetas, clave_buscada, lambda r: r.nombre.lower())
                print(f"[ENCONTRADO] {resultado.nombre}" if resultado else "[!] No encontrado.")
            else:
                print("Opción inválida.")
                
        elif opcion == "4":
            print("\n--- Ordenar Catálogo ---")
            print("Criterios: 1) Nombre   2) Tiempo de preparación")
            criterio = input("> ").strip()
            
            print("Algoritmos: 1) Selección  2) Inserción  3) Shell Sort (Extra)")
            algo = input("> ").strip()
            
            lista_recetas = recetario.obtener_todas()
            
            if criterio == "1":
                clave_fn = lambda r: r.nombre.lower()
                nom_crit = "Nombre"
            elif criterio == "2":
                clave_fn = lambda r: r.tiempo_min
                nom_crit = "Tiempo"
            else:
                print("Criterio inválido.")
                continue
            
            if algo == "1":
                ordenar_seleccion(lista_recetas, clave_fn)
                guardar_todo(recetario)
                print(f"[OK] Catálogo ordenado por {nom_crit} (Selección).")
            elif algo == "2":
                ordenar_insercion(lista_recetas, clave_fn)
                guardar_todo(recetario)
                print(f"[OK] Catálogo ordenado por {nom_crit} (Inserción).")
            elif algo == "3":
                ordenar_shell(lista_recetas, clave_fn)
                guardar_todo(recetario)
                print(f"[OK] Catálogo ordenado por {nom_crit} (Shell Sort).")
            else:
                print("Algoritmo inválido.")

        # --- OPCIONES DE LA ENTREGA 5 ---
        elif opcion == "9":
            print("\n--- Guardar / Cargar Archivos ---")
            print("a) Cargar catálogo desde .txt (data/recetas.txt)")
            print("b) Guardar catálogo en .txt (data/recetas.txt)")
            print("c) Guardar catálogo en binario (data/recetas.bin)")
            print("d) Cargar catálogo desde binario (data/recetas.bin)")
            print("e) Cargar archivo por ruta (validar ArchivoInvalidoError)")
            sub = input("Subopción > ").strip().lower()

            try:
                if sub == "a":
                    recetario.recetas = armar_recetas_desde_txt(RUTA_TXT)
                    print(f"[OK] Catálogo cargado desde .txt: {len(recetario)} ítems.")
                elif sub == "b":
                    guardar_texto(RUTA_TXT, filas_desde_recetas(recetario), ENCABEZADOS_RECETAS)
                    print(f"[OK] Catálogo guardado en {RUTA_TXT}.")
                elif sub == "c":
                    guardar_binario(RUTA_BIN, recetario)
                    print(f"[OK] Catálogo guardado en {RUTA_BIN}.")
                elif sub == "d":
                    recetario.recetas = cargar_binario(RUTA_BIN)
                    print(f"[OK] Catálogo cargado desde .bin: {len(recetario)} ítems.")
                elif sub == "e":
                    ruta_custom = Path(input("Ruta del archivo a validar (ej. data/basura.bin): ").strip())
                    if ruta_custom.suffix.lower() == ".txt":
                        recetario.recetas = armar_recetas_desde_txt(ruta_custom)
                    else:
                        recetario.recetas = cargar_binario(ruta_custom)
                    print(f"[OK] Archivo válido cargado: {len(recetario)} ítems.")
                else:
                    print("Subopción inválida.")
            except ArchivoInvalidoError as error:
                print(f"[ERROR] Archivo inválido: {error}")

        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()