# Purr & Brew 2D: resumen para la entrega

Texto listo para pegar en el informe (Programación 2, Facultad de Diseño, Universidad ORT Uruguay).

## Descripción
Purr & Brew 2D es un juego cozy de cafetería en pixel art hecho con Python y Pygame. El jugador es un
Licenciado en Diseño recién recibido que, convertido en gato barista, reemplaza a Don Salmón durante 5 días.
Cada día hay que juntar una meta de dinero atendiendo a los vecinos: se preparan cafés con leche y medialunas
(con frutilla, dulce de leche y vainilla que se desbloquean con los días), se entregan en la mesa y se junta la
plata que dejan. Entre día y día se compra ropa que mejora la velocidad, la bandeja y las ganancias. Se pierde si
4 vecinos quedan sin mesa a la vez.

## Experiencia de usuario
- **Tutorial breve de Don Salmón (3 páginas, con dibujos):** se muestra la primera vez, después de elegir el
  gato. Explica controles, recetas y cómo atender y cobrar. Se puede saltar con Esc y volver a ver desde la
  pausa (tecla T). Los carteles de novedad de los días 2, 3 y 4 recuerdan dónde encontrarlo.
- **Pista visual para cobrar:** las mesas con plata sin juntar tienen un aro dorado que late y brillitos que
  titilan, porque olvidarse de cobrar es lo que más puede complicar a un jugador nuevo.
- **Audio a medida:** M y N silencian música y sonidos en cualquier momento (también jugando), y la pausa tiene
  un control de volumen de 10 tramos.
- **Sin presión:** no hay temporizadores ni clientes enojados; la ventana de la pared va de la mañana a la tarde
  a medida que se junta la meta.

## Decisiones técnicas
- Todo el arte (gatos, ítems, muebles, escenas) se dibuja por código a partir de grillas de texto, sin archivos
  de imagen.
- Los sonidos y la música se sintetizan desde cero con `generar_sonidos.py`.
- Tipografía Jersey 15 (SIL Open Font License 1.1).
- Constantes y balance en `ajustes.py`; pruebas automáticas con `unittest` (`test_cambios.py` y `test_tutorial.py`).

## Uso de Inteligencia Artificial Generativa
Herramienta: Claude (Anthropic). Se usó para generar el código a partir de la especificación del juego
(concepto, historia, mecánicas, arquitectura de módulos y reglas) y de los pedidos de cambio posteriores (pixel
art, toppings, pausa, tutorial corto, control de volumen, teclas M y N, brillo en las mesas con plata).
