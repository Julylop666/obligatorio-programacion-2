"""escenas.py - Ilustraciones pixel art de la portada y la historia de introducción.

Todo se dibuja con figuras sobre una Surface chica y se agranda con "vecino más cercano"
(pixel art). Las escenas se arman UNA sola vez antes del bucle principal. Si en la carpeta
imagenes/ hay un PNG con el nombre de una escena, se usa ese en lugar del dibujo por código.
"""
import os
import pygame
from ajustes import (COLORES_PASTEL as C, PX_MUNDO, COLOR_DON_SALMON, COLOR_OJOS_JUGADOR, PELAJES,
                     RUTA_IMAGENES, ANCHO, ALTO)
from dibujo import dibujar_gato, pixelar, texto_centrado

TAM_ESCENA = (880, 320)       # tamaño en pantalla de las viñetas de la historia

_DELANTAL_GRANDE = (
    "....O....O....",
    "....O....O....",
    "...OOOOOOOO...",
    "..OAAAAAAAAO..",
    "..OAAAAAAAAO..",
    "..OAAAAAAAAO..",
    ".OAAAAAAAAAAO.",
    ".OAAAWWWWAAAO.",
    ".OAAAWWWWAAAO.",
    ".OAAAAAAAAAAO.",
    ".OOOOOOOOOOOO.",
)
_BRILLO = (
    "..Y..",
    "..Y..",
    "YYYYY",
    "..Y..",
    "..Y..",
)


def _agrandar(chica, factor=PX_MUNDO):
    """Agranda una Surface chica con vecino más cercano (pixel art nítido)."""
    return pygame.transform.scale(chica, (chica.get_width() * factor, chica.get_height() * factor))


def _imagen_opcional(nombre, tam):
    """Devuelve la ilustración propia imagenes/<nombre>.png escalada a tam, o None si no existe."""
    ruta = os.path.join(RUTA_IMAGENES, nombre + ".png")
    if not os.path.exists(ruta):
        return None
    try:
        return pygame.transform.smoothscale(pygame.image.load(ruta).convert_alpha(), tam)
    except pygame.error:
        return None


def _bandas_cielo(chica, colores):
    """Pinta el cielo con franjas horizontales (efecto atardecer pixel art)."""
    alto = chica.get_height()
    for i, color in enumerate(colores):
        pygame.draw.rect(chica, color, (0, i * alto // len(colores), chica.get_width(),
                                        alto // len(colores) + 1))


def _nube(chica, x, y):
    """Dibuja una nubecita de pixeles en (x, y)."""
    for dx, dy, w, h in ((2, 0, 8, 3), (0, 2, 14, 3), (4, -2, 5, 3)):
        pygame.draw.rect(chica, (255, 250, 245), (x + dx, y + dy, w, h))


def _cafeteria(chica, x, y):
    """Dibuja la fachada de la cafetería (96 x 50 pixeles de arte) con su cartelito en la ventana."""
    pared, ladrillo = (255, 236, 214), (255, 222, 196)
    pygame.draw.rect(chica, C["contorno"], (x, y, 96, 50))
    pygame.draw.rect(chica, pared, (x + 1, y + 1, 94, 48))
    for fila in range(y + 4, y + 49, 4):                                   # ladrillos
        pygame.draw.line(chica, ladrillo, (x + 1, fila), (x + 94, fila))
    pygame.draw.rect(chica, C["contorno"], (x + 18, y + 2, 60, 12))        # letrero de madera
    pygame.draw.rect(chica, C["madera_oscura"], (x + 19, y + 3, 58, 10))
    for i in range(5):                                                      # tacitas del letrero
        pygame.draw.rect(chica, C["leche"], (x + 26 + i * 10, y + 6, 5, 4))
        pygame.draw.rect(chica, C["cafe"], (x + 26 + i * 10, y + 6, 5, 1))
    for i in range(0, 100, 6):                                              # toldo a rayas
        color = (248, 160, 180) if (i // 6) % 2 == 0 else (255, 255, 255)
        pygame.draw.rect(chica, color, (x - 2 + i, y + 14, 6, 6))
        pygame.draw.rect(chica, color, (x - 1 + i, y + 20, 4, 2))
    pygame.draw.rect(chica, C["contorno"], (x + 6, y + 24, 46, 24))        # ventana
    pygame.draw.rect(chica, (196, 222, 244), (x + 7, y + 25, 44, 22))
    pygame.draw.rect(chica, (222, 238, 250), (x + 9, y + 26, 8, 3))        # reflejo
    pygame.draw.rect(chica, C["madera_oscura"], (x + 4, y + 47, 50, 3))    # alféizar
    pygame.draw.rect(chica, C["contorno"], (x + 17, y + 28, 22, 17))       # el cartelito
    pygame.draw.rect(chica, (255, 248, 224), (x + 18, y + 29, 20, 15))
    for i, color in enumerate(((248, 143, 150), (120, 170, 225), (248, 143, 150), (120, 170, 225))):
        pygame.draw.line(chica, color, (x + 20, y + 32 + i * 3), (x + 34 - (i % 2) * 3, y + 32 + i * 3))
    pygame.draw.rect(chica, (246, 206, 124), (x + 16, y + 28, 4, 2))        # cintas
    pygame.draw.rect(chica, (246, 206, 124), (x + 36, y + 28, 4, 2))
    pygame.draw.rect(chica, C["contorno"], (x + 62, y + 24, 24, 26))       # puerta
    pygame.draw.rect(chica, C["barra"], (x + 63, y + 25, 22, 25))
    pygame.draw.rect(chica, (196, 222, 244), (x + 67, y + 28, 14, 9))
    pygame.draw.rect(chica, C["dorado"], (x + 80, y + 40, 2, 3))            # picaporte


def _escena_calle():
    """Viñeta 1: el barrio, la cafetería y el cartelito con crayón. Devuelve una Surface."""
    chica = pygame.Surface((TAM_ESCENA[0] // PX_MUNDO, TAM_ESCENA[1] // PX_MUNDO))
    _bandas_cielo(chica, [C["cielo_a"], (255, 222, 204), C["cielo_b"], (255, 240, 220)])
    pygame.draw.circle(chica, (255, 236, 190), (182, 22), 12)
    pygame.draw.circle(chica, (255, 246, 214), (182, 22), 8)
    for x, y in ((14, 8), (96, 5), (146, 12)):
        _nube(chica, x, y)
    for x, ancho, techo, color in ((0, 32, 24, (238, 200, 200)), (30, 26, 34, (214, 206, 230)),
                                   (160, 28, 30, (238, 200, 200)), (186, 34, 18, (214, 206, 230))):
        pygame.draw.rect(chica, color, (x, techo, ancho, 62 - techo))
        for vx in range(x + 4, x + ancho - 4, 8):
            for vy in range(techo + 5, 56, 10):
                pygame.draw.rect(chica, (255, 246, 232), (vx, vy, 3, 4))
    _cafeteria(chica, 62, 12)
    pygame.draw.rect(chica, (214, 204, 222), (0, 62, 220, 18))              # vereda
    pygame.draw.rect(chica, (190, 180, 204), (0, 62, 220, 3))
    for x in range(10, 220, 22):
        pygame.draw.line(chica, (196, 186, 210), (x, 65), (x - 4, 80))
    pygame.draw.rect(chica, (96, 96, 120), (196, 28, 2, 36))                # farol
    pygame.draw.rect(chica, (246, 206, 124), (192, 24, 10, 6))
    pygame.draw.rect(chica, C["contorno"], (192, 24, 10, 1))
    pygame.draw.rect(chica, (178, 110, 80), (56, 56, 9, 8))                 # macetas
    pygame.draw.rect(chica, (150, 205, 150), (55, 50, 11, 7))
    pygame.draw.rect(chica, (178, 110, 80), (158, 56, 9, 8))
    pygame.draw.rect(chica, (150, 205, 150), (157, 50, 11, 7))
    escena = _agrandar(chica)
    dibujar_gato(escena, (120, 262), PELAJES[0][1], escala=1.33, ojos=COLOR_OJOS_JUGADOR)
    return escena


def _interior(chica):
    """Dibuja el interior de la cafetería (pared, estantes, ventana, mostrador) en la Surface chica."""
    pygame.draw.rect(chica, C["pared"], (0, 0, 220, 80))
    for x in range(0, 220, 8):                                              # papel tapiz a rayas
        pygame.draw.rect(chica, (250, 212, 202), (x, 0, 2, 56))
    pygame.draw.rect(chica, C["madera_oscura"], (0, 44, 220, 36))           # guardapared de madera
    pygame.draw.rect(chica, C["zocalo"], (0, 42, 220, 3))
    for repisa in (14, 30):                                                 # estantes con tacitas
        pygame.draw.rect(chica, C["contorno"], (92, repisa + 4, 110, 3))
        pygame.draw.rect(chica, C["barra"], (92, repisa + 4, 110, 2))
        for i, color in enumerate(((255, 240, 225), (248, 160, 180), (172, 202, 236), (246, 206, 124))):
            for x in (96 + i * 12, 148 + i * 12):
                pygame.draw.rect(chica, color, (x, repisa, 6, 4))
                pygame.draw.rect(chica, C["contorno"], (x, repisa + 3, 6, 1))
    pygame.draw.rect(chica, C["contorno"], (8, 6, 40, 34))                  # ventana con sol
    pygame.draw.rect(chica, (196, 222, 244), (10, 8, 36, 30))
    pygame.draw.circle(chica, (255, 240, 190), (36, 18), 6)
    pygame.draw.line(chica, (255, 255, 255), (28, 8), (28, 38))
    pygame.draw.line(chica, (255, 255, 255), (10, 23), (46, 23))
    pygame.draw.rect(chica, (248, 160, 180), (8, 6, 5, 34))                 # cortinas
    pygame.draw.rect(chica, (248, 160, 180), (43, 6, 5, 34))
    pygame.draw.line(chica, C["contorno"], (60, 0), (60, 12))               # lámpara colgante
    pygame.draw.rect(chica, C["dorado"], (54, 12, 12, 5))
    pygame.draw.rect(chica, (255, 240, 190), (56, 17, 8, 2))


def _mostrador(chica):
    """Dibuja el mostrador de madera (se pinta DESPUÉS de Don Salmón para que quede detrás)."""
    pygame.draw.rect(chica, C["contorno"], (0, 52, 220, 28))
    pygame.draw.rect(chica, C["barra_tapa"], (0, 53, 220, 4))
    pygame.draw.rect(chica, C["barra"], (0, 57, 220, 23))
    for x in range(8, 220, 16):
        pygame.draw.line(chica, (172, 126, 92), (x, 58), (x, 79))
    pygame.draw.ellipse(chica, C["contorno"], (150, 49, 22, 8))             # platito de agua
    pygame.draw.ellipse(chica, (255, 252, 246), (151, 50, 20, 6))
    pygame.draw.ellipse(chica, (150, 200, 240), (154, 51, 14, 3))


def _escena_salmon():
    """Viñeta 2: Don Salmón detrás del mostrador, hablando con el protagonista."""
    chica = pygame.Surface((TAM_ESCENA[0] // PX_MUNDO, TAM_ESCENA[1] // PX_MUNDO))
    _interior(chica)
    escena = _agrandar(chica)
    dibujar_gato(escena, (330, 150), COLOR_DON_SALMON, escala=2.67, lentes=True, chaleco=True)
    chica2 = pygame.Surface(chica.get_size(), pygame.SRCALPHA)
    _mostrador(chica2)
    escena.blit(_agrandar(chica2), (0, 0))
    dibujar_gato(escena, (640, 214), PELAJES[0][1], escala=2.0, ojos=COLOR_OJOS_JUGADOR, mirando=-1)
    return escena


def _escena_delantal():
    """Viñeta 3: Don Salmón le ofrece al protagonista el delantal básico."""
    chica = pygame.Surface((TAM_ESCENA[0] // PX_MUNDO, TAM_ESCENA[1] // PX_MUNDO))
    _interior(chica)
    _mostrador(chica)
    escena = _agrandar(chica)
    dibujar_gato(escena, (230, 200), COLOR_DON_SALMON, escala=2.67, lentes=True, chaleco=True)
    dibujar_gato(escena, (650, 200), PELAJES[0][1], escala=2.67, ojos=COLOR_OJOS_JUGADOR, mirando=-1)
    delantal = pixelar(_DELANTAL_GRANDE, {"O": C["contorno"], "A": (248, 160, 180), "W": (255, 255, 255)}, 8)
    escena.blit(delantal, delantal.get_rect(center=(440, 150)))
    brillo = pixelar(_BRILLO, {"Y": C["dorado"]}, 4)
    for x, y in ((360, 80), (520, 96), (400, 230), (500, 220)):
        escena.blit(brillo, (x, y))
    return escena


def _portada(fuente_titulo, fuente_sub):
    """Pantalla de título: atardecer, la cafetería y los gatos baristas. Devuelve una Surface."""
    chica = pygame.Surface((ANCHO // PX_MUNDO, ALTO // PX_MUNDO))
    colores = [(255, 200 + i * 4, 196 + i * 2) for i in range(10)]
    _bandas_cielo(chica, colores)
    pygame.draw.circle(chica, (255, 232, 196), (120, 104), 34)
    pygame.draw.circle(chica, (255, 246, 214), (120, 104), 26)
    for x, y in ((14, 70), (190, 64), (100, 78), (36, 20), (200, 26)):
        _nube(chica, x, y)
    for x, ancho, techo, color in ((0, 30, 100, (238, 200, 200)), (28, 24, 112, (214, 206, 230)),
                                   (176, 30, 104, (214, 206, 230)), (206, 34, 96, (238, 200, 200))):
        pygame.draw.rect(chica, color, (x, techo, ancho, 140 - techo))
        for vx in range(x + 4, x + ancho - 4, 8):
            for vy in range(techo + 5, 134, 10):
                pygame.draw.rect(chica, (255, 246, 232), (vx, vy, 3, 4))
    _cafeteria(chica, 72, 90)
    pygame.draw.rect(chica, (214, 204, 222), (0, 140, 240, 20))
    pygame.draw.rect(chica, (190, 180, 204), (0, 140, 240, 3))
    portada = _agrandar(chica)
    dibujar_gato(portada, (130, 568), COLOR_DON_SALMON, escala=2.0, lentes=True, chaleco=True)
    dibujar_gato(portada, (830, 568), PELAJES[0][1], {"delantal": True, "gorro": 2}, escala=2.0,
                 ojos=COLOR_OJOS_JUGADOR, mirando=-1)
    dibujar_gato(portada, (900, 590), PELAJES[1][1], {"delantal": True, "gorro": 1}, escala=1.67,
                 mirando=-1)
    for dx, dy, color in ((6, 6, C["zocalo"]), (0, 0, C["texto"])):          # título con sombra
        texto_centrado(portada, "Michi Café", fuente_titulo, color, (ANCHO // 2 + dx, 120 + dy))
    texto_centrado(portada, "2D", fuente_titulo, C["acento"], (ANCHO // 2, 200))
    texto_centrado(portada, "Un juego cozy de cafetería", fuente_sub, C["texto"], (ANCHO // 2, 262))
    return portada


def crear_escenas(fuente_titulo, fuente_sub):
    """Arma todas las ilustraciones una sola vez. Devuelve {nombre: Surface}.

    Nombres: 'portada', 'escena_calle', 'escena_salmon', 'escena_delantal'. Usa los PNG de
    imagenes/ cuando existen.
    """
    escenas = {
        "portada": ((ANCHO, ALTO), lambda: _portada(fuente_titulo, fuente_sub)),
        "escena_calle": (TAM_ESCENA, _escena_calle),
        "escena_salmon": (TAM_ESCENA, _escena_salmon),
        "escena_delantal": (TAM_ESCENA, _escena_delantal),
    }
    return {nombre: _imagen_opcional(nombre, tam) or dibujar() for nombre, (tam, dibujar) in escenas.items()}
