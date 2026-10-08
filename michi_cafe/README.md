# Michi Café 2D

Juego cozy de cafetería en **pixel art**, hecho con Python y Pygame para Programación 2 (Facultad de Diseño, Universidad ORT Uruguay).
Sos un Licenciado en Diseño recién recibido que, convertido en gato barista, reemplaza a Don Salmón durante 5 días en su cafetería.

**Repositorio en GitHub:** https://github.com/Julylop666/obligatorio-programacion-2

## Cómo se juega

**Objetivo:** juntar la meta de dinero de cada día (Día 1: $50, Día 2: $120, Día 3: $220, Día 4: $350, Día 5: $500) y sobrevivir los 5 días.
Entre día y día podés comprar ropa en el ropero de Don Salmón para trabajar mejor.

**Cómo se gana:** completar el Día 5.
**Cómo se pierde:** si 4 vecinos quedan sin mesa a la vez, el local se desborda. Ojo: una mesa no se libera hasta que juntás el dinero que dejó el cliente.
En la pantalla de derrota o victoria, apretá **R** para volver a jugar sin cerrar la ventana (vuelve a la portada). También podés reiniciar con **R** desde el menú de pausa.
No hay temporizadores ni clientes enojados: los vecinos esperan con paciencia.

**Preparar un café con leche:** Leche -> Vaporizador -> Espresso. Queda en la bandeja que llevás en la mano.
**Medialunas:** se sacan del exhibidor y quedan en la bandeja.
**Estaciones que se desbloquean (las bloqueadas se ven grises con un candado y el día en que se abren):**
- **Día 2:** los vecinos pueden pedir medialuna con **frutilla**. Llevá una medialuna simple a la estación *Frutilla*.
- **Día 3:** también piden medialuna con **dulce de leche** (estación *Dulce de leche*).
- **Día 4:** también piden **café con vainilla** (llevá un café simple a la estación *Vainilla*).

**Tacho:** desde el Día 1 podés tirar el último ítem de la bandeja si te equivocaste, pero se te descuenta lo que valía.

**Paso del tiempo:** la ventana de la pared va de la mañana a la tarde a medida que juntás la meta del día (arranca de mañana cada día).

Cada pedido aparece en un globito sobre el cliente. Entregalo en su mesa y después juntá el dinero que deja.

| Ítem | Precio |
|---|---|
| Medialuna | $8 |
| Medialuna con frutilla / con dulce de leche | $11 |
| Café con leche | $12 |
| Café con vainilla | $14 |

### Controles

| Tecla | Acción |
|---|---|
| W A S D / Flechas | Moverse en 8 direcciones |
| E / Espacio | Interactuar (estaciones, mesas, cobrar) y avanzar menús |
| P / Esc / botón `\|\|` (clic) | Pausar y reanudar |
| 1 - 5 | Comprar prendas en la tienda |
| R | Volver a jugar (pantallas de derrota y victoria) |

### Ropa de la tienda
- **Delantal gastronómico:** más dinero por pedido (+20%).
- **Cofia / sombrero de chef:** la bandeja carga 2 o 3 ítems.
- **Championes antideslizantes / championes de cocina:** más velocidad (+15% / +30%).
- **Desbloqueos:** los championes de cocina están disponibles desde la tienda del Día 2; el sombrero de chef, desde la del Día 3. Cada prenda avanzada requiere comprar primero su versión anterior.

## Instalación y ejecución

Requiere Python 3.9 o superior.

```bash
pip install -r requirements.txt
python main.py
```

Es la única biblioteca externa. Ejecutá siempre `main.py` desde la carpeta del juego (o con la carpeta completa, con `sonidos/` y `fuentes/` al lado).

### Si no se escucha el sonido
Al iniciar, el juego imprime en la consola `Audio iniciado: (...)` si pudo abrir el audio, o un `Aviso:` con el motivo si algo falló.
Revisá que (1) la carpeta `sonidos/` esté junto a `main.py`, (2) el volumen de la compu y del mezclador de Windows (pygame / python) no esté silenciado, (3) tengas la última versión de pygame (`pip install --upgrade pygame`).
En el menú de pausa también aparece si el sonido está activado.

## Qué hay en cada archivo

| Archivo | Contenido |
|---|---|
| `main.py` | Bucle principal, máquina de estados (clase `Juego`), pausa, pantallas y HUD |
| `ajustes.py` | Todas las constantes: colores (incluidos los del pixel art), tamaños, velocidades, niveles, precios, tienda, desbloqueos y textos de la historia |
| `ventana.py` | La ventana del salón: el cielo pasa de la mañana a la tarde a medida que cumplís la meta del día |
| `jugador.py` | Clase `Jugador` (movimiento animado, bandeja, ropa y atributos) |
| `estaciones.py` | Clases `Estacion` (leche, vapor, espresso, medialunas, frutilla, dulce de leche, vainilla, tacho) y `Mesa` |
| `clientes.py` | Clase `Cliente` (Llegando, Sentado, Esperando, Atendido) y funciones para crear y sentar clientes |
| `dibujo.py` | Sprites pixel art (gatos, ítems, bandeja) escritos como grillas de texto, paneles y texto |
| `escenas.py` | Portada e ilustraciones pixel art de la historia de introducción |
| `generar_sonidos.py` | Script que sintetiza los sonidos y la música, normalizados por sonoridad (se ejecuta una vez; los .wav ya vienen incluidos) |
| `sonidos/` | Un sonido por acción (`leche`, `vapor`, `espresso`, `medialuna`, `topping`, `tacho`, `parcial`, `entrega`, `billete`, `caja`, `dia_completo`, `miau`) y `musica_lofi.wav` |
| `fuentes/` | Tipografía Jersey 15 y su licencia |
| `test_cambios.py` | Pruebas automáticas de las estaciones nuevas (`python -m unittest test_cambios`) |
| `requirements.txt` | Biblioteca necesaria (`pygame-ce`) |
| `imagenes/` | Opcional: PNG propios que reemplazan las ilustraciones de la introducción (ver `LEEME.txt`) |

## Imágenes, sonidos y tipografía: origen y licencia

- **Imágenes:** no hay archivos de imagen. Todo el pixel art (gatos, ítems, muebles, fondos y escenas) se dibuja por código con grillas y figuras de Pygame (propio).
- **Sonidos y música:** generados desde cero con `generar_sonidos.py` (ondas seno y ruido). Son propios, sin material de terceros.
- **Tipografía:** [Jersey 15](https://github.com/scfried/soft-type-jersey), de The Soft Type Project, licencia SIL Open Font License 1.1 (texto completo en `fuentes/OFL.txt`). Es de uso libre, incluso para entregas académicas.

## Uso de Inteligencia Artificial Generativa
- **Herramienta:** Claude (Anthropic).
- **Contexto de uso:** generación del código del juego a partir de mi especificación (concepto, historia, mecánicas, arquitectura de módulos y reglas) y de mis pedidos de cambio (pixel art, toppings de medialunas, pausa, bandeja en la mano, ojos verdes, etc.).