"""Clase 35 (M1) · Cuerpos geométricos: prisma y cilindro; volumen, superficie y capacidad."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import cylinder_fig
import geo
import viz
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


def box_fig(a, b, c, u):
    return geo.box3d(a, b, c, {"a": f"{a} {u}", "b": f"{b} {u}", "c": f"{c} {u}"}, letters=False)


def num(x):
    return f"{int(x):,}".replace(",", ".")


# ---------------------------------------------------------------- Resolver problemas
def t_prism(r, l):
    u = r.choice(["cm", "m"])
    a, b, c = r.randint(3, 15), r.randint(2, 10), r.randint(2, 12)
    if len({a, b, c}) < 3:
        raise Reject
    fig = box_fig(a, b, c, u)
    kind = r.choice(["vol", "area"] if l else ["vol"])
    if kind == "vol":
        val = a * b * c
        stem = "¿Cuál es el volumen del prisma rectangular de la figura?"
        alts = [2 * (a * b + b * c + a * c), a + b + c, a * b + c, val + a * b, a * b * 2 * c]
        ans = f"{val} {u}³"
        ex = f"V = {a}·{b}·{c} = {val} {u}³."
        al = uq(ans, [f"{t} {u}³" for t in alts if t > 0 and t != val])
    else:
        val = 2 * (a * b + b * c + a * c)
        stem = "¿Cuál es el área total de la superficie del prisma rectangular de la figura?"
        alts = [a * b * c, a * b + b * c + a * c, 2 * (a + b + c), val + a * b, 2 * a * b + 2 * b * c]
        ans = f"{val} {u}²"
        ex = f"A = 2(ab + bc + ac) = 2({a * b} + {b * c} + {a * c}) = {val} {u}²."
        al = uq(ans, [f"{t} {u}²" for t in alts if t > 0 and t != val])
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_cylinder(r, l):
    u = r.choice(["cm", "m"])
    rad, h = r.randint(2, 9), r.randint(3, 15)
    fig = cylinder_fig(f"r = {rad} {u}", f"h = {h} {u}")
    kind = r.choice(["vol", "lat", "tot"] if l else ["vol", "lat"])
    if kind == "vol":
        val = rad * rad * h
        stem = "¿Cuál es el volumen del cilindro de la figura? (Expresa el resultado en función de π.)"
        ans = f"{val}π {u}³"
        alts = [f"{2 * rad * h}π {u}³", f"{rad * h}π {u}³", f"{rad * rad * h * 2}π {u}³", f"{(2 * rad) ** 2 * h}π {u}³", f"{rad * rad * h + rad}π {u}³"]
        ex = f"V = πr²h = π·{rad}²·{h} = {val}π {u}³."
    elif kind == "lat":
        val = 2 * rad * h
        stem = "¿Cuál es el área de la superficie lateral del cilindro de la figura? (Expresa el resultado en función de π.)"
        ans = f"{val}π {u}²"
        alts = [f"{rad * rad * h}π {u}²", f"{rad * h}π {u}²", f"{2 * rad * (rad + h)}π {u}²", f"{4 * rad * h}π {u}²", f"{val + rad}π {u}²"]
        ex = f"A lateral = 2πrh = 2π·{rad}·{h} = {val}π {u}²."
    else:
        val = 2 * rad * (rad + h)
        stem = "¿Cuál es el área total de la superficie del cilindro de la figura (incluidas las dos bases)? (Expresa el resultado en función de π.)"
        ans = f"{val}π {u}²"
        alts = [f"{2 * rad * h}π {u}²", f"{rad * rad * h}π {u}²", f"{2 * rad * h + rad * rad}π {u}²", f"{2 * rad * h + 4 * rad * rad}π {u}²", f"{val + rad}π {u}²"]
        ex = f"A total = 2πr(r + h) = 2π·{rad}·({rad} + {h}) = {val}π {u}²."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_find_dim(r, l):
    a, b, c = r.randint(3, 12), r.randint(3, 10), r.randint(2, 9)
    V = a * b * c
    u = "cm"
    fig = geo.box3d(a, b, c, {"a": f"{a} {u}", "b": f"{b} {u}", "c": "h"}, letters=False)
    stem = f"Un prisma rectangular de base {a} {u} por {b} {u} tiene un volumen de {V} {u}³. ¿Cuál es su altura h?"
    ans = f"{c} {u}"
    alts = [f"{V // (a + b) if V % (a + b) == 0 else c + 3} {u}", f"{V // a if V % a == 0 else c + 1} {u}", f"{c + 1} {u}", f"{c - 1 if c > 1 else c + 4} {u}", f"{a * b} {u}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"h = V/(a·b) = {V}/{a * b} = {c} {u}.")


# ---------------------------------------------------------------- Modelar
def _lt(t, unit):
    t = F(t)
    if t.denominator != 1:
        d = t.denominator
        while d % 2 == 0: d //= 2
        while d % 5 == 0: d //= 5
        if d != 1:
            return None
        return dstr(t) + unit
    return fs(t) + unit


def _alts(ts, unit, ans):
    out = []
    for t in ts:
        if t <= 0:
            continue
        s = _lt(t, unit)
        if s and s != ans and s not in out:
            out.append(s)
    return out


def t_capacity(r, l):
    kind = r.choice(["box", "cyl"])
    if kind == "box":
        a, b, c = r.randrange(20, 105, 5), r.randrange(20, 65, 5), r.randrange(20, 65, 5)
        V = a * b * c
        fig = geo.box3d(a, b, c, {"a": f"{a} cm", "b": f"{b} cm", "c": f"{c} cm"}, letters=False)
        L_ = F(V, 1000)
        what = r.choice(["Una pecera", "Un contenedor de agua", "Una tina"])
        stem = f"{what} con forma de prisma rectangular mide {a} cm de largo, {b} cm de ancho y {c} cm de alto. ¿Cuántos litros de agua caben si se llena completamente? (1 L = 1.000 cm³)"
        alts = [V, F(V, 100), L_ * 10, F(a * b, 1000) * c * 2, L_ + 10, L_ / 10, F(2 * (a * b + b * c + a * c), 1000)]
        ex = f"V = {a}·{b}·{c} = {V} cm³ = {fs(L_)} L."
    else:
        rad, h = r.randrange(5, 35, 5), r.randrange(10, 85, 5)
        fig = cylinder_fig(f"r = {rad} cm", f"h = {h} cm")
        L_ = F(314 * rad * rad * h, 100 * 1000)
        what = r.choice(["Un estanque cilíndrico", "Un tambor cilíndrico", "Un depósito cilíndrico"])
        stem = f"{what} tiene {rad} cm de radio y {h} cm de altura. ¿Cuántos litros caben aproximadamente? (Usa π = 3,14 y 1 L = 1.000 cm³)"
        alts = [L_ * 10, L_ / 10, F(314 * rad * h, 100 * 1000), L_ * 2, L_ + 5, L_ * 4]
        ex = f"V = 3,14·{rad}²·{h} = {dstr(F(314 * rad * rad * h, 100))} cm³ ≈ {dstr(L_)} L."
    ans = _lt(L_, " L")
    if ans is None:
        raise Reject
    return make(stem, fig, ans, _alts(alts, " L", ans)[:4], Q_MOD, ex)


def t_equiv(r, l):
    a, b = r.randrange(10, 55, 5), r.randrange(10, 45, 5)
    rad, Hc = r.choice([5, 10, 15, 20]), r.randint(4, 30)
    hp = F(314 * rad * rad * Hc, 100 * a * b)
    ans = _lt(hp, " cm")
    if ans is None or hp > 60:
        raise Reject
    fig = card([f"Cilindro: radio {rad} cm, agua hasta {Hc} cm", f"Prisma vacío: base {a} × {b} cm", "Se vierte toda el agua en el prisma"], 170, 18)
    stem = f"El agua contenida en un cilindro de {rad} cm de radio, que alcanza {Hc} cm de altura, se vierte en un prisma de base rectangular de {a} cm × {b} cm. ¿Qué altura alcanza el agua en el prisma? (Usa π = 3,14.)"
    alts = [hp * 3, hp / 2, F(rad * rad * Hc, a * b), F(314 * rad * Hc, 100 * a * b), hp + 5, hp * 2, F(314 * rad * rad, 100 * a * b)]
    return make(stem, fig, ans, _alts(alts, " cm", ans)[:4], Q_MOD, f"3,14·{rad}²·{Hc} = {a}·{b}·h ⟹ h = {dstr(hp)} cm.")


def t_carton(r, l):
    a, b, c = r.randrange(20, 65, 5), r.randrange(10, 45, 5), r.randrange(10, 35, 5)
    if len({a, b, c}) < 3:
        raise Reject
    fig = box_fig(a, b, c, "cm")
    kind = r.choice(["closed", "open"])
    obj = r.choice(["caja de cartón", "caja de madera", "caja de plástico"])
    if kind == "closed":
        val = 2 * (a * b + b * c + a * c)
        stem = f"Se fabrica una {obj} cerrada de {a} cm × {b} cm × {c} cm. ¿Cuántos cm² de material se necesitan (sin considerar solapas ni pérdidas)?"
        alts = [a * b * c, a * b + b * c + a * c, val - 2 * a * b, 2 * (a + b + c), val + a * b]
    else:
        val = a * b + 2 * (a * c + b * c)
        stem = f"Se fabrica una {obj} sin tapa de {a} cm × {b} cm × {c} cm. ¿Cuántos cm² de material se necesitan (sin considerar pérdidas)?"
        alts = [2 * (a * b + b * c + a * c), a * b * c, a * b + a * c + b * c, val + a * b, 2 * a * b + 2 * (a * c + b * c)]
    ans = f"{num(val)} cm²"
    al = list(dict.fromkeys(f"{num(t)} cm²" for t in alts if t > 0 and t != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Se suman las áreas de las caras que forman la caja: {num(val)} cm².")


def t_fill(r, l):
    a, b, c = r.randrange(40, 130, 10), r.randrange(30, 80, 10), r.randrange(30, 70, 10)
    V = F(a * b * c, 1000)
    q = r.choice([5, 10, 12, 15, 20, 25, 30, 40])
    t = V / q
    ans = _lt(t, " min")
    if ans is None or t > 400:
        raise Reject
    fig = box_fig(a, b, c, "cm")
    stem = f"Un estanque con forma de prisma de {a} cm × {b} cm × {c} cm está vacío. Se llena con una llave que entrega {q} litros por minuto. ¿Cuántos minutos tarda en llenarse? (1 L = 1.000 cm³)"
    alts = [t * 10, t / 10, V * q, V + q, V - q, t * 2]
    return make(stem, fig, ans, _alts(alts, " min", ans)[:4], Q_MOD, f"V = {fs(V)} L; tiempo = {fs(V)} : {q} = {dstr(t) if t.denominator != 1 else fs(t)} min.")


# ---------------------------------------------------------------- Representar
def t_surface_expr(r, l):
    a, b, c = r.randint(3, 12), r.randint(2, 9), r.randint(2, 8)
    if len({a, b, c}) < 3:
        raise Reject
    fig = box_fig(a, b, c, "cm")
    ans = f"2·({a}·{b} + {b}·{c} + {a}·{c})"
    alts = [f"{a}·{b}·{c}", f"{a}·{b} + {b}·{c} + {a}·{c}", f"2·({a} + {b} + {c})", f"2·{a}·{b} + {b}·{c}", f"({a} + {b})·{c}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("¿Qué expresión permite calcular el área total de la superficie del prisma de la figura?", fig, ans, al[:4], Q_REP, "El área total es la suma de las áreas de las seis caras: tres pares de rectángulos iguales.")


def t_cyl_expr(r, l):
    rad, h = r.randint(2, 9), r.randint(3, 14)
    fig = cylinder_fig(f"r = {rad} cm", f"h = {h} cm")
    kind = r.choice(["vol", "lat"])
    if kind == "vol":
        ans = f"π·{rad}²·{h}"
        alts = [f"2·π·{rad}·{h}", f"π·{h}²·{rad}", f"π·{2 * rad}²·{h}", f"π·{rad}·{h}", f"2·π·{rad}²"]
        stem = "¿Qué expresión permite calcular el volumen del cilindro de la figura?"
        ex = "V = π·r²·h."
    else:
        ans = f"2·π·{rad}·{h}"
        alts = [f"π·{rad}²·{h}", f"2·π·{rad}²", f"π·{rad}·{h}", f"2·π·{rad}·({rad} + {h})", f"π·{h}²·{rad}"]
        stem = "¿Qué expresión permite calcular el área de la superficie lateral del cilindro de la figura?"
        ex = "El área lateral es un rectángulo de base 2πr (la circunferencia) y altura h."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, ex)


def t_units_table(r, l):
    vs = [1000, 2000, 5000, 20000, 50000, 100000]
    hide = r.randrange(1, len(vs))
    rows = [[num(v) for v in vs], [str(v // 1000) if i != hide else "?" for i, v in enumerate(vs)]]
    fig = viz.table_fig(["Volumen (cm³)"] + [num(v) for v in vs][:0] + ["1", "2", "3", "4", "5", "6"][:0], [[num(v) for v in vs]]) if False else viz.table_fig(["cm³"] + [num(v) for v in vs], [["Litros"] + [str(v // 1000) if i != hide else "?" for i, v in enumerate(vs)]])
    val = vs[hide] // 1000
    stem = "La tabla relaciona volúmenes en centímetros cúbicos con su capacidad en litros. ¿Qué valor corresponde a «?»"
    ans = str(val)
    alts = [val * 10, val // 10 if val >= 10 else val + 2, val + 5, vs[hide] // 100, val * 2]
    al = [str(t) for t in dict.fromkeys(alts) if t != val and t > 0]
    return make(stem, fig, ans, al[:4], Q_REP, "Como 1 L = 1.000 cm³, se divide el volumen en cm³ por 1.000.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, b, c = r.randint(3, 9), r.randint(3, 9), r.randint(3, 9)
    if k == 0:
        return [f"Prisma de {a} cm × {b} cm × {c} cm", f"Volumen = {a} + {b} + {c} = {a + b + c} cm³"], "Sumó las aristas: el volumen es el producto del largo, el ancho y el alto", \
            ["Multiplicó solo el largo y el ancho sin considerar la altura del prisma", "Calculó el área total de la superficie en lugar de calcular el volumen", "Multiplicó las tres medidas y dividió por dos el resultado obtenido", "Sumó dos de las medidas y multiplicó el resultado por la tercera medida"]
    if k == 1:
        return [f"Cilindro de diámetro {2 * a} cm y altura {b} cm", f"V = π · {2 * a}² · {b} = {4 * a * a * b}π cm³"], "Usó el diámetro como radio: en V = πr²h el radio es la mitad del diámetro", \
            ["Usó el radio como si fuera el diámetro al reemplazar en la fórmula del volumen", "Multiplicó el radio por la altura sin elevar el radio al cuadrado", "Calculó el área lateral del cilindro en lugar de calcular su volumen", "Sumó el radio y la altura antes de multiplicar por π para obtener el volumen"]
    if k == 2:
        return ["Un estanque tiene un volumen de 3.000 cm³", "Su capacidad es 3.000 litros"], "Confundió las unidades: 1 L = 1.000 cm³, por lo que 3.000 cm³ son 3 litros", \
            ["Dividió por 100 en lugar de dividir por 1.000 para convertir a litros", "Multiplicó por 1.000 en lugar de dividir al pasar de centímetros cúbicos a litros", "Pasó de centímetros cúbicos a litros restando 1.000 al volumen indicado", "Consideró que 1 litro equivale a 1 cm³ al convertir la unidad de volumen"]
    return [f"Cubo de arista {a} cm", f"Si la arista se duplica, el volumen se duplica"], "Al duplicar la arista, el volumen se multiplica por 2³ = 8, no por 2", \
        ["Al duplicar la arista, el volumen se multiplica por 4 porque hay dos dimensiones", "Al duplicar la arista, el volumen se multiplica por 6 porque el cubo tiene seis caras", "Al duplicar la arista, el volumen se suma con la arista original del cubo", "Al duplicar la arista, el volumen no cambia porque el cubo mantiene su forma"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_scale(r, l):
    a = r.randint(2, 8)
    k = r.choice([2, 3])
    fig = geo.two_cubes(k, f"arista {a} cm", f"arista {k * a} cm")
    stem = f"El segundo cubo tiene una arista {'doble' if k == 2 else 'triple'} de la del primero. ¿Cómo se comparan sus volúmenes?"
    ans = f"El volumen del segundo es {k ** 3} veces el del primero"
    alts = [f"El volumen del segundo es {k} veces el del primero", f"El volumen del segundo es {k * k} veces el del primero", f"El volumen del segundo es {k ** 3 + k} veces el del primero", f"Ambos cubos tienen el mismo volumen"]
    return make(stem, fig, ans, alts, Q_ARG, f"Volumen ∝ arista³: {k}³ = {k ** 3}.")


TRUE = ["El volumen de un prisma es el área de su base por su altura", "El volumen de un cilindro de radio r y altura h es πr²h", "1 litro equivale a 1.000 cm³",
        "Si se duplica la arista de un cubo, su volumen se multiplica por 8", "El área lateral de un cilindro es 2πrh", "1 m³ equivale a 1.000 litros"]
FALSE = ["El volumen de un prisma es la suma de sus aristas", "El volumen de un cilindro de radio r y altura h es 2πrh", "1 litro equivale a 100 cm³",
         "Si se duplica la arista de un cubo, su volumen se duplica", "El área lateral de un cilindro es πr²h", "1 m³ equivale a 100 litros"]


def _fig(r):
    return geo.box3d(r.randint(4, 8), r.randint(3, 6), r.randint(3, 7), {}, letters=False)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre prismas y cilindros es verdadera?", "Sobre volumen y superficie de cuerpos geométricos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las fórmulas de volumen y superficie.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre prismas y cilindros es falsa?", "Sobre volumen y superficie de cuerpos geométricos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las fórmulas de volumen y superficie.")


BY_SKILL = {
    Q_RES: [t_prism, t_cylinder, t_find_dim],
    Q_MOD: [t_capacity, t_equiv, t_carton, t_fill],
    Q_REP: [t_surface_expr, t_cyl_expr, t_units_table],
    Q_ARG: [t_error, t_scale, t_true, t_false],
}
