"""Contenidos del temario oficial DEMRE M2 que la planificación no cubre con clase propia:
modelos probabilísticos (binomial y normal), circunferencia y esfera, rectas, funciones seno/coseno,
matemática financiera, sistemas 2x2 y suficiencia de datos. Se integran al Ensayo General."""
import math
from fractions import Fraction as F
from math import comb
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO


def n_(x):
    return f"{int(x):,}".replace(",", ".")


def dc(x, d=3):
    return f"{x:.{d}f}".replace(".", ",")


SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(SUP)


def uniq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = a if isinstance(a, str) else fs(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


# ================================================================ Modelos probabilísticos
PTAB = {0.67: 0.749, 0.99: 0.839, 1.00: 0.841, 1.15: 0.875, 1.28: 0.900, 1.64: 0.950, 1.96: 0.975, 2.00: 0.977, 2.17: 0.985, 2.32: 0.990, 2.58: 0.995}


def bell(shade, labels=(), title=None):
    """Curva normal estándar (x en -3.5..3.5); sombrea entre shade=(a, b). labels: [(x, texto)] bajo el eje."""
    x0, x1, base, hh = 40, 520, 175, 140
    X = lambda x: x0 + (x + 3.5) / 7 * (x1 - x0)
    Y = lambda x: base - hh * math.exp(-x * x / 2)
    a, b = max(shade[0], -3.5), min(shade[1], 3.5)
    pts = [(X(a + (b - a) * i / 60), Y(a + (b - a) * i / 60)) for i in range(61)]
    poly = [(X(a), base)] + pts + [(X(b), base)]
    body = P(poly, FILL3, FILL3, 1)
    curve = " ".join(f"{X(-3.5 + 7 * i / 200):.1f},{Y(-3.5 + 7 * i / 200):.1f}" for i in range(201))
    body += f'<polyline fill="none" stroke="{NAVY}" stroke-width="4" points="{curve}"/>' + L(x0 - 10, base, x1 + 10, base, INK, 3)
    for xv, t in labels:
        body += L(X(xv), base, X(xv), base + 7, INK, 2.5) + T(X(xv), base + 28, t, 16)
    return wrap(560, 225, body, "Curva de la distribución normal con una zona sombreada")


def t_normal_table(r, l):
    z = r.choice([k for k in PTAB if k >= 0.67])
    p = PTAB[z]
    kind = r.choice(["gt", "between", "lt_neg", "gt_neg" if l else "gt"])
    zs = dc(z, 2)
    if kind == "gt":
        val, sh, lab, txt = 1 - p, (z, 9), [(0, "0"), (z, zs)], f"P(Z > {zs})"
    elif kind == "between":
        val, sh, lab, txt = 2 * p - 1, (-z, z), [(-z, "−" + zs), (z, zs)], f"P(−{zs} ≤ Z ≤ {zs})"
    elif kind == "lt_neg":
        val, sh, lab, txt = 1 - p, (-9, -z), [(-z, "−" + zs), (0, "0")], f"P(Z ≤ −{zs})"
    else:
        val, sh, lab, txt = p, (-z, 9), [(-z, "−" + zs), (0, "0")], f"P(Z ≥ −{zs})"
    stem = f"Sea Z una variable aleatoria con distribución normal N(0, 1), tal que P(Z ≤ {zs}) = {dc(p)}. ¿Cuál es el valor de {txt}?"
    ans = dc(val)
    alts = [p, 1 - p, 2 * p - 1, 2 * (1 - p), 2 * p, p - 0.5, 1 - 2 * p if p < 0.5 else 2 * p - 1 + 0.001]
    alts = [dc(a) for a in alts if 0 < a < 1]
    alts = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, bell(sh, lab), ans, alts[:4], Q_RES, f"Por simetría de la normal: {txt} = {ans}.")


def t_normal_std(r, l):
    cands = [(z, s) for z in PTAB for s in (4, 5, 10, 20, 25, 50, 100) if (F(str(z)) * s).denominator == 1 and F(str(z)) * s >= 1]
    z, s = r.choice(cands)
    mu = r.choice([50, 60, 100, 120, 150, 500, 1000])
    x = mu + int(F(str(z)) * s)
    what = r.choice(["Peso", "Tiempo", "Puntaje", "Longitud"])
    unit = {"Peso": "gramos", "Tiempo": "minutos", "Puntaje": "puntos", "Longitud": "cm"}[what]
    upper = r.random() < 0.5 and l > 0
    stem = (f"{what} de un producto: variable con distribución normal de media {mu} y desviación estándar {s} ({unit}). "
            f"Se sabe que P(Z ≤ {dc(z, 2)}) = {dc(PTAB[z])}. ¿Cuál es la probabilidad de que el valor {'supere' if upper else 'sea a lo más'} {x}?")
    p = PTAB[z]
    ans = dc(1 - p if upper else p)
    fig = bell((z, 9) if upper else (-9, z), [(0, f"μ = {mu}"), (z, str(x))])
    alts = [p, 1 - p, 2 * p - 1, 0.5, p / 2, 1 - p / 2]
    alts = [dc(a) for a in dict.fromkeys(alts) if 0 < a < 1 and dc(a) != ans]
    return make(stem, fig, ans, alts[:4], Q_RES, f"z = ({x} − {mu})/{s} = {dc(z, 2)}; se usa la tabla: {ans}.")


def _binom_data(r, l):
    n = r.randint(4, 8 if l else 6)
    k = r.randint(1, n - 1)
    if k == n - k:
        raise Reject
    p = r.choice([0.2, 0.3, 0.4, 0.6, 0.7, 0.8])
    return n, k, p


def t_binom_expr(r, l):
    n, k, p = _binom_data(r, l)
    q = round(1 - p, 1)
    ps, qs = dc(p, 1), dc(q, 1)
    ctx = r.choice([("Un jugador encesta un tiro libre con probabilidad", "encestes", "tiros"), ("Una máquina produce una pieza sin fallas con probabilidad", "piezas sin fallas", "piezas"),
                    ("Un estudiante acierta una pregunta con probabilidad", "aciertos", "preguntas")])
    stem = f"{ctx[0]} {ps}, de forma independiente en cada intento. ¿Qué expresión representa la probabilidad de obtener exactamente {k} {ctx[1]} en {n} {ctx[2]}?"
    ans = f"C({n},{k})·({ps}){sup(k)}·({qs}){sup(n - k)}"
    alts = [f"({ps}){sup(k)}·({qs}){sup(n - k)}", f"C({n},{k})·({ps}){sup(n - k)}·({qs}){sup(k)}", f"C({n},{k})·({ps}){sup(k)}·({qs}){sup(k)}", f"{n}·({ps}){sup(k)}·({qs}){sup(n - k)}", f"C({n},{k})·({ps}){sup(k)}"]
    fig = card([f"n = {n} intentos independientes", f"p (éxito) = {ps}", f"X = número de {ctx[1]}"], 170, 19)
    return make(stem, fig, ans, alts[:4], Q_MOD, "X ~ Binomial(n, p): P(X = k) = C(n,k)·p^k·(1 − p)^(n−k).")


def bars(vals, labels, hi=None, mark=None):
    n = len(vals)
    hi = hi or max(vals)
    bw = min(70, 430 // n)
    gap = (500 - n * bw) / max(1, n - 1)
    body = L(30, 190, 540, 190, INK, 3)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        x = 40 + i * (bw + gap)
        h = 140 * v / hi
        body += R(x, 190 - h, bw, h, FILL2 if mark == i else FILL) + T(x + bw / 2, 214, lab, 17)
    return wrap(560, 230, body, "Diagrama de barras de una variable binomial")


def t_binom_calc(r, l):
    n = r.randint(3, 8 if l else 6)
    k = r.randint(1, n - 1)
    vals = [comb(n, j) for j in range(n + 1)]
    fig = bars(vals, [f"X={j}" if n <= 6 else str(j) for j in range(n + 1)], mark=k)
    stem = f"Se lanza {n} veces una moneda equilibrada; las barras son proporcionales a las formas de obtener cada número de caras. ¿Cuál es la probabilidad de obtener exactamente {k} caras?"
    ans = fs(F(comb(n, k), 2 ** n))
    alts = [F(1, 2 ** n), F(k, n), F(comb(n, k), 2 ** k), F(comb(n, k), n), F(comb(n, k), 2 * n), F(1, 2)]
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, f"C({n},{k})/2^{n} = {comb(n, k)}/{2 ** n}.")


def t_binom_bars(r, l):
    n = r.randint(4, 5)
    while True:
        w = [r.randint(1, 8) * 5 for _ in range(n + 1)]
        if sum(w) == 100:
            break
        w = None
        if r.random() < 0.02:
            break
    if not w:
        raise Reject
    body = L(30, 190, 540, 190, INK, 3)
    bw = 54
    gap = (500 - (n + 1) * bw) / n
    for i, v in enumerate(w):
        x = 40 + i * (bw + gap)
        h = 140 * v / max(w)
        body += R(x, 190 - h, bw, h, FILL) + tag(x + bw / 2, 190 - h - 16, f"{v}%", 16) + T(x + bw / 2, 216, f"X={i}", 16)
    fig = wrap(560, 234, body, "Distribución de probabilidad de X")
    k = r.randint(1, n - 1)
    kind = r.choice(["ge", "le", "gt", "lt"])
    f_ = {"ge": lambda j: j >= k, "le": lambda j: j <= k, "gt": lambda j: j > k, "lt": lambda j: j < k}
    sym = {"ge": "≥", "le": "≤", "gt": ">", "lt": "<"}
    val = {kk: sum(v for j, v in enumerate(w) if f_[kk](j)) for kk in f_}
    ans = f"{val[kind]}%"
    alts = [f"{val[x]}%" for x in f_ if x != kind] + [f"{w[k]}%", f"{100 - val[kind]}%"]
    alts = [a for a in dict.fromkeys(alts) if a != ans]
    stem = f"El gráfico muestra la distribución de probabilidad de una variable X. ¿Cuál es el valor de P(X {sym[kind]} {k})?"
    return make(stem, fig, ans, alts[:4], Q_REP, f"Se suman las probabilidades de los valores de X que cumplen la condición: {ans}.")


TN = ["La curva es simétrica respecto de la media", "La media, la mediana y la moda coinciden", "Aproximadamente el 68% de los datos está a una desviación estándar de la media",
      "El área total bajo la curva es igual a 1", "Si se suma una constante a los datos, la curva solo se desplaza"]
FN = ["La curva es simétrica respecto del eje X", "La probabilidad de un valor exacto es siempre positiva", "Aproximadamente el 68% de los datos está a dos desviaciones estándar de la media",
      "El área total bajo la curva depende de la desviación estándar", "Si se suma una constante a los datos, la curva se hace más ancha"]


def t_normal_arg(r, l):
    ctx = r.choice(["las estaturas", "los tiempos de reacción", "los pesos", "los puntajes de una prueba"])
    stem = f"Se modela {ctx} de una población con una distribución normal. ¿Cuál de las siguientes afirmaciones es verdadera?"
    m = r.randint(-1, 1)
    return make(stem, bell((-1, 1), [(-1, "μ − σ"), (0, "μ"), (1, "μ + σ")]), r.choice(TN), r.sample(FN, 4), Q_ARG, "Propiedades de la normal: simetría, media = mediana = moda, área total 1 y regla 68–95–99,7.")


# ================================================================ Circunferencia, esfera y rectas
def _pt(cx, cy, rad, deg):
    a = math.radians(deg)
    return cx + rad * math.cos(a), cy - rad * math.sin(a)


def t_inscribed(r, l):
    th = r.choice([40, 50, 60, 70, 80, 100, 110, 120, 130, 140])
    a0 = r.choice([200, 210, 220, 230])
    cx, cy, rad = 280, 165, 110
    O = (cx, cy)
    A, B = _pt(cx, cy, rad, a0), _pt(cx, cy, rad, a0 + th)
    C_ = _pt(cx, cy, rad, a0 + th + (360 - th) / 2)
    ask_ins = r.random() < 0.6
    body = f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="#EFF6FF" stroke="{NAVY}" stroke-width="4"/>'
    body += L(*O, *A, INK, 3) + L(*O, *B, INK, 3) + L(*C_, *A, ACC, 3.5) + L(*C_, *B, ACC, 3.5)
    for pt in (O, A, B, C_):
        body += C(pt[0], pt[1], 5, INK, INK, 1)
    body += tag(O[0], O[1] + 28, f"{th}°" if ask_ins else "?", 16)
    body += tag(C_[0], C_[1] + (22 if C_[1] > cy else -22), "?" if ask_ins else f"{th // 2}°", 16)
    for nm, pt, dx, dy in (("O", O, 12, -10), ("A", A, -18, 0), ("B", B, 18, 6), ("C", C_, 0, 26 if C_[1] > cy else -30)):
        body += T(pt[0] + dx, pt[1] + dy + 6, nm, 20)
    fig = wrap(560, 310, body, "Circunferencia con ángulo del centro y ángulo inscrito")
    if ask_ins:
        stem = f"En la circunferencia de centro O, el ángulo del centro AOB mide {th}°. ¿Cuánto mide el ángulo inscrito ACB, que subtiende el mismo arco AB?"
        ans, alts = f"{th // 2}°", [f"{th}°", f"{2 * th}°", f"{180 - th // 2}°", f"{90 - th // 2}°", f"{th // 2 + 10}°"]
    else:
        stem = f"En la circunferencia de centro O, el ángulo inscrito ACB mide {th // 2}°. ¿Cuánto mide el ángulo del centro AOB que subtiende el mismo arco?"
        ans, alts = f"{th}°", [f"{th // 2}°", f"{2 * th}°", f"{180 - th}°", f"{th + 10}°", f"{th // 4}°"]
    return make(stem, fig, ans, uniq(ans, alts)[:4], Q_RES, "El ángulo del centro mide el doble que el ángulo inscrito que subtiende el mismo arco.")


def t_chords(r, l):
    a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 9)
    if (a * b) % c or a * b // c == c or a * b // c > 24:
        raise Reject
    x = a * b // c
    cx, cy, rad = 280, 140, 110
    A, B = _pt(cx, cy, rad, 170), _pt(cx, cy, rad, 10)
    Cp, D = _pt(cx, cy, rad, 100), _pt(cx, cy, rad, 280)
    Pp = (cx + 8, cy - 14)
    body = f'<circle cx="{cx}" cy="{cy}" r="{rad}" fill="#EFF6FF" stroke="{NAVY}" stroke-width="4"/>'
    body += L(*A, *B, INK, 3.5) + L(*Cp, *D, ACC, 3.5)
    mid = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    for pt in (A, B, Cp, D, Pp):
        body += C(pt[0], pt[1], 5, INK, INK, 1)
    body += tag(*[u + v for u, v in zip(mid(A, Pp), (0, -20))], str(a), 16) + tag(*[u + v for u, v in zip(mid(Pp, B), (0, 20))], str(b), 16)
    body += tag(*[u + v for u, v in zip(mid(Cp, Pp), (-26, 0))], str(c), 16) + tag(*[u + v for u, v in zip(mid(Pp, D), (26, 0))], "x", 16)
    for nm, pt, dx, dy in (("A", A, -18, 4), ("B", B, 18, 4), ("C", Cp, 0, -14), ("D", D, 0, 26), ("P", Pp, 18, -8)):
        body += T(pt[0] + dx, pt[1] + dy + 6, nm, 20)
    fig = wrap(560, 285, body, "Dos cuerdas que se cortan en el interior")
    stem = f"En la circunferencia, las cuerdas AB y CD se cortan en P, con AP = {a}, PB = {b} y CP = {c}. ¿Cuál es el valor de x = PD?"
    ans = str(x)
    alts = [a + b - c, F(a * b, c + 1) if False else a * b, F(a + b, c), c * (a + b) // max(a, 1), a * c // max(b, 1) + 1, x + 1, x - 1 if x > 1 else x + 2]
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, f"Teorema de las cuerdas: AP·PB = CP·PD, luego x = {a}·{b}/{c} = {x}.")


TRI = [(6, 4, 9), (4, 2, 8), (6, 3, 12), (10, 5, 20), (12, 9, 16), (3, 1, 9), (10, 4, 25), (6, 2, 18), (8, 4, 16), (15, 9, 25), (9, 3, 27), (12, 8, 18)]


def t_secant(r, l):
    t, a, m = r.choice(TRI)
    b = m - a
    O = (150, 140)
    rad = 90
    Pp = (500, 140)
    d = Pp[0] - O[0]
    phi = math.acos(rad / d)
    T_ = (O[0] + rad * math.cos(phi), O[1] - rad * math.sin(phi))
    A_, B_ = (O[0] + rad, 140), (O[0] - rad, 140)
    body = f'<circle cx="{O[0]}" cy="{O[1]}" r="{rad}" fill="#EFF6FF" stroke="{NAVY}" stroke-width="4"/>'
    body += L(*Pp, *T_, ACC, 3.5) + L(*Pp, *B_, INK, 3.5)
    for pt in (Pp, T_, A_, B_):
        body += C(pt[0], pt[1], 5, INK, INK, 1)
    ask = r.choice(["t", "b"])
    body += tag((Pp[0] + T_[0]) / 2 + 14, (Pp[1] + T_[1]) / 2 - 12, "x" if ask == "t" else str(t), 16) + tag((Pp[0] + A_[0]) / 2, 168, str(a), 16)
    body += tag(150, 168, "x" if ask == "b" else str(b), 16)
    for nm, pt, dx, dy in (("P", Pp, 18, 4), ("T", T_, 0, -14), ("A", A_, 14, 22), ("B", B_, -16, 4)):
        body += T(pt[0] + dx, pt[1] + dy + 6, nm, 20)
    fig = wrap(560, 250, body, "Tangente y secante desde un punto exterior")
    if ask == "t":
        stem = f"Desde el punto exterior P se trazan la tangente PT y la secante PAB a una circunferencia, con PA = {a} y AB = {b}. ¿Cuánto mide PT = x?"
        ans, alts = str(t), [a + b, a * b, m // 2, t + 1, t - 1 if t > 2 else t + 3, a + t]
        ex = f"PT² = PA·PB = {a}·{m} = {t * t}, luego PT = {t}."
    else:
        stem = f"Desde el punto exterior P se trazan la tangente PT y la secante PAB a una circunferencia, con PT = {t} y PA = {a}. ¿Cuánto mide AB = x?"
        ans, alts = str(b), [m, t * t // a if False else t - a, t * t // 2, a * t, b + 2, F(t * t, a + 1)]
        ex = f"PT² = PA·PB: {t * t} = {a}·PB, luego PB = {m} y AB = {m} − {a} = {b}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def sphere_fig(lab):
    body = f'<circle cx="280" cy="120" r="90" fill="#DBEAFE" stroke="{NAVY}" stroke-width="4"/>'
    body += f'<ellipse cx="280" cy="120" rx="90" ry="26" fill="none" stroke="{NAVY}" stroke-width="2.5" stroke-dasharray="7 6"/>'
    body += L(280, 120, 370, 120, ACC, 4) + C(280, 120, 5, INK, INK, 1) + tag(325, 98, lab, 17)
    return wrap(560, 240, body, "Esfera con su radio")


def t_sphere(r, l):
    rad = r.choice([3, 6, 9, 12])
    use_d = r.random() < 0.5
    D = 2 * rad
    what = r.choice(["volumen", "área de su superficie"])
    lab = f"D = {D} cm" if use_d else f"r = {rad} cm"
    stem = f"Una esfera de {'diámetro ' + str(D) if use_d else 'radio ' + str(rad)} cm. ¿Qué expresión representa su {what}?"
    if what == "volumen":
        ans = f"(4/3)·π·{rad}³ cm³"
        alts = [f"(4/3)·π·{D}³ cm³", f"4·π·{rad}² cm²".replace("cm²", "cm³"), f"(4/3)·π·{rad}² cm³", f"(1/3)·π·{rad}³ cm³", f"(4/3)·π·{rad}³ cm²"]
    else:
        ans = f"4·π·{rad}² cm²"
        alts = [f"4·π·{D}² cm²", f"(4/3)·π·{rad}³ cm²", f"2·π·{rad}² cm²", f"4·π·{rad}³ cm²", f"π·{rad}² cm²"]
    return make(stem, sphere_fig(lab), ans, uniq(ans, alts)[:4], Q_MOD, "V = (4/3)πr³ y A = 4πr², con r igual a la mitad del diámetro.")


def t_sphere_arg(r, l):
    k = r.choice([2, 3, 4])
    stem = f"El radio de una esfera se multiplica por {k}. ¿Cómo cambian el área de su superficie y su volumen?"
    ans = f"El área se multiplica por {k * k} y el volumen por {k ** 3}"
    alts = [f"El área se multiplica por {k} y el volumen por {k}", f"El área se multiplica por {k ** 3} y el volumen por {k * k}", f"El área se multiplica por {k * k} y el volumen por {k * k}", f"El área se multiplica por {k} y el volumen por {k * k}"]
    return make(stem, sphere_fig(f"r → {k}r"), ans, alts, Q_ARG, "El área es proporcional a r² y el volumen a r³.")


def t_rects(r, l):
    kind = r.choice(["par", "perp", "sec", "sec"])
    m1 = r.choice([1, 2, 3, -1, -2, -3, F(1, 2), F(-1, 2)])
    if kind == "par":
        m2 = m1
    elif kind == "perp":
        m2 = -1 / F(m1)
    else:
        m2 = r.choice([x for x in (1, 2, 3, -1, -2, F(1, 2), F(-1, 2), F(1, 3)) if x != m1 and x != -1 / F(m1)])
    n1, n2 = r.randint(-3, 3), r.randint(-3, 3)
    if kind == "par" and n1 == n2:
        n2 += 2
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    p.curve(lambda x: float(m1) * x + n1, -6, 6, ACC, 4.5)
    p.curve(lambda x: float(m2) * x + n2, -6, 6, NAVY, 4.5)
    fig = p.svg("Dos rectas en el plano cartesiano")

    def eq(m, n):
        ms = "x" if m == 1 else "−x" if m == -1 else f"({fs(F(m))})x"
        return f"y = {ms} {'+' if n >= 0 else '−'} {abs(n)}"
    stem = f"Las rectas L₁: {eq(m1, n1)} y L₂: {eq(m2, n2)} se representan en el plano. ¿Cuál es su posición relativa?"
    names = {"par": "Paralelas", "perp": "Perpendiculares", "sec": "Secantes no perpendiculares"}
    ans = names[kind]
    alts = [v for k_, v in names.items() if k_ != kind] + ["Coincidentes", "No se puede determinar"]
    return make(stem, fig, ans, alts, Q_REP, "Paralelas: igual pendiente; perpendiculares: producto de pendientes −1; si no, secantes.")


# ================================================================ Funciones seno y coseno
def _sin(t):
    d = {F(0): F(0), F(1, 6): F(1, 2), F(1, 2): F(1), F(5, 6): F(1, 2), F(1): F(0), F(7, 6): F(-1, 2), F(3, 2): F(-1), F(11, 6): F(-1, 2), F(2): F(0)}
    return d.get(F(t) % 2 if F(t) % 2 else F(0)) if False else d.get(F(t) % 2 if F(t) % 2 != 0 else F(0))


def _cos(t):
    d = {F(0): F(1), F(1, 3): F(1, 2), F(1, 2): F(0), F(2, 3): F(-1, 2), F(1): F(-1), F(4, 3): F(-1, 2), F(3, 2): F(0), F(5, 3): F(1, 2)}
    return d.get(F(t) % 2)


def pistr(t):
    t = F(t)
    if t == 0: return "0"
    num = "π" if t.numerator == 1 else f"{t.numerator}π"
    return num if t.denominator == 1 else f"{num}/{t.denominator}"


SIN_ANG = [F(0), F(1, 6), F(1, 2), F(5, 6), F(1), F(7, 6), F(3, 2), F(11, 6)]


def t_sin_value(r, l):
    theta = r.choice(SIN_ANG)
    phi = r.choice([F(1, 6), F(1, 3), F(1, 2), F(1), F(3, 2)])
    x0 = (theta - phi) % 2
    if x0 == theta or _sin(x0) is None and l == 0:
        pass
    a = r.choice([2, 3, 4, 5, 6])
    c = r.choice([-2, -1, 0, 1, 2, 3]) if l else 0
    s = _sin(theta)
    val = a * s + c
    def sh(v): return fs(v)
    fx = f"f(x) = {a} sen(x + {pistr(phi)})" + (f" {'+' if c > 0 else '−'} {abs(c)}" if c else "")
    fx = fx.replace("x + 0", "x")
    xs = pistr(x0) if x0 != 0 else "0"
    stem = f"Considera la función f definida por {fx}. ¿Cuál es el valor de f({xs})?"
    ans = sh(val)
    cs = _cos(theta)
    alts = [a * cs + c if cs is not None else None, a * s, -a * s + c, val + a, val - a if val - a != val else None, F(a * s + c) / 2 if False else val + 1, a * (_sin(x0) or 0) + c if _sin(x0) is not None else None]
    alts = [x for x in alts if x is not None]
    fig = card(["Función:", fx.replace("f(x) = ", "f(x) = "), f"Evaluar en x = {xs}"], 150, 20)
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts + [val + 2, val - 2])), Q_RES, f"x + {pistr(phi)} = {pistr(theta)}, y sen({pistr(theta)}) = {fs(s)}: f = {ans}.")


def _form(A, C, fn="sen"):
    s = "" if A == 1 else "−" if A == -1 else str(A) + " "
    if A in (1, -1): s = ("" if A == 1 else "−")
    body = f"{s}{fn}(x)".replace("  ", " ")
    if A not in (1, -1): body = f"{A} {fn}(x)"
    return f"f(x) = {body}" + (f" {'+' if C > 0 else '−'} {abs(C)}" if C else "")


def t_sin_graph(r, l):
    A = r.choice([1, 2, 3])
    C = r.choice([0, 1, -1, 2]) if l else r.choice([0, 1])
    fn = r.choice(["sen", "cos"])
    p = Plot(560, 300, 0, 2, -4, 5)
    p.axes(0.5, 1)
    g = (lambda x: A * math.sin(math.pi * x) + C) if fn == "sen" else (lambda x: A * math.cos(math.pi * x) + C)
    p.curve(g, 0, 2, ACC, 4.5)
    fig = p.svg("Gráfica de una función trigonométrica").replace("</svg>", tag(470, 22, "x en múltiplos de π", 15) + "</svg>")
    ans = _form(A, C, fn).replace("−", "-").replace("-", "−")
    other = "cos" if fn == "sen" else "sen"
    alts = [_form(A, C, other), _form(A, -C if C else 1, fn), _form(A + 1, C, fn), _form(-A, C, fn), _form(A, C + 1, fn)]
    alts = [a for a in dict.fromkeys(alts) if a != ans]
    return make("¿Cuál de las siguientes funciones tiene la gráfica mostrada (x en radianes)?", fig, ans, alts[:4], Q_REP, "Se leen la amplitud (distancia máx − mín)/2, la línea media y el valor en x = 0 para distinguir seno de coseno.")


def t_period(r, l):
    k = r.choice([4, 6, 8, 12])
    a = r.choice([1, 2, 3, 4])
    c = r.choice([2, 3, 4, 5, 6]) + a
    ctx = r.choice([("La altura de la marea", "h", "metros", "horas"), ("La temperatura de una cámara", "T", "°C", "horas"), ("La posición de un péndulo", "y", "cm", "segundos")])
    kind = r.choice(["period", "first_max", "max"])
    fx = f"{ctx[1]}(t) = {a} sen(πt/{k}) + {c}"
    fig = card(["Modelo con t en " + ctx[3] + ":", fx, "t ≥ 0"], 150, 19)
    if kind == "period":
        stem = f"{ctx[0]} se modela con {fx} ({ctx[2]}), con t en {ctx[3]}. ¿Cuánto dura un ciclo completo?"
        ans = f"{2 * k} {ctx[3]}"
        alts = [f"{k} {ctx[3]}", f"{4 * k} {ctx[3]}", f"{k // 2} {ctx[3]}", f"{2 * k + 2} {ctx[3]}", f"{a} {ctx[3]}"]
        ex = f"El período es 2π/(π/{k}) = {2 * k}."
    elif kind == "first_max":
        stem = f"{ctx[0]} se modela con {fx} ({ctx[2]}), con t en {ctx[3]}. ¿En qué instante se alcanza el primer máximo?"
        ans = f"t = {k // 2} {ctx[3]}"
        alts = [f"t = {k} {ctx[3]}", f"t = {2 * k} {ctx[3]}", f"t = {k // 4} {ctx[3]}", f"t = 0 {ctx[3]}", f"t = {k + k // 2} {ctx[3]}"]
        ex = f"El seno vale 1 cuando πt/{k} = π/2, es decir t = {k // 2}."
    else:
        stem = f"{ctx[0]} se modela con {fx} ({ctx[2]}), con t en {ctx[3]}. ¿Cuál es el valor máximo que alcanza?"
        ans = f"{a + c} {ctx[2]}"
        alts = [f"{c} {ctx[2]}", f"{a} {ctx[2]}", f"{a * c} {ctx[2]}", f"{c - a} {ctx[2]}", f"{a + c + 1} {ctx[2]}"]
        ex = f"El máximo del seno es 1: {a}·1 + {c} = {a + c}."
    return make(stem, fig, ans, uniq(ans, alts)[:4], Q_MOD, ex)


TT = ["Para todo x, −1 ≤ sen(x) ≤ 1", "La función coseno cumple cos(−x) = cos(x)", "El período de sen(2x) es π", "sen(x + 2π) = sen(x) para todo x", "La amplitud de 3 sen(x) + 1 es 3", "sen(π − x) = sen(x) para todo x"]
FT = ["El período de sen(2x) es 4π", "sen(2x) = 2 sen(x) para todo x", "La función seno cumple sen(−x) = sen(x)", "cos(x + π) = cos(x) para todo x", "El valor máximo de 3 sen(x) + 1 es 3", "La amplitud de sen(3x) es 3"]


def t_trig_arg(r, l):
    p = Plot(560, 260, 0, 2, -1.5, 1.5)
    p.axes(0.5, 0.5)
    p.curve(lambda x: math.sin(math.pi * x), 0, 2, ACC, 4.5)
    p.curve(lambda x: math.cos(math.pi * x), 0, 2, NAVY, 4.5)
    fig = p.svg("Gráficas de seno y coseno").replace("</svg>", tag(470, 22, "x en múltiplos de π", 15) + "</svg>")
    stem = r.choice(["Sobre las funciones seno y coseno, ¿cuál de las siguientes afirmaciones es verdadera?", "Considera las gráficas de sen(x) y cos(x). ¿Cuál afirmación es verdadera?"])
    return make(stem, fig, r.choice(TT), r.sample(FT, 4), Q_ARG, "Propiedades: acotadas entre −1 y 1, periódicas de período 2π; el seno es impar y el coseno es par.")


# ================================================================ Matemática financiera, sistemas 2x2 y suficiencia de datos
def t_credit(r, l):
    P_ = r.choice([500, 800, 1000, 1200, 1500, 2000]) * 1000
    i = r.choice([1, 2, 3, 4])
    cuota = r.choice([100, 150, 200, 250, 300]) * 1000
    g = f"{1 + i / 100:.2f}".replace(".", ",")
    fig = card([f"Crédito de consumo: ${n_(P_)}", f"Interés: {i}% mensual sobre el saldo", f"Cuota mensual: ${n_(cuota)} (al fin de mes)"], 160, 19)
    stem = "Una persona paga el crédito con cuotas mensuales iguales, al final de cada mes, y el interés se aplica sobre el saldo al inicio del mes. ¿Qué expresión representa la deuda después de pagar la segunda cuota?"
    ans = f"({n_(P_)}·{g} − {n_(cuota)})·{g} − {n_(cuota)}"
    alts = [f"({n_(P_)} − {n_(cuota)})·{g} − {n_(cuota)}", f"{n_(P_)}·{g}² − {n_(cuota)}", f"{n_(P_)}·{g}·{g} − 2·{n_(cuota)}·{g}".replace("·" + g + "·" + g, "·" + g + "²"), f"{n_(P_)}·{g}² − 2·{n_(cuota)}·{g}", f"{n_(P_)} + {n_(cuota)}·{g}²"]
    return make(stem, fig, ans, uniq(ans, alts)[:4], Q_MOD, "Cada mes: saldo·(1 + i) − cuota. Se aplica dos veces.")


def t_afp(r, l):
    S = r.choice([600, 800, 900, 1000, 1200, 1500]) * 1000
    anios = r.randint(2, 6)
    pct = 10
    total = S * pct // 100 * 12 * anios
    fig = card([f"Sueldo mensual imponible: ${n_(S)}", f"Cotización obligatoria: {pct}% del sueldo", f"Tiempo: {anios} años (sin reajustes ni rentabilidad)"], 160, 19)
    stem = "En un sistema de ahorro previsional se destina un porcentaje fijo del sueldo cada mes. ¿Cuánto se habrá acumulado en total?"
    ans = f"${n_(total)}"
    alts = [f"${n_(S * pct // 100 * anios)}", f"${n_(S * 12 * anios)}", f"${n_(S * pct * 12 * anios)}", f"${n_(S * pct // 100 * 12)}", f"${n_(total + S)}"]
    return make(stem, fig, ans, uniq(ans, alts)[:4], Q_RES, f"{pct}% de {n_(S)} = {n_(S * pct // 100)} al mes; en {anios * 12} meses: {n_(total)}.")


def t_system_cases(r, l):
    kind = r.choice(["uni", "uni", "par", "same"])
    m1, m2 = r.sample([-2, -1, 1, 2, 3], 2)
    x0, y0 = r.randint(-3, 3), r.randint(-3, 3)
    n1 = y0 - m1 * x0
    if kind == "uni":
        n2 = y0 - m2 * x0
        mm2 = m2
    elif kind == "par":
        mm2, n2 = m1, n1 + r.choice([-3, -2, 2, 3])
    else:
        mm2, n2 = m1, n1
    if max(abs(n1), abs(n2)) > 5:
        raise Reject
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    p.curve(lambda x: m1 * x + n1, -6, 6, ACC, 4.5)
    if kind == "same":
        p.curve(lambda x: mm2 * x + n2, -6, 6, NAVY, 2.5)
    else:
        p.curve(lambda x: mm2 * x + n2, -6, 6, NAVY, 4.5)
    fig = p.svg("Gráficas de las dos ecuaciones de un sistema 2×2")
    stem = "Las dos ecuaciones de un sistema lineal 2×2 se grafican en el plano cartesiano. ¿Cuál afirmación describe correctamente su conjunto solución?"
    xs, ys = x0, y0
    ans = {"uni": f"Única solución: ({xs}, {ys})", "par": "Sin solución", "same": "Infinitas soluciones"}[kind]
    ans = ans.replace("-", "−")
    alts = [f"Única solución: ({ys}, {xs})", f"Única solución: ({-xs}, {ys})", f"Única solución: ({xs}, {-ys})", "Sin solución", "Infinitas soluciones"]
    alts = [a.replace("-", "−") for a in alts if a.replace("-", "−") != ans]
    if kind != "uni":
        alts = [f"Única solución: ({xs}, {ys})", f"Única solución: ({ys}, {xs})", f"Única solución: ({-xs}, {ys})"] + [a for a in ("Sin solución", "Infinitas soluciones") if a != ans]
        alts = [a.replace("-", "−") for a in alts]
    return make(stem, fig, ans, alts[:4], Q_REP, "Rectas que se cortan: una solución; paralelas: ninguna; coincidentes: infinitas.")


def t_system_k(r, l):
    a, b = r.choice([(2, 1), (1, 1), (3, 1), (2, 3), (1, 2), (3, 2)])
    d = r.choice([2, 4, 6])
    if (a * d) % b:
        raise Reject
    k = a * d // b
    c = r.randint(2, 9)
    e_par = c * d // b + r.choice([1, 2, -1, 3]) if (c * d) % b == 0 else c * d // b + 1
    no_sol = r.random() < 0.5
    e = e_par if no_sol else c * d // b
    if (c * d) % b:
        raise Reject
    fig = card([f"{a}x + {b}y = {c}", f"kx + {d}y = {e}"], 130, 22)
    stem = f"Considera el sistema de ecuaciones {'' if True else ''}con k un número real. ¿Para qué valor de k el sistema {'no tiene solución' if no_sol else 'tiene infinitas soluciones'}?"
    ans = str(k)
    alts = [F(d, b), a * d, F(a, d), k + 1, k - 1 if k > 1 else k + 2, b * d, F(a * b, d)]
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_ARG,
                f"Las pendientes deben ser iguales: {a}/{b} = k/{d}, luego k = {k}; " + ("con términos independientes no proporcionales no hay solución." if no_sol else "con términos independientes proporcionales hay infinitas soluciones."))


SUF = ["(1) por sí sola", "(2) por sí sola", "Ambas juntas, (1) y (2)", "Cada una por sí sola, (1) ó (2)", "Se requiere información adicional"]


def _rank_ok(eqs, goal):
    """goal=(gx,gy): ¿se determina gx·x+gy·y con las ecuaciones eqs (a,b,c)?"""
    rows = [(F(a), F(b)) for a, b, c in eqs]
    if not rows:
        return False
    def rank(rs):
        rs = [list(x) for x in rs]
        rk = 0
        for col in (0, 1):
            piv = next((i for i in range(rk, len(rs)) if rs[i][col] != 0), None)
            if piv is None: continue
            rs[rk], rs[piv] = rs[piv], rs[rk]
            for i in range(len(rs)):
                if i != rk and rs[i][col] != 0:
                    f = rs[i][col] / rs[rk][col]
                    rs[i] = [u - f * v for u, v in zip(rs[i], rs[rk])]
            rk += 1
        return rk
    return rank(rows) == rank(rows + [(F(goal[0]), F(goal[1]))])


def t_sufic(r, l):
    goal = r.choice([(1, 0), (0, 1), (1, 1), (1, -1)])
    gtxt = {(1, 0): "x", (0, 1): "y", (1, 1): "x + y", (1, -1): "x − y"}[goal]
    x0, y0 = r.randint(1, 9), r.randint(1, 9)
    def eq():
        a, b = r.randint(-3, 4), r.randint(-3, 4)
        if a == 0 and b == 0: raise Reject
        return (a, b, a * x0 + b * y0)
    e0 = eq() if r.random() < 0.5 else None
    e1, e2 = eq(), eq()
    base = [e0] if e0 else []
    s1, s2, both = _rank_ok(base + [e1], goal), _rank_ok(base + [e2], goal), _rank_ok(base + [e1, e2], goal)
    if s1 and s2: idx = 3
    elif s1: idx = 0
    elif s2: idx = 1
    elif both: idx = 2
    else: idx = 4
    def t(e):
        a, b, c = e
        parts = []
        if a: parts.append(f"{'' if abs(a) == 1 else abs(a)}x".replace("", "") if False else (("−" if a < 0 else "") + ("" if abs(a) == 1 else str(abs(a))) + "x"))
        if b:
            sgn = ("−" if b < 0 else "+") if parts else ("−" if b < 0 else "")
            parts.append((sgn + " " if parts else sgn) + ("" if abs(b) == 1 else str(abs(b))) + "y")
        return " ".join(parts) + f" = {c}"
    lines = ["¿Cuál es el valor de " + gtxt + "?"]
    if e0: lines.append("Se sabe que " + t(e0))
    lines += ["(1) " + t(e1), "(2) " + t(e2)]
    lines = [x.replace("-", "−") for x in lines]
    fig = card(lines, 60 + 42 * len(lines), 19)
    stem = f"Suficiencia de datos: ¿se puede determinar el valor de {gtxt}? Elige la opción según las afirmaciones (1) y (2) de la figura."
    ans = SUF[idx]
    return make(stem, fig, ans, [s for s in SUF if s != ans], Q_ARG, "Se comprueba si cada afirmación, sola o junta, determina un único valor de la expresión pedida.")


G_PROB = {Q_RES: [t_normal_table, t_normal_std, t_binom_calc], Q_MOD: [t_binom_expr], Q_REP: [t_binom_bars], Q_ARG: [t_normal_arg]}
G_CIRC = {Q_RES: [t_inscribed, t_chords, t_secant], Q_MOD: [t_sphere], Q_REP: [t_rects], Q_ARG: [t_sphere_arg]}
G_TRIG = {Q_RES: [t_sin_value], Q_MOD: [t_period], Q_REP: [t_sin_graph], Q_ARG: [t_trig_arg]}
G_FIN = {Q_RES: [t_afp], Q_MOD: [t_credit], Q_REP: [t_system_cases], Q_ARG: [t_system_k, t_sufic]}
GROUPS = {101: G_PROB, 102: G_CIRC, 103: G_TRIG, 104: G_FIN}
