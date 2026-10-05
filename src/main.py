from src.config import TEMA
from src.dominio.recetario import Recetario
from src.persistencia.texto import cargar_recetas, cargar_relaciones_subrecetas

# --- IMPORTS AGREGADOS PARA LA ENTREGA 3 ---
from src.dominio.menu_semanal import MenuSemanal
from src.tads.pila import Pila
from src.tads.cola import Cola
from src.excepciones import ColeccionLlenaError, PilaVaciaError, ColaVaciaError

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
            
        # --- OPCIONES DE LA ENTREGA 3 ---
        elif opcion == "6":
            print("\n--- Menú Semanal (Colección con Tope) ---")
            print("A. Agregar receta")
            print("B. Listar menú")
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
                
        elif opcion in {"3", "4", "9"}:
            pendiente()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    main()