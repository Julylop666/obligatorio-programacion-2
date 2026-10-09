"""ajustes.py - Constantes de Purr & Brew 2D.

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
TITULO = "Purr & Brew 2D"

# ---------------------------------------------------------------- colores pastel
# Paleta "cozy menta y cielo": verdes y celestes apagados + madera y crema cálidos.
# Solo quedan rosas las cosas que lo piden (nariz y orejas de los gatos, frutilla).
COLORES_PASTEL = {
    "piso_a": (248, 228, 204),
    "piso_b": (241, 217, 189),
    "pared": (205, 228, 218),             # verde menta apagado
    "zocalo": (146, 190, 180),            # zócalo y bordes de paneles: verde agua apagado
    "barra": (196, 150, 110),
    "barra_tapa": (224, 186, 142),
    "mesa": (240, 205, 165),
    "mantel": (172, 208, 228),            # mantel celeste
    "texto": (94, 62, 52),
    "texto_claro": (255, 250, 243),
    "panel": (255, 247, 238),
    "acento": (68, 136, 146),             # textos destacados: verde azulado
    "verde": (170, 214, 172),
    "azul": (172, 202, 236),
    "dorado": (246, 206, 124),
    "cafe": (139, 94, 60),
    "leche": (255, 252, 246),
    "rosa_oreja": (250, 190, 200),      # SIGUE ROSA: interior de las orejas
    "rosa_nariz": (244, 143, 150),       # SIGUE ROSA: nariz de los gatos
    "sombra": (210, 185, 160),
    "billete": (150, 205, 150),
    "resaltado": (255, 255, 255),
    "contorno": (62, 42, 50),
    "madera_oscura": (150, 104, 76),
    "metal": (206, 210, 220),
    "metal_oscuro": (150, 156, 170),
    "caramelo": (150, 80, 30),
    "chocolate": (100, 58, 40),
    "cielo_a": (176, 212, 238),
    "cielo_b": (212, 233, 242),
    "cielo_c": (196, 222, 244),
    # --- colores del arte (escenarios, íconos, ropa), agrupados por uso
    "agua": (150, 200, 240),  # agua del platito
    "anteojos": (216, 207, 219),  # marco de los anteojos
    "azul_medio": (120, 170, 225),  # azul de la caja de leche y del crayón
    "blanco": (255, 255, 255),  # blanco puro (brillos, cofia, rayas del toldo)
    "bloqueada_madera": (170, 160, 160),  # mueble de una estación bloqueada
    "bloqueada_tapa": (200, 192, 192),  # tapa de una estación bloqueada
    "cartel_papel": (255, 248, 224),  # papel del cartelito
    "chaleco_verde": (112, 156, 124),  # chaleco de Don Salmón
    "cielo_d": (194, 223, 240),  # franja del cielo
    "cielo_e": (230, 242, 242),  # franja clara del cielo
    "cofia_verde": (130, 180, 155),  # cinta de la cofia
    "delantal_celeste": (130, 187, 214),  # delantal
    "dulce_base": (176, 98, 40),  # fondo del frasco de dulce de leche
    "dulce_pintitas": (214, 140, 66),  # pintitas del frasco de dulce de leche
    "edificio_celeste": (204, 216, 236),  # edificio celeste del fondo
    "edificio_verde": (188, 216, 198),  # edificio verde del fondo
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
    "papel_rayas": (190, 217, 207),  # rayas del papel tapiz
    "pared_fachada": (255, 236, 214),  # pared de la fachada
    "piso_punto": (232, 206, 176),  # puntitos de textura del piso
    "planta": (150, 205, 150),  # hojas de las macetas
    "reflejo_ventana": (222, 238, 250),  # reflejo del vidrio
    "brillo_dorado": (236, 166, 32),  # brillitos y aro de la mesa con plata sin juntar
    "boton_espresso": (140, 206, 184),  # botón verde de la máquina de espresso
    "menta": (166, 212, 192),  # menta (toldo, tapa del dulce de leche, tacita del estante)
    "cortina": (126, 182, 170),  # cortinas
    "verde_crayon": (118, 190, 150),  # crayón verde del cartelito
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
    "zapato_verde": (112, 198, 152),  # championes de cocina
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
                    (96, 122, 136), (255, 255, 255), (150, 110, 90)]
COLOR_OJOS_JUGADOR = (78, 150, 110)
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
CIELO_PORTADA_INICIO = (172, 210, 238)
CIELO_PORTADA_PASO = (5, 3, 0)
CIELO_PORTADA_FRANJAS = 10

# velo oscuro (con transparencia) que se pone sobre el juego al pausar
COLOR_VELO_PAUSA = (62, 42, 50, 150)

# alto de la pared del salón en pixeles del mundo (cada uno = PX_MUNDO pantalla); el zócalo son sus últimas 3 filas
FILAS_PARED = 53

# ---------------------------------------------------------------- ventana del salón (paso del tiempo)
# El cielo de la ventana avanza de la mañana a la tarde según cuánto de la meta del día juntaste
# (no hay temporizadores en el juego, así que el reloj nunca apura a nadie).
POS_VENTANA = (380, 68)          # esquina de arriba a la izquierda, en pantalla
VELOCIDAD_CIELO = 1.2            # qué tan rápido el cielo alcanza al progreso (más alto = más rápido)
VELOCIDAD_NUBES = 1.2            # pixeles del mundo por segundo
# Momentos del día: "t" es el progreso (0 = empieza el día, 1 = meta cumplida); entre uno y otro se mezcla.
MOMENTOS_DIA = [
    {"t": 0.00, "arriba": (186, 222, 240), "horizonte": (238, 240, 226), "sol": (255, 246, 206),
     "nube": (255, 255, 255), "colina_atras": (164, 210, 182), "colina_frente": (124, 182, 150)},
    {"t": 0.50, "arriba": (146, 202, 240), "horizonte": (216, 238, 246), "sol": (255, 244, 190),
     "nube": (255, 255, 255), "colina_atras": (150, 204, 170), "colina_frente": (110, 176, 138)},
    {"t": 1.00, "arriba": (166, 194, 228), "horizonte": (252, 220, 170), "sol": (255, 214, 140),
     "nube": (255, 240, 222), "colina_atras": (168, 196, 150), "colina_frente": (128, 168, 120)},
]

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
POS_INICIAL = (480, 253)
ALCANCE_INTERACCION = 34
ZONA_JUEGO = pygame.Rect(20, 223, 920, 397)

# ---------------------------------------------------------------- estaciones y mesas
# Ancho de 104px por mueble con un salto de 130px entre cada uno. Las 7 de la barra están a y=128
# (bajadas 48px para que entre la ventana del salón en la pared).
ESTACIONES_RECT = {
    "leche": (30, 128, 104, 72),
    "vapor": (160, 128, 104, 72),
    "espresso": (290, 128, 104, 72),
    "medialunas": (420, 128, 104, 72),
    "frutilla": (550, 128, 104, 72),
    "dulce": (680, 128, 104, 72),
    "syrup": (810, 128, 104, 72),
    "basura": (830, 500, 104, 72),
}

# día desde el cual se puede usar cada estación
DIA_ESTACION = {"frutilla": 2, "dulce": 3, "syrup": 4, "basura": 1}
CENTROS_MESAS = [(300, 344), (500, 344), (700, 344),
                 (300, 524), (500, 524), (700, 524)]
TAM_MESA = 80
DESPLAZAMIENTO_ASIENTO = 65

# ---------------------------------------------------------------- clientes
PUERTA = (-40, 580)
POS_COLA_X = 70
POS_COLA_Y = 270
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
DIA_ITEM = {"cafe": 1, "cafe_syrup": 4, "medialuna": 1, "medialuna_frutilla": 2,
            "medialuna_dulce": 3}

AVISO_TUTORIAL = "Tutorial: T en la pausa"     # última línea (más chica) de los carteles de novedad

AVISOS_DESBLOQUEO = {
    2: "¡Novedad! Medialunas con frutilla.\nSacá una medialuna y pasala por la estación de Frutilla.\n" + AVISO_TUTORIAL,
    3: "¡Novedad! Medialunas con dulce de leche.\nPasá una medialuna por la estación de Dulce de leche.\n" + AVISO_TUTORIAL,
    4: "¡Novedad! Café con vainilla.\nLlevá un café simple a la estación Vainilla.\n" + AVISO_TUTORIAL,
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
                     "dia_desbloqueo": 2,
                     "detalle": "+30% de velocidad"},
    "gorro_2":      {"nombre": "Sombrero de chef", "precio": 90, "slot": "gorro", "nivel": 2,
                     "atributo": "capacidad_bandeja", "valor": 3, "requiere": "gorro_1",
                     "dia_desbloqueo": 3,
                     "detalle": "Bandeja para 3 ítems"},
}

# ---------------------------------------------------------------- sonido
# Cada acción tiene su propio sonido (antes "miau" sonaba en casi todo).
ARCHIVOS_SONIDO = {
    "miau": "miau.wav",              # elegir gato
    "leche": "leche.wav",            # servir leche
    "vapor": "vapor.wav",            # vaporizador
    "espresso": "espresso.wav",      # máquina de espresso
    "medialuna": "medialuna.wav",    # sacar una medialuna
    "topping": "topping.wav",        # frutilla / dulce de leche / vainilla
    "tacho": "tacho.wav",            # tirar un ítem
    "parcial": "parcial.wav",        # entregaste solo una parte del pedido
    "entrega": "entrega.wav",        # pedido completo
    "billete": "billete.wav",        # juntar la plata de la mesa
    "caja": "caja.wav",              # comprar ropa
    "dia_completo": "dia_completo.wav",  # meta del día cumplida
}
ARCHIVO_MUSICA = "musica_lofi.wav"
# Los .wav ya vienen parejos (misma sonoridad, ver generar_sonidos.py). Estos volúmenes son
# los que se usan en el juego: el general y un ajuste fino por sonido (1.0 = sin cambios).
# Volúmenes al 100% del control de la pausa. El juego arranca en VOLUMEN_INICIAL (0.7), que suena igual
# que antes; con las flechas en la pausa se baja hasta silencio o se sube un poco más.
VOLUMEN_EFECTOS = 0.86
VOLUMEN_MUSICA = 0.72
VOLUMEN_INICIAL = 0.7
PASO_VOLUMEN = 0.1
VOLUMEN_RELATIVO = {"miau": 0.8, "vapor": 0.9, "caja": 0.85, "dia_completo": 0.9}

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
 "Te recibiste de Diseñador con el mejor promedio. Armaste tu portafolio en Behance "
 "con obras digitales hermosas, pero el mercado está difícil y no sale nada. Caminando por el barrio "
 "ves un cartelito escrito con marcador en la ventana de una cafetería: \"Se busca barista "
 "principiante. Se enseña desde cero. Hay leche de dulce de leche y buena onda.\""),

("Don Salmón",
 "Te recibe Don Salmón, un gato viejo, esponjoso, con lentes en la punta de la nariz y un "
 "chaleco tejido: \"¡Buenas! Qué lindo tu currículum, ¡qué arte que tenés en las manos! "
 "Mirá, la verdad es que yo ya estoy grande y el cuerpo me pide un descanso esta semana. Me "
 "voy unos días a la casa de mi hermana en el campo a tomar un poco de solcito...\""),

("El trato",
 "\"Tranqui que acá nadie nace sabiendo, yo te enseño. Es una pavada: agarrás la leche, la pasás "
 "por el vaporizador y le servís el espresso arriba. Si te animás, sacás unas medialunas "
 "calientitas del horno y listo el pollo. Atendé a los vecinos con una sonrisa, juntá tu platita "
 "y si te entusiasmás, en el ropero del fondo hay delantales y gorritos re coquetos. "
 "¡Mucho éxito en tu primer día!\"")
]


# ---------------------------------------------------------------- tutorial de Don Salmón y menú de pausa
TUTORIAL = "TUTORIAL"                              # estado: Don Salmón te explica cómo se juega
RECT_TUTORIAL_ILUSTRACION = (32, 14, 896, 276)     # cuadro de arriba, donde se muestra todo
RECT_TUTORIAL_TEXTO = (190, 300, 738, 262)         # globito de texto de Don Salmón
POS_DON_SALMON_TUTORIAL = (110, 562)               # donde apoya los pies Don Salmón
ESCALA_DON_SALMON_TUTORIAL = 2.0
BOTONES_TUTORIAL = {"saltar": (32, 574, 170, 42), "atras": (606, 574, 150, 42),
                    "siguiente": (766, 574, 162, 42)}

RECT_PANEL_PAUSA = (180, 96, 600, 448)
BOTONES_PAUSA = {"musica": (200, 180, 176, 46), "efectos": (392, 180, 176, 46),
                 "tutorial": (584, 180, 176, 46), "continuar": (330, 474, 300, 50),
                 "vol_menos": (322, 240, 40, 40), "vol_mas": (592, 240, 40, 40)}
RECT_BARRA_VOLUMEN = (370, 240, 214, 40)           # 10 tramos clickeables entre los botones - y +
