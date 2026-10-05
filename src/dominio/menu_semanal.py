from src.tads.lista_enlazada import ListaEnlazada
from src.excepciones import ColeccionLlenaError

class MenuSemanal:
    def __init__(self, tope=6):
        self._recetas = ListaEnlazada()
        self._tope = tope

    def agregar(self, receta):
        if self._recetas.tamanio() >= self._tope:
            raise ColeccionLlenaError(f"El menú está lleno (máximo {self._tope}). No se puede agregar más.")
        self._recetas.insertar_al_final(receta)

    def listar(self):
        for r in self._recetas:
            print(f" - {r}")