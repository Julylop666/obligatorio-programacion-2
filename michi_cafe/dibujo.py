"""dibujo.py - Funciones de dibujo en estilo PIXEL ART (el juego no usa imágenes externas).

Los sprites (gatos, ítems, íconos) están escritos como grillas de texto: cada letra
es un pixel del arte y la paleta dice de qué color es cada letra. La función
pixelar() convierte la grilla en una Surface agrandada con "vecino más cercano",
así los pixeles quedan nítidos. Podés editar las grillas para cambiar el dibujo.
"""
import functools
import pygame
from ajustes import (COLORES_PASTEL as C, PX_GATO, PX_ITEM, COLOR_OJOS_CLIENTE)


# ---------------------------------------------------------------- colores y pixelado
def oscurecer(color, factor=0.8):
    """Devuelve el mismo color pero más oscuro (factor < 1)."""
    return tuple(int(canal * factor) for canal in color)


def aclarar(color, factor=0.5):
    """Devuelve el mismo color pero más claro (factor entre 0 y 1)."""
    return tuple(int(canal + (255 - canal) * factor) for canal in color)


@functools.lru_cache(maxsize=None)
def _pixelar(grilla, paleta, px):
    """Versión con caché de pixelar() (los argumentos tienen que ser hashables)."""
    colores = dict(paleta)
    ancho = max(len(fila) for fila in grilla)
    chica = pygame.Surface((ancho, len(grilla)), pygame.SRCALPHA)
    for y, fila in enumerate(grilla):
        for x, letra in enumerate(fila):
            if letra in colores:
                chica.set_at((x, y), colores[letra])
    return pygame.transform.scale(chica, (ancho * px, len(grilla) * px))


def pixelar(grilla, paleta, px):
    """Convierte una grilla de texto en una Surface pixel art agrandada px veces.

    grilla: lista de strings (una letra = un pixel, '.' = transparente).
    paleta: diccionario {letra: (r, g, b)}.
    """
    return _pixelar(tuple(grilla), tuple(sorted(paleta.items())), px)


# ---------------------------------------------------------------- paneles y texto
def dibujar_panel(pantalla, rect, color=None, radio=18):
    """Dibuja un panel pixel art (esquinas escalonadas) y devuelve su Rect.

    El parámetro radio se conserva por compatibilidad y no se usa.
    """
    color = color or C["panel"]
    rect = pygame.Rect(rect)
    b = 4                                            # grosor del borde (un pixel del mundo)
    x, y, w, h = rect
    for caja in ((x + b, y, w - 2 * b, h), (x, y + b, w, h - 2 * b)):
        pygame.draw.rect(pantalla, C["zocalo"], caja)
    for caja in ((x + 2 * b, y + b, w - 4 * b, h - 2 * b), (x + b, y + 2 * b, w - 2 * b, h - 4 * b)):
        pygame.draw.rect(pantalla, color, caja)
    return rect


def texto_envuelto(pantalla, texto, fuente, color, rect, interlineado=4):
    """Escribe texto partiéndolo en líneas para que entre en el rect.

    Devuelve la coordenada y donde terminó el texto.
    """
    y = rect.top
    linea = ""
    for palabra in texto.split():
        prueba = (linea + " " + palabra).strip()
        if fuente.size(prueba)[0] <= rect.width:
            linea = prueba
        else:
            pantalla.blit(fuente.render(linea, False, color), (rect.left, y))
            y += fuente.get_height() + interlineado
            linea = palabra
    if linea:
        pantalla.blit(fuente.render(linea, False, color), (rect.left, y))
        y += fuente.get_height() + interlineado
    return y


def texto_centrado(pantalla, texto, fuente, color, centro):
    """Escribe una línea de texto centrada en el punto dado."""
    superficie = fuente.render(texto, False, color)
    pantalla.blit(superficie, superficie.get_rect(center=centro))


# ---------------------------------------------------------------- ítems (pixel art)
_PAL_ITEM = {"O": C["contorno"], "W": (255, 252, 246), "M": (244, 228, 205), "C": C["cafe"],
             "Y": (236, 174, 86), "D": (203, 132, 58), "K": C["chocolate"], "Q": C["caramelo"]}

_CAFE = (
    ".OOOOOOO..",
    "OMMCCMMO..",
    "OWWWWWWOOO",
    "OWWWWWWO.O",
    "OWWWWWWOOO",
    ".OWWWWOO..",
    "..OOOOOO..",
)
_MEDIALUNA = (
    "....OOOO....",
    "..OOYYYYOO..",
    ".OYYDYYDYYO.",
    "OYYO.OO.OYYO",
    "OYO......OYO",
    ".O........O.",
)


def _con_puntos(grilla, puntos, letra):
    """Devuelve una copia de la grilla con la letra puesta en cada (x, y) de puntos."""
    filas = [list(fila) for fila in grilla]
    for x, y in puntos:
        filas[y][x] = letra
    return tuple("".join(fila) for fila in filas)


ITEMS_PIXEL = {
    "cafe": _CAFE,
    "medialuna": _MEDIALUNA,
    # chispas de chocolate: puntitos oscuros sobre la medialuna
    "medialuna_chispas": _con_puntos(_MEDIALUNA, [(5, 1), (3, 2), (6, 2), (9, 2), (2, 3), (10, 3)], "K"),
    # dulce de leche: baño de caramelo con un par de gotas
    "medialuna_dulce": _con_puntos(_MEDIALUNA, [(4, 1), (5, 1), (6, 1), (7, 1), (3, 2), (5, 2), (6, 2),
                                                (8, 2), (2, 3), (9, 3)], "Q"),
}


def dibujar_item(pantalla, item, centro, escala=1.0, base=False, px=None):
    """Dibuja el ícono pixel art de un ítem ('cafe', 'medialuna', 'medialuna_chispas', ...).

    centro: punto central del ítem (o el punto de apoyo de abajo si base=True).
    px: tamaño del pixel; si no se indica se calcula a partir de escala.
    """
    px = px or max(1, int(escala * 2.5 + 0.5))
    sprite = pixelar(ITEMS_PIXEL.get(item, _CAFE), _PAL_ITEM, px)
    rect = sprite.get_rect()
    if base:
        rect.midbottom = centro
    else:
        rect.center = centro
    pantalla.blit(sprite, rect)


# ---------------------------------------------------------------- gatos (pixel art)
ALTO_SOMBRERO = 6      # filas libres arriba de la cabeza para los gorros
_ZAPATOS = [None, (120, 190, 235), (240, 120, 150)]    # color según el nivel de calzado

# Cabeza y cuerpo (16 x 15). O = contorno, F = pelaje, L = pelaje claro, E = ojo,
# P = interior de la oreja, N = nariz.
_GATO_CUERPO = (
    "..OO........OO..",
    ".OFFO......OFFO.",
    ".OFPFOOOOOOFPFO.",
    ".OFFFFFFFFFFFFO.",
    ".OFFFFFFFFFFFFO.",
    ".OFFEEFFFFEEFFO.",
    ".OFFEEFFFFEEFFO.",
    ".OFFFFFNNFFFFFO.",
    ".OFFFLLLLLLFFFO.",
    "..OFFFFFFFFFFO..",
    "...OOOOOOOOOO...",
    "...OFFFFFFFFO...",
    "...OFLLLLLLFO...",
    "...OFLLLLLLFO...",
    "...OFFFFFFFFO...",
)
_PIES_1 = "...OSSSOOSSSO..."                      # fila de las patitas (S = zapato o pelaje)
_PIES_2 = {0: "....OOO..OOO....", 1: "....OOO.........",
           2: "....OOO..OOO....", 3: ".........OOO...."}   # al caminar una patita se levanta
_COLA_PELO = [(13, 14), (14, 14), (14, 13), (14, 12), (14, 11)]
_COLA_BORDE = [(13, 13), (15, 11), (15, 12), (15, 13), (15, 14), (13, 15), (14, 15), (14, 10)]
_ANTEOJOS = ([(x, 4) for x in (3, 4, 5, 6, 9, 10, 11, 12)] + [(x, 7) for x in (3, 4, 5, 6, 9, 10, 11, 12)]
             + [(x, y) for x in (3, 6, 9, 12) for y in (5, 6)] + [(7, 5), (8, 5)])
# prendas (letras: W blanco, P rosa, A delantal rosa, V chaleco)
_COFIA = (".....OOOOOO.....",
          "....OWWWWWWO....",
          "....OPPPPPPO....")                    # empieza una fila arriba de la cabeza
_SOMBRERO = ("....OOOOOOOO....",
             "...OWWWWWWWWO...",
             "..OWWWWWWWWWWO..",
             "..OWWWWWWWWWWO..",
             "...OWWWWWWWWO...",
             "....OWWWWWWO....",
             "....OPPPPPPO....")                 # empieza cinco filas arriba de la cabeza
_DELANTAL = ("......WWWW......",
             "....AAAAAAAA....",
             "....AAAAAAAA....",
             "....AAWWWWAA....",
             "....AAWWWWAA....")                 # filas 10 a 14 del cuerpo
_CHALECO = ("................",
            "....VVV..VVV....",
            "....VVV..VVV....",
            "....VVV..VVV....",
            "....VVV..VVV....")


@functools.lru_cache(maxsize=None)
def _construir_gato(color, ojos, gorro, delantal, calzado, lentes, chaleco, frame):
    """Arma (una sola vez por combinación) el sprite chico de un gato. Devuelve una Surface."""
    chica = pygame.Surface((16, ALTO_SOMBRERO + 17), pygame.SRCALPHA)
    dy = ALTO_SOMBRERO - (1 if frame in (1, 3) else 0)       # al caminar el cuerpo "rebota"
    zapato = _ZAPATOS[calzado] or color
    paleta = {"O": oscurecer(color, 0.38), "F": color, "L": aclarar(color, 0.55), "E": ojos,
              "P": C["rosa_oreja"], "N": C["acento"], "S": zapato}
    ropa = {"O": C["contorno"], "W": (255, 255, 255), "P": (248, 160, 180), "A": (248, 160, 180),
            "V": (112, 156, 124)}

    def poner(grilla, fila0, colores):
        """Copia una grilla de texto sobre el sprite, desde la fila fila0, usando esa paleta."""
        for y, fila in enumerate(grilla):
            for x, letra in enumerate(fila):
                if letra in colores and 0 <= fila0 + y < chica.get_height():
                    chica.set_at((x, fila0 + y), colores[letra])

    for x, y in _COLA_PELO:
        chica.set_at((x, dy + y), color)
    for x, y in _COLA_BORDE:
        chica.set_at((x, dy + y), paleta["O"])
    poner(_GATO_CUERPO, dy, paleta)
    poner((_PIES_1, _PIES_2[frame]), dy + 15, paleta)
    if chaleco:
        poner(_CHALECO, dy + 10, ropa)
    if delantal:
        poner(_DELANTAL, dy + 10, ropa)
    if lentes:
        for x, y in _ANTEOJOS:
            chica.set_at((x, dy + y), (214, 170, 90))      # marco dorado
    if gorro == 1:
        poner(_COFIA, dy - 1, ropa)
    elif gorro == 2:
        poner(_SOMBRERO, dy - 5, ropa)
    return chica


def frame_caminata(t_anim, camina):
    """Devuelve qué cuadro de animación (0 a 3) corresponde: 0 si está quieto."""
    if not camina:
        return 0
    return (1, 0, 3, 2)[int(t_anim * 9) % 4]


def dibujar_gato(pantalla, centro, color, ropa=None, escala=1.0, lentes=False, ojos=None,
                 frame=0, mirando=1, chaleco=False):
    """Dibuja un gatito pixel art con sombra.

    ropa: diccionario {"delantal": bool, "gorro": 0-2, "calzado": 0-2} (opcional).
    lentes / chaleco: los anteojitos y el chaleco tejido de Don Salmón.
    ojos: color de ojos (por defecto oscuros; el protagonista los tiene verdes).
    frame: cuadro de animación (0 quieto; 1 a 3 caminando). mirando: 1 derecha, -1 izquierda.
    """
    ropa = ropa or {}
    px = max(1, round(escala * PX_GATO))
    sprite = _construir_gato(tuple(color), tuple(ojos or COLOR_OJOS_CLIENTE), ropa.get("gorro", 0),
                             bool(ropa.get("delantal")), ropa.get("calzado", 0), lentes,
                             chaleco or bool(ropa.get("chaleco")), frame)
    sprite = pygame.transform.scale(sprite, (sprite.get_width() * px, sprite.get_height() * px))
    if mirando < 0:
        sprite = pygame.transform.flip(sprite, True, False)
    rect = sprite.get_rect(midbottom=(round(centro[0]), round(centro[1]) + 7 * px))
    sombra = pygame.Rect(0, 0, 14 * px, 4 * px)
    sombra.center = (rect.centerx, rect.bottom - px)
    pygame.draw.ellipse(pantalla, C["sombra"], sombra)
    pantalla.blit(sprite, rect)


def dibujar_bandeja(pantalla, centro, items, capacidad, color, mirando=1, frame=0):
    """Dibuja la bandeja que el gato lleva en la mano (como un mozo), con los ítems arriba.

    El ancho de la bandeja crece con la capacidad (la mejoran los gorros de la tienda).
    """
    cx, cy = centro
    px, d = PX_GATO, mirando
    borde = oscurecer(color, 0.38)
    y_pies = cy + 7 * px - (px if frame in (1, 3) else 0)      # acompaña el rebote al caminar
    ancho = capacidad * 26 + 10
    centro_x = cx + d * (30 + ancho // 2)
    y_plato = y_pies - 38                                       # altura de los hombros
    hombro = (cx + d * 13, y_pies - 16)
    mano = (centro_x, y_plato + 14)
    pygame.draw.line(pantalla, borde, hombro, mano, 11)         # brazo levantado
    pygame.draw.line(pantalla, color, hombro, mano, 5)
    palma = pygame.Rect(0, 0, 16, 12)
    palma.center = mano
    pygame.draw.rect(pantalla, borde, palma.inflate(4, 4))
    pygame.draw.rect(pantalla, color, palma)
    plato = pygame.Rect(0, 0, ancho, 8)                         # la bandeja
    plato.midtop = (centro_x, y_plato)
    pygame.draw.rect(pantalla, C["contorno"], plato.inflate(6, 6))
    pygame.draw.rect(pantalla, C["metal"], plato)
    pygame.draw.rect(pantalla, C["metal_oscuro"], (plato.left, plato.bottom - 3, ancho, 3))
    pygame.draw.line(pantalla, C["leche"], plato.topleft, (plato.right - 1, plato.top), 2)
    for lado in (plato.left, plato.right - 4):                  # bordecitos de la bandeja
        pygame.draw.rect(pantalla, C["contorno"], (lado - 1, plato.top - 5, 6, 6))
        pygame.draw.rect(pantalla, C["metal"], (lado, plato.top - 4, 4, 4))
    for i, item in enumerate(items):                            # lo que lleva encima
        dibujar_item(pantalla, item, (plato.left + 13 + i * 26, plato.top - 1), base=True, px=PX_ITEM)
