"""main.py - Michi Café 2D: bucle principal y máquina de estados.

Estados: HISTORIA_INTRO -> SELECCION_GATO -> JUGANDO -> DIA_COMPLETADO
         -> TIENDA_MEJORAS -> JUGANDO (día siguiente) ... -> VICTORIA_FINAL
         (y DERROTA si el local se desborda; con R se vuelve a jugar sin cerrar).
"""
import os
import random
import sys
import pygame
from ajustes import *
from ajustes import COLORES_PASTEL as C
from jugador import Jugador
from estaciones import crear_estaciones, crear_mesas
from clientes import crear_cliente, asignar_mesas
from dibujo import (dibujar_gato, dibujar_item, dibujar_panel, texto_envuelto,
                    texto_centrado)


def cargar_sonidos():
    """Carga los efectos y la música UNA sola vez. Devuelve un diccionario {clave: Sound}.

    Si no hay placa de sonido o faltan los archivos, el juego sigue sin sonido.
    """
    sonidos = {}
    try:
        for clave, archivo in ARCHIVOS_SONIDO.items():
            sonido = pygame.mixer.Sound(os.path.join(RUTA_SONIDOS, archivo))
            sonido.set_volume(VOLUMEN_EFECTOS)
            sonidos[clave] = sonido
        pygame.mixer.music.load(os.path.join(RUTA_SONIDOS, ARCHIVO_MUSICA))
        pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError) as error:
        print("Aviso: sin sonido (", error, "). Ejecutá generar_sonidos.py")
    return sonidos


def crear_fondo():
    """Dibuja el salón (piso a cuadros, pared, zócalo, puerta) en una Surface. La devuelve."""
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill(C["piso_a"])
    for fila in range(0, ALTO, 40):
        for col in range(0, ANCHO, 40):
            if (fila // 40 + col // 40) % 2:
                pygame.draw.rect(fondo, C["piso_b"], (col, fila, 40, 40))
    pygame.draw.rect(fondo, C["pared"], (0, 0, ANCHO, 165))
    pygame.draw.rect(fondo, C["zocalo"], (0, 160, ANCHO, 8))
    pygame.draw.rect(fondo, C["azul"], (740, 85, 150, 60), border_radius=8)      # ventana
    pygame.draw.line(fondo, C["leche"], (815, 85), (815, 145), 4)
    pygame.draw.rect(fondo, C["acento"], (0, 540, 12, 80))                        # puerta
    return fondo


def objeto_cercano(jugador, objetos):
    """Devuelve el objeto interactuable más cercano al jugador, o None si no hay ninguno."""
    zona = jugador.rect.inflate(2 * ALCANCE_INTERACCION, 2 * ALCANCE_INTERACCION)
    mejor, mejor_dist = None, None
    for objeto in objetos:
        if zona.colliderect(objeto.rect):
            distancia = pygame.math.Vector2(objeto.rect.center).distance_to(jugador.rect.center)
            if mejor is None or distancia < mejor_dist:
                mejor, mejor_dist = objeto, distancia
    return mejor


class Juego:
    """Contiene todo el estado de la partida y las tres fases del bucle: eventos, actualizar, dibujar."""

    def __init__(self):
        """Inicia pygame, ventana, fuentes, sonidos (una vez) y el estado inicial."""
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            print("Aviso: no se pudo iniciar el audio")
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente_xl = pygame.font.Font(None, 64)
        self.fuente_l = pygame.font.Font(None, 40)
        self.fuente_m = pygame.font.Font(None, 28)
        self.fuente_s = pygame.font.Font(None, 22)
        self.sonidos = cargar_sonidos()
        self.fondo = crear_fondo()
        self.estado = HISTORIA_INTRO
        self.vineta = 0
        self.indice_gato = 0
        self.aviso_texto = ""
        self.aviso_t = 0.0
        self.nueva_partida()

    # ------------------------------------------------------------ utilidades
    def reproducir(self, clave):
        """Reproduce un efecto de sonido si existe."""
        if clave in self.sonidos:
            self.sonidos[clave].play()

    def avisar(self, texto):
        """Muestra un mensaje breve arriba de la pantalla."""
        self.aviso_texto = texto
        self.aviso_t = DURACION_AVISO

    def nueva_partida(self):
        """Reinicia dinero, día y jugador (se usa al empezar y al volver a jugar)."""
        self.dia = 1
        self.monedero = 0
        self.dinero_dia = 0
        self.jugador = None
        self.clientes = []
        self.estaciones = crear_estaciones()
        self.mesas = crear_mesas()
        self.t_llegada = 0.0

    def iniciar_dia(self):
        """Prepara un día de trabajo: salón vacío, meta del día y primer cliente en 2 segundos."""
        self.dinero_dia = 0
        self.clientes = []
        self.estaciones = crear_estaciones()
        self.mesas = crear_mesas()
        self.jugador.reiniciar_posicion()
        self.t_llegada = 2.0
        self.estado = JUGANDO
        self.avisar(f"Día {self.dia}: juntá ${NIVELES[self.dia]['meta']}")

    def comprar(self, clave):
        """Intenta comprar una prenda. Descuenta del monedero y se la pone al gato."""
        prenda = TIENDA[clave]
        if clave in self.jugador.compras:
            self.avisar("Ya tenés esa prenda.")
        elif prenda["requiere"] and prenda["requiere"] not in self.jugador.compras:
            self.avisar("Primero comprá la prenda anterior.")
        elif self.monedero < prenda["precio"]:
            self.avisar("No te alcanza la plata.")
        else:
            self.monedero -= prenda["precio"]
            self.jugador.equipar(clave)
            self.reproducir("caja")
            self.avisar(f"¡Compraste: {prenda['nombre']}!")

    def interactuar(self):
        """Acción de E/Espacio: usa la estación o mesa más cercana."""
        objeto = objeto_cercano(self.jugador, self.estaciones + self.mesas)
        if objeto is None:
            return
        mensaje, sonido, dinero = objeto.interactuar(self.jugador)
        self.avisar(mensaje)
        self.reproducir(sonido)
        self.dinero_dia += dinero
        self.monedero += dinero

    # ------------------------------------------------------------ eventos
    def manejar_evento(self, evento):
        """Procesa un evento de pygame. Devuelve False si hay que cerrar el juego."""
        if evento.type == pygame.QUIT:
            return False
        if evento.type != pygame.KEYDOWN:
            return True
        tecla = evento.key
        confirmar = tecla in (pygame.K_SPACE, pygame.K_RETURN)
        if self.estado == HISTORIA_INTRO and confirmar:
            self.vineta += 1
            if self.vineta >= len(VINETAS):
                self.estado = SELECCION_GATO
        elif self.estado == SELECCION_GATO:
            if tecla in (pygame.K_a, pygame.K_LEFT):
                self.indice_gato = (self.indice_gato - 1) % len(PELAJES)
            elif tecla in (pygame.K_d, pygame.K_RIGHT):
                self.indice_gato = (self.indice_gato + 1) % len(PELAJES)
            elif confirmar:
                self.jugador = Jugador(PELAJES[self.indice_gato][1])
                self.reproducir("miau")
                self.iniciar_dia()
        elif self.estado == JUGANDO and tecla in (pygame.K_e, pygame.K_SPACE):
            self.interactuar()
        elif self.estado == DIA_COMPLETADO and confirmar:
            if self.dia >= DIAS_TOTALES:
                self.estado = VICTORIA_FINAL
            else:
                self.estado = TIENDA_MEJORAS
        elif self.estado == TIENDA_MEJORAS:
            claves = list(TIENDA)
            if pygame.K_1 <= tecla < pygame.K_1 + len(claves):
                self.comprar(claves[tecla - pygame.K_1])
            elif confirmar:
                self.dia += 1
                self.iniciar_dia()
        elif self.estado in (DERROTA, VICTORIA_FINAL) and tecla == pygame.K_r:
            self.nueva_partida()
            self.estado = SELECCION_GATO            # volver a jugar sin cerrar la ventana
        return True

    # ------------------------------------------------------------ lógica
    def actualizar(self, dt):
        """Avanza la lógica del juego un cuadro (solo en el estado JUGANDO)."""
        self.aviso_t = max(0.0, self.aviso_t - dt)
        if self.estado != JUGANDO:
            return
        self.jugador.mover(dt, pygame.key.get_pressed(), [m.rect for m in self.mesas])
        self.t_llegada -= dt
        if self.t_llegada <= 0:                       # llega un vecino nuevo
            self.clientes.append(crear_cliente(self.dia))
            self.t_llegada = NIVELES[self.dia]["intervalo"]
        sin_mesa = asignar_mesas(self.clientes, self.mesas)
        for cliente in self.clientes:
            cliente.actualizar(dt)
        self.clientes = [c for c in self.clientes if not c.se_fue]   # la lista cambia durante la partida
        if sin_mesa >= MAX_COLA:
            self.estado = DERROTA
        elif self.dinero_dia >= NIVELES[self.dia]["meta"]:
            self.reproducir("caja")
            self.estado = DIA_COMPLETADO

    # ------------------------------------------------------------ dibujo
    def dibujar_hud(self):
        """Dibuja día, meta, monedero, bandeja y estado de la taza arriba de la pantalla."""
        meta = NIVELES[self.dia]["meta"]
        dibujar_panel(self.pantalla, (10, 8, 940, 56), C["panel"], radio=14)
        self.pantalla.blit(self.fuente_l.render(f"Día {self.dia}/{DIAS_TOTALES}", True, C["texto"]), (24, 24))
        barra = pygame.Rect(170, 22, 260, 22)
        pygame.draw.rect(self.pantalla, C["sombra"], barra, border_radius=11)
        relleno = barra.copy()
        relleno.width = int(barra.width * min(1, self.dinero_dia / meta))
        pygame.draw.rect(self.pantalla, C["verde"], relleno, border_radius=11)
        texto_centrado(self.pantalla, f"${self.dinero_dia} / ${meta}", self.fuente_m, C["texto"], barra.center)
        self.pantalla.blit(self.fuente_m.render(f"Monedero: ${self.monedero}", True, C["texto"]), (450, 28))
        nombres_taza = {TAZA_VACIA: "vacía", TAZA_LECHE: "con leche", TAZA_CALIENTE: "leche caliente"}
        self.pantalla.blit(self.fuente_m.render(f"Taza: {nombres_taza[self.jugador.taza]}", True, C["texto"]), (620, 28))
        for i in range(self.jugador.capacidad_bandeja):    # ranuras de la bandeja
            casilla = pygame.Rect(810 + i * 42, 16, 38, 38)
            pygame.draw.rect(self.pantalla, C["sombra"], casilla, border_radius=8)
            if i < len(self.jugador.bandeja):
                dibujar_item(self.pantalla, self.jugador.bandeja[i], casilla.center, 0.9)
        if self.aviso_t > 0:
            texto = self.fuente_m.render(self.aviso_texto, True, C["texto_claro"])
            caja = texto.get_rect(center=(ANCHO // 2, 190)).inflate(30, 14)
            pygame.draw.rect(self.pantalla, C["texto"], caja, border_radius=12)
            self.pantalla.blit(texto, texto.get_rect(center=caja.center))

    def dibujar_juego(self):
        """Dibuja el salón: fondo, estaciones, mesas, clientes, jugador y HUD."""
        self.pantalla.blit(self.fondo, (0, 0))
        cercano = objeto_cercano(self.jugador, self.estaciones + self.mesas)
        for estacion in self.estaciones:
            estacion.dibujar(self.pantalla, self.fuente_s, estacion is cercano)
        for mesa in self.mesas:
            mesa.dibujar(self.pantalla, self.fuente_s, mesa is cercano)
        # se dibuja de arriba hacia abajo para que los de adelante tapen a los de atrás
        for cliente in sorted(self.clientes, key=lambda c: c.pos.y):
            cliente.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)
        self.dibujar_hud()
        if cercano is not None:
            texto_centrado(self.pantalla, "E / Espacio: interactuar", self.fuente_s, C["texto"],
                           (ANCHO // 2, ALTO - 14))

    def dibujar_intro(self):
        """Dibuja la historia de introducción, una viñeta por pantalla."""
        self.pantalla.fill(C["pared"])
        titulo, texto = VINETAS[self.vineta]
        escena = dibujar_panel(self.pantalla, (80, 40, 800, 280), C["azul"])
        if self.vineta == 0:                                   # el cartel en la ventana
            pygame.draw.rect(self.pantalla, C["piso_a"], (330, 80, 300, 200), border_radius=10)
            pygame.draw.rect(self.pantalla, C["leche"], (390, 110, 180, 100), border_radius=6)
            texto_centrado(self.pantalla, "SE BUSCA", self.fuente_l, C["acento"], (480, 140))
            texto_centrado(self.pantalla, "BARISTA", self.fuente_l, C["acento"], (480, 180))
        elif self.vineta == 1:                                 # Don Salmón con su platito
            pygame.draw.ellipse(self.pantalla, C["leche"], (500, 250, 90, 28))
            dibujar_gato(self.pantalla, (420, 190), COLOR_DON_SALMON, escala=3.6, lentes=True)
        else:                                                  # el delantal básico
            dibujar_gato(self.pantalla, (480, 190), PELAJES[0][1], {"delantal": True}, escala=3.6)
        dibujar_panel(self.pantalla, (80, 340, 800, 250))
        self.pantalla.blit(self.fuente_l.render(titulo, True, C["acento"]), (105, 355))
        texto_envuelto(self.pantalla, texto, self.fuente_m, C["texto"], pygame.Rect(105, 395, 750, 180))
        texto_centrado(self.pantalla, f"Espacio para seguir  ({self.vineta + 1}/{len(VINETAS)})",
                       self.fuente_s, C["texto"], (ANCHO // 2, 615))

    def dibujar_seleccion(self):
        """Dibuja la pantalla para elegir el color de pelaje del gato."""
        self.pantalla.fill(C["pared"])
        texto_centrado(self.pantalla, "Elegí tu michi", self.fuente_xl, C["texto"], (ANCHO // 2, 90))
        for i, (nombre, color) in enumerate(PELAJES):
            centro = (150 + i * 220, 330)
            if i == self.indice_gato:
                pygame.draw.circle(self.pantalla, C["dorado"], (centro[0], centro[1] - 10), 95)
            dibujar_gato(self.pantalla, centro, color, escala=3.0)
            texto_centrado(self.pantalla, nombre, self.fuente_m, C["texto"], (centro[0], 450))
        texto_centrado(self.pantalla, "A / D o flechas para elegir  -  Espacio para confirmar",
                       self.fuente_m, C["texto"], (ANCHO // 2, 560))

    def dibujar_mensaje(self, titulo, lineas, pie):
        """Dibuja una pantalla de mensaje (día completado, derrota, victoria) sobre el salón."""
        self.pantalla.blit(self.fondo, (0, 0))
        dibujar_panel(self.pantalla, (160, 130, 640, 380))
        texto_centrado(self.pantalla, titulo, self.fuente_xl, C["acento"], (ANCHO // 2, 190))
        for i, linea in enumerate(lineas):
            texto_centrado(self.pantalla, linea, self.fuente_m, C["texto"], (ANCHO // 2, 260 + i * 36))
        texto_centrado(self.pantalla, pie, self.fuente_m, C["texto"], (ANCHO // 2, 470))

    def dibujar_tienda(self):
        """Dibuja la tienda de ropa con precios, bonus y el monedero."""
        self.pantalla.fill(C["pared"])
        texto_centrado(self.pantalla, "Ropero de Don Salmón", self.fuente_xl, C["texto"], (ANCHO // 2, 50))
        texto_centrado(self.pantalla, f"Monedero: ${self.monedero}", self.fuente_l, C["acento"], (ANCHO // 2, 100))
        for i, (clave, prenda) in enumerate(TIENDA.items()):
            fila = pygame.Rect(120, 140 + i * 66, 720, 58)
            dibujar_panel(self.pantalla, fila, C["panel"], radio=12)
            if clave in self.jugador.compras:
                estado = "COMPRADO"
            elif prenda["requiere"] and prenda["requiere"] not in self.jugador.compras:
                estado = "BLOQUEADO"
            else:
                estado = f"${prenda['precio']}"
            self.pantalla.blit(self.fuente_m.render(f"[{i + 1}] {prenda['nombre']}", True, C["texto"]), (140, fila.top + 8))
            self.pantalla.blit(self.fuente_s.render(prenda["detalle"], True, C["texto"]), (140, fila.top + 34))
            texto_centrado(self.pantalla, estado, self.fuente_m, C["acento"], (fila.right - 80, fila.centery))
        dibujar_gato(self.pantalla, (900, 300), self.jugador.color, self.jugador.ropa, escala=1.6)
        texto_centrado(self.pantalla, "Tocá 1-5 para comprar  -  Espacio para empezar el día " + str(self.dia + 1),
                       self.fuente_m, C["texto"], (ANCHO // 2, 560))
        if self.aviso_t > 0:
            texto_centrado(self.pantalla, self.aviso_texto, self.fuente_m, C["acento"], (ANCHO // 2, 600))

    def dibujar(self):
        """Dibuja la pantalla que corresponde al estado actual y la muestra."""
        if self.estado == HISTORIA_INTRO:
            self.dibujar_intro()
        elif self.estado == SELECCION_GATO:
            self.dibujar_seleccion()
        elif self.estado == JUGANDO:
            self.dibujar_juego()
        elif self.estado == TIENDA_MEJORAS:
            self.dibujar_tienda()
        elif self.estado == DIA_COMPLETADO:
            self.dibujar_mensaje(f"¡Día {self.dia} completado!",
                                 [f"Juntaste ${self.dinero_dia} (meta: ${NIVELES[self.dia]['meta']})",
                                  "Los vecinos se fueron felices."],
                                 "Espacio para continuar")
        elif self.estado == DERROTA:
            self.dibujar_mensaje("¡El local se desbordó!",
                                 ["Se juntaron demasiados vecinos sin mesa.",
                                  "Don Salmón vuelve del campo y te ayuda a ordenar."],
                                 "R para volver a jugar")
        elif self.estado == VICTORIA_FINAL:
            self.dibujar_mensaje("¡Sos el barista del barrio!",
                                 ["Completaste los 5 días de trabajo.",
                                  f"Te quedan ${self.monedero} para tu próximo outfit."],
                                 "R para volver a jugar")
        pygame.display.flip()

    # ------------------------------------------------------------ bucle principal
    def ejecutar(self):
        """Bucle principal: eventos -> actualizar -> dibujar -> reloj.tick."""
        corriendo = True
        while corriendo:
            dt = min(self.reloj.tick(FPS) / 1000, 0.05)
            for evento in pygame.event.get():
                if not self.manejar_evento(evento):
                    corriendo = False
            self.actualizar(dt)
            self.dibujar()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Juego().ejecutar()
