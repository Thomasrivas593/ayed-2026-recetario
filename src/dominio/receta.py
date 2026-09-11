class Receta:
    def __init__ (self, id_receta, nombre, tiempo_min, dificultad, categoria) :
        self.id = id_receta
        self.nombre = nombre
        self.tiempo_min = int(tiempo_min)
        self.dificultad = dificultad
        self.categoria = categoria

    def __repr__(self):
        return f"Receta(id={self.id}, nombre={self.nombre}, tiempo_min={self.tiempo_min}, dificultad={self.dificultad}, categoria={self.categoria})"