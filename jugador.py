"""jugador.py - Clase Jugador: el gato barista que controlamos."""
import pygame
from ajustes import (TAM_JUGADOR, VELOCIDAD_BASE, CAPACIDAD_BASE, POS_INICIAL,
                     ZONA_JUEGO, TAZA_VACIA, TIENDA)
from dibujo import dibujar_gato, dibujar_item


def leer_direccion(teclas):
    """Convierte las teclas apretadas (WASD o flechas) en un vector de dirección.

    Devuelve un Vector2 normalizado (largo 1) o (0, 0) si no hay movimiento,
    así en diagonal no se avanza más rápido.
    """
    x = (teclas[pygame.K_d] or teclas[pygame.K_RIGHT]) - (teclas[pygame.K_a] or teclas[pygame.K_LEFT])
    y = (teclas[pygame.K_s] or teclas[pygame.K_DOWN]) - (teclas[pygame.K_w] or teclas[pygame.K_UP])
    direccion = pygame.math.Vector2(x, y)
    if direccion.length_squared() > 0:
        direccion = direccion.normalize()
    return direccion


class Jugador(pygame.sprite.Sprite):
    """El gato barista: se mueve, lleva una bandeja y se puede vestir con ropa de la tienda."""

    def __init__(self, color_pelaje):
        """Crea al jugador con el color de pelaje elegido y los atributos base."""
        super().__init__()
        self.color = color_pelaje
        # atributos que mejora la ropa
        self.velocidad = VELOCIDAD_BASE
        self.capacidad_bandeja = CAPACIDAD_BASE
        self.multiplicador_propina = 1.0
        self.ropa = {"delantal": False, "gorro": 0, "calzado": 0}
        self.compras = set()
        # estado de trabajo
        self.bandeja = []             # ítems que lleva ("cafe", "medialuna")
        self.taza = TAZA_VACIA        # progreso del café con leche
        # posición (float) y rect para colisiones
        self.rect = pygame.Rect(0, 0, TAM_JUGADOR, TAM_JUGADOR)
        self.pos = pygame.math.Vector2(POS_INICIAL)
        self.rect.center = POS_INICIAL

    def reiniciar_posicion(self):
        """Vuelve al jugador al inicio y vacía bandeja y taza (se usa al empezar cada día)."""
        self.pos = pygame.math.Vector2(POS_INICIAL)
        self.rect.center = POS_INICIAL
        self.bandeja = []
        self.taza = TAZA_VACIA

    def hay_espacio(self):
        """Devuelve True si todavía entra otro ítem en la bandeja."""
        return len(self.bandeja) < self.capacidad_bandeja

    def agregar_item(self, item):
        """Agrega un ítem a la bandeja. Devuelve True si pudo, False si estaba llena."""
        if not self.hay_espacio():
            return False
        self.bandeja.append(item)
        return True

    def equipar(self, clave):
        """Aplica la prenda de la tienda indicada: cambia el atributo y la ropa visible."""
        prenda = TIENDA[clave]
        self.compras.add(clave)
        self.ropa[prenda["slot"]] = prenda["nivel"] if prenda["slot"] != "delantal" else True
        if prenda["atributo"] == "velocidad":
            self.velocidad = VELOCIDAD_BASE * prenda["valor"]
        elif prenda["atributo"] == "capacidad_bandeja":
            self.capacidad_bandeja = prenda["valor"]
        elif prenda["atributo"] == "multiplicador_propina":
            self.multiplicador_propina = prenda["valor"]

    def mover(self, dt, teclas, obstaculos):
        """Mueve al gato en 8 direcciones, chocando con los obstáculos y el borde del salón.

        Se mueve primero en X y después en Y para poder "deslizar" contra las mesas.
        """
        paso = leer_direccion(teclas) * self.velocidad * dt
        for eje in ("x", "y"):
            anterior = self.pos.copy()
            if eje == "x":
                self.pos.x += paso.x
            else:
                self.pos.y += paso.y
            self.rect.center = (round(self.pos.x), round(self.pos.y))
            if self.rect.collidelist(obstaculos) != -1:
                self.pos = anterior                # chocó: deshace este eje
                self.rect.center = (round(self.pos.x), round(self.pos.y))
        self.rect.clamp_ip(ZONA_JUEGO)
        self.pos.update(self.rect.center)

    def dibujar(self, pantalla):
        """Dibuja al gato con su ropa y, arriba de la cabeza, lo que lleva en la bandeja."""
        cx, cy = self.rect.centerx, self.rect.centery - 6
        dibujar_gato(pantalla, (cx, cy), self.color, self.ropa)
        for i, item in enumerate(self.bandeja):
            dibujar_item(pantalla, item, (cx - 14 * (len(self.bandeja) - 1) + i * 28, cy - 62), 0.9)
