"""Clase 33 (M1) · Figuras planas I: perímetros y cercos de terrenos."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import polygon_fig
from clase13 import co
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


def circle_fig(lab, kind="r"):
    body = f'<circle cx="280" cy="115" r="90" fill="{FILL}" stroke="{NAVY}" stroke-width="4"/>'
    if kind == "r":
        body += L(280, 115, 370, 115, ACC, 4) + C(280, 115, 5, INK, INK, 1) + tag(325, 92, lab, 17)
    else:
        body += L(190, 115, 370, 115, ACC, 4) + C(280, 115, 5, INK, INK, 1) + tag(280, 92, lab, 17)
    return wrap(560, 230, body, "Circunferencia con su radio o diámetro")


# ---------------------------------------------------------------- Resolver problemas
def t_perim(r, l):
    kind = r.choice(["rect", "square", "tri", "trap", "para", "hex"] if l else ["rect", "square", "tri"])
    u = r.choice(["cm", "m"])
    if kind == "rect":
        a, b = r.randint(3, 20), r.randint(3, 20)
        if a == b:
            raise Reject
        fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} {u}", f"{b} {u}", None, None])
        val = 2 * (a + b)
        alts = [a * b, a + b, 2 * a + b, a + 2 * b if a + 2 * b != val else val + 2, val + a]
        stem = "¿Cuál es el perímetro del rectángulo de la figura?"
        ex = f"P = 2·({a} + {b}) = {val} {u}."
    elif kind == "square":
        a = r.randint(2, 25)
        fig = polygon_fig([(0, 0), (a, 0), (a, a), (0, a)], [f"{a} {u}", None, None, None])
        val = 4 * a
        alts = [a * a, 2 * a, 3 * a, a + a * a, val + a]
        stem = "¿Cuál es el perímetro del cuadrado de la figura?"
        ex = f"P = 4·{a} = {val} {u}."
    elif kind == "tri":
        a, b, c = r.choice([(6, 8, 10), (5, 5, 6), (7, 9, 12), (10, 13, 15), (8, 8, 8), (9, 12, 15), (13, 14, 15)])
        s = 1
        x = (b * b + c * c - a * a) / (2 * c)
        y = math.sqrt(max(b * b - x * x, 0.01))
        fig = polygon_fig([(0, 0), (c, 0), (x, y)], [f"{c} {u}", f"{a} {u}", f"{b} {u}"])
        val = a + b + c
        alts = [(a + b + c) // 2 if (a + b + c) % 2 == 0 else val + 1, a + b, a * b, val + c, 2 * val]
        stem = "¿Cuál es el perímetro del triángulo de la figura?"
        ex = f"P = {a} + {b} + {c} = {val} {u}."
    elif kind == "trap":
        b1, b2, h, s1, s2 = r.choice([(12, 6, 4, 5, 5), (14, 8, 4, 5, 5), (16, 10, 4, 5, 5), (20, 8, 8, 10, 10)])
        d = (b1 - b2) / 2
        fig = polygon_fig([(0, 0), (b1, 0), (b1 - d, h), (d, h)], [f"{b1} {u}", f"{s1} {u}", f"{b2} {u}", f"{s2} {u}"])
        val = b1 + b2 + s1 + s2
        alts = [b1 + b2 + h, (b1 + b2) * h // 2, val + h, b1 + b2 + 2 * h, val - s1]
        stem = "¿Cuál es el perímetro del trapecio isósceles de la figura?"
        ex = f"P = {b1} + {s1} + {b2} + {s2} = {val} {u}."
    elif kind == "para":
        a, b, h = r.choice([(10, 6, 4), (12, 7, 5), (9, 5, 4), (14, 8, 6)])
        d = math.sqrt(max(b * b - h * h, 1))
        fig = polygon_fig([(0, 0), (a, 0), (a + d, h), (d, h)], [f"{a} {u}", f"{b} {u}", f"{a} {u}", f"{b} {u}"])
        val = 2 * (a + b)
        alts = [a * h, a + b, 2 * (a + h), val + h, a * b]
        stem = "¿Cuál es el perímetro del paralelogramo de la figura?"
        ex = f"P = 2·({a} + {b}) = {val} {u}."
    else:
        a = r.randint(3, 12)
        pts = [(math.cos(math.radians(60 * i)) * 3, math.sin(math.radians(60 * i)) * 3) for i in range(6)]
        fig = polygon_fig(pts, [f"{a} {u}", None, None, None, None, None])
        val = 6 * a
        alts = [5 * a, 4 * a, 3 * a, 6 * a + a, 2 * 6]
        stem = "La figura es un hexágono regular. ¿Cuál es su perímetro?"
        ex = f"P = 6·{a} = {val} {u}."
    ans = f"{val} {u}"
    al = uq(ans, [f"{fs(F(t))} {u}" for t in alts if F(t) > 0 and F(t) != val])
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_missing_side(r, l):
    u = r.choice(["cm", "m"])
    kind = r.choice(["rect", "tri", "sq"])
    if kind == "rect":
        a = r.randint(4, 20)
        b = r.randint(2, 15)
        if a == b:
            raise Reject
        P_ = 2 * (a + b)
        fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} {u}", "x", None, None])
        stem = f"Un rectángulo tiene un lado de {a} {u} y un perímetro de {P_} {u}. ¿Cuánto mide el otro lado x?"
        val = b
        alts = [P_ - a, P_ // 2, P_ - 2 * a + a, b + 2, a - b if a > b else b + 3]
    elif kind == "tri":
        a, b, c = r.choice([(6, 8, 10), (7, 9, 12), (10, 13, 15), (9, 12, 15)])
        x = (b * b + c * c - a * a) / (2 * c)
        y = math.sqrt(max(b * b - x * x, 0.01))
        P_ = a + b + c
        fig = polygon_fig([(0, 0), (c, 0), (x, y)], [f"{c} {u}", "x", f"{b} {u}"])
        stem = f"Un triángulo tiene lados de {c} {u}, {b} {u} y x, y su perímetro es {P_} {u}. ¿Cuánto mide x?"
        val = a
        alts = [P_ - c, P_ - b, c - b, a + 2, P_ // 2]
    else:
        a = r.randint(3, 25)
        P_ = 4 * a
        fig = card([f"Cuadrado de perímetro {P_} {u}"], 110, 22)
        stem = f"Un cuadrado tiene un perímetro de {P_} {u}. ¿Cuánto mide cada lado?"
        val = a
        alts = [P_ // 2, P_ - 4, a * a, a + 2, P_ // 3 if P_ % 3 == 0 else a + 4]
    ans = f"{val} {u}"
    al = uq(ans, [f"{fs(F(t))} {u}" for t in alts if F(t) > 0 and F(t) != val])
    return make(stem, fig, ans, al[:4], Q_RES, f"Se resta al perímetro los lados conocidos y se divide según corresponda: {val} {u}.")


def t_circle(r, l):
    rad = r.choice([2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 20])
    u = r.choice(["cm", "m"])
    kind = r.choice(["pi", "num", "inv"] if l else ["pi", "num"])
    if kind == "pi":
        fig = circle_fig(f"r = {rad} {u}")
        stem = f"¿Cuál es la longitud de la circunferencia de radio {rad} {u}? (Expresa el resultado en función de π.)"
        ans = f"{2 * rad}π {u}"
        alts = [f"{rad}π {u}", f"{rad * rad}π {u}", f"{4 * rad}π {u}", f"{2 * rad * rad}π {u}", f"{rad + 2}π {u}"]
        ex = f"L = 2πr = 2π·{rad} = {2 * rad}π {u}."
        al = [x for x in dict.fromkeys(alts) if x != ans]
        return make(stem, fig, ans, al[:4], Q_RES, ex)
    if kind == "num":
        fig = circle_fig(f"d = {2 * rad} {u}", "d")
        val = F(314, 100) * 2 * rad
        stem = f"¿Cuál es la longitud de una circunferencia de diámetro {2 * rad} {u}? (Usa π = 3,14.)"
        ans = f"{dstr(val)} {u}".replace(",00", "")
        alts = [F(314, 100) * rad, F(314, 100) * 4 * rad, F(314, 100) * rad * rad, F(314, 100) * 2 * rad + 2, val + F(314, 100)]
        al = [f"{dstr(F(t))} {u}" for t in alts if F(t) != val]
        return make(stem, fig, ans, list(dict.fromkeys(al))[:4], Q_RES, f"L = π·d = 3,14·{2 * rad} = {dstr(val)} {u}.")
    L_ = 2 * rad
    fig = card([f"Circunferencia de longitud {L_}π {u}"], 110, 22)
    stem = f"Una circunferencia tiene una longitud de {L_}π {u}. ¿Cuánto mide su radio?"
    ans = f"{rad} {u}"
    alts = [f"{L_} {u}", f"{rad * 2 + 2} {u}", f"{rad // 2 + 1} {u}", f"{L_ * 2} {u}", f"{rad + 1} {u}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"2πr = {L_}π ⟹ r = {rad} {u}.")


# ---------------------------------------------------------------- Modelar
def t_lshape(r, l):
    W, H = r.randint(10, 30), r.randint(8, 24)
    a, b = r.randint(3, W - 3), r.randint(3, H - 3)
    pts = [(0, 0), (W, 0), (W, H - b), (W - a, H - b), (W - a, H), (0, H)]
    labs = [f"{W} m", f"{H - b} m", f"{a} m", f"{b} m", f"{W - a} m", f"{H} m"]
    show = [labs[0], None, labs[2], labs[3], None, labs[5]] if l < 2 else [labs[0], labs[1], None, labs[3], None, labs[5]]
    if l < 2:
        stem = f"Un terreno tiene forma de L, con las medidas indicadas en la figura (en metros). ¿Cuántos metros de cerca se necesitan para rodearlo completamente?"
    else:
        stem = "Un terreno tiene forma de L, con las medidas indicadas en la figura. ¿Cuántos metros de cerca se necesitan para rodearlo completamente?"
    fig = polygon_fig(pts, show, h=300)
    val = 2 * (W + H)
    ans = f"{val} m"
    alts = [W + H, val + a, val - a, val + b, val - b + a, 2 * W + H + a + b]
    al = uq(ans, [f"{t} m" for t in alts if t > 0 and t != val])
    return make(stem, fig, ans, al[:4], Q_MOD, f"El perímetro del terreno en L es igual al del rectángulo que lo encierra: 2·({W} + {H}) = {val} m.")


def t_track(r, l):
    Lr = r.choice([40, 50, 60, 80, 100])
    d = r.choice([20, 30, 40, 50, 60])
    body = R(140, 70, 280, 100, FILL, NAVY, 3) + f'<path d="M 140 70 A 50 50 0 0 0 140 170" fill="{FILL}" stroke="{NAVY}" stroke-width="3"/><path d="M 420 70 A 50 50 0 0 1 420 170" fill="{FILL}" stroke="{NAVY}" stroke-width="3"/>'
    body += tag(280, 50, f"{Lr} m", 16) + tag(280, 195, f"{Lr} m", 16) + tag(55, 120, f"{d} m", 16)
    fig = wrap(560, 230, body, "Pista con dos tramos rectos y dos semicircunferencias")
    stem = f"Una pista tiene dos tramos rectos de {Lr} m y dos semicircunferencias de diámetro {d} m en sus extremos. ¿Cuál es la longitud de una vuelta completa? (Usa π = 3,14.)"
    val = 2 * Lr + F(314, 100) * d
    ans = f"{dstr(val)} m"
    alts = [Lr + F(314, 100) * d, 2 * Lr + F(314, 100) * d / 2, 2 * Lr + d, 2 * Lr + 2 * F(314, 100) * d, val + d]
    al = list(dict.fromkeys(f"{dstr(F(t))} m" for t in alts if F(t) != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Las dos semicircunferencias forman una circunferencia de diámetro {d}: 2·{Lr} + 3,14·{d} = {dstr(val)} m.")


def t_cost(r, l):
    a, b = r.randint(10, 30), r.randint(8, 25)
    price = r.choice([2500, 3000, 4500, 5000, 6500])
    fig = polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a} m", f"{b} m", None, None])
    stem = f"Un terreno rectangular de {a} m por {b} m se cerca por todos sus lados con una reja que cuesta ${price:,} el metro. ¿Cuánto cuesta cercarlo?".replace(",", ".")
    P_ = 2 * (a + b)
    val = P_ * price
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    ans = f(val)
    alts = [a * b * price, (a + b) * price, P_ * price + price, (P_ - a) * price, 2 * a * price]
    al = list(dict.fromkeys(f(t) for t in alts if t != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Perímetro = {P_} m; costo = {P_}·{price} = {val}.")


# ---------------------------------------------------------------- Representar
def poly_cells(r):
    cells = {(0, 0)}
    n = r.randint(6, 9)
    while len(cells) < n:
        x, y = r.choice(sorted(cells))
        dx, dy = r.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        c = (x + dx, y + dy)
        if 0 <= c[0] < 5 and 0 <= c[1] < 4:
            cells.add(c)
    return cells


def perim_cells(cells):
    return sum(1 for (x, y) in cells for d in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + d[0], y + d[1]) not in cells)


def t_polyomino(r, l):
    cells = poly_cells(r)
    cs = 46
    body = ""
    ox, oy = 150, 30
    for (x, y) in cells:
        body += R(ox + x * cs, oy + y * cs, cs, cs, FILL3, NAVY, 3)
    fig = wrap(560, 250, body, "Figura formada por cuadrados de 1 unidad de lado")
    P_ = perim_cells(cells)
    stem = "La figura está formada por cuadrados iguales de 1 unidad de lado. ¿Cuál es su perímetro?"
    ans = f"{P_} unidades"
    alts = [len(cells), 4 * len(cells), P_ + 2, P_ - 2, P_ + 4, len(cells) * 2]
    al = list(dict.fromkeys(f"{t} unidades" for t in alts if t > 0 and t != P_))
    return make(stem, fig, ans, al[:4], Q_REP, f"Se cuentan los lados de cuadrado que quedan en el borde de la figura: {P_}.")


def t_alg_perimeter(r, l):
    a, b = r.randint(1, 4), r.randint(1, 6)
    x_l = f"x + {b}"
    fig = polygon_fig([(0, 0), (10, 0), (10, 5), (0, 5)], [f"{a}x", x_l, None, None])
    stem = "Un rectángulo tiene lados de longitud " + f"{a}x y ({x_l}). ¿Qué expresión representa su perímetro?"
    ans = f"{2 * a + 2}x + {2 * b}"
    alts = [f"{a}x² + {a * b}x", f"{a + 1}x + {b}", f"{2 * a + 2}x + {b}", f"{a}x + {b}", f"{2 * a}x + {2 * b}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"P = 2·({a}x) + 2·(x + {b}) = {ans}.")


def t_compare(r, l):
    a, b = r.randint(4, 12), r.randint(2, 10)
    if a == b:
        raise Reject
    s = r.randint(max(a, b), a + b)
    body = R(50, 60, a * 15, b * 15, FILL, NAVY, 3) + tag(50 + a * 7.5, 60 + b * 15 + 24, f"{a} m", 16) + tag(40, 60 + b * 7.5, f"{b} m", 16) + tag(50 + a * 7.5, 40, "Terreno A", 15)
    body += R(330, 60, s * 10, s * 10, FILL2, NAVY, 3) + tag(330 + s * 5, 60 + s * 10 + 24, f"{s} m", 16) + tag(330 + s * 5, 40, "Terreno B", 15)
    fig = wrap(560, 260, body, "Dos terrenos con sus medidas")
    PA, PB = 2 * (a + b), 4 * s
    if PA == PB:
        raise Reject
    stem = "La figura muestra dos terrenos: uno rectangular (A) y otro cuadrado (B). ¿Cuál necesita más cerca y cuántos metros más?"
    big = "A" if PA > PB else "B"
    ans = f"El terreno {big}, con {abs(PA - PB)} m más"
    other = "B" if big == "A" else "A"
    alts = [f"El terreno {other}, con {abs(PA - PB)} m más", f"El terreno {big}, con {abs(a * b - s * s)} m más", f"El terreno {other}, con {abs(a * b - s * s)} m más", f"Ambos necesitan la misma cantidad de cerca"]
    return make(stem, fig, ans, alts, Q_REP, f"Perímetro A = {PA} m y perímetro B = {PB} m.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, b = r.randint(3, 9), r.randint(3, 9)
    if a == b:
        b += 1
    if k == 0:
        return [f"Rectángulo de {a} m por {b} m", f"Perímetro = {a} · {b} = {a * b} m"], "Multiplicó los lados: eso es el área; el perímetro es la suma de todos los lados, 2(a + b)", \
            ["Sumó solo dos lados del rectángulo y omitió los otros dos lados iguales", "Sumó un lado y el doble del otro lado sin considerar los lados restantes", "Elevó al cuadrado uno de los lados y lo sumó con el otro lado", "Multiplicó la suma de los lados por dos y luego la dividió por dos"]
    if k == 1:
        return [f"Rectángulo de {a} m por {b} m", f"Perímetro = {a} + {b} = {a + b} m"], "Sumó solo dos lados: en el perímetro deben sumarse los cuatro lados, es decir 2(a + b)", \
            ["Multiplicó los dos lados en lugar de sumar las medidas de los cuatro lados", "Duplicó solo uno de los lados antes de sumar el otro lado sin duplicar", "Restó los lados entre sí y duplicó el resultado obtenido para el perímetro", "Sumó los lados y elevó al cuadrado el resultado obtenido en el cálculo"]
    if k == 2:
        return [f"Circunferencia de diámetro {2 * a} cm", f"Longitud = 2π · {2 * a} = {4 * a}π cm"], "Usó el diámetro como si fuera el radio: la longitud es π·d o 2π·r", \
            ["Usó el radio como si fuera el diámetro y dividió la longitud por dos", "Multiplicó el diámetro por π y luego por dos al calcular la longitud total", "Calculó el área de la circunferencia en lugar de calcular su longitud", "Sumó el radio y el diámetro antes de multiplicar el resultado por π al final"]
    return [f"Terreno en forma de L: 10 m × 8 m con esquina cortada", "Cerca = suma de solo los lados marcados en la figura"], "Debe sumarse todo el borde: el perímetro de la L equivale al del rectángulo que la encierra si sus lados son perpendiculares", \
        ["Debe restarse el área de la esquina cortada al perímetro del rectángulo completo", "Debe calcularse el área de la L y luego multiplicarla por el precio de la cerca", "Debe sumarse solo la mitad de los lados marcados para no repetir medidas", "Debe considerarse solamente el lado más largo de la figura como el perímetro"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_same_perim(r, l):
    a, b = r.choice([(6, 2), (7, 1), (5, 3)])
    s = (a + b) // 2
    body = R(50, 70, a * 24, b * 24, FILL, NAVY, 3) + tag(50 + a * 12, 70 + b * 24 + 22, f"{a} cm × {b} cm", 15) + R(330, 40, s * 24, s * 24, FILL2, NAVY, 3) + tag(330 + s * 12, 40 + s * 24 + 22, f"{s} cm × {s} cm", 15)
    fig = wrap(560, 240, body, "Dos figuras con el mismo perímetro")
    stem = f"Un estudiante afirma: «Dos figuras con igual perímetro tienen siempre igual área». Considerando el rectángulo y el cuadrado de la figura (ambos de perímetro {2 * (a + b)} cm), ¿es correcta su afirmación?"
    ans = f"No: el rectángulo tiene área {a * b} cm² y el cuadrado {s * s} cm², aunque sus perímetros son iguales"
    alts = [f"Sí: como sus perímetros son iguales, ambas áreas son {a * b} cm²", f"Sí: el cuadrado siempre tiene menor área que el rectángulo del mismo perímetro", f"No: porque los perímetros de las figuras no son iguales entre sí", f"Sí: el área y el perímetro miden lo mismo en cualquier figura plana"]
    return make(stem, fig, ans, alts, Q_ARG, "El perímetro y el área son medidas distintas: figuras con igual perímetro pueden tener áreas diferentes.")


TRUE = ["El perímetro de una figura es la suma de las longitudes de todos sus lados", "El perímetro de un cuadrado de lado a es 4a", "La longitud de una circunferencia de radio r es 2πr",
        "El perímetro de un rectángulo de lados a y b es 2(a + b)", "Figuras con distinta forma pueden tener el mismo perímetro", "El perímetro de un hexágono regular de lado a es 6a"]
FALSE = ["El perímetro de una figura es la medida de la superficie que encierra", "El perímetro de un cuadrado de lado a es a²", "La longitud de una circunferencia de radio r es πr²",
         "El perímetro de un rectángulo de lados a y b es a·b", "Si dos figuras tienen igual perímetro, entonces tienen igual área", "El perímetro de un triángulo equilátero de lado a es 2a"]


def _fig(r):
    a, b = r.randint(4, 12), r.randint(3, 9)
    return polygon_fig([(0, 0), (a, 0), (a, b), (0, b)], [f"{a}", f"{b}", None, None])


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre perímetros es verdadera?", "Sobre el perímetro de figuras planas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la definición de perímetro y las fórmulas usuales.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre perímetros es falsa?", "Sobre el perímetro de figuras planas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la definición de perímetro.")


BY_SKILL = {
    Q_RES: [t_perim, t_missing_side, t_circle],
    Q_MOD: [t_lshape, t_track, t_cost],
    Q_REP: [t_polyomino, t_alg_perimeter, t_compare],
    Q_ARG: [t_error, t_same_perim, t_true, t_false],
}
