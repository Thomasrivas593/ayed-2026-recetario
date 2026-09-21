class Recetario: 
    def __init__(self, recetas=None, subrecetas=None): 
        # Si no se pasa una lista de recetas, se inicializa con una lista vacía
        self.recetas = recetas if recetas is not None else []
        # Guarda tuplas: (receta, subreceta)
        self._subrecetas = subrecetas if subrecetas is not None else []

    def agregar_receta(self, receta):
        self.recetas.append(receta)

    def obtener_todas(self):
        return self.recetas
    
    def __iter__(self):
        return iter(self.recetas)

    def obtener_por_id(self, id_receta):
        id_buscado = str(id_receta).strip()
        for receta in self.recetas:
            if str(receta.id).strip() == id_buscado:
                return receta
        return None

    def asociar_subreceta(self, receta_id, subreceta):
        receta = self.obtener_por_id(receta_id)
        if receta:
            self._subrecetas.append((receta, subreceta))
            return True
        return False

    def subrecetas(self, receta_id):
        id_buscado = str(receta_id).strip()
        return [subreceta for receta, subreceta in self._subrecetas if str(receta.id).strip() == id_buscado]

    def desglosar_subrecetas(self, receta_id):
        """
        Función recursiva del dominio (Ítem 2 de E2):
        Desglosa una receta en todos sus componentes y subrecetas.
        """
        id_str = str(receta_id).strip()
        hijos = self.subrecetas(id_str)

        # CASO BASE: no tiene sub-recetas (es una receta 'hoja')
        if not hijos:
            return [id_str]

        # CASO RECURSIVO: se llama a sí misma por cada subreceta
        resultado = [id_str]
        for sub in hijos:
            sub_id = sub.id if hasattr(sub, "id") else sub
            resultado += self.desglosar_subrecetas(sub_id)
        return resultado

    def __len__(self):
        return len(self.recetas)