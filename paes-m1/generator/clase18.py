"""Clase 18 (M1) · Ecuaciones de primer grado II: planteo (edades, monedas, movimiento, consecutivos, reparto)."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
import viz


def f_(z):
    return "$" + f"{z:,}".replace(",", ".")


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


NAMES = [("Ana", "su madre"), ("Luis", "su padre"), ("Marta", "su abuela"), ("Pedro", "su tío")]
PEOPLE = [("Ana", "Bruno", "Carla"), ("Luis", "Marta", "Pablo"), ("Sofía", "Diego", "Elena"), ("Rosa", "Tomás", "Julia")]


def prob(r, kind, l):
    """Problema tipo con solución entera; devuelve dict con texto, x, ecuación y erróneas."""
    if kind == "age":
        who, rel = r.choice(NAMES)
        x = r.randint(6, 16)
        m = r.randint(2, 4)
        t = r.randint(3, 10)
        S = (x + t) + (m * x + t)
        text = f"{who} tiene x años y {rel} tiene {m} veces su edad. Dentro de {t} años, la suma de las edades de ambos será {S} años."
        eq = f"(x + {t}) + ({m}x + {t}) = {S}"
        wr = [f"x + {m}x + {t} = {S}", f"(x + {t}) · ({m}x + {t}) = {S}", f"x + {m + t}x = {S}", f"(x + {t}) + {m}x = {S}"]
        asks = [(f"la edad actual de {who}", x), (f"la edad actual de {rel}", m * x)]
        if l == 0:
            asks = asks[:1]
        fig = [f"{who}: x años", f"{rel.capitalize()}: {m}x años", f"Dentro de {t} años, suma = {S}"]
        expr_q = (f"¿Qué expresión representa la edad de {rel} dentro de {t} años?", f"{m}x + {t}", [f"{m}(x + {t})", f"{m + t}x", f"x + {m + t}", f"{m}x − {t}"])
    elif kind == "coins":
        x = r.randint(4, 20)
        a = r.randint(2, 8)
        v1, v2 = r.choice([(100, 50), (500, 100), (100, 10), (500, 50)])
        T = v1 * x + v2 * (x + a)
        text = f"En una alcancía hay x monedas de {f_(v1)} y {a} monedas más de {f_(v2)} que de {f_(v1)}. En total hay {f_(T)}."
        eq = f"{v1}x + {v2}(x + {a}) = {T}"
        wr = [f"{v1}x + {v2}x + {a} = {T}", f"{v1}x · {v2}(x + {a}) = {T}", f"{v1}x + {v2}(x − {a}) = {T}", f"{v1 + v2}(x + {a}) = {T}"]
        asks = [(f"la cantidad de monedas de {f_(v1)}", x), (f"la cantidad de monedas de {f_(v2)}", x + a)]
        if l == 0:
            asks = asks[:1]
        fig = [f"Monedas de {f_(v1)}: x", f"Monedas de {f_(v2)}: x + {a}", f"Total: {f_(T)}"]
        expr_q = (f"¿Qué expresión representa el dinero, en pesos, que suman las monedas de {f_(v2)}?", f"{v2}(x + {a})", [f"{v2}x + {a}", f"{v2} + (x + {a})", f"{v2}x", f"(x + {a}) : {v2}"])
    elif kind == "motion":
        x = r.randint(2, 6)
        v1, v2 = r.choice([(40, 60), (50, 70), (30, 50), (45, 55), (60, 80), (20, 30)])
        D = (v1 + v2) * x
        text = f"Dos trenes salen a la vez de dos ciudades separadas {D} km, uno hacia el otro, a {v1} km/h y {v2} km/h. Se encuentran después de x horas."
        eq = f"{v1}x + {v2}x = {D}"
        wr = [f"{v1}x − {v2}x = {D}", f"{v1 * v2}x = {D}", f"{v1}x + {v2} = {D}", f"({v1} + {v2}) : x = {D}"]
        asks = [("las horas que tardan en encontrarse", x), (f"los kilómetros que recorre el tren de {v2} km/h hasta el encuentro", v2 * x)]
        if l == 0:
            asks = asks[:1]
        fig = [f"Distancia entre ciudades: {D} km", f"Velocidades: {v1} y {v2} km/h", "Se encuentran en x horas"]
        expr_q = ("¿Qué expresión representa los kilómetros recorridos por el primer tren hasta el encuentro?", f"{v1}x", [f"{v1} + x", f"{v1} : x", f"{D} − {v1}", f"{v1 + v2}x"])
    elif kind == "consec":
        x = r.randint(4, 30)
        cnt = r.choice([3, 4] if l else [3])
        step = r.choice([1, 2]) if l else 1
        nums = [x + step * i for i in range(cnt)]
        S = sum(nums)
        kd = "consecutivos" if step == 1 else "pares consecutivos" if x % 2 == 0 else "impares consecutivos"
        if step == 2 and x % 2:
            kd = "impares consecutivos"
        text = f"La suma de {cnt} números {kd} es {S}. El menor de ellos es x."
        eq = " + ".join([f"x" if i == 0 else f"(x + {step * i})" for i in range(cnt)]) + f" = {S}"
        wr = [" + ".join(["x"] + [f"{step * i}" for i in range(1, cnt)]) + f" = {S}", f"x · (x + {step}) · (x + {2 * step}) = {S}", " + ".join(["x"] + [f"(x − {step * i})" for i in range(1, cnt)]) + f" = {S}", f"{cnt}x = {S}"]
        asks = [("el menor de los números", x), ("el mayor de los números", nums[-1])]
        if l == 0:
            asks = asks[:1]
        fig = [f"{cnt} números {kd}", f"Menor = x; los demás suman {step} más cada vez", f"Suma = {S}"]
        expr_q = ("¿Qué expresión representa el segundo número?", f"x + {step}", ["2x", f"x − {step}", f"x + {2 * step}", f"x + {step + 1}"])
    else:
        who = r.choice(PEOPLE)
        x = r.randint(20, 90) * 100
        a = r.randint(5, 30) * 100
        N = x + (x + a) + 2 * x
        text = f"Se reparten {f_(N)} entre {who[0]}, {who[1]} y {who[2]}. {who[1]} recibe {f_(a)} más que {who[0]} y {who[2]} recibe el doble de lo que recibe {who[0]}. Sea x lo que recibe {who[0]}."
        eq = f"x + (x + {a}) + 2x = {N}"
        wr = [f"x + x + {a} + 2x = {N} · 2", f"x · (x + {a}) · 2x = {N}", f"x + (x + {a}) + x + 2 = {N}", f"x + (x + {a}) + 2(x + {a}) = {N}"]
        asks = [(f"lo que recibe {who[0]}", x), (f"lo que recibe {who[2]}", 2 * x)]
        if l == 0:
            asks = asks[:1]
        fig = [f"Total: {f_(N)}", f"{who[0]}: x  ·  {who[1]}: x + {a}", f"{who[2]}: 2x"]
        expr_q = (f"¿Qué expresión representa lo que recibe {who[2]}?", "2x", [f"x + 2", f"x + {a}", f"2 + x", f"x : 2"])
    ask = r.choice(asks)
    return dict(text=text, x=x, eq=eq, wrongs=wr, ask=ask, fig=fig, expr=expr_q, kind=kind)


KINDS0 = ["age", "consec", "split"]
KINDS1 = ["age", "coins", "motion", "consec", "split"]


def fmt_val(kind, v):
    if kind == "coins":
        return str(v)
    return f"{v:,}".replace(",", ".") if v >= 10000 else str(v)


# ---------------------------------------------------------------- Resolver problemas
def t_solve_problem(r, l):
    p = prob(r, r.choice(KINDS0 if l == 0 else KINDS1), l)
    ask, val = p["ask"]
    fig = card(p["fig"], 60 + 40 * len(p["fig"]), 18)
    stem = f"{p['text']} ¿Cuánto es {ask}?" if p["kind"] != "split" else f"{p['text']} ¿Cuánto es {ask}?"
    u = " pesos" if p["kind"] == "split" else ""
    ans = fmt_val(p["kind"], val) + u
    x = p["x"]
    alts = [x + 1, x - 1 if x > 1 else x + 3, val + x, val * 2, val + 5, x * 2]
    al = uq(ans, [fmt_val(p["kind"], a) + u for a in alts if a > 0])
    al = [a for a in al if a != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"Se plantea {p['eq']} y se resuelve: x = {fmt_val(p['kind'], x)}; {ask} = {ans}.")


# ---------------------------------------------------------------- Modelar
def t_pose(r, l):
    p = prob(r, r.choice(KINDS0 if l == 0 else KINDS1), l)
    fig = card(p["fig"], 60 + 40 * len(p["fig"]), 18)
    stem = f"{p['text']} ¿Qué ecuación permite calcular el valor de x?"
    return make(stem, fig, p["eq"], p["wrongs"], Q_MOD, "Se traduce cada frase del enunciado a una expresión con x y se iguala al dato total.")


def t_expr(r, l):
    p = prob(r, r.choice(KINDS1), l)
    fig = card(p["fig"], 60 + 40 * len(p["fig"]), 18)
    q, ans, wr = p["expr"]
    stem = f"{p['text']} {q}"
    return make(stem, fig, ans, wr, Q_MOD, "Se relaciona la cantidad pedida con x según el enunciado.")


def t_ratio_age(r, l):
    a = r.randint(8, 18)
    m = r.randint(2, 4)
    t = r.randint(2, 12)
    val = m * (a + t)
    stem = f"Hoy Ana tiene {a} años. Dentro de {t} años, su padre tendrá {m} veces la edad que Ana tendrá entonces. ¿Cuántos años tendrá el padre dentro de {t} años?"
    fig = card([f"Ana hoy: {a} años", f"En {t} años: Ana {a + t}", f"Padre = {m} · (edad de Ana)"], 170, 18)
    ans = str(val)
    alts = [m * a + t, m * a, a + t + m, m * (a - t) if a > t else val + m, val + t]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_MOD, f"Edad de Ana en {t} años = {a + t}; padre = {m}·{a + t} = {val}.")


# ---------------------------------------------------------------- Representar
def t_motion_diag(r, l):
    x = r.randint(2, 6)
    v1, v2 = r.choice([(40, 60), (50, 70), (30, 50), (45, 55), (60, 80), (20, 30)])
    D = (v1 + v2) * x
    body = L(60, 110, 500, 110, INK, 4) + C(60, 110, 8, INK, INK, 1) + C(500, 110, 8, INK, INK, 1)
    body += tag(60, 140, "A", 17) + tag(500, 140, "B", 17) + tag(280, 60, f"{D} km", 18)
    body += L(80, 85, 200, 85, ACC, 5) + P([(200, 75), (222, 85), (200, 95)], ACC, ACC, 1) + L(480, 85, 360, 85, NAVY, 5) + P([(360, 75), (338, 85), (360, 95)], NAVY, NAVY, 1)
    body += tag(140, 165, f"{v1} km/h", 16) + tag(420, 165, f"{v2} km/h", 16)
    fig = wrap(560, 200, body, "Dos móviles que se acercan")
    stem = "Dos móviles salen a la vez de A y de B, uno hacia el otro, con las rapideces de la figura, y se encuentran después de x horas. ¿Qué ecuación permite calcular x?"
    ans = f"{v1}x + {v2}x = {D}"
    alts = [f"{v1}x − {v2}x = {D}", f"{v1}x = {D}", f"({v1} + {v2}) : x = {D}", f"{v1} + {v2}x = {D}"]
    return make(stem, fig, ans, alts, Q_REP, "Entre ambos recorren toda la distancia: la suma de lo que recorre cada uno es la distancia total.")


def t_coin_table(r, l):
    x = r.randint(3, 15)
    a = r.randint(2, 6)
    v1, v2 = r.choice([(100, 50), (500, 100), (100, 10)])
    rows = [[f_(v1), "x", f"{v1}x"], [f_(v2), f"x + {a}", f"{v2}(x + {a})"]]
    fig = viz.table_fig(["Moneda", "Cantidad", "Dinero"], rows)
    T = v1 * x + v2 * (x + a)
    stem = f"La tabla resume las monedas de una alcancía y el dinero que aporta cada tipo. Si en total hay {f_(T)}, ¿qué ecuación permite calcular x?"
    ans = f"{v1}x + {v2}(x + {a}) = {T}"
    alts = [f"{v1}x + {v2}x + {a} = {T}", f"{v1}x · {v2}(x + {a}) = {T}", f"{v1 + v2}x = {T}", f"{v1}(x + {a}) + {v2}x = {T}"]
    return make(stem, fig, ans, alts, Q_REP, "Dinero total = dinero de las monedas de un tipo + dinero de las del otro.")


def t_bar_model(r, l):
    a = r.randint(5, 30) * 100
    x = r.randint(20, 90) * 100
    N = 4 * x + a
    w = 440
    tot = 4
    body = ""
    segs = [("x", 1, FILL), (f"x + {a}", 1, FILL2), ("2x", 2, FILL3)]
    xx = 60
    for lab, n, col in segs:
        ww = w * n / tot
        body += R(xx, 60, ww, 60, col, NAVY, 3) + T(xx + ww / 2, 98, lab, 20)
        xx += ww
    body += tag(280, 30, f"Total: {f_(N)}", 17)
    fig = wrap(560, 150, body, "Barra dividida en tres partes")
    stem = "La barra representa el reparto de una cantidad de dinero en tres partes. ¿Qué ecuación permite calcular x?"
    ans = f"x + (x + {a}) + 2x = {N}"
    alts = [f"x + x + {a} + 2x = {N} + x", f"x · (x + {a}) · 2x = {N}", f"x + (x + {a}) + x + 2 = {N}", f"4x = {N}"]
    return make(stem, fig, ans, alts, Q_REP, "La suma de las tres partes de la barra es el total.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.randint(2, 6), r.randint(2, 9)
    if k == 0:
        return [f"«El doble de un número, aumentado en {b}»", f"Ecuación: 2(x + {b})"], f"Agrupó la suma dentro del paréntesis: el doble afecta solo a x, por lo que debía ser 2x + {b}", \
            ["Cambió el orden de las operaciones y sumó antes de multiplicar el número por dos", "Escribió el doble como x + 2 en lugar de 2x al traducir la frase", "Multiplicó el número por el valor aumentado en lugar de sumarlo", "Restó el valor en lugar de sumarlo al traducir la palabra aumentado"]
    if k == 1:
        return [f"«{b} menos que el triple de un número»", f"Ecuación: {b} − 3x"], f"Invirtió el orden de la resta: «{b} menos que» significa restar {b} al triple, es decir 3x − {b}", \
            ["Escribió el triple como x + 3 en vez de multiplicar el número por tres", "Sumó el valor al triple del número sin considerar las palabras menos que", "Multiplicó el valor por el triple en lugar de restarlo del triple del número", "Dividió el número por tres al traducir la frase del enunciado"]
    if k == 2:
        return [f"«Ana tiene {a} años más que Luis»", f"Ana = x, Luis = x + {a}"], "Asignó la edad mayor a Luis: si x es la edad de Luis, Ana tiene x + a, o si x es la de Ana, Luis tiene x − a", \
            ["Sumó los años a ambas edades para que los dos aumenten por igual", "Multiplicó la edad de Luis por los años de diferencia con Ana", "Restó los años a ambas edades sin distinguir quién es mayor", "Dejó las dos edades iguales porque no consideró el dato de la diferencia"]
    if k == 3:
        return [f"«La suma de dos números consecutivos es {2 * b + 1}»", f"Ecuación: x + x + 1 = {2 * b + 1}"], "La ecuación x + x + 1 sí es correcta pero el estudiante no la resolvió: 2x + 1 = " + str(2 * b + 1), \
            ["Debió plantear x · (x + 1) porque la palabra suma implica multiplicación", "Debió plantear x + (x − 1) porque el segundo número es menor que el primero", "Debió plantear 2(x + 1) porque hay dos números y ambos aumentan uno", "Debió plantear x + 2 porque consecutivo significa dos unidades más"]
    return [f"«El {a}% de un número es {b * 10}»", f"Ecuación: {a}x = {b * 10}"], f"Usó {a} en lugar de {a}/100 al plantear: el porcentaje es una fracción sobre 100", \
        ["Usó la fracción invertida 100/x en lugar de multiplicar el número por el porcentaje", "Sumó el porcentaje al número en vez de tomar esa parte de él", "Dividió el número por el porcentaje y no por cien como corresponde", "Restó el porcentaje del número y llamó al resultado el total"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Planteo de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 18)
    if "sí es correcta" in ans:
        raise Reject
    return make("Observa el planteo de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_valid(r, l):
    kind = r.choice([("la edad de una persona", "años"), ("el número de monedas de una alcancía", "monedas"), ("la cantidad de personas de un curso", "personas"), ("el tiempo, en horas, que dura un viaje", "horas")])
    bad = r.choice([("−4", "es negativo"), ("2,5", "no es un número entero"), ("−12", "es negativo"), ("0,75", "no es un número entero")])
    if kind[0].startswith("el tiempo") and bad[1] == "no es un número entero":
        raise Reject
    fig = card([f"Al resolver una ecuación se obtiene x = {bad[0]}", f"x representa: {kind[0]}"], 130, 19)
    stem = f"Al resolver una ecuación de un problema se obtiene x = {bad[0]}, donde x representa {kind[0]}. ¿Qué se puede concluir?"
    ans = f"La solución no es válida en el contexto, porque {bad[1]} y no puede representar esa cantidad"
    alts = ["La solución es válida, porque toda solución de la ecuación lo es en el problema", "La solución es válida solo si se toma su valor absoluto sin analizar el contexto", "La solución no es válida porque la ecuación está mal resuelta sin importar el contexto", "No se puede concluir nada hasta plantear una nueva ecuación diferente"]
    return make(stem, fig, ans, alts, Q_ARG, "Toda solución debe interpretarse en el contexto: una cantidad de objetos no puede ser negativa ni fraccionaria.")


TRUE = ["Antes de plantear una ecuación conviene definir qué representa la incógnita", "Una solución debe comprobarse en el enunciado del problema y no solo en la ecuación", "«Tres más que un número» se escribe x + 3",
        "«El triple de un número» se escribe 3x", "Si x es un número, el siguiente consecutivo se escribe x + 1", "«Dos menos que un número» se escribe x − 2"]
FALSE = ["«Tres más que un número» se escribe 3x", "«Dos menos que un número» se escribe 2 − x", "El siguiente número par de x se escribe x + 1",
         "Una solución negativa siempre es válida en un problema de edades", "«El doble de un número, aumentado en 5» se escribe 2(x + 5)", "No es necesario definir la incógnita si el enunciado es corto"]


def _fig(r):
    return card(["Planteo de ecuaciones", "Definir la incógnita · traducir · resolver · comprobar"], 130, 18)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el planteo de ecuaciones es verdadera?", "Sobre traducir enunciados a ecuaciones, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las reglas de traducción del lenguaje natural al algebraico.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el planteo de ecuaciones es falsa?", "Sobre traducir enunciados a ecuaciones, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las reglas de traducción.")


BY_SKILL = {
    Q_RES: [t_solve_problem],
    Q_MOD: [t_pose, t_expr, t_ratio_age],
    Q_REP: [t_motion_diag, t_coin_table, t_bar_model],
    Q_ARG: [t_error, t_valid, t_true, t_false],
}
