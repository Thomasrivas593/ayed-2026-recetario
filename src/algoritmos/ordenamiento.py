def ordenar_seleccion(coleccion, obtener_clave):
    n = len(coleccion)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            if obtener_clave(coleccion[j]) < obtener_clave(coleccion[pos_min]):
                pos_min = j
        coleccion[i], coleccion[pos_min] = coleccion[pos_min], coleccion[i]
    return coleccion

def ordenar_insercion(coleccion, obtener_clave):
    for i in range(1, len(coleccion)):
        actual = coleccion[i]
        j = i - 1
        while j >= 0 and obtener_clave(coleccion[j]) > obtener_clave(actual):
            coleccion[j + 1] = coleccion[j]
            j -= 1
        coleccion[j + 1] = actual
    return coleccion

def ordenar_shell(coleccion, obtener_clave): #tercer algoritmo de ordenamiento, para el punto extra 
    n = len(coleccion)
    brecha = n // 2
    while brecha > 0:
        for i in range(brecha, n):
            temp = coleccion[i]
            j = i
            while j >= brecha and obtener_clave(coleccion[j - brecha]) > obtener_clave(temp):
                coleccion[j] = coleccion[j - brecha]
                j -= brecha
            coleccion[j] = temp
        brecha //= 2
    return coleccion