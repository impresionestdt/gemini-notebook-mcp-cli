"""Clase 17 (M1) · Ecuaciones de primer grado I: resolución y comprobación."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
from figs import numline
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


def eq(a, b, c, d, v="x"):
    """a v + b = c v + d"""
    return f"{lin(a, b, v)} = {lin(c, d, v)}"


# ---------------------------------------------------------------- Resolver problemas
def t_solve(r, l):
    x = F(rr(r, -9, 12))
    v = r.choice("xyzt") if l else "x"
    if l == 0:
        a, b = rr(r, -6, 7), rr(r, -12, 12)
        if abs(a) == 1:
            raise Reject
        c = a * x + b
        disp = f"{lin(a, b, v)} = {int(c)}".replace("-", "−")
        alts = [F(int(c) + b, a), F(int(c) - b, a) * -1, F(int(c) - b), F(int(c) + b) * -1 / a if True else 0, x + 1]
        step = f"{a}{v} = {int(c)} {'−' if b > 0 else '+'} {abs(b)} = {int(c - b)}"
    elif l == 1:
        a, c = rr(r, -6, 7), rr(r, -6, 7)
        if a == c:
            raise Reject
        b = rr(r, -10, 10)
        d = a * x + b - c * x
        disp = eq(a, b, c, int(d), v)
        alts = [F(int(d) + b, a - c), F(int(d) - b, a + c) if a + c else None, F(int(d) - b, c - a) * -1 if False else F(int(d) + b, c - a), F(b - int(d), a - c) * -1 if False else F(int(d), a - c), x + 1]
        step = f"({a - c}){v} = {int(d - b)}"
    else:
        k = r.randint(2, 5)
        a, b, c = rr(r, 1, 5), rr(r, -8, 8), rr(r, -6, 6)
        d = k * (a * x + b) - c
        disp = f"{k}({lin(a, b, v)}) − {abs(c)} = {int(d)}" if c > 0 else f"{k}({lin(a, b, v)}) + {abs(c)} = {int(d)}"
        val = k * (a * x + b) - c
        if val != d:
            raise Reject
        disp = disp.replace("-", "−")
        alts = [F(int(d) + c - k * b, a), F(int(d) + c, k * a) - b, F(int(d) - c - k * b, k * a), F(int(d) + c - b, k * a), x + 2]
        step = ""
    if abs(x) > 40:
        raise Reject
    fig = card(["Resuelve la ecuación:", disp], 130, 22)
    ans = fs(x)
    return make("¿Cuál es la solución de la ecuación de la figura?", fig, ans, pick4(ans, uq(ans, alts + [-x, x * 2])), Q_RES, f"Se aíslan los términos con {v} y se divide por su coeficiente: {v} = {ans}.")


def t_fraction_eq(r, l):
    x = F(rr(r, -6, 12))
    d1, d2 = r.choice([(2, 3), (3, 4), (2, 5), (3, 6), (4, 6), (2, 4)])
    kind = r.choice(["sum", "frac"] if l else ["frac"])
    if kind == "sum":
        c = x / d1 + x / d2
        if c.denominator != 1:
            raise Reject
        disp = f"x/{d1} + x/{d2} = {int(c)}"
        alts = [F(int(c) * (d1 + d2)), F(int(c), d1 + d2), F(int(c) * d1 * d2, d1 + d2) + 1, F(int(c)) - d1 - d2, x + d1]
    else:
        b = rr(r, -6, 8)
        c = (x + b) / d1
        if c.denominator != 1:
            raise Reject
        disp = f"(x + {b})/{d1} = {int(c)}".replace("+ -", "− ")
        alts = [F(int(c)) - b, F(int(c) * d1) + b, F(int(c)) + b, F(int(c), d1) - b, x + 1]
    fig = card(["Resuelve la ecuación:", disp.replace("-", "−")], 130, 22)
    ans = fs(x)
    return make("¿Cuál es la solución de la ecuación de la figura?", fig, ans, pick4(ans, uq(ans, alts + [-x])), Q_RES, f"Se multiplica por el denominador común y luego se despeja x: x = {ans}.")


def t_check(r, l):
    x = rr(r, -6, 9)
    a, b = rr(r, 2, 6), rr(r, -8, 9)
    c = a * x + b
    if l >= 1:
        k = rr(r, 2, 4)
        d = rr(r, 1, 5)
        c2 = k * (x + d) - a
        disp = f"{k}(x + {d}) − {a} = {c2}"
        alts = [x + 1, x - 1, -x, x + d, x * 2]
        ex = f"Se reemplaza: {k}({x} + {d}) − {a} = {k * (x + d) - a} ✓."
    else:
        disp = f"{lin(a, b)} = {c}"
        alts = [x + 1, x - 1, -x, x + 2, x * 2]
        ex = f"Reemplazando x = {x}: {a}·{x if x >= 0 else '(' + str(x) + ')'} {'+' if b >= 0 else '−'} {abs(b)} = {c} ✓."
    fig = card(["Ecuación:", disp.replace("-", "−")], 130, 22)
    ans = fs(F(x))
    return make("¿Cuál de los siguientes valores de x es solución de la ecuación de la figura?", fig, ans, pick4(ans, uq(ans, alts)), Q_RES, ex.replace("-", "−"))


# ---------------------------------------------------------------- Modelar
def t_balance(r, l):
    x = r.randint(2, 12)
    a, c = rr(r, 1, 5), rr(r, 1, 4)
    if a <= c:
        a, c = c + 1, a
    b = r.randint(1, 9)
    d = (a - c) * x + b
    body = L(280, 190, 280, 110, INK, 5) + P([(250, 200), (310, 200), (280, 170)], NAVY, NAVY, 2)
    body += L(120, 110, 440, 110, INK, 5) + R(70, 100, 160, 30, FILL, NAVY, 3) + R(330, 100, 160, 30, FILL2, NAVY, 3)
    body += tag(150, 80, lin(a, b), 19) + tag(410, 80, lin(c, d), 19)
    fig = wrap(560, 220, body, "Balanza en equilibrio")
    stem = "La balanza de la figura está en equilibrio y las expresiones indican el peso de cada platillo en gramos. ¿Cuánto vale x?"
    ans = str(x)
    alts = [F(d + b, a + c), F(d - b, a + c), F(d + b, a - c), d - b, x + 1, x * 2]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"{lin(a, b)} = {lin(c, d)} ⟹ {a - c}x = {d - b} ⟹ x = {x}.")


def t_perim_eq(r, l):
    x = r.randint(2, 15)
    a = r.randint(1, 6)
    b = r.randint(1, 8)
    P_ = 2 * ((x + a) + (2 * x - b))
    body = R(120, 40, 320, 120, FILL, NAVY, 3) + tag(280, 178, f"x + {a}", 18) + tag(90, 100, f"2x − {b}", 18)
    fig = wrap(560, 210, body, "Rectángulo de lados x + a y 2x − b")
    stem = f"Un rectángulo tiene lados de (x + {a}) cm y (2x − {b}) cm. Si su perímetro es {P_} cm, ¿cuánto vale x?"
    ans = str(x)
    alts = [F(P_ - a + b, 6) if True else 0, F(P_, 6), F(P_ // 2 - a + b, 3), F(P_ - 2 * a + 2 * b, 3), x + 2, x - 1]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"Perímetro = 2[(x + {a}) + (2x − {b})] = 6x + {2 * a - 2 * b} = {P_}, luego x = {x}.".replace("+ -", "− "))


def t_plan(r, l):
    x = r.randint(3, 20)
    fixed, per = r.choice([(4000, 500), (5000, 800), (3000, 600), (2000, 300)]), None
    a, b = fixed
    total = a + b * x
    ctx = r.choice([("Un plan de internet cobra", "de cargo fijo más", "por cada GB adicional", "GB"), ("Un taxi cobra", "de bajada más", "por kilómetro", "km"), ("Un gimnasio cobra", "de matrícula más", "por cada clase", "clases")])
    f = lambda z: "$" + f"{z:,}".replace(",", ".")
    fig = card([f"{ctx[0]} {f(a)} {ctx[1]}", f"{f(b)} {ctx[2]}", f"Total pagado: {f(total)}"], 170, 19)
    stem = f"{ctx[0]} {f(a)} {ctx[1]} {f(b)} {ctx[2]}. Si se pagó un total de {f(total)}, ¿cuántos {ctx[3]} se usaron?"
    ans = str(x)
    alts = [F(total, b), F(total + a, b), total - a, F(total - a, a), x + 1, x * 2]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"{a} + {b}x = {total} ⟹ x = {x}.")


# ---------------------------------------------------------------- Representar
def t_numline_sol(r, l):
    x = rr(r, -8, 9)
    a, b = rr(r, 2, 5), rr(r, -6, 8)
    c = a * x + b
    pts = [x]
    while len(pts) < 5:
        p = rr(r, -9, 9)
        if all(abs(p - q) >= 2 for q in pts):
            pts.append(p)
    r.shuffle(pts)
    lab = dict(zip("ABCDE", pts))
    fig = numline(-10, 10, lab)
    ans = [k for k, v in lab.items() if v == x][0]
    fig_note = f"{lin(a, b)} = {c}".replace("-", "−")
    stem = f"Los puntos A, B, C, D y E de la recta numérica representan posibles valores de x. ¿Cuál de ellos es solución de la ecuación {fig_note}?"
    return make(stem, fig, ans, [k for k in "ABCDE" if k != ans], Q_REP, f"La solución es x = {x}, que corresponde al punto {ans}.")


def t_table_sol(r, l):
    a, b = rr(r, 1, 5), rr(r, -6, 8)
    x = r.randint(1, 5)
    c = a * x + b
    xs = [0, 1, 2, 3, 4, 5, 6]
    fig = viz.table_fig(["x"] + [str(t) for t in xs], [["y"] + [str(a * t + b).replace("-", "−") for t in xs]])
    stem = f"La tabla muestra los valores de y = {lin(a, b)} para distintos valores de x. Según la tabla, ¿cuál es la solución de la ecuación {lin(a, b)} = {c}?".replace("-", "−")
    ans = str(x)
    alts = [c, x + 1, x - 1 if x > 1 else x + 2, a * x, b]
    al = [str(v) for v in dict.fromkeys(alts) if str(v) != ans and str(v).lstrip("-").isdigit()]
    al = [x_ for x_ in al if x_ != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"Se busca en la fila de y el valor {c}: corresponde a x = {x}.")


def t_eq_from_balance(r, l):
    a, b, c, d = rr(r, 2, 6), r.randint(1, 9), rr(r, 1, 4), r.randint(5, 20)
    body = L(280, 190, 280, 110, INK, 5) + P([(250, 200), (310, 200), (280, 170)], NAVY, NAVY, 2) + L(120, 110, 440, 110, INK, 5)
    body += R(70, 100, 160, 30, FILL, NAVY, 3) + R(330, 100, 160, 30, FILL2, NAVY, 3)
    bol = lambda n: "1 bolsa" if n == 1 else f"{n} bolsas"
    body += tag(150, 80, f"{bol(a)} + {b} g", 16) + tag(410, 80, f"{bol(c)} + {d} g", 16)
    fig = wrap(560, 220, body, "Balanza con bolsas iguales de x gramos")
    cx, ax = ("x" if c == 1 else f"{c}x"), f"{a}x"
    dx = "x" if d == 1 else f"{d}x"
    ans = f"{ax} + {b} = {cx} + {d}"
    alts = [f"{ax} + {b} = {c} + {dx}", f"{a} + {b}x = {c} + {dx}", f"{ax} + {b} + {cx} = {d}", f"{a + c}x = {b + d}"]
    return make("La balanza está en equilibrio y cada bolsa pesa x gramos. ¿Qué ecuación representa la situación?", fig, ans, alts, Q_REP, "Cada platillo pesa (bolsas·x + gramos sueltos); ambos pesos son iguales.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b, c = r.randint(2, 6), r.randint(2, 9), r.randint(10, 30)
    if k == 0:
        return [f"{a}x − {b} = {c}", f"{a}x = {c} − {b}"], "Al pasar el término al otro lado no cambió su signo: −b pasa sumando", \
            ["Restó dos veces el mismo término a ambos lados de la ecuación original", "Dividió por el coeficiente de x antes de pasar el término numérico", "Cambió el signo del lado derecho pero no el del término que se movió", "Multiplicó ambos lados por el coeficiente en lugar de dividirlos entre él"]
    if k == 1:
        return [f"{a}(x + {b}) = {c}", f"{a}x + {b} = {c}"], "No distribuyó el factor sobre todos los términos: el paréntesis multiplica también a b", \
            ["Sumó el factor externo a cada término dentro del paréntesis", "Dividió el lado derecho por el factor externo sin distribuirlo", "Eliminó el paréntesis y dejó el factor externo escrito a la izquierda", "Multiplicó solo el segundo término del paréntesis por el factor externo"]
    if k == 2:
        return [f"x/{a} = {b}", f"x = {b}/{a}"], "Dividió en vez de multiplicar: para despejar x hay que multiplicar ambos lados por el denominador", \
            ["Multiplicó solo el lado izquierdo de la ecuación por el denominador", "Restó el denominador a ambos lados de la igualdad", "Elevó al cuadrado ambos lados en lugar de multiplicar por el denominador", "Sumó el denominador al lado derecho sin modificar el lado izquierdo"]
    if k == 3:
        return [f"{a}x = {a * b}", f"x = {a * b} − {a}"], "Restó el coeficiente en vez de dividir: el coeficiente de x multiplica, por lo que se divide", \
            ["Multiplicó ambos lados por el coeficiente en lugar de dividirlos entre él", "Sumó el coeficiente al lado derecho en lugar de restarlo del izquierdo", "Dividió solo el lado izquierdo de la ecuación entre el coeficiente de x", "Restó el coeficiente a ambos lados y obtuvo el mismo resultado luego"]
    return [f"−{a}x = {a * b}", f"x = {a * b}/{a} = {b}"], "Omitió el signo: al dividir por −a el resultado es negativo, x = −b", \
        ["Dividió por el valor absoluto del coeficiente y cambió el signo del lado izquierdo", "Multiplicó por −1 solo el lado derecho de la ecuación al despejar", "Restó el coeficiente del lado derecho sin considerar el signo negativo", "Pasó el coeficiente al otro lado sumando en lugar de dividiendo"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante en el segundo paso?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equiv(r, l):
    x = rr(r, 2, 9)
    a, b = rr(r, 2, 5), rr(r, 1, 9)
    c = a * x + b
    base = f"{a}x + {b} = {c}"
    good = [f"{a}x = {c - b}", f"{a}x + {b} − {b} = {c} − {b}", f"x = {x}", f"{2 * a}x + {2 * b} = {2 * c}"]
    bad = r.choice([f"{a}x = {c + b}", f"x = {c - b}", f"{a}x + {b} = {c + a}", f"{2 * a}x + {b} = {2 * c}"])
    fig = card(["Ecuación:", base], 130, 24)
    return make("¿Cuál de las siguientes ecuaciones NO es equivalente a la ecuación de la figura?", fig, bad, good, Q_ARG, f"La solución de la ecuación es x = {x}.")


TRUE = ["Sumar el mismo número a ambos lados de una ecuación mantiene su solución", "Multiplicar ambos lados por un número distinto de cero mantiene la solución", "Una ecuación de primer grado con una incógnita puede tener una única solución",
        "Para comprobar una solución se reemplaza en la ecuación original", "Dos ecuaciones son equivalentes si tienen exactamente las mismas soluciones", "La ecuación 0x = 5 no tiene solución"]
FALSE = ["Multiplicar ambos lados por cero mantiene las soluciones de la ecuación", "Toda ecuación de primer grado tiene exactamente dos soluciones", "Para comprobar una solución basta reemplazarla en el resultado final",
         "Restar un número solo del lado izquierdo mantiene la igualdad", "La ecuación 0x = 0 no tiene solución", "Dos ecuaciones con distinta forma nunca pueden ser equivalentes"]


def _fig(r):
    return card(["Ecuaciones de primer grado", "Lo que se hace a un lado, se hace al otro"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ecuaciones es verdadera?", "Sobre resolver ecuaciones de primer grado, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de la igualdad.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ecuaciones es falsa?", "Sobre resolver ecuaciones de primer grado, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de la igualdad.")


BY_SKILL = {
    Q_RES: [t_solve, t_fraction_eq, t_check],
    Q_MOD: [t_balance, t_perim_eq, t_plan],
    Q_REP: [t_numline_sol, t_table_sol, t_eq_from_balance],
    Q_ARG: [t_error, t_not_equiv, t_true, t_false],
}
