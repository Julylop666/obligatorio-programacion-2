"""main.py - Michi Café 2D: bucle principal y máquina de estados.

Estados: HISTORIA_INTRO -> SELECCION_GATO -> JUGANDO -> DIA_COMPLETADO
         -> TIENDA_MEJORAS -> JUGANDO (día siguiente) ... -> VICTORIA_FINAL
         (y DERROTA si el local se desborda; con R se vuelve a jugar sin cerrar).
Durante JUGANDO se puede pausar con P, Esc o el botón || del HUD.
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
                    texto_centrado, frame_caminata)
from escenas import crear_escenas
from ventana import VentanaDia


def cargar_sonidos():
    """Carga los efectos UNA sola vez. Devuelve un diccionario {clave: Sound}.

    Si no hay placa de sonido o falta algún archivo, avisa por consola y el juego sigue.
    """
    sonidos = {}
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(44100, -16, 2, 512)
        except pygame.error as error:
            print("Aviso: no se pudo iniciar el audio:", error)
            return sonidos
    print("Audio iniciado:", pygame.mixer.get_init())
    for clave, archivo in ARCHIVOS_SONIDO.items():
        ruta = os.path.join(RUTA_SONIDOS, archivo)
        try:
            sonido = pygame.mixer.Sound(ruta)
            sonido.set_volume(VOLUMEN_EFECTOS * VOLUMEN_RELATIVO.get(clave, 1.0))
            sonidos[clave] = sonido
        except (pygame.error, FileNotFoundError) as error:
            print(f"Aviso: no se pudo cargar {ruta}: {error}")
    return sonidos


def iniciar_musica():
    """Carga y reproduce en loop la música de fondo. Devuelve True si pudo, False si no."""
    ruta = os.path.join(RUTA_SONIDOS, ARCHIVO_MUSICA)
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(VOLUMEN_MUSICA)
        pygame.mixer.music.play(-1)
        return True
    except (pygame.error, FileNotFoundError) as error:
        print(f"Aviso: no se pudo cargar la música {ruta}: {error}")
        return False


def cargar_fuente(tamano):
    """Devuelve la fuente pixel art del juego en ese tamaño (o la de pygame si falta el archivo)."""
    try:
        return pygame.font.Font(RUTA_FUENTE, tamano)
    except (pygame.error, FileNotFoundError):
        return pygame.font.Font(None, int(tamano * 1.2))


def crear_fondo():
    """Dibuja el salón en pixel art (piso a cuadros, pared, zócalo, puerta). Devuelve una Surface.

    La ventana NO se dibuja acá: cambia con el paso del tiempo y la dibuja ventana.py en cada cuadro.
    """
    px = PX_MUNDO
    azar = random.Random(7)                       # semilla fija: el piso siempre queda igual
    chica = pygame.Surface((ANCHO // px, ALTO // px))
    chica.fill(C["piso_a"])
    for fila in range(0, ALTO // px, 10):
        for col in range(0, ANCHO // px, 10):
            if (fila // 10 + col // 10) % 2:
                pygame.draw.rect(chica, C["piso_b"], (col, fila, 10, 10))
    for _ in range(320):                          # puntitos de textura en el piso
        chica.set_at((azar.randrange(0, ANCHO // px), azar.randrange(FILAS_PARED + 3, ALTO // px)), C["piso_punto"])
    pygame.draw.rect(chica, C["pared"], (0, 0, ANCHO // px, FILAS_PARED))
    for x in range(0, ANCHO // px, 8):            # papel tapiz a rayas
        pygame.draw.rect(chica, C["papel_rayas"], (x, 0, 2, FILAS_PARED - 3))
    pygame.draw.rect(chica, C["zocalo"], (0, FILAS_PARED - 3, ANCHO // px, 3))
    pygame.draw.rect(chica, C["contorno"], (0, FILAS_PARED, ANCHO // px, 1))
    pygame.draw.rect(chica, C["contorno"], (0, 129, 6, 27))                  # puerta
    pygame.draw.rect(chica, C["barra"], (0, 130, 5, 25))
    pygame.draw.rect(chica, C["dorado"], (3, 142, 1, 2))
    return pygame.transform.scale(chica, (ANCHO, ALTO))


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
        """Inicia pygame, ventana, fuentes, sonidos e ilustraciones (una vez) y el estado inicial."""
        pygame.mixer.pre_init(44100, -16, 2, 512)      # configuración de audio antes de pygame.init
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption(TITULO)
        self.reloj = pygame.time.Clock()
        self.fuente_titulo = cargar_fuente(120)
        self.fuente_xl = cargar_fuente(60)
        self.fuente_l = cargar_fuente(40)
        self.fuente_m = cargar_fuente(30)
        self.fuente_s = cargar_fuente(22)
        self.fuente_xs = cargar_fuente(18)      # etiquetas de las estaciones
        self.sonidos = cargar_sonidos()
        self.musica_ok = iniciar_musica() if self.sonidos else False
        self.fondo = crear_fondo()
        self.ventana = VentanaDia()
        self.escenas = crear_escenas(self.fuente_titulo, self.fuente_l)
        self.velo_pausa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        self.velo_pausa.fill(COLOR_VELO_PAUSA)
        self.estado = HISTORIA_INTRO
        self.vineta = -1                       # -1 es la portada; después van las viñetas
        self.indice_gato = 0
        self.aviso_texto = ""
        self.aviso_t = 0.0
        self.nueva_partida()

    # ------------------------------------------------------------ utilidades
    def reproducir(self, clave):
        """Reproduce un efecto de sonido si existe."""
        if clave in self.sonidos:
            self.sonidos[clave].play()

    def avisar(self, texto, duracion=DURACION_AVISO):
        """Muestra un mensaje breve arriba de la pantalla (\\n separa líneas)."""
        self.aviso_texto = texto
        self.aviso_t = duracion

    def objetos_activos(self):
        """Devuelve las estaciones ya desbloqueadas y las mesas (lo que se puede usar)."""
        return [e for e in self.estaciones if e.activa] + self.mesas

    def nueva_partida(self):
        """Reinicia dinero, día y jugador (se usa al empezar y al volver a jugar)."""
        self.dia = 1
        self.monedero = 0
        self.dinero_dia = 0
        self.jugador = None
        self.pausado = False
        self.clientes = []
        self.estaciones = crear_estaciones(1)
        self.mesas = crear_mesas()
        self.t_llegada = 0.0
        self.ventana.reiniciar()

    def iniciar_dia(self):
        """Prepara un día de trabajo: salón vacío, meta del día y primer cliente en 2 segundos."""
        self.dinero_dia = 0
        self.clientes = []
        self.estaciones = crear_estaciones(self.dia)
        self.mesas = crear_mesas()
        self.jugador.reiniciar_posicion()
        self.t_llegada = 2.0
        self.ventana.reiniciar()                      # cada día arranca de mañana
        self.pausado = False
        self.estado = JUGANDO
        texto = f"Día {self.dia}: juntá ${NIVELES[self.dia]['meta']}"
        if self.dia in AVISOS_DESBLOQUEO:
            self.avisar(texto + "\n" + AVISOS_DESBLOQUEO[self.dia], DURACION_AVISO_DIA)
        else:
            self.avisar(texto)

    def cambiar_pausa(self):
        """Pausa o reanuda el juego (también pausa la música)."""
        self.pausado = not self.pausado
        if self.musica_ok:
            if self.pausado:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

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
        objeto = objeto_cercano(self.jugador, self.objetos_activos())
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
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.estado == JUGANDO:
            if self.pausado or pygame.Rect(BOTON_PAUSA).collidepoint(evento.pos):
                self.cambiar_pausa()
            return True
        if evento.type != pygame.KEYDOWN:
            return True
        tecla = evento.key
        confirmar = tecla in (pygame.K_SPACE, pygame.K_RETURN)
        if self.estado == JUGANDO and tecla in (pygame.K_p, pygame.K_ESCAPE):
            self.cambiar_pausa()
        elif self.estado == JUGANDO and self.pausado:
            if tecla == pygame.K_r:
                self.nueva_partida()
                self.vineta = -1
                self.estado = HISTORIA_INTRO
        elif self.estado == HISTORIA_INTRO and confirmar:
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
            self.vineta = -1
            self.estado = HISTORIA_INTRO            # vuelve a mostrar la presentación antes de jugar
        return True

    # ------------------------------------------------------------ lógica
    def actualizar(self, dt):
        """Avanza la lógica del juego un cuadro (solo en el estado JUGANDO y sin pausa)."""
        if self.pausado:
            return
        self.aviso_t = max(0.0, self.aviso_t - dt)
        self.ventana.actualizar(dt, self.dinero_dia / NIVELES[self.dia]["meta"])
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
            self.reproducir("dia_completo")
            self.estado = DIA_COMPLETADO

    # ------------------------------------------------------------ dibujo
    def dibujar_aviso(self):
        """Dibuja el mensaje breve (de una o varias líneas) en un cartelito arriba del salón."""
        lineas = self.aviso_texto.split("\n")
        textos = [self.fuente_m.render(linea, False, C["texto_claro"]) for linea in lineas]
        ancho = max(t.get_width() for t in textos) + 36
        alto = sum(t.get_height() for t in textos) + 18
        caja = pygame.Rect(0, 0, ancho, alto)
        caja.midbottom = (ANCHO // 2, ALTO - 28)          # abajo, para no tapar los pedidos
        dibujar_panel(self.pantalla, caja, C["texto"])
        y = caja.top + 9
        for texto in textos:
            self.pantalla.blit(texto, texto.get_rect(midtop=(caja.centerx, y)))
            y += texto.get_height()

    def dibujar_hud(self):
        """Dibuja día, pausa, meta, monedero, lo que se está preparando y la bandeja."""
        meta = NIVELES[self.dia]["meta"]
        dibujar_panel(self.pantalla, RECT_HUD, C["panel"])
        self.pantalla.blit(self.fuente_l.render(f"Día {self.dia}/{DIAS_TOTALES}", False, C["texto"]), (26, 17))
        boton = pygame.Rect(BOTON_PAUSA)                                # botón de pausa
        dibujar_panel(self.pantalla, boton, C["azul"] if self.pausado else C["leche"])
        for dx in (11, 21):
            pygame.draw.rect(self.pantalla, C["texto"], (boton.x + dx, boton.y + 9, 5, 18))
        barra = pygame.Rect(RECT_BARRA_META)
        pygame.draw.rect(self.pantalla, C["sombra"], barra)
        relleno = barra.copy()
        relleno.width = int(barra.width * min(1, self.dinero_dia / meta))
        pygame.draw.rect(self.pantalla, C["verde"], relleno)
        pygame.draw.rect(self.pantalla, C["zocalo"], barra, 3)
        texto_centrado(self.pantalla, f"${self.dinero_dia} / ${meta}", self.fuente_s, C["texto"], barra.center)
        self.pantalla.blit(self.fuente_m.render(f"Monedero: ${self.monedero}", False, C["texto"]), POS_MONEDERO)
        # solo se muestra la taza cuando hay un café con leche en preparación
        nombres_taza = {TAZA_LECHE: "leche", TAZA_CALIENTE: "leche espumosa"}
        if self.jugador.taza in nombres_taza:
            x_taza, y_taza = POS_PREPARANDO
            self.pantalla.blit(self.fuente_s.render("Preparando", False, C["acento"]), (x_taza, y_taza))
            self.pantalla.blit(self.fuente_s.render(nombres_taza[self.jugador.taza], False, C["texto"]),
                               (x_taza, y_taza + 20))
        for i in range(self.jugador.capacidad_bandeja):    # ranuras de la bandeja
            casilla = pygame.Rect(POS_BANDEJA_HUD[0] + i * SEPARACION_CASILLA_BANDEJA, POS_BANDEJA_HUD[1],
                                  TAM_CASILLA_BANDEJA, TAM_CASILLA_BANDEJA)
            pygame.draw.rect(self.pantalla, C["sombra"], casilla)
            pygame.draw.rect(self.pantalla, C["zocalo"], casilla, 3)
            if i < len(self.jugador.bandeja):
                dibujar_item(self.pantalla, self.jugador.bandeja[i], casilla.center, px=2)
        if self.aviso_t > 0:
            self.dibujar_aviso()

    def dibujar_pausa(self):
        """Dibuja el menú de pausa sobre el salón."""
        self.pantalla.blit(self.velo_pausa, (0, 0))
        dibujar_panel(self.pantalla, (200, 170, 560, 320))
        texto_centrado(self.pantalla, "PAUSA", self.fuente_xl, C["acento"], (ANCHO // 2, 225))
        texto_centrado(self.pantalla, "P, Esc o clic para continuar", self.fuente_m, C["texto"], (ANCHO // 2, 305))
        texto_centrado(self.pantalla, "R - Reiniciar partida", self.fuente_m, C["acento"], (ANCHO // 2, 345))
        texto_centrado(self.pantalla, "Los vecinos esperan con paciencia.", self.fuente_s, C["texto"], (ANCHO // 2, 385))
        texto_centrado(self.pantalla, "WASD / flechas: moverte  -  E / Espacio: interactuar",
                       self.fuente_s, C["texto"], (ANCHO // 2, 420))
        estado_audio = "Sonido: activado" if self.sonidos else "Sonido: no disponible (mirá la consola)"
        texto_centrado(self.pantalla, estado_audio, self.fuente_s, C["acento"], (ANCHO // 2, 455))

    def dibujar_salon(self):
        """Dibuja el fondo del salón y la ventana con el cielo del momento del día."""
        self.pantalla.blit(self.fondo, (0, 0))
        self.ventana.dibujar(self.pantalla)

    def dibujar_juego(self):
        """Dibuja el salón: fondo, ventana, estaciones, mesas, clientes, jugador y HUD."""
        self.dibujar_salon()
        cercano = objeto_cercano(self.jugador, self.objetos_activos())
        for estacion in self.estaciones:
            estacion.dibujar(self.pantalla, self.fuente_xs, estacion is cercano)
        for mesa in self.mesas:
            mesa.dibujar(self.pantalla, self.fuente_s, mesa is cercano)
        # se dibuja de arriba hacia abajo para que los de adelante tapen a los de atrás
        for cliente in sorted(self.clientes, key=lambda c: c.pos.y):
            cliente.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)
        self.dibujar_hud()
        if cercano is not None and not self.pausado:
            texto_centrado(self.pantalla, "E / Espacio: interactuar  -  P: pausa", self.fuente_s, C["texto"],
                           (ANCHO // 2, ALTO - 14))
        if self.pausado:
            self.dibujar_pausa()

    def dibujar_intro(self):
        """Dibuja la portada y después la historia de introducción, una viñeta por pantalla."""
        if self.vineta < 0:
            self.pantalla.blit(self.escenas["portada"], (0, 0))
            if (pygame.time.get_ticks() // 600) % 2 == 0:             # texto que parpadea
                texto_centrado(self.pantalla, "Presioná ESPACIO para empezar", self.fuente_m, C["texto"],
                               (ANCHO // 2, 600))
            return
        titulo, texto = VINETAS[self.vineta]
        self.pantalla.fill(C["pared"])
        dibujar_panel(self.pantalla, (32, 20, 896, 336), C["panel"])
        self.pantalla.blit(self.escenas[ESCENAS_VINETAS[self.vineta]], (40, 28))
        dibujar_panel(self.pantalla, (32, 368, 896, 236))
        self.pantalla.blit(self.fuente_l.render(titulo, False, C["acento"]), (60, 382))
        texto_envuelto(self.pantalla, texto, self.fuente_m, C["texto"], pygame.Rect(60, 428, 840, 165))
        texto_centrado(self.pantalla, f"Espacio para seguir  ({self.vineta + 1}/{len(VINETAS)})",
                       self.fuente_s, C["texto"], (ANCHO // 2, 624))

    def dibujar_seleccion(self):
        """Dibuja la pantalla para elegir el color de pelaje del gato."""
        self.pantalla.fill(C["pared"])
        texto_centrado(self.pantalla, "Elegí tu michi", self.fuente_xl, C["texto"], (ANCHO // 2, 80))
        for i, (nombre, color) in enumerate(PELAJES):
            centro = (150 + i * 220, 330)
            elegido = i == self.indice_gato
            if elegido:
                dibujar_panel(self.pantalla, (centro[0] - 100, 160, 200, 300), C["dorado"])
            salta = elegido and (pygame.time.get_ticks() // 350) % 2 == 0   # el elegido camina en el lugar
            dibujar_gato(self.pantalla, centro, color, escala=3.0, ojos=COLOR_OJOS_JUGADOR,
                         frame=1 if salta else 0)
            texto_centrado(self.pantalla, nombre, self.fuente_m, C["texto"], (centro[0], 435))
        texto_centrado(self.pantalla, "A / D o flechas para elegir  -  Espacio para confirmar",
                       self.fuente_m, C["texto"], (ANCHO // 2, 560))

    def dibujar_mensaje(self, titulo, lineas, pie):
        """Dibuja una pantalla de mensaje (día completado, derrota, victoria) sobre el salón."""
        self.dibujar_salon()
        dibujar_panel(self.pantalla, (160, 130, 640, 380))
        texto_centrado(self.pantalla, titulo, self.fuente_xl, C["acento"], (ANCHO // 2, 190))
        for i, linea in enumerate(lineas):
            texto_centrado(self.pantalla, linea, self.fuente_m, C["texto"], (ANCHO // 2, 270 + i * 40))
        texto_centrado(self.pantalla, pie, self.fuente_m, C["texto"], (ANCHO // 2, 460))

    def dibujar_tienda(self):
        """Dibuja la tienda de ropa con precios, bonus y el monedero."""
        self.pantalla.fill(C["pared"])
        texto_centrado(self.pantalla, "Ropero de Don Salmón", self.fuente_xl, C["texto"], (ANCHO // 2, 50))
        texto_centrado(self.pantalla, f"Monedero: ${self.monedero}", self.fuente_l, C["acento"], (ANCHO // 2, 102))
        for i, (clave, prenda) in enumerate(TIENDA.items()):
            fila = pygame.Rect(120, 140 + i * 66, 720, 58)
            dibujar_panel(self.pantalla, fila, C["panel"])
            if clave in self.jugador.compras:
                estado = "COMPRADO"
            elif prenda["requiere"] and prenda["requiere"] not in self.jugador.compras:
                estado = "BLOQUEADO"
            else:
                estado = f"${prenda['precio']}"
            self.pantalla.blit(self.fuente_m.render(f"[{i + 1}] {prenda['nombre']}", False, C["texto"]), (142, fila.top + 6))
            self.pantalla.blit(self.fuente_s.render(prenda["detalle"], False, C["texto"]), (142, fila.top + 33))
            texto_centrado(self.pantalla, estado, self.fuente_m, C["acento"], (fila.right - 90, fila.centery))
        dibujar_gato(self.pantalla, (900, 300), self.jugador.color, self.jugador.ropa, escala=1.6,
                     ojos=COLOR_OJOS_JUGADOR)
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