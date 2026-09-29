"""Clase 16 (M1) · Factorización de expresiones; simplificación con restricciones."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
import viz

SUPR = "²³"


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def bn(a, v="x"):
    """(v + a) escrito como '(x + 3)' o '(x − 3)'."""
    return f"({v} {'+' if a > 0 else '−'} {abs(a)})"


def poly2(b, c, v="x"):
    """v² + b v + c."""
    return co(1, v + "²", True) + co(b, v, False) + co(c, "", False)


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        if a not in seen:
            seen.add(a); out.append(a)
    return out


# ---------------------------------------------------------------- Resolver problemas
def t_factor(r, l):
    v = r.choice("xmnt") if l else "x"
    kind = r.choice(["common", "dsq", "perf", "tri"] if l else ["common", "dsq", "perf"])
    if kind == "common":
        g = r.choice([2, 3, 4, 5, 6])
        p, q = rr(r, -5, 6), rr(r, 1, 7)
        deg = r.choice([1, 2])
        if deg == 1:
            expr = co(g * p, v + "²", True) + co(g * q, v, False)
            ans = f"{g}{v}({co(p, v, True)}{co(q, '', False)})"
            alts = [f"{g}({co(p * g, v + '²', True)}{co(q * g, v, False)})" if False else f"{g}{v}({co(p * g, v, True)}{co(q * g, '', False)})", f"{g}({co(p, v + '²', True)}{co(q, v, False)})", f"{v}({co(g * p, v, True)}{co(g * q, '', False)})", f"{g}{v}({co(p, v, True)}{co(q + 1, '', False)})", f"{g * p}{v}({v}{co(q, '', False)})" if False else f"{g}{v}({co(p, v, True)}{co(-q, '', False)})"]
        else:
            expr = co(g * p, v + "³", True) + co(g * q, v + "²", False)
            ans = f"{g}{v}²({co(p, v, True)}{co(q, '', False)})"
            alts = [f"{g}{v}({co(p, v + '²', True)}{co(q, v, False)})", f"{g}({co(p, v + '³', True)}{co(q, v + '²', False)})", f"{v}²({co(g * p, v, True)}{co(g * q, '', False)})", f"{g}{v}²({co(p, v, True)}{co(-q, '', False)})", f"{g}{v}³({co(p, v, True)}{co(q, '', False)})"]
        ex = "Se extrae el máximo factor común de todos los términos (coeficiente y parte literal)."
    elif kind == "dsq":
        a = r.randint(2, 12)
        c = r.choice([1, 4, 9]) if l else 1
        k = int(math.isqrt(c))
        expr = co(c, v + "²", True) + co(-a * a, "", False)
        ans = f"({k if k > 1 else ''}{v} + {a})({k if k > 1 else ''}{v} − {a})".replace("(1", "(")
        alts = [f"({k if k > 1 else ''}{v} − {a})²".replace("(1", "("), f"({k if k > 1 else ''}{v} + {a})²".replace("(1", "("), f"({k if k > 1 else ''}{v} + {a * a})({k if k > 1 else ''}{v} − 1)".replace("(1", "("), f"({k if k > 1 else ''}{v} − {a})({k if k > 1 else ''}{v} − {a})".replace("(1", "("), f"({k if k > 1 else ''}{v} + {a})({k if k > 1 else ''}{v} + {a})".replace("(1", "(")]
        ex = "Diferencia de cuadrados: a² − b² = (a + b)(a − b)."
    elif kind == "perf":
        a = rr(r, -9, 9)
        expr = poly2(2 * a, a * a, v)
        ans = f"({v} {'+' if a > 0 else '−'} {abs(a)})²"
        alts = [f"({v} {'−' if a > 0 else '+'} {abs(a)})²", f"({v} + {abs(a)})({v} − {abs(a)})", f"({v} {'+' if a > 0 else '−'} {abs(a * a)})²", f"({v} {'+' if a > 0 else '−'} {abs(2 * a)})({v} {'+' if a > 0 else '−'} {abs(a)})", f"({v} {'+' if a > 0 else '−'} {abs(a)})({v} {'−' if a > 0 else '+'} {abs(a)})"]
        ex = "Trinomio cuadrado perfecto: a² ± 2ab + b² = (a ± b)²."
    else:
        m, n = rr(r, -8, 8), rr(r, -8, 8)
        if m == n or m + n == 0:
            raise Reject
        expr = poly2(m + n, m * n, v)
        ans = bn(m, v) + bn(n, v)
        alts = [bn(-m, v) + bn(-n, v), bn(m, v) + bn(-n, v), bn(m + n, v) + bn(m * n, v) if abs(m * n) < 100 else bn(m, v) + bn(n + 1, v), bn(m, v) + bn(n + 1, v), bn(-m, v) + bn(n, v)]
        ex = f"Se buscan dos números que sumen {m + n} y multipliquen {m * n}: {m} y {n}."
    fig = card(["Factoriza:", expr], 130, 22)
    al = uq(ans, alts)
    return make("¿Cuál es la factorización de la expresión de la figura?", fig, ans, al[:4], Q_RES, ex)


def t_simplify(r, l):
    a = r.randint(2, 9)
    v = r.choice("xmn") if l else "x"
    kind = r.choice(["dsq", "common", "tri"] if l else ["dsq", "common"])
    if kind == "dsq":
        num = co(1, v + "²", True) + co(-a * a, "", False)
        den = f"{v} − {a}"
        ans = f"{v} + {a}"
        alts = [f"{v} − {a}", f"{v}² + {a}", f"{v} + {a * a}", f"{a}", f"({v} + {a})²"]
        ex = f"({v}² − {a * a}) = ({v} + {a})({v} − {a}); se simplifica el factor común ({v} − {a})."
    elif kind == "common":
        g = r.choice([2, 3, 4, 5])
        b = r.randint(1, 8)
        num = co(g, v + "²", True) + co(g * b, v, False)
        den = f"{g}{v}"
        ans = f"{v} + {b}"
        alts = [f"{v}² + {b}", f"{v} + {g * b}", f"{g}{v} + {b}", f"{v} + {b}{v}", f"{v} + {b + g}"]
        ex = f"{num} = {g}{v}({v} + {b}); se simplifica {g}{v}."
    else:
        m = r.randint(2, 7)
        n = r.randint(1, 7)
        num = poly2(m + n, m * n, v)
        den = f"{v} + {m}"
        ans = f"{v} + {n}"
        alts = [f"{v} + {m * n}", f"{v} + {m + n}", f"{v}² + {n}", f"{v} + {m}", f"{n}"]
        ex = f"{num} = ({v} + {m})({v} + {n}); se simplifica ({v} + {m})."
    fig = card(["Simplifica:", f"({num}) / ({den})"], 130, 21)
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("¿Cuál es la expresión simplificada de la fracción algebraica de la figura?", fig, ans, al[:4], Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def area_model(a, b, v="x"):
    """Rectángulo de lados (v + a) y (v + b) dividido en cuatro regiones."""
    wA, wB = 150, 60
    body = R(80, 30, wA, wA, FILL, NAVY, 3) + R(80 + wA, 30, wB + 30, wA, FILL2, NAVY, 3) + R(80, 30 + wA, wA, wB + 30, FILL2, NAVY, 3) + R(80 + wA, 30 + wA, wB + 30, wB + 30, FILL3, NAVY, 3)
    body += T(80 + wA / 2, 30 + wA / 2 + 8, v + "²", 26) + T(80 + wA + 45, 30 + wA / 2 + 6, (str(b) if b != 1 else "") + v, 20) + T(80 + wA / 2, 30 + wA + 50, (str(a) if a != 1 else "") + v, 20) + T(80 + wA + 45, 30 + wA + 52, str(a * b), 20)
    body += tag(80 + wA / 2, 18, v, 15) + tag(80 + wA + 45, 18, str(b), 15) + tag(58, 30 + wA / 2, v, 15) + tag(58, 30 + wA + 50, str(a), 15)
    return wrap(560, 300, body, "Modelo de áreas de un rectángulo dividido en cuatro regiones")


def t_rect_dims(r, l):
    m, n = r.randint(1, 9), r.randint(1, 9)
    v = r.choice("xmn") if l else "x"
    kind = r.choice(["side", "perim"])
    A = poly2(m + n, m * n, v)
    if kind == "side":
        stem = f"Un rectángulo tiene área {A} y una de sus dimensiones es ({v} + {m}). ¿Cuál es la otra dimensión?"
        ans = f"{v} + {n}"
        alts = [f"{v} + {m * n}", f"{v} + {m + n}", f"{v}² + {n}", f"{v} − {n}", f"{v} + {m}"]
        ex = f"Área = ({v} + {m})({v} + {n}); la otra dimensión es {v} + {n}."
    else:
        stem = f"Un rectángulo tiene área {A} y sus lados son binomios de la forma ({v} + a). ¿Cuál es el perímetro del rectángulo?"
        ans = co(4, v, True) + co(2 * (m + n), "", False)
        alts = [co(2, v, True) + co(m + n, "", False), co(4, v, True) + co(m + n, "", False), co(4, v, True) + co(2 * m * n, "", False), poly2(2 * (m + n), 2 * m * n, v), co(2, v, True) + co(2 * (m + n), "", False)]
        ex = f"Lados ({v} + {m}) y ({v} + {n}); perímetro = 2·(2{v} + {m + n})."
    fig = card([f"Área del rectángulo: {A}"], 110, 21) if kind == "perim" else area_model(m, n, v)
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_square_tiles(r, l):
    a = r.randint(1, 9)
    v = r.choice("xmn") if l else "x"
    expr = poly2(2 * a, a * a, v)
    fig = card([f"Se tienen {v}² + {2 * a}{v} + {a * a} baldosas", "Con ellas se forma un cuadrado perfecto"], 130, 19)
    stem = f"Con {expr} baldosas cuadradas de 1 unidad se arma un cuadrado sin que sobren ni falten. ¿Qué expresión representa la medida de su lado?"
    ans = f"{v} + {a}"
    alts = [f"{v} + {a * a}", f"{v} + {2 * a}", f"{v}² + {a}", f"2{v} + {a}", f"{v} − {a}"]
    return make(stem, fig, ans, alts[:4], Q_MOD, f"{expr} = ({v} + {a})², luego el lado es {v} + {a}.")


def t_common_area(r, l):
    g = r.choice([2, 3, 4, 5])
    p = r.randint(1, 6)
    A = co(g, "x²", True) + co(g * p, "x", False)
    body = R(120, 40, 300, 120, FILL, NAVY, 3) + T(270, 108, f"Área = {A}", 22)
    fig = wrap(560, 190, body, "Rectángulo cuya área es un binomio")
    stem = f"El área de un rectángulo es {A}. Si la base mide {g}x, ¿cuánto mide la altura?"
    ans = f"x + {p}"
    alts = [f"x + {g * p}", f"{g}x + {p}", f"x² + {p}", f"x + {p + g}"]
    return make(stem, fig, ans, alts, Q_MOD, f"{A} = {g}x(x + {p}), luego la altura es x + {p}.")


# ---------------------------------------------------------------- Representar
def t_area_read(r, l):
    a, b = r.randint(1, 8), r.randint(1, 8)
    v = r.choice("xmnt")
    fig = area_model(a, b, v)
    kind = r.choice(["fac", "exp"])
    tot = poly2(a + b, a * b, v)
    if kind == "fac":
        stem = "El rectángulo de la figura está dividido en cuatro regiones cuyas áreas se indican. ¿Qué factorización representa su área total?"
        ans = f"({v} + {a})({v} + {b})"
        alts = [f"({v} + {a + b})({v} + {a * b})", f"({v} + {a * b})({v} + 1)", f"({v} + {a})({v} + {a})" if a != b else f"({v} + {a + 1})({v} + {b})", f"({v} − {a})({v} − {b})", f"{v}({v} + {a + b}) + {a * b}"]
        ex = "Los lados del rectángulo son (v + a) y (v + b); su producto es el área total."
    else:
        stem = "El rectángulo de la figura está dividido en cuatro regiones cuyas áreas se indican. ¿Qué expresión representa el área total desarrollada?"
        ans = tot
        alts = [f"{v}² + {a * b}", co(1, v + "²", True) + co(a * b, v, False) + co(a + b, "", False), co(1, v + "²", True) + co(a + b, v, False), co(1, v + "²", True) + co(a + b + 1, v, False) + co(a * b, "", False), co(2, v + "²", True) + co(a + b, v, False) + co(a * b, "", False)]
        ex = f"Se suman las cuatro regiones: {v}² + {b}{v} + {a}{v} + {a * b} = {tot}."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, ex)


def t_table_fact(r, l):
    m, n = rr(r, -4, 5), rr(r, 1, 5)
    if m == n:
        raise Reject
    xs = [1, 2, 3, 4]
    ys = [(x + m) * (x + n) for x in xs]
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [["Valor"] + [str(y).replace("-", "−") for y in ys]])
    ans = bn(m) + bn(n)
    alts = [bn(-m) + bn(n), bn(m) + bn(-n), bn(-m) + bn(-n), bn(m + 1) + bn(n), bn(m) + bn(n + 2)]
    vals = lambda s: None
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("La tabla muestra los valores de una expresión que es el producto de dos binomios, para distintos valores de x. ¿Cuál es la expresión?", fig, ans, al[:4], Q_REP, f"Para x = 1 el valor es {ys[0]}: solo {ans} entrega los valores de la tabla.".replace("-", "−"))


def t_common_factor_read(r, l):
    g = r.choice([2, 3, 4, 5, 6])
    p, q = r.randint(1, 5), r.randint(1, 5)
    e1 = g * p
    e2 = g * q
    from math import gcd
    if gcd(e1, e2) != g:
        raise Reject
    v = r.choice("xmn")
    t1, t2 = f"{e1}{v}²", f"{e2}{v}"

    def dec(n_):
        f = []
        d = 2
        m = n_
        while d * d <= m:
            while m % d == 0:
                f.append(str(d)); m //= d
            d += 1
        if m > 1 or not f:
            f.append(str(m))
        return "·".join(f)
    body = R(60, 30, 200, 100, FILL, NAVY, 3) + T(160, 62, t1, 22) + T(160, 100, f"{dec(e1)}·{v}·{v}", 18)
    body += R(300, 30, 200, 100, FILL2, NAVY, 3) + T(400, 62, t2, 22) + T(400, 100, f"{dec(e2)}·{v}", 18)
    fig = wrap(560, 160, body, "Dos términos y su descomposición")
    ans = f"{g}{v}"
    alts = [f"{g}", f"{v}", f"{g}{v}²", f"{e1}{v}", f"{g * 2}{v}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("La figura muestra dos términos y su descomposición en factores. ¿Cuál es el máximo factor común de ambos?", fig, ans, al[:4], Q_REP, "Se toman los factores comunes con su menor exponente.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a = r.randint(2, 9)
    if k == 0:
        return [f"x² − {a * a} = (x − {a})²"], "Usó el cuadrado de binomio: una diferencia de cuadrados se factoriza como (x + a)(x − a)", \
            [f"Factorizó bien pero cambió el signo de uno de los dos factores binomiales", "Extrajo el factor común x y dejó el término numérico sin factorizar", "Dividió el término numérico por dos en lugar de sacarle raíz cuadrada", "Sumó los cuadrados en vez de restarlos al factorizar la expresión"]
    if k == 1:
        return [f"x² + {a * a} = (x + {a})(x + {a})"], "Factorizó una suma de cuadrados como si fuera un trinomio cuadrado perfecto: falta el término central 2ax", \
            ["Factorizó una suma de cuadrados como si fuera una diferencia de cuadrados", "Extrajo el factor común de todos los términos y olvidó el resto de la expresión", "Sacó raíz cuadrada al término numérico pero se equivocó con el signo", "Multiplicó los binomios pero no verificó el producto obtenido al final"]
    if k == 2:
        b, c = a, a + 2
        return [f"x² − {b + c}x + {b * c} = (x − {b + 1})(x − {c - 1})".replace("-", "−")], "Escogió números que no cumplen: deben sumar el coeficiente de x y multiplicar el término numérico a la vez", \
            ["Escogió números con la suma correcta pero con un producto que no coincide", "Escogió números con el producto correcto pero con una suma que no coincide", "Usó números positivos en los factores siendo negativos los coeficientes", "Intercambió el coeficiente de x con el término numérico al factorizar"]
    if k == 3:
        return [f"(x² − {a * a}) / (x − {a}) = x² / x − {a * a} / {a} = x − {a}"], "Simplificó términos por separado: solo pueden simplificarse factores, no términos sumados o restados", \
            ["Simplificó bien los factores pero olvidó anotar la restricción del denominador", "Dividió el numerador completo por el denominador sin factorizar previamente", "Factorizó el denominador pero no el numerador de la fracción algebraica", "Canceló el signo menos y dejó el resultado con el signo cambiado al final"]
    return [f"{2 * a}x + {4 * a} = {a}(2x + 4)"], f"No extrajo el máximo factor común: se puede factorizar {2 * a} y queda {2 * a}(x + 2)", \
        ["Extrajo un factor que no divide a ninguno de los dos términos de la expresión", "Extrajo el factor común pero dejó los términos sin dividir por él", "Factorizó la variable x pero no el coeficiente numérico común de los términos", "Sumó los coeficientes en lugar de buscar su máximo divisor común"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_restriction(r, l):
    a = r.randint(2, 9)
    kind = r.choice(["dsq", "tri"] if l else ["dsq"])
    if kind == "dsq":
        expr = f"(x² − {a * a}) / (x − {a})"
        simp = f"x + {a}"
        bad = a
    else:
        m = r.randint(2, 8)
        expr = f"({poly2(a + m, a * m)}) / (x + {a})"
        simp = f"x + {m}"
        bad = -a
    fig = card(["Simplifica y considera las restricciones:", expr + f" = {simp}"], 150, 19)
    ans = f"x ≠ {bad}".replace("-", "−")
    alts = [f"x ≠ {-bad}", f"x ≠ 0", f"x > {bad}", f"x ≠ {bad} y x ≠ {-bad}", f"x ≠ {bad * bad}"]
    alts = [x.replace("-", "−") for x in alts]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("Al simplificar la fracción algebraica de la figura, ¿qué restricción debe cumplir x para que la igualdad sea válida?", fig, ans, al[:4], Q_ARG, "El denominador original no puede ser cero: la restricción se mantiene aunque el factor se simplifique.")


def t_not_factor(r, l):
    m, n = rr(r, -6, 7), rr(r, 1, 7)
    if m == n or m + n == 0:
        raise Reject
    E = poly2(m + n, m * n)
    good = [bn(m) + bn(n), bn(n) + bn(m), f"x² + {abs(m + n)}x".replace("+", "+" if m + n > 0 else "−") + co(m * n, "", False) if False else E, f"({E})·1"]
    bad = r.choice([bn(-m) + bn(-n), bn(m) + bn(-n), bn(m + 1) + bn(n), bn(m) + bn(n + 1)])
    good = [g for g in dict.fromkeys(good) if g != bad]
    if len(good) < 4 or bad == bn(m) + bn(n) or bad == bn(n) + bn(m):
        raise Reject
    fig = card(["Expresión:", E], 130, 24)
    return make("¿Cuál de las siguientes NO es una forma equivalente de la expresión de la figura?", fig, bad, good[:4], Q_ARG, f"La expresión es {bn(m) + bn(n)}.")


TRUE = ["x² − 25 se factoriza como (x + 5)(x − 5)", "x² + 6x + 9 es un trinomio cuadrado perfecto", "Factorizar consiste en escribir una expresión como producto de factores",
        "En (x² − 9)/(x − 3) = x + 3 debe cumplirse x ≠ 3", "El máximo factor común de 6x² y 9x es 3x", "(x + 2)(x + 3) = x² + 5x + 6"]
FALSE = ["x² + 25 se factoriza como (x + 5)(x − 5)", "x² + 6x + 9 se factoriza como (x + 3)(x − 3)", "Al simplificar una fracción algebraica pueden cancelarse términos sumados",
        "En (x² − 9)/(x − 3) = x + 3 no importa el valor de x", "El máximo factor común de 6x² y 9x es 6x", "(x + 2)(x + 3) = x² + 6"]


def _fig(r):
    return card(["Factorización", "Factor común · diferencia de cuadrados · trinomios"], 130, 18)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre factorización es verdadera?", "Sobre factorizar y simplificar expresiones, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con los casos de factorización y las restricciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre factorización es falsa?", "Sobre factorizar y simplificar expresiones, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice los casos de factorización.")


BY_SKILL = {
    Q_RES: [t_factor, t_simplify],
    Q_MOD: [t_rect_dims, t_square_tiles, t_common_area],
    Q_REP: [t_area_read, t_table_fact, t_common_factor_read],
    Q_ARG: [t_error, t_restriction, t_not_factor, t_true, t_false],
}
