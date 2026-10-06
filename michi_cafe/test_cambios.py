import unittest

from ajustes import DIA_ITEM, TIENDA, ESTACIONES_RECT
from estaciones import EstacionBasura, EstacionSyrup, crear_estaciones
from jugador import Jugador


class CambiosJuegoTest(unittest.TestCase):
    def test_tacho_descarta_un_item_de_la_bandeja(self):
        jugador = Jugador((240, 170, 100))
        jugador.bandeja = ["cafe", "medialuna"]

        resultado = EstacionBasura().interactuar(jugador)

        self.assertEqual(resultado[0], "Ítem descartado.")
        self.assertEqual(jugador.bandeja, ["cafe"])

    def test_syrup_desbloquea_en_el_dia_3(self):
        estaciones = crear_estaciones(2)
        self.assertNotIn("syrup", [estacion.clave for estacion in estaciones if estacion.activa])

        estaciones_dia_3 = crear_estaciones(3)
        self.assertIn("syrup", [estacion.clave for estacion in estaciones_dia_3 if estacion.activa])

    def test_syrup_transforma_un_cafe_en_cafe_con_vainilla(self):
        jugador = Jugador((240, 170, 100))
        jugador.bandeja = ["cafe"]

        resultado = EstacionSyrup().interactuar(jugador)

        self.assertEqual(resultado[0], "¡Café con vainilla!")
        self.assertEqual(jugador.bandeja, ["cafe_syrup"])

    def test_syrup_disponible_desde_el_dia_3(self):
        self.assertEqual(DIA_ITEM["cafe_syrup"], 3)
        self.assertEqual(TIENDA["zapatillas_1"]["slot"], "calzado")

    def test_basura_esta_a_la_derecha_y_frente_al_salon(self):
        self.assertEqual(ESTACIONES_RECT["basura"], (830, 500, 104, 72))

    def test_frutilla_reemplaza_la_cobertura_de_chispas(self):
        self.assertIn("medialuna_frutilla", DIA_ITEM)
        self.assertEqual(DIA_ITEM["medialuna_frutilla"], 2)

    def test_frutilla_cubre_el_centro_de_la_medialuna(self):
        sprite = __import__("dibujo", fromlist=["ITEMS_PIXEL"]).ITEMS_PIXEL["medialuna_frutilla"]
        self.assertEqual(sprite[2], ".OYYYYYYYYO.")
        self.assertEqual(sprite[3], "OYYYYRRRYYYYO")


if __name__ == "__main__":
    unittest.main()
