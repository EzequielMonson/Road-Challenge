import pygame
import colores
import time
from funciones import *
from temporizador import iniciar_temporizador, mostrar_tiempo
from tamanio_posiciones import ALTO_VENTANA, LINEA_DER_X, LINEA_IZQ_X,meta_final
from puntajes import actualizar_datos_en_la_tabla
from clase import Vehiculo

def iniciar_juego(pantalla,dic_calle,dic_pasto,dic_linea_ruta, espacio_entre_lineas,timer_segundos,usuario,id_usuario):
    auto_principal = Vehiculo("Rojo",(50,60),False, 5,True,[0,0],r"img\Auto.png",3)
    tiempo_transcurrido = 0
    clock = pygame.time.Clock()
    segundos = clock.tick(60) / 1000
    pygame.time.set_timer(timer_segundos,100)
    auto_principal.posicion = [dic_calle['ancho']-auto_principal.tamaño[0]/2,600]
    total_inicial_enemigos = 1
    flag_boton_right = False
    flag_boton_left = False
    flag_boton_down = False
    bandera_salir = False
    lista_enemigos = []
    total_inicial_enemigos = 1
    score = 0
    tiempo_actual = time.time()
    tiempo_anterior = tiempo_actual
    tiempo_transcurrido = 0
    
    explosion_sonido = pygame.mixer.Sound(r"sonidos\explosion.wav")
    derrape_sonido = pygame.mixer.Sound(r"sonidos\derrape.wav")
    arranque_sonido = pygame.mixer.Sound(r"sonidos\arrancar.wav")
    arranque_sonido.set_volume(0.1)
    derrape_sonido.set_volume(0.1)
    explosion_sonido.set_volume(0.1)
    
    corriendo = True
    while corriendo:
        
        tiempo_actual = time.time()
        lista_eventos = pygame.event.get()
        for eventos in lista_eventos:
            if eventos.type == pygame.QUIT:
                corriendo = False
                resultado = "salir"
            elif eventos.type ==  pygame.KEYUP:
                if pygame.K_RIGHT or pygame.K_d:
                    flag_boton_right = False
                if pygame.K_LEFT or pygame.K_a:
                    flag_boton_left = False
                if pygame.K_DOWN or pygame.K_s:
                    flag_boton_down = False
            elif eventos.type == pygame.KEYDOWN:
                lista_teclas = pygame.key.get_pressed()
                if True in lista_teclas:
                    if lista_teclas[pygame.K_RIGHT] or lista_teclas[pygame.K_d]:
                        flag_boton_right = True
                    if lista_teclas[pygame.K_LEFT] or lista_teclas[pygame.K_a]:
                        flag_boton_left = True
                    if lista_teclas[pygame.K_DOWN] or lista_teclas[pygame.K_s]:
                        flag_boton_down = True
                    if lista_teclas[pygame.K_ESCAPE]:
                        bandera_salir = True
                        
            # Actualizar posición de la línea
            elif eventos.type == pygame.USEREVENT:
                if eventos.type == timer_segundos:
                    if flag_boton_left:
                        auto_principal.movimiento = True
                    elif flag_boton_right:
                        auto_principal.movimiento = True
                    elif flag_boton_down:
                        auto_principal.movimiento = False
                    else:
                        auto_principal.movimiento = True
        ################################################
        # Si el auto no colosionó  o no se detuvo,     #
        # verifica que no salga de la calle            #
        ################################################
        if auto_principal.movimiento and auto_principal.vidas >=0:
            arranque_sonido.play()
            derrape_sonido.stop()
            if flag_boton_left:
                auto_principal.posicion[0] = auto_principal.posicion[0] - auto_principal.velocidad
                if auto_principal.posicion[0]<dic_calle['pos_x']:
                    auto_principal.posicion[0] = dic_calle['pos_x'] 
            if flag_boton_right:
                auto_principal.posicion[0] = auto_principal.posicion[0] + auto_principal.velocidad
                if auto_principal.posicion[0] > dic_calle['pos_x']+dic_calle['ancho']-auto_principal.tamaño[0]:
                    auto_principal.posicion[0] = dic_calle['pos_x']+dic_calle['ancho']-auto_principal.tamaño[0]
        #############################################################
        #Si el auto frena o choca, las lineas y enemigos se detienen#
        #############################################################
        if not auto_principal.movimiento or auto_principal.vidas <0:
            derrape_sonido.play()
            arranque_sonido.stop()
            dic_linea_ruta['velocidad'] -= dic_linea_ruta['velocidad']
            if dic_linea_ruta['velocidad'] <=0:
                dic_linea_ruta['velocidad'] = 0
            for enemigo in lista_enemigos:
                if enemigo.color != "Negro": 
                    enemigo.posicion[1] -= (enemigo.velocidad * 2)
            score -= 50 
        ###########################################################
        # si el auto está avanzando las lineas se mueven          #
        ###########################################################
        for enemigo in lista_enemigos:
            enemigo.mover(pantalla, dic_calle["pos_x"], dic_calle["ancho"])
        if auto_principal.movimiento:
            dic_linea_ruta['velocidad'] += 0.025
            if dic_linea_ruta['velocidad'] >=6:
                dic_linea_ruta['velocidad'] = 6
        dic_linea_ruta['pos_y'] += dic_linea_ruta['velocidad']
        if dic_linea_ruta['pos_y'] >= dic_linea_ruta['alto']:
            dic_linea_ruta['pos_y'] = 0-dic_linea_ruta['alto']
        lista_enemigos, total_inicial_enemigos = actualizar_lista_enemigos(lista_enemigos,dic_calle['ancho'],dic_calle['pos_x'],total_inicial_enemigos,ALTO_VENTANA,5,dic_linea_ruta)
        pantalla.fill((0,0,0))
        dibujar_ruta(pantalla,dic_pasto,dic_calle,LINEA_DER_X,LINEA_IZQ_X,ALTO_VENTANA)
        dibujar_lineas_ruta(pantalla,colores.WHITE,[dic_linea_ruta['pos_x'],dic_linea_ruta['pos_y']],espacio_entre_lineas,dic_linea_ruta['alto'],dic_linea_ruta['ancho'])
        score = actualizar_pantalla(lista_enemigos, pantalla, auto_principal, score,dic_calle['pos_x'],dic_calle['ancho'],tiempo_actual, tiempo_anterior)
        verificar_colisiones(lista_enemigos)
        auto_principal.mover(pantalla, dic_calle['pos_x'], dic_calle['ancho'])
        font = pygame.font.SysFont("Arial", 50)
        texto = font.render("SCORE: {0}".format(score),True, colores.WHITE)
        pantalla.blit(texto,((dic_pasto['ancho']+10),10))
        texto_vidas = font.render(f"Vidas: {auto_principal.vidas}", True, (0, 0, 0))
        pantalla.blit(texto_vidas, (10, 10))
        if auto_principal.vidas >=0:
            tiempo_transcurrido = iniciar_temporizador(pantalla,tiempo_transcurrido,segundos)
        if auto_principal.vidas < 0:
            mostrar_game_over(pantalla, lista_enemigos, dic_pasto["ancho"], dic_pasto["alto"])
            auto_principal.actualizar_frame(tiempo_actual, tiempo_anterior)
            tiempo_transcurrido = tiempo_transcurrido
            
            if not auto_principal.frame >= 9:
                auto_principal.explotar_auto()
                explosion_sonido.play()
                arranque_sonido.stop()
                derrape_sonido.stop()
            else:
                auto_principal.visible = False
                explosion_sonido.stop()
                arranque_sonido.stop()
                derrape_sonido.stop()
            if bandera_salir:
                corriendo = False
                resultado = "volver"
        if tiempo_transcurrido <= -116 and tiempo_transcurrido > -120 and auto_principal.vidas >=0: 
            finalizar_recorrido(pantalla,meta_final,dic_linea_ruta,lista_enemigos, auto_principal)
        if auto_principal.rect.colliderect(pygame.Rect(meta_final['pos_x'],meta_final['pos_y'], meta_final['ancho'], meta_final['alto'])) or tiempo_transcurrido <= -118:
            score = score
            tiempo_transcurrido = tiempo_transcurrido
            actualizar_datos_en_la_tabla(id_usuario, usuario,score,auto_principal.vidas)
            arranque_sonido.stop()
            derrape_sonido.stop()
            corriendo = False
            resultado = "volver"
        pygame.display.flip()
    return resultado


