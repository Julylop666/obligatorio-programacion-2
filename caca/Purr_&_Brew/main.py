"""main.py - Purr & Brew 2D: bucle principal y máquina de estados.

Estados: HISTORIA_INTRO -> SELECCION_GATO -> TUTORIAL (Don Salmón explica en 3 páginas, la primera vez)
         -> JUGANDO -> DIA_COMPLETADO
         -> TIENDA_MEJORAS -> JUGANDO (día siguiente) ... -> VICTORIA_FINAL
         (y DERROTA si el local se desborda; con R se vuelve a jugar sin cerrar).
Durante JUGANDO se puede pausar con P, Esc o el botón || del HUD. La música (M) y los sonidos (N) se
silencian en cualquier momento, también sin pausar. En la pausa además se regula el volumen (flechas
izquierda/derecha, + y - o clic en la barra) y se vuelve a ver el tutorial (T).
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
                    texto_centrado, frame_caminata, dibujar_boton)
from escenas import crear_escenas
from ventana import VentanaDia
from tutorial import Tutorial


def cargar_sonidos(volumen=VOLUMEN_INICIAL):
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
            sonido.set_volume(VOLUMEN_EFECTOS * VOLUMEN_RELATIVO.get(clave, 1.0) * volumen)
            sonidos[clave] = sonido
        except (pygame.error, FileNotFoundError) as error:
            print(f"Aviso: no se pudo cargar {ruta}: {error}")
    return sonidos


def iniciar_musica(volumen=VOLUMEN_INICIAL):
    """Carga y reproduce en loop la música de fondo. Devuelve True si pudo, False si no."""
    ruta = os.path.join(RUTA_SONIDOS, ARCHIVO_MUSICA)
    try:
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.set_volume(VOLUMEN_MUSICA * volumen)
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


def prenda_desbloqueada(prenda, dia):
    """Indica si la prenda ya está disponible en la tienda de este día."""
    return dia >= prenda.get("dia_desbloqueo", 1)


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
        self.volumen = VOLUMEN_INICIAL          # control de volumen de la pausa (0.0 a 1.0)
        self.sonidos = cargar_sonidos(self.volumen)
        self.musica_ok = iniciar_musica(self.volumen) if self.sonidos else False
        self.musica_activada = True            # lo que elige el jugador en el menú de pausa
        self.efectos_activados = True
        self.fondo = crear_fondo()
        self.ventana = VentanaDia()
        self.escenas = crear_escenas(self.fuente_titulo, self.fuente_l)
        self.tutorial = Tutorial({"xl": self.fuente_xl, "l": self.fuente_l, "m": self.fuente_m,
                                  "s": self.fuente_s, "xs": self.fuente_xs})
        self.tutorial_visto = False            # se muestra solo la primera vez (después, con T en la pausa)
        self.tutorial_desde_pausa = False
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
        if self.efectos_activados and clave in self.sonidos:
            self.sonidos[clave].play()

    def avisar(self, texto, duracion=DURACION_AVISO):
        """Muestra un mensaje breve arriba de la pantalla (\\n separa líneas)."""
        self.aviso_texto = texto
        self.aviso_t = duracion

    def objetos_activos(self):
        """Devuelve las estaciones ya desbloqueadas y las mesas (lo que se puede usar)."""
        return [e for e in self.estaciones if e.activa] + self.mesas

    def obstaculos_movimiento(self):
        """Devuelve las mesas y el tacho, que bloquean el paso del jugador."""
        return ([mesa.rect for mesa in self.mesas]
                + [estacion.rect for estacion in self.estaciones if estacion.clave == "basura"])

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
        self.actualizar_musica()                      # reiniciar desde la pausa no deja la música callada

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
        self.actualizar_musica()

    def actualizar_musica(self):
        """Hace que la música suene solo si está activada y el juego no está en pausa."""
        if not self.musica_ok:
            return
        if self.musica_activada and not self.pausado:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def alternar_musica(self):
        """Prende o apaga la música (botón del menú de pausa o tecla M)."""
        if not self.musica_ok:
            self.avisar("La música no está disponible (mirá la consola).")
            return
        self.musica_activada = not self.musica_activada
        self.actualizar_musica()
        self.avisar_audio("Música", self.musica_activada)

    def alternar_efectos(self):
        """Prende o apaga los efectos de sonido (botón del menú de pausa o tecla N)."""
        if not self.sonidos:
            self.avisar("Los sonidos no están disponibles (mirá la consola).")
            return
        self.efectos_activados = not self.efectos_activados
        if self.efectos_activados:
            self.reproducir("topping")                # un sonidito para confirmar que ya suenan
        else:
            pygame.mixer.stop()                       # corta los efectos que estén sonando (no la música)
        self.avisar_audio("Sonidos", self.efectos_activados)

    def avisar_audio(self, nombre, activado):
        """Cartelito 'Música: apagada' al silenciar sin pausa (en la pausa ya lo dice el botón)."""
        if not self.pausado and self.estado == JUGANDO:
            self.avisar(f"{nombre}: {'prendida' if activado else 'apagada'}", 1.5)

    def cambiar_volumen(self, nivel):
        """Fija el volumen general (0.0 a 1.0, de a PASO_VOLUMEN) y se lo aplica a música y efectos."""
        nivel = round(min(1.0, max(0.0, nivel)) / PASO_VOLUMEN) * PASO_VOLUMEN
        self.volumen = round(nivel, 2)
        for clave, sonido in self.sonidos.items():
            sonido.set_volume(VOLUMEN_EFECTOS * VOLUMEN_RELATIVO.get(clave, 1.0) * self.volumen)
        if self.musica_ok:
            pygame.mixer.music.set_volume(VOLUMEN_MUSICA * self.volumen)
        self.reproducir("topping")                    # un sonidito para escuchar cómo quedó

    def subir_volumen(self, paso):
        """Sube (paso > 0) o baja (paso < 0) el volumen un escalón."""
        self.cambiar_volumen(self.volumen + paso * PASO_VOLUMEN)

    def abrir_tutorial(self, desde_pausa):
        """Muestra el tutorial de Don Salmón. Si se abrió desde la pausa, al cerrarlo se vuelve a ella."""
        self.tutorial.reiniciar(desde_pausa)
        self.tutorial_desde_pausa = desde_pausa
        self.tutorial_visto = True
        self.estado = TUTORIAL

    def cerrar_tutorial(self):
        """Termina o salta el tutorial: vuelve a la pausa o arranca el día, según de dónde venga."""
        if self.tutorial_desde_pausa:
            self.estado = JUGANDO                     # sigue pausado: reaparece el menú de pausa
        else:
            self.iniciar_dia()

    def pasar_pagina_tutorial(self):
        """Avanza una página del tutorial; después de la última lo cierra."""
        if self.tutorial.siguiente():
            self.cerrar_tutorial()

    def clic_tutorial(self, pos):
        """Clic en uno de los botones de abajo del tutorial."""
        accion = self.tutorial.clic(pos)
        if accion == "siguiente":
            self.pasar_pagina_tutorial()
        elif accion == "atras":
            self.tutorial.anterior()
        elif accion == "saltar":
            self.cerrar_tutorial()

    def clic_pausa(self, pos):
        """Clic con el juego en pausa: botones del menú; un clic afuera del menú sigue el juego."""
        botones = {nombre: pygame.Rect(rect) for nombre, rect in BOTONES_PAUSA.items()}
        if pygame.Rect(BOTON_PAUSA).collidepoint(pos) or botones["continuar"].collidepoint(pos):
            self.cambiar_pausa()
        elif botones["musica"].collidepoint(pos):
            self.alternar_musica()
        elif botones["efectos"].collidepoint(pos):
            self.alternar_efectos()
        elif botones["tutorial"].collidepoint(pos):
            self.abrir_tutorial(True)
        elif botones["vol_menos"].collidepoint(pos):
            self.subir_volumen(-1)
        elif botones["vol_mas"].collidepoint(pos):
            self.subir_volumen(1)
        elif pygame.Rect(RECT_BARRA_VOLUMEN).collidepoint(pos):
            barra = pygame.Rect(RECT_BARRA_VOLUMEN)
            tramo = int((pos[0] - barra.left) * 10 / barra.width) + 1      # 1 a 10
            self.cambiar_volumen(tramo * PASO_VOLUMEN)
        elif not pygame.Rect(RECT_PANEL_PAUSA).collidepoint(pos):
            self.cambiar_pausa()

    def comprar(self, clave):
        """Intenta comprar una prenda. Descuenta del monedero y se la pone al gato."""
        prenda = TIENDA[clave]
        if clave in self.jugador.compras:
            self.avisar("Ya tenés esa prenda.")
        elif not prenda_desbloqueada(prenda, self.dia):
            self.avisar(f"Se desbloquea el día {prenda['dia_desbloqueo']}.")
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
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.estado == TUTORIAL:
            self.clic_tutorial(evento.pos)
            return True
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.estado == JUGANDO:
            if self.pausado:
                self.clic_pausa(evento.pos)
            elif pygame.Rect(BOTON_PAUSA).collidepoint(evento.pos):
                self.cambiar_pausa()
            return True
        if evento.type != pygame.KEYDOWN:
            return True
        tecla = evento.key
        confirmar = tecla in (pygame.K_SPACE, pygame.K_RETURN)
        if self.estado == TUTORIAL:
            if confirmar or tecla in (pygame.K_RIGHT, pygame.K_d):
                self.pasar_pagina_tutorial()
            elif tecla in (pygame.K_LEFT, pygame.K_a):
                self.tutorial.anterior()
            elif tecla == pygame.K_ESCAPE:
                self.cerrar_tutorial()
            return True
        if tecla == pygame.K_m:                          # silenciar rápido: vale en todo el juego
            self.alternar_musica()
        elif tecla == pygame.K_n:
            self.alternar_efectos()
        elif self.estado == JUGANDO and tecla in (pygame.K_p, pygame.K_ESCAPE):
            self.cambiar_pausa()
        elif self.estado == JUGANDO and self.pausado:
            if tecla == pygame.K_r:
                self.nueva_partida()
                self.vineta = -1
                self.estado = HISTORIA_INTRO
            elif tecla == pygame.K_t:
                self.abrir_tutorial(True)
            elif tecla in (pygame.K_RIGHT, pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                self.subir_volumen(1)
            elif tecla in (pygame.K_LEFT, pygame.K_MINUS, pygame.K_KP_MINUS):
                self.subir_volumen(-1)
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
                if self.tutorial_visto:
                    self.iniciar_dia()
                else:
                    self.abrir_tutorial(False)        # la primera vez, Don Salmón explica antes de abrir
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
        self.jugador.mover(dt, pygame.key.get_pressed(), self.obstaculos_movimiento())
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
        textos = [self.fuente_s.render(linea, False, C["dorado"]) if linea == AVISO_TUTORIAL
                  else self.fuente_m.render(linea, False, C["texto_claro"]) for linea in lineas]
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
        sobre_boton = boton.collidepoint(pygame.mouse.get_pos())
        dibujar_panel(self.pantalla, boton, C["azul"] if self.pausado else C["dorado"] if sobre_boton else C["leche"])
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
        """Dibuja el menú de pausa: botones de música, sonidos y tutorial, y la barra de volumen."""
        self.pantalla.blit(self.velo_pausa, (0, 0))
        dibujar_panel(self.pantalla, RECT_PANEL_PAUSA)
        texto_centrado(self.pantalla, "PAUSA", self.fuente_xl, C["acento"], (ANCHO // 2, 138))
        mouse = pygame.mouse.get_pos()
        botones = {nombre: pygame.Rect(rect) for nombre, rect in BOTONES_PAUSA.items()}
        etiqueta_musica = ("Música: SÍ [M]" if self.musica_activada else "Música: NO [M]") if self.musica_ok \
            else "Música: no hay"
        etiqueta_efectos = ("Sonidos: SÍ [N]" if self.efectos_activados else "Sonidos: NO [N]") if self.sonidos \
            else "Sonidos: no hay"
        for nombre, etiqueta, color, activo in (
                ("musica", etiqueta_musica, C["verde"], self.musica_ok and self.musica_activada),
                ("efectos", etiqueta_efectos, C["verde"], bool(self.sonidos) and self.efectos_activados),
                ("tutorial", "Tutorial [T]", C["azul"], True),
                ("continuar", "Continuar [P]", C["dorado"], True),
                ("vol_menos", "-", C["leche"], self.volumen > 0),
                ("vol_mas", "+", C["leche"], self.volumen < 1)):
            dibujar_boton(self.pantalla, botones[nombre], etiqueta, self.fuente_s, color,
                          resaltado=botones[nombre].collidepoint(mouse), activo=activo)
        self.dibujar_barra_volumen()
        texto_centrado(self.pantalla, "P, Esc o clic afuera para continuar", self.fuente_m, C["texto"], (ANCHO // 2, 322))
        texto_centrado(self.pantalla, "R - Reiniciar partida", self.fuente_m, C["acento"], (ANCHO // 2, 356))
        texto_centrado(self.pantalla, "Los vecinos esperan con paciencia.", self.fuente_s, C["texto"], (ANCHO // 2, 390))
        texto_centrado(self.pantalla, "WASD / flechas: moverte  -  E / Espacio: interactuar",
                       self.fuente_s, C["texto"], (ANCHO // 2, 418))
        if not self.sonidos:
            texto_centrado(self.pantalla, "Sonido: no disponible (mirá la consola)", self.fuente_s, C["acento"],
                           (ANCHO // 2, 446))
        else:
            texto_centrado(self.pantalla, "Flechas izq/der o + / -: volumen", self.fuente_s, C["acento"],
                           (ANCHO // 2, 446))

    def dibujar_barra_volumen(self):
        """Dibuja 'Volumen', la barra de 10 tramos (entre los botones - y +) y el porcentaje."""
        self.pantalla.blit(self.fuente_m.render("Volumen", False, C["texto"]), (200, 247))
        barra = pygame.Rect(RECT_BARRA_VOLUMEN)
        lleno = round(self.volumen / PASO_VOLUMEN)
        ancho = barra.width // 10
        for i in range(10):
            tramo = pygame.Rect(barra.left + i * ancho, barra.top + 6, ancho - 3, barra.height - 12)
            pygame.draw.rect(self.pantalla, C["verde"] if i < lleno else C["sombra"], tramo)
            pygame.draw.rect(self.pantalla, C["zocalo"], tramo, 2)
        texto_centrado(self.pantalla, f"{round(self.volumen * 100)}%", self.fuente_m, C["acento"], (700, 260))

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
            texto_centrado(self.pantalla, "E / Espacio: interactuar  -  P: pausa  -  M / N: música y sonidos", self.fuente_s, C["texto"],
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
        texto_centrado(self.pantalla, "Elegí tu pelaje", self.fuente_xl, C["texto"], (ANCHO // 2, 80))
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
            detalle = prenda["detalle"]
            if clave in self.jugador.compras:
                estado = "COMPRADO"
            elif not prenda_desbloqueada(prenda, self.dia):
                estado = "BLOQUEADO"
                detalle += f" · Disponible desde el día {prenda['dia_desbloqueo']}"
            elif prenda["requiere"] and prenda["requiere"] not in self.jugador.compras:
                estado = "BLOQUEADO"
            else:
                estado = f"${prenda['precio']}"
            self.pantalla.blit(self.fuente_m.render(f"[{i + 1}] {prenda['nombre']}", False, C["texto"]), (142, fila.top + 6))
            self.pantalla.blit(self.fuente_s.render(detalle, False, C["texto"]), (142, fila.top + 33))
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
        elif self.estado == TUTORIAL:
            self.tutorial.dibujar(self.pantalla, pygame.mouse.get_pos())
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