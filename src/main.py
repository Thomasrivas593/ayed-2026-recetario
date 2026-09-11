from src.config import TEMA
from src.persistencia.texto import cargar_recetas

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
    print("6. Colección principal (equipo / menú / playlist)")
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


def main():
    if TEMA not in TEMAS:
        print("Seteá TEMA en src/config.py: 'pokedex', 'recetario' o 'musica'.")
        return

    # Cargamos el dataset al inicio
    recetas = cargar_recetas()

    opcion = None
    while opcion != "0":
        mostrar_menu()
        opcion = input("> ").strip()
        if opcion == "0":
            print("Chau.")
        elif opcion == "1":
            listar_catalogo(recetas)
        elif opcion == "2":
            ver_detalle(recetas)
        elif opcion in {"3", "4", "5", "6", "7", "8", "9"}:
            pendiente()
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
