"""Clase 24 (M1) · Función lineal y afín II: modelación y comparación de tarifas."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
import viz


def f_(z):
    return "$" + f"{z:,}".replace(",", ".")


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


PLANS = [("un plan de internet", "GB", "GB"), ("un plan de telefonía", "minutos", "min"), ("una tarifa de electricidad", "kWh", "kWh"), ("un servicio de taxi", "kilómetros", "km"), ("un arriendo de auto", "días", "días"), ("un club deportivo", "clases", "clases")]


def tariff(r):
    ctx = r.choice(PLANS)
    a = r.choice([2000, 3000, 4000, 5000, 6000, 8000])
    b = r.choice([100, 150, 200, 250, 300, 400, 500])
    return ctx, a, b


# ---------------------------------------------------------------- Resolver problemas
def t_eval(r, l):
    (ctx, un, ab), a, b = tariff(r)
    n = r.randint(5, 60)
    fig = card([f"Tarifa de {ctx.split(' ', 1)[1]}", f"Cargo fijo: {f_(a)}", f"Por cada {ab}: {f_(b)}"], 170, 19)
    if l == 0:
        val = a + b * n
        stem = f"El costo mensual de {ctx} es C(n) = {a} + {b}n pesos, con n la cantidad de {un}. ¿Cuánto se paga si se usan {n} {un}?"
        alts = [(a + b) * n, a * n + b, a + b + n, val + b, val - a]
        ex = f"C({n}) = {a} + {b}·{n} = {val}."
    else:
        tot = a + b * n
        val = n
        stem = f"El costo mensual de {ctx} es C(n) = {a} + {b}n pesos, con n la cantidad de {un}. Si se pagaron {f_(tot)}, ¿cuántos {un} se usaron?"
        alts = [F(tot, b), F(tot + a, b), tot - a, n + 1, n - 1, F(tot - a, a)]
        ex = f"{a} + {b}n = {tot} ⟹ n = {n}."
    if l == 0:
        ans = f_(val)
        al = list(dict.fromkeys(f_(int(x)) for x in alts if F(x).denominator == 1 and x > 0 and x != val))
    else:
        ans = str(val)
        al = list(dict.fromkeys(fs(F(x)) for x in alts if F(x) > 0 and F(x) != val))
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_break_even(r, l):
    u = r.randint(5, 40)
    b1, b2 = r.choice([(300, 100), (400, 200), (500, 250), (600, 300), (250, 50), (150, 100)])
    d = (b1 - b2) * u
    a = r.choice([1000, 2000, 3000])
    c = a + d
    ctx = r.choice(PLANS)
    fig = card([f"Plan A: {f_(a)} + {f_(b1)} por {ctx[2]}", f"Plan B: {f_(c)} + {f_(b2)} por {ctx[2]}"], 130, 18)
    stem = f"El plan A cuesta C_A(n) = {a} + {b1}n y el plan B cuesta C_B(n) = {c} + {b2}n, con n la cantidad de {ctx[1]}. ¿Para qué valor de n ambos planes cuestan lo mismo?"
    ans = str(u)
    alts = [F(c - a, b1 + b2), F(c + a, b1 - b2), u + 5, u - 1, c - a]
    al = list(dict.fromkeys(fs(F(x)) for x in alts if F(x) > 0 and F(x) != u))
    return make(stem, fig, ans, al[:4], Q_RES, f"{a} + {b1}n = {c} + {b2}n ⟹ {b1 - b2}n = {d} ⟹ n = {u}.")


def t_prop(r, l):
    k = r.choice([3, 4, 5, 6, 8, 12, 15, 20])
    x = r.randint(3, 14)
    kind = r.choice(["val", "k"])
    ctx = r.choice([("Un auto recorre", "km", "litros"), ("Una máquina produce", "piezas", "horas"), ("Una llave llena", "litros", "minutos")])
    y = k * x
    if kind == "val":
        stem = f"{ctx[0]} {k * 2} {ctx[1]} en 2 {ctx[2]} de forma proporcional. ¿Cuántos {ctx[1]} recorre/produce en {x} {ctx[2]}?".replace("recorre/produce", "en total").replace("¿Cuántos", "¿Cuántos") if False else f"Una relación proporcional cumple f(2) = {k * 2}. ¿Cuánto vale f({x})?"
        ans = str(y)
        alts = [y + k, k * 2 + x, y - k, 2 * y, k + x]
        ex = f"f(x) = {k}x, luego f({x}) = {y}."
    else:
        stem = f"Una función lineal f(x) = kx cumple f({x}) = {y}. ¿Cuál es el valor de k?"
        ans = str(k)
        alts = [y - x, F(x, y), y + x, k + 1, k * x]
        ex = f"k = f({x})/{x} = {k}."
    fig = card(["Función lineal (proporcional):", "f(x) = kx"], 130, 20)
    al = list(dict.fromkeys(fs(F(a)) for a in alts if F(a) > 0 and fs(F(a)) != ans))
    return make(stem, fig, ans, al[:4], Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_choose(r, l):
    (ctx, un, ab), a, b = tariff(r)
    b2 = b + r.choice([50, 100])
    c = a - r.randint(1, 3) * 500
    if c <= 0:
        raise Reject
    n = r.randint(5, 40)
    ca, cb = a + b * n, c + b2 * n
    if ca == cb:
        raise Reject
    fig = card([f"Plan A: {f_(a)} + {f_(b)} por {ab}", f"Plan B: {f_(c)} + {f_(b2)} por {ab}", f"Uso mensual estimado: {n} {un}"], 170, 18)
    stem = f"Para {ctx} se comparan dos planes: el A cobra {f_(a)} más {f_(b)} por {ab} y el B cobra {f_(c)} más {f_(b2)} por {ab}. Con un uso de {n} {un} al mes, ¿qué plan conviene y cuánto se ahorra?"
    best = "A" if ca < cb else "B"
    ans = f"El plan {best}, con un ahorro de {f_(abs(ca - cb))}"
    other = "B" if best == "A" else "A"
    alts = [f"El plan {other}, con un ahorro de {f_(abs(ca - cb))}", f"El plan {best}, con un ahorro de {f_(abs(a - c))}", f"El plan {other}, con un ahorro de {f_(abs(b2 - b) * n + 500)}", f"El plan {best}, con un ahorro de {f_(abs(b2 - b))}"]
    return make(stem, fig, ans, alts, Q_MOD, f"Costo A = {f_(ca)} y costo B = {f_(cb)}: conviene el plan {best}.")


def t_piecewise(r, l):
    (ctx, un, ab), a, b = tariff(r)
    L = r.choice([5, 10, 15, 20])
    n = L + r.randint(2, 15)
    fig = card([f"{ctx.capitalize()}:", f"hasta {L} {un}: {f_(a)} en total", f"cada {ab} adicional: {f_(b)}"], 170, 18)
    kind = r.choice(["val", "expr"])
    if kind == "val":
        stem = f"En {ctx}, se pagan {f_(a)} por hasta {L} {un} y {f_(b)} por cada {ab} adicional sobre ese límite. ¿Cuánto se paga si se usan {n} {un}?"
        val = a + b * (n - L)
        ans = f_(val)
        alts = [a + b * n, b * n, val + b, a + b * (n - L) - a // 2, a * n]
        al = list(dict.fromkeys(f_(int(x)) for x in alts if x > 0 and x != val))
        return make(stem, fig, ans, al[:4], Q_MOD, f"Se paga el cargo por el límite más {n - L} unidades adicionales: {a} + {b}·{n - L} = {val}.")
    stem = f"En {ctx}, se pagan {f_(a)} por hasta {L} {un} y {f_(b)} por cada {ab} adicional sobre ese límite. ¿Qué expresión da el costo C(n) cuando n > {L}?"
    ans = f"C(n) = {a} + {b}(n − {L})"
    alts = [f"C(n) = {a} + {b}n", f"C(n) = {b}(n − {L})", f"C(n) = {a}(n − {L}) + {b}", f"C(n) = {a} + {b}(n + {L})"]
    return make(stem, fig, ans, alts, Q_MOD, "Sobre el límite solo se cobran las unidades adicionales (n − L) a la tarifa por unidad.")


# ---------------------------------------------------------------- Representar
def t_graph_two(r, l):
    m1, m2 = r.sample([1, 2, 3, 4], 2)
    n1, n2 = r.randint(1, 8), r.randint(1, 8)
    if n1 == n2:
        raise Reject
    p = Plot(560, 300, 0, 10, 0, 40)
    p.axes(2, 10)
    p.curve(lambda t: n1 + m1 * t, 0, 10, ACC, 4.5)
    p.curve(lambda t: n2 + m2 * t, 0, 10, NAVY, 4.5)
    fig = p.svg("Costo de dos planes").replace("</svg>", tag(300, 22, "Costo (miles de $) según el uso", 15) + "</svg>")
    kind = r.choice(["fixed", "slope"])
    if kind == "fixed":
        stem = "El gráfico muestra el costo de dos planes según el uso (rojo: plan A, azul: plan B). ¿Cuál plan tiene el menor cargo fijo?"
        ans = "Plan A" if n1 < n2 else "Plan B"
        ex = "El cargo fijo es el valor donde la recta corta al eje vertical (uso cero)."
    else:
        stem = "El gráfico muestra el costo de dos planes según el uso (rojo: plan A, azul: plan B). ¿Cuál plan tiene el mayor costo por unidad usada?"
        ans = "Plan A" if m1 > m2 else "Plan B"
        ex = "El costo por unidad es la pendiente: la recta más inclinada."
    other = "Plan B" if ans == "Plan A" else "Plan A"
    alts = [other, "Ambos planes tienen el mismo valor", "No se puede determinar con el gráfico", "Depende del uso que se haga"]
    return make(stem, fig, ans, alts, Q_REP, ex)


def t_table_plans(r, l):
    a, c = r.choice([(2, 6), (1, 5), (3, 7), (2, 8), (1, 9), (4, 10), (3, 9), (2, 4), (1, 3), (5, 11), (4, 8)])
    b1, b2 = 3, 1
    u = (c - a) // (b1 - b2) if (c - a) % (b1 - b2) == 0 else None
    if u is None or u < 1 or u > 5:
        raise Reject
    ns = [0, 1, 2, 3, 4, 5, 6]
    fig = viz.table_fig(["n"] + [str(n) for n in ns], [["Plan A"] + [str(a + b1 * n) for n in ns], ["Plan B"] + [str(c + b2 * n) for n in ns]])
    kind = r.choice(["eq", "cheap"])
    if kind == "eq":
        stem = "La tabla muestra el costo (en miles de pesos) de dos planes según el uso n. ¿Para qué valor de n ambos planes cuestan lo mismo?"
        ans = str(u)
        alts = [u + 1, u - 1 if u > 1 else u + 2, c, a, u + 2]
        al = [str(x) for x in dict.fromkeys(alts) if x != u and x >= 0]
        return make(stem, fig, ans, al[:4], Q_REP, f"En n = {u} ambas filas valen {a + b1 * u}.")
    n = min(6, u + r.choice([1, 2]))
    stem = f"La tabla muestra el costo (en miles de pesos) de dos planes según el uso n. ¿Qué plan es más barato para n = {n}?"
    ans = "Plan A" if a + b1 * n < c + b2 * n else "Plan B"
    alts = ["Plan B" if ans == "Plan A" else "Plan A", "Cuestan lo mismo", "No se puede saber con la tabla", "Depende del cargo fijo únicamente"]
    return make(stem, fig, ans, alts, Q_REP, f"Para n = {n} el plan A cuesta {a + b1 * n} y el plan B {c + b2 * n}.")


def t_graph_piece(r, l):
    L = r.choice([2, 4, 5, 6])
    a = r.choice([10, 12, 15, 20])
    m = r.choice([2, 3, 4])
    f = lambda t: a if t <= L else a + m * (t - L)
    p = Plot(560, 300, 0, 10, 0, 40)
    p.axes(2, 10)
    p.curve(f, 0, 10, ACC, 4.5, n=400)
    fig = p.svg("Costo con un tramo fijo y un tramo variable").replace("</svg>", tag(300, 22, "Costo (miles de $) según el uso", 15) + "</svg>")
    n = L + r.randint(1, 10 - L)
    if f(n) > 40:
        raise Reject
    kind = r.choice(["val", "meaning"])
    if kind == "val":
        stem = f"El gráfico muestra el costo (en miles de pesos) de una tarifa según el uso. ¿Cuánto cuesta un uso de {n}?"
        val = f(n)
        ans = str(val)
        alts = [a, a + m * n, val + m, val - m, a + n]
        al = [str(x) for x in dict.fromkeys(alts) if x != val and x > 0]
        return make(stem, fig, ans, al[:4], Q_REP, f"Después de {L} el costo crece {m} por unidad: {a} + {m}·{n - L} = {val}.")
    stem = "El gráfico muestra el costo (en miles de pesos) de una tarifa según el uso. ¿Qué describe el tramo horizontal inicial?"
    ans = f"Hasta un uso de {L} el costo es constante e igual a {a} mil pesos"
    alts = [f"Hasta un uso de {L} el costo aumenta {a} mil pesos por unidad", f"Con un uso de {a} el costo es {L} mil pesos", f"Desde un uso de {L} el costo se mantiene constante", "El costo disminuye mientras aumenta el uso de la tarifa"]
    return make(stem, fig, ans, alts, Q_REP, "Un tramo horizontal indica que el costo no cambia al aumentar el uso.")


# ---------------------------------------------------------------- Argumentar
def t_claim(r, l):
    (ctx, un, ab), a, b = tariff(r)
    c = a + r.randint(1, 3) * 1000
    b2 = b - r.choice([50, 100])
    if b2 <= 0:
        raise Reject
    u = (c - a) // (b - b2) if (c - a) % (b - b2) == 0 else None
    if u is None or u < 3:
        raise Reject
    fig = card([f"Plan A: {f_(a)} + {f_(b)} por {ab}", f"Plan B: {f_(c)} + {f_(b2)} por {ab}"], 130, 18)
    stem = f"Un cliente dice: «El plan B siempre es más barato que el plan A porque cobra menos por {ab}». ¿Es correcta su afirmación?"
    ans = f"No: con menos de {u} {un} el plan A es más barato, porque su cargo fijo es menor"
    alts = [f"Sí: el plan B es más barato con cualquier uso, porque su pendiente es menor", f"No: con más de {u} {un} el plan A es más barato, porque su cargo fijo es menor", f"Sí: con {u} {un} el plan B es más barato que el plan A", "No: ambos planes cuestan lo mismo con cualquier uso mensual"]
    return make(stem, fig, ans, alts, Q_ARG, f"Ambos cuestan lo mismo con {u} {un}; antes conviene A (menor cargo fijo) y después B (menor costo por {ab}).")


def _err(r):
    k = r.randrange(4)
    a, b = r.choice([(3000, 200), (5000, 300), (2000, 500)])
    n = r.randint(5, 20)
    if k == 0:
        return [f"C(n) = {a} + {b}n", f"C({n}) = ({a} + {b})·{n} = {(a + b) * n}"], "Sumó el cargo fijo al costo unitario antes de multiplicar: el cargo fijo se paga una sola vez", \
            ["Multiplicó el cargo fijo por la cantidad de unidades y sumó el costo unitario", "Restó el cargo fijo en lugar de sumarlo al costo variable del uso", "Usó el costo por unidad como si fuera el cargo fijo de la tarifa", "Reemplazó n por el cargo fijo y calculó el costo variable con ese número"]
    if k == 1:
        return [f"Plan: {a} fijos y {b} por unidad", f"C(n) = {b} + {a}n"], "Intercambió el cargo fijo y el costo por unidad: el costo por unidad multiplica a n", \
            ["Sumó ambos valores y multiplicó el total por n para obtener el costo", "Restó el costo unitario del cargo fijo antes de multiplicar por n", "Dejó el costo por unidad sin variable y multiplicó solo el cargo fijo", "Escribió correctamente la función pero cambió la variable por otra letra"]
    if k == 2:
        return [f"Dos planes con pendientes {b} y {b + 100}", "El de pendiente menor siempre es más barato"], "No consideró el cargo fijo: un plan de menor pendiente puede ser más caro para poco uso", \
            ["Consideró que la pendiente menor implica un cargo fijo mayor en todos los casos", "Comparó los costos solo cuando el uso es cero y concluyó con ese valor", "Supuso que ambas rectas se cruzan siempre en el origen del plano cartesiano", "Comparó las pendientes pero olvidó que el costo depende también de n"]
    return [f"Gráfico de costo: recta que sube {b} por unidad", "«El punto donde corta al eje Y es el costo por unidad»"], "El corte con el eje vertical es el cargo fijo (uso cero); el costo por unidad es la pendiente", \
        ["El corte con el eje vertical es el uso máximo permitido por la tarifa", "El corte con el eje horizontal es el cargo fijo de la tarifa siempre", "El corte con el eje vertical es el costo total para un uso muy grande", "El corte con el eje vertical siempre vale cero en una función afín"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["En C(n) = a + bn, a es el cargo fijo y b es el costo por unidad", "Dos tarifas lineales se cruzan en el uso en que sus costos son iguales", "Una función lineal f(x) = kx representa una relación de proporcionalidad directa",
        "Una función afín con intercepto distinto de cero no representa una proporcionalidad directa", "Para comparar dos planes hay que considerar el cargo fijo y el costo por unidad", "Después del punto de cruce, conviene el plan de menor pendiente"]
FALSE = ["En C(n) = a + bn, a es el costo por unidad y b es el cargo fijo", "El plan con menor cargo fijo es más barato para cualquier uso", "Una función afín con intercepto distinto de cero siempre pasa por el origen",
         "Dos tarifas lineales con distinta pendiente nunca se cruzan", "Basta comparar los precios por unidad para decidir cuál plan conviene", "Antes del punto de cruce, conviene siempre el plan de mayor cargo fijo"]


def _fig(r):
    return card(["Modelos lineales de tarifas", "C(n) = cargo fijo + costo por unidad · n"], 130, 18)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre modelos lineales de tarifas es verdadera?", "Sobre comparar planes con funciones lineales, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el significado de cargo fijo y costo por unidad.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre modelos lineales de tarifas es falsa?", "Sobre comparar planes con funciones lineales, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el modelo C(n) = a + bn.")


BY_SKILL = {
    Q_RES: [t_eval, t_break_even, t_prop],
    Q_MOD: [t_choose, t_piecewise],
    Q_REP: [t_graph_two, t_table_plans, t_graph_piece],
    Q_ARG: [t_claim, t_error, t_true, t_false],
}
