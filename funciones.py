import random
import pygame
import colores
from clase import Vehiculo

def eliminar_enemigo_pasado(lista_de_enemigos:list, alto_pantalla:int):
    for enemigo in lista_de_enemigos:
        if enemigo.posicion[1] >= alto_pantalla:
            indice_enemigo_pasado = lista_de_enemigos.index(enemigo)
            lista_de_enemigos.pop(indice_enemigo_pasado)

def dibujar_ruta(pantalla,dic_pasto:dict,dic_calle:dict, pos_x_linea_der:int, pos_x_linea_izq:int,alto_ventana:int)->None:
    # este es el pasto, 
    pygame.draw.rect(pantalla,colores.CHARTREUSE3,((dic_pasto['pos_x'],dic_pasto['pos_y'],dic_pasto['ancho'],dic_pasto['alto'])))
    # es la calle
    pygame.draw.rect(pantalla,colores.GRAY38,((dic_calle['pos_x'], dic_calle['pos_y'],dic_calle['ancho'],dic_calle['alto'])))
    #linea izquierda
    pygame.draw.line(pantalla,colores.GRAY95,((pos_x_linea_izq, 0)), (pos_x_linea_izq,alto_ventana), 3)
    #linea derecha
    pygame.draw.line(pantalla,colores.GRAY95,((pos_x_linea_der, 0)), (pos_x_linea_der,alto_ventana), 3)
    #linea de ruta
    

def generar_enemigo_aleatorio(posicion_x_calle:int, ancho_calle:int,dic_linea_ruta:dict)->object:
    tipos_vehiculo = ["Amarillo", "Verde", "Rojo", "Negro"]
    probabilidades = [0.6, 0.3, 0.1, 0.2]  # Porcentaje de probabilidad para cada tipo de vehículo
    tipo_vehiculo = random.choices(tipos_vehiculo, probabilidades)[0]
    posicion_x_random = random.randint(posicion_x_calle, posicion_x_calle + ancho_calle)
    if tipo_vehiculo == "Amarillo":
        enemigo = Vehiculo("Amarillo", (50, 60), True, 2, True, [posicion_x_random, -60], r"img\Auto_amarillo.png",1)
    elif tipo_vehiculo == "Verde":
        enemigo = Vehiculo("Verde", (50, 60), True, 1.5, True, [posicion_x_random, -60], r"img\Auto_verde.png",1)
    elif tipo_vehiculo == "Rojo":
        enemigo = Vehiculo("Rojo", (100, 200), True, 1, True, [posicion_x_random, -200], r"img\Camion.png",1)
    elif tipo_vehiculo == "Negro":
        enemigo = Vehiculo("Negro", (60, 60), True, dic_linea_ruta["velocidad"], True, [posicion_x_random, -60], r"img\mancha.png",1)
    verificar_colisiones([enemigo])
    return enemigo

def actualizar_lista_enemigos(lista_de_enemigos:list,ancho_calle:int, posicion_x_calle:int,total_enemigos:int, alto_pantalla:int,maximo_enemigos:int,dic_linea_ruta:dict):
    if len(lista_de_enemigos) == 0 or len(lista_de_enemigos) < total_enemigos:
        lista_de_enemigos.append(generar_enemigo_aleatorio(posicion_x_calle,ancho_calle,dic_linea_ruta))
    elif len(lista_de_enemigos) >= total_enemigos:
        total_enemigos = aumentar_enemigos(total_enemigos,maximo_enemigos)
        eliminar_enemigo_pasado(lista_de_enemigos,alto_pantalla)
    return lista_de_enemigos, total_enemigos

def aumentar_enemigos(total_enemigos, maximo_enemigos)->int:
    if total_enemigos < maximo_enemigos:
        total_enemigos+= 1
    elif total_enemigos >= maximo_enemigos:
        total_enemigos = 0
    return total_enemigos


def actualizar_pantalla(lista_enemigos:list, pantalla, jugador:object, score:int, posicion_x_calle:int, ancho_calle:int):
    for enemigo in lista_enemigos:
        enemigo.mover(pantalla, posicion_x_calle, ancho_calle)
        
        if enemigo.rect.colliderect(jugador.rect) and enemigo.color != "Negro":
            if enemigo.visible:
                jugador.vidas -= 1
                enemigo.visible = False
                score -=5000
            if jugador.vidas <0:
                if not enemigo.visible:
                    jugador.explotar_auto()
                score = max(0, score)
            elif jugador.vidas >= 0:
                if not enemigo.visible:
                    if not jugador.frame >=9:
                        jugador.derrapar()
                    else:
                        jugador.estabilizar()
        if enemigo.rect.colliderect(jugador.rect) and enemigo.color == "Negro":
            if enemigo.visible:
                enemigo.visible = False
                score -= 2000
            elif not enemigo.visible:
                if not jugador.frame >=9:
                    jugador.derrapar()
                else:
                    jugador.estabilizar()
        if not jugador.rect.colliderect(enemigo.rect) and jugador.vidas >= 0:
            score +=1              
            jugador.estabilizar()    
    if jugador.rect.left <= posicion_x_calle or jugador.rect.right >= posicion_x_calle + ancho_calle:
        score -= 25
    score = max(0, score)
    return score



        
def mostrar_texto(pantalla, mensaje:str, fuente, color:tuple, posicion:tuple):
    texto = fuente.render(mensaje, True, color)
    pantalla.blit(texto, posicion)


def verificar_colisiones(lista_enemigos:list):
    for i in range(len(lista_enemigos)):
        for j in range(i + 1, len(lista_enemigos)):
            if lista_enemigos[i].color != "Negro" and lista_enemigos[j].color != "Negro":
                if lista_enemigos[i].rect.colliderect(lista_enemigos[j].rect):
                    enemigo_i = lista_enemigos[i]
                    enemigo_j = lista_enemigos[j]
                    if enemigo_i.posicion[1] < enemigo_j.posicion[1] + enemigo_j.tamaño[1] and enemigo_i.posicion[1] + enemigo_i.tamaño[1] > enemigo_j.posicion[1]:
                        # Si hay colisión vertical (en el eje Y)
                        # Desplazar los enemigos hacia abajo para evitar la colisión
                        enemigo_i.posicion[1] += enemigo_j.posicion[1] + enemigo_j.tamaño[1] - enemigo_i.posicion[1]
                        enemigo_j.posicion[1] += enemigo_j.posicion[1] + enemigo_j.tamaño[1] - enemigo_i.posicion[1]
                    else:
                        # Si hay colisión horizontal (en el eje X)
                        # Desplazar los enemigos hacia los lados para evitar la colisión
                        if enemigo_i.posicion[0] < enemigo_j.posicion[0]:
                            # Mover el enemigo i hacia la izquierda y el enemigo j hacia la derecha
                            enemigo_i.posicion[0] -= enemigo_i.tamaño[0]
                            enemigo_j.posicion[0] += enemigo_j.tamaño[0]
                        else:
                            # Mover el enemigo i hacia la derecha y el enemigo j hacia la izquierda
                            enemigo_i.posicion[0] += enemigo_i.tamaño[0]
                            enemigo_j.posicion[0] -= enemigo_j.tamaño[0]

def dibujar_lineas_ruta(pantalla, color:tuple, posicion:list, separacion:int, alto:int, ancho:int):
    for i in range(0, 9):
        if i == 1 or i % 2 != 0:
            pygame.draw.rect(pantalla, color, (posicion[0], posicion[1] + separacion + alto * i, ancho, alto))
        else:
            pygame.draw.rect(pantalla, color, (posicion[0], posicion[1], ancho, alto)) 


def verificar_click(boton:dict, posicion_click:tuple)->bool:
    posicion_del_click = list(posicion_click)
    resultado = False
    if posicion_del_click[0] >= boton["pos_x"] and posicion_del_click[0] <= boton["pos_x"] + boton["ancho"]:
        if posicion_del_click[1] >= boton["pos_y"] and posicion_del_click[1] <= boton["pos_y"] + boton["alto"]:
            resultado = True
    return resultado



def finalizar_recorrido(pantalla, meta:dict,dic_lineas:dict, lista_enemigos:list,jugador:object):
    meta["img"] = pygame.transform.scale(meta["img"],(meta["ancho"],meta["alto"])) 
    if meta["pos_y"] <= 0 + meta['alto']:
        meta['pos_y'] +=  6
    elif meta["pos_y"]*2 > 0 + meta['alto']:
        meta['pos_y'] ==  meta['pos_y']
    if meta['pos_y'] < jugador.posicion[1]:
        jugador.posicion[1] -= jugador.velocidad
    elif meta['pos_y'] >= jugador.velocidad:
        jugador.posicion[1]=jugador.posicion[1]
    pantalla.blit(meta['img'],(meta['pos_x'],meta['pos_y']))
    dic_lineas['velocidad'] = 0.005
    jugador.posicion[1] +=1 
    for enemigo in lista_enemigos:
        enemigo.posicion[1] -= (enemigo.velocidad * 2)

def mostrar_game_over(pantalla, lista_enemigos:list, ancho_pasto:int, alto_pasto:int):
    fuente = pygame.font.Font(None, 50)
    texto_game_over = fuente.render("Game Over", True, (0, 0, 0))
    pantalla.blit(texto_game_over, (ancho_pasto/ 2, alto_pasto/ 2))
    for enemigo in lista_enemigos:
        enemigo.posicion[1] -= (enemigo.velocidad * 2)
    pygame.display.update()
