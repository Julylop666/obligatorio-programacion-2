"""generar_sonidos.py - Crea los sonidos y la música del juego desde cero.

Todos los .wav de la carpeta sonidos/ se sintetizan con matemática (ondas seno,
ruido y envolventes), sin copiar nada de internet: son 100% propios y libres.
Ejecutar una sola vez:  python generar_sonidos.py
"""
import math
import os
import random
import struct
import wave

TASA = 22050
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos")


def guardar(nombre, muestras):
    """Normaliza la lista de muestras (-1..1) y la guarda como WAV mono de 16 bits."""
    maximo = max(1e-9, max(abs(m) for m in muestras))
    datos = b"".join(struct.pack("<h", int(m / maximo * 0.85 * 32767)) for m in muestras)
    os.makedirs(CARPETA, exist_ok=True)
    with wave.open(os.path.join(CARPETA, nombre), "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(TASA)
        archivo.writeframes(datos)


def generar_miau():
    """Un 'miau' suave: un tono que sube y baja con armónicos."""
    duracion = 0.5
    muestras, fase = [], 0.0
    for i in range(int(duracion * TASA)):
        avance = i / (duracion * TASA)
        frecuencia = 480 + 420 * math.sin(math.pi * avance ** 0.8)
        fase += 2 * math.pi * frecuencia / TASA
        envolvente = math.sin(math.pi * avance) ** 0.6
        muestras.append(envolvente * (math.sin(fase) + 0.4 * math.sin(2 * fase) + 0.2 * math.sin(3 * fase)))
    return muestras


def generar_billete():
    """Papel de billete: ruido agudo con dos 'crujidos' que decaen."""
    muestras, anterior = [], 0.0
    for i in range(int(0.3 * TASA)):
        t = i / TASA
        ruido = random.uniform(-1, 1)
        agudo = ruido - anterior          # resta = filtro pasa-altos (suena a papel)
        anterior = ruido
        muestras.append(agudo * math.exp(-(t % 0.13) * 35) * math.exp(-t * 4))
    return muestras


def generar_vapor():
    """Vapor de la máquina de café: ruido suave que sube y baja."""
    muestras, y = [], 0.0
    for i in range(int(1.0 * TASA)):
        avance = i / TASA
        y = y * 0.55 + random.uniform(-1, 1) * 0.45
        muestras.append(y * math.sin(math.pi * avance) ** 1.5)
    return muestras


def generar_caja():
    """Timbre de caja registradora: un 'clic' y dos campanitas."""
    muestras = []
    for i in range(int(0.9 * TASA)):
        t = i / TASA
        valor = random.uniform(-1, 1) * math.exp(-t * 300) * 0.8                       # clic
        valor += math.sin(2 * math.pi * 1760 * t) * math.exp(-t * 6)                    # ding 1
        if t > 0.15:
            valor += math.sin(2 * math.pi * 2349 * (t - 0.15)) * math.exp(-(t - 0.15) * 6)  # ding 2
        muestras.append(valor * 0.6)
    return muestras


def generar_musica():
    """Loop lo-fi de 16 segundos: acordes suaves (Am7-Dm7-G7-Cmaj7), bajo y notitas sueltas."""
    random.seed(7)                                   # misma música cada vez que se genera
    acordes = [
        (110.0, [220.0, 261.63, 329.63, 392.0]),     # Am7
        (146.83, [293.66, 349.23, 440.0, 523.25]),   # Dm7
        (98.0, [196.0, 246.94, 293.66, 349.23]),     # G7
        (130.81, [261.63, 329.63, 392.0, 493.88]),   # Cmaj7
    ]
    seg = 4.0
    total = int(seg * len(acordes) * TASA)
    buf = [0.0] * total
    for n_acorde, (bajo, notas) in enumerate(acordes):
        inicio = int(n_acorde * seg * TASA)
        for i in range(int(seg * TASA)):
            t = i / TASA
            env = min(1.0, t / 0.4) * min(1.0, (seg - t) / 0.6)       # entra y sale suave
            pad = sum(math.sin(2 * math.pi * f * t) for f in notas) * 0.07
            pad += math.sin(2 * math.pi * bajo * t) * 0.22
            buf[inicio + i] += pad * env
        for paso in range(int(seg / 0.5)):                            # notitas cada medio segundo
            if random.random() < 0.55:
                f = random.choice(notas) * 2
                ini = inicio + int(paso * 0.5 * TASA)
                for i in range(int(0.45 * TASA)):
                    t = i / TASA
                    if ini + i < total:
                        buf[ini + i] += math.sin(2 * math.pi * f * t) * math.exp(-t * 7) * 0.12
    for i in range(total):                                            # crujidito de vinilo
        if random.random() < 0.0006:
            buf[i] += random.uniform(-0.05, 0.05)
    return buf


if __name__ == "__main__":
    guardar("miau.wav", generar_miau())
    guardar("billete.wav", generar_billete())
    guardar("vapor.wav", generar_vapor())
    guardar("caja.wav", generar_caja())
    guardar("musica_lofi.wav", generar_musica())
    print("Sonidos generados en", CARPETA)
