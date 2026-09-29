"""Clase 23 (M1) · Función lineal y afín I: gráficas, pendiente e intercepto."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
import viz


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def M(s):
    return s.replace("-", "−")


def eqline(m, n):
    """y = m x + n con m racional."""
    m = F(m)
    if m.denominator == 1:
        ms = co(int(m), "x", True)
    else:
        ms = ("−" if m < 0 else "") + (f"{abs(m.numerator)}x/{m.denominator}")
    nn = F(n)
    ns = "" if nn == 0 else (f" − {fs(abs(nn))}" if nn < 0 else f" + {fs(nn)}")
    return f"y = {ms}{ns}" if m != 0 else f"y = {fs(nn)}"


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def pair(x, y):
    return M(f"({fs(F(x))}, {fs(F(y))})")


def line_plot(f, pts=(), labels=True, yr=(-6, 6), xr=(-6, 6)):
    p = Plot(560, 300, xr[0], xr[1], yr[0], yr[1])
    p.axes(2, 2)
    p.curve(f, xr[0], xr[1], ACC, 4.5)
    for (x, y) in pts:
        p.pt(x, y, pair(x, y) if labels else None, 0, -26)
    return p.svg("Gráfico de una recta")


# ---------------------------------------------------------------- Resolver problemas
def t_slope(r, l):
    m = F(rr(r, -4, 5)) if l < 2 else F(rr(r, -4, 4), r.choice([2, 3]))
    x1 = rr(r, -4, 3)
    dx = m.denominator * r.randint(1, 2) if m.denominator != 1 else rr(r, 1, 4)
    y1 = rr(r, -5, 5)
    x2 = x1 + dx
    y2 = y1 + m * dx
    if y2.denominator != 1 or abs(y2) > 12:
        raise Reject
    kind = r.choice(["slope", "eq"]) if l else "slope"
    fig = card(["Puntos de una recta:", f"A = {pair(x1, y1)}", f"B = {pair(x2, int(y2))}"], 170, 21)
    if kind == "slope":
        ans = fs(m)
        alts = [-m, F(1, m) if m else 1, F(x2 - x1, int(y2) - y1) if int(y2) != y1 else 2, m + 1, F(int(y2) + y1, x2 + x1) if x2 + x1 else 3]
        return make("¿Cuál es la pendiente de la recta que pasa por los puntos A y B?", fig, ans, pick4(ans, uq(ans, alts)), Q_RES, f"m = (y₂ − y₁)/(x₂ − x₁) = ({int(y2)} − {y1})/({x2} − {x1}) = {fs(m)}.".replace("-", "−"))
    n = y1 - m * x1
    ans = M(eqline(m, n))
    alts = [eqline(-m, n), eqline(m, -n), eqline(m, y1), eqline(F(1, m) if m else 1, n), eqline(m, n + 1)]
    return make("¿Cuál es la ecuación de la recta que pasa por los puntos A y B?", fig, ans, pick4(ans, uq(ans, [M(a) for a in alts])), Q_RES, f"Pendiente {fs(m)} y n = y₁ − m·x₁ = {fs(n)}.".replace("-", "−"))


def t_intercepts(r, l):
    m = rr(r, -4, 5)
    xi = rr(r, -5, 6)
    n = -m * xi
    if abs(n) > 20:
        raise Reject
    ask = r.choice(["x", "y"])
    fig = card(["Recta:", M(eqline(m, n))], 130, 24)
    if ask == "x":
        stem = f"¿En qué punto corta al eje X la recta {M(eqline(m, n))}?"
        ans = pair(xi, 0)
        alts = [pair(0, n), pair(-xi, 0), pair(n, 0), pair(0, xi), pair(xi + 1, 0)]
        ex = f"Con y = 0: {m}x + ({n}) = 0 ⟹ x = {xi}."
    else:
        stem = f"¿En qué punto corta al eje Y la recta {M(eqline(m, n))}?"
        ans = pair(0, n)
        alts = [pair(n, 0), pair(0, -n), pair(xi, 0), pair(0, m), pair(0, n + 1)]
        ex = f"Con x = 0: y = {n}."
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, M(ex))


def t_line_eq(r, l):
    m = rr(r, -4, 5)
    x0, y0 = rr(r, -4, 4), rr(r, -6, 6)
    n = y0 - m * x0
    fig = card(["Recta con pendiente " + fs(F(m)).replace("-", "−"), f"que pasa por el punto {pair(x0, y0)}"], 130, 20)
    ans = M(eqline(m, n))
    alts = [eqline(m, y0), eqline(m, -n), eqline(-m, n), eqline(m, y0 + x0), eqline(F(1, m), n)]
    return make("¿Cuál es la ecuación de la recta descrita en la figura?", fig, ans, pick4(ans, uq(ans, [M(a) for a in alts])), Q_RES, f"y − {y0} = {m}(x − {x0}) ⟹ {ans}.".replace("-", "−"))


# ---------------------------------------------------------------- Modelar
def t_two_data(r, l):
    a, b = r.choice([(2, 10), (3, 14), (1, 8), (4, 20), (2, 7), (5, 18)])
    m = rr(r, 1, 6) if l < 2 else -rr(r, 1, 3)
    t1, t2 = r.randint(1, 4), r.randint(5, 9)
    v1, v2 = b + m * t1, b + m * t2
    if v1 <= 0 or v2 <= 0:
        raise Reject
    ctx = r.choice([("Un tanque de agua", "litros", "horas"), ("Una planta", "cm", "semanas"), ("Un ahorro", "miles de pesos", "meses")])
    fig = viz.table_fig(["Tiempo", str(t1), str(t2)], [["Cantidad", str(v1), str(v2)]])
    kind = r.choice(["model", "value"])
    if kind == "model":
        stem = f"La tabla muestra la cantidad de {ctx[1]} de {ctx[0].lower()} a los {t1} y a los {t2} ({ctx[2]}) y se sabe que el cambio es lineal. ¿Qué función modela la cantidad C según el tiempo t?"
        ans = M(f"C(t) = {lin(m, b, 't')}")
        alts = [f"C(t) = {lin(m, b + m, 't')}", f"C(t) = {lin(-m, b, 't')}", f"C(t) = {lin(b, m, 't')}", f"C(t) = {lin(m, v1, 't')}", f"C(t) = {lin(m + 1, b, 't')}"]
        return make(stem, fig, ans, pick4(ans, uq(ans, [M(x) for x in alts])), Q_MOD, f"m = ({v2} − {v1})/({t2} − {t1}) = {m}; C(0) = {b}.".replace("-", "−"))
    t3 = t2 + r.randint(1, 4)
    v3 = b + m * t3
    if v3 <= 0:
        raise Reject
    stem = f"La tabla muestra la cantidad de {ctx[1]} de {ctx[0].lower()} a los {t1} y a los {t2} ({ctx[2]}); el cambio es lineal. ¿Cuánto habrá a los {t3} ({ctx[2]})?"
    ans = str(v3)
    alts = [v2 + (v2 - v1), v3 + m, v3 - m, v2 + m, v3 + b]
    al = [str(x) for x in dict.fromkeys(alts) if x != v3 and x > 0]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Se usa la tasa de cambio {m} por cada unidad de tiempo: {v3}.".replace("-", "−"))


def t_candle(r, l):
    h0 = r.choice([20, 24, 30, 36, 40, 48])
    v = r.choice([2, 3, 4, 6])
    if h0 % v:
        raise Reject
    T = h0 // v
    fig = card([f"Una vela mide {h0} cm", f"y se consume {v} cm cada hora"], 130, 21)
    kind = r.choice(["expr", "end", "at"])
    if kind == "expr":
        stem = f"Una vela mide {h0} cm y se consume {v} cm cada hora. ¿Qué función representa su altura h después de t horas?"
        ans = f"h(t) = {h0} − {v}t"
        alts = [f"h(t) = {h0} + {v}t", f"h(t) = {v} − {h0}t", f"h(t) = {v}t − {h0}", f"h(t) = {h0}·{v}t"]
        return make(stem, fig, ans, alts, Q_MOD, "Altura inicial menos lo consumido: la pendiente es negativa.")
    if kind == "end":
        stem = f"Una vela mide {h0} cm y se consume {v} cm cada hora. ¿Después de cuántas horas se acaba?"
        ans = str(T)
        alts = [h0 * v, T + 1, T - 1 if T > 1 else T + 2, h0 - v, F(v, h0)]
        al = [fs(F(x)) for x in dict.fromkeys(alts) if F(x) != T and F(x) > 0]
        return make(stem, fig, ans, al[:4], Q_MOD, f"{h0} − {v}t = 0 ⟹ t = {T}.")
    t = r.randint(1, T - 1)
    stem = f"Una vela mide {h0} cm y se consume {v} cm cada hora. ¿Cuánto mide después de {t} horas?"
    ans = str(h0 - v * t)
    alts = [h0 + v * t, h0 - v, v * t, h0 - t, h0 - v * t + v]
    al = [str(x) for x in dict.fromkeys(alts) if x != h0 - v * t and x > 0]
    return make(stem, fig, ans, al[:4], Q_MOD, f"h({t}) = {h0} − {v}·{t} = {h0 - v * t}.")


# ---------------------------------------------------------------- Representar
def t_read_line(r, l):
    m = rr(r, -3, 3)
    n = rr(r, -4, 4)
    f = lambda x: m * x + n
    xs = sorted(r.sample([-3, -2, -1, 0, 1, 2, 3], 2))
    pts = [(x, f(x)) for x in xs]
    if any(abs(y) > 6 for _, y in pts):
        raise Reject
    fig = line_plot(f, pts)
    ans = M(eqline(m, n))
    alts = [eqline(-m, n), eqline(m, -n), eqline(n, m), eqline(m, n + 1), eqline(-m, -n)]
    return make("El gráfico muestra una recta con dos de sus puntos. ¿Cuál es su ecuación?", fig, ans, pick4(ans, uq(ans, [M(a) for a in alts])), Q_REP, f"La recta corta al eje Y en {n} y su pendiente es {m}.".replace("-", "−"))


def t_interpret(r, l):
    a = r.randint(2, 8)
    b = r.randint(1, 4)
    p = Plot(560, 300, 0, 10, 0, 40)
    p.axes(2, 10)
    p.curve(lambda t: a * 2 + b * 4 * t / 2, 0, 10, ACC, 4.5)
    fig = p.svg("Costo según las unidades")
    slope = 2 * b
    icept = 2 * a
    fig = fig.replace("</svg>", tag(300, 22, "Costo (miles de $) según unidades usadas", 15) + "</svg>")
    kind = r.choice(["slope", "icept"])
    if kind == "slope":
        stem = f"El gráfico muestra el costo (en miles de pesos) de un servicio según las unidades usadas. ¿Qué representa la pendiente de la recta?"
        ans = f"El costo, en miles de pesos, de cada unidad adicional usada: {slope} mil pesos"
        alts = [f"El costo del servicio cuando no se usa ninguna unidad: {icept} mil pesos", f"El costo total cuando se usan 10 unidades: {icept + slope * 10} mil pesos", f"La cantidad máxima de unidades que se pueden usar: 10 unidades", f"El costo fijo que se paga sin importar el uso: {slope} mil pesos"]
    else:
        stem = f"El gráfico muestra el costo (en miles de pesos) de un servicio según las unidades usadas. ¿Qué representa el punto donde la recta corta al eje vertical?"
        ans = f"El costo fijo, que se paga aunque no se use ninguna unidad: {icept} mil pesos"
        alts = [f"El costo de cada unidad adicional usada: {icept} mil pesos", f"El costo total al usar 10 unidades: {icept + slope * 10} mil pesos", f"La cantidad de unidades cuyo costo es cero: {icept} unidades", f"El costo promedio por unidad usada: {slope} mil pesos"]
    return make(stem, fig, ans, alts, Q_REP, "La pendiente es la tasa de cambio (costo por unidad) y el intercepto vertical es el valor inicial (costo fijo).")


def t_compare(r, l):
    ms = r.sample([-3, -2, -1, 1, 2, 3], 3)
    ns = [rr(r, -3, 3) for _ in range(3)]
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    cols = [ACC, NAVY, "#166534"]
    for i, (m, n) in enumerate(zip(ms, ns)):
        p.curve(lambda x, m=m, n=n: m * x + n, -6, 6, cols[i], 4.5)
    body = ""
    fig = p.svg("Tres rectas")
    labs = ""
    for i, (m, n) in enumerate(zip(ms, ns)):
        y = m * 5 + n
        if abs(y) > 5.5:
            xx = (5.5 if y > 0 else -5.5 - n) / m if False else (5.5 - n) / m if y > 0 else (-5.5 - n) / m
            xp, yp = xx, m * xx + n
        else:
            xp, yp = 5, y
        labs += tag(p.X(xp) - 10, min(max(p.Y(yp) - 18, 16), 284), f"L{i + 1}", 15)
    fig = fig.replace("</svg>", labs + "</svg>")
    kind = r.choice(["max", "neg"])
    names = ["L1", "L2", "L3"]
    if kind == "max":
        idx = max(range(3), key=lambda i: ms[i])
        stem = "El gráfico muestra tres rectas (L1 roja, L2 azul, L3 verde). ¿Cuál de ellas tiene la mayor pendiente?"
    else:
        negs = [i for i in range(3) if ms[i] < 0]
        if len(negs) != 1:
            raise Reject
        idx = negs[0]
        stem = "El gráfico muestra tres rectas (L1 roja, L2 azul, L3 verde). ¿Cuál de ellas tiene pendiente negativa (es decreciente)?"
    ans = names[idx]
    al = [n for n in names if n != ans] + ["Las tres tienen la misma pendiente", "Ninguna de las tres"]
    return make(stem, fig, ans, al[:4], Q_REP, "Una recta creciente tiene pendiente positiva; mientras más inclinada, mayor es su valor absoluto.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 5), r.randint(1, 6)
    if k == 0:
        return [f"A(1, 2) y B({1 + a}, {2 + b * a})", f"m = ({1 + a} − 1) / ({2 + b * a} − 2) = {a}/{b * a}"], "Invirtió el cociente: la pendiente es la variación de y dividida por la variación de x, no al revés", \
            ["Restó las coordenadas en distinto orden en el numerador y el denominador", "Sumó las coordenadas en lugar de restarlas antes de dividir el resultado", "Dividió la variación de x por la variación de y y luego cambió el signo", "Usó las coordenadas de un solo punto para calcular el cociente pedido"]
    if k == 1:
        return [f"y = −{a}x + {b}", "La recta es creciente porque el coeficiente de x es distinto de cero"], "Una recta con pendiente negativa es decreciente: el signo de la pendiente indica si crece o decrece", \
            ["El signo de la pendiente no tiene relación con el crecimiento de la recta", "La recta es creciente porque el término independiente es positivo en la ecuación", "Toda recta con pendiente distinta de cero es creciente sin importar su signo", "La recta es horizontal porque el coeficiente de x es un número entero"]
    if k == 2:
        return [f"y = {a}x + {b}", f"«La recta corta al eje X en {b}»"], f"El punto (0, {b}) es el corte con el eje Y: el corte con el eje X se obtiene haciendo y = 0", \
            [f"El corte con el eje X es {a}, porque es el coeficiente de x en la ecuación", f"La recta corta al eje X en −{b}, porque se cambia el signo del término independiente", "La recta no corta al eje X porque tiene pendiente positiva en toda su extensión", f"El corte con el eje X es {a * b}, porque se multiplica la pendiente por n"]
    return [f"y = {a}x + {b} e y = {a}x − {b}", "Las rectas se cortan en un punto porque son distintas"], "Tienen la misma pendiente: son paralelas, no se cortan, aunque sus interceptos sean distintos", \
        ["Tienen pendientes opuestas, por lo que son perpendiculares entre sí siempre", "Tienen el mismo intercepto, por lo que se cortan en el eje vertical siempre", "Tienen distinta pendiente porque sus términos independientes son distintos entre sí", "Son la misma recta porque tienen el mismo coeficiente de x"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_statement(r, l):
    m = rr(r, -5, 5)
    n = rr(r, -6, 6)
    fig = card(["Recta:", M(eqline(m, n))], 130, 24)
    trend = "creciente" if m > 0 else "decreciente"
    ans = f"Es {trend} y corta al eje Y en el punto (0, {n})".replace("-", "−")
    opp = "decreciente" if m > 0 else "creciente"
    alts = [f"Es {opp} y corta al eje Y en el punto (0, {n})", f"Es {trend} y corta al eje Y en el punto ({n}, 0)", f"Es {trend} y corta al eje X en el punto ({n}, 0)", f"Es {opp} y corta al eje Y en el punto (0, {-n})"]
    alts = [a.replace("-", "−") for a in alts]
    if n == 0:
        raise Reject
    return make("¿Cuál de las siguientes afirmaciones sobre la recta de la figura es verdadera?", fig, ans, alts, Q_ARG, f"La pendiente {m} es {'positiva' if m > 0 else 'negativa'} y el intercepto con el eje Y es {n}.".replace("-", "−"))


TRUE = ["Dos rectas con la misma pendiente y distinto intercepto son paralelas", "Una recta con pendiente positiva es creciente", "En y = mx + n, n es la ordenada del punto donde la recta corta al eje Y",
        "Una función lineal y = mx pasa por el origen", "La pendiente de una recta horizontal es cero", "La pendiente mide cuánto cambia y por cada unidad que aumenta x"]
FALSE = ["Una recta con pendiente negativa es creciente", "En y = mx + n, n es la pendiente de la recta", "Una función afín y = mx + n con n distinto de cero pasa por el origen",
         "La pendiente de una recta horizontal es uno", "Dos rectas con la misma pendiente siempre se cortan en un punto", "La pendiente mide el valor de y cuando x vale cero"]


def _fig(r):
    return card(["Recta: y = mx + n", "m: pendiente · n: intercepto con el eje Y"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones lineales y afines es verdadera?", "Sobre pendiente e intercepto, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el significado de m y n en y = mx + n.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones lineales y afines es falsa?", "Sobre pendiente e intercepto, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el significado de m y n.")


BY_SKILL = {
    Q_RES: [t_slope, t_intercepts, t_line_eq],
    Q_MOD: [t_two_data, t_candle],
    Q_REP: [t_read_line, t_interpret, t_compare],
    Q_ARG: [t_error, t_statement, t_true, t_false],
}
