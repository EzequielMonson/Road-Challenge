import pygame
from funciones import mostrar_texto
from colores import WHITE

def iniciar_temporizador(ventana, tiempo_transcurrido, segundos):
    # Actualizar el temporizador
    if tiempo_transcurrido > -119:
        tiempo_transcurrido -= segundos  # Sumar segundos al tiempo transcurrido
    else:
        tiempo_transcurrido = tiempo_transcurrido
    # Calcular minutos y segundos
    minutos = tiempo_transcurrido // 60 * -1
    if minutos > 1:
        minutos = 0
    segundos_restantes = tiempo_transcurrido % 60
    mostrar_texto(ventana, "Tiempo: {0:02d}:{1:02d}".format(int(minutos), int(segundos_restantes)), pygame.font.SysFont("Arial", 20), WHITE, (1000, 100))
    pygame.display.update()
    return tiempo_transcurrido

def mostrar_tiempo(tiempo_transcurrido)->str:
    minutos = tiempo_transcurrido // 60 * -1
    if minutos > 1:
        minutos = 0
    segundos_restantes = tiempo_transcurrido % 60
    tiempo = "{0:02d}:{1:02d}".format(int(minutos), int(segundos_restantes))
    return tiempo