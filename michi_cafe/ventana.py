"""ventana.py - La ventana del salón: muestra el paso del tiempo, de la mañana a la tarde.

El cielo avanza según cuánto de la meta del día lleva el jugador (0 = recién abrió la cafetería,
1 = meta cumplida). Nunca retrocede dentro del mismo día: si tirás algo al tacho y baja el dinero,
el sol no vuelve para atrás. Todo se dibuja en pixel art sobre una Surface chica que se agranda.
"""
import math
import pygame
from ajustes import (COLORES_PASTEL as C, PX_MUNDO, POS_VENTANA, VELOCIDAD_CIELO, VELOCIDAD_NUBES,
                     MOMENTOS_DIA)
from dibujo import oscurecer

# tamaño en pixeles del mundo: el vidrio entra dentro del marco, y el alféizar sobresale
ANCHO_VENTANA, ALTO_VENTANA = 50, 18
POS_VIDRIO = (3, 2)
TAM_VIDRIO = (44, 11)
BANDAS_CIELO = 6                 # el cielo se pinta en franjas (efecto pixel art)


def mezclar(a, b, t):
    """Mezcla dos colores (t = 0 da a, t = 1 da b). Sirve para tuplas de cualquier largo."""
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def momento_del_dia(progreso):
    """Devuelve un diccionario con los colores del cielo para ese progreso (0 a 1)."""
    progreso = max(0.0, min(1.0, progreso))
    for antes, despues in zip(MOMENTOS_DIA, MOMENTOS_DIA[1:]):
        if progreso <= despues["t"]:
            t = (progreso - antes["t"]) / (despues["t"] - antes["t"])
            return {clave: mezclar(antes[clave], despues[clave], t) for clave in antes if clave != "t"}
    return {clave: valor for clave, valor in MOMENTOS_DIA[-1].items() if clave != "t"}


def _construir_marco():
    """Arma (una vez) el marco, las cortinas y el alféizar. El vidrio queda transparente."""
    marco = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
    pygame.draw.rect(marco, C["contorno"], (0, 14, 50, 4))                # alféizar
    pygame.draw.rect(marco, C["barra_tapa"], (1, 14, 48, 2))
    pygame.draw.line(marco, C["blanco"], (2, 14), (47, 14))
    pygame.draw.rect(marco, C["contorno"], (1, 0, 48, 15))                # cuerpo del marco
    pygame.draw.rect(marco, C["leche"], (2, 1, 46, 13))
    marco.fill((0, 0, 0, 0), (*POS_VIDRIO, *TAM_VIDRIO))                  # hueco del vidrio
    pygame.draw.rect(marco, C["leche"], (24, 2, 2, 11))                   # cruz de la ventana
    pygame.draw.rect(marco, C["leche"], (3, 7, 44, 1))
    for x in (3, 42):                                                     # cortinas
        pygame.draw.rect(marco, C["cortina"], (x, 2, 5, 11))
        pygame.draw.line(marco, oscurecer(C["cortina"], 0.85), (x + 2, 2), (x + 2, 12))
        pygame.draw.rect(marco, oscurecer(C["cortina"], 0.7), (x, 8, 5, 1))   # lazo
    for x, y in ((12, 3), (11, 4), (10, 5), (33, 3), (32, 4), (31, 5)):   # brillos del vidrio
        marco.set_at((x, y), (255, 255, 255, 120))
    return marco


class VentanaDia:
    """La ventana con el cielo: guarda el progreso del día y se dibuja sola."""

    def __init__(self):
        """Empieza de mañana, con el marco ya armado."""
        self.marco = _construir_marco()
        self.t = 0.0              # tiempo acumulado (mueve las nubes)
        self.progreso = 0.0       # lo que se ve ahora (0 a 1)
        self.objetivo = 0.0       # hacia dónde va el cielo (nunca baja dentro del día)

    def reiniciar(self):
        """Vuelve a la mañana (se usa al empezar cada día y cada partida)."""
        self.progreso = 0.0
        self.objetivo = 0.0

    def actualizar(self, dt, avance):
        """Mueve las nubes y acerca el cielo al avance del día (0 a 1) de a poco, sin saltos."""
        self.t += dt
        self.objetivo = max(self.objetivo, min(1.0, avance))
        self.progreso += (self.objetivo - self.progreso) * min(1.0, dt * VELOCIDAD_CIELO)
        if abs(self.objetivo - self.progreso) < 0.0005:
            self.progreso = self.objetivo

    def _pintar_cielo(self):
        """Dibuja lo que se ve por el vidrio: cielo, sol, nubes y colinas. Devuelve una Surface chica."""
        ancho, alto = TAM_VIDRIO
        colores = momento_del_dia(self.progreso)
        cielo = pygame.Surface(TAM_VIDRIO)
        for y in range(alto):                                          # cielo en franjas
            franja = round(y / (alto - 1) * (BANDAS_CIELO - 1)) / (BANDAS_CIELO - 1)
            pygame.draw.line(cielo, mezclar(colores["arriba"], colores["horizonte"], franja), (0, y), (ancho, y))
        # el sol cruza de izquierda a derecha en arco: alto al mediodía, bajito a la mañana y a la tarde
        angulo = math.pi * (0.12 + 0.76 * self.progreso)
        sol_x = 8 + self.progreso * 28
        sol_y = 9 - math.sin(angulo) * 7
        halo = mezclar(colores["sol"], colores["horizonte"], 0.55)
        pygame.draw.circle(cielo, halo, (round(sol_x), round(sol_y)), 4)
        pygame.draw.circle(cielo, colores["sol"], (round(sol_x), round(sol_y)), 2)
        for y, inicio, velocidad in ((1, 4, 1.0), (3, 22, 0.7), (2, 38, 1.3)):   # nubes que pasan despacio
            x = (inicio - self.t * VELOCIDAD_NUBES * velocidad) % (ancho + 16) - 12
            for dx, dy, w in ((2, 0, 5), (0, 1, 10), (1, 2, 8)):
                pygame.draw.rect(cielo, colores["nube"], (round(x) + dx, y + dy, w, 1))
        for x in range(ancho):                                         # dos filas de colinas verdes
            atras = 6 + round(1.5 * math.sin(x * 0.20 + 0.8))
            frente = 8 + round(1.0 * math.sin(x * 0.33 + 2.4))
            pygame.draw.line(cielo, colores["colina_atras"], (x, atras), (x, alto))
            pygame.draw.line(cielo, colores["colina_frente"], (x, frente), (x, alto))
        return cielo

    def dibujar(self, pantalla):
        """Dibuja la ventana completa (cielo + marco) en su lugar de la pared."""
        chica = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        chica.blit(self._pintar_cielo(), POS_VIDRIO)
        chica.blit(self.marco, (0, 0))
        pantalla.blit(pygame.transform.scale(chica, (ANCHO_VENTANA * PX_MUNDO, ALTO_VENTANA * PX_MUNDO)),
                      POS_VENTANA)