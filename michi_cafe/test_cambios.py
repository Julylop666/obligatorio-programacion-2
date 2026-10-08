import unittest

from ajustes import DIA_ITEM, TIENDA, ESTACIONES_RECT
from estaciones import EstacionBasura, EstacionSyrup, crear_estaciones
from jugador import Jugador


class CambiosJuegoTest(unittest.TestCase):
    """Pruebas de las estaciones nuevas (tacho, vainilla, frutilla) y de la ropa."""

    def test_tacho_descarta_un_item_de_la_bandeja(self):
        """El tacho saca el último ítem de la bandeja."""
        jugador = Jugador((240, 170, 100))
        jugador.bandeja = ["cafe", "medialuna"]

        resultado = EstacionBasura().interactuar(jugador)

        self.assertEqual(resultado[0], "Ítem descartado.")
        self.assertEqual(jugador.bandeja, ["cafe"])

    def test_tacho_descuenta_el_precio_del_item(self):
        """Descartar un café descuenta su precio ($12)."""
        jugador = Jugador((240, 170, 100))
        jugador.bandeja = ["cafe"]

        resultado = EstacionBasura().interactuar(jugador)

        self.assertEqual(resultado, ("Ítem descartado.", "miau", -12))
        self.assertEqual(jugador.bandeja, [])

    def test_syrup_desbloquea_en_el_dia_3(self):
        """La estación de vainilla recién está activa desde el día 3."""
        estaciones = crear_estaciones(2)
        self.assertNotIn("syrup", [estacion.clave for estacion in estaciones if estacion.activa])

        estaciones_dia_3 = crear_estaciones(3)
        self.assertIn("syrup", [estacion.clave for estacion in estaciones_dia_3 if estacion.activa])

    def test_syrup_transforma_un_cafe_en_cafe_con_vainilla(self):
        """La vainilla convierte un café simple en café con vainilla."""
        jugador = Jugador((240, 170, 100))
        jugador.bandeja = ["cafe"]

        resultado = EstacionSyrup().interactuar(jugador)

        self.assertEqual(resultado[0], "¡Café con vainilla!")
        self.assertEqual(jugador.bandeja, ["cafe_syrup"])

    def test_syrup_disponible_desde_el_dia_3(self):
        """El café con vainilla se pide desde el día 3 y los championes van en el slot calzado."""
        self.assertEqual(DIA_ITEM["cafe_syrup"], 3)
        self.assertEqual(TIENDA["championes_1"]["slot"], "calzado")

    def test_basura_esta_a_la_derecha_y_frente_al_salon(self):
        """El tacho está en la posición definida en ajustes."""
        self.assertEqual(ESTACIONES_RECT["basura"], (830, 500, 104, 72))

    def test_frutilla_reemplaza_la_cobertura_de_chispas(self):
        """La medialuna con frutilla existe y se desbloquea el día 2."""
        self.assertIn("medialuna_frutilla", DIA_ITEM)
        self.assertEqual(DIA_ITEM["medialuna_frutilla"], 2)

    def test_frutilla_cubre_el_centro_de_la_medialuna(self):
        """El sprite de frutilla tiene la cobertura en el centro de la medialuna."""
        sprite = __import__("dibujo", fromlist=["ITEMS_PIXEL"]).ITEMS_PIXEL["medialuna_frutilla"]
        self.assertEqual(sprite[2], ".OYRDRRDRYO.")
        self.assertEqual(sprite[3], "OYRO.OO.ORYO")


if __name__ == "__main__":
    unittest.main()