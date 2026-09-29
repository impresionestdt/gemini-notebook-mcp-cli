"""Clase 13 · Repaso integrado de Álgebra y Funciones M2 (contraste entre modelos)."""
from fractions import Fraction as F
from math import log
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase10 import nice, fexp, bs
import clase05, clase06, clase07, clase09, clase10, clase11, clase12

FAM = ["Función lineal", "Función cuadrática", "Función exponencial", "Función potencia con exponente negativo", "Función logarítmica"]
FAMG = ["Función lineal", "Función cuadrática", "Función potencia cúbica", "Función exponencial", "Función logarítmica"]


def table_svg(xs, ys):
    n = len(xs)
    w = 500 / (n + 1)
    body = R(30, 50, 500, 50, "#E0F2FE") + R(30, 100, 500, 50, WHITE) + T(30 + w / 2, 83, "x", 22) + T(30 + w / 2, 133, "y", 22)
    for i, (x, y) in enumerate(zip(xs, ys)):
        body += T(30 + w * (i + 1.5), 83, fs(x), 20) + T(30 + w * (i + 1.5), 133, fs(y), 20)
    for i in range(n + 2):
        body += L(30 + w * i, 50, 30 + w * i, 150, NAVY, 2)
    return wrap(560, 190, body, "Tabla de valores")


# ---------------------------------------------------------------- Argumentar / Representar
def t_family_table(r, l):
    fams = [0, 1, 2] if l == 0 else [0, 1, 2, 3, 4]
    k = r.choice(fams)
    off = 0 if l < 2 else r.choice([-3, -2, 2, 3, 5])
    if k == 0:
        a = r.choice([-4, -3, -2, 2, 3, 4, 5]); b = r.randint(-5, 8)
        xs = [0, 1, 2, 3, 4]; ys = [a * x + b for x in xs]
    elif k == 1:
        a = r.choice([-2, -1, 1, 2, 3]); b = r.randint(-4, 4); c = r.randint(-4, 6)
        xs = [0, 1, 2, 3, 4]; ys = [a * x * x + b * x + c for x in xs]
    elif k == 2:
        a = r.choice([1, 2, 3, 5]); b = r.choice([2, 3, 4])
        xs = [0, 1, 2, 3]; ys = [a * b ** x + off for x in xs]
    elif k == 3:
        kk = r.choice([12, 24, 36, 60]); xs = [1, 2, 3, 4]
        ys = [F(kk, x) for x in xs]
        if any(v.denominator != 1 for v in ys): raise Reject
        ys = [int(v) + off for v in ys]
    else:
        a = r.choice([1, 2, 3, -1, -2]); xs = [1, 2, 4, 8]
        ys = [a * int(log(x, 2) + 0.5) + off for x in xs]
    stem = "La tabla muestra datos de una magnitud. ¿Qué tipo de función los modela mejor?"
    ex = {0: "Las diferencias entre valores consecutivos son constantes.", 1: "Las segundas diferencias son constantes (y no nulas).",
          2: "Los cocientes entre valores consecutivos (menos el desplazamiento) son constantes.", 3: "El producto x·y es constante (proporcionalidad inversa).",
          4: "Al duplicar x, y aumenta en una cantidad constante."}[k]
    return make(stem, table_svg(xs, ys), FAM[k], [x for i, x in enumerate(FAM) if i != k], Q_ARG, ex)


def t_family_graph(r, l):
    k = r.choice([0, 1, 2, 3, 4])
    s = 1 if l == 0 else r.choice([1, -1])
    if k == 0:
        m = r.choice([1, 2, 3]) * s; n = r.randint(-3, 3)
        f = lambda x: m * x + n; x0, x1 = -4, 4
    elif k == 1:
        h, c = r.randint(-2, 2), r.randint(-3, 3)
        f = lambda x: s * (x - h) ** 2 + c; x0, x1 = -5, 5
    elif k == 2:
        h, c = (0, 0) if l == 0 else (r.randint(-2, 2), r.randint(-3, 3))
        f = lambda x: s * (x - h) ** 3 / 2 + c; x0, x1 = -4, 4
    elif k == 3:
        b = r.choice([2, 3, F(1, 2)]) if l else 2
        c = 0 if l < 2 else r.choice([-2, -1, 1, 2])
        f = lambda x: float(b) ** x * s + c; x0, x1 = -4, 4
    else:
        b = r.choice([2, 3]) if l < 2 else r.choice([2, 3, F(1, 2)])
        h = 0 if l < 2 else r.randint(-2, 2)
        f = lambda x: s * log(x - h) / log(float(b)); x0, x1 = h - 1, h + 8
    ys = []
    for i in range(81):
        x = x0 + (x1 - x0) * i / 80
        try: ys.append(f(x))
        except Exception: pass
    lo, hi = max(min(ys), -12), min(max(ys), 12)
    pad = max(2, 0.12 * (hi - lo))
    lo, hi = min(lo, -pad), max(hi, pad)
    pl = Plot(560, 280, x0, x1, lo, hi)
    pl.axes(1 if x1 - x0 <= 10 else 2, nice((hi - lo) / 6))
    pl.curve(f, x0 if k != 4 else h + 0.02, x1)
    return make("¿Qué tipo de función representa la gráfica?", pl.svg("Gráfica de una función"), FAMG[k], [x for i, x in enumerate(FAMG) if i != k], Q_REP,
                "Se observa la forma: recta, parábola, curva en S, crecimiento o decaimiento con asíntota horizontal, o crecimiento lento con asíntota vertical.")


# ---------------------------------------------------------------- Modelar
def t_compare(r, l):
    p, q = r.randint(20, 100), r.randint(8, 30)
    c, d = r.randint(1, 3), r.randint(0, 40)
    e = r.choice([1, 2, 3, 5]); b = 2 if l < 2 else r.choice([2, 3])
    fA = lambda t: p + q * t
    fB = lambda t: c * t * t + d
    fC = lambda t: e * b ** t
    T0 = r.choice([10, 12]) if l < 2 else r.choice([8, 9, 10])
    cc = "" if c == 1 else c
    vals = {"A": fA(T0), "B": fB(T0), "C": fC(T0)}
    if len(set(vals.values())) < 3: raise Reject
    best = max(vals.values())
    if l == 0:
        stem = f"El costo del plan A es {p} + {q}t, el del plan B es {cc}t² + {d}, y el del plan C es {e}·{b}ᵗ (t en meses). ¿Cuánto cuesta el plan más caro en t = {T0}?"
    else:
        stem = f"Tres planes tienen costos (en miles de pesos) A(t) = {p} + {q}t, B(t) = {cc}t² + {d} y C(t) = {e}·{b}ᵗ. ¿Cuál es el costo del plan más caro en el mes t = {T0}?"
    ans = f"{best:,}".replace(",", ".")
    others = sorted(v for v in vals.values() if v != best)
    cands = [f"{o:,}".replace(",", ".") for o in others] + [f"{best + q:,}".replace(",", "."), f"{best - c:,}".replace(",", "."), f"{fC(T0 - 1):,}".replace(",", "."), f"{best + 10:,}".replace(",", ".")]
    tt = 6
    ymax = max(fA(tt), fB(tt), fA(tt) + 20) * 1.5
    pl = Plot(560, 280, 0, tt, 0, ymax)
    pl.axes(1, nice(ymax / 6))
    for f, col in ((fA, ACC), (fB, NAVY), (fC, "#475569")):
        pl.curve(f, 0, tt, col, 4)
    for i, (nm, col) in enumerate((("A", ACC), ("B", NAVY), ("C", "#475569"))):
        pl.parts.append(f'<rect x="{pl.ml + 8}" y="{6 + 28 * i}" width="60" height="24" rx="6" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/>' + L(pl.ml + 12, 18 + 28 * i, pl.ml + 32, 18 + 28 * i, col, 4) + T(pl.ml + 40, 23 + 28 * i, nm, 15, "start"))
    return make(stem, pl.svg("Tres planes: lineal, cuadrático y exponencial"), ans, pick4(ans, cands), Q_MOD,
                f"A({T0}) = {vals['A']}, B({T0}) = {vals['B']}, C({T0}) = {vals['C']}: el mayor es {best}.")


# ---------------------------------------------------------------- Resolver
def t_intersections(r, l):
    ns = {0: [2, 3], 1: [2, 3], 2: [2, 3, 4]}[l]
    for _ in range(400):
        a1, n = r.choice([1, 2, 3]), r.choice(ns)
        b = r.choice([2, 3]); a2 = r.choice([1, 2, 3, 4]); d = r.choice([0, 0, -1, 1, 2, -2])
        f = lambda x: a1 * F(x) ** n
        g = lambda x: a2 * F(b) ** x + d
        sol = [x for x in range(-3, 9) if f(x) == g(x)]
        if 1 <= len(sol) <= 3: break
    else:
        raise Reject
    pr = lambda L_: " y ".join(f"x = {v}" for v in L_)
    ans = pr(sol)
    cands = [pr([-v for v in sol]), pr([v + 1 for v in sol]), pr(sol[:-1]) if len(sol) > 1 else pr([sol[0] + 2]), pr(sol + [max(sol) + 2]), pr([v * 2 for v in sol]), pr([v - 1 for v in sol]), pr(sorted(set(sol + [0]))) if 0 not in sol else pr([v + 3 for v in sol])]
    tx = lambda a, e: (f"{a}·" if a != 1 else "") + f"x{'²' if e == 2 else '³' if e == 3 else '⁴'}"
    fs_ = tx(a1, n); gs_ = fexp(a2, b, d)
    x0 = min(sol) - 3
    xr = max(sol) + 3
    ymax = max(float(f(x)) for x in sol) * 2.2 + 6
    pl = Plot(560, 280, x0, xr, -max(3, ymax * 0.08), ymax)
    pl.axes(1 if xr <= 10 else 2, nice(ymax / 6))
    pl.curve(lambda x: float(a1) * x ** n, x0, xr, ACC, 4)
    pl.curve(lambda x: float(a2) * float(b) ** x + d, x0, xr, NAVY, 4)
    return make(f"Se grafican y = {fs_} (rojo) e y = {gs_} (azul). ¿Para qué valores enteros de x se cumple {fs_} = {gs_}?", pl.svg("Potencia y exponencial"), ans, pick4(ans, cands), Q_RES,
                "Se evalúan ambas expresiones en los enteros cercanos a los cruces del gráfico y se comprueba la igualdad.")


BY_SKILL = {
    Q_RES: [t_intersections, clase05.t_param_disc, clase06.t_vertex, clase09.t_inv_value, clase10.t_params, clase12.t_line_parab],
    Q_MOD: [t_compare, clase06.t_optim, clase10.t_model, clase12.t_break_even, clase06.t_proj],
    Q_REP: [t_family_graph, clase07.t_shift, clase11.t_graph_formula, clase09.t_bij_graph, clase06.t_transform],
    Q_ARG: [t_family_table, clase07.t_props, clase09.t_which_inv, clase10.t_props, clase12.t_props],
    Q_PRO: [clase05.t_solve, clase06.t_complete, clase10.t_simplify, clase11.t_inverse, clase07.t_solve_pow],
}
