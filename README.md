# Michi Café 2D

Juego cozy de cafetería hecho con Python y Pygame para Programación 2 (Facultad de Diseño, Universidad ORT Uruguay).
Sos un Licenciado en Diseño recién recibido que, convertido en gato, reemplaza a Don Salmón durante 5 días en su cafetería.

**Autor:** Ignacio López (N° 78200) - Grupo LT M4 A
**Repositorio:** https://github.com/TU-USUARIO/michi-cafe-2d   <!-- COMPLETAR con tu enlace real -->

## Cómo se juega

**Objetivo:** juntar la meta de dinero de cada día (Día 1: $50, Día 2: $120, Día 3: $220, Día 4: $350, Día 5: $500) y sobrevivir los 5 días.
Entre día y día podés comprar ropa en el ropero de Don Salmón para trabajar mejor.

**Cómo se gana:** completar el Día 5.
**Cómo se pierde:** si 4 vecinos quedan sin mesa a la vez, el local se desborda. Ojo: una mesa no se libera hasta que juntás el dinero que dejó el cliente.
En la pantalla de derrota o victoria, apretá **R** para volver a jugar sin cerrar la ventana.
No hay temporizadores ni clientes enojados: los vecinos esperan con paciencia.

**Preparar un café con leche:** Leche -> Vaporizador -> Espresso -> entregarlo en la mesa. Las medialunas se sacan directo del exhibidor.

### Controles

| Tecla | Acción |
|---|---|
| W A S D / Flechas | Moverse en 8 direcciones |
| E / Espacio | Interactuar (estaciones, mesas, cobrar) y avanzar menús |
| 1 - 5 | Comprar prendas en la tienda |
| R | Volver a jugar (pantallas de derrota y victoria) |

### Ropa de la tienda
- **Delantales:** más dinero por pedido (+20%).
- **Cofia / sombrero de chef:** la bandeja carga 2 o 3 ítems.
- **Calzado antideslizante / zapatillas de cocina:** más velocidad (+15% / +30%).

## Instalación y ejecución

Requiere Python 3.9 o superior.

```bash
pip install pygame
python main.py
```

Es la única biblioteca externa. Si no hay placa de sonido, el juego funciona igual sin audio.

## Qué hay en cada archivo

| Archivo | Contenido |
|---|---|
| `main.py` | Bucle principal, máquina de estados (clase `Juego`), pantallas y HUD |
| `ajustes.py` | Todas las constantes: colores, tamaños, velocidades, niveles, precios, tienda y textos de la historia |
| `jugador.py` | Clase `Jugador` (movimiento, bandeja, ropa y atributos) |
| `estaciones.py` | Clases `Estacion` (y sus hijas: leche, vapor, espresso, medialunas) y `Mesa` |
| `clientes.py` | Clase `Cliente` (Llegando, Sentado, Esperando, Atendido) y funciones para crear y sentar clientes |
| `dibujo.py` | Funciones para dibujar gatos, ítems, paneles y texto con formas de Pygame |
| `generar_sonidos.py` | Script que sintetiza los sonidos y la música (se ejecuta una vez; los .wav ya vienen incluidos) |
| `sonidos/` | `miau.wav`, `billete.wav`, `vapor.wav`, `caja.wav` y `musica_lofi.wav` |

## Imágenes y sonidos: origen y licencia

- **Imágenes:** no hay archivos de imagen. Todo está dibujado con figuras de Pygame (propio).
- **Sonidos y música:** generados desde cero con `generar_sonidos.py` (ondas seno y ruido). Son propios, sin material de terceros ni licencias que citar.

## Uso de Inteligencia Artificial Generativa

Según las pautas del obligatorio, se declara el uso de IA:

- **Herramienta:** Claude (Anthropic).
- **Contexto de uso:** generación inicial del código del juego a partir de mi especificación (concepto, historia, mecánicas, arquitectura de módulos y reglas), propuesta de estructura del informe, borrador de textos de documentación y composición del afiche.
- **Revisión:** revisé, probé y comprendí el código antes de entregarlo; los errores que contenga son mi responsabilidad. La idea, la historia, los personajes, las mecánicas, la estética y el balance del juego son propios.

## Créditos

Idea, diseño y dirección: Ignacio López. Inspirado en la estructura de los juegos de Papa Louie y en el estilo de los cozy games.
