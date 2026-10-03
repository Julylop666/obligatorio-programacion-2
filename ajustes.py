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
}

# Pelajes entre los que elige el jugador (nombre, color)
PELAJES = [
    ("Naranja", (240, 170, 100)),
    ("Gris", (172, 178, 190)),
    ("Crema", (246, 226, 192)),
    ("Negro", (78, 72, 84)),
]
COLOR_DON_SALMON = (236, 150, 118)
COLORES_CLIENTES = [(240, 170, 100), (172, 178, 190), (246, 226, 192),
                    (200, 160, 130), (255, 205, 205), (190, 170, 220)]

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
TAM_JUGADOR = 34              # lado del rect de colisión
VELOCIDAD_BASE = 230          # píxeles por segundo
CAPACIDAD_BASE = 1            # ítems en la bandeja
POS_INICIAL = (480, 205)
ALCANCE_INTERACCION = 34      # distancia extra para poder interactuar
ZONA_JUEGO = pygame.Rect(20, 175, 920, 445)

# ---------------------------------------------------------------- estaciones y mesas
ESTACIONES_RECT = {
    "leche": (70, 80, 120, 70),
    "vapor": (230, 80, 120, 70),
    "espresso": (390, 80, 120, 70),
    "medialunas": (550, 80, 120, 70),
}
CENTROS_MESAS = [(300, 320), (500, 320), (700, 320),
                 (300, 500), (500, 500), (700, 500)]
TAM_MESA = 80
DESPLAZAMIENTO_ASIENTO = 65   # el cliente se sienta a la izquierda de la mesa

# ---------------------------------------------------------------- clientes
PUERTA = (-40, 580)
POS_COLA_X = 70
POS_COLA_Y = 250
SEPARACION_COLA = 60
VELOCIDAD_CLIENTE = 130
TIEMPO_SENTADO = 1.0          # segundos mirando el menú antes de pedir
MAX_COLA = 4                  # si 4 vecinos quedan sin mesa, el local se desborda (derrota)

# ---------------------------------------------------------------- menú y niveles
PRECIOS = {"cafe": 12, "medialuna": 8}
NOMBRES_ITEMS = {"cafe": "Café con leche", "medialuna": "Medialuna"}

# meta de recaudación por día, ritmo de llegada de clientes y máximo de ítems por pedido
NIVELES = {
    1: {"meta": 50,  "intervalo": 9.0, "max_items": 1},
    2: {"meta": 120, "intervalo": 8.0, "max_items": 1},
    3: {"meta": 220, "intervalo": 7.0, "max_items": 2},
    4: {"meta": 350, "intervalo": 6.5, "max_items": 2},
    5: {"meta": 500, "intervalo": 6.0, "max_items": 2},
}
DIAS_TOTALES = len(NIVELES)

# ---------------------------------------------------------------- tienda de ropa
# slot: parte del cuerpo; nivel: qué tan avanzada es la prenda; atributo: qué mejora
TIENDA = {
    "delantal":     {"nombre": "Delantal gastronómico", "precio": 30, "slot": "delantal", "nivel": 1,
                     "atributo": "multiplicador_propina", "valor": 1.20, "requiere": None,
                     "detalle": "+20% de dinero por pedido"},
    "zapatillas_1": {"nombre": "Calzado antideslizante", "precio": 30, "slot": "calzado", "nivel": 1,
                     "atributo": "velocidad", "valor": 1.15, "requiere": None,
                     "detalle": "+15% de velocidad"},
    "gorro_1":      {"nombre": "Cofia de cocina", "precio": 50, "slot": "gorro", "nivel": 1,
                     "atributo": "capacidad_bandeja", "valor": 2, "requiere": None,
                     "detalle": "Bandeja para 2 ítems"},
    "zapatillas_2": {"nombre": "Zapatillas de cocina", "precio": 60, "slot": "calzado", "nivel": 2,
                     "atributo": "velocidad", "valor": 1.30, "requiere": "zapatillas_1",
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
VOLUMEN_EFECTOS = 0.6
VOLUMEN_MUSICA = 0.25

# ---------------------------------------------------------------- textos
DURACION_AVISO = 2.5          # segundos que se ve un mensaje en pantalla

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
