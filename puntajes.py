import sqlite3
import pygame
def crear_tabla():
    with sqlite3.connect("tabla_puntajes.db") as conexion:
            try:
                sentencia = ''' create table tabla_puntajes
                                (
                                    id text,
                                    usuario text,
                                    score integer,
                                    vidas integer
                                )
                            '''
                conexion.execute(sentencia)
                print("Se creo la tabla puntajes.")
            except sqlite3.OperationalError:
                print("La tabla puntajes ya existe.")


def actualizar_datos_en_la_tabla(id_ingresado, usuario_ingresado, score_ingresado, vidas_restantes):
    with sqlite3.connect("tabla_puntajes.db") as conexion:
        try:
            conexion.execute("INSERT INTO tabla_puntajes (id, usuario, score, vidas) VALUES (?, ?, ?, ?)",
                             (id_ingresado, usuario_ingresado, score_ingresado, vidas_restantes))
            conexion.commit()
            print("Datos actualizados correctamente.")
        except sqlite3.Error as error:
            print("Error al actualizar los datos:", error)



def imprimir_tabla():
    with sqlite3.connect("tabla_puntajes.db") as conexion:
        cursor = conexion.execute("SELECT * FROM tabla_puntajes")
        for fila in cursor:
            print(fila)
            
import sqlite3

def acomodar_puntajes(puntajes: list) -> list:
    """
    Ordena una lista de puntajes en orden descendente según la clave "score" de cada diccionario.
    El parametro que toma: puntajes (list): Una lista de diccionarios que representan puntajes. Cada diccionario
    debe tener una clave "score" que contenga el puntaje.
    Retorna la lista de puntajes ordenada en orden descendente según la clave "score" y "vidas".
    """
    puntajes.sort(key=lambda x: x["score"], reverse=True)
    puntajes.sort(key=lambda x: x["vidas"], reverse=True)
    return puntajes

def obtener_datos_desde_tabla()->list:
    """
    devuelve una lista con diccionarios, donde cada elemento es un diccionario que contiene (id,usuario,vidas,score)
    """
    lista_datos = []

    with sqlite3.connect("tabla_puntajes.db") as conexion:
        cursor = conexion.execute("SELECT id, usuario, score, vidas FROM tabla_puntajes")

        for fila in cursor:
            id = fila[0]
            usuario = fila[1]
            score = fila[2]
            vidas = fila[3]

            lista_datos.append({
                "id" : id,
                "usuario": usuario,
                "score": score,
                "vidas": vidas
            }) 

    return acomodar_puntajes(lista_datos)

def mostrar_tabla(pantalla, tamaño_tabla, datos, img_fondo, posicion_tabla):
    corriendo = True
    resultado = None
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    corriendo = False
                    resultado = "volver"
            elif evento.type == pygame.QUIT:
                corriendo = False
                resultado = "salir"

        COLOR_BORDE = (255, 0, 51)
        COLOR_TEXTO = (0, 0, 0)
        COLOR_FONDO = (255, 255, 255)
        FILAS = 11  # Número de filas, incluyendo la fila de encabezados
        COLUMNAS = 4  # Número de columnas

        ANCHO_CELDA = tamaño_tabla[0] // COLUMNAS
        ALTO_CELDA = tamaño_tabla[1] // FILAS

        x_tabla = posicion_tabla[0]
        y_tabla = posicion_tabla[1]

        pantalla.blit(img_fondo, (0, 0))
        pygame.draw.rect(pantalla, COLOR_FONDO, (x_tabla, y_tabla, ANCHO_CELDA * COLUMNAS, ALTO_CELDA * FILAS))

        encabezados = ["Puesto", "Usuario", "Score", "Vidas"]
        for i, encabezado in enumerate(encabezados):
            x_celda = x_tabla + i * ANCHO_CELDA
            y_celda = y_tabla

            pygame.draw.rect(pantalla, COLOR_BORDE, (x_celda, y_celda, ANCHO_CELDA, ALTO_CELDA), 3)

            font = pygame.font.Font("C:/USERS/EZEMONSON/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/TAPE LOOP REGULAR.TTF", 24)
            texto = font.render(encabezado, True, COLOR_TEXTO)
            centro_x = x_celda + ANCHO_CELDA // 2 - texto.get_width() // 2
            centro_y = y_celda + ALTO_CELDA // 2 - texto.get_height() // 2
            pantalla.blit(texto, (centro_x, centro_y))
        
        for i in range(FILAS - 1):  # Filas de datos, se resta 1 para excluir la fila de encabezados
            for j in range(COLUMNAS):  # Columnas de datos
                x_celda = x_tabla + j * ANCHO_CELDA
                y_celda = y_tabla + (i + 1) * ALTO_CELDA

                pygame.draw.rect(pantalla, COLOR_BORDE, (x_celda, y_celda, ANCHO_CELDA, ALTO_CELDA), 3)
                
                if i < len(datos):
                    dato = datos[i]
                    if j == 0:
                        valor = str(i + 1)  # Mostrar el número de puesto
                    elif j == 1:
                        valor = dato["id"]  # Obtener el valor del ID
                    elif j == 2:
                        valor = str(dato["score"])
                    else:
                        valor = str(dato["vidas"])  # Obtener el valor del nombre

                    font = pygame.font.Font("C:/USERS/EZEMONSON/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/TAPE LOOP REGULAR.TTF", 24)
                    texto = font.render((valor), True, COLOR_TEXTO)
                    centro_x = x_celda + ANCHO_CELDA // 2 - texto.get_width() // 2
                    centro_y = y_celda + ALTO_CELDA // 2 - texto.get_height() // 2
                    pantalla.blit(texto, (centro_x, centro_y))
        
        pygame.display.flip()

    return resultado




