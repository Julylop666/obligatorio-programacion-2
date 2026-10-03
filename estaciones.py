"""estaciones.py - Estaciones de la barra y mesas del salón.

Todas las estaciones comparten el método interactuar(jugador), que devuelve
una tupla (mensaje, sonido, dinero_ganado). Así main.py las trata igual.
"""
import pygame
from ajustes import (COLORES_PASTEL as C, ESTACIONES_RECT, CENTROS_MESAS, TAM_MESA,
                     DESPLAZAMIENTO_ASIENTO, TAZA_VACIA, TAZA_LECHE, TAZA_CALIENTE, ESPERANDO)
from dibujo import dibujar_item


class Estacion:
    """Estación genérica de la barra. Las hijas implementan dibujar_icono e interactuar."""

    def __init__(self, clave, nombre):
        """Crea la estación en la posición definida en ajustes.ESTACIONES_RECT."""
        self.nombre = nombre
        self.rect = pygame.Rect(ESTACIONES_RECT[clave])

    def dibujar_icono(self, pantalla):
        """Dibuja el ícono propio de la estación (lo redefine cada clase hija)."""

    def dibujar(self, pantalla, fuente, resaltada=False):
        """Dibuja el mueble, su ícono, su nombre y un borde blanco si está resaltada."""
        pygame.draw.rect(pantalla, C["barra"], self.rect, border_radius=12)
        pygame.draw.rect(pantalla, C["barra_tapa"], self.rect.inflate(-10, -34).move(0, -14), border_radius=8)
        self.dibujar_icono(pantalla)
        texto = fuente.render(self.nombre, True, C["texto_claro"])
        pantalla.blit(texto, texto.get_rect(center=(self.rect.centerx, self.rect.bottom - 11)))
        if resaltada:
            pygame.draw.rect(pantalla, C["resaltado"], self.rect.inflate(6, 6), 4, border_radius=14)

    def interactuar(self, jugador):
        """Acción al apretar E/Espacio. Devuelve (mensaje, sonido, dinero)."""
        return "", None, 0


class EstacionLeche(Estacion):
    """Heladera con leche: primer paso del café con leche."""

    def __init__(self):
        """Crea la estación de leche."""
        super().__init__("leche", "Leche")

    def dibujar_icono(self, pantalla):
        """Dibuja una cajita de leche."""
        x, y = self.rect.centerx, self.rect.centery - 18
        pygame.draw.rect(pantalla, C["leche"], (x - 11, y - 10, 22, 26), border_radius=3)
        pygame.draw.polygon(pantalla, C["azul"], [(x - 11, y - 10), (x + 11, y - 10), (x, y - 20)])
        pygame.draw.rect(pantalla, C["azul"], (x - 7, y + 1, 14, 8), border_radius=2)

    def interactuar(self, jugador):
        """Recoge leche en la taza si la taza está vacía."""
        if jugador.taza != TAZA_VACIA:
            return "Ya tenés una taza en preparación.", None, 0
        jugador.taza = TAZA_LECHE
        return "Recogiste leche. Ahora al vaporizador.", "miau", 0


class EstacionVapor(Estacion):
    """Vaporizador: calienta y espuma la leche."""

    def __init__(self):
        """Crea la estación vaporizadora."""
        super().__init__("vapor", "Vaporizador")

    def dibujar_icono(self, pantalla):
        """Dibuja una jarrita con vapor."""
        x, y = self.rect.centerx, self.rect.centery - 16
        pygame.draw.rect(pantalla, (200, 205, 212), (x - 10, y - 4, 20, 20), border_radius=4)
        for dx in (-6, 0, 6):
            pygame.draw.arc(pantalla, C["leche"], (x + dx - 4, y - 18, 8, 12), 0.5, 3.6, 2)

    def interactuar(self, jugador):
        """Calienta la leche si el jugador ya la recogió."""
        if jugador.taza == TAZA_LECHE:
            jugador.taza = TAZA_CALIENTE
            return "Leche espumosa. Ahora el espresso.", "vapor", 0
        if jugador.taza == TAZA_CALIENTE:
            return "La leche ya está caliente.", None, 0
        return "Primero buscá leche.", None, 0


class EstacionEspresso(Estacion):
    """Máquina de espresso: termina el café con leche y lo pone en la bandeja."""

    def __init__(self):
        """Crea la máquina espresso."""
        super().__init__("espresso", "Espresso")

    def dibujar_icono(self, pantalla):
        """Dibuja una máquina de café."""
        x, y = self.rect.centerx, self.rect.centery - 16
        pygame.draw.rect(pantalla, (120, 110, 120), (x - 16, y - 10, 32, 24), border_radius=5)
        pygame.draw.circle(pantalla, C["acento"], (x - 8, y - 3), 3)
        pygame.draw.circle(pantalla, C["dorado"], (x + 2, y - 3), 3)
        pygame.draw.rect(pantalla, C["leche"], (x - 6, y + 6, 12, 8))

    def interactuar(self, jugador):
        """Si la leche está caliente, prepara el café y lo agrega a la bandeja."""
        if jugador.taza != TAZA_CALIENTE:
            return "Necesitás leche vaporizada primero.", None, 0
        if not jugador.hay_espacio():
            return "La bandeja está llena, entregá algo primero.", None, 0
        jugador.taza = TAZA_VACIA
        jugador.agregar_item("cafe")
        return "¡Café con leche listo!", "vapor", 0


class ExhibidorMedialunas(Estacion):
    """Horno/exhibidor de medialunas calentitas."""

    def __init__(self):
        """Crea el exhibidor."""
        super().__init__("medialunas", "Medialunas")

    def dibujar_icono(self, pantalla):
        """Dibuja una bandejita con medialunas."""
        x, y = self.rect.centerx, self.rect.centery - 16
        pygame.draw.ellipse(pantalla, C["leche"], (x - 22, y - 4, 44, 18))
        dibujar_item(pantalla, "medialuna", (x - 8, y + 2), 0.8)
        dibujar_item(pantalla, "medialuna", (x + 9, y + 3), 0.8)

    def interactuar(self, jugador):
        """Agrega una medialuna a la bandeja si hay lugar."""
        if jugador.agregar_item("medialuna"):
            return "Medialuna calentita en la bandeja.", "miau", 0
        return "La bandeja está llena.", None, 0


class Mesa:
    """Mesa del salón: recibe un cliente, el pedido y deja el dinero hasta que se junta."""

    def __init__(self, centro):
        """Crea la mesa centrada en 'centro', sin cliente ni dinero."""
        self.rect = pygame.Rect(0, 0, TAM_MESA, TAM_MESA)
        self.rect.center = centro
        self.asiento = (centro[0] - DESPLAZAMIENTO_ASIENTO, centro[1])
        self.cliente = None
        self.dinero = 0

    def libre(self):
        """Devuelve True si no hay cliente sentado ni dinero sin juntar."""
        return self.cliente is None and self.dinero == 0

    def dibujar(self, pantalla, fuente, resaltada=False):
        """Dibuja la mesa con mantel y, si corresponde, el dinero que dejó el cliente."""
        pygame.draw.ellipse(pantalla, C["sombra"], self.rect.inflate(6, -14).move(0, 14))
        pygame.draw.ellipse(pantalla, C["mantel"], self.rect)
        pygame.draw.ellipse(pantalla, C["mesa"], self.rect.inflate(-20, -20))
        if self.dinero > 0:
            for i in range(2):
                billete = pygame.Rect(0, 0, 26, 14)
                billete.center = (self.rect.centerx - 6 + i * 8, self.rect.centery - i * 3)
                pygame.draw.rect(pantalla, C["billete"], billete, border_radius=3)
                pygame.draw.rect(pantalla, C["texto"], billete, 1, border_radius=3)
            pantalla.blit(fuente.render(f"${self.dinero}", True, C["texto"]),
                          (self.rect.centerx - 12, self.rect.centery + 6))
        if resaltada:
            pygame.draw.ellipse(pantalla, C["resaltado"], self.rect.inflate(6, 6), 4)

    def interactuar(self, jugador):
        """Junta el dinero si hay, o entrega los pedidos que el jugador lleve en la bandeja."""
        if self.dinero > 0:
            ganado = round(self.dinero * jugador.multiplicador_propina)
            self.dinero = 0
            return f"+${ganado}", "billete", ganado
        cliente = self.cliente
        if cliente is None:
            return "Mesa libre.", None, 0
        if cliente.estado != ESPERANDO:
            return "Todavía está mirando el menú.", None, 0
        entregados = 0
        for item in list(cliente.pedido):
            if item in jugador.bandeja:
                jugador.bandeja.remove(item)
                cliente.pedido.remove(item)
                entregados += 1
        if entregados == 0:
            return "No tenés lo que pidió.", None, 0
        if cliente.pedido:
            return "Falta algo del pedido.", "miau", 0
        self.dinero = cliente.total       # deja la plata en la mesa
        self.cliente = None
        cliente.atender()
        return "¡Pedido completo! Juntá el dinero.", "caja", 0


def crear_estaciones():
    """Devuelve la lista con las 4 estaciones de la barra."""
    return [EstacionLeche(), EstacionVapor(), EstacionEspresso(), ExhibidorMedialunas()]


def crear_mesas():
    """Devuelve la lista de mesas del salón según ajustes.CENTROS_MESAS."""
    return [Mesa(centro) for centro in CENTROS_MESAS]
