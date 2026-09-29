"""Clase 6 · Función cuadrática: análisis paramétrico y optimización."""
from fractions import Fraction as F
from math import sqrt
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase05 import poly, parab

HALF = {F(1, 2): "½", F(-1, 2): "−½"}


def cf(a):
    a = F(a)
    if a == 1: return ""
    if a == -1: return "−"
    if a in HALF: return HALF[a]
    return fs(a)


def vf(a, h, k):
    h, k = F(h), F(k)
    core = "x²" if h == 0 else f"(x {'−' if h > 0 else '+'} {fs(abs(h))})²"
    s = cf(a) + core
    if k > 0: s += f" + {fs(k)}"
    elif k < 0: s += f" − {fs(abs(k))}"
    return s


def P_(x, y):
    return f"({fs(x)}, {fs(y)})"


def rng_y(f, x0, x1):
    ys = [f(x0 + (x1 - x0) * i / 60) for i in range(61)]
    return min(ys), max(ys)


# ---------------------------------------------------------------- Resolver
def t_vertex(r, l):
    if l == 0:
        a, h, k = r.choice([1, -1]), r.randint(-5, 5), r.randint(-6, 6)
        if h == 0 and k == 0: raise Reject
        f = lambda x: a * (x - h) ** 2 + k
        stem = f"¿Cuáles son las coordenadas del vértice de la parábola f(x) = {vf(a, h, k)}?"
        ans = P_(h, k)
        cands = [P_(-h, k), P_(h, -k), P_(k, h), P_(-h, -k), P_(h, k + 1), P_(h + 1, k)]
        ex = f"En la forma a(x − h)² + k el vértice es (h, k) = {ans}."
        fig = parab(f, h - 4, h + 4, [], extra=lambda p: p.vline(h)).svg("Parábola con su eje de simetría")
    elif l == 1:
        a, h, k = r.choice([1, 2, 3, -1, -2]), r.randint(-4, 4), r.randint(-8, 8)
        b, c = -2 * a * h, a * h * h + k
        ext = "mínimo" if a > 0 else "máximo"
        stem = f"¿Cuál es el valor {ext} de la función f(x) = {poly(a, b, c)}?"
        ans = str(k)
        cands = [c, h, -h, -k, b, k + a]
        cands = [str(x) for x in cands]
        f = lambda x: a * x * x + b * x + c
        fig = parab(f, h - 4, h + 4, [], extra=lambda p: p.vline(h)).svg("Gráfico de la función")
        ex = f"x del vértice = −b/2a = {h}; f({h}) = {k}."
    else:
        r1, r2 = r.choice([(-4, 2), (-3, 5), (0, 6), (-5, 1), (1, 7), (-6, 2), (2, 8), (-2, 4)])
        a = r.choice([1, 2, -1, -2, 3, -3, 1, -1])
        m = (r1 + r2) // 2
        k = a * (m - r1) * (m - r2)
        ext = "mínimo" if a > 0 else "máximo"
        stem = f"La función f(x) = {cf(a)}(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("(x + 0)", "x").replace("(x − 0)", "x") + f" tiene un {ext}. ¿Cuál es su valor?"
        ans = str(k)
        cands = [str(a * r1 * r2), str(m), str(-k), str(a * (r2 - r1)), str(k + a), str(abs(k) * 2)]
        f = lambda x: a * (x - r1) * (x - r2)
        y0, y1 = rng_y(f, r1 - 3, r2 + 3)
        fig = parab(f, r1 - 3, r2 + 3, [(r1, 0, f"({r1}, 0)", -28 if a > 0 else 28), (r2, 0, f"({r2}, 0)", -28 if a > 0 else 28)]).svg("Parábola con sus raíces")
        ex = f"El vértice está en x = ({r1} + {r2})/2 = {m}: f({m}) = {k}."
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, ex)


def t_param(r, l):
    if l == 0:
        b, c = r.randint(-6, 6), r.randint(-8, 8)
        p = r.choice([x for x in range(-4, 5) if x])
        q = p * p + b * p + c
        stem = f"La parábola f(x) = x² {'−' if b < 0 else '+'} {abs(b)}x + c pasa por el punto ({p}, {q}). ¿Cuál es el valor de c?".replace("+ 0x", "").replace("− 0x", "")
        ans = str(c)
        cands = [q - p * p + b * p, q + p * p + b * p, q - b * p, q, c + 1, q - p * p]
        cands = [str(x) for x in cands]
        f = lambda x: x * x + b * x + c
        fig = parab(f, -5, 5, [(p, q, f"({p}, {q})", -28)]).svg("Parábola que pasa por un punto")
        ex = f"{q} = {p}² + ({b})({p}) + c ⟹ c = {c}."
    elif l == 1:
        a = r.choice([1, 2, 3])
        h = r.choice([x for x in range(-4, 5) if x])
        k = -2 * a * h
        c = r.randint(-5, 5)
        stem = f"El eje de simetría de f(x) = {cf(a)}x² + kx {'+' if c >= 0 else '−'} {abs(c)} es la recta x = {h}. ¿Cuál es el valor de k?"
        ans = str(k)
        cands = [-k, h, -h, 2 * h, k + a, F(k, 2) if k % 2 == 0 else k + 2]
        cands = [str(x) for x in cands]
        f = lambda x: a * x * x + k * x + c
        fig = parab(f, h - 4, h + 4, [], extra=lambda p: p.vline(h)).svg("Parábola con eje de simetría dado")
        ex = f"−k/(2·{a}) = {h} ⟹ k = {k}."
    else:
        a = r.choice([1, 2, 3, -1, -2, -3])
        h, k = r.randint(-3, 3), r.randint(-5, 5)
        d = r.choice([x for x in range(-3, 4) if x and x != 0])
        p, q = h + d, k + a * d * d
        stem = f"La parábola f(x) = a{vf(1, h, k).replace('x²', 'x²') if False else ''}(x {'−' if h > 0 else '+'} {abs(h)})² {'+' if k >= 0 else '−'} {abs(k)} pasa por el punto ({p}, {q}). ¿Cuál es el valor de a?".replace("(x + 0)", "x").replace("(x − 0)", "x")
        ans = str(a)
        cands = [-a, a + 1, F(q - k, abs(d)) if (q - k) % abs(d) == 0 else a + 2, q - k, a - 1, 1]
        cands = [str(x) for x in cands]
        f = lambda x: a * (x - h) ** 2 + k
        fig = parab(f, h - 4, h + 4, [(h, k, f"V({h}, {k})", 28 if a < 0 else -28), (p, q, f"({p}, {q})", -28 if a > 0 else 28)]).svg("Parábola con vértice y un punto")
        ex = f"{q} = a({p} − {h})² + {k} ⟹ a = {a}."
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_optim(r, l):
    if l == 0:
        S = r.choice(range(6, 42, 2))
        A = (S // 2) ** 2
        stem = f"La suma de dos números reales es {S}. ¿Cuál es el máximo valor posible de su producto?"
        ans = str(A)
        cands = [S * S // 2, S * S, S // 2, A + S // 2, A - S // 2 if A > S // 2 else A + 3, S * (S - 1)]
        cands = [str(x) for x in cands]
        fig = parab(lambda x: x * (S - x), 0, S, [], yr=(0, A + 4), extra=lambda p: p.parts.append(tag(p.X(S / 2), p.Y(A / 2), "x·(S − x)", 16))).svg("Producto de dos números con suma fija")
        ex = f"P(x) = x({S} − x) tiene su máximo en x = {S//2}: P = {A}."
    elif l == 1:
        Lf = r.choice(range(8, 64, 4))
        A = Lf * Lf // 8
        stem = f"Se dispone de {Lf} m de malla para cercar un corral rectangular que usa una pared como uno de sus lados (la pared no lleva malla). ¿Cuál es el área máxima del corral, en m²?"
        ans = str(A)
        cands = [Lf * Lf // 4, Lf * Lf // 16, (Lf // 2) ** 2, A + Lf // 4, Lf * Lf // 2, A - Lf // 4]
        cands = [str(x) for x in cands]
        body = L(140, 40, 420, 40, INK, 8) + tag(280, 22, "pared", 15) + R(190, 40, 180, 130, FILL2) + tag(160, 105, "x", 17) + tag(400, 105, "x", 17) + tag(280, 195, "L − 2x", 17)
        fig = wrap(560, 225, body, "Corral junto a una pared")
        ex = f"Área = x({Lf} − 2x), máxima en x = {Lf//4}: {A} m²."
    else:
        b = r.choice([2, 4, 5, 10])
        ps = r.choice([10, 15, 20, 25, 30, 40, 50])
        a = 2 * b * ps
        stem = f"La demanda de un producto es q = {a} − {b}p unidades cuando el precio es p pesos. El ingreso es I = p·q. ¿Qué precio maximiza el ingreso?"
        ans = f"${ps}"
        cands = [f"${a // b}", f"${a // 2}", f"${ps * (a - b * ps)}", f"${ps + 5}", f"${max(1, ps - 5)}", f"${a}"]
        Rf = lambda p: p * (a - b * p)
        fig = parab(Rf, 0, a / b, [], yr=(0, Rf(ps) * 1.1), extra=lambda pl: pl.parts.append(tag(pl.X(a / b * 0.5), pl.Y(Rf(ps) * 0.5), "I(p) = p(a − bp)", 16))).svg("Ingreso según el precio")
        ex = f"I(p) = p({a} − {b}p) es máximo en p = {a}/{2*b} = {ps}."
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


def t_proj(r, l):
    v, h0 = r.choice([10, 20, 30, 40]), r.choice([0, 5, 10, 15, 20, 25, 30, 45])
    hf = lambda t: -5 * t * t + v * t + h0
    tm = v / 10
    tmax = (v + sqrt(v * v + 20 * h0)) / 10
    hmax = h0 + v * v // 20
    ec = f"h(t) = −5t² + {v}t" + (f" + {h0}" if h0 else "")
    if l == 0:
        stem = f"La altura (en m) de un objeto lanzado hacia arriba es {ec}, con t en segundos. ¿En qué instante alcanza su altura máxima?"
        ans = f"{tm:g} s".replace(".", ",")
        cands = [f"{v / 5:g} s", f"{v / 20:g} s", f"{hmax} s", f"{v} s", f"{tm + 1:g} s", f"{h0 // 5 + 1} s"]
        ex = f"t = −b/2a = {v}/10 = {tm:g} s."
    elif l == 1:
        stem = f"La altura (en m) de un objeto lanzado hacia arriba es {ec}, con t en segundos. ¿Cuál es la altura máxima que alcanza?"
        ans = f"{hmax} m"
        cands = [f"{h0 + v} m", f"{hmax + 5} m", f"{h0 + v * v // 10} m", f"{v * v // 20} m" if h0 else f"{hmax + 10} m", f"{hmax - 5} m", f"{int(hf(v / 5))} m" if hf(v / 5) != hmax else f"{hmax + 15} m"]
        ex = f"h({tm:g}) = {hmax} m."
    else:
        stem = f"La altura (en m) de un objeto lanzado hacia arriba es {ec}, con t en segundos. ¿Durante cuántos segundos su altura es mayor o igual que la altura desde la que se lanzó?"
        ans = f"{v / 5:g} s".replace(".", ",")
        cands = [f"{tm:g} s", f"{v / 20:g} s", f"{v:g} s", f"{tmax:.0f} s" if h0 and abs(tmax - round(tmax)) < 1e-9 else f"{v / 5 + 1:g} s", f"{2 * v / 5:g} s"]
        ex = f"h(t) = h₀ ⟹ −5t² + {v}t = 0 ⟹ t = 0 o t = {v/5:g}."
    cands = [c.replace(".", ",") for c in cands]
    pl = parab(hf, 0, tmax + 0.5, [(0, h0, f"h₀ = {h0}", 28)], yr=(0, hmax + 5))
    return make(stem, pl.svg("Trayectoria del objeto"), ans, pick4(ans, cands), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_transform(r, l):
    if l == 0:
        a = 1
    elif l == 1:
        a = r.choice([2, -1, -2, 3])
    else:
        a = r.choice([F(1, 2), F(-1, 2), 2, -2, 3, -3])
    h, k = r.choice([x for x in range(-4, 5) if x]), r.choice([x for x in range(-5, 6) if x])
    if l >= 1:
        dx = 2 if F(a).denominator == 2 else 1
        pt = (h + dx, k + F(a) * dx * dx)
    g = lambda x: float(a) * (x - h) ** 2 + k
    marks = [(h, k, f"V({h}, {k})", 28 if a < 0 else -28)]
    if l >= 1:
        marks.append((float(pt[0]), float(pt[1]), f"({fs(pt[0])}, {fs(pt[1])})", -28 if a < 0 else 28))
    ys = [g(h + d / 4) for d in range(-16, 17)] + [x * x for x in range(-4, 5)]
    def extra(p):
        p.curve(lambda x: x * x, h - 4, h + 4, NAVY, 3)
        for i, (mx, my, lab, dy) in enumerate(marks):
            p.pt(mx, my, lab, dx=(-55 if i == 0 else 55), dy=dy)
    pl = parab(g, h - 4, h + 4, [], yr=(max(-12, min(ys) - 1), min(14, max(g(h - 4), g(h + 4), 6) + 1)), extra=extra)
    ans = "g(x) = " + vf(a, h, k)
    cands = ["g(x) = " + vf(a, -h, k), "g(x) = " + vf(a, h, -k), "g(x) = " + vf(a, -h, -k), "g(x) = " + vf(-a, h, k),
             "g(x) = " + (vf(F(1), h, k) if a != 1 else vf(2, h, k)), "g(x) = " + vf(a, k, h)]
    fig = pl.svg("Parábola g y parábola f(x) = x² en azul")
    return make("La curva roja es la gráfica de g y la azul es la de f(x) = x². ¿Cuál es la ecuación de g?", fig, ans, pick4(ans, cands), Q_REP,
                f"El vértice es ({h}, {k})" + ("" if l == 0 else f" y el punto indicado da a = {fs(a)}") + f": g(x) = {vf(a, h, k)}.")


def t_intervals(r, l):
    a = r.choice([1, -1])
    if l < 2:
        h, k = r.randint(-4, 4), r.randint(-5, 5)
        if h == k: raise Reject
        f = lambda x: a * (x - h) ** 2 + k
        pl = parab(f, h - 4, h + 4, [], extra=lambda p: p.vline(h))
        if l == 0:
            kind = r.choice(["creciente", "decreciente"])
            inc_right = a > 0
            side = (">" if inc_right else "<") if kind == "creciente" else ("<" if inc_right else ">")
            ans = f"x {side} {h}"
            cands = [f"x {'<' if side == '>' else '>'} {h}", f"x {side} {k}", f"x {'<' if side == '>' else '>'} {k}", f"x ≠ {h}", f"x {side} {-h}"]
            stem = f"La gráfica muestra una función cuadrática con su eje de simetría. ¿En qué intervalo es la función {kind}?"
            ex = f"El vértice está en x = {h}; la parábola abre hacia {'arriba' if a > 0 else 'abajo'}."
        else:
            ans = f"y {'≥' if a > 0 else '≤'} {k}"
            cands = [f"y {'≤' if a > 0 else '≥'} {k}", f"y {'≥' if a > 0 else '≤'} {h}", f"y {'≤' if a > 0 else '≥'} {h}", f"y {'>' if a > 0 else '<'} {k}", f"y ≠ {k}"]
            stem = "La gráfica muestra una función cuadrática f con su eje de simetría. ¿Cuál es el recorrido de f?"
            ex = f"El valor {'mínimo' if a > 0 else 'máximo'} es {k}, luego el recorrido es {ans}."
    else:
        r1, r2 = sorted(r.sample(range(-5, 6), 2))
        f = lambda x: a * (x - r1) * (x - r2)
        pos = r.choice([True, False])
        pl = parab(f, r1 - 3, r2 + 3, [(r1, 0, f"({r1}, 0)", -28 if a > 0 else 28), (r2, 0, f"({r2}, 0)", -28 if a > 0 else 28)])
        out = f"x < {r1} o x > {r2}"
        inn = f"{r1} < x < {r2}"
        ans = (out if a > 0 else inn) if pos else (inn if a > 0 else out)
        cands = [inn if ans == out else out, f"x < {r1}", f"x > {r2}", f"x ≠ {r1} y x ≠ {r2}", f"x ≤ {r1} o x ≥ {r2}"]
        stem = f"La gráfica corta al eje X en los puntos indicados. ¿Para qué valores de x se cumple f(x) {'>' if pos else '<'} 0?"
        ex = "Se observa dónde la curva está " + ("por encima" if pos else "por debajo") + " del eje X."
    return make(stem, pl.svg("Gráfica de una función cuadrática"), ans, pick4(ans, cands), Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
def t_statements(r, l):
    a = r.choice([1, -1]) if l == 0 else r.choice([2, 3, -2, -3]) if l == 1 else r.choice([1, 2, -1, -2, 3, -3])
    h, k = r.randint(-4, 4), r.randint(-6, 6)
    b, c = -2 * a * h, a * h * h + k
    ext, oext = ("mínimo", "máximo") if a > 0 else ("máximo", "mínimo")
    T = [f"Su vértice es el punto {P_(h, k)}", f"Su eje de simetría es la recta x = {h}", f"Tiene un {ext} de valor {k}",
         f"Corta al eje Y en el punto (0, {c})", f"Abre hacia {'arriba' if a > 0 else 'abajo'}"]
    Fl = [f"Su vértice es el punto {P_(-h, k)}", f"Su vértice es el punto {P_(h, -k)}", f"Su vértice es el punto {P_(k, h)}",
          f"Su eje de simetría es la recta x = {-h}", f"Su eje de simetría es la recta x = {k}", f"Tiene un {oext} de valor {k}",
          f"Tiene un {ext} de valor {h}", f"Tiene un {ext} de valor {-k}", f"Corta al eje Y en el punto (0, {k})", f"Corta al eje Y en el punto (0, {-c})",
          f"Abre hacia {'abajo' if a > 0 else 'arriba'}"]
    Fl = [x for x in dict.fromkeys(Fl) if x not in T]
    eq = f"f(x) = {vf(a, h, k)}" if l < 2 else f"f(x) = {poly(a, b, c)}"
    f = lambda x: a * (x - h) ** 2 + k
    pl = parab(f, h - 4, h + 4, [])
    if l < 2:
        good, bad = r.choice(T), r.sample(Fl, 4)
        stem = f"Sobre la función {eq}, ¿cuál de las siguientes afirmaciones es verdadera?"
        ex = "Se compara con el vértice (h, k), el signo de a y la ordenada en el origen."
    else:
        good, bad = r.choice(Fl), r.sample(T, 4)
        stem = f"Sobre la función {eq}, ¿cuál de las siguientes afirmaciones es FALSA?"
        ex = "Las otras cuatro afirmaciones se deducen del vértice, el signo de a y el punto (0, c)."
    return make(stem, pl.svg("Gráfica de la función"), good, bad, Q_ARG, ex)


def t_family(r, l):
    a3 = r.choice([(F(1, 2), F(1), F(2)), (F(1), F(2), F(3)), (F(1, 4), F(1, 2), F(1)), (F(1), F(3), F(5)), (F(1, 2), F(2), F(4))])
    sg = 1 if l == 0 else r.choice([1, -1])
    A = [sg * x for x in a3]
    closed = max(A, key=abs); opened = min(A, key=abs)
    lab = lambda x: fs(x) if x.denominator == 1 else fs(x)
    T = ["Las tres curvas tienen el mismo vértice (0, 0)", "Las tres curvas son simétricas respecto del eje Y",
         f"La curva con a = {lab(closed)} es la más cerrada (angosta)", f"La curva con a = {lab(opened)} es la más abierta (ancha)",
         f"Las tres curvas abren hacia {'arriba' if sg > 0 else 'abajo'}"]
    other = [x for x in A if x not in (closed, opened)][0]
    Fl = [f"La curva con a = {lab(opened)} es la más cerrada (angosta)", f"La curva con a = {lab(closed)} es la más abierta (ancha)",
          "Las tres curvas tienen distinto vértice", "Las tres curvas cortan al eje X en dos puntos", f"Las tres curvas abren hacia {'abajo' if sg > 0 else 'arriba'}",
          f"La curva con a = {lab(other)} es la más cerrada (angosta)", "Las tres curvas tienen distinto eje de simetría"]
    ymax = 7
    pl = Plot(560, 270, -3, 3, -ymax if sg < 0 else -1, 1 if sg < 0 else ymax)
    pl.axes(1, 2)
    for i, av in enumerate(A):
        pl.curve(lambda x, av=av: float(av) * x * x, -3, 3, [ACC, NAVY, "#475569"][i], 4)
        yl = sg * (2.2 + 1.7 * i)
        xl = sqrt(abs(yl / float(av)))
        if xl < 2.9:
            pl.parts.append(tag(pl.X(xl), pl.Y(yl), f"a = {lab(av)}", 15))
    if l < 2:
        good, bad = r.choice(T), r.sample(Fl, 4)
        stem = "Se grafican tres funciones de la forma f(x) = ax². ¿Cuál de las siguientes afirmaciones es verdadera?"
        ex = "A mayor valor absoluto de a, más cerrada es la parábola."
    else:
        good, bad = r.choice(Fl), r.sample(T, 4)
        stem = "Se grafican tres funciones de la forma f(x) = ax². ¿Cuál de las siguientes afirmaciones es FALSA?"
        ex = "A mayor valor absoluto de a, más cerrada es la parábola; todas comparten vértice y eje."
    return make(stem, pl.svg("Tres parábolas y = ax²"), good, bad, Q_ARG, ex)


def t_counter_par(r, l):
    if l == 0:
        claim, cond, want = "Si b > 0, el vértice de f(x) = ax² + bx + c está a la izquierda del eje Y.", lambda a, b, c: b > 0, lambda a, b, c: a < 0
        gen = lambda: (r.choice([-3, -2, -1, 1, 2, 3]), r.randint(1, 9), r.randint(-5, 5))
    elif l == 1:
        claim, cond, want = "Si a > 0, el valor mínimo de f(x) = ax² + bx + c es positivo.", lambda a, b, c: a > 0, lambda a, b, c: c - F(b * b, 4 * a) <= 0
        gen = lambda: (r.randint(1, 4), r.randint(-6, 6), r.randint(-6, 8))
    else:
        claim, cond, want = "Si a < 0, el valor máximo de f(x) = ax² + bx + c es positivo.", lambda a, b, c: a < 0, lambda a, b, c: c - F(b * b, 4 * a) <= 0
        gen = lambda: (r.randint(-4, -1), r.randint(-6, 6), r.randint(-8, 6))
    goods, bads = set(), set()
    for _ in range(500):
        a, b, c = gen()
        if not cond(a, b, c) or (l == 0 and b == 0): continue
        (goods if want(a, b, c) else bads).add(f"f(x) = {poly(a, b, c)}")
    if not goods or len(bads) < 4: raise Reject
    good = r.choice(sorted(goods)); bad = r.sample(sorted(bads), 4)
    fig = card(["Afirmación de un estudiante:", claim.split(", ")[0].rstrip(".") + " ⟹ conclusión", "¿Con qué función se refuta?"], 210, 20)
    return make(f"Un estudiante afirma: «{claim}» ¿Cuál de las siguientes funciones sirve como contraejemplo?", fig, good, bad, Q_ARG,
                "Un contraejemplo cumple la condición de la afirmación pero no su conclusión.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_complete(r, l):
    if l == 0:
        b = r.choice(range(-12, 13, 2))
        c = r.randint(-9, 9)
        if b == 0: raise Reject
        a, h, k = 1, F(-b, 2), c - F(b * b, 4)
        cands = [vf(1, -h, k), vf(1, h, c + F(b * b, 4)), vf(1, h, c - F(b * b, 2)), vf(1, -b, c - b * b), vf(1, h, c)]
    elif l == 1:
        a = r.choice([2, 3, -1, -2])
        h = r.choice([x for x in range(-4, 5) if x]); k = r.randint(-6, 6)
        b, c = -2 * a * h, a * h * h + k
        cands = [vf(1, h, k), vf(a, -h, k), vf(a, h, c - h * h), vf(a, h, c), vf(a, h, -k)]
    else:
        a = r.choice([1, 2, 3, -1, -2])
        h, k = r.choice([x for x in range(-4, 5) if x]), r.randint(-6, 6)
        b, c = -2 * a * h, a * h * h + k
        stem = f"¿Cuál es la forma general de la función f(x) = {vf(a, h, k)}?"
        ans = "f(x) = " + poly(a, b, c)
        ds = ["f(x) = " + poly(a, -b, c), "f(x) = " + poly(a, b, k), "f(x) = " + poly(a, b, h * h + k), "f(x) = " + poly(1, b, c), "f(x) = " + poly(a, -b, k)]
        return make(stem, card([f"f(x) = {vf(a, h, k)}", "Desarrolla el cuadrado y ordena"], 190, 22), ans, pick4(ans, ds), Q_PRO, f"a(x − h)² + k = {poly(a, b, c)}.")
    stem = f"¿Cuál es la forma canónica a(x − h)² + k de la función f(x) = {poly(a, b, c)}?"
    ans = "f(x) = " + vf(a, h, k)
    return make(stem, card([f"f(x) = {poly(a, b, c)}", "Completa el cuadrado"], 190, 22), ans, pick4(ans, ["f(x) = " + x for x in cands]), Q_PRO,
                f"Se completa el cuadrado: f(x) = {vf(a, h, k)}.")


def t_features(r, l):
    if l == 0:
        a = r.choice([1, 2, 3, -1, -2, 4]); h = r.randint(-6, 6)
        b, c = -2 * a * h, r.randint(-6, 6)
        stem = f"¿Cuál es la ecuación del eje de simetría de f(x) = {poly(a, b, c)}?"
        ans = f"x = {h}"
        cands = [f"x = {-h}", f"x = {2 * h}", f"x = {-2 * h}", f"x = {c}", f"x = {h + 1}", f"x = {b}"]
        ex = f"x = −b/(2a) = {-b}/{2*a} = {h}."
        eq = poly(a, b, c)
    elif l == 1:
        a = r.choice([1, 2, 3, -1, -2, -3]); h, k = r.randint(-4, 4), r.randint(-8, 8)
        b, c = -2 * a * h, a * h * h + k
        stem = f"¿Cuáles son las coordenadas del vértice de f(x) = {poly(a, b, c)}?"
        ans = P_(h, k)
        cands = [P_(h, c), P_(-h, k), P_(h, -k), P_(2 * h, k), P_(h, k + a), P_(-h, c)]
        ex = f"h = −b/2a = {h}; k = f({h}) = {k}."
        eq = poly(a, b, c)
    else:
        a = r.choice([1, 2, -1, -2, 3])
        r1, r2 = r.sample(range(-6, 7), 2)
        b, c = -a * (r1 + r2), a * r1 * r2
        stem = f"La gráfica de f(x) = {poly(a, b, c)} corta al eje X en dos puntos. ¿Cuánto mide el segmento que une esos puntos?"
        d = abs(r2 - r1)
        ans = str(d)
        cands = [abs(r1 + r2), abs(r1 * r2), d * abs(a) if abs(a) > 1 else d + 1, d + 1, d - 1 if d > 1 else d + 2, abs(r1) + abs(r2) + 1]
        cands = [str(x) for x in cands]
        ex = f"Las raíces son {r1} y {r2}; la distancia es {d}."
        eq = poly(a, b, c)
        return make(stem, card([f"f(x) = {eq}", "Δ = b² − 4ac  ·  distancia = |x₁ − x₂|"], 190, 22), ans, pick4(ans, cands), Q_PRO, ex)
    return make(stem, card([f"f(x) = {eq}", "x_v = −b / (2a)"], 190, 22), ans, pick4(ans, cands), Q_PRO, ex)


BY_SKILL = {
    Q_RES: [t_vertex, t_param],
    Q_MOD: [t_optim, t_proj],
    Q_REP: [t_transform, t_intervals],
    Q_ARG: [t_statements, t_family, t_counter_par],
    Q_PRO: [t_complete, t_features],
}
