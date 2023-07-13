import random

def generar_id_unico(ids_existente, usuario):
    longitud = 4
    caracteres = '0123456789'
    id_numerico = ''.join(random.sample(caracteres, longitud))
    nombre_usuario = usuario
    id_unico = f"{nombre_usuario}#{id_numerico}"
    if id_unico in ids_existente:
        return None
    
    return id_unico


def devolver_lista_id(lista_puntajes:list)->list:
    lista_ids = []
    for puntaje in lista_puntajes:
        lista_ids.append(puntaje["id"])
    return lista_ids