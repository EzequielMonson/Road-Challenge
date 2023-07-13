import pygame
import time
def obtener_superficies(path:str, filas:int, columnas:int)->list:
    lista = []
    superficie_imagen = pygame.image.load(path)
    fotograma_ancho = superficie_imagen.get_width() // columnas
    fotograma_alto = superficie_imagen.get_height() // filas
    for fila in range(filas):
        for columna in range(columnas):
            x = columna * fotograma_ancho
            y = fila * fotograma_alto
            # un pedacito de la imagen del sprite
            superficie_fotograma = superficie_imagen.subsurface(pygame.Rect(x, y, fotograma_ancho, fotograma_alto))
            lista.append(superficie_fotograma)
    return lista

class Vehiculo:
    def __init__(self, color:str, tamaño:tuple, bot:bool, velocidad:int, movimiento:bool, posicion:list, animacion_andando, vidas:int):
        """
        Constructor de la clase Vehiculo. Crea una instancia de Vehiculo con los atributos especificados.
        Argumentos:
            color (str): El color del vehículo.
            tamaño (tuple): Una tupla que representa el tamaño (ancho, alto) del vehículo.
            bot (bool): Un valor booleano que indica si el vehículo es controlado por la computadora (bot) o por un jugador humano.
            velocidad (int): La velocidad del vehículo.
            movimiento (bool): Un valor booleano que indica si el vehículo se está moviendo o no.
            posicion (list): Una lista que contiene las coordenadas x e y de la posición del vehículo.
            angulo (int): El ángulo de rotación del vehículo.
            animacion_andando: El path de la imagen de animación para cuando el vehículo está avanzando o frenando.
            vidas (int): El número de vidas del vehículo
        No retorna ningún valor.
        """
        self.color = color
        self.tamaño = tamaño
        self.bot = bot
        self.dic_animaciones = {
            'avanzar': obtener_superficies(animacion_andando, 2, 5),
            'explotar': obtener_superficies(r"img\explosion.png", 2, 5)
        }
        self.frame = 0
        self.animacion = self.dic_animaciones['avanzar'][self.frame]
        self.img = pygame.transform.scale(self.animacion, self.tamaño)
        self.velocidad = velocidad
        self.movimiento = movimiento
        self.posicion = posicion
        self.rect = pygame.Rect(self.posicion[0], self.posicion[1], self.tamaño[0], self.tamaño[1])
        self.colision = False
        self.animacion_terminada = True
        self.iniciar_animacion = False
        self.visible = True
        self.vidas = vidas
        self.vidas_restantes = self.vidas

    def devolver_estado(self):
        """
        Descripción: Devuelve el estado actual del movimiento del vehículo.
        Retorna: Un valor booleano que indica si el vehículo está en movimiento o no.
        """
        return self.movimiento

    def mover(self, pantalla, posicion_x_calle:int, ancho_calle:int) -> None:
        """
        Descripción: Mueve el vehículo en la pantalla según las condiciones dadas.
        Argumentos:
            pantalla: La superficie de la pantalla de juego en la que se dibuja el vehículo.
            posicion_x_calle: La posición x inicial de la calle en la que se mueve el vehículo.
            ancho_calle: El ancho de la calle por la que se mueve el vehículo.
        Retorna: No retorna ningún valor.
        """
        if self.movimiento:
            if self.color == "Amarillo" or (self.color == "Rojo" and self.bot):
                self.posicion[1] += self.velocidad
            elif self.color == "Verde":
                if self.posicion[0] <= posicion_x_calle:
                    self.posicion[0] += self.velocidad
                    self.posicion[1] += self.velocidad
                elif self.posicion[0] >= posicion_x_calle + ancho_calle - self.tamaño[0]:
                    self.posicion[0] -= self.tamaño[0]
                    self.posicion[1] += self.velocidad
                else:
                    self.posicion[1] += self.velocidad
            elif self.color == "Negro":
                self.posicion[1] += self.velocidad
            if self.posicion[0] < posicion_x_calle:
                self.posicion[0] = posicion_x_calle
            elif self.posicion[0] + self.tamaño[0] > posicion_x_calle + ancho_calle:
                self.posicion[0] = posicion_x_calle + ancho_calle - self.tamaño[0]
        self.rect = pygame.Rect(self.posicion[0], self.posicion[1], self.tamaño[0], self.tamaño[1])  # Actualizar la posición del rectángulo
        self.actualizar_frame
        self.dibujar(pantalla)

    def actualizar_frame(self, tiempo_actual:int, tiempo_anterior:int)->None:
        """
        Descripción: Actualiza el fotograma actual de la animación del vehículo basándose en el tiempo transcurrido desde el último fotograma.
        Argumentos:
            tiempo_actual: El tiempo actual del juego.
            tiempo_anterior: El tiempo en el que se actualizó el fotograma anteriormente.
        Retorna: No retorna ningún valor.
        """
        tiempo_transcurrido = tiempo_actual - tiempo_anterior
        if tiempo_transcurrido >= 0.025:
            if self.iniciar_animacion and not self.animacion_terminada:
                self.frame = self.frame + 1 if self.frame < 9 else 0
                if self.frame == 9:
                    self.animacion_terminada = True
                tiempo_anterior = tiempo_actual

    def explotar_auto(self):
        self.animacion = self.dic_animaciones['explotar']
        if self.animacion_terminada:
            self.iniciar_animacion = True
            self.animacion_terminada = False
            self.frame = 0
        self.img = pygame.transform.scale(self.animacion[self.frame], self.tamaño)
        if self.frame >= 9 or self.animacion_terminada:
            self.frame = 9

    def estabilizar(self):
        self.animacion = self.dic_animaciones['avanzar']
        if self.animacion_terminada:
            self.iniciar_animacion = True
            self.animacion_terminada = False
            self.frame = 0
        self.img = pygame.transform.scale(self.animacion[self.frame], self.tamaño)
        

    def derrapar(self):
        self.dic_animaciones['choque'] = obtener_superficies(r"img\Auto_choque.png", 2, 5)
        self.animacion = self.dic_animaciones['choque']
        if self.animacion_terminada:
            self.iniciar_animacion = True
            self.animacion_terminada = False
            self.frame = 0
        self.img = pygame.transform.scale(self.animacion[self.frame], self.tamaño)
            


    def dibujar(self, pantalla):
        """
        Descripción: Dibuja el vehículo en la pantalla de juego.
        Argumentos:
            pantalla: La superficie de la pantalla de juego en la que se dibuja el vehículo.
        Retorna: No retorna ningún valor.
        """
        if self.visible:
            pantalla.blit(self.img, (self.posicion[0], self.posicion[1]))
