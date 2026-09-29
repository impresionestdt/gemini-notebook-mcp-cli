"""Clase 12 · Sistemas de ecuaciones avanzados (no lineales): rectas con parábolas."""
from fractions import Fraction as F
from math import ceil, floor, sqrt
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase05 import poly
from clase08 import lx
from clase10 import nice


def pts(lst):
    return " y ".join(f"({fs(x)}, {fs(y)})" for x, y in sorted(lst))


def eq_par(a, b, c):
    return "y = " + poly(a, b, c)


def eq_lin(m, n):
    return "y = " + lx(m, n).replace("x", "x") if m != 0 else f"y = {n}"


def sysstr(a, b, c, m, n):
    return f"{{ {eq_par(a, b, c)} ; {eq_lin(m, n)} }}"


def plot2(fs_, x0, x1, y0=None, y1=None, marks=(), clip=30):
    xs = [x0 + (x1 - x0) * i / 80 for i in range(81)]
    ys = [f(x) for f in fs_ for x in xs]
    lo = min(ys) if y0 is None else y0
    hi = max(ys) if y1 is None else y1
    lo, hi = max(lo, -clip), min(hi, clip)
    pad = max(2, 0.12 * (hi - lo))
    lo, hi = min(lo, -pad), max(hi, pad)
    pl = Plot(560, 285, x0, x1, lo, hi)
    pl.axes(1 if x1 - x0 <= 12 else 2, nice((hi - lo) / 6))
    cols = [ACC, NAVY, "#475569"]
    for i, f in enumerate(fs_):
        pl.curve(f, x0, x1, cols[i % 3], 4)
    for (x, y, lab, dx, dy) in marks:
        pl.pt(x, y, lab, dx=dx, dy=dy)
    return pl


def mutate_pts(sol, r):
    """Conjuntos de puntos erróneos a partir de la solución correcta."""
    out = []
    out.append([(-x, y) for x, y in sol])
    out.append([(x, -y) for x, y in sol])
    out.append([(y, x) for x, y in sol])
    if len(sol) > 1:
        out.append(sol[:1]); out.append(sol[1:])
        out.append([(x, y + 1) for x, y in sol])
    else:
        out.append([(sol[0][0] + 1, sol[0][1])])
    out.append([(x + 1, y) for x, y in sol])
    return [pts(o) for o in out]


# ---------------------------------------------------------------- Resolver
def build_lp(r, l):
    a = 1 if l == 0 else r.choice([1, -1, 2, -2])
    b, c = r.randint(-4, 4), r.randint(-5, 5)
    kind = "two" if l < 2 else r.choice(["two", "tan", "none"])
    p = lambda x: a * x * x + b * x + c
    if kind == "two":
        r1, r2 = sorted(r.sample(range(-4, 5), 2))
        m = a * (r1 + r2) + b
        n = p(r1) - m * r1
        sol = [(r1, p(r1)), (r2, p(r2))]
    elif kind == "tan":
        r1 = r.randint(-4, 4)
        m = 2 * a * r1 + b
        n = p(r1) - m * r1
        sol = [(r1, p(r1))]
    else:
        m = r.randint(-3, 3)
        q = F((b - m) ** 2, 4 * a)
        n = c - ceil(q) - 1 if a > 0 else c - floor(q) + 1
        sol = []
    return a, b, c, m, n, sol


def t_line_parab(r, l):
    a, b, c, m, n, sol = build_lp(r, l)
    p = lambda x: a * x * x + b * x + c
    ln = lambda x: m * x + n
    ans = pts(sol) if sol else "No hay solución real"
    if sol:
        cands = mutate_pts(sol, r) + (["No hay solución real"] if l == 2 else [])
    else:
        cands = [pts([(0, p(0)), (1, p(1))]), pts([(-1, p(-1)), (2, p(2))]), pts([(0, n), (1, m + n)]), pts([(1, p(1))]), pts([(0, c), (-1, p(-1))]), pts([(-c, 0)]) if c else pts([(2, p(2))])]
    xs = [s[0] for s in sol] or [0]
    pl = plot2([p, ln], min(xs) - 4, max(xs) + 4)
    return make(f"La parábola (roja) y la recta (azul) del gráfico forman el sistema {sysstr(a, b, c, m, n)}. ¿Cuál es su solución?", pl.svg("Parábola y recta"), ans, pick4(ans, cands), Q_RES,
                "Se igualan las expresiones de y, se resuelve la ecuación cuadrática y se calcula y en la recta." if sol else "Al igualar las expresiones el discriminante es negativo: no hay soluciones reales.")


def t_sum_prod(r, l):
    if l == 0:
        p, q = sorted(r.sample(range(-8, 9), 2))
        S, P = p + q, p * q
        stem = f"Resuelve el sistema {{ x + y = {S} ; x·y = {P} }}."
        sol = [(p, q), (q, p)]
        card_ = [f"x + y = {S}", f"x · y = {P}"]
    elif l == 1:
        p, q = sorted(r.sample(range(1, 13), 2))
        d = q - p
        stem = f"Resuelve el sistema {{ x − y = {d} ; x·y = {p * q} }}."
        sol = [(q, p), (-p, -q)]
        card_ = [f"x − y = {d}", f"x · y = {p * q}"]
    else:
        trip = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15)])
        p, q, h = trip
        if r.random() < 0.5:
            stem = f"Resuelve el sistema {{ x + y = {p + q} ; x² + y² = {h * h} }}."
            sol = [(p, q), (q, p)]
            card_ = [f"x + y = {p + q}", f"x² + y² = {h * h}"]
        else:
            stem = f"Resuelve el sistema {{ x − y = {q - p} ; x² + y² = {h * h} }}."
            sol = [(q, p), (-p, -q)]
            card_ = [f"x − y = {q - p}", f"x² + y² = {h * h}"]
    ans = pts(sol)
    cands = mutate_pts(sol, r)
    card_ = [x.replace("-", "−") for x in card_]
    return make(stem, card(["Sistema no lineal:"] + card_, 210, 21), ans, pick4(ans, cands), Q_RES,
                "Se despeja una variable en la ecuación lineal, se sustituye en la otra y se resuelve la cuadrática; luego se calcula la otra variable.")


# ---------------------------------------------------------------- Modelar
def t_trajectory(r, l):
    a = r.choice([-1, -1, -2])
    r1, r2 = sorted(r.sample(range(0, 9), 2))
    b = r.randint(2, 8) if a == -1 else r.randint(4, 12)
    p = lambda x: a * x * x + b * x
    m = a * (r1 + r2) + b
    n = p(r1) - m * r1
    if abs(m) > 12 or p(r1) < 0 or p(r2) < 0 or n < -20: raise Reject
    ctx = r.choice([("Una pelota describe la trayectoria", "y una rampa"), ("Un chorro de agua sigue la curva", "y golpea una pared inclinada"), ("Un puente en arco tiene forma", "y una carretera recta")])
    stem0 = f"{ctx[0]} y = {poly(a, b, 0)} (x, y en metros) {ctx[1]} de ecuación {eq_lin(m, n)}"
    if l == 0:
        stem = stem0 + ". ¿En qué valores de x se cruzan?"
        ans = f"x = {r1} y x = {r2}"
        cands = [f"x = {-r1} y x = {-r2}", f"x = {r1} y x = {r1 + r2}", f"x = {p(r1)} y x = {p(r2)}", f"x = {r1 + 1} y x = {r2 + 1}", f"x = {r1} y x = {r2 + 2}", f"x = {r2} y x = {r1 + r2 + 1}"]
    elif l == 1:
        stem = stem0 + ". ¿Qué distancia horizontal hay entre los dos puntos de cruce?"
        ans = f"{r2 - r1} m"
        cands = [f"{r1 + r2} m", f"{abs(p(r2) - p(r1))} m" if abs(p(r2) - p(r1)) != r2 - r1 else f"{r2 - r1 + 3} m", f"{r2 - r1 + 1} m", f"{max(1, r2 - r1 - 1)} m", f"{r2 * r1} m" if r1 * r2 != r2 - r1 and r1 * r2 > 0 else f"{r2 - r1 + 2} m", f"{r2} m"]
    else:
        stem = stem0 + ". ¿A qué altura y se produce el cruce que ocurre más lejos (mayor x)?"
        ans = f"{p(r2)} m"
        cands = [f"{p(r1)} m", f"{m * r2} m", f"{p(r2) + n} m", f"{-p(r2)} m", f"{p(r1) + p(r2)} m", f"{r2} m", f"{p(r2) + 1} m"]
    pl = plot2([p, lambda x: m * x + n], min(-1, r1 - 2), r2 + 3)
    return make(stem, pl.svg("Trayectoria y recta"), ans, pick4(ans, cands), Q_MOD, f"Se iguala {poly(a, b, 0)} = {lx(m, n)} y se resuelve: x = {r1} o x = {r2}.")


def t_break_even(r, l):
    r1, r2 = sorted(r.sample(range(1, 13), 2))
    if l == 2 and (r1 + r2) % 2: raise Reject
    b = r.randint(0, 5)
    m = r1 + r2 + b
    c = r1 * r2
    C = lambda x: x * x + b * x + c
    Rv = lambda x: m * x
    ctx = f"El costo total de producir x unidades es C(x) = {poly(1, b, c)} y el ingreso por su venta es I(x) = {m}x (en miles de pesos)"
    if l == 0:
        stem = ctx + ". ¿Para qué cantidades de unidades el costo es igual al ingreso?"
        ans = f"x = {r1} y x = {r2}"
        cands = [f"x = {-r1} y x = {-r2}", f"x = {r1} y x = {r1 + r2}", f"x = {c} y x = {m}", f"x = {r1 + 1} y x = {r2 - 1}" if r2 - 1 != r1 + 1 else f"x = {r1 + 1} y x = {r2 + 1}", f"x = {r1 - 1} y x = {r2 + 1}", f"x = {b} y x = {c}"]
    elif l == 1:
        stem = ctx + ". ¿Para qué cantidades de unidades el ingreso es mayor que el costo (hay ganancia)?"
        ans = f"{r1} < x < {r2}"
        cands = [f"x < {r1} o x > {r2}", f"{r1} ≤ x ≤ {r2}", f"x > {r1}", f"x < {r2}", f"{-r2} < x < {-r1}", f"0 < x < {r1}"]
    else:
        stem = ctx + ". ¿Con cuántas unidades la ganancia (ingreso menos costo) es máxima?"
        ans = f"{(r1 + r2) // 2} unidades"
        cands = [f"{r1} unidades", f"{r2} unidades", f"{r1 + r2} unidades", f"{r1 * r2} unidades", f"{(r1 + r2) // 2 + 1} unidades", f"{abs(r2 - r1)} unidades"]
    pl = plot2([C, Rv], 0, r2 + 2, 0, None, clip=400)
    return make(stem, pl.svg("Costo (rojo) e ingreso (azul)"), ans, pick4(ans, cands), Q_MOD, f"I(x) = C(x) ⟹ x² − {m - b}x + {c} = 0 ⟹ x = {r1} o x = {r2}.")


# ---------------------------------------------------------------- Representar
def t_which_system(r, l):
    a, b, c, m, n, sol = build_lp(r, 0 if l == 0 else 1)
    if len(sol) != 2: raise Reject
    p = lambda x: a * x * x + b * x + c
    cands = [(a, b, c, m, n + 1), (a, b, c, -m, n), (-a, b, c, m, n), (a, -b, c, m, n), (a, b, c + 1, m, n), (a, b, c, m + 1, n), (a, b, -c, m, n) if c else (a, b, 1, m, n)]
    if l == 2:
        cands += [(a, b, c, m, -n) if n else (a, b, c, m, 2), (a, b + 1, c, m, n)]
    cands = [x for x in dict.fromkeys(cands) if x != (a, b, c, m, n)]
    ans = sysstr(a, b, c, m, n)
    ds = [sysstr(*x) for x in cands]
    xs = [s[0] for s in sol]
    labels = [(x, y, f"({x}, {y})", 0, -28 if y >= 0 else 28) for x, y in sol]
    pl = plot2([p, lambda x: m * x + n], min(xs) - 3, max(xs) + 3, marks=labels)
    return make("En el gráfico se muestran una parábola y una recta que se cortan en los puntos indicados. ¿Cuál de los siguientes sistemas tiene esos puntos como solución?", pl.svg("Parábola y recta con sus puntos de cruce"), ans, pick4(ans, ds), Q_REP,
                "Se reemplazan los puntos indicados en ambas ecuaciones: solo el sistema correcto se cumple en los dos puntos.")


CNT = ["Ninguna solución", "Exactamente 1 solución", "Exactamente 2 soluciones", "Exactamente 3 soluciones", "Infinitas soluciones"]


def count_lp(a, b, c, m, n):
    D = (b - m) ** 2 - 4 * a * (c - n)
    return 0 if D < 0 else 1 if D == 0 else 2


def t_count(r, l):
    if l == 0:
        for _ in range(40):
            a = r.choice([1, -1]); b, c, m, n = r.randint(-3, 3), r.randint(-4, 4), r.randint(-3, 3), r.randint(-5, 5)
            k = count_lp(a, b, c, m, n)
            if k in (0, 1, 2): break
        p, q = (lambda x: a * x * x + b * x + c), (lambda x: m * x + n)
        ans_i = k
        fig = plot2([p, q], -5, 5)
    elif l == 1:
        for _ in range(60):
            a1, a2 = r.choice([1, 2, -1, -2]), r.choice([1, 2, -1, -2])
            if a1 == a2: continue
            b1, b2, c1, c2 = (r.randint(-3, 3) for _ in range(4))
            D = (b1 - b2) ** 2 - 4 * (a1 - a2) * (c1 - c2)
            k = 0 if D < 0 else 1 if D == 0 else 2
            break
        p, q = (lambda x: a1 * x * x + b1 * x + c1), (lambda x: a2 * x * x + b2 * x + c2)
        ans_i = k
        fig = plot2([p, q], -5, 5)
    else:
        for _ in range(200):
            a, b, c, m, n = r.choice([1, -1]), r.randint(-4, 4), r.randint(-3, 3), r.randint(-4, 4), r.randint(-4, 4)
            g = lambda x: a * x ** 3 + b * x * x * 0 + c * x - (m * x + n) + (b * x * x)
            vals = [g(-6 + i * 0.01) for i in range(1201)]
            roots = sum(1 for i in range(1200) if vals[i] == 0 or vals[i] * vals[i + 1] < 0)
            if 1 <= roots <= 3 and min(abs(v) for v in vals if abs(v) > 0) > 0: break
        p, q = (lambda x: a * x ** 3 + b * x * x + c * x), (lambda x: m * x + n)
        ans_i = roots
        fig = plot2([p, q], -5, 5)
        fig.parts if False else None
    ans = CNT[ans_i]
    rest = [x for i, x in enumerate(CNT) if i != ans_i]
    kind = "una parábola y una recta" if l == 0 else "dos parábolas" if l == 1 else "una curva cúbica y una recta"
    return make(f"Se grafican {kind}. ¿Cuántas soluciones reales tiene el sistema formado por sus dos ecuaciones?", fig.svg("Dos curvas"), ans, rest, Q_REP,
                "Las soluciones del sistema son los puntos donde las gráficas se cortan: se cuentan los cruces.")


# ---------------------------------------------------------------- Argumentar
def t_param(r, l):
    a = r.choice([1, 1, 2, -1]); b, c = r.randint(-4, 4), r.randint(-4, 4); m = r.randint(-3, 3)
    # y = a x² + b x + c ; y = m x + k  →  a x² + (b−m) x + (c−k) = 0
    Dm = (b - m) ** 2
    k0 = F(Dm, 4 * a) + c  # k con Δ = 0
    if k0.denominator != 1: raise Reject
    k0 = int(k0)
    par = "y = " + poly(a, b, c)
    lin = f"y = {lx(m, 0)} + k".replace("y = x + k", "y = x + k") if m != 0 else "y = k"
    lin = "y = " + (lx(m, 0) + " + k" if m != 0 else "k")
    if l == 0:
        stem = f"¿Para qué valor de k el sistema {{ {par} ; {lin} }} tiene exactamente una solución?"
        ans = f"k = {k0}"
        cands = [f"k = {-k0}", f"k = {k0 + 1}", f"k = {k0 - 1}", f"k = {c}", f"k = {k0 + 2}", f"k = {(b - m) ** 2}"]
        ex = f"Se iguala: {poly(a, b - m, c)} − k = 0; Δ = 0 ⟹ k = {k0}."
    elif l == 1:
        two = a > 0
        stem = f"¿Para qué valores de k el sistema {{ {par} ; {lin} }} tiene {'dos soluciones reales distintas' if two else 'dos soluciones reales distintas'}?"
        ans = f"k > {k0}" if a > 0 else f"k < {k0}"
        cands = [f"k < {k0}" if a > 0 else f"k > {k0}", f"k ≥ {k0}" if a > 0 else f"k ≤ {k0}", f"k > {-k0}", f"k = {k0}", f"k > {k0 + 1}" if a > 0 else f"k < {k0 + 1}", f"k ≠ {k0}"]
        ans, cands = (f"k > {k0}", cands) if a > 0 else (f"k < {k0}", cands)
        ex = f"Se necesita Δ > 0: se obtiene {ans}."
    else:
        stem = f"¿Para qué valores de k el sistema {{ {par} ; {lin} }} NO tiene solución real?"
        ans = f"k < {k0}" if a > 0 else f"k > {k0}"
        cands = [f"k > {k0}" if a > 0 else f"k < {k0}", f"k ≤ {k0}" if a > 0 else f"k ≥ {k0}", f"k = {k0}", f"k < {-k0}" if k0 else f"k < 1", f"k < {k0 + 1}" if a > 0 else f"k > {k0 + 1}", f"k ≠ {k0}"]
        ex = f"Se necesita Δ < 0: se obtiene {ans}."
    fig = card([par, lin, "Se iguala y se analiza el discriminante"], 210, 21)
    return make(stem, fig, ans, pick4(ans, cands), Q_ARG, ex)


TRUE_S = ["Una recta y una parábola pueden tener 0, 1 o 2 puntos en común", "Si al igualar las expresiones resulta una cuadrática con Δ < 0, el sistema no tiene solución real",
          "Si la recta es tangente a la parábola, el sistema tiene una única solución", "Las soluciones del sistema son los puntos donde se cortan las gráficas",
          "Una solución del sistema debe cumplir las dos ecuaciones a la vez"]
FALSE_S = ["Una recta y una parábola siempre se cortan en dos puntos", "Si Δ = 0 al igualar las expresiones, el sistema no tiene solución", "Todo sistema no lineal tiene al menos una solución real",
           "Una recta y una parábola pueden tener 3 puntos en común", "Un punto que cumple solo una de las ecuaciones es solución del sistema", "Al igualar las expresiones de y siempre resulta una ecuación de primer grado",
           "Si Δ > 0 el sistema tiene infinitas soluciones"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_S), r.sample(FALSE_S, 4)
        stem = "Sobre un sistema formado por una recta y una parábola, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_S), r.sample(TRUE_S, 4)
        stem = "Sobre un sistema formado por una recta y una parábola, ¿cuál de las siguientes afirmaciones es FALSA?"
    a, b, c = 1, r.randint(-2, 2), r.randint(-4, 0)
    m = r.randint(-1, 2); n = r.randint(0, 3)
    pl = plot2([lambda x: a * x * x + b * x + c, lambda x: m * x + n], -5, 5)
    return make(stem, pl.svg("Parábola y recta"), good, bad, Q_ARG, "Se razona con el discriminante de la ecuación que resulta al igualar las expresiones.")


ERR = ["Olvidó la solución negativa al sacar la raíz cuadrada", "Al obtener y no reemplazó x en una de las ecuaciones", "Cometió un error de signo al igualar y ordenar",
       "Entregó solo los valores de x como solución del sistema", "Cometió un error al factorizar la ecuación cuadrática"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 2, 3])
    if k == 0:
        s = r.randint(2, 9)
        lines = [f"{{ y = x² ; y = {s * s} }}", f"x² = {s * s} ⟹ x = {s}", f"Solución: ({s}, {s * s})"]
    elif k == 1:
        p, q = sorted(r.sample(range(-4, 5), 2))
        lines = [f"{{ y = x² ; y = {p + q}x − {p * q} }}", f"x² − {p + q}x + {p * q} = 0 ⟹ x = {p} o x = {q}".replace("+ -", "− "), f"Solución: ({p}, {p}) y ({q}, {q})"]
    elif k == 2:
        b, c = r.randint(1, 5), r.randint(1, 8)
        lines = [f"{{ y = x² ; y = {b}x + {c} }}", f"x² = {b}x + {c} ⟹ x² + {b}x + {c} = 0", "Se resuelve esa ecuación"]
    elif k == 3:
        p, q = sorted(r.sample(range(-4, 5), 2))
        lines = [f"{{ y = x² ; y = {p + q}x − {p * q} }}", f"x² − {p + q}x + {p * q} = 0 ⟹ x = {p} o x = {q}".replace("+ -", "− "), f"Solución: x = {p} ; x = {q}"]
    else:
        p, q = sorted(r.sample(range(1, 8), 2))
        lines = [f"{{ y = x² ; y = {p + q}x − {p * q} }}", f"x² − {p + q}x + {p * q} = 0", f"(x − {p + 1})(x − {q + 1}) = 0 ⟹ x = {p + 1} o x = {q + 1}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 250, 19), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_vieta(r, l):
    a, b, c = r.choice([1, 1, 2, -1]), r.randint(-4, 4), r.randint(-5, 5)
    r1, r2 = sorted(r.sample(range(-4, 6), 2))
    m = a * (r1 + r2) + b
    n = a * r1 * r1 + b * r1 + c - m * r1
    p = lambda x: a * x * x + b * x + c
    y1, y2 = p(r1), p(r2)
    what = r.choice(["x", "y"]) if l else "x"
    kind = r.choice(["suma", "producto"])
    if what == "x":
        val = r1 + r2 if kind == "suma" else r1 * r2
        cands = [-(r1 + r2), abs(r1 * r2), r1 + r2 + 1, y1 + y2, r2 - r1, m]
        target = f"la {kind} de las abscisas (valores de x)"
    else:
        val = y1 + y2 if kind == "suma" else y1 * y2
        cands = [r1 + r2, r1 * r2, y1 + y2 + 1, -(y1 + y2), (y1 - y2), m * (r1 + r2)]
        target = f"la {kind} de las ordenadas (valores de y)"
    stem = f"Las soluciones del sistema {sysstr(a, b, c, m, n)} son dos puntos. ¿Cuál es {target}?"
    ans = str(val)
    cands = [str(c_) for c_ in cands]
    fig = card([eq_par(a, b, c), eq_lin(m, n), "Suma y producto de las soluciones"], 210, 21)
    return make(stem, fig, ans, pick4(ans, cands), Q_PRO, f"Las soluciones son ({r1}, {y1}) y ({r2}, {y2}); {kind} pedida: {ans}.")


def t_solve_sys(r, l):
    if l == 0:
        S = r.randint(2, 14)
        p, q = sorted(r.sample(range(-6, 12), 2))
        S = p + q
        stem = f"Resuelve el sistema {{ x + y = {S} ; x² + y² = {p * p + q * q} }}."
        sol = [(p, q), (q, p)]
        card_ = [f"x + y = {S}", f"x² + y² = {p * p + q * q}"]
    elif l == 1:
        p, q = r.sample(range(-7, 8), 2)
        d = p - q
        if d == 0: raise Reject
        stem = f"Resuelve el sistema {{ x − y = {d} ; x² + y² = {p * p + q * q} }}."
        sol = [(p, q), (-q, -p)]
        if sol[0] == sol[1]: raise Reject
        card_ = [f"x − y = {d}", f"x² + y² = {p * p + q * q}"]
    else:
        y0 = r.randint(-5, 6); d = r.choice([x for x in range(-5, 6) if x]); x0 = y0 + d
        Dv = x0 * x0 - y0 * y0
        if Dv == 0: raise Reject
        stem = f"Resuelve el sistema {{ x − y = {d} ; x² − y² = {Dv} }}."
        sol = [(x0, y0)]
        card_ = [f"x − y = {d}", f"x² − y² = {Dv}"]
    ans = pts(sol)
    cands = mutate_pts(sol, r)
    if l == 2:
        cands += [pts([(y0, x0)]), pts([(-x0, -y0)]), pts([(x0 + 1, y0 + 1)])]
    card_ = [x.replace("-", "−") for x in card_]
    return make(stem, card(["Sistema no lineal:"] + card_, 210, 21), ans, pick4(ans, cands), Q_PRO,
                "Se resuelve por sustitución (o factorizando x² − y² = (x − y)(x + y)) y se verifican ambas ecuaciones.")


BY_SKILL = {
    Q_RES: [t_line_parab, t_sum_prod],
    Q_MOD: [t_trajectory, t_break_even],
    Q_REP: [t_which_system, t_count],
    Q_ARG: [t_param, t_props, t_error],
    Q_PRO: [t_vieta, t_solve_sys],
}
