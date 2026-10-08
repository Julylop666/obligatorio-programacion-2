"""ajustes.py - Constantes de Michi Café 2D.

Acá viven TODOS los colores, tamaños, velocidades, textos de la historia,
los niveles (metas de dinero por día) y la tienda de ropa.
Si querés cambiar el balance del juego, solo tocás este archivo.
"""
import os
import pygame

# ---------------------------------------------------------------- rutas
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_SONIDOS = os.path.join(RUTA_BASE, "sonidos")
RUTA_IMAGENES = os.path.join(RUTA_BASE, "imagenes")
RUTA_FUENTE = os.path.join(RUTA_BASE, "fuentes", "Jersey15.ttf")

# ---------------------------------------------------------------- ventana
ANCHO = 960
ALTO = 640
FPS = 60
TITULO = "Michi Café 2D"

# ---------------------------------------------------------------- colores pastel
COLORES_PASTEL = {
    "piso_a": (248, 228, 204),
    "piso_b": (241, 217, 189),
    "pared": (255, 224, 214),
    "zocalo": (226, 170, 150),
    "barra": (196, 150, 110),
    "barra_tapa": (224, 186, 142),
    "mesa": (240, 205, 165),
    "mantel": (255, 190, 202),
    "texto": (94, 62, 52),
    "texto_claro": (255, 250, 243),
    "panel": (255, 247, 238),
    "acento": (244, 143, 150),
    "verde": (170, 214, 172),
    "azul": (172, 202, 236),
    "dorado": (246, 206, 124),
    "cafe": (139, 94, 60),
    "leche": (255, 252, 246),
    "rosa_oreja": (250, 190, 200),
    "sombra": (210, 185, 160),
    "billete": (150, 205, 150),
    "resaltado": (255, 255, 255),
    "contorno": (62, 42, 50),
    "madera_oscura": (150, 104, 76),
    "metal": (206, 210, 220),
    "metal_oscuro": (150, 156, 170),
    "caramelo": (150, 80, 30),
    "chocolate": (100, 58, 40),
    "cielo_a": (255, 214, 200),
    "cielo_b": (255, 232, 210),
    "cielo_c": (196, 222, 244),
    # --- colores del arte (escenarios, íconos, ropa), agrupados por uso
    "agua": (150, 200, 240),  # agua del platito
    "anteojos": (214, 170, 90),  # marco de los anteojos
    "azul_medio": (120, 170, 225),  # azul de la caja de leche y del crayón
    "blanco": (255, 255, 255),  # blanco puro (brillos, cofia, rayas del toldo)
    "bloqueada_madera": (170, 160, 160),  # mueble de una estación bloqueada
    "bloqueada_tapa": (200, 192, 192),  # tapa de una estación bloqueada
    "cartel_papel": (255, 248, 224),  # papel del cartelito
    "chaleco_verde": (112, 156, 124),  # chaleco de Don Salmón
    "cielo_d": (255, 222, 204),  # franja del cielo del atardecer
    "cielo_e": (255, 240, 220),  # franja clara del cielo
    "cofia_verde": (130, 180, 155),  # cinta de la cofia
    "delantal_celeste": (130, 187, 214),  # delantal
    "dulce_base": (176, 98, 40),  # fondo del frasco de dulce de leche
    "dulce_pintitas": (214, 140, 66),  # pintitas del frasco de dulce de leche
    "edificio_lila": (214, 206, 230),  # edificio lila del fondo
    "edificio_rosa": (238, 200, 200),  # edificio rosa del fondo
    "espuma": (244, 228, 205),  # espuma del café
    "farol_poste": (96, 96, 120),  # poste del farol de la calle
    "frutilla_cobertura": (240, 110, 150),  # cobertura de frutilla
    "frutilla_crema": (255, 235, 240),  # fondo del frasco de frutilla
    "frutilla_pintitas": (230, 100, 145),  # pintitas del frasco de frutilla
    "frutilla_tapa": (192, 72, 110),  # tapa del frasco de frutilla
    "ladrillo": (255, 222, 196),  # líneas de ladrillo de la fachada
    "luz_amarilla": (255, 220, 120),  # lucecita de la máquina de espresso
    "maceta": (178, 110, 80),  # maceta de barro
    "masa_clara": (236, 174, 86),  # masa de la medialuna
    "masa_oscura": (203, 132, 58),  # pliegues de la medialuna
    "masa_sombra": (155, 112, 55),  # sombra de la medialuna
    "metal_espresso": (132, 124, 140),  # cuerpo de la máquina de espresso
    "nube": (255, 250, 245),  # nubes
    "papel_rayas": (250, 212, 202),  # rayas del papel tapiz
    "pared_fachada": (255, 236, 214),  # pared de la fachada
    "piso_punto": (232, 206, 176),  # puntitos de textura del piso
    "planta": (150, 205, 150),  # hojas de las macetas
    "reflejo_ventana": (222, 238, 250),  # reflejo del vidrio
    "rosa_boton": (248, 150, 170),  # botón rosa de la máquina de espresso
    "rosa_claro": (248, 160, 180),  # rosa claro (toldo, tapa del dulce de leche, cortinas)
    "rosa_crayon": (248, 143, 150),  # crayón rosa del cartelito
    "sol_centro": (255, 246, 214),  # centro del sol
    "sol_halo": (255, 232, 196),  # halo del sol de la portada
    "sol_luz": (255, 236, 190),  # sol de la viñeta 1
    "sol_ventana": (255, 240, 190),  # sol visto por la ventana / luz de la lámpara
    "tablas_barra": (172, 126, 92),  # tablas del mostrador
    "taza_crema": (255, 240, 225),  # tacita crema del estante
    "vainilla": (245, 210, 110),  # jarabe de vainilla
    "vainilla_crema": (255, 245, 214),  # fondo del frasco de vainilla
    "vainilla_pintitas": (233, 200, 130),  # pintitas del frasco de vainilla
    "vainilla_tapa": (178, 132, 82),  # tapa del frasco de vainilla
    "vapor_claro": (240, 242, 248),  # brillo de la jarra del vaporizador
    "ventana_edificio": (255, 246, 232),  # ventanitas de los edificios
    "vereda": (214, 204, 222),  # vereda
    "vereda_borde": (190, 180, 204),  # borde de la vereda
    "vereda_raya": (196, 186, 210),  # rayas de la vereda
    "zapato_celeste": (120, 190, 235),  # championes antideslizantes
    "zapato_rosa": (240, 120, 150),  # championes de cocina
}

# Pelajes entre los que elige el jugador (nombre, color)
PELAJES = [
    ("Naranja", (240, 170, 100)),
    ("Gris", (172, 178, 190)),
    ("Crema", (246, 226, 192)),
    ("Negro", (78, 72, 84)),
]
COLOR_DON_SALMON = (236, 150, 118)
COLORES_CLIENTES = [(240, 170, 100), (172, 178, 190), (200, 160, 130),
                    (255, 205, 205), (190, 170, 220), (150, 110, 90)]
COLOR_OJOS_JUGADOR = (70, 205, 110)
COLOR_OJOS_CLIENTE = (50, 35, 45)

# ---------------------------------------------------------------- pixel art
PX_GATO = 3
PX_ITEM = 2
PX_MUNDO = 4

# animación de los gatos y tamaños del arte
VELOCIDAD_ANIMACION = 9          # cuadros de patitas por segundo al caminar
ALTO_SOMBRERO = 6                # filas libres arriba de la cabeza para los gorros
GROSOR_BORDE_PANEL = 4           # grosor del borde de los paneles (un pixel del mundo)
TAM_ESCENA = (880, 320)          # tamaño en pantalla de las viñetas de la historia

# cielo de la portada: franjas que van de un color inicial sumando un paso por franja
CIELO_PORTADA_INICIO = (255, 200, 196)
CIELO_PORTADA_PASO = (0, 4, 2)
CIELO_PORTADA_FRANJAS = 10

# velo oscuro (con transparencia) que se pone sobre el juego al pausar
COLOR_VELO_PAUSA = (62, 42, 50, 150)

# ---------------------------------------------------------------- estados del juego
HISTORIA_INTRO = "HISTORIA_INTRO"
SELECCION_GATO = "SELECCION_GATO"
JUGANDO = "JUGANDO"
DIA_COMPLETADO = "DIA_COMPLETADO"
TIENDA_MEJORAS = "TIENDA_MEJORAS"
DERROTA = "DERROTA"
VICTORIA_FINAL = "VICTORIA_FINAL"

# estados de un cliente
LLEGANDO = "Llegando"
SENTADO = "Sentado"
ESPERANDO = "Esperando"
ATENDIDO = "Atendido"

# estados de la taza que prepara el jugador
TAZA_VACIA = 0
TAZA_LECHE = 1
TAZA_CALIENTE = 2

# ---------------------------------------------------------------- jugador
TAM_JUGADOR = 34
VELOCIDAD_BASE = 230
CAPACIDAD_BASE = 1
POS_INICIAL = (480, 205)
ALCANCE_INTERACCION = 34
ZONA_JUEGO = pygame.Rect(20, 175, 920, 445)

# ---------------------------------------------------------------- estaciones y mesas
# Ancho de 96px por mueble con un salto perfecto de 112px entre cada uno
ESTACIONES_RECT = {
    "leche": (30, 80, 104, 72),
    "vapor": (160, 80, 104, 72),
    "espresso": (290, 80, 104, 72),
    "medialunas": (420, 80, 104, 72),
    "frutilla": (550, 80, 104, 72),
    "dulce": (680, 80, 104, 72),
    "syrup": (810, 80, 104, 72),
    "basura": (830, 500, 104, 72),
}

# día desde el cual se puede usar cada estación
DIA_ESTACION = {"frutilla": 2, "dulce": 3, "syrup": 3, "basura": 1}
CENTROS_MESAS = [(300, 320), (500, 320), (700, 320),
                 (300, 500), (500, 500), (700, 500)]
TAM_MESA = 80
DESPLAZAMIENTO_ASIENTO = 65

# ---------------------------------------------------------------- clientes
PUERTA = (-40, 580)
POS_COLA_X = 70
POS_COLA_Y = 250
SEPARACION_COLA = 60
VELOCIDAD_CLIENTE = 130
TIEMPO_SENTADO = 1.0
MAX_COLA = 4

# ---------------------------------------------------------------- menú y niveles
PRECIOS = {"cafe": 12, "cafe_syrup": 14, "medialuna": 8, "medialuna_frutilla": 11,
           "medialuna_dulce": 11}
NOMBRES_ITEMS = {"cafe": "Café con leche", "cafe_syrup": "Café con vainilla",
                 "medialuna": "Medialuna", "medialuna_frutilla": "Medialuna con frutilla",
                 "medialuna_dulce": "Medialuna con dulce de leche"}
DIA_ITEM = {"cafe": 1, "cafe_syrup": 3, "medialuna": 1, "medialuna_frutilla": 2,
            "medialuna_dulce": 3}

AVISOS_DESBLOQUEO = {
    2: "¡Novedad! Medialunas con frutilla.\nSacá una medialuna y pasala por la estación de Frutilla.",
    3: "¡Novedad! Café con vainilla y medialunas con dulce de leche.\nUsá el jarabe y el frasco de dulce de leche.",
}

NIVELES = {
    1: {"meta": 50,  "intervalo": 9.0, "max_items": 1},
    2: {"meta": 120, "intervalo": 8.0, "max_items": 1},
    3: {"meta": 220, "intervalo": 7.0, "max_items": 2},
    4: {"meta": 350, "intervalo": 6.5, "max_items": 2},
    5: {"meta": 500, "intervalo": 6.0, "max_items": 2},
}
DIAS_TOTALES = len(NIVELES)

# ---------------------------------------------------------------- tienda de ropa
TIENDA = {
    "delantal":     {"nombre": "Delantal gastronómico", "precio": 30, "slot": "delantal", "nivel": 1,
                     "atributo": "multiplicador_propina", "valor": 1.20, "requiere": None,
                     "detalle": "+20% de dinero por pedido"},
    "championes_1": {"nombre": "Championes antideslizantes", "precio": 30, "slot": "calzado", "nivel": 1,
                     "atributo": "velocidad", "valor": 1.15, "requiere": None,
                     "detalle": "+15% de velocidad"},
    "gorro_1":      {"nombre": "Cofia de cocina", "precio": 50, "slot": "gorro", "nivel": 1,
                     "atributo": "capacidad_bandeja", "valor": 2, "requiere": None,
                     "detalle": "Bandeja para 2 ítems"},
    "championes_2": {"nombre": "Championes de cocina", "precio": 60, "slot": "calzado", "nivel": 2,
                     "atributo": "velocidad", "valor": 1.30, "requiere": "championes_1",
                     "detalle": "+30% de velocidad"},
    "gorro_2":      {"nombre": "Sombrero de chef", "precio": 90, "slot": "gorro", "nivel": 2,
                     "atributo": "capacidad_bandeja", "valor": 3, "requiere": "gorro_1",
                     "detalle": "Bandeja para 3 ítems"},
}

# ---------------------------------------------------------------- sonido
ARCHIVOS_SONIDO = {
    "miau": "miau.wav",
    "billete": "billete.wav",
    "vapor": "vapor.wav",
    "caja": "caja.wav",
}
ARCHIVO_MUSICA = "musica_lofi.wav"
VOLUMEN_EFECTOS = 0.9
VOLUMEN_MUSICA = 0.35

# ---------------------------------------------------------------- textos
DURACION_AVISO = 2.5
DURACION_AVISO_DIA = 5.0
BOTON_PAUSA = (156, 14, 36, 36)

# ---------------------------------------------------------------- HUD (barra de arriba)
RECT_HUD = (10, 8, 940, 56)
RECT_BARRA_META = (206, 20, 230, 24)
POS_MONEDERO = (456, 22)
POS_PREPARANDO = (655, 14)             # texto "Preparando" (el nombre va 20 px más abajo)
POS_BANDEJA_HUD = (810, 16)            # primera casilla de la bandeja
TAM_CASILLA_BANDEJA = 38
SEPARACION_CASILLA_BANDEJA = 42

ESCENAS_VINETAS = ["escena_calle", "escena_salmon", "escena_delantal"]

VINETAS = [
    ("El drama profesional",
     "Te recibiste de Licenciado en Diseño con las mejores notas. Armaste tu portafolio en Behance "
     "con tipografías hermosas, pero el mercado está bravo y no sale nada. Paseando por el barrio "
     "ves un cartelito dibujado con crayón en la ventana de una cafetería: \"Se busca barista "
     "principiante. Se enseña desde cero. Hay leche de almendras y buena onda.\""),
    ("Don Salmón",
     "Te recibe Don Salmón, un gato viejo, esponjoso, con anteojitos en la punta de la nariz y un "
     "chaleco tejido: \"¡Buenas! Che, qué lindo tu currículum, ¡qué arte que tenés en las manos! "
     "Mirá, la verdad es que yo ya estoy grande y los huesos me piden un descanso esta semana. Me "
     "voy unos días a la casa de mi hermana en el campo a tomar solcito...\""),
    ("El trato",
     "\"Tranqui que acá nadie nace sabiendo, yo te enseño. Es una papa: agarrás la leche, la pasás "
     "por el vaporizador y le mandás el espresso arriba. Si te animás, sacás unas medialunas "
     "calentitas del horno y listo el pollo. Atendé a los vecinos con una sonrisa, juntá tu platita "
     "y si te va bien, en el ropero del fondo hay delantales y gorritos re coquetos. "
     "¡Éxitos en tu primer día!\""),
]