"""clientes.py - Los vecinos que llegan a la cafetería."""
import random
import pygame
from ajustes import (COLORES_PASTEL as C, COLORES_CLIENTES, PRECIOS, NIVELES, PUERTA, POS_COLA_X,
                     POS_COLA_Y, SEPARACION_COLA, VELOCIDAD_CLIENTE, TIEMPO_SENTADO,
                     LLEGANDO, SENTADO, ESPERANDO, ATENDIDO)
from dibujo import dibujar_gato, dibujar_item, dibujar_panel


class Cliente:
    """Un vecino con estado (Llegando, Sentado, Esperando, Atendido), pedido y dinero que deja."""

    def __init__(self, pedido, color):
        """Crea al cliente en la puerta con su pedido (lista de ítems) y color de pelaje."""
        self.pos = pygame.math.Vector2(PUERTA)
        self.objetivo = pygame.math.Vector2(PUERTA)
        self.color = color
        self.pedido = list(pedido)
        self.total = sum(PRECIOS[item] for item in pedido)   # lo que va a pagar
        self.estado = LLEGANDO
        self.mesa = None
        self.temporizador = 0.0
        self.se_fue = False                                    # True cuando salió por la puerta

    def esta_en_cola(self):
        """Devuelve True si está esperando que se libere una mesa."""
        return self.mesa is None and self.estado == LLEGANDO

    def atender(self):
        """Marca al cliente como atendido y lo manda hacia la puerta."""
        self.estado = ATENDIDO
        self.objetivo = pygame.math.Vector2(PUERTA)

    def actualizar(self, dt):
        """Hace caminar al cliente hacia su objetivo y avanza su estado."""
        if self.estado in (LLEGANDO, ATENDIDO):
            resto = self.objetivo - self.pos
            paso = VELOCIDAD_CLIENTE * dt
            if resto.length() <= paso:                 # llegó a destino
                self.pos = pygame.math.Vector2(self.objetivo)
                if self.estado == ATENDIDO:
                    self.se_fue = True
                elif self.mesa is not None:
                    self.estado = SENTADO
                    self.temporizador = TIEMPO_SENTADO
            else:
                self.pos += resto.normalize() * paso
        elif self.estado == SENTADO:
            self.temporizador -= dt
            if self.temporizador <= 0:
                self.estado = ESPERANDO

    def dibujar(self, pantalla):
        """Dibuja al gato cliente y, si espera, un globito con su pedido."""
        dibujar_gato(pantalla, (self.pos.x, self.pos.y), self.color, escala=0.9)
        if self.estado == ESPERANDO and self.pedido:
            ancho = 18 + 30 * len(self.pedido)
            globo = pygame.Rect(0, 0, ancho, 36)
            globo.midbottom = (self.pos.x, self.pos.y - 40)
            dibujar_panel(pantalla, globo, C["leche"], radio=12)
            for i, item in enumerate(self.pedido):
                dibujar_item(pantalla, item, (globo.left + 24 + i * 30, globo.centery), 0.8)


def crear_cliente(dia):
    """Crea un cliente nuevo con un pedido al azar según el día (más ítems en días avanzados)."""
    cantidad = random.randint(1, NIVELES[dia]["max_items"])
    pedido = [random.choice(list(PRECIOS)) for _ in range(cantidad)]
    return Cliente(pedido, random.choice(COLORES_CLIENTES))


def asignar_mesas(clientes, mesas):
    """Sienta a los clientes que esperan en las mesas libres (por orden de llegada).

    Los que no consiguen mesa se acomodan en la cola junto a la pared.
    Devuelve cuántos clientes quedaron sin mesa.
    """
    en_cola = [c for c in clientes if c.esta_en_cola()]
    libres = [m for m in mesas if m.libre()]
    for cliente, mesa in zip(en_cola, libres):
        mesa.cliente = cliente
        cliente.mesa = mesa
        cliente.objetivo = pygame.math.Vector2(mesa.asiento)
    pendientes = en_cola[len(libres):]
    for i, cliente in enumerate(pendientes):
        cliente.objetivo = pygame.math.Vector2(POS_COLA_X, POS_COLA_Y + i * SEPARACION_COLA)
    return len(pendientes)
