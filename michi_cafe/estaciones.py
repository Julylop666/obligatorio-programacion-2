"""estaciones.py - Estaciones de la barra y mesas del salón (en pixel art).

Todas las estaciones comparten el método interactuar(jugador), que devuelve
una tupla (mensaje, sonido, dinero_ganado). Así main.py las trata igual.
"""
import pygame
from ajustes import (COLORES_PASTEL as C, ESTACIONES_RECT, DIA_ESTACION, CENTROS_MESAS, TAM_MESA,
                     DESPLAZAMIENTO_ASIENTO, TAZA_VACIA, TAZA_LECHE, TAZA_CALIENTE, ESPERANDO,
                     PX_MUNDO, PX_GATO, PRECIOS)
from dibujo import dibujar_item, pixelar, oscurecer

# ---------------------------------------------------------------- íconos pixel art de las estaciones
_ICONO_LECHE = (
    "..OOOO..",
    ".OBBBBO.",
    "OOOOOOOO",
    "OWWWWWWO",
    "OWBBBBWO",
    "OWBWWBWO",
    "OWBBBBWO",
    "OWWWWWWO",
    "OWWWWWWO",
    "OWWWWWWO",
    "OOOOOOOO",
)
_PAL_LECHE = {"O": C["contorno"], "W": C["leche"], "B": C["azul_medio"]}

_ICONO_VAPOR = (
    "...W..W...",
    "..W..W....",
    "...W..W...",
    ".OOOOOOO..",
    "OGHHGGGGO.",
    "OGHGGGGGOO",
    "OGGGGGGGOO",
    "OGGGGGGGOO",
    "OGGGGGGGO.",
    ".OGGGGGO..",
    "..OOOOO...",
)
_PAL_VAPOR = {"O": C["contorno"], "G": C["metal"], "H": C["vapor_claro"], "W": C["blanco"]}

_ICONO_ESPRESSO = (
    "..OOOOOOOOOO..",
    ".OGGGGGGGGGGO.",
    ".OGPGGGGGJGGO.",
    ".OGGGGGGGGGGO.",
    ".OGGGOOOOGGGO.",
    ".OGGGGKKGGGGO.",
    ".OOOOOKKOOOOO.",
    ".....OWWO.....",
    ".OOOOOOOOOOOO.",
)
_PAL_ESPRESSO = {"O": C["contorno"], "G": C["metal_espresso"], "P": C["rosa_boton"], "J": C["luz_amarilla"],
                 "K": C["cafe"], "W": C["leche"]}

_ICONO_FRASCO = (
    "..OOOOO..",
    ".OLLLLLO.",
    "OOOOOOOOO",
    "OWWWWWWWO",
    "OWCWWCWWO",
    "OWWCWWCWO",
    "OWCWCWWWO",
    "OWWWWCWWO",
    "OWCWWWCWO",
    "OWWWWWWWO",
    "OOOOOOOOO",
)
_PAL_FRUTILLA = {"O": C["contorno"], "L": C["frutilla_tapa"], "W": C["frutilla_crema"], "C": C["frutilla_pintitas"]}
_PAL_DULCE = {"O": C["contorno"], "L": C["rosa_claro"], "W": C["dulce_base"], "C": C["dulce_pintitas"]}
_PAL_SYRUP = {"O": C["contorno"], "L": C["vainilla_tapa"], "W": C["vainilla_crema"], "C": C["vainilla_pintitas"]}

_PLATO = (
    "..OOOOOOOOOOOOOO..",
    ".OWWWWWWWWWWWWWWO.",
    "..OOOOOOOOOOOOOO..",
)

_ICONO_BASURA = (
    "..OOOOO..",
    ".OWWWWW.O",
    ".OWWWWWO.",
    ".OWWWWWO.",
    ".OWWWWWO.",
    ".O....OO.",
    "..OOOOO..",
)

_CANDADO = (
    "..OOO..",
    ".O...O.",
    ".O...O.",
    "OOOOOOO",
    "OYYYYYO",
    "OYYOYYO",
    "OYYYYYO",
    "OOOOOOO",
)


def _base_estacion(ancho, alto, bloqueada=False):
    """Arma el mueble pixel art de una estación (mesada + frente de madera). Devuelve una Surface."""
    px = PX_MUNDO
    chica = pygame.Surface((ancho // px, alto // px), pygame.SRCALPHA)
    madera, tapa = C["barra"], C["barra_tapa"]
    if bloqueada:
        madera, tapa = C["bloqueada_madera"], C["bloqueada_tapa"]
    w, h = chica.get_size()
    oscuro = oscurecer(madera, 0.7)
    pygame.draw.rect(chica, C["contorno"], (0, 7, w, 5))                 # contorno de la tapa
    pygame.draw.rect(chica, tapa, (1, 8, w - 2, 3))
    pygame.draw.line(chica, C["blanco"], (2, 8), (w - 3, 8))         # brillo de la tapa
    pygame.draw.rect(chica, C["contorno"], (0, 12, w, h - 12))           # contorno del frente
    pygame.draw.rect(chica, madera, (1, 12, w - 2, h - 13))
    for x in range(7, w - 2, 8):                                          # tablitas del frente
        pygame.draw.line(chica, oscuro, (x, 13), (x, h - 2))
    return pygame.transform.scale(chica, (ancho, alto))


class Estacion:
    """Estación genérica de la barra. Las hijas implementan dibujar_icono e interactuar."""

    def __init__(self, clave, nombre):
        """Crea la estación en la posición definida en ajustes.ESTACIONES_RECT."""
        self.clave = clave
        self.nombre = nombre
        self.rect = pygame.Rect(ESTACIONES_RECT[clave])
        self.dia_desbloqueo = DIA_ESTACION.get(clave, 1)
        self.activa = True                       # False mientras el día no la desbloquea

    def dibujar_icono(self, pantalla):
        """Dibuja el ícono propio de la estación (lo redefine cada clase hija)."""

    def punto_apoyo(self):
        """Devuelve el punto de la mesada donde se apoya el ícono."""
        return self.rect.centerx, self.rect.top + 42

    def dibujar_grilla(self, pantalla, grilla, paleta):
        """Dibuja un ícono (grilla de texto) apoyado en la mesada, centrado."""
        sprite = pixelar(grilla, paleta, PX_GATO)
        pantalla.blit(sprite, sprite.get_rect(midbottom=self.punto_apoyo()))

    def dibujar(self, pantalla, fuente, resaltada=False):
        """Dibuja el mueble, su ícono, su nombre y un borde blanco si está resaltada.

        Si todavía no está desbloqueada se ve gris, con un candado y el día en que se abre.
        """
        pantalla.blit(_base_estacion(self.rect.width, self.rect.height, not self.activa), self.rect)
        if self.activa:
            self.dibujar_icono(pantalla)
            etiqueta, color = self.nombre, C["texto_claro"]
        else:
            candado = pixelar(_CANDADO, {"O": C["contorno"], "Y": C["dorado"]}, PX_GATO)
            pantalla.blit(candado, candado.get_rect(midbottom=self.punto_apoyo()))
            etiqueta, color = f"Día {self.dia_desbloqueo}", C["contorno"]
        texto = fuente.render(etiqueta, False, color)
        pantalla.blit(texto, texto.get_rect(center=(self.rect.centerx, self.rect.bottom - 14)))
        if resaltada:
            pygame.draw.rect(pantalla, C["resaltado"], self.rect.inflate(8, 8), 4)

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
        self.dibujar_grilla(pantalla, _ICONO_LECHE, _PAL_LECHE)

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
        self.dibujar_grilla(pantalla, _ICONO_VAPOR, _PAL_VAPOR)

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
        self.dibujar_grilla(pantalla, _ICONO_ESPRESSO, _PAL_ESPRESSO)

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
        """Dibuja un platito con dos medialunas."""
        self.dibujar_grilla(pantalla, _PLATO, {"O": C["contorno"], "W": C["leche"]})
        x, y = self.punto_apoyo()
        dibujar_item(pantalla, "medialuna", (x - 12, y - 4), base=True, px=PX_GATO - 1)
        dibujar_item(pantalla, "medialuna", (x + 12, y - 4), base=True, px=PX_GATO - 1)

    def interactuar(self, jugador):
        """Agrega una medialuna simple a la bandeja si hay lugar."""
        if jugador.agregar_item("medialuna"):
            return "Medialuna calentita en la bandeja.", "miau", 0
        return "La bandeja está llena.", None, 0


class EstacionTopping(Estacion):
    """Estación que le agrega un topping a una medialuna simple que lleve el jugador."""

    def __init__(self, clave, nombre, item_resultado, paleta, mensaje):
        """Crea la estación: item_resultado es el ítem que se obtiene (ej. 'medialuna_frutilla')."""
        super().__init__(clave, nombre)
        self.item_resultado = item_resultado
        self.paleta = paleta
        self.mensaje = mensaje

    def dibujar_icono(self, pantalla):
        """Dibuja el frasquito del topping."""
        self.dibujar_grilla(pantalla, _ICONO_FRASCO, self.paleta)

    def interactuar(self, jugador):
        """Convierte una medialuna simple de la bandeja en una con topping."""
        if "medialuna" not in jugador.bandeja:
            return "Primero llevá una medialuna simple en la bandeja.", None, 0
        jugador.bandeja[jugador.bandeja.index("medialuna")] = self.item_resultado
        return self.mensaje, "miau", 0


class EstacionFrutilla(EstacionTopping):
    """Frasco de cobertura de frutilla (se desbloquea el día 2)."""

    def __init__(self):
        """Crea la estación de cobertura de frutilla."""
        super().__init__("frutilla", "Frutilla", "medialuna_frutilla", _PAL_FRUTILLA,
                         "¡Medialuna con frutilla!")


class EstacionDulce(EstacionTopping):
    """Frasco de dulce de leche (se desbloquea el día 3)."""

    def __init__(self):
        """Crea la estación de dulce de leche."""
        super().__init__("dulce", "Dulce de leche", "medialuna_dulce", _PAL_DULCE,
                         "¡Medialuna con dulce de leche!")


class EstacionSyrup(Estacion):
    """Jarabe de vainilla que se agrega a un café."""

    def __init__(self):
        """Crea la estación de vainilla."""
        super().__init__("syrup", "Vainilla")

    def dibujar_icono(self, pantalla):
        """Dibuja un frasco de jarabe de vainilla."""
        self.dibujar_grilla(pantalla, _ICONO_FRASCO, _PAL_SYRUP)

    def interactuar(self, jugador):
        """Convierte un café simple en uno con vainilla si hay uno en la bandeja."""
        if "cafe" not in jugador.bandeja:
            return "Primero llevá un café simple en la bandeja.", None, 0
        jugador.bandeja[jugador.bandeja.index("cafe")] = "cafe_syrup"
        return "¡Café con vainilla!", "miau", 0


class EstacionBasura(Estacion):
    """Tacho que descarta un ítem de la bandeja."""

    def __init__(self):
        """Crea el tacho de basura."""
        super().__init__("basura", "Tacho")

    def dibujar_icono(self, pantalla):
        """Dibuja un tacho con una tapa y una manija."""
        sprite = pixelar(_ICONO_BASURA, {"O": C["contorno"], "W": C["metal"], "P": C["metal_oscuro"]}, PX_GATO)
        pantalla.blit(sprite, sprite.get_rect(midbottom=self.punto_apoyo()))

    def interactuar(self, jugador):
        """Descarta un único ítem de la bandeja y pierde su valor."""
        if not jugador.bandeja:
            return "La bandeja ya está vacía.", None, 0
        item = jugador.bandeja.pop()
        costo = PRECIOS.get(item, 0)
        return "Ítem descartado.", "miau", -costo


# ---------------------------------------------------------------- mesas
_BILLETE = (
    "OOOOOOOO",
    "OGGGGGGO",
    "OGGOOGGO",
    "OGGGGGGO",
    "OOOOOOOO",
)


def _sprite_mesa():
    """Arma (una vez) la mesa pixel art con mantel. Devuelve una Surface de TAM_MESA de ancho."""
    px = PX_MUNDO
    w, h = TAM_MESA // px, (TAM_MESA - 8) // px
    chica = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(chica, C["contorno"], (0, 0, w, h))
    pygame.draw.ellipse(chica, C["mantel"], (1, 1, w - 2, h - 2))
    pygame.draw.ellipse(chica, C["mesa"], (4, 3, w - 8, h - 6))
    pygame.draw.ellipse(chica, C["blanco"], (6, 4, 5, 2))            # brillo
    return pygame.transform.scale(chica, (w * px, h * px))


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
        sprite = _sprite_mesa()
        zona = sprite.get_rect(center=self.rect.center)
        sombra = zona.inflate(0, -20).move(0, 18)
        pygame.draw.ellipse(pantalla, C["sombra"], sombra)
        pantalla.blit(sprite, zona)
        if self.dinero > 0:
            billete = pixelar(_BILLETE, {"O": C["contorno"], "G": C["billete"]}, PX_GATO)
            for i in range(2):
                pantalla.blit(billete, billete.get_rect(center=(self.rect.centerx - 6 + i * 10,
                                                                self.rect.centery - 8 - i * 4)))
            pantalla.blit(fuente.render(f"${self.dinero}", False, C["texto"]),
                          (self.rect.centerx - 14, self.rect.centery + 2))
        if resaltada:
            pygame.draw.ellipse(pantalla, C["resaltado"], zona.inflate(8, 8), 4)

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


def crear_estaciones(dia=1):
    """Devuelve la lista con las 8 estaciones de la barra.

    Las que todavía no se desbloquearon en 'dia' quedan con activa = False.
    """
    estaciones = [EstacionLeche(), EstacionVapor(), EstacionEspresso(), ExhibidorMedialunas(),
                  EstacionFrutilla(), EstacionDulce(), EstacionSyrup(), EstacionBasura()]
    for estacion in estaciones:
        estacion.activa = dia >= estacion.dia_desbloqueo
    return estaciones


def crear_mesas():
    """Devuelve la lista de mesas del salón según ajustes.CENTROS_MESAS."""
    return [Mesa(centro) for centro in CENTROS_MESAS]