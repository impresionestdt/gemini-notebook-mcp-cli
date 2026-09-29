"""Clase 22 (M1) · Función: concepto y evaluación; variable dependiente e independiente."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
from figs import arrow_diagram
import viz


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def fexpr(kind, a, b, c=0):
    if kind == "lin":
        return lin(a, b)
    return co(1, "x²", True) + co(a, "x", False) + co(b, "", False)


def fval(kind, a, b, x):
    return a * x + b if kind == "lin" else x * x + a * x + b


# ---------------------------------------------------------------- Resolver problemas
def t_eval(r, l):
    kind = "lin" if l == 0 else r.choice(["lin", "quad"])
    a, b = (rr(r, -6, 7), rr(r, -8, 9)) if kind == "lin" else (rr(r, -5, 5), rr(r, -8, 8))
    x = rr(r, -5, 6)
    v = fval(kind, a, b, x)
    fx = fexpr(kind, a, b)
    if l == 2:
        x2 = rr(r, -4, 4)
        while x2 == x:
            x2 = rr(r, -4, 4)
        v = fval(kind, a, b, x) + fval(kind, a, b, x2)
        stem = f"Sea f(x) = {fx}. ¿Cuál es el valor de f({x}) + f({x2})?".replace("-", "−")
        alts = [fval(kind, a, b, x + x2), fval(kind, a, b, x) - fval(kind, a, b, x2), fval(kind, a, b, x) * fval(kind, a, b, x2), v + a, -v]
        ex = f"f({x}) = {fval(kind, a, b, x)} y f({x2}) = {fval(kind, a, b, x2)}; la suma es {v}."
    else:
        stem = f"Sea f(x) = {fx}. ¿Cuál es el valor de f({x})?".replace("-", "−")
        alts = [fval(kind, a, b, -x), fval(kind, -a, b, x) if kind == "lin" else fval(kind, a, -b, x), a * x, v + 1, v - 1, v + a]
        if kind == "quad":
            alts.append(-x * x + a * x + b)
        ex = f"Se reemplaza x por {x}: f({x}) = {v}."
    if abs(v) > 300:
        raise Reject
    fig = card(["Función:", f"f(x) = {fx}".replace("-", "−")], 130, 24)
    ans = fs(F(v))
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, ex.replace("-", "−"))


def t_find_x(r, l):
    a, b = rr(r, -6, 7), rr(r, -8, 9)
    if abs(a) == 1:
        a *= 2
    x = rr(r, -6, 8)
    k = a * x + b
    fig = card(["Función:", f"f(x) = {lin(a, b)}".replace("-", "−"), f"f(x) = {k}".replace("-", "−")], 170, 22)
    stem = f"Sea f(x) = {lin(a, b)}. ¿Para qué valor de x se cumple que f(x) = {k}?".replace("-", "−")
    ans = fs(F(x))
    alts = [F(k - b, -a), F(k + b, a), F(k, a) + b, x + 1, -x, F(k - b)]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, f"{lin(a, b)} = {k} ⟹ x = {x}.".replace("-", "−"))


def t_range(r, l):
    a, b = rr(r, -3, 4), rr(r, -4, 5)
    dom = sorted(r.sample(range(-3, 5), 4))
    kind = "lin" if l < 2 else r.choice(["lin", "quad"])
    if kind == "quad":
        a, b = rr(r, -2, 2), rr(r, -3, 3)
    ys = sorted({fval(kind, a, b, x) for x in dom})
    fx = fexpr(kind, a, b)
    fig = card(["Función:", f"f(x) = {fx}".replace("-", "−"), ("Dominio: {" + ", ".join(map(str, dom)) + "}").replace("-", "−")], 170, 20)
    ans = "{" + ", ".join(map(str, ys)) + "}"
    alts = ["{" + ", ".join(str(fval(kind, a, b, x) + 1) for x in dom) + "}", "{" + ", ".join(str(-fval(kind, a, b, x)) for x in dom) + "}", "{" + ", ".join(map(str, dom)) + "}", "{" + ", ".join(str(fval(kind, a, b, x)) for x in dom[:-1]) + "}", "{" + ", ".join(str(a * x) for x in dom) + "}"]
    al = uq(ans.replace("-", "−"), [x.replace("-", "−") for x in alts])
    stem = f"La función f(x) = {fx} tiene como dominio el conjunto de la figura. ¿Cuál es su recorrido?".replace("-", "−")
    return make(stem, fig, ans.replace("-", "−"), al[:4], Q_RES, "El recorrido es el conjunto de las imágenes f(x) de cada elemento del dominio.")


# ---------------------------------------------------------------- Modelar
def t_cost_fn(r, l):
    a, b = r.choice([(2000, 500), (3000, 800), (1500, 300), (5000, 1000), (4000, 600)])
    n = r.randint(3, 20)
    ctx = r.choice([("una tarifa de estacionamiento", "horas", "por hora"), ("un servicio de taxi", "kilómetros", "por kilómetro"), ("un arriendo de bicicleta", "horas", "por hora")])
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    kind = r.choice(["eval", "model"])
    fig = card([f"{ctx[0].capitalize()}: {f(a)} fijos", f"más {f(b)} {ctx[2]}"], 130, 19)
    if kind == "eval":
        stem = f"El costo de {ctx[0]} es C(n) = {a} + {b}n, con n la cantidad de {ctx[1]}. ¿Cuál es el costo para n = {n}?"
        val = a + b * n
        alts = [(a + b) * n, a * n + b, a + b + n, val + b, val - a]
        ans = f(val)
        al = list(dict.fromkeys(f(x) for x in alts if x > 0 and x != val))
        return make(stem, fig, ans, al[:4], Q_MOD, f"C({n}) = {a} + {b}·{n} = {val}.")
    stem = f"{ctx[0].capitalize()} cobra {f(a)} fijos más {f(b)} {ctx[2]}. ¿Qué función representa el costo C en función de n ({ctx[1]})?"
    ans = f"C(n) = {a} + {b}n"
    alts = [f"C(n) = {a}n + {b}", f"C(n) = {a + b}n", f"C(n) = {a}·{b}n", f"C(n) = {b} + {a}n"]
    return make(stem, fig, ans, alts, Q_MOD, "Costo = parte fija + costo variable por cada unidad.")


def t_conversion(r, l):
    c = r.choice([-10, 0, 5, 10, 15, 20, 25, 30, 35, 40, 100])
    fig = card(["Fórmula: F(C) = 9C/5 + 32", "C: grados Celsius · F: grados Fahrenheit"], 130, 19)
    kind = r.choice(["fwd", "back"])
    if kind == "fwd":
        val = F(9 * c, 5) + 32
        if val.denominator != 1:
            raise Reject
        stem = f"La temperatura en grados Fahrenheit se calcula con F(C) = 9C/5 + 32, con C en grados Celsius. ¿Cuál es F({c})?".replace("-", "−")
        alts = [F(9 * c, 5), 9 * c // 5 - 32, c + 32, F(5 * c, 9) + 32, val + 9]
        ans = fs(val)
        return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"F({c}) = 9·{c}/5 + 32 = {fs(val)}.".replace("-", "−"))
    fh = 9 * c // 5 + 32 if (9 * c) % 5 == 0 else None
    if fh is None:
        raise Reject
    stem = f"La temperatura en grados Fahrenheit se calcula con F(C) = 9C/5 + 32. Si una temperatura es {fh} °F, ¿cuántos grados Celsius son?".replace("-", "−")
    alts = [F(5 * fh, 9) + 32, F(5 * fh, 9), fh - 32, F(9 * (fh - 32), 5), c + 5]
    ans = fs(F(c))
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"9C/5 + 32 = {fh} ⟹ C = {c}.".replace("-", "−"))


def t_area_fn(r, l):
    k = r.randint(1, 6)
    x = r.randint(2, 9)
    body = R(140, 40, 240, 110, FILL, NAVY, 3) + tag(260, 165, f"x + {k}", 18) + tag(110, 95, "x", 18)
    fig = wrap(560, 200, body, "Rectángulo de lados x y x + k")
    A = x * (x + k)
    stem = f"El área de un rectángulo de lados x y (x + {k}) se modela con A(x) = x(x + {k}). ¿Cuál es el área cuando x = {x}?"
    ans = str(A)
    alts = [2 * x + k, x * x + k, A + k, 2 * (x + x + k), x + x + k]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"A({x}) = {x}·{x + k} = {A}.")


# ---------------------------------------------------------------- Representar
def t_table(r, l):
    a, b = rr(r, -4, 5), rr(r, -6, 7)
    xs = [-2, -1, 0, 1, 2, 3]
    k = r.choice([x for x in xs if x != 0])
    fig = viz.table_fig(["x"] + [str(x).replace("-", "−") for x in xs], [["f(x)"] + [str(a * x + b).replace("-", "−") for x in xs]])
    kind = r.choice(["read", "formula"])
    if kind == "read":
        stem = f"La tabla muestra algunos valores de una función f. ¿Cuál es el valor de f({k})?".replace("-", "−")
        ans = str(a * k + b).replace("-", "−")
        alts = [k, a * k + b + 1, b, a * (-k) + b, a * k]
        al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != a * k + b]
        return make(stem, fig, ans, al[:4], Q_REP, f"Se busca la columna x = {k}: f({k}) = {ans}.".replace("-", "−"))
    stem = "La tabla muestra los valores de una función f de la forma f(x) = ax + b. ¿Cuál es la expresión de f?"
    ans = f"f(x) = {lin(a, b)}".replace("-", "−")
    alts = [f"f(x) = {lin(b, a)}", f"f(x) = {lin(a, -b)}", f"f(x) = {lin(-a, b)}", f"f(x) = {lin(a + 1, b)}", f"f(x) = {lin(a, b + 1)}"]
    al = uq(ans, [x.replace("-", "−") for x in alts])
    return make(stem, fig, ans, al[:4], Q_REP, f"f(0) = {b} es el término independiente y la variación por cada unidad de x es {a}.".replace("-", "−"))


def t_arrow(r, l):
    A = [1, 2, 3, 4][: 3 + (l > 0)]
    a, b = rr(r, 1, 3), rr(r, -3, 4)
    B = sorted({a * x + b for x in A} | {r.randint(-4, 12)})
    pairs = [(x, a * x + b) for x in A]
    fig = arrow_diagram(A, B, pairs)
    k = r.choice(A)
    kind = r.choice(["img", "pre"])
    if kind == "img":
        stem = f"El diagrama muestra una función de A en B (cada flecha une un elemento con su imagen). ¿Cuál es la imagen de {k}?"
        val = a * k + b
        alts = [k, val + 1, val - 1, a * k, val + a]
        ans = str(val).replace("-", "−")
        al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != val]
        ex = f"La flecha que sale de {k} llega a {ans}."
    else:
        val = k
        y = a * k + b
        stem = f"El diagrama muestra una función de A en B (cada flecha une un elemento con su imagen). ¿Qué elemento de A tiene como imagen a {y}?".replace("-", "−")
        alts = [x for x in A if x != k] + [y]
        ans = str(k)
        al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != k]
        ex = f"La flecha que llega a {y} sale de {k}.".replace("-", "−")
    return make(stem, fig, ans, al[:4], Q_REP, ex.replace("-", "−")) if len(al) >= 4 else (_ for _ in ()).throw(Reject())


def t_graph_read(r, l):
    kind = r.choice(["lin", "quad"]) if l else "lin"
    if kind == "lin":
        a, b = rr(r, -2, 3), rr(r, -3, 4)
        f = lambda x: a * x + b
        fx = None
    else:
        a, b = rr(r, -1, 1), rr(r, -3, 2)
        f = lambda x: x * x + a * x + b
    p = Plot(560, 300, -5, 5, -6, 10)
    p.axes(1, 2)
    p.curve(f, -5, 5, ACC, 4.5)
    fig = p.svg("Gráfico de una función")
    k = rr(r, -3, 3)
    v = f(k)
    if not (-6 <= v <= 10):
        raise Reject
    stem = f"El gráfico muestra la función f. ¿Cuál es el valor de f({k})?".replace("-", "−")
    ans = str(v).replace("-", "−")
    alts = [k, v + 1, v - 1, f(-k), v + 2]
    al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != v]
    return make(stem, fig, ans, al[:4], Q_REP, f"Se ubica x = {k} en el eje horizontal y se lee la altura de la curva: {ans}.".replace("-", "−"))


# ---------------------------------------------------------------- Argumentar
def t_is_function(r, l):
    xs = [1, 2, 3, 4]
    good = "{" + ", ".join(f"({x}, {r.randint(1, 9)})" for x in xs) + "}"
    def bad():
        ys = [r.randint(1, 9) for _ in xs]
        i = r.randrange(3)
        pts = [f"({x}, {y})" for x, y in zip(xs, ys)]
        pts[i + 1] = f"({xs[i]}, {ys[i] + r.randint(1, 4)})"
        return "{" + ", ".join(pts) + "}"
    alts = list(dict.fromkeys(bad() for _ in range(8)))
    alts = [a for a in alts if a != good]
    if len(alts) < 4:
        raise Reject
    fig = card(["Una función asigna a cada x", "exactamente un valor de y"], 130, 21)
    return make("¿Cuál de las siguientes relaciones, dadas como pares (x, y), representa una función de x?", fig, good, alts[:4], Q_ARG, "En una función cada valor de x aparece con un único valor de y; en las demás relaciones un x se repite con dos valores distintos.")


CTX = [("el costo total de la compra", "los kilos comprados", "el precio por kilo"), ("la distancia recorrida", "el tiempo de viaje", "la rapidez constante"), ("el pago por horas trabajadas", "las horas trabajadas", "el valor de la hora"),
       ("el monto de la cuenta de luz", "los kWh consumidos", "el precio por kWh"), ("el volumen de agua en un estanque", "el tiempo que lleva llenándose", "el caudal constante"), ("el área de un cuadrado", "la medida de su lado", "la forma cuadrada")]


def t_dependent(r, l):
    dep, ind, const = r.choice(CTX)
    ask = r.choice(["ind", "dep"])
    fig = card(["Relación entre dos cantidades:", dep.capitalize(), f"depende de {ind}"], 170, 19)
    if ask == "ind":
        stem = f"En la relación «{dep} depende de {ind}», ¿cuál es la variable independiente?"
        ans = ind.capitalize()
        alts = [dep.capitalize(), const.capitalize() + ", que cambia en cada valor", "Ambas variables son independientes", "Ninguna, porque la relación no es una función"]
    else:
        stem = f"En la relación «{dep} depende de {ind}», ¿cuál es la variable dependiente?"
        ans = dep.capitalize()
        alts = [ind.capitalize(), const.capitalize() + ", que cambia en cada valor", "Ambas variables son dependientes", "Ninguna, porque la relación no es una función"]
    return make(stem, fig, ans, alts, Q_ARG, "La variable independiente es la que se elige libremente; la dependiente queda determinada por ella.")


def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 6), r.randint(1, 9)
    if k == 0:
        return [f"f(x) = x² + {b}x", f"f(−3) = −9 − {3 * b}"], "Elevó al cuadrado solo el número 3 y no el signo: (−3)² = 9, no −9", \
            ["Reemplazó x por 3 en lugar de reemplazarlo por −3 en ambos términos", "Multiplicó el valor por el exponente en vez de elevarlo al cuadrado", "Sumó el exponente al valor en lugar de elevar la base al cuadrado", "Cambió el signo del término lineal pero no el del término cuadrático"]
    if k == 1:
        return [f"f(x) = {a}x − {b}", f"f(2) = {a} · 2 − {b} = {a} · (2 − {b})"], "Distribuyó mal el producto: a·2 − b no es a·(2 − b); solo el 2 multiplica al coeficiente", \
            ["Reemplazó x por 2 solo en el término numérico de la función dada", "Sumó el 2 al coeficiente de x en vez de multiplicarlo por él", "Restó el 2 al término independiente y omitió el producto con x", "Evaluó la función en x = 0 y no en x = 2 como se pedía"]
    if k == 2:
        return [f"f(x) = {a}x + {b}", f"f(x + 1) = {a}x + {b} + 1"], "Sumó 1 al resultado en vez de reemplazar x por (x + 1): f(x + 1) = a(x + 1) + b", \
            ["Sumó 1 solo al término independiente y dejó el término con x intacto", "Reemplazó x por 1 y no por (x + 1) en la expresión de la función", "Multiplicó la función completa por (x + 1) en lugar de reemplazarla", "Evaluó f en x y luego agregó uno al coeficiente de la variable"]
    return ["y depende de x", "«x es la variable dependiente porque se elige primero»"], "La variable que se elige primero es la independiente; la dependiente es la que resulta de aplicarle la regla de la función", \
        ["La variable dependiente es la que se elige y la independiente la que resulta siempre", "Ambas variables se llaman independientes cuando la relación es una función lineal", "La variable dependiente se elige en el eje horizontal y la otra en el eje vertical siempre", "No existe diferencia entre variable dependiente e independiente en una función"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["En una función, cada valor de x tiene exactamente una imagen", "El dominio de una función es el conjunto de valores que puede tomar x", "El recorrido de una función es el conjunto de sus imágenes",
        "Si f(2) = 5, el punto (2, 5) pertenece al gráfico de f", "En f(x) = 3x, la variable independiente es x", "Dos valores distintos de x pueden tener la misma imagen en una función"]
FALSE = ["En una función, un valor de x puede tener dos imágenes distintas", "El recorrido de una función es el conjunto de valores que puede tomar x", "Si f(2) = 5, el punto (5, 2) pertenece al gráfico de f",
         "En f(x) = 3x, la variable independiente es f(x)", "Dos valores distintos de x nunca pueden tener la misma imagen en una función", "Toda relación entre dos variables es una función"]


def _fig(r):
    return card(["Funciones", "Dominio · recorrido · imagen · variable independiente"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones es verdadera?", "Sobre el concepto de función, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la definición de función.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones es falsa?", "Sobre el concepto de función, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la definición de función.")


BY_SKILL = {
    Q_RES: [t_eval, t_find_x, t_range],
    Q_MOD: [t_cost_fn, t_conversion, t_area_fn],
    Q_REP: [t_table, t_arrow, t_graph_read],
    Q_ARG: [t_is_function, t_dependent, t_error, t_true, t_false],
}
