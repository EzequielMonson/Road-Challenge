import pygame
from funciones import verificar_click, mostrar_texto
from tamanio_posiciones import *
from juego import iniciar_juego
from puntajes import *
from unico_id import generar_id_unico, devolver_lista_id


timer_segundos = pygame.USEREVENT
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
fondo_inicio = r"img\fondo_inicio.png"
fondo_inicio = pygame.image.load(fondo_inicio)
fondo_inicio = pygame.transform.scale(fondo_inicio,(ANCHO_VENTANA,ALTO_VENTANA))
titulo = r"img\titulo.png"
titulo_inicio = pygame.image.load(titulo)
titulo_inicio = pygame.transform.scale(titulo_inicio,(tamaño_titulo[0],tamaño_titulo[1]))
boton_play["img"] = pygame.transform.scale(boton_play["img"],(boton_play["ancho"],boton_play["alto"])) 
boton_scores["img"]  = pygame.transform.scale(boton_scores["img"],(boton_scores["ancho"],boton_scores["alto"])) 
estado = True
font_input = pygame.font.Font("C:/USERS/EZEMONSON/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/TAPE LOOP REGULAR.TTF", 50)
ingreso = ''
ingreso_rect = pygame.Rect(boton_play["pos_x"]+10,boton_play["pos_y"]-(boton_play["alto"]*2-20),boton_play["ancho"]-20,boton_play["alto"])
crear_tabla()
lista_puntajes = obtener_datos_desde_tabla()
lista_ids = devolver_lista_id(lista_puntajes)

while estado:
    
    bandera_nombre = False
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            estado = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if verificar_click(boton_play, evento.pos):
                if len(ingreso)>0:
                    id = generar_id_unico(lista_ids,ingreso)
                    print(id)
                    opcion = iniciar_juego(ventana,calle, pasto, linea_ruta, espacio_entre_lineas, timer_segundos,ingreso,id)
                    lista_puntajes = obtener_datos_desde_tabla()
                    if opcion == "salir":
                        estado = False
                else:
                    bandera_nombre = True
            elif verificar_click(boton_scores, evento.pos):
                if len(lista_puntajes)>0:
                    if mostrar_tabla(ventana,[600,500],lista_puntajes,fondo_inicio,[ANCHO_VENTANA/4, 20]) == "salir":  
                        estado = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_BACKSPACE:
                ingreso = ingreso[0:-1]
            else:
                ingreso += evento.unicode
    ventana.blit(fondo_inicio, (0, 0))
    ventana.blit(titulo_inicio,(posicion_titulo[0],posicion_titulo[1]))
    ventana.blit(boton_play["img"],(boton_play["pos_x"],boton_play["pos_y"]))
    ventana.blit(boton_scores["img"],(boton_scores["pos_x"],boton_scores["pos_y"]))
    pygame.draw.rect(ventana, (255,0,51), ingreso_rect, 5)
    font_input_surface = font_input.render(ingreso,True,(255,0,51))
    ventana.blit(font_input_surface,(ingreso_rect.x+5,ingreso_rect.y+5))
    if len(ingreso)>0:
        bandera_nombre = True
    if not bandera_nombre:
        mostrar_texto(ventana,"ingrese su nombre",font_input,(255,0,51),(ingreso_rect.x+5,ingreso_rect.y+5))
    pygame.display.flip()
pygame.quit()