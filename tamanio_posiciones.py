import pygame
ANCHO_VENTANA = 1200
ALTO_VENTANA = 700
#tamaño y posicion pasto
pasto = { 'ancho' : ANCHO_VENTANA - ANCHO_VENTANA/3,
        'alto' : ALTO_VENTANA,
        'pos_x' : 0,
        'pos_y' : 0}
#tamaño y posicion calle
calle = { 'ancho' : pasto['ancho']/2,
        'alto' : pasto['alto'],
        'pos_x' : pasto['ancho']/2/2,
        'pos_y' : 0}

#lineas laterales de la calle, tmaño y posicion
LINEA_IZQ_X = calle['pos_x']
LINEA_DER_X = pasto['ancho'] - calle['pos_x']
x_linea = calle['ancho'] // 2
y_linea = calle['alto']
linea_ruta = {'ancho': 10,
            'alto': 100,
            'pos_x' : calle['pos_x']+calle['pos_x']- 10,
            'pos_y' : -calle['alto']/2,
            'velocidad': 0.025}
espacio_entre_lineas = linea_ruta['alto']
tamaño_titulo = [ANCHO_VENTANA - ANCHO_VENTANA/3,ALTO_VENTANA/4]
posicion_titulo = [ANCHO_VENTANA/6,ALTO_VENTANA/2 - tamaño_titulo[1]]
boton_play = {
    "ancho" :  ANCHO_VENTANA/3,
    "alto" : 80,
    "pos_x" : ANCHO_VENTANA/3,
    "pos_y" : ALTO_VENTANA/2+(50*2),
    "img" : pygame.image.load(r"img\boton_play.png")
}
boton_scores = {
    "ancho" :  ANCHO_VENTANA/3,
    "alto" : 80,
    "pos_x" : ANCHO_VENTANA/3,
    "pos_y" : ALTO_VENTANA/2+(50*4),
    "img" : pygame.image.load(r"img\boton_scores.png")
}

meta_final = {
    'ancho': calle['ancho'],
    'alto': 100,
    'pos_x': calle['pos_x'],
    'pos_y': -100,
    'img': pygame.image.load(r"img\meta.png")
}
