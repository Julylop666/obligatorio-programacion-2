"""tutorial.py - El tutorial de Don Salmón: 3 páginas cortas, con dibujos de lo esencial.

El juego es intuitivo, así que el tutorial es breve: controles, recetas y cómo atender y cobrar.

Cada página tiene un título, el texto que "dice" Don Salmón en su globito y una función
que dibuja la ilustración de arriba. Las ilustraciones reutilizan las MISMAS estaciones, mesas,
clientes e ítems del juego (de estaciones.py, clientes.py y dibujo.py), así que lo que se ve
acá es exactamente lo que después aparece al jugar.

Para agregar o cambiar una página alcanza con editar la lista PAGINAS (arriba de la clase Tutorial).
"""
import pygame
from ajustes import (COLORES_PASTEL as C, PRECIOS, NOMBRES_ITEMS, COLOR_DON_SALMON, COLOR_OJOS_JUGADOR, PELAJES,
                     ESPERANDO, RECT_TUTORIAL_ILUSTRACION, RECT_TUTORIAL_TEXTO, POS_DON_SALMON_TUTORIAL,
                     ESCALA_DON_SALMON_TUTORIAL, BOTONES_TUTORIAL, PX_GATO)
from dibujo import (dibujar_gato, dibujar_item, dibujar_panel, dibujar_bandeja, dibujar_boton,
                    texto_envuelto, texto_centrado, frame_caminata)
from estaciones import EstacionLeche, EstacionVapor, EstacionEspresso, ExhibidorMedialunas, Mesa
from clientes import Cliente

COLOR_GATO_TUTORIAL = PELAJES[0][1]          # el gato naranja hace de jugador en los dibujos


# ---------------------------------------------------------------- piezas de dibujo reutilizables
def _estacion(lienzo, fuentes, clase, x, y, resaltada=False):
    """Dibuja una estación real del juego con su esquina de arriba a la izquierda en (x, y)."""
    estacion = clase()
    estacion.rect.topleft = (x, y)
    estacion.dibujar(lienzo, fuentes["xs"], resaltada)
    return estacion


def _flecha(lienzo, desde, hasta, color=None, grosor=6):
    """Dibuja una flecha gruesa desde un punto hasta otro (la punta queda en 'hasta')."""
    color = color or C["acento"]
    inicio, fin = pygame.math.Vector2(desde), pygame.math.Vector2(hasta)
    if inicio == fin:
        return
    u = (fin - inicio).normalize()
    n = pygame.math.Vector2(-u.y, u.x)
    base = fin - u * 16
    pygame.draw.line(lienzo, color, inicio, base, grosor)
    pygame.draw.polygon(lienzo, color, [fin, base + n * 11, base - n * 11])


def _tecla(lienzo, fuentes, centro, texto, ancho=52):
    """Dibuja una tecla del teclado con una letra o palabra adentro."""
    rect = pygame.Rect(0, 0, ancho, 52)
    rect.center = centro
    dibujar_panel(lienzo, rect, C["leche"])
    pygame.draw.rect(lienzo, C["sombra"], (rect.x + 8, rect.bottom - 12, rect.width - 16, 4))
    texto_centrado(lienzo, texto, fuentes["m"], C["texto"], (rect.centerx, rect.centery - 3))


def _tecla_flecha(lienzo, centro, direccion):
    """Dibuja una tecla de flecha del teclado (direccion: 'arriba', 'abajo', 'izq' o 'der')."""
    rect = pygame.Rect(0, 0, 52, 52)
    rect.center = centro
    dibujar_panel(lienzo, rect, C["leche"])
    cx, cy = rect.center
    puntas = {"arriba": [(cx, cy - 12), (cx - 11, cy + 8), (cx + 11, cy + 8)],
              "abajo": [(cx, cy + 12), (cx - 11, cy - 8), (cx + 11, cy - 8)],
              "izq": [(cx - 12, cy), (cx + 8, cy - 11), (cx + 8, cy + 11)],
              "der": [(cx + 12, cy), (cx - 8, cy - 11), (cx - 8, cy + 11)]}
    pygame.draw.polygon(lienzo, C["texto"], puntas[direccion])


def _numero(lienzo, fuentes, centro, numero):
    """Dibuja un cuadradito con el número de paso."""
    rect = pygame.Rect(0, 0, 34, 34)
    rect.center = centro
    dibujar_panel(lienzo, rect, C["acento"])
    texto_centrado(lienzo, str(numero), fuentes["m"], C["texto_claro"], (rect.centerx, rect.centery - 1))


def _cartel(lienzo, fuentes, centro, texto, tamano="m"):
    """Dibuja un cartelito oscuro como el que aparece abajo en el juego."""
    superficie = fuentes[tamano].render(texto, False, C["texto_claro"])
    rect = superficie.get_rect().inflate(36, 18)
    rect.center = centro
    dibujar_panel(lienzo, rect, C["texto"])
    lienzo.blit(superficie, superficie.get_rect(center=rect.center))


def _lineas(lienzo, fuentes, centro_x, y, lineas, tamano="s", color=None):
    """Escribe varias líneas centradas en x, una debajo de la otra, desde la altura y."""
    for i, linea in enumerate(lineas):
        texto_centrado(lienzo, linea, fuentes[tamano], color or C["texto"],
                       (centro_x, y + i * (fuentes[tamano].get_height() - 2)))


def _gato_jugador(lienzo, centro, ropa=None, bandeja=(), capacidad=1, escala=1.0, camina=False):
    """Dibuja al gato barista (ojos verdes) con su bandeja, igual que en el juego."""
    ropa = ropa or {}
    tiempo = pygame.time.get_ticks() / 1000
    cuadro = frame_caminata(tiempo, camina)
    dibujar_gato(lienzo, centro, COLOR_GATO_TUTORIAL, ropa, escala=escala, ojos=COLOR_OJOS_JUGADOR, frame=cuadro)
    if bandeja is not None:
        dibujar_bandeja(lienzo, centro, list(bandeja), capacidad, COLOR_GATO_TUTORIAL, 1, cuadro)


# ---------------------------------------------------------------- ilustraciones (una por página)
# Todas reciben el lienzo (880 x 260 px, el interior del cuadro de arriba) y las fuentes.
def _ilus_controles(l, f):
    """Moverse con WASD o flechas, y hacer todo con E o Espacio."""
    texto_centrado(l, "Moverte", f["l"], C["acento"], (210, 24))
    _tecla(l, f, (110, 88), "W")
    for x, letra in ((52, "A"), (110, "S"), (168, "D")):
        _tecla(l, f, (x, 146), letra)
    texto_centrado(l, "o", f["l"], C["texto"], (232, 118))
    _tecla_flecha(l, (330, 88), "arriba")
    for x, direccion in ((272, "izq"), (330, "abajo"), (388, "der")):
        _tecla_flecha(l, (x, 146), direccion)
    texto_centrado(l, "Las mesas y el tacho te cortan el paso", f["xs"], C["texto"], (210, 214))
    pygame.draw.line(l, C["zocalo"], (450, 20), (450, 240), 3)
    texto_centrado(l, "Hacer todo", f["l"], C["acento"], (665, 24))
    _tecla(l, f, (540, 88), "E")
    texto_centrado(l, "o", f["l"], C["texto"], (600, 88))
    _tecla(l, f, (700, 88), "Espacio", 130)
    _estacion(l, f, EstacionLeche, 540, 130, resaltada=True)
    _gato_jugador(l, (730, 176), bandeja=None, camina=True)
    texto_centrado(l, "Se usa lo que tengas más cerca (borde blanco)", f["xs"], C["texto"], (665, 228))


def _ilus_recetas(l, f):
    """Café en 3 pasos, medialunas directas y los toppings que se suman con los días."""
    for x, clase in ((16, EstacionLeche), (166, EstacionVapor), (316, EstacionEspresso)):
        _estacion(l, f, clase, x, 20)
    for x in (124, 274, 424):
        _flecha(l, (x + 2, 56), (x + 38, 56), grosor=5)
    dibujar_item(l, "cafe", (500, 56), px=6)
    l.blit(f["s"].render(f"{NOMBRES_ITEMS['cafe']}  ${PRECIOS['cafe']}", False, C["texto"]), (545, 40))
    _estacion(l, f, ExhibidorMedialunas, 16, 120)
    _flecha(l, (124, 156), (160, 156), grosor=5)
    dibujar_item(l, "medialuna", (212, 156), px=6)
    l.blit(f["s"].render(f"Medialuna  ${PRECIOS['medialuna']}", False, C["texto"]), (254, 140))
    pygame.draw.line(l, C["zocalo"], (16, 106), (864, 106), 3)
    texto_centrado(l, "Y con los días se suman estos toppings:", f["s"], C["acento"], (640, 126))
    extras = ((2, "medialuna_frutilla", "Frutilla"), (3, "medialuna_dulce", "Dulce de leche"),
              (4, "cafe_syrup", "Vainilla"))
    for i, (dia, item, nombre) in enumerate(extras):
        x = 490 + i * 140
        dibujar_item(l, item, (x, 176), px=4)
        texto_centrado(l, f"Día {dia}", f["xs"], C["texto"], (x, 214))
        texto_centrado(l, nombre, f["xs"], C["acento"], (x, 232))
    texto_centrado(l, "Frutilla y dulce de leche:", f["xs"], C["texto"], (150, 212))
    texto_centrado(l, "pasá una medialuna por el frasco.", f["xs"], C["texto"], (150, 230))
    texto_centrado(l, "Vainilla: al final, sobre un café.", f["xs"], C["texto"], (150, 248))


def _ilus_atender(l, f):
    """Mirar el globito, entregar el pedido y juntar la plata (que brilla en la mesa)."""
    pasos = ("Mirá el globito", "Llevale el pedido y apretá E", "Juntá la plata con E")
    ancho = l.get_width()
    centros = [round(ancho * (i + 0.5) / 3) for i in range(3)]
    for i, (paso, centro) in enumerate(zip(pasos, centros)):
        _numero(l, f, (centro, 24), i + 1)
        texto_centrado(l, paso, f["s"], C["texto"], (centro, 62))
    for i in (1, 2):
        x = round(ancho * i / 3)
        pygame.draw.line(l, C["zocalo"], (x, 82), (x, 244), 3)

    mesa = Mesa((centros[0] + 33, 190))                       # 1: el vecino con su pedido
    mesa.dibujar(l, f["s"])
    cliente = Cliente(["cafe", "medialuna_frutilla"], (172, 178, 190))
    cliente.pos = pygame.math.Vector2(centros[0] - 32, 190)
    cliente.estado = ESPERANDO
    cliente.dibujar(l)
    _gato_jugador(l, (centros[1] - 80, 190), ropa={"gorro": 1},
                  bandeja=["cafe", "medialuna_frutilla"], capacidad=2)
    _flecha(l, (centros[1] - 15, 190), (centros[1] + 40, 190), grosor=5)  # 2: se lo lleva a su mesa
    Mesa((centros[1] + 70, 190)).dibujar(l, f["s"], True)
    con_plata = Mesa((centros[2], 170))                        # 3: el vecino se fue y dejó plata
    con_plata.dinero = 23
    con_plata.dibujar(l, f["s"], True)
    texto_centrado(l, "Hasta que no la juntes,", f["xs"], C["texto"], (centros[2], 224))
    texto_centrado(l, "la mesa no se libera", f["xs"], C["texto"], (centros[2], 242))


# ---------------------------------------------------------------- las páginas: (título, lo que dice Don Salmón, ilustración)
PAGINAS = [
    ("¡Buenas! Soy Don Salmón",
     "Quedás a cargo de la cafetería 5 días. Cada día tenés una meta de plata: cuando la juntás, pasás "
     "al siguiente. Moverte es con W A S D o las flechas, y todo lo demás (agarrar, preparar, entregar "
     "y cobrar) es con E o Espacio. ¡Así de fácil!",
     _ilus_controles),
    ("Café y medialunas",
     "El café con leche va en orden: Leche, Vaporizador y Espresso. Las medialunas se sacan del horno y "
     "listo. Cada pedido aparece en un globito sobre el vecino. Con los días se suman frutilla, dulce de "
     "leche y vainilla: los carteles te avisan cuándo. Entre un día y otro hay ropa en mi ropero.",
     _ilus_recetas),
    ("Atender y cobrar",
     "Llevale el pedido a su mesa. Cuando se va, deja la plata sobre la mesa y ahí brilla: ¡juntala con E! "
     "Hasta que no lo hagas, la mesa no se libera, y si 4 vecinos se quedan sin mesa, perdés. Con P pausás "
     "y con T en la pausa volvés a ver este tutorial. ¡Mucho éxito!",
     _ilus_atender),
]


# ---------------------------------------------------------------- la pantalla del tutorial
class Tutorial:
    """Muestra las páginas de PAGINAS de a una, con Don Salmón hablando abajo a la izquierda."""

    def __init__(self, fuentes):
        """fuentes: diccionario con las fuentes del juego en las claves 'xl', 'l', 'm', 's' y 'xs'."""
        self.fuentes = fuentes
        self.pagina = 0
        self.desde_pausa = False

    def reiniciar(self, desde_pausa=False):
        """Vuelve a la primera página. desde_pausa cambia los textos de los botones de salida."""
        self.pagina = 0
        self.desde_pausa = desde_pausa

    def siguiente(self):
        """Pasa a la página siguiente. Devuelve True si ya era la última (el tutorial terminó)."""
        if self.pagina >= len(PAGINAS) - 1:
            return True
        self.pagina += 1
        return False

    def anterior(self):
        """Vuelve a la página anterior (en la primera se queda donde está)."""
        self.pagina = max(0, self.pagina - 1)

    def clic(self, pos):
        """Devuelve 'saltar', 'atras' o 'siguiente' si el clic cayó en ese botón; si no, None."""
        for nombre, rect in BOTONES_TUTORIAL.items():
            if pygame.Rect(rect).collidepoint(pos):
                return nombre
        return None

    def _texto_de_don_salmon(self, pantalla, titulo, texto, rect):
        """Escribe el título y el texto dentro del globito; si no entra con letra grande usa la chica."""
        f = self.fuentes
        pantalla.blit(f["l"].render(titulo, False, C["acento"]), (rect.left + 26, rect.top + 14))
        zona = pygame.Rect(rect.left + 26, rect.top + 62, rect.width - 52, rect.height - 76)
        fuente = f["m"]
        if texto_envuelto(pygame.Surface((1, 1)), texto, fuente, C["texto"], zona) > zona.bottom:
            fuente = f["s"]
        texto_envuelto(pantalla, texto, fuente, C["texto"], zona)

    def dibujar(self, pantalla, mouse=(0, 0)):
        """Dibuja la página actual completa: ilustración, Don Salmón con su globito y los botones."""
        f = self.fuentes
        titulo, texto, ilustracion = PAGINAS[self.pagina]
        pantalla.fill(C["pared"])
        marco = dibujar_panel(pantalla, RECT_TUTORIAL_ILUSTRACION, C["panel"])
        ilustracion(pantalla.subsurface(marco.inflate(-16, -16)), f)

        px = max(1, round(ESCALA_DON_SALMON_TUTORIAL * PX_GATO))
        pie_x, pie_y = POS_DON_SALMON_TUTORIAL
        dibujar_gato(pantalla, (pie_x, pie_y - 7 * px), COLOR_DON_SALMON, escala=ESCALA_DON_SALMON_TUTORIAL,
                     lentes=True, chaleco=True)
        globo = dibujar_panel(pantalla, RECT_TUTORIAL_TEXTO)
        for i, ancho in enumerate((12, 8, 4)):                       # piquito del globo hacia Don Salmón
            y = globo.top + 150 + i * 4
            pygame.draw.rect(pantalla, C["zocalo"], (globo.left - ancho, y, ancho + 4, 4))
        pygame.draw.rect(pantalla, C["panel"], (globo.left - 4, globo.top + 154, 8, 4))
        self._texto_de_don_salmon(pantalla, titulo, texto, globo)

        ultima = self.pagina == len(PAGINAS) - 1
        etiquetas = {"saltar": "Cerrar (Esc)" if self.desde_pausa else "Saltar (Esc)",
                     "atras": "< Atrás",
                     "siguiente": ("Volver" if self.desde_pausa else "¡A trabajar!") if ultima else "Siguiente >"}
        colores = {"saltar": C["leche"], "atras": C["leche"], "siguiente": C["dorado"]}
        for nombre, rect in BOTONES_TUTORIAL.items():
            activo = not (nombre == "atras" and self.pagina == 0)
            dibujar_boton(pantalla, rect, etiquetas[nombre], f["s"], colores[nombre],
                          resaltado=pygame.Rect(rect).collidepoint(mouse), activo=activo)
        texto_centrado(pantalla, f"{self.pagina + 1} / {len(PAGINAS)}", f["m"], C["texto"], (400, 588))
        texto_centrado(pantalla, "Flechas o Espacio", f["xs"], C["texto"], (400, 612))
