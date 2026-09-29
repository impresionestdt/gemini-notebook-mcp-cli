"""Clase 34 (M1) · Figuras planas II: áreas; descomposición y resta de áreas."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import polygon_fig
from clase33 import circle_fig
from num import dstr


def uq(ans, alts, unit=""):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a)) + unit
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def right_mark(x, y, dx=1, dy=-1, u=14):
    return f'<polyline fill="none" stroke="{INK}" stroke-width="2.5" points="{x + dx * u},{y} {x + dx * u},{y + dy * u} {x},{y + dy * u}"/>'


def tri_h(b, h, u, side=None):
    B = 300
    H = min(150, 300 * h / b)
    x0, y0 = 130, 190
    apex = (x0 + B * 0.35, y0 - H)
    body = P([(x0, y0), (x0 + B, y0), apex], FILL) + L(apex[0], apex[1], apex[0], y0, ACC, 4, "9 6") + right_mark(apex[0], y0, -1, -1)
    body += tag(x0 + B / 2, y0 + 26, f"{b} {u}", 16) + tag(apex[0] + 32, (apex[1] + y0) / 2, f"{h} {u}", 16)
    return wrap(560, 240, body, "Triángulo con su base y su altura")


def para_h(b, h, u):
    B = 300
    H = min(140, 300 * h / b)
    x0, y0 = 130, 190
    d = 60
    body = P([(x0, y0), (x0 + B, y0), (x0 + B + d, y0 - H), (x0 + d, y0 - H)], FILL) + L(x0 + d, y0 - H, x0 + d, y0, ACC, 4, "9 6") + right_mark(x0 + d, y0, -1, -1)
    body += tag(x0 + B / 2, y0 + 26, f"{b} {u}", 16) + tag(x0 + d + 34, y0 - H / 2, f"{h} {u}", 16)
    return wrap(560, 240, body, "Paralelogramo con su base y su altura")


def trap_h(b1, b2, h, u):
    B1 = 320
    B2 = 320 * b2 / b1
    H = min(130, 320 * h / b1 * 1.2)
    x0, y0 = 120, 190
    dx = (B1 - B2) / 2
    body = P([(x0, y0), (x0 + B1, y0), (x0 + B1 - dx, y0 - H), (x0 + dx, y0 - H)], FILL) + L(x0 + dx, y0 - H, x0 + dx, y0, ACC, 4, "9 6") + right_mark(x0 + dx, y0, -1, -1)
    body += tag(x0 + B1 / 2, y0 + 26, f"{b1} {u}", 16) + tag(x0 + B1 / 2, y0 - H - 20, f"{b2} {u}", 16) + tag(x0 + dx + 34, y0 - H / 2, f"{h} {u}", 16)
    return wrap(560, 250, body, "Trapecio con sus bases y su altura")


# ---------------------------------------------------------------- Resolver problemas
def t_area(r, l):
    u = r.choice(["cm", "m"])
    kind = r.choice(["rect", "tri", "para", "trap", "circ"] if l else ["rect", "tri", "para"])
    if kind == "rect":
        a, b = r.randint(3, 20), r.randint(3, 20)
        if a == b:
            raise Reject
        fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} {u}", f"{b} {u}", None, None])
        val = a * b
        alts = [2 * (a + b), a + b, val + a, val - b, a * a]
        stem = "¿Cuál es el área del rectángulo de la figura?"
        ex = f"A = {a}·{b} = {val} {u}²."
    elif kind == "tri":
        b, h = r.choice([(8, 5), (10, 6), (12, 7), (9, 8), (14, 5), (6, 6)])
        b, h = b * r.choice([1, 2]), h
        fig = tri_h(b, h, u)
        val = F(b * h, 2)
        alts = [b * h, b + h, F(b * h, 3), val + b, 2 * (b + h)]
        stem = "¿Cuál es el área del triángulo de la figura?"
        ex = f"A = base·altura/2 = {b}·{h}/2 = {fs(val)} {u}²."
    elif kind == "para":
        b, h = r.randint(5, 20), r.randint(3, 12)
        fig = para_h(b, h, u)
        val = b * h
        alts = [F(b * h, 2), b + h, 2 * (b + h), val + b, val - h]
        stem = "¿Cuál es el área del paralelogramo de la figura?"
        ex = f"A = base·altura = {b}·{h} = {val} {u}²."
    elif kind == "trap":
        b1, b2, h = r.choice([(12, 6, 4), (14, 8, 5), (16, 10, 6), (10, 4, 6), (20, 12, 5)])
        fig = trap_h(b1, b2, h, u)
        val = F((b1 + b2) * h, 2)
        alts = [(b1 + b2) * h, b1 * b2, b1 + b2 + h, val + h, F(b1 * h, 2)]
        stem = "¿Cuál es el área del trapecio de la figura?"
        ex = f"A = (B + b)·h/2 = ({b1} + {b2})·{h}/2 = {fs(val)} {u}²."
    else:
        rad = r.choice([2, 3, 4, 5, 6, 7, 10])
        fig = circle_fig(f"r = {rad} {u}")
        stem = f"¿Cuál es el área del círculo de radio {rad} {u}? (Expresa el resultado en función de π.)"
        ans = f"{rad * rad}π {u}²"
        alts = [f"{2 * rad}π {u}²", f"{rad}π {u}²", f"{2 * rad * rad}π {u}²", f"{4 * rad * rad}π {u}²", f"{rad * rad + 2}π {u}²"]
        al = [x for x in dict.fromkeys(alts) if x != ans]
        return make(stem, fig, ans, al[:4], Q_RES, f"A = πr² = π·{rad}² = {rad * rad}π {u}².")
    ans = f"{fs(F(val))} {u}²"
    al = uq(ans, [f"{fs(F(t))} {u}²" for t in alts if F(t) > 0 and F(t) != val])
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_decomp(r, l):
    W, H = r.randint(10, 24), r.randint(8, 20)
    a, b = r.randint(3, W - 3), r.randint(3, H - 3)
    kind = r.choice(["L", "hole"])
    if kind == "L":
        pts = [(0, 0), (W, 0), (W, H - b), (W - a, H - b), (W - a, H), (0, H)]
        labs = [f"{W} m", None, f"{a} m", f"{b} m", None, f"{H} m"]
        fig = polygon_fig(pts, labs, h=300)
        val = W * H - a * b
        stem = "La figura muestra un terreno en forma de L (las medidas están en metros). ¿Cuál es su área?"
        alts = [W * H, a * b, W * H + a * b, (W - a) * H, val + a]
        ex = f"Área = rectángulo grande − esquina cortada = {W}·{H} − {a}·{b} = {val} m²."
    else:
        wall = R(120, 40, 320, 170, FILL, NAVY, 3) + R(250, 90, 120, 70, WHITE, NAVY, 3)
        x0 = 120
        body = wall + tag(280, 235, f"{W} m", 16) + tag(90, 125, f"{H} m", 16) + tag(310, 125, f"{a} m × {b} m", 15)
        fig = wrap(560, 260, body, "Rectángulo con un hueco rectangular")
        val = W * H - a * b
        stem = f"Un patio rectangular de {W} m por {H} m tiene una piscina rectangular de {a} m por {b} m en su interior. ¿Cuál es el área del patio sin considerar la piscina?"
        alts = [W * H, a * b, W * H + a * b, 2 * (W + H) - 2 * (a + b), val + a]
        ex = f"Área = {W}·{H} − {a}·{b} = {val} m²."
    ans = f"{val} m²"
    al = uq(ans, [f"{t} m²" for t in alts if t > 0 and t != val])
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_ring(r, l):
    R_, r_ = r.choice([(5, 3), (6, 4), (10, 6), (8, 5), (7, 2), (9, 6), (12, 8)])
    body = f'<circle cx="280" cy="115" r="95" fill="{FILL2}" stroke="{NAVY}" stroke-width="4"/><circle cx="280" cy="115" r="50" fill="{WHITE}" stroke="{NAVY}" stroke-width="4"/>'
    body += L(280, 115, 375, 115, ACC, 4) + L(280, 115, 230, 115, INK, 3) + tag(445, 115, f"R = {R_} cm", 15) + tag(135, 115, f"r = {r_} cm", 15)
    fig = wrap(560, 240, body, "Corona circular")
    val = R_ * R_ - r_ * r_
    stem = f"Una corona circular está limitada por dos circunferencias concéntricas de radios {R_} cm y {r_} cm. ¿Cuál es su área? (Expresa el resultado en función de π.)"
    ans = f"{val}π cm²"
    alts = [f"{(R_ - r_) ** 2}π cm²", f"{R_ * R_ + r_ * r_}π cm²", f"{2 * (R_ - r_)}π cm²", f"{R_ - r_}π cm²", f"{val + R_}π cm²"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"A = π({R_}² − {r_}²) = {val}π cm².")


# ---------------------------------------------------------------- Modelar
def t_paint(r, l):
    a, b = r.randint(3, 12), r.randint(2, 5)
    door_w, door_h = 1, 2
    price = r.choice([2000, 3500, 5000, 6500])
    nwalls = r.choice([1, 2, 4])
    fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} m", f"{b} m", None, None])
    stem = f"Se quiere pintar {'una pared' if nwalls == 1 else f'{nwalls} paredes iguales'} rectangular{'es' if nwalls > 1 else ''} de {a} m de largo y {b} m de alto. Si el m² cuesta ${price:,} pintado, ¿cuánto cuesta el trabajo?".replace(",", ".")
    val = a * b * nwalls * price
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    ans = f(val)
    alts = [2 * (a + b) * nwalls * price, a * b * price, (a + b) * nwalls * price, val + price, a * b * nwalls]
    al = list(dict.fromkeys(f(t) for t in alts if t != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Área = {a}·{b}·{nwalls} = {a * b * nwalls} m²; costo = {a * b * nwalls}·{price}.")


def t_tiles(r, l):
    a, b = r.randint(4, 12), r.randint(3, 10)
    t = r.choice([25, 50, 20, 40])
    if (a * 100 * b * 100) % (t * t):
        raise Reject
    fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} m", f"{b} m", None, None])
    n = (a * 100 * b * 100) // (t * t)
    stem = f"Un piso rectangular de {a} m por {b} m se cubre con baldosas cuadradas de {t} cm de lado, sin cortes ni pérdidas. ¿Cuántas baldosas se necesitan?"
    ans = f"{n:,}".replace(",", ".")
    alts = [n // 100 if n % 100 == 0 else n + 10, (a * b * 100) // t, a * b, n * 4 if n * 4 != n else n + 5, n // 2]
    al = list(dict.fromkeys(f"{t_:,}".replace(",", ".") for t_ in alts if t_ > 0 and t_ != n))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Área del piso: {a * b} m² = {a * b * 10000} cm²; cada baldosa: {t * t} cm²; n = {n}.")


def t_path(r, l):
    a, b, w = r.randint(6, 20), r.randint(5, 15), r.randint(1, 3)
    body = R(120, 40, 320, 190, FILL2, NAVY, 3) + R(120 + 40, 40 + 40, 320 - 80, 190 - 80, FILL, NAVY, 3) + T(280, 140, f"{a} m × {b} m", 20) + tag(150, 60, f"{w} m", 14)
    fig = wrap(560, 260, body, "Jardín rodeado de un camino")
    val = (a + 2 * w) * (b + 2 * w) - a * b
    stem = f"Un jardín rectangular de {a} m por {b} m está rodeado por un camino de {w} m de ancho. ¿Cuál es el área del camino?"
    ans = f"{val} m²"
    alts = [2 * w * (a + b), (a + 2 * w) * (b + 2 * w), w * (a + b), val + w * w, val - 4 * w * w if val > 4 * w * w else val + 2 * w]
    al = uq(ans, [f"{t} m²" for t in alts if t > 0 and t != val])
    return make(stem, fig, ans, al[:4], Q_MOD, f"Área total − área del jardín = {a + 2 * w}·{b + 2 * w} − {a}·{b} = {val} m².")


# ---------------------------------------------------------------- Representar
def grid_poly(r):
    pts = r.choice([[(0, 0), (4, 0), (4, 3), (0, 3)], [(0, 0), (5, 0), (2, 4)], [(0, 0), (4, 0), (6, 3), (2, 3)], [(1, 0), (5, 0), (4, 3), (2, 3)], [(0, 0), (6, 0), (6, 2), (3, 2), (3, 4), (0, 4)], [(0, 0), (5, 0), (5, 3), (2, 3)]])
    return pts


def shoelace(pts):
    n = len(pts)
    return abs(sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))) / 2


def t_grid(r, l):
    pts = grid_poly(r)
    cs = 40
    ox, oy = 100, 200
    body = ""
    for i in range(0, 9):
        body += L(ox + i * cs, oy - 4 * cs - 10, ox + i * cs, oy + 10, "#CBD5E1", 1)
    for j in range(0, 6):
        body += L(ox - 10, oy - j * cs, ox + 8 * cs + 10, oy - j * cs, "#CBD5E1", 1)
    body += P([(ox + x * cs, oy - y * cs) for x, y in pts], FILL3, NAVY, 3.5)
    fig = wrap(560, 240, body, "Polígono dibujado sobre una cuadrícula")
    A = shoelace(pts)
    stem = "El polígono está dibujado sobre una cuadrícula de cuadrados de 1 unidad de lado. ¿Cuál es su área en unidades cuadradas?"
    ans = fs(F(A).limit_denominator(2))
    alts = [A + 1, A - 1, A * 2, A + 2, A + F(1, 2)]
    al = uq(ans, [fs(F(t).limit_denominator(2)) for t in alts if t > 0 and F(t) != A])
    return make(stem, fig, ans, al[:4], Q_REP, "Se descompone o se completa la figura en rectángulos y triángulos con la cuadrícula.")


def t_expr_area(r, l):
    a, b = r.randint(1, 5), r.randint(1, 6)
    fig = polygon_fig([(0, 0), (10, 0), (10, 5), (0, 5)], [f"x + {b}", f"{a}x", None, None])
    stem = f"Un rectángulo tiene lados de longitud (x + {b}) y {a}x. ¿Qué expresión representa su área?"
    ans = f"{a}x² + {a * b}x"
    alts = [f"{a}x² + {b}", f"{a + 1}x + {b}", f"{2 * a + 2}x + {2 * b}", f"{a}x + {a * b}", f"{a}x² + {a + b}x"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"A = {a}x·(x + {b}) = {ans}.")


def t_split_expr(r, l):
    a, b, c, d = r.randint(6, 12), r.randint(3, 6), r.randint(2, 5), r.randint(4, 8)
    body = R(120, 40, 300, 100, FILL, NAVY, 3) + R(120, 140, 130, 90, FILL2, NAVY, 3) + L(250, 140, 420, 140, ACC, 3, "8 6")
    body += tag(270, 24, f"{a} m", 15) + tag(95, 90, f"{b} m", 15) + tag(185, 250, f"{c} m", 15) + tag(95, 185, f"{d} m", 15)
    fig = wrap(560, 275, body, "Figura compuesta por dos rectángulos")
    stem = "La figura está formada por dos rectángulos: uno de la parte superior y otro de la parte inferior izquierda. ¿Qué expresión permite calcular el área total?"
    ans = f"{a}·{b} + {c}·{d}"
    alts = [f"{a}·{b} − {c}·{d}", f"({a} + {c})·({b} + {d})", f"{a}·{b}·{c}·{d}", f"2·({a} + {b}) + 2·({c} + {d})", f"{a}·{d} + {b}·{c}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, "El área total es la suma de las áreas de las dos regiones rectangulares.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.randint(4, 12), r.randint(3, 9)
    if k == 0:
        return [f"Triángulo de base {2 * a} cm y altura {b} cm", f"Área = {2 * a}·{b} = {2 * a * b} cm²"], "Olvidó dividir por 2: el área del triángulo es base·altura/2", \
            ["Sumó la base y la altura en lugar de multiplicarlas entre sí para obtener el área", "Multiplicó la base por la altura y luego duplicó el resultado obtenido", "Usó la fórmula del perímetro en lugar de la fórmula del área del triángulo", "Dividió la base por 2 y también dividió la altura por 2 antes de multiplicar"]
    if k == 1:
        return [f"Rectángulo de {a} m por {b} m", f"Área = 2({a} + {b}) = {2 * (a + b)} m²"], "Calculó el perímetro: el área de un rectángulo es el producto de sus lados", \
            ["Sumó los dos lados sin duplicar el resultado obtenido para calcular el área", "Multiplicó los lados y luego los sumó al resultado para obtener el área", "Elevó al cuadrado uno de los lados y no consideró el otro lado en el cálculo", "Usó el perímetro dividido por dos, que corresponde a la suma de dos lados"]
    if k == 2:
        return [f"Círculo de diámetro {2 * a} cm", f"Área = π · {2 * a}² = {4 * a * a}π cm²"], "Usó el diámetro como si fuera el radio: el área es π·r², con r = a", \
            ["Usó el radio como si fuera el diámetro y por eso dividió el resultado por cuatro", "Multiplicó el diámetro por π y no elevó ningún valor al cuadrado en el cálculo", "Calculó la longitud de la circunferencia en lugar de calcular el área del círculo", "Elevó al cuadrado solo el número π y multiplicó por el diámetro al final"]
    if k == 3:
        return [f"Trapecio de bases {2 * a} y {a} cm, altura {b} cm", f"Área = {2 * a}·{a}·{b}/2"], "Multiplicó las bases: el área del trapecio es (B + b)·h/2, con la suma de las bases", \
            ["Usó solo la base mayor y la altura del trapecio para calcular el área", "Sumó las bases pero no multiplicó por la altura al calcular el área del trapecio", "Dividió las bases por la altura en lugar de sumarlas antes de multiplicar", "Restó las bases entre sí en lugar de sumarlas antes de multiplicar por la altura"]
    return ["1 m² = 100 cm²", f"Un piso de {a} m² son {a * 100} cm²"], f"Confundió las unidades: 1 m² = 100 · 100 = 10.000 cm², por lo que {a} m² son {a * 10000} cm²", \
        ["Convirtió los metros cuadrados a centímetros lineales y no a centímetros cuadrados", "Dividió por 100 en lugar de multiplicar por 10.000 al cambiar de unidades", "Multiplicó por 1.000 porque 1 m = 1.000 mm sin considerar que son dos dimensiones", "Sumó 100 al valor en metros cuadrados para pasar a centímetros cuadrados"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_double(r, l):
    a, b = r.randint(3, 9), r.randint(2, 8)
    fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} m", f"{b} m", None, None])
    k = r.choice([2, 3])
    stem = f"Un rectángulo de {a} m por {b} m aumenta cada uno de sus lados al {'doble' if k == 2 else 'triple'}. ¿Qué ocurre con su área?"
    ans = f"Se multiplica por {k * k}"
    alts = [f"Se multiplica por {k}", f"Se multiplica por {2 * k}", f"Se suma {k * k} unidades cuadradas", f"Se multiplica por {k * k * k}"]
    return make(stem, fig, ans, alts, Q_ARG, f"Cada lado se multiplica por {k}: el área se multiplica por {k}·{k} = {k * k}.")


TRUE = ["El área de un rectángulo de lados a y b es a·b", "El área de un triángulo es la mitad del producto de su base por su altura", "El área de un paralelogramo es su base por su altura",
        "El área de un círculo de radio r es πr²", "Un m² equivale a 10.000 cm²", "Para calcular el área de una figura irregular se puede descomponer en figuras conocidas"]
FALSE = ["El área de un rectángulo de lados a y b es 2(a + b)", "El área de un triángulo es el producto de su base por su altura", "El área de un paralelogramo es la suma de sus lados",
         "El área de un círculo de radio r es 2πr", "Un m² equivale a 100 cm²", "Si se duplican los lados de una figura, su área también se duplica"]


def _fig(r):
    b, h = r.randint(6, 14), r.randint(4, 8)
    return tri_h(b, h, "cm")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre áreas es verdadera?", "Sobre el área de figuras planas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las fórmulas de área.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre áreas es falsa?", "Sobre el área de figuras planas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las fórmulas de área.")


BY_SKILL = {
    Q_RES: [t_area, t_decomp, t_ring],
    Q_MOD: [t_paint, t_tiles, t_path],
    Q_REP: [t_grid, t_expr_area, t_split_expr],
    Q_ARG: [t_error, t_double, t_true, t_false],
}
