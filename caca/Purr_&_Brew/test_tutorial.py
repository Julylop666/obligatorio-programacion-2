"""Pruebas del tutorial de Don Salmón y de la pausa: música, sonidos, volumen, M/N en juego y brillo de la plata.

Se ejecutan sin ventana ni placa de sonido:  python -m unittest test_tutorial
"""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")        # sin ventana real
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")        # sin placa de sonido
import unittest

import pygame
from ajustes import (BOTON_PAUSA, BOTONES_PAUSA, BOTONES_TUTORIAL, RECT_PANEL_PAUSA, RECT_BARRA_VOLUMEN, JUGANDO,
                     TUTORIAL, SELECCION_GATO, ANCHO, ALTO, AVISOS_DESBLOQUEO, AVISO_TUTORIAL, VOLUMEN_INICIAL)
from main import Juego, cargar_fuente
from tutorial import Tutorial, PAGINAS
from estaciones import Mesa
from ajustes import COLORES_PASTEL as C


def clic(juego, rect):
    """Simula un clic izquierdo en el centro de un rectángulo."""
    pos = pygame.Rect(rect).center
    juego.manejar_evento(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=pos))


def tecla(juego, codigo):
    """Simula apretar una tecla."""
    juego.manejar_evento(pygame.event.Event(pygame.KEYDOWN, key=codigo))


class FalsoSonido:
    """Reemplaza a un Sound de pygame para contar cuántas veces suena."""

    def __init__(self):
        self.veces = 0

    def play(self):
        self.veces += 1

    def set_volume(self, volumen):
        self.volumen = volumen


class TutorialTest(unittest.TestCase):
    """El tutorial en sí: páginas y navegación."""

    def setUp(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        fuentes = {k: cargar_fuente(t) for k, t in (("xl", 60), ("l", 40), ("m", 30), ("s", 22), ("xs", 18))}
        self.tutorial = Tutorial(fuentes)

    def test_todas_las_paginas_se_dibujan_sin_errores(self):
        """Cada página (ilustración, globito y botones) se dibuja completa."""
        for i in range(len(PAGINAS)):
            self.tutorial.pagina = i
            self.tutorial.dibujar(self.pantalla, (0, 0))

    def test_el_tutorial_es_corto(self):
        """El juego es intuitivo: el tutorial tiene pocas páginas (como mucho 4)."""
        self.assertLessEqual(len(PAGINAS), 4)

    def test_el_tutorial_explica_lo_esencial(self):
        """Controles, orden del café, cobrar la plata y cómo volver a verlo."""
        textos = " ".join(texto for _, texto, _ in PAGINAS).lower()
        self.assertIn("w a s d", textos)
        self.assertIn("leche, vaporizador y espresso", textos)
        self.assertIn("juntala con e", textos)
        self.assertIn("t en la pausa", textos)

    def test_navegacion_adelante_y_atras(self):
        """Siguiente avanza, anterior retrocede (sin pasarse del principio) y la última página termina."""
        self.assertEqual(self.tutorial.pagina, 0)
        self.tutorial.anterior()
        self.assertEqual(self.tutorial.pagina, 0)
        self.assertFalse(self.tutorial.siguiente())
        self.assertEqual(self.tutorial.pagina, 1)
        for _ in range(len(PAGINAS) - 2):
            self.assertFalse(self.tutorial.siguiente())
        self.assertEqual(self.tutorial.pagina, len(PAGINAS) - 1)
        self.assertTrue(self.tutorial.siguiente())

    def test_los_botones_responden_al_clic(self):
        """Cada botón devuelve su nombre y un clic en otro lado no devuelve nada."""
        for nombre, rect in BOTONES_TUTORIAL.items():
            self.assertEqual(self.tutorial.clic(pygame.Rect(rect).center), nombre)
        self.assertIsNone(self.tutorial.clic((400, 100)))


class JuegoConTutorialYPausaTest(unittest.TestCase):
    """El flujo completo dentro de Juego: tutorial al empezar y botones del menú de pausa."""

    def setUp(self):
        self.juego = Juego()
        self.juego.estado = SELECCION_GATO

    def empezar_a_jugar(self):
        """Elige gato y salta el tutorial con Esc: queda jugando."""
        tecla(self.juego, pygame.K_SPACE)
        tecla(self.juego, pygame.K_ESCAPE)

    def test_la_primera_vez_aparece_el_tutorial_despues_de_elegir_gato(self):
        """Elegir gato abre el tutorial; saltarlo arranca el día 1."""
        tecla(self.juego, pygame.K_SPACE)
        self.assertEqual(self.juego.estado, TUTORIAL)
        tecla(self.juego, pygame.K_ESCAPE)
        self.assertEqual(self.juego.estado, JUGANDO)
        self.assertEqual(self.juego.dia, 1)

    def test_el_tutorial_se_puede_recorrer_entero_con_espacio(self):
        """Apretar Espacio en cada página termina el tutorial y empieza el día."""
        tecla(self.juego, pygame.K_SPACE)
        for _ in range(len(PAGINAS)):
            self.assertEqual(self.juego.estado, TUTORIAL)
            tecla(self.juego, pygame.K_SPACE)
        self.assertEqual(self.juego.estado, JUGANDO)

    def test_el_tutorial_se_puede_recorrer_con_clics(self):
        """El botón Siguiente (clic) avanza y Atrás retrocede."""
        tecla(self.juego, pygame.K_SPACE)
        clic(self.juego, BOTONES_TUTORIAL["siguiente"])
        clic(self.juego, BOTONES_TUTORIAL["siguiente"])
        self.assertEqual(self.juego.tutorial.pagina, 2)
        clic(self.juego, BOTONES_TUTORIAL["atras"])
        self.assertEqual(self.juego.tutorial.pagina, 1)
        clic(self.juego, BOTONES_TUTORIAL["saltar"])
        self.assertEqual(self.juego.estado, JUGANDO)

    def test_al_reiniciar_no_se_repite_el_tutorial(self):
        """Después de verlo una vez, elegir gato de nuevo va directo al día 1."""
        self.empezar_a_jugar()
        self.juego.nueva_partida()
        self.juego.estado = SELECCION_GATO
        tecla(self.juego, pygame.K_SPACE)
        self.assertEqual(self.juego.estado, JUGANDO)

    def test_boton_de_pausa_del_hud_pausa_y_reanuda(self):
        """Clic en el botón || pausa el juego y otro clic lo reanuda."""
        self.empezar_a_jugar()
        clic(self.juego, BOTON_PAUSA)
        self.assertTrue(self.juego.pausado)
        clic(self.juego, BOTON_PAUSA)
        self.assertFalse(self.juego.pausado)

    def test_boton_musica_apaga_y_prende(self):
        """El botón de música cambia el interruptor y la música queda pausada o sonando."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        clic(self.juego, BOTONES_PAUSA["musica"])
        self.assertFalse(self.juego.musica_activada)
        clic(self.juego, BOTONES_PAUSA["musica"])
        self.assertTrue(self.juego.musica_activada)
        self.assertTrue(self.juego.pausado)                  # tocar un botón no reanuda el juego

    def test_al_reanudar_con_la_musica_apagada_sigue_apagada(self):
        """Si apagaste la música en la pausa, continuar no la vuelve a prender."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        tecla(self.juego, pygame.K_m)
        espiadas = []
        original = pygame.mixer.music.unpause
        pygame.mixer.music.unpause = lambda: espiadas.append(1)
        try:
            tecla(self.juego, pygame.K_p)
        finally:
            pygame.mixer.music.unpause = original
        self.assertFalse(self.juego.pausado)
        self.assertEqual(espiadas, [])

    def test_boton_sonidos_silencia_los_efectos(self):
        """Con los sonidos apagados reproducir() no suena; al prenderlos vuelve a sonar."""
        falso = FalsoSonido()
        self.juego.sonidos["caja"] = falso
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        clic(self.juego, BOTONES_PAUSA["efectos"])
        self.assertFalse(self.juego.efectos_activados)
        self.juego.reproducir("caja")
        self.assertEqual(falso.veces, 0)
        tecla(self.juego, pygame.K_n)
        self.assertTrue(self.juego.efectos_activados)
        self.juego.reproducir("caja")
        self.assertEqual(falso.veces, 1)

    def test_tutorial_desde_la_pausa_vuelve_a_la_pausa(self):
        """El botón Tutorial abre el tutorial y al cerrarlo reaparece el menú de pausa."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        clic(self.juego, BOTONES_PAUSA["tutorial"])
        self.assertEqual(self.juego.estado, TUTORIAL)
        tecla(self.juego, pygame.K_ESCAPE)
        self.assertEqual(self.juego.estado, JUGANDO)
        self.assertTrue(self.juego.pausado)

    def test_boton_continuar_y_clic_afuera_reanudan(self):
        """Continuar y un clic fuera del menú reanudan; un clic en un hueco del menú no hace nada."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        clic(self.juego, BOTONES_PAUSA["continuar"])
        self.assertFalse(self.juego.pausado)
        tecla(self.juego, pygame.K_p)
        centro_hueco = (pygame.Rect(RECT_PANEL_PAUSA).centerx, pygame.Rect(RECT_PANEL_PAUSA).top + 205)
        self.juego.manejar_evento(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=centro_hueco))
        self.assertTrue(self.juego.pausado)
        self.juego.manejar_evento(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(20, 600)))
        self.assertFalse(self.juego.pausado)

    def test_el_menu_de_pausa_y_el_tutorial_se_dibujan(self):
        """Dibujar el juego pausado y el tutorial no da errores, con el audio prendido o apagado."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        self.juego.dibujar()
        tecla(self.juego, pygame.K_m)
        tecla(self.juego, pygame.K_n)
        self.juego.dibujar()
        tecla(self.juego, pygame.K_t)
        self.juego.dibujar()

    def test_m_y_n_silencian_sin_pausar(self):
        """Durante el juego, M y N apagan y prenden música y sonidos sin pausar, y avisan con un cartelito."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_m)
        self.assertFalse(self.juego.musica_activada)
        self.assertFalse(self.juego.pausado)
        self.assertIn("apagada", self.juego.aviso_texto)
        tecla(self.juego, pygame.K_m)
        self.assertTrue(self.juego.musica_activada)
        tecla(self.juego, pygame.K_n)
        self.assertFalse(self.juego.efectos_activados)
        self.assertFalse(self.juego.pausado)
        tecla(self.juego, pygame.K_n)
        self.assertTrue(self.juego.efectos_activados)

    def test_volumen_con_teclas_y_botones(self):
        """Flechas, + y - y los botones de la pausa suben y bajan el volumen sin salirse de 0 a 1."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        self.assertAlmostEqual(self.juego.volumen, VOLUMEN_INICIAL)
        tecla(self.juego, pygame.K_LEFT)
        self.assertAlmostEqual(self.juego.volumen, VOLUMEN_INICIAL - 0.1)
        clic(self.juego, BOTONES_PAUSA["vol_mas"])
        clic(self.juego, BOTONES_PAUSA["vol_mas"])
        self.assertAlmostEqual(self.juego.volumen, VOLUMEN_INICIAL + 0.1)
        for _ in range(15):
            tecla(self.juego, pygame.K_RIGHT)
        self.assertAlmostEqual(self.juego.volumen, 1.0)
        for _ in range(15):
            clic(self.juego, BOTONES_PAUSA["vol_menos"])
        self.assertAlmostEqual(self.juego.volumen, 0.0)
        self.assertTrue(self.juego.pausado)                  # tocar el volumen no reanuda el juego

    def test_clic_en_la_barra_de_volumen_elige_el_tramo(self):
        """Un clic en el tramo 3 de la barra deja el volumen en 30%; en el último, al máximo."""
        self.empezar_a_jugar()
        tecla(self.juego, pygame.K_p)
        barra = pygame.Rect(RECT_BARRA_VOLUMEN)
        ancho = barra.width / 10
        clic(self.juego, (barra.left + ancho * 2.5, barra.centery, 1, 1))
        self.assertAlmostEqual(self.juego.volumen, 0.3)
        clic(self.juego, (barra.right - 3, barra.centery, 1, 1))
        self.assertAlmostEqual(self.juego.volumen, 1.0)

    def test_el_volumen_se_aplica_a_los_sonidos(self):
        """Cambiar el volumen se lo pasa a cada efecto (con su ajuste relativo) y a la música."""
        falso = FalsoSonido()
        self.juego.sonidos["caja"] = falso
        self.juego.cambiar_volumen(0.5)
        self.assertGreater(falso.volumen, 0)
        self.juego.cambiar_volumen(1.0)
        mayor = falso.volumen
        self.juego.cambiar_volumen(0.2)
        self.assertLess(falso.volumen, mayor)

    def test_los_carteles_de_novedad_nombran_el_tutorial(self):
        """Los días 2, 3 y 4 el cartel de novedad recuerda que el tutorial está con T en la pausa."""
        self.assertEqual(sorted(AVISOS_DESBLOQUEO), [2, 3, 4])
        for aviso in AVISOS_DESBLOQUEO.values():
            self.assertTrue(aviso.endswith(AVISO_TUTORIAL))
        self.assertIn("T en la pausa", AVISO_TUTORIAL)

    def test_la_mesa_con_plata_brilla(self):
        """Una mesa con plata sin juntar dibuja el aro y los brillitos: se ve distinta que sin plata."""
        pantalla = pygame.Surface((200, 200))
        fuente = pygame.font.Font(None, 20)
        mesa = Mesa((100, 100))
        pantalla.fill((248, 228, 204))
        mesa.dibujar(pantalla, fuente)
        vacia = pygame.image.tobytes(pantalla, "RGB")
        mesa.dinero = 15
        pantalla.fill((248, 228, 204))
        mesa.dibujar(pantalla, fuente)
        self.assertNotEqual(vacia, pygame.image.tobytes(pantalla, "RGB"))
        self.assertTrue(any(pantalla.get_at((x, y))[:3] == C["brillo_dorado"]
                            for x in range(200) for y in range(200)))


if __name__ == "__main__":
    unittest.main()
