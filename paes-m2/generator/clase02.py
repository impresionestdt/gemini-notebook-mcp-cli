"""Clase 2 · Logaritmos: concepto, operatoria y propiedades."""
from fractions import Fraction as F
from functools import reduce
from math import gcd, log, log10
from svgkit import *
from common import Reject, make as _make


def make(stem, svg, correct, dists, skill, expl):
    m = lambda t: t.replace('-', '−')
    return _make(m(stem), m(svg) if False else svg, m(correct), [m(d) for d in dists], skill, m(expl))

Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO = ("Resolver problemas", "Modelar", "Representar",
                                     "Argumentar", "Aplicar procedimientos")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def lg(b):
    return "log" + str(b).translate(SUB)


def dec(x):
    return f"{x:.2f}".replace(".", ",")


def fs(x):
    x = F(x)
    return (str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}").replace("-", "−")


def pick4(correct, cands):
    out = []
    for c in cands:
        if c != correct and c not in out:
            out.append(c)
        if len(out) == 4:
            return out
    raise Reject


def lc(terms):
    """Combinación lineal de símbolos ('a','b','' = constante)."""
    terms = [(F(c), s) for c, s in terms if c != 0]
    if not terms:
        return "0"
    d = reduce(lambda x, y: x * y // gcd(x, y), [c.denominator for c, _ in terms])
    nums = [int(c * d) for c, _ in terms]
    g = reduce(gcd, [abs(x) for x in nums] + [d])
    nums = [x // g for x in nums]
    d //= g
    out = []
    for i, (x, (_, s)) in enumerate(zip(nums, terms)):
        core = (str(abs(x)) if (abs(x) != 1 or s == "") else "") + s
        out.append(("−" if x < 0 else "") + core if i == 0 else (" − " if x < 0 else " + ") + core)
    body = "".join(out)
    return body if d == 1 else (f"{body}/{d}" if len(terms) == 1 else f"({body})/{d}")


# ---------------------------------------------------------------- figuras
class Plot:
    def __init__(s, w, h, x0, x1, y0, y1, ml=44, mb=30, mt=14, mr=14):
        s.w, s.h, s.x0, s.x1, s.y0, s.y1, s.ml, s.mb, s.mt, s.mr = w, h, x0, x1, y0, y1, ml, mb, mt, mr
        s.parts = []

    def X(s, x): return s.ml + (x - s.x0) / (s.x1 - s.x0) * (s.w - s.ml - s.mr)
    def Y(s, y): return s.h - s.mb - (y - s.y0) / (s.y1 - s.y0) * (s.h - s.mb - s.mt)

    def axes(s, sx, sy):
        g = ""
        x = int(s.x0 // sx * sx)
        while x <= s.x1 + 1e-9:
            if x >= s.x0:
                g += L(s.X(x), s.Y(s.y0), s.X(x), s.Y(s.y1), "#CBD5E1", 1) + T(s.X(x), s.h - 8, fs(x), 14)
            x += sx
        y = int(s.y0 // sy * sy)
        while y <= s.y1 + 1e-9:
            if y >= s.y0:
                g += L(s.X(s.x0), s.Y(y), s.X(s.x1), s.Y(y), "#CBD5E1", 1) + T(s.ml - 8, s.Y(y) + 5, fs(y), 14, "end")
            y += sy
        g += L(s.X(s.x0), s.Y(0), s.X(s.x1), s.Y(0), INK, 2.5) + L(s.X(0), s.Y(s.y0), s.X(0), s.Y(s.y1), INK, 2.5)
        s.parts.append(g)

    def curve(s, f, xa, xb, color=ACC, sw=4, n=300):
        segs, cur = [], []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError, OverflowError):
                y = None
            if y is not None and s.y0 <= y <= s.y1:
                cur.append((s.X(x), s.Y(y)))
            elif cur:
                segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            if len(sg) > 1:
                s.parts.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (color, sw, " ".join(f"{a:.1f},{b:.1f}" for a, b in sg)))

    def pt(s, x, y, label=None, dx=0, dy=-26):
        s.parts.append(C(s.X(x), s.Y(y), 7, ACC))
        if label: s.parts.append(tag(s.X(x) + dx, s.Y(y) + dy, label.replace("-", "−"), 16))

    def vline(s, x, dash="8 6"): s.parts.append(L(s.X(x), s.Y(s.y0), s.X(x), s.Y(s.y1), NAVY, 2.5, dash))
    def hline(s, y, dash="8 6"): s.parts.append(L(s.X(s.x0), s.Y(y), s.X(s.x1), s.Y(y), NAVY, 2.5, dash))
    def svg(s, label): return wrap(s.w, s.h, "".join(s.parts), label)


def pow_strip(b, cells, final):
    """Cajas con las primeras potencias y una última caja con la incógnita."""
    n = len(cells) + 1
    w = 96
    gap = (520 - n * w) / (n - 1)
    body = ""
    for i, c in enumerate(cells + [final]):
        x = 20 + i * (w + gap)
        last = i == n - 1
        body += R(x, 60, w, 70, FILL2 if last else FILL) + T(x + w / 2, 102, c, 19 if len(c) < 7 else 15)
        if i:
            body += L(x - gap + 2, 95, x - 2, 95, ACC, 3)
    return wrap(560, 190, body + tag(280, 30, f"Cada paso multiplica por {b}", 16), "Sucesión de potencias")


def card(lines, h=200, size=22):
    body = R(30, 25, 500, h - 50, "#F1F5F9")
    n = len(lines)
    for i, t in enumerate(lines):
        body += T(280, 25 + (h - 50) * (i + 1) / (n + 1) + 7, t, size)
    return wrap(560, h, body, " ".join(lines))


# ---------------------------------------------------------------- Resolver
def t_pow_eq(r, l):
    b = r.choice([2, 3, 4, 5, 10])
    k = r.randint(2, 6 if b < 5 else 4)
    if l == 0:
        N, ans, stem = b ** k, F(k), f"¿Para qué valor de x se cumple {b}^x = {b**k}?"
        ex = f"{b**k} = {b}^{k}, entonces x = {k} (x = {lg(b)} {b**k})."
    elif l == 1:
        c = r.choice([2, 3, 5])
        stem, ans = f"¿Para qué valor de x se cumple {c}·{b}^x = {c * b**k}?", F(k)
        ex = f"Se divide por {c}: {b}^x = {b**k}, luego x = {k}."
    else:
        m = r.choice([2, 3])
        j = r.randint(1, 4)
        kk = m * j + 1  # b^(mx-1) = b^kk
        stem, ans = f"¿Para qué valor de x se cumple {b}^({m}x − 1) = {b**kk}?", F(kk + 1, m)
        ex = f"{m}x − 1 = {kk}, entonces x = {fs(ans)}."
    k0 = int(ans) if ans.denominator == 1 else ans
    cands = [fs(ans + 1), fs(ans - 1), fs(F(b ** (k if l < 2 else kk), b)), fs(ans * 2), fs(b ** k if l < 2 else b ** kk), fs(F(1, ans) if ans else 1)]
    cands = [c for c in cands if c != fs(ans)]
    if l == 2:
        cands = [fs(F(kk, m)), fs(kk), fs(F(kk - 1, m)), fs(kk + 1), fs(F(kk + 2, m))] + cands
    d = pick4(fs(ans), cands)
    cells = [f"{b}^0 = 1", f"{b}^1 = {b}", f"{b}^2 = {b*b}", f"{b}^3 = {b**3}"] if b < 10 else ["10^0 = 1", "10^1 = 10", "10^2 = 100", "10^3 = 1000"]
    return make(stem, pow_strip(b, cells, f"{b}^x"), fs(ans), d, Q_RES, ex)


def t_log_eq(r, l):
    if l == 0:
        b, k = r.choice([2, 3, 4, 5, 10]), r.randint(2, 4)
        ans, stem = b ** k, f"Resuelve la ecuación {lg(b)}(x) = {k}."
        cands = [b * k, k ** b, b ** k - 1, b ** k + b, k, (b ** k) // 2]
        f = lambda x: log(x, b)
        pl = Plot(560, 250, 0, b ** k * 1.3, -2, k + 1)
        pl.axes(max(1, round(b ** k / 6)), 1); pl.curve(f, 0.02, b ** k * 1.3); pl.hline(k); pl.pt(ans, k, f"x = ?", dy=-26)
        fig, ex = pl.svg("Gráfica de la función logaritmo"), f"{lg(b)}(x) = {k} equivale a x = {b}^{k} = {ans}."
    elif l == 1:
        b, k, c = r.choice([2, 3, 5]), r.randint(2, 3), r.randint(1, 6)
        ans, stem = b ** k - c, f"Resuelve la ecuación {lg(b)}(x + {c}) = {k}."
        cands = [b ** k + c, b * k - c, b ** k, k ** b - c, b ** k - c + 1, b ** k - 2 * c]
        pl = Plot(560, 250, -c - 1, b ** k, -2, k + 1)
        pl.axes(max(1, round(b ** k / 6)), 1); pl.vline(-c); pl.curve(lambda x: log(x + c, b), -c + 0.03, b ** k); pl.hline(k)
        fig, ex = pl.svg("Función logarítmica desplazada"), f"x + {c} = {b}^{k} = {b**k}, entonces x = {ans}."
    else:
        b = r.choice([2, 2, 3])
        i = r.randint(2, 4 if b == 2 else 2)
        j = r.randint(0, i - 1)
        x0, xm = b ** i, b ** j
        c, k = x0 - xm, i + j
        ans = x0
        stem = f"Resuelve {lg(b)}(x) + {lg(b)}(x − {c}) = {k}. ¿Cuál es el valor de x?"
        cands = [-xm, b ** k, x0 + c, c, xm, x0 - 1]
        fig = card([f"{lg(b)}(x) + {lg(b)}(x − {c}) = {k}", "Recuerda el dominio: x > " + str(c)])
        ex = f"x(x − {c}) = {b}^{k} = {b**k}; las raíces son {x0} y {-xm}, y solo {x0} está en el dominio."
    d = pick4(str(ans), [str(c) for c in cands])
    return make(stem, fig, str(ans), d, Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def scale_fig(vals, labels, top):
    body = ""
    for i, (v, lab) in enumerate(zip(vals, labels)):
        h = 150 * v / top
        x = 90 + i * 210
        body += R(x, 190 - h, 110, h, FILL2 if i else FILL) + tag(x + 55, 190 - h - 16, lab, 16)
    body += L(50, 190, 520, 190, INK, 3)
    return wrap(560, 230, body, "Barras comparativas")


def t_ph_richter(r, l):
    if l == 0:
        k = r.randint(2, 12)
        stem = f"Una solución tiene [H⁺] = 10^(−{k}) mol/L. Si pH = −log[H⁺], ¿cuál es su pH?"
        ans = str(k)
        cands = [str(14 - k), str(-k), str(k + 1), str(k - 1), f"10^{k}"]
        body = ""
        cols = ["#FCA5A5", "#FDE68A", "#BBF7D0", "#BFDBFE", "#DDD6FE"]
        for i in range(15):
            body += R(20 + i * 34.6, 70, 34.6, 50, cols[i * 5 // 15], INK, 1.5) + T(37 + i * 34.6, 152, str(i), 15)
        fig = wrap(560, 190, body + tag(280, 30, "Escala de pH", 18), "Escala de pH de 0 a 14")
        ex = f"pH = −log(10^(−{k})) = {k}."
    elif l == 1:
        k, c = r.randint(2, 9), r.choice([2, 3, 5])
        lgc = {2: 0.30, 3: 0.48, 5: 0.70}[c]
        stem = f"Una solución tiene [H⁺] = {c}·10^(−{k}) mol/L. Si log {c} = {dec(lgc)}, ¿cuál es su pH? (pH = −log[H⁺])"
        ans = dec(k - lgc)
        cands = [dec(k + lgc), dec(k), dec(lgc), dec(k - 2 * lgc), dec(k + 1 - lgc), dec(k - 1 + lgc)]
        fig = card([f"[H⁺] = {c}·10^(−{k})", f"log {c} = {dec(lgc)}", "pH = ?"], 210)
        ex = f"pH = −(log {c} − {k}) = {k} − {dec(lgc)} = {ans}."
    else:
        m2 = r.randint(2, 5)
        d = r.randint(1, 4)
        m1 = m2 + d
        stem = (f"La magnitud de un sismo es M = log(A/A₀). Un sismo tiene magnitud {m1} y otro {m2}. "
                f"¿Cuántas veces mayor es la amplitud del primero que la del segundo?")
        ans = f"10^{d} veces"
        cands = [f"{d} veces", f"{10 * d} veces", f"10^{m1 + m2} veces", f"{round(m1 / m2, 1)} veces".replace(".", ","), f"10^{m1 - m2 + 1} veces", f"10^{m1} veces"]
        fig = scale_fig([m1, m2], [f"M = {m1}", f"M = {m2}"], m1)
        ex = f"A₁/A₂ = 10^({m1}−{m2}) = 10^{d}."
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


def t_growth(r, l):
    if l == 0:
        b, T, j = 2, r.randint(2, 9), r.randint(3, 8)
        stem = f"Un cultivo se duplica cada {T} horas. Si parte con 1 unidad, ¿en cuántas horas llegará a {2**j} unidades?"
        unit, ans = "horas", j * T
    elif l == 1:
        b, T, j = r.choice([2, 3, 4, 5]), r.randint(2, 6), r.randint(2, 5)
        stem = f"Una población se multiplica por {b} cada {T} años. Si hoy hay P₀ habitantes, ¿en cuántos años habrá {b**j}·P₀?"
        unit, ans = "años", j * T
    else:
        b, T, j = 2, r.randint(2, 12), r.randint(3, 7)
        M = r.choice([64, 96, 160, 320])
        stem = (f"Una sustancia tiene una vida media de {T} días (cada {T} días queda la mitad). "
                f"Si hay {M * 2**j} g, ¿en cuántos días quedarán {M} g?")
        unit, ans = "días", j * T
    cands = [T * b ** j, j + T, T * b, T * (j + 1), T * (j - 1), b * j, T * j * b]
    cands = [f"{c} {unit}" for c in cands if c != ans and c > 0]
    correct = f"{ans} {unit}"
    cells = ["1", str(b), str(b * b), str(b ** 3)] if l < 2 else [str(M * 2 ** j), str(M * 2 ** (j - 1)), str(M * 2 ** (j - 2)), "…"]
    fig = pow_strip(b, cells, "?" if l < 2 else str(M))
    if l == 2:
        fig = fig.replace("Cada paso multiplica por 2", f"Cada {T} días queda la mitad")
    return make(stem, fig, correct, pick4(correct, cands), Q_MOD, f"Se necesitan {j} períodos de {T} {unit}: {j}·{T} = {ans} {unit}.")


# ---------------------------------------------------------------- Representar
def t_graph_base(r, l):
    if l < 2:
        b, k = r.choice([2, 3, 4, 5]), r.choice([2, 3])
        neg = l == 1
        N = F(1, b ** k) if neg else F(b ** k)
        kk = -k if neg else k
        xmax = 1.3 if neg else float(N) * 1.25
        pl = Plot(560, 260, 0, xmax, -4 if neg else -2, 1 if neg else k + 1)
        pl.axes(0.25 if neg else max(1, round(float(N) / 6)), 1)
        pl.curve(lambda x: log(x, b), 0.004, xmax)
        pl.pt(float(N), kk, f"({fs(N)}, {kk})", dx=0 if not neg else 40, dy=-28 if not neg else -28)
        stem = f"La función f(x) = log_b(x) pasa por el punto ({fs(N)}, {kk}), como muestra el gráfico. ¿Cuál es el valor de b?"
        cands = [b + 1, b - 1, k, b * k, int(N * 1) if not neg else b ** k, 2 * b]
        cands = [str(c) for c in cands if c > 0]
        fig, ans = pl.svg("Gráfico de f(x) = log_b(x)"), str(b)
        ex = f"{kk} = log_b({fs(N)}) implica b^({kk}) = {fs(N)}, luego b = {b}."
    else:
        b, c = r.choice([2, 3, 4, 5]), r.randint(1, 4)
        right = r.random() < 0.5
        s = c if right else -c
        pl = Plot(560, 260, s - 3 if not right else s - 3, s + 8, -3, 3)
        pl.axes(1, 1)
        pl.vline(s)
        pl.curve(lambda x: log(x - s, b), s + 0.01, s + 8)
        pl.pt(s + 1, 0, f"({s + 1}, 0)", dy=26, dx=8); pl.pt(s + b, 1, f"({s + b}, 1)", dy=-28)
        sg = "−" if right else "+"
        ans = f"f(x) = {lg(b)}(x {sg} {c})"
        cands = [f"f(x) = {lg(b)}(x {'+' if right else '−'} {c})", f"f(x) = {lg(b)}(x) {sg} {c}", f"f(x) = {lg(b)}(x) {'+' if right else '−'} {c}",
                 f"f(x) = {lg(b)}({c}x)", f"f(x) = {lg(b + 1)}(x {sg} {c})"]
        stem = "El gráfico muestra la función f con su asíntota vertical (línea punteada). ¿Cuál es la ecuación de f?"
        fig, ex = pl.svg("Función logarítmica con asíntota vertical"), f"La asíntota es x = {s} y f({s + 1}) = 0, así que f(x) = {lg(b)}(x {sg} {c})."
    return make(stem, fig, ans, pick4(ans, cands), Q_REP, ex)


def t_inverse(r, l):
    b, p = r.choice([(2, -2), (2, -1), (2, 1), (2, 2), (2, 3), (3, -1), (3, 1), (4, -1), (4, 1), (5, 1), (2, 0), (3, 0)])
    q = F(b) ** p
    kind = r.choice("ABCD") if l else r.choice("ABC")
    pl = Plot(560, 300, -4, 8, -4, 8, mb=26)
    pl.axes(2, 2)
    pl.curve(lambda x: b ** x, -4, 8, ACC); pl.curve(lambda x: log(x, b), 0.001, 8, NAVY); pl.curve(lambda x: x, -4, 8, "#475569", 2.5)
    fp, fq = fs(p), fs(q)
    P_ = f"({fp}, {fq})"
    if kind == "A":
        pl.pt(p, float(q), f"P{P_}", dy=-26)
        stem = f"En el gráfico, la curva roja es y = {b}^x y la azul es y = {lg(b)}(x). El punto P{P_} está en y = {b}^x. ¿Qué punto está en y = {lg(b)}(x)?"
        ans, cands = f"({fq}, {fp})", [P_, f"({fs(-p)}, {fq})", f"({fq}, {fs(-p)})", f"({fs(-q)}, {fp})", f"({fs(1 / q)}, {fp})", f"({fq}, {fs(p + 1)})"]
        ex = f"Las funciones son inversas: si ({fp}, {fq}) está en {b}^x, entonces ({fq}, {fp}) está en {lg(b)}(x)."
    elif kind == "B":
        pl.pt(float(q), p, f"P({fq}, {fp})", dy=-26)
        stem = f"La curva roja es y = {b}^x y la azul es y = {lg(b)}(x). El punto P({fq}, {fp}) está en y = {lg(b)}(x). ¿Qué punto está en y = {b}^x?"
        ans, cands = P_, [f"({fq}, {fp})", f"({fs(-p)}, {fq})", f"({fp}, {fs(-q)})", f"({fs(1 / q)}, {fp})", f"({fp}, {fs(q + 1)})"]
        ex = f"El punto simétrico respecto de y = x es ({fp}, {fq})."
    elif kind == "C":
        pl.pt(p, float(q), f"P{P_}", dy=-26)
        stem = f"El punto P{P_} está en la curva roja y = {b}^x. ¿Cuál es el simétrico de P respecto de la recta y = x (línea gris)?"
        ans, cands = f"({fq}, {fp})", [P_, f"({fs(-q)}, {fs(-p)})", f"({fs(-p)}, {fs(-q)})", f"({fq}, {fs(-p)})", f"({fs(-q)}, {fp})"]
        ex = "La reflexión respecto de y = x intercambia las coordenadas."
    else:
        pl.pt(p, float(q), f"P{P_}", dy=-26)
        stem = f"El punto P{P_} pertenece a y = {b}^x (curva roja). ¿Cuánto vale {lg(b)}({fq})?"
        ans, cands = fp, [fq, fs(-p), fs(p + 1), fs(1 / q if q else 1), fs(p - 1), fs(p * 2)]
        ex = f"{b}^({fp}) = {fq}, entonces {lg(b)}({fq}) = {fp}."
    return make(stem, pl.svg("Funciones exponencial y logarítmica"), ans, pick4(ans, cands), Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
def t_domain(r, l):
    b = r.choice([2, 3, 4, 5, 10])
    c = r.randint(1, 12)
    if l == 0:
        s = r.choice([1, -1])
        expr = f"x {'−' if s > 0 else '+'} {c}"
        pts = [s * c]
        ans = f"x > {s * c}"
        cands = [f"x ≥ {s * c}", f"x < {s * c}", f"x ≠ {s * c}", f"x > {-s * c}", f"x ≤ {s * c}"]
    elif l == 1:
        expr, pts = f"{c} − x", [c]
        ans = f"x < {c}"
        cands = [f"x ≤ {c}", f"x > {c}", f"x ≠ {c}", f"x < {-c}", f"x ≥ {c}"]
    else:
        expr, pts = f"x² − {c*c}", [-c, c]
        ans = f"x < {-c} o x > {c}"
        cands = [f"−{c} < x < {c}", f"x > {c}", f"x ≠ {-c} y x ≠ {c}", f"x ≤ {-c} o x ≥ {c}", f"x < {-c}"]
    lo, hi = min(pts) - 4, max(pts) + 4
    sc = 500 / (hi - lo)
    body = L(30, 100, 530, 100, INK, 3)
    for v in range(lo, hi + 1):
        body += L(30 + (v - lo) * sc, 92, 30 + (v - lo) * sc, 108, INK, 2)
        if (v - lo) % max(1, (hi - lo) // 10) == 0:
            body += T(30 + (v - lo) * sc, 135, str(v).replace("-", "−"), 15)
    for p_ in pts:
        body += C(30 + (p_ - lo) * sc, 100, 8, WHITE, ACC, 4)
    fig = wrap(560, 170, body + tag(280, 40, f"{lg(b)}({expr})", 22), "Recta numérica con puntos críticos")
    return make(f"¿Para qué valores reales de x está definida la expresión {lg(b)}({expr})?", fig, ans, pick4(ans, cands), Q_ARG,
                f"El argumento del logaritmo debe ser positivo: {expr} > 0, lo que da {ans}.")


TRUE_S = [("{L}(x·y) = {L}(x) + {L}(y)"), ("{L}(x/y) = {L}(x) − {L}(y)"), ("{L}(x^n) = n·{L}(x)"), ("{L}(1) = 0"), ("{L}(b) = 1")]
FALSE_S = ["{L}(x + y) = {L}(x) + {L}(y)", "{L}(x·y) = {L}(x)·{L}(y)", "{L}(x/y) = {L}(x)/{L}(y)", "{L}(x^n) = ({L}(x))^n",
           "{L}(x − y) = {L}(x)/{L}(y)", "{L}(0) = 0", "{L}(x·y) = {L}(x) − {L}(y)", "{L}(x/y) = {L}(y) − {L}(x)", "{L}(1) = 1", "{L}(b) = 0"]


def t_props(r, l):
    b = r.choice([2, 3, 4, 5, 10, 7])
    L_ = lg(b)
    tsel = r.choice(TRUE_S)
    tsel = tsel.replace("(b)", f"({b})")
    ts = tsel.format(L=L_)
    fs_ = r.sample(FALSE_S, 4)
    fal = [f.format(L=L_) for f in fs_]
    if l == 0:
        stem, good, bad = "Sean x, y > 0. ¿Cuál de las siguientes igualdades es VERDADERA?", ts, fal
        ex = "Es una propiedad de los logaritmos: " + ts + "."
    else:
        allf = list(fal)
        stem = "Sean x, y > 0 e n real. ¿Cuál de las siguientes igualdades es FALSA?"
        f0 = fal[0]
        others = [t.format(L=L_).replace("(b)", f"({b})") for t in r.sample(TRUE_S, 4)]
        good, bad = f0, [o.replace("(b)", f"({b})") for o in others]
        ex = "No existe esa propiedad: " + f0 + " es falsa."
    good = good.replace("{L}", L_)
    body = (R(60, 40, 440, 60, "#F1F5F9") + T(280, 78, f"x, y > 0   ·   {b} > 0, {b} ≠ 1", 20)
            + R(60, 120, 130, 50, FILL) + T(125, 152, "x, y", 20) + L(190, 145, 230, 145, ACC, 4)
            + R(230, 120, 100, 50, FILL2) + T(280, 152, L_, 22) + L(330, 145, 370, 145, ACC, 4) + R(370, 120, 130, 50, FILL) + T(435, 152, "resultado", 18))
    bad = [x for x in bad if x != good][:4]
    if len(bad) < 4 or len(set(bad + [good])) != 5:
        raise Reject
    return make(stem, wrap(560, 200, body, "Máquina logaritmo"), good, bad, Q_ARG, ex)


def t_counter_log(r, l):
    eq = [(2, "2"), (3, "1,5"), (5, "1,25"), (6, "1,2"), (9, "1,125"), (11, "1,1"), (21, "1,05"), (4, "4/3"), (7, "7/6"), (8, "8/7"), (10, "10/9")]
    good_pairs = ["a = 3 y b = 3", "a = 2 y b = 5", "a = 4 y b = 6", "a = 5 y b = 10", "a = 7 y b = 2", "a = 6 y b = 6", "a = 8 y b = 3", "a = 10 y b = 10", "a = 9 y b = 5", "a = 12 y b = 2"]
    if l == 0:
        stem_eq, pairs = "log(a + b) = log(a) + log(b)", [f"a = {a} y b = {b.replace('/', ',') if '/' not in b else b}" for a, b in eq if "/" not in b]
    elif l == 1:
        stem_eq = "log(a + b) = log(a) + log(b)"
        pairs = [f"a = {a} y b = {b}" for a, b in eq]
    else:
        stem_eq = "log(a + b) = log(a) + log(b)"
        pairs = [f"a = {b} y b = {a}" for a, b in eq if "/" not in b] + [f"a = {a} y b = {b}" for a, b in eq if "/" in b]
    if len(pairs) < 5:
        raise Reject
    bad = r.sample(pairs, 4)
    good = r.choice(good_pairs)
    if good in bad:
        raise Reject
    fig = card([f"Afirmación: {stem_eq}", "para todo a, b > 0", "¿En qué par se refuta?"], 210, 21)
    return make(f"Una estudiante afirma que {stem_eq} para todos los a, b > 0. ¿Con cuál de los siguientes pares la igualdad NO se cumple?",
                fig, good, bad, Q_ARG, "La igualdad solo vale cuando a + b = a·b. En el par correcto a + b ≠ a·b, así que sirve de contraejemplo.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_in_terms(r, l):
    if l < 2:
        i, j = r.randint(1, 4), r.randint(1, 3)
        kind = r.choice(["mul", "div", "sqrt"] if l else ["mul", "div"])
        if kind == "mul":
            N, ans, cands = 2 ** i * 3 ** j, [(i, "a"), (j, "b")], None
            wrong = [[(j, "a"), (i, "b")], [(i + j, "a"), (i + j, "b")], [(i, "a"), (-j, "b")], [(i * j, "a"), (i * j, "b")], [(i, "a"), (j + 1, "b")]]
            txt = f"log {N}"
        elif kind == "div":
            N, ans = F(2 ** i, 3 ** j), [(i, "a"), (-j, "b")]
            wrong = [[(j, "a"), (-i, "b")], [(i, "a"), (j, "b")], [(F(i, j), "a"), (F(1), "b")], [(-i, "a"), (j, "b")], [(i, "a"), (-j - 1, "b")]]
            txt = f"log ({2**i}/{3**j})"
        else:
            i, j = 2 * r.randint(1, 2), 2 * r.randint(1, 2)
            N, ans = 2 ** i * 3 ** j, [(F(i, 2), "a"), (F(j, 2), "b")]
            wrong = [[(i, "a"), (j, "b")], [(F(j, 2), "a"), (F(i, 2), "b")], [(F(i + j, 2), "a"), (F(i + j, 2), "b")], [(i, "a"), (F(j, 2), "b")], [(F(i, 2), "a"), (j, "b")]]
            txt = f"log √{N}"
        hint = ["log 2 = a", "log 3 = b"]
    else:
        i, j, k = r.randint(1, 4), r.randint(1, 3), r.randint(1, 2)
        N = 2 ** i * 3 ** j * 5 ** k
        ans = [(i - k, "a"), (j, "b"), (k, "")]
        wrong = [[(i + k, "a"), (j, "b"), (k, "")], [(i - k, "a"), (j, "b"), (-k, "")], [(i, "a"), (j, "b"), (k, "")], [(i - k, "a"), (j, "b")], [(k - i, "a"), (j, "b"), (k, "")], [(i + k, "a"), (j, "b"), (-k, "")]]
        txt = f"log {N}"
        hint = ["log 2 = a", "log 3 = b", "log 10 = 1"]
    correct = lc(ans)
    fig = card([f"{h}" for h in hint] + [f"{txt} = ?"], 230 if l == 2 else 210)
    cands = [lc(w) for w in wrong]
    stem = f"Con log 2 = a y log 3 = b" + (" y log 10 = 1" if l == 2 else "") + f", ¿cuál es el valor de {txt} en términos de a y b?"
    return make(stem, fig, correct, pick4(correct, cands), Q_PRO, f"Se descompone en factores y se aplican las propiedades: {txt} = {correct}.")


def t_eval(r, l):
    b = r.choice([2, 3, 5]) if l < 2 else r.choice([2, 3])
    e = lambda: r.randint(1, 5 if b == 2 else 3)
    if l == 0:
        i, j, k = e(), e(), e()
        expr, ans = f"{lg(b)}({b**i}) + {lg(b)}({b**j})", i + j
        cands = [i * j, i + j + 1, i + j - 1, b ** i + b ** j, i + j + k]
        if False: pass
    elif l == 1:
        i, j, k = e() + 1, e(), e()
        expr, ans = f"{lg(b)}({b**i}) − {lg(b)}({b**j}) + {lg(b)}({b**k})", i - j + k
        cands = [i + j + k, i - j - k, i * k - j, i - j, abs(i - j) + k + 1]
    else:
        i, j = 2 * r.randint(1, 3), 2 * r.randint(1, 3)
        expr, ans = f"2·{lg(b)}({b**i}) − ½·{lg(b)}({b**j})", 2 * i - j // 2
        cands = [i * 2 - j, 2 * i + j // 2, i - j, 2 * i - j // 2 + 1, i + j // 2 * 2]
        ans = 2 * i - j // 2
    cells = "".join(R(20 + n * 84, 60, 84, 46, FILL, NAVY, 2) + T(62 + n * 84, 90, f"{b}^{n + 1} = {b ** (n + 1)}", 15) for n in range(6))
    fig = wrap(560, 180, cells + tag(280, 25, "Tabla de potencias", 16) + tag(280, 145, f"{expr} = ?", 20), "Tabla de potencias")
    correct = str(ans)
    return make(f"¿Cuál es el valor de {expr}?", fig, correct, pick4(correct, [str(c) for c in cands]), Q_PRO,
                f"Se aplican las propiedades y {lg(b)}({b}^n) = n: el resultado es {ans}.")


BY_SKILL = {
    Q_RES: [t_pow_eq, t_log_eq],
    Q_MOD: [t_ph_richter, t_growth],
    Q_REP: [t_graph_base, t_inverse],
    Q_ARG: [t_domain, t_props, t_counter_log],
    Q_PRO: [t_in_terms, t_eval],
}
