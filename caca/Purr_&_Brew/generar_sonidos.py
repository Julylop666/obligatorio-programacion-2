"""generar_sonidos.py - Crea los sonidos y la música del juego desde cero.

Todos los .wav de la carpeta sonidos/ se sintetizan con matemática (ondas seno,
ruido y envolventes), sin copiar nada de internet: son 100% propios y libres.
Ejecutar una sola vez:  python generar_sonidos.py

Todos los sonidos se NORMALIZAN por sonoridad (RMS), no por el pico: así ningún efecto
suena más fuerte que otro, y la música queda varios dB por debajo de los efectos.
Los volúmenes finales dentro del juego se ajustan en ajustes.py (VOLUMEN_EFECTOS, etc.).
"""
import math
import os
import random
import struct
import wave

TASA = 22050
CARPETA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sonidos")

RMS_EFECTOS = 0.09       # sonoridad objetivo de los efectos (aprox. -21 dBFS)
RMS_MUSICA = 0.045       # la música va ~6 dB más baja que los efectos
TECHO_PICO = 0.80        # ningún sonido pasa de este pico (evita distorsión)


def guardar(nombre, muestras, rms_objetivo=RMS_EFECTOS):
    """Normaliza las muestras (-1..1) a una sonoridad pareja y las guarda como WAV mono de 16 bits.

    La ganancia se calcula con el RMS de la parte que suena (sin contar el silencio de las colas),
    y se limita para que el pico nunca pase de TECHO_PICO. También aplica un fundido corto al
    principio y al final para que no haya 'clics'.
    """
    muestras = list(muestras)
    fade = int(0.006 * TASA)
    for i in range(min(fade, len(muestras))):
        muestras[i] *= i / fade
        muestras[-1 - i] *= i / fade
    pico = max(1e-9, max(abs(m) for m in muestras))
    activas = [m for m in muestras if abs(m) > 0.02 * pico]
    rms = math.sqrt(sum(m * m for m in activas) / len(activas))
    ganancia = min(rms_objetivo / rms, TECHO_PICO / pico)
    datos = b"".join(struct.pack("<h", int(max(-1.0, min(1.0, m * ganancia)) * 32767)) for m in muestras)
    os.makedirs(CARPETA, exist_ok=True)
    with wave.open(os.path.join(CARPETA, nombre), "wb") as archivo:
        archivo.setnchannels(1)
        archivo.setsampwidth(2)
        archivo.setframerate(TASA)
        archivo.writeframes(datos)


def pasa_bajos(muestras, factor):
    """Filtro pasa-bajos simple (factor chico = más grave y suave)."""
    salida, y = [], 0.0
    for m in muestras:
        y += (m - y) * factor
        salida.append(y)
    return salida


def campanita(frecuencia, t, decaimiento):
    """Una nota tipo cajita de música / campanita en el instante t."""
    if t < 0:
        return 0.0
    return (math.sin(2 * math.pi * frecuencia * t) + 0.25 * math.sin(4 * math.pi * frecuencia * t)
            + 0.08 * math.sin(6 * math.pi * frecuencia * t)) * math.exp(-t * decaimiento)


def generar_miau():
    """Un 'miau' suave: un tono que sube y baja con armónicos. Solo suena al elegir gato."""
    duracion = 0.5
    muestras, fase = [], 0.0
    for i in range(int(duracion * TASA)):
        avance = i / (duracion * TASA)
        frecuencia = 480 + 420 * math.sin(math.pi * avance ** 0.8)
        fase += 2 * math.pi * frecuencia / TASA
        envolvente = math.sin(math.pi * avance) ** 0.6
        muestras.append(envolvente * (math.sin(fase) + 0.4 * math.sin(2 * fase) + 0.2 * math.sin(3 * fase)))
    return pasa_bajos(muestras, 0.45)             # le saca lo chillón


def generar_billete():
    """Papel de billete: ruido agudo con dos 'crujidos' que decaen."""
    azar = random.Random(11)
    muestras, anterior = [], 0.0
    for i in range(int(0.3 * TASA)):
        t = i / TASA
        ruido = azar.uniform(-1, 1)
        agudo = ruido - anterior          # resta = filtro pasa-altos (suena a papel)
        anterior = ruido
        muestras.append(agudo * math.exp(-(t % 0.13) * 35) * math.exp(-t * 4))
    return pasa_bajos(muestras, 0.6)


def generar_vapor():
    """Vapor del vaporizador: ruido suave que sube y baja."""
    azar = random.Random(12)
    muestras, y = [], 0.0
    for i in range(int(1.0 * TASA)):
        avance = i / TASA
        y = y * 0.55 + azar.uniform(-1, 1) * 0.45
        muestras.append(y * math.sin(math.pi * avance) ** 1.5)
    return pasa_bajos(muestras, 0.5)


def generar_caja():
    """Timbre de caja registradora: un 'clic' y dos campanitas. Suena al comprar ropa."""
    azar = random.Random(13)
    muestras = []
    for i in range(int(0.9 * TASA)):
        t = i / TASA
        valor = azar.uniform(-1, 1) * math.exp(-t * 300) * 0.8                          # clic
        valor += math.sin(2 * math.pi * 1760 * t) * math.exp(-t * 6)                    # ding 1
        if t > 0.15:
            valor += math.sin(2 * math.pi * 2349 * (t - 0.15)) * math.exp(-(t - 0.15) * 6)  # ding 2
        muestras.append(valor * 0.6)
    return muestras


def generar_leche():
    """Leche que se sirve: chorrito grave con tres 'blup' de burbujas."""
    azar = random.Random(21)
    duracion = 0.75
    ruido = pasa_bajos([azar.uniform(-1, 1) for _ in range(int(duracion * TASA))], 0.12)
    muestras = []
    for i, r in enumerate(ruido):
        t = i / TASA
        envolvente = min(1.0, t / 0.08) * min(1.0, (duracion - t) / 0.2)
        muestras.append(r * 4.0 * envolvente * (0.65 + 0.35 * math.sin(2 * math.pi * 9 * t)))
    for inicio, base in ((0.12, 320), (0.31, 380), (0.50, 440)):         # burbujitas que suben de tono
        for i in range(int(0.09 * TASA)):
            t = i / TASA
            frecuencia = base * (1 + 2.0 * t)
            pos = int((inicio + t) * TASA)
            if pos < len(muestras):
                muestras[pos] += math.sin(2 * math.pi * frecuencia * t) * math.exp(-t * 38) * 0.9
    return muestras


def generar_espresso():
    """Máquina de espresso: zumbido de la bomba, chorrito de café y un 'plink' final."""
    azar = random.Random(22)
    duracion = 1.0
    total = int(duracion * TASA)
    ruido = pasa_bajos([azar.uniform(-1, 1) for _ in range(total)], 0.25)
    muestras = []
    for i in range(total):
        t = i / TASA
        bomba = (math.sin(2 * math.pi * 62 * t) + 0.5 * math.sin(2 * math.pi * 124 * t)) \
            * min(1.0, t / 0.05) * math.exp(-max(0.0, t - 0.35) * 9)
        chorro = ruido[i] * 2.5 * max(0.0, min(1.0, (t - 0.3) / 0.1)) * min(1.0, (duracion - t) / 0.3)
        muestras.append(bomba * 0.55 + chorro * 0.5)
    for i in range(int(0.3 * TASA)):                                     # gotita final
        t = i / TASA
        pos = int(0.7 * TASA) + i
        if pos < total:
            muestras[pos] += math.sin(2 * math.pi * 1250 * t) * math.exp(-t * 22) * 0.5
    return muestras


def generar_medialuna():
    """Medialuna crocante: tres 'crac' cortitos y un golpecito grave."""
    azar = random.Random(23)
    total = int(0.28 * TASA)
    muestras = [0.0] * total
    for inicio, fuerza in ((0.0, 1.0), (0.05, 0.7), (0.10, 0.5)):
        base = int(inicio * TASA)
        crujido = pasa_bajos([azar.uniform(-1, 1) for _ in range(int(0.05 * TASA))], 0.55)
        for i, c in enumerate(crujido):
            if base + i < total:
                muestras[base + i] += c * math.exp(-i / TASA * 80) * fuerza
    for i in range(total):
        t = i / TASA
        muestras[i] += math.sin(2 * math.pi * 140 * t) * math.exp(-t * 30) * 0.6
    return muestras


def generar_topping():
    """Topping/jarabe: un 'plop' húmedo (tono que cae) y otro más chiquito."""
    azar = random.Random(24)
    total = int(0.3 * TASA)
    muestras = [0.0] * total
    for inicio, f0, fuerza in ((0.0, 760, 1.0), (0.13, 960, 0.55)):
        base = int(inicio * TASA)
        fase = 0.0
        for i in range(int(0.14 * TASA)):
            t = i / TASA
            fase += 2 * math.pi * (f0 * math.exp(-t * 11) + 160) / TASA
            if base + i < total:
                muestras[base + i] += (math.sin(fase) * math.exp(-t * 26) + azar.uniform(-1, 1) * 0.08
                                       * math.exp(-t * 60)) * fuerza
    return pasa_bajos(muestras, 0.6)


def generar_tacho():
    """Tacho: un 'fsss' de papel que cae y un golpe sordo al fondo."""
    azar = random.Random(25)
    total = int(0.4 * TASA)
    ruido = pasa_bajos([azar.uniform(-1, 1) for _ in range(total)], 0.3)
    muestras = []
    for i, r in enumerate(ruido):
        t = i / TASA
        golpe = math.sin(2 * math.pi * 85 * t) * math.exp(-max(0.0, t - 0.16) * 22) if t > 0.16 else 0.0
        muestras.append(r * 2.2 * math.sin(math.pi * min(1.0, t / 0.2) / 2) * math.exp(-t * 7) + golpe * 0.9)
    return muestras


def generar_parcial():
    """Entregaste solo una parte: dos 'bips' suaves y cortitos, de tono parecido."""
    total = int(0.3 * TASA)
    muestras = [0.0] * total
    for inicio, frecuencia in ((0.0, 523.25), (0.13, 587.33)):
        for i in range(int(0.15 * TASA)):
            t = i / TASA
            pos = int(inicio * TASA) + i
            if pos < total:
                muestras[pos] += (math.sin(2 * math.pi * frecuencia * t) + 0.2 * math.sin(4 * math.pi * frecuencia * t)) \
                    * math.sin(math.pi * t / 0.15) ** 0.5 * math.exp(-t * 14)
    return muestras


def generar_entrega():
    """Pedido completo: campanita cálida de dos notas (sol y re)."""
    total = int(0.9 * TASA)
    return [campanita(784.0, i / TASA, 5) * 0.8 + campanita(1174.66, i / TASA - 0.12, 5) for i in range(total)]


def generar_dia_completo():
    """Día completado: arpegio ascendente tipo cajita de música (do-mi-sol-do) con brillito final."""
    total = int(1.8 * TASA)
    notas = ((523.25, 0.0), (659.25, 0.16), (783.99, 0.32), (1046.5, 0.48))
    muestras = []
    for i in range(total):
        t = i / TASA
        valor = sum(campanita(f, t - ini, 3.2 if f < 1000 else 2.4) for f, ini in notas)
        valor += campanita(2093.0, t - 0.5, 5) * 0.25                     # brillito
        muestras.append(valor)
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
    guardar("leche.wav", generar_leche())
    guardar("espresso.wav", generar_espresso())
    guardar("medialuna.wav", generar_medialuna())
    guardar("topping.wav", generar_topping())
    guardar("tacho.wav", generar_tacho())
    guardar("parcial.wav", generar_parcial())
    guardar("entrega.wav", generar_entrega())
    guardar("dia_completo.wav", generar_dia_completo())
    guardar("musica_lofi.wav", generar_musica(), RMS_MUSICA)
    print("Sonidos generados en", CARPETA)