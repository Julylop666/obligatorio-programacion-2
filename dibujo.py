"""dibujo.py - Funciones de dibujo con figuras (el juego no usa imágenes externas).

Todas las funciones reciben la superficie donde dibujar. Así el estilo
ilustrado suave queda en un único lugar y se reutiliza para el jugador,
los clientes, Don Salmón y las pantallas de menú.
"""
import pygame
from ajustes import COLORES_PASTEL as C


def oscurecer(color, factor=0.8):
    """Devuelve el mismo color pero más oscuro (factor < 1)."""
    return tuple(int(canal * factor) for canal in color)


def dibujar_panel(pantalla, rect, color=None, radio=18):
    """Dibuja un panel redondeado con borde suave y devuelve su Rect."""
    color = color or C["panel"]
    rect = pygame.Rect(rect)
    pygame.draw.rect(pantalla, color, rect, border_radius=radio)
    pygame.draw.rect(pantalla, C["zocalo"], rect, width=3, border_radius=radio)
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
            pantalla.blit(fuente.render(linea, True, color), (rect.left, y))
            y += fuente.get_height() + interlineado
            linea = palabra
    if linea:
        pantalla.blit(fuente.render(linea, True, color), (rect.left, y))
        y += fuente.get_height() + interlineado
    return y


def texto_centrado(pantalla, texto, fuente, color, centro):
    """Escribe una línea de texto centrada en el punto dado."""
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, superficie.get_rect(center=centro))


def dibujar_item(pantalla, item, centro, escala=1.0):
    """Dibuja el ícono de un ítem del menú ('cafe' o 'medialuna')."""
    cx, cy = centro
    k = escala
    if item == "cafe":
        pygame.draw.ellipse(pantalla, C["sombra"], (cx - 13 * k, cy + 5 * k, 26 * k, 8 * k))
        pygame.draw.rect(pantalla, C["leche"], (cx - 10 * k, cy - 8 * k, 20 * k, 17 * k),
                         border_bottom_left_radius=int(8 * k), border_bottom_right_radius=int(8 * k))
        pygame.draw.ellipse(pantalla, C["cafe"], (cx - 10 * k, cy - 11 * k, 20 * k, 7 * k))
        pygame.draw.circle(pantalla, C["leche"], (int(cx + 11 * k), int(cy)), int(5 * k), max(1, int(2 * k)))
    else:
        pygame.draw.ellipse(pantalla, (225, 160, 80), (cx - 14 * k, cy - 7 * k, 28 * k, 15 * k))
        for dx in (-7, 0, 7):                       # los "gajos" de la medialuna
            pygame.draw.line(pantalla, (190, 120, 55), (cx + dx * k, cy - 6 * k),
                             (cx + dx * k, cy + 6 * k), max(1, int(2 * k)))


def dibujar_gato(pantalla, centro, color, ropa=None, escala=1.0, lentes=False):
    """Dibuja un gatito con figuras simples.

    ropa: diccionario {"delantal": bool, "gorro": 0-2, "calzado": 0-2} (opcional).
    lentes: True para dibujar los anteojitos de Don Salmón.
    """
    ropa = ropa or {}
    cx, cy = centro
    k = escala
    borde = oscurecer(color, 0.7)
    # cola
    pygame.draw.lines(pantalla, color, False,
                      [(cx + 14 * k, cy + 14 * k), (cx + 28 * k, cy + 8 * k), (cx + 30 * k, cy - 8 * k)],
                      max(2, int(6 * k)))
    # cuerpo y patas
    pygame.draw.ellipse(pantalla, color, (cx - 17 * k, cy - 4 * k, 34 * k, 30 * k))
    color_pata = [color, (120, 190, 235), (240, 120, 150)][ropa.get("calzado", 0)]
    for dx in (-10, 10):
        pygame.draw.ellipse(pantalla, color_pata, (cx + (dx - 6) * k, cy + 21 * k, 12 * k, 7 * k))
    if ropa.get("delantal"):
        pygame.draw.rect(pantalla, (255, 255, 255), (cx - 10 * k, cy + 1 * k, 20 * k, 21 * k),
                         border_radius=int(5 * k))
        pygame.draw.rect(pantalla, C["acento"], (cx - 10 * k, cy + 1 * k, 20 * k, 21 * k),
                         width=max(1, int(2 * k)), border_radius=int(5 * k))
    # orejas y cabeza
    for lado in (-1, 1):
        puntos = [(cx + lado * 14 * k, cy - 20 * k), (cx + lado * 13 * k, cy - 35 * k),
                  (cx + lado * 3 * k, cy - 27 * k)]
        pygame.draw.polygon(pantalla, color, puntos)
        interior = [(cx + lado * 11 * k, cy - 22 * k), (cx + lado * 11 * k, cy - 30 * k),
                    (cx + lado * 6 * k, cy - 26 * k)]
        pygame.draw.polygon(pantalla, C["rosa_oreja"], interior)
    pygame.draw.circle(pantalla, color, (int(cx), int(cy - 14 * k)), int(15 * k))
    # cara
    for lado in (-1, 1):
        pygame.draw.circle(pantalla, C["texto"], (int(cx + lado * 6 * k), int(cy - 15 * k)), max(1, int(2.5 * k)))
        pygame.draw.line(pantalla, borde, (cx + lado * 10 * k, cy - 8 * k), (cx + lado * 19 * k, cy - 9 * k), 1)
        pygame.draw.line(pantalla, borde, (cx + lado * 10 * k, cy - 6 * k), (cx + lado * 19 * k, cy - 4 * k), 1)
        if lentes:
            pygame.draw.circle(pantalla, C["texto"], (int(cx + lado * 6 * k), int(cy - 15 * k)),
                               int(5.5 * k), max(1, int(1.5 * k)))
    pygame.draw.polygon(pantalla, C["acento"], [(cx - 2 * k, cy - 11 * k), (cx + 2 * k, cy - 11 * k), (cx, cy - 8 * k)])
    # gorros
    if ropa.get("gorro") == 1:      # cofia
        pygame.draw.ellipse(pantalla, (255, 255, 255), (cx - 13 * k, cy - 34 * k, 26 * k, 12 * k))
        pygame.draw.ellipse(pantalla, C["azul"], (cx - 13 * k, cy - 34 * k, 26 * k, 12 * k), max(1, int(2 * k)))
    elif ropa.get("gorro") == 2:    # sombrero de chef
        pygame.draw.rect(pantalla, (255, 255, 255), (cx - 10 * k, cy - 36 * k, 20 * k, 14 * k))
        pygame.draw.circle(pantalla, (255, 255, 255), (int(cx - 8 * k), int(cy - 40 * k)), int(8 * k))
        pygame.draw.circle(pantalla, (255, 255, 255), (int(cx + 8 * k), int(cy - 40 * k)), int(8 * k))
        pygame.draw.circle(pantalla, (255, 255, 255), (int(cx), int(cy - 45 * k)), int(9 * k))
        pygame.draw.rect(pantalla, C["azul"], (cx - 10 * k, cy - 26 * k, 20 * k, 4 * k))
