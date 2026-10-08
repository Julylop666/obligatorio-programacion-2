import os
import unittest

from ajustes import (DIA_ITEM, TIENDA, ESTACIONES_RECT, ARCHIVOS_SONIDO, RUTA_SONIDOS, ARCHIVO_MUSICA,
                     VOLUMEN_RELATIVO)
from estaciones import (EstacionBasura, EstacionSyrup, EstacionLeche, EstacionEspresso, ExhibidorMedialunas,
                        EstacionFrutilla, crear_estaciones)
from jugador import Jugador
from ventana import VentanaDia, momento_del_dia


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

        self.assertEqual(resultado, ("Ítem descartado.", "tacho", -12))
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

    def test_cada_accion_tiene_su_propio_sonido(self):
        """Leche, espresso, medialuna, topping y tacho ya no comparten el mismo sonido."""
        def nuevo(bandeja=(), taza=0):
            jugador = Jugador((240, 170, 100))
            jugador.capacidad_bandeja = 3
            jugador.bandeja = list(bandeja)
            jugador.taza = taza
            return jugador

        sonidos = [EstacionLeche().interactuar(nuevo())[1],
                   EstacionEspresso().interactuar(nuevo(taza=2))[1],
                   ExhibidorMedialunas().interactuar(nuevo())[1],
                   EstacionFrutilla().interactuar(nuevo(["medialuna"]))[1],
                   EstacionSyrup().interactuar(nuevo(["cafe"]))[1],
                   EstacionBasura().interactuar(nuevo(["cafe"]))[1]]
        self.assertEqual(sonidos, ["leche", "espresso", "medialuna", "topping", "topping", "tacho"])

    def test_todos_los_sonidos_declarados_existen_como_archivo(self):
        """Cada sonido de ajustes tiene su .wav (si falta: python generar_sonidos.py)."""
        for archivo in list(ARCHIVOS_SONIDO.values()) + [ARCHIVO_MUSICA]:
            self.assertTrue(os.path.exists(os.path.join(RUTA_SONIDOS, archivo)), archivo)
        self.assertTrue(set(VOLUMEN_RELATIVO) <= set(ARCHIVOS_SONIDO))

    def test_la_ventana_avanza_hacia_la_tarde_y_no_retrocede(self):
        """El cielo se acerca al avance del día y no vuelve atrás si el dinero baja."""
        ventana = VentanaDia()
        for _ in range(300):
            ventana.actualizar(0.05, 0.6)
        self.assertAlmostEqual(ventana.progreso, 0.6, places=2)
        for _ in range(300):
            ventana.actualizar(0.05, 0.2)          # el dinero bajó (tacho)
        self.assertAlmostEqual(ventana.progreso, 0.6, places=2)
        ventana.reiniciar()
        self.assertEqual(ventana.progreso, 0.0)

    def test_los_colores_del_cielo_cambian_de_manana_a_tarde(self):
        """El horizonte pasa de crema a dorado y el progreso fuera de rango no rompe nada."""
        manana, tarde = momento_del_dia(0.0), momento_del_dia(1.0)
        self.assertNotEqual(manana["horizonte"], tarde["horizonte"])
        self.assertEqual(momento_del_dia(-5), manana)
        self.assertEqual(momento_del_dia(7), tarde)


if __name__ == "__main__":
    unittest.main()