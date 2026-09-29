"""Clase 26 · Medidas de dispersión: rango, varianza y desviación estándar."""
from fractions import Fraction as F
from collections import Counter
from math import isqrt
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO


# ---------------------------------------------------------------- estadística exacta
def mean(d):
    return F(sum(d), len(d))


def ssd(d):
    m = mean(d)
    return sum((x - m) ** 2 for x in d)


def var(d):
    return ssd(d) / len(d)


def sd_exact(v):
    """Raíz cuadrada exacta de un Fraction, o None."""
    v = F(v)
    a, b = isqrt(v.numerator), isqrt(v.denominator)
    return F(a, b) if a * a == v.numerator and b * b == v.denominator else None


def dataset(r, l, need="var", n=None, tries=400):
    """Datos enteros con media entera y varianza entera (need='var') o desviación entera (need='sd')."""
    for _ in range(tries):
        n_ = n or r.choice([4, 5, 6, 8] if l == 0 else [5, 6, 8, 10])
        m = r.randint(6, 40)
        s = r.randint(2, 5 if l == 0 else 8)
        dev = [r.randint(-s, s) for _ in range(n_ - 1)]
        dev.append(-sum(dev))
        if abs(dev[-1]) > s + 2 or len(set(dev)) < 3:
            continue
        d = [m + x for x in dev]
        v = F(sum(x * x for x in dev), n_)
        if v.denominator != 1 or v == 0:
            continue
        if need == "sd" and sd_exact(v) is None:
            continue
        r.shuffle(d)
        return d
    raise Reject("sin datos")


def lst(d):
    return ", ".join(str(x) for x in d)


def uniq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = a if isinstance(a, str) else fs(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- figuras
def _dots(d, lo, hi, y0, ymax, x0=40, x1=520, label=None):
    """Diagrama de puntos sobre eje horizontal con base en y0 (eje) y pila máxima ymax."""
    n = hi - lo
    step = (x1 - x0) / n
    b = L(x0 - 10, y0, x1 + 10, y0, INK, 3)
    every = 1 if n <= 14 else (2 if n <= 28 else 5)
    for v in range(lo, hi + 1):
        x = x0 + (v - lo) * step
        b += L(x, y0, x, y0 + 6, INK, 2)
        if (v - lo) % every == 0:
            b += T(x, y0 + 24, str(v), 15)
    rad = min(11, step / 2 - 1, 11)
    for v, k in sorted(Counter(d).items()):
        x = x0 + (v - lo) * step
        for j in range(k):
            b += C(x, y0 - rad - 2 - j * (2 * rad + 2), rad, FILL3, NAVY, 2)
    return b


def dots(d):
    lo, hi = min(d), max(d)
    lo, hi = lo - 1, hi + 1
    fm = max(Counter(d).values())
    h = 60 + fm * 24
    return wrap(560, h + 14, _dots(d, lo, hi, h - 20, fm), "Diagrama de puntos de los datos")


def dots2(dA, dB, la="A", lb="B"):
    lo, hi = min(dA + dB) - 1, max(dA + dB) + 1
    fa, fb = max(Counter(dA).values()), max(Counter(dB).values())
    ha, hb = 50 + fa * 24, 50 + fb * 24
    body = tag(30, 20, la, 16)
    body += _dots(dA, lo, hi, ha, fa)
    off = ha + 40
    body += tag(30, off + 20, lb, 16)
    body += _dots(dB, lo, hi, off + hb, fb)
    return wrap(560, off + hb + 40, body, "Dos diagramas de puntos con el mismo eje")


def freq_table(vals, freqs, head=("Valor", "Frecuencia")):
    n = len(vals)
    cw = min(80, 470 // (n + 1))
    x0 = 30
    b = ""
    for i, (row, lab) in enumerate(zip((vals, freqs), head)):
        y = 20 + i * 50
        b += R(x0, y, 90, 50, FILL, NAVY, 3) + T(x0 + 45, y + 31, lab, 14)
        for j, v in enumerate(row):
            b += R(x0 + 90 + j * cw, y, cw, 50, WHITE if i else FILL2, NAVY, 3) + T(x0 + 90 + j * cw + cw / 2, y + 32, str(v), 20)
    return wrap(560, 135, b, "Tabla de frecuencias")


def two_cards(a, b, la, lb):
    """Dos recuadros con estadísticos (líneas de texto) lado a lado."""
    body = ""
    for k, (lines, lab) in enumerate(((a, la), (b, lb))):
        x = 20 + k * 270
        body += R(x, 20, 250, 30 + 34 * len(lines) + 20, "#F1F5F9", NAVY, 3) + T(x + 125, 52, lab, 20)
        for i, t in enumerate(lines):
            body += T(x + 125, 92 + i * 34, t, 18)
    return wrap(560, 90 + 34 * len(a), body, "Comparación de dos grupos")


CTX = [("las notas de un curso", "puntos"), ("los tiempos de armado de una pieza", "minutos"), ("las edades de un grupo", "años"),
       ("los pesos de unos paquetes", "kg"), ("los puntajes de un juego", "puntos"), ("las temperaturas registradas", "°C")]
GRP = [("Curso A", "Curso B"), ("Máquina A", "Máquina B"), ("Equipo A", "Equipo B"), ("Sucursal A", "Sucursal B"), ("Sección A", "Sección B")]


# ---------------------------------------------------------------- Resolver problemas
def t_range_dots(r, l):
    d = dataset(r, 0 if l == 0 else 1, "var")
    rng = max(d) - min(d)
    ctx, u = r.choice(CTX)
    stem = f"El diagrama de puntos muestra {ctx}. ¿Cuál es el rango de los datos ({u})?"
    ans = str(rng)
    alts = [max(d), min(d), rng + 1, rng - 1, mean(d), max(d) - r.randint(2, 4), rng * 2]
    ex = f"Rango = máximo − mínimo = {max(d)} − {min(d)} = {rng}."
    return make(stem, dots(d), ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_variance(r, l):
    d = dataset(r, l, "var")
    v = var(d); m = mean(d)
    ctx, u = r.choice(CTX)
    stem = f"Se registraron {ctx}: {lst(d)}. Si la media es {m}, ¿cuál es la varianza de estos datos?"
    ans = fs(v)
    alts = [ssd(d), ssd(d) / (len(d) - 1), max(d) - min(d), F(sd_exact(v) or isqrt(int(v))), v + m, sum(abs(x - m) for x in d) / len(d)]
    ex = f"Varianza = suma de (x − media)² dividida por n: {fs(ssd(d))}/{len(d)} = {ans}."
    return make(stem, card(["Datos: " + lst(d), f"Media = {m}"], 150, 19), ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_sd_context(r, l):
    d = dataset(r, l, "sd")
    v = var(d); s = sd_exact(v); m = mean(d)
    ctx, u = r.choice(CTX)
    if l == 0:
        stem = f"Un conjunto de datos tiene varianza {fs(v)}. ¿Cuál es su desviación estándar?"
        ans = fs(s)
        alts = [v, v / 2, s + 1, s * 2, v * v, s - 1 if s > 1 else s + 2]
        ex = f"La desviación estándar es la raíz cuadrada de la varianza: √{fs(v)} = {ans}."
        return make(stem, card([f"Varianza = {fs(v)}"], 110, 22), ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)
    k = 2 if l == 2 else 1
    stem = f"{ctx.capitalize()} tienen media {m} {u} y varianza {fs(v)}. ¿Entre qué valores se encuentran los datos que están a lo más a {k} desviación{'es' if k > 1 else ''} estándar de la media?"
    lo, hi = m - k * s, m + k * s
    ans = f"Entre {fs(lo)} y {fs(hi)}"
    alts = [f"Entre {fs(m - k * v)} y {fs(m + k * v)}", f"Entre {fs(m - k * s * 2)} y {fs(m + k * s * 2)}", f"Entre {fs(m - s)} y {fs(m + s)}" if k == 2 else f"Entre {fs(m - 2 * s)} y {fs(m + 2 * s)}",
            f"Entre {fs(m - k * s - 1)} y {fs(m + k * s)}", f"Entre {fs(lo)} y {fs(hi + s)}"]
    ex = f"σ = √{fs(v)} = {fs(s)}; el intervalo es media ± {k}·σ = {fs(lo)} a {fs(hi)}."
    return make(stem, card([f"Varianza = {fs(v)}"], 110, 22), ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_daily_range(r, l):
    days = ["Lun", "Mar", "Mié", "Jue", "Vie"]
    k = 5 if l < 2 else 5
    mins = [r.randint(2, 12) for _ in range(k)]
    maxs = [m + r.randint(6, 20) for m in mins]
    amps = [b - a for a, b in zip(mins, maxs)]
    if len(set(amps)) < 4:
        raise Reject
    i = amps.index(max(amps))
    if amps.count(max(amps)) > 1:
        raise Reject
    b = ""
    for j, lab in enumerate(("Día", "Mín °C", "Máx °C")):
        pass
    head = R(20, 20, 100, 44, FILL) + T(70, 49, "Día", 16) + R(20, 64, 100, 44, FILL) + T(70, 93, "Mín (°C)", 16) + R(20, 108, 100, 44, FILL) + T(70, 137, "Máx (°C)", 16)
    for j in range(k):
        x = 120 + j * 84
        head += R(x, 20, 84, 44, FILL2) + T(x + 42, 49, days[j], 17)
        head += R(x, 64, 84, 44, WHITE) + T(x + 42, 93, str(mins[j]), 20)
        head += R(x, 108, 84, 44, WHITE) + T(x + 42, 137, str(maxs[j]), 20)
    fig = wrap(560, 172, head, "Temperaturas mínimas y máximas por día")
    if l == 0:
        stem = "La tabla muestra las temperaturas mínima y máxima de cinco días. ¿Qué día tuvo mayor variación térmica (mayor rango)?"
        ans = days[i]
        alts = [d for d in days if d != ans]
        ex = f"Rango diario = máx − mín. El mayor es {max(amps)} °C, el día {ans}."
        return make(stem, fig, ans, alts[:4], Q_MOD, ex)
    j = r.choice([x for x in range(k) if x != i])
    stem = "La tabla muestra las temperaturas mínima y máxima de cinco días. ¿Cuántos °C más de rango tuvo el día de mayor variación que el de menor variación?"
    ans = str(max(amps) - min(amps))
    alts = [max(amps), min(amps), max(maxs) - min(mins), max(amps) + min(amps), max(amps) - min(amps) + 1, max(amps) - min(amps) - 1]
    ex = f"Rangos diarios: {', '.join(str(a) for a in amps)}. Diferencia entre el mayor y el menor: {ans}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_MOD, ex)


def t_compare_sd(r, l):
    ga, gb = r.choice(GRP)
    ctx, u = r.choice(CTX)
    m = r.randint(20, 80)
    sa, sb = r.sample(range(2, 15), 2)
    if abs(sa - sb) < 2:
        raise Reject
    if l == 0:
        ma = mb = m
    else:
        ma, mb = r.sample(range(20, 90), 2)
        if l == 2 and (sa < sb) != (ma > mb):
            pass
    fig = two_cards([f"Media: {ma}", f"Desviación estándar: {sa}"], [f"Media: {mb}", f"Desviación estándar: {sb}"], ga, gb)
    homo = ga if sa < sb else gb
    other = gb if sa < sb else ga
    stem = f"Se comparan {ctx} de dos grupos. ¿Cuál de los grupos presenta datos más homogéneos (menos dispersos)?"
    ans = f"{homo}, porque su desviación estándar es menor"
    alts = [f"{other}, porque su desviación estándar es menor", f"{homo}, porque su desviación estándar es mayor", f"{other}, porque su desviación estándar es mayor",
            f"{ga}, porque su media es {'mayor' if ma > mb else 'menor'}" if ma != mb else "Ambos son igual de homogéneos, porque tienen la misma media"]
    ex = f"Menor desviación estándar implica datos más concentrados alrededor de la media: {homo}."
    return make(stem, fig, ans, pick4(ans, alts + ["No se puede saber sin conocer todos los datos"]), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_which_more_spread(r, l):
    while True:
        n = r.choice([6, 8, 10])
        m = r.randint(8, 24)
        s1 = r.randint(1, 2)
        s2 = r.randint(3, 6 if l < 2 else 5)
        A = [m + r.randint(-s1, s1) for _ in range(n)]
        B = [m + r.randint(-s2, s2) for _ in range(n)]
        if max(B) - min(B) > max(A) - min(A) + 1 and len(set(A)) > 1 and len(set(B)) > 1:
            break
    if l == 1:
        # etiquetar aleatoriamente
        pass
    swap = r.random() < 0.5
    if swap:
        A, B = B, A
    more = "A" if swap else "B"
    less = "B" if swap else "A"
    ctx, u = r.choice(CTX)
    stem = f"Los diagramas representan {ctx} de dos conjuntos con igual cantidad de datos y valores centrales similares. ¿Qué afirmación es correcta?"
    ans = f"El conjunto {more} tiene mayor dispersión, pues sus datos están más alejados de la media"
    alts = [f"El conjunto {less} tiene mayor dispersión, pues sus datos están más alejados de la media",
            f"El conjunto {more} tiene menor dispersión, pues sus datos están más alejados de la media",
            f"Ambos conjuntos tienen igual dispersión, pues sus datos están centrados en un valor similar",
            f"El conjunto {less} tiene menor dispersión, pues su rango es mayor"]
    ex = f"El conjunto {more} ocupa un tramo más ancho del eje: mayor rango y datos más alejados de la media, luego mayor desviación estándar."
    return make(stem, dots2(A, B), ans, alts, Q_REP, ex)


def t_read_range(r, l):
    d = dataset(r, 0 if l == 0 else 1, "var")
    ctx, u = r.choice(CTX)
    k = r.choice(["rango", "diferencia entre el mayor y el menor dato"])
    rng = max(d) - min(d)
    stem = f"A partir del diagrama, que representa {ctx}, ¿cuál es la {k}?" if k != "rango" else f"A partir del diagrama, que representa {ctx}, ¿cuál es el rango?"
    ans = str(rng)
    alts = [max(d) + min(d), rng + 2, rng - 1, len(d), max(d), F(max(d) + min(d), 2)]
    ex = f"{max(d)} − {min(d)} = {rng}."
    return make(stem, dots(d), ans, pick4(ans, uniq(ans, alts)), Q_REP, ex)


def t_freq_var(r, l):
    """Interpretar tabla de frecuencias: promedio de las desviaciones cuadráticas."""
    for _ in range(300):
        vals = sorted(r.sample(range(1, 15), 4 if l < 2 else 5))
        fr = [r.randint(1, 5) for _ in vals]
        d = [v for v, f in zip(vals, fr) for _ in range(f)]
        m = mean(d)
        if m.denominator != 1:
            continue
        v = var(d)
        if v.denominator == 1 and v > 0:
            break
    else:
        raise Reject
    ctx, u = r.choice(CTX)
    stem = f"La tabla resume {ctx}. ¿Cuál es el rango de los datos y cuál su media?"
    rng = max(d) - min(d)
    ans = f"Rango {rng} y media {m}"
    alts = [f"Rango {rng} y media {fs(F(sum(vals), len(vals)))}", f"Rango {max(d)} y media {m}", f"Rango {rng + 1} y media {m + 1}", f"Rango {len(d)} y media {m}", f"Rango {rng} y media {fs(m + 1)}"]
    ex = f"Rango = {max(d)} − {min(d)} = {rng}; media ponderada por las frecuencias = {m}."
    alts = [a for a in alts if a != ans]
    return make(stem, freq_table(vals, fr), ans, alts[:4], Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
TRUE = [
    "La desviación estándar nunca es negativa",
    "Si todos los datos son iguales, la varianza es cero",
    "La desviación estándar se expresa en la misma unidad que los datos",
    "La varianza es el promedio de los cuadrados de las desviaciones respecto de la media",
    "Un rango mayor no siempre implica una desviación estándar mayor",
    "Si la desviación estándar es cero, todos los datos coinciden con la media",
    "Mientras más concentrados están los datos, menor es la desviación estándar",
    "La varianza es el cuadrado de la desviación estándar",
]
FALSE = [
    "La varianza puede ser negativa si hay datos menores que la media",
    "La suma de las desviaciones respecto de la media siempre es positiva",
    "Si el rango es cero, la desviación estándar es positiva",
    "La desviación estándar es siempre menor que el rango dividido por dos",
    "Dos conjuntos con la misma media tienen siempre la misma desviación estándar",
    "La varianza y la desviación estándar siempre coinciden",
    "Agregar un dato muy alejado de los demás disminuye el rango",
    "Una desviación estándar mayor indica que los datos son más homogéneos",
    "El rango depende de todos los datos y no solo de los extremos",
    "La varianza se expresa en la misma unidad que los datos",
    "La desviación estándar es la mitad de la varianza",
    "Si la media aumenta, la desviación estándar aumenta siempre",
]


def _disp_fig(r):
    m = r.randint(8, 20)
    A = [m + r.choice([-1, 0, 0, 1]) for _ in range(8)]
    B = [m + r.choice([-5, -3, 0, 3, 5]) for _ in range(8)]
    return dots2(A, B, "Poco", "Mucho")


def t_props(r, l):
    ctx, u = r.choice(CTX)
    t = r.choice(TRUE)
    fs_ = r.sample(FALSE, 4)
    stem = f"Respecto de la dispersión de {ctx}, ¿cuál de las siguientes afirmaciones es verdadera?"
    return make(stem, _disp_fig(r), t, fs_, Q_ARG, "La afirmación correcta se deduce de la definición: la varianza promedia los cuadrados de las desviaciones y σ = √varianza ≥ 0.")


def t_which_false(r, l):
    ctx, u = r.choice(CTX)
    f_ = r.choice(FALSE)
    ts = r.sample(TRUE, 4)
    stem = f"Sobre las medidas de dispersión de {ctx}, ¿cuál de las siguientes afirmaciones es FALSA?"
    return make(stem, _disp_fig(r), f_, ts, Q_ARG, "Se contrasta cada afirmación con la definición de rango, varianza y desviación estándar; solo una es incorrecta.")


def t_error(r, l):
    d = dataset(r, 0, "var")
    m, v = mean(d), var(d)
    k = r.randrange(3)
    ERR = ["Dividió por la media en lugar de dividir por el número de datos",
           "Usó las desviaciones sin elevarlas al cuadrado, por lo que se anulan",
           "Entregó la suma de los cuadrados sin dividir por el número de datos",
           "Calculó el rango y lo presentó como varianza"]
    if k == 0:
        line = f"Varianza = {fs(ssd(d))} / {fs(m)} = {fs(ssd(d) / m)}"; ans = ERR[0]
    elif k == 1:
        line = f"Varianza = (suma de desviaciones) / {len(d)} = 0"; ans = ERR[1]
    else:
        line = f"Varianza = {fs(ssd(d))}"; ans = ERR[2]
    if k == 0 and ssd(d) / m == v:
        raise Reject
    fig = card([f"Datos: {lst(d)}", f"Media = {m}", line.replace("-", "−")], 190, 19)
    stem = "Un estudiante calculó la varianza de los datos como se muestra. ¿Qué error cometió?"
    return make(stem, fig, ans, [e for e in ERR if e != ans] + ["Usó la desviación estándar en vez de la media"], Q_ARG,
                "La varianza es la suma de los cuadrados de las desviaciones dividida por el número de datos.")


def t_homog_arg(r, l):
    ga, gb = r.choice(GRP)
    ctx, u = r.choice(CTX)
    sa, sb = r.sample(range(3, 20), 2)
    if abs(sa - sb) < 2:
        raise Reject
    ma = r.randint(30, 90)
    mb = ma
    homo, oth = (ga, gb) if sa < sb else (gb, ga)
    fig = two_cards([f"Media: {ma}", f"Varianza: {sa * sa}"], [f"Media: {mb}", f"Varianza: {sb * sb}"], ga, gb)
    stem = f"Dos grupos tienen {ctx} con la misma media. ¿Cuál afirmación es correcta según sus varianzas?"
    ans = f"{homo} es más homogéneo, pues su varianza es menor"
    alts = [f"{oth} es más homogéneo, pues su varianza es menor", f"{homo} es más homogéneo, pues su varianza es mayor", f"{oth} es más homogéneo, pues su varianza es mayor", "Ambos son igual de homogéneos, pues sus medias coinciden"]
    return make(stem, fig, ans, alts, Q_ARG, "Con igual media, menor varianza indica datos más cercanos a la media, es decir más homogéneos.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_var_calc(r, l):
    d = dataset(r, l, "var")
    v = var(d); m = mean(d)
    stem = f"Calcula la varianza (poblacional) del conjunto de datos: {lst(d)}."
    ans = fs(v)
    alts = [ssd(d), ssd(d) / (len(d) - 1), max(d) - min(d), F(isqrt(int(v))) + 1 if v > 1 else v + 1, v + 1, m]
    ex = f"Media = {m}. Suma de (x − media)² = {fs(ssd(d))}; dividida por {len(d)} da {ans}."
    return make(stem, dots(d), ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


def t_sd_calc(r, l):
    d = dataset(r, l, "sd")
    v = var(d); s = sd_exact(v); m = mean(d)
    stem = f"¿Cuál es la desviación estándar (poblacional) de los datos: {lst(d)}?"
    ans = fs(s)
    alts = [v, s + 1, s * 2, ssd(d), max(d) - min(d), s - 1 if s > 1 else s + 3]
    ex = f"Media = {m}; varianza = {fs(v)}; desviación estándar = √{fs(v)} = {ans}."
    return make(stem, dots(d), ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


def t_missing(r, l):
    d = dataset(r, 0, "var")
    if l == 0:
        i, j = d.index(max(d)), d.index(min(d))
        rest = [x for k, x in enumerate(d) if k != i]
        rng = max(d) - min(d)
        stem = f"Los datos {lst(rest)} y un valor desconocido x tienen rango {rng}, y x es el mayor. ¿Cuánto vale x?"
        ans = str(max(d))
        alts = [rng, rng + min(d) + 1, max(d) + 2, max(d) - 1, min(d) - rng]
        ex = f"x − {min(d)} = {rng}, luego x = {max(d)}."
        return make(stem, card(["Datos conocidos: " + lst(rest) + (" y x" if l == 0 else "")], 120, 19), ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)
    m = mean(d)
    i = r.randrange(len(d))
    rest = d[:i] + d[i + 1:]
    stem = f"Cinco o más datos tienen media {m}. Se conocen {len(rest)} de ellos: {lst(rest)}. ¿Cuál es el dato que falta?"
    ans = str(d[i])
    alts = [m, d[i] + 1, d[i] - 1, sum(rest), d[i] + 2, F(sum(rest), len(rest))]
    ex = f"La suma total es {m}·{len(d)} = {m * len(d)}; falta {m * len(d)} − {sum(rest)} = {d[i]}."
    return make(stem, card(["Datos conocidos: " + lst(rest) + (" y x" if l == 0 else "")], 120, 19), ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


BY_SKILL = {
    Q_RES: [t_range_dots, t_variance, t_sd_context],
    Q_MOD: [t_daily_range, t_compare_sd],
    Q_REP: [t_which_more_spread, t_read_range, t_freq_var],
    Q_ARG: [t_props, t_which_false, t_error, t_homog_arg],
    Q_PRO: [t_var_calc, t_sd_calc, t_missing],
}
