"""Clase 19 (M1) · Sistemas de ecuaciones lineales 2x2 I: resolución y elección de método."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
import viz


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def lin2(a, b, vx="x", vy="y"):
    s = ""
    if a:
        s += co(a, vx, True)
    if b:
        s += co(b, vy, not a)
    return s or "0"


def eqn(a, b, c, vx="x", vy="y"):
    return f"{lin2(a, b, vx, vy)} = {str(c).replace('-', '−')}"


def pair(x, y):
    return f"({x}, {y})".replace("-", "−")


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        if a not in seen:
            seen.add(a); out.append(a)
    return out


def gen_sys(r, l):
    """Sistema con solución entera; devuelve (eqs, x0, y0)."""
    for _ in range(300):
        x0, y0 = rr(r, -6, 8), rr(r, -6, 8)
        if l == 0:
            m, n = rr(r, -3, 4), rr(r, -6, 6)
            d, e = rr(r, 1, 3), rr(r, 1, 3)
            y1 = m * x0 + n
            if y1 != y0:
                y0 = y1
            if abs(y0) > 12:
                continue
            f = d * x0 + e * y0
            eqs = [(f"y = {co(m, 'x', True)}{co(n, '', False)}", None), (eqn(d, e, f), None)]
            return eqs, x0, y0, "sub"
        if l == 1:
            a, b = rr(r, 1, 5), rr(r, -5, 5)
            d, e = rr(r, 1, 5), -b
            if a * e - b * d == 0:
                continue
            eqs = [(eqn(a, b, a * x0 + b * y0), None), (eqn(d, e, d * x0 + e * y0), None)]
            return eqs, x0, y0, "red"
        a, b, d, e = rr(r, -5, 5), rr(r, -5, 5), rr(r, -5, 5), rr(r, -5, 5)
        if a * e - b * d == 0 or abs(a) == 1 and abs(e) == 1 and False:
            continue
        eqs = [(eqn(a, b, a * x0 + b * y0), None), (eqn(d, e, d * x0 + e * y0), None)]
        return eqs, x0, y0, "gen"
    raise Reject


# ---------------------------------------------------------------- Resolver problemas
def t_solve(r, l):
    eqs, x0, y0, meth = gen_sys(r, l)
    fig = card(["Resuelve el sistema:"] + [e for e, _ in eqs], 60 + 44 * (len(eqs) + 1), 22)
    ans = pair(x0, y0)
    alts = [pair(y0, x0), pair(-x0, y0), pair(x0, -y0), pair(x0 + 1, y0), pair(x0, y0 + 1), pair(-x0, -y0)]
    al = [a for a in dict.fromkeys(alts) if a != ans]
    return make("¿Cuál es la solución (x, y) del sistema de ecuaciones de la figura?", fig, ans, al[:4], Q_RES, f"Se resuelve por {'sustitución' if meth == 'sub' else 'reducción'}: x = {x0}, y = {y0}.".replace("-", "−"))


def t_value_asked(r, l):
    eqs, x0, y0, meth = gen_sys(r, max(l, 1))
    kind = r.choice(["sum", "diff", "prod"])
    if kind == "sum":
        val, txt = x0 + y0, "x + y"
        alts = [x0 - y0, x0 * y0, x0, y0, val + 1]
    elif kind == "diff":
        val, txt = x0 - y0, "x − y"
        alts = [x0 + y0, y0 - x0, x0 * y0, x0, val + 1]
    else:
        val, txt = x0 * y0, "x · y"
        alts = [x0 + y0, x0 - y0, x0, y0, val + 2]
    fig = card(["Sistema:"] + [e for e, _ in eqs], 60 + 44 * (len(eqs) + 1), 22)
    ans = str(val).replace("-", "−")
    al = [str(a).replace("-", "−") for a in dict.fromkeys(alts) if a != val]
    return make(f"Si (x, y) es la solución del sistema de la figura, ¿cuál es el valor de {txt}?", fig, ans, al[:4], Q_RES, f"x = {x0}, y = {y0}, luego {txt} = {ans}.".replace("-", "−"))


# ---------------------------------------------------------------- Modelar
def t_prices(r, l):
    p, q = r.randint(2, 9) * 100, r.randint(2, 9) * 100
    if p == q:
        raise Reject
    a1, b1 = r.randint(1, 4), r.randint(1, 4)
    a2, b2 = r.randint(1, 4), r.randint(1, 4)
    if a1 * b2 - a2 * b1 == 0:
        raise Reject
    T1, T2 = a1 * p + b1 * q, a2 * p + b2 * q
    it = r.choice([("cuadernos", "lápices"), ("bebidas", "sándwiches"), ("entradas de adulto", "entradas de niño")])
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    rows = [["Compra 1", str(a1), str(b1), f(T1)], ["Compra 2", str(a2), str(b2), f(T2)]]
    fig = viz.table_fig(["", it[0].split()[0].capitalize(), it[1].split()[0].capitalize(), "Total"], rows)
    ask = r.choice([0, 1])
    stem = f"La tabla muestra dos compras de {it[0]} y {it[1]} (cada tipo tiene un precio unitario fijo). ¿Cuánto cuesta {'un(a) ' + it[ask][:-1] if not it[ask].endswith('ño') else 'una ' + it[ask]}?".replace("un(a) ", "un(a) ") if False else f"La tabla muestra dos compras de {it[0]} y {it[1]}; cada tipo tiene un precio unitario fijo. ¿Cuál es el precio de un elemento del segundo tipo ({it[1]})?" if ask else f"La tabla muestra dos compras de {it[0]} y {it[1]}; cada tipo tiene un precio unitario fijo. ¿Cuál es el precio de un elemento del primer tipo ({it[0]})?"
    val = q if ask else p
    ans = f(val)
    alts = [p if ask else q, val + 100, val - 100 if val > 100 else val + 200, F(T1, a1 + b1), val * 2]
    al = [f(int(a)) for a in dict.fromkeys(alts) if F(a).denominator == 1 and a > 0 and a != val]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Sistema: {a1}a + {b1}b = {T1}, {a2}a + {b2}b = {T2}; se resuelve por reducción.")


def t_pose(r, l):
    p, q = r.randint(2, 9) * 100, r.randint(2, 9) * 100
    a1, b1, a2, b2 = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    if a1 * b2 - a2 * b1 == 0 or p == q:
        raise Reject
    T1, T2 = a1 * p + b1 * q, a2 * p + b2 * q
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    stem = f"{a1} cuadernos y {b1} lápices cuestan {f(T1)}, y {a2} cuadernos y {b2} lápices cuestan {f(T2)}. Si c es el precio de un cuaderno y l el de un lápiz, ¿qué sistema representa la situación?"
    ans = f"{a1}c + {b1}l = {T1} ; {a2}c + {b2}l = {T2}"
    alts = [f"{a1}c + {b1}l = {T2} ; {a2}c + {b2}l = {T1}", f"{b1}c + {a1}l = {T1} ; {b2}c + {a2}l = {T2}", f"{a1}c + {b1}l = {T1} ; {a2}c − {b2}l = {T2}", f"{a1 + b1}cl = {T1} ; {a2 + b2}cl = {T2}"]
    fig = card([f"{a1} cuadernos + {b1} lápices → {f(T1)}", f"{a2} cuadernos + {b2} lápices → {f(T2)}"], 130, 18)
    return make(stem, fig, ans, alts, Q_MOD, "Cada compra da una ecuación: cantidad de cada producto por su precio, igualada al total.")


def t_people(r, l):
    A = r.randint(20, 80)
    B = r.randint(20, 80)
    pa, pb = r.choice([(3000, 1500), (5000, 2000), (4000, 2500), (6000, 3000)])
    N = A + B
    T = pa * A + pb * B
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    fig = card([f"Entradas de adulto: {f(pa)}", f"Entradas de niño: {f(pb)}", f"Personas: {N}  ·  Recaudación: {f(T)}"], 170, 18)
    stem = f"En una función asistieron {N} personas entre adultos y niños. Las entradas de adulto cuestan {f(pa)} y las de niño {f(pb)}, y se recaudaron {f(T)}. ¿Cuántos adultos asistieron?"
    ans = str(A)
    alts = [B, N - A - 1, F(N, 2), A + 10, F(T, pa)]
    al = [str(int(a)) for a in dict.fromkeys(alts) if F(a).denominator == 1 and a > 0 and a != A]
    return make(stem, fig, ans, al[:4], Q_MOD, f"a + n = {N}; {pa}a + {pb}n = {T} ⟹ a = {A}.")


# ---------------------------------------------------------------- Representar
def t_graph(r, l):
    x0, y0 = rr(r, -4, 5), rr(r, -4, 5)
    m1, m2 = r.sample([-2, -1, 1, 2, 3], 2)
    n1, n2 = y0 - m1 * x0, y0 - m2 * x0
    if max(abs(n1), abs(n2)) > 6:
        raise Reject
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    p.curve(lambda t: m1 * t + n1, -6, 6, ACC, 4.5)
    p.curve(lambda t: m2 * t + n2, -6, 6, NAVY, 4.5)
    fig = p.svg("Gráfico de dos rectas")
    ans = pair(x0, y0)
    alts = [pair(y0, x0), pair(-x0, y0), pair(x0, -y0), pair(0, n1), pair(-n2 // m2 if m2 and n2 % m2 == 0 else 1, 0)]
    al = [a for a in dict.fromkeys(alts) if a != ans]
    return make("Las dos rectas del gráfico representan las ecuaciones de un sistema. ¿Cuál es la solución (x, y) del sistema?", fig, ans, al[:4], Q_REP, "La solución es el punto donde se cruzan las dos rectas.")


def t_graph_to_sys(r, l):
    x0, y0 = rr(r, -3, 4), rr(r, -3, 4)
    m1, m2 = r.sample([-2, -1, 1, 2, 3], 2)
    n1, n2 = y0 - m1 * x0, y0 - m2 * x0
    if max(abs(n1), abs(n2)) > 6:
        raise Reject
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    p.curve(lambda t: m1 * t + n1, -6, 6, ACC, 4.5)
    p.curve(lambda t: m2 * t + n2, -6, 6, NAVY, 4.5)
    fig = p.svg("Gráfico de dos rectas")
    e = lambda m, n: "y = " + (co(m, "x", True) + co(n, "", False))
    ans = f"{e(m1, n1)} ; {e(m2, n2)}"
    alts = [f"{e(-m1, n1)} ; {e(m2, n2)}", f"{e(m1, -n1)} ; {e(m2, -n2)}", f"{e(m1, n2)} ; {e(m2, n1)}", f"{e(m2, n1)} ; {e(m1, n2)}"]
    al = [a for a in dict.fromkeys(alts) if a != ans]
    if len(al) < 4:
        raise Reject
    return make("¿Qué sistema de ecuaciones está representado por las dos rectas del gráfico (la roja y la azul, en ese orden)?", fig, ans, al[:4], Q_REP, "Se lee en cada recta el corte con el eje Y (n) y la pendiente (m).")


def t_table_equal(r, l):
    a, b = rr(r, 1, 4), rr(r, -4, 5)
    c, d = rr(r, 1, 4), rr(r, -4, 5)
    if a == c:
        raise Reject
    x0 = F(d - b, a - c)
    if x0.denominator != 1 or not (0 <= x0 <= 5):
        raise Reject
    xs = [0, 1, 2, 3, 4, 5]
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [[f"y = {co(a, 'x', True)}{co(b, '', False)}".replace("-", "−")] + [str(a * x + b).replace("-", "−") for x in xs], [f"y = {co(c, 'x', True)}{co(d, '', False)}".replace("-", "−")] + [str(c * x + d).replace("-", "−") for x in xs]]) if False else viz.table_fig(["x"] + [str(x) for x in xs], [["Recta 1"] + [str(a * x + b).replace("-", "−") for x in xs], ["Recta 2"] + [str(c * x + d).replace("-", "−") for x in xs]])
    y0 = a * int(x0) + b
    stem = "La tabla muestra los valores de y en dos rectas para distintos valores de x. ¿Cuál es la solución (x, y) del sistema formado por ambas rectas?"
    ans = pair(int(x0), y0)
    alts = [pair(y0, int(x0)), pair(int(x0) + 1, y0), pair(int(x0), y0 + 1), pair(int(x0) - 1, y0), pair(0, b)]
    al = [a_ for a_ in dict.fromkeys(alts) if a_ != ans]
    return make(stem, fig, ans, al[:4], Q_REP, "Se busca el valor de x donde ambas filas entregan el mismo valor de y.")


# ---------------------------------------------------------------- Argumentar
def t_check(r, l):
    x0, y0 = rr(r, -5, 7), rr(r, -5, 7)
    a, b, d, e = rr(r, 1, 4), rr(r, -4, 4), rr(r, 1, 4), rr(r, -4, 4)
    if a * e - b * d == 0:
        raise Reject
    c = a * x0 + b * y0
    f = d * x0 + e * y0
    kind = r.choice(["both", "first", "second", "none"])
    if kind == "both":
        tx, ty = x0, y0
    elif kind == "first":
        tx, ty = x0 + r.choice([1, 2]), y0
        while a * tx + b * ty != c:
            tx += 1
            y_new = F(c - a * tx, b) if b else None
            if b and y_new is not None and y_new.denominator == 1:
                ty = int(y_new)
                break
            if tx > x0 + 20:
                raise Reject
        if d * tx + e * ty == f:
            raise Reject
    elif kind == "second":
        tx, ty = x0 + r.choice([1, 2]), y0
        while d * tx + e * ty != f:
            tx += 1
            y_new = F(f - d * tx, e) if e else None
            if e and y_new is not None and y_new.denominator == 1:
                ty = int(y_new)
                break
            if tx > x0 + 20:
                raise Reject
        if a * tx + b * ty == c:
            raise Reject
    else:
        tx, ty = x0 + r.choice([1, 2, -1]), y0 + r.choice([1, -1, 2])
    ok1, ok2 = a * tx + b * ty == c, d * tx + e * ty == f
    fig = card([eqn(a, b, c), eqn(d, e, f), f"¿Es (x, y) = {pair(tx, ty)} solución?"], 190, 21)
    ans = "Sí, el par cumple ambas ecuaciones" if ok1 and ok2 else "No, el par cumple solo la primera ecuación" if ok1 else "No, el par cumple solo la segunda ecuación" if ok2 else "No, el par no cumple ninguna de las dos ecuaciones"
    opts = ["Sí, el par cumple ambas ecuaciones", "No, el par cumple solo la primera ecuación", "No, el par cumple solo la segunda ecuación", "No, el par no cumple ninguna de las dos ecuaciones", "No se puede saber sin resolver el sistema completo"]
    al = [o for o in opts if o != ans]
    return make("Para el sistema de la figura, ¿qué se puede afirmar sobre el par (x, y) indicado?", fig, ans, al, Q_ARG, "Un par es solución solo si cumple simultáneamente ambas ecuaciones.")


def t_method(r, l):
    kind = r.choice(["red", "sub", "eq"])
    a, b = rr(r, 2, 6), rr(r, 2, 6)
    if kind == "red":
        eqs = [eqn(a, b, a * 3 + b * 2), eqn(rr(r, 1, 5), -b, 0 + 3 * 1 - 2 * b)]
        eqs = [f"{a}x + {b}y = {a * 3 + b * 2}", f"{a + 1}x − {b}y = {(a + 1) * 3 - b * 2}"]
        ans = "Reducción, porque los coeficientes de y son opuestos y se anulan al sumar"
    elif kind == "sub":
        m = rr(r, 2, 5)
        eqs = [f"y = {m}x", f"{a}x + {b}y = {a * 2 + b * 2 * m}"]
        ans = "Sustitución, porque una incógnita ya está despejada en la primera ecuación"
    else:
        m, n = rr(r, 2, 5), rr(r, 1, 6)
        eqs = [f"y = {m}x + {n}", f"y = {m + 1}x − {n}"]
        ans = "Igualación, porque ambas ecuaciones tienen la misma incógnita despejada"
    fig = card(["Sistema:"] + eqs, 60 + 44 * (len(eqs) + 1), 22)
    opts = ["Reducción, porque los coeficientes de y son opuestos y se anulan al sumar", "Sustitución, porque una incógnita ya está despejada en la primera ecuación", "Igualación, porque ambas ecuaciones tienen la misma incógnita despejada",
            "Reducción, porque las dos ecuaciones tienen el mismo término independiente", "Sustitución, porque hay que despejar una incógnita antes de cualquier otro paso", "Igualación, porque los coeficientes de x son opuestos en ambas ecuaciones"]
    al = [o for o in opts if o != ans][:4]
    return make("¿Qué método resulta más rápido para resolver el sistema de la figura y por qué?", fig, ans, al, Q_ARG, "Se elige el método según cómo están escritas las ecuaciones.")


def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 6), r.randint(2, 6)
    if k == 0:
        return ["x + y = 8", "x − y = 2", "Sumando: 2x = 6 → x = 3;  y = 8 + 3 = 11"], "Sustituyó mal: debió reemplazar x = 3 en la primera ecuación y obtener y = 5", \
            ["Sumó las ecuaciones pero no dividió el resultado por el coeficiente de x", "Restó las ecuaciones en lugar de sumarlas y por eso obtuvo un valor equivocado", "Despejó y de la segunda ecuación pero cambió el signo del término x", "Comprobó el valor de x pero no lo reemplazó en ninguna de las ecuaciones"]
    if k == 1:
        return ["2x + y = 7", "x + y = 4", "Restando: 2x − x + y − y = 7 + 4 → x = 11"], "Al restar las ecuaciones sumó los lados derechos: debió calcular 7 − 4 = 3", \
            ["Sumó las ecuaciones en lugar de restarlas antes de eliminar la incógnita", "Eliminó la incógnita x en lugar de la incógnita y en el sistema completo", "Multiplicó una de las ecuaciones por dos antes de operar con la otra", "Despejó y de la primera ecuación y la reemplazó en la misma ecuación"]
    if k == 2:
        return ["y = 2x + 1", "3x + y = 11", "Sustituyendo: 3x + 2x + 1 = 11 → 5x = 11 + 1 → x = 12/5"], "Al pasar el 1 al otro lado no cambió su signo: 5x = 11 − 1 = 10, luego x = 2", \
            ["Sustituyó y por 2x pero olvidó el término independiente de la primera ecuación", "Reemplazó y en la primera ecuación en vez de hacerlo en la segunda ecuación", "Multiplicó la segunda ecuación por 2 antes de reemplazar el valor de y", "Sumó 3x y 2x y obtuvo un coeficiente que no corresponde a la suma"]
    return ["x + 2y = 5", "3x − 2y = 3", "Sumando: 4x = 8 → x = 2;  luego 2 + 2y = 5 → y = 5/2 − 2"], "Despejó mal y: de 2y = 3 se obtiene y = 3/2, no se resta 2 después de dividir", \
        ["Sumó las ecuaciones cuando debió restarlas para eliminar la incógnita y", "Dividió por 4 el lado derecho pero no el lado izquierdo de la ecuación", "Reemplazó el valor de x en la segunda ecuación y no en la primera", "Cambió el signo de y al despejarla y después comprobó con el signo cambiado"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 40 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["La solución de un sistema es el par de valores que cumple ambas ecuaciones a la vez", "Al sumar dos ecuaciones se suman los lados izquierdos y los lados derechos",
        "La solución de un sistema de dos rectas que se cruzan es su punto de intersección", "Multiplicar una ecuación por un número distinto de cero no cambia su solución",
        "Si una incógnita ya está despejada, conviene sustituirla en la otra ecuación", "Los métodos de sustitución y reducción entregan la misma solución"]
FALSE = ["Un par que cumple solo una ecuación es solución del sistema", "Al sumar dos ecuaciones solo se suman los lados izquierdos", "Dos rectas distintas siempre se cortan en exactamente un punto",
         "Multiplicar una ecuación por cero mantiene la solución del sistema", "Los métodos de sustitución y reducción pueden entregar soluciones distintas", "La solución de un sistema es el punto donde una recta corta al eje Y"]


def _fig(r):
    return card(["Sistemas de ecuaciones 2x2", "Sustitución · Igualación · Reducción"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre sistemas de ecuaciones es verdadera?", "Sobre resolver sistemas de dos ecuaciones, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la definición de solución de un sistema.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre sistemas de ecuaciones es falsa?", "Sobre resolver sistemas de dos ecuaciones, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la definición de solución de un sistema.")


BY_SKILL = {
    Q_RES: [t_solve, t_value_asked],
    Q_MOD: [t_prices, t_pose, t_people],
    Q_REP: [t_graph, t_graph_to_sys, t_table_equal],
    Q_ARG: [t_check, t_method, t_error, t_true, t_false],
}
