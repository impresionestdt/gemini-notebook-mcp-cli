"""Clase 20 (M1) · Sistemas de ecuaciones lineales 2x2 II: problemas y toma de decisiones."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
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
        if a not in seen:
            seen.add(a); out.append(a)
    return out


def sprob(r, kind):
    if kind == "tickets":
        A, B = r.randint(20, 80), r.randint(20, 80)
        pa, pb = r.choice([(3000, 1500), (5000, 2000), (4000, 2500), (6000, 3000)])
        N, T = A + B, pa * A + pb * B
        text = f"En una función se vendieron {N} entradas entre adultos y niños. La entrada de adulto cuesta {f_(pa)} y la de niño {f_(pb)}; se recaudaron {f_(T)}."
        sys_ = (f"a + n = {N}", f"{pa}a + {pb}n = {T}")
        wr = [(f"a + n = {T}", f"{pa}a + {pb}n = {N}"), (f"a − n = {N}", f"{pa}a + {pb}n = {T}"), (f"a + n = {N}", f"{pa}a − {pb}n = {T}"), (f"a + n = {N}", f"{pb}a + {pa}n = {T}")]
        asks = [("adultos que asistieron", A), ("niños que asistieron", B)]
        lines = [f"Entradas vendidas: {N}", f"Adulto: {f_(pa)} · Niño: {f_(pb)}", f"Recaudación: {f_(T)}"]
        vars_ = "a: adultos, n: niños"
    elif kind == "coins":
        x, y = r.randint(5, 30), r.randint(5, 30)
        N, T = x + y, 100 * x + 500 * y
        text = f"En una alcancía hay {N} monedas, todas de {f_(100)} o de {f_(500)}, con un valor total de {f_(T)}."
        sys_ = (f"x + y = {N}", f"100x + 500y = {T}")
        wr = [(f"x + y = {T}", f"100x + 500y = {N}"), (f"x − y = {N}", f"100x + 500y = {T}"), (f"x + y = {N}", f"500x + 100y = {T}"), (f"x + y = {N}", f"600xy = {T}")]
        asks = [(f"monedas de {f_(100)}", x), (f"monedas de {f_(500)}", y)]
        lines = [f"Monedas en total: {N}", "Tipos: $100 y $500", f"Dinero total: {f_(T)}"]
        vars_ = "x: monedas de $100, y: monedas de $500"
    elif kind == "mix":
        x, y = r.randint(2, 12), r.randint(2, 12)
        pa, pb = r.choice([(4000, 6000), (5000, 8000), (3000, 5000), (6000, 9000)])
        K, T = x + y, pa * x + pb * y
        text = f"Se mezclan dos tipos de café: el primero cuesta {f_(pa)} el kg y el segundo {f_(pb)} el kg. La mezcla pesa {K} kg y costó {f_(T)}."
        sys_ = (f"x + y = {K}", f"{pa}x + {pb}y = {T}")
        wr = [(f"x + y = {T}", f"{pa}x + {pb}y = {K}"), (f"x + y = {K}", f"{pb}x + {pa}y = {T}"), (f"x − y = {K}", f"{pa}x + {pb}y = {T}"), (f"x + y = {K}", f"{pa}x − {pb}y = {T}")]
        asks = [("kg del primer café", x), ("kg del segundo café", y)]
        lines = [f"Mezcla: {K} kg", f"Precios: {f_(pa)} y {f_(pb)} por kg", f"Costo total: {f_(T)}"]
        vars_ = "x: kg del primero, y: kg del segundo"
    elif kind == "ages":
        x, y = r.randint(10, 30), r.randint(2, 9)
        S, D = x + y, x - y
        text = f"La suma de las edades de dos hermanos es {S} años y su diferencia es {D} años."
        sys_ = (f"x + y = {S}", f"x − y = {D}")
        wr = [(f"x + y = {D}", f"x − y = {S}"), (f"x + y = {S}", f"x + y = {D}"), (f"x · y = {S}", f"x − y = {D}"), (f"x + y = {S}", f"y − x = {D}")]
        asks = [("la edad del mayor", x), ("la edad del menor", y)]
        lines = [f"Suma de edades: {S}", f"Diferencia: {D}"]
        vars_ = "x: edad del mayor, y: edad del menor"
    else:
        y = r.randint(4, 30)
        x = 2 * y
        S = x + y
        text = f"La suma de dos números es {S} y uno de ellos es el doble del otro."
        sys_ = (f"x + y = {S}", "x = 2y")
        wr = [(f"x + y = {S}", "y = 2x"), (f"x · y = {S}", "x = 2y"), (f"x + y = {S}", "x = y + 2"), (f"x − y = {S}", "x = 2y")]
        asks = [("el mayor de los números", x), ("el menor de los números", y)]
        lines = [f"Suma: {S}", "Uno es el doble del otro"]
        vars_ = "x: el mayor, y: el menor"
    return dict(text=text, sys=sys_, wr=wr, asks=asks, lines=lines, vars=vars_, kind=kind)


KINDS = ["tickets", "coins", "mix", "ages", "numbers"]


# ---------------------------------------------------------------- Resolver problemas
def t_solve_problem(r, l):
    p = sprob(r, r.choice(KINDS if l else ["ages", "numbers", "coins"]))
    ask, val = r.choice(p["asks"])
    fig = card(p["lines"], 60 + 40 * len(p["lines"]), 18)
    stem = f"{p['text']} ¿Cuántos/cuál es {ask}?".replace("¿Cuántos/cuál es", "¿Cuál es la cantidad de") if False else f"{p['text']} ¿Cuánto es {ask}?"
    ans = str(val)
    x = val
    alts = [x + 1, x - 1 if x > 1 else x + 3, x + 5, x * 2, x + 10]
    al = [str(a) for a in dict.fromkeys(alts) if a != val and a > 0]
    return make(stem, fig, ans, al[:4], Q_RES, f"Se plantea el sistema {p['sys'][0]} ; {p['sys'][1]} y se resuelve por reducción o sustitución.")


def t_equal_cost(r, l):
    u = r.randint(2, 9)
    b1, b2 = r.randint(2, 6), r.randint(1, 3)
    if b1 <= b2:
        raise Reject
    c = r.randint(5, 20) * 100
    a = c - (b1 - b2) * u * 100
    if a <= 0:
        raise Reject
    ctx = r.choice([("Plan A", "Plan B", "GB", "internet"), ("Empresa A", "Empresa B", "km", "transporte"), ("Gimnasio A", "Gimnasio B", "clases", "gimnasio")])
    fig = card([f"{ctx[0]}: {f_(a)} fijo + {f_(b1 * 100)} por {ctx[2][:-1] if ctx[2].endswith('s') else ctx[2]}", f"{ctx[1]}: {f_(c)} fijo + {f_(b2 * 100)} por {ctx[2][:-1] if ctx[2].endswith('s') else ctx[2]}"], 140, 17)
    stem = f"{ctx[0]} cobra {f_(a)} fijos más {f_(b1 * 100)} por cada {ctx[2][:-1] if ctx[2].endswith('s') else ctx[2]}; {ctx[1]} cobra {f_(c)} fijos más {f_(b2 * 100)} por cada {ctx[2][:-1] if ctx[2].endswith('s') else ctx[2]}. ¿Con cuántos {ctx[2]} ambos cuestan lo mismo?"
    ans = str(u)
    alts = [u + 1, u - 1 if u > 1 else u + 2, u * 2, F(c - a, 100), F(c + a, (b1 + b2) * 100)]
    al = [str(int(x)) for x in dict.fromkeys(alts) if F(x).denominator == 1 and x > 0 and x != u]
    return make(stem, fig, ans, al[:4], Q_RES, f"{a} + {b1 * 100}x = {c} + {b2 * 100}x ⟹ x = {u}.")


# ---------------------------------------------------------------- Modelar
def t_pose_system(r, l):
    p = sprob(r, r.choice(KINDS))
    fig = card(p["lines"] + [p["vars"]], 60 + 36 * (len(p["lines"]) + 1), 17)
    stem = f"{p['text']} ¿Qué sistema de ecuaciones permite resolver el problema?"
    ans = f"{p['sys'][0]} ; {p['sys'][1]}"
    alts = [f"{a} ; {b}" for a, b in p["wr"]]
    return make(stem, fig, ans, alts, Q_MOD, "Cada dato del enunciado da una ecuación distinta con las dos incógnitas.")


def t_decide(r, l):
    u = r.randint(3, 9)
    b1, b2 = r.randint(2, 5), r.randint(1, 3)
    if b1 <= b2:
        raise Reject
    c = r.randint(6, 20) * 100
    a = c - (b1 - b2) * u * 100
    if a <= 0:
        raise Reject
    n = u + r.choice([-2, -1, 1, 2, 3])
    if n <= 0 or n == u:
        raise Reject
    fig = card([f"Plan A: {f_(a)} + {f_(b1 * 100)} por unidad", f"Plan B: {f_(c)} + {f_(b2 * 100)} por unidad", f"Uso previsto: {n} unidades"], 170, 18)
    stem = f"El plan A cobra {f_(a)} fijos más {f_(b1 * 100)} por unidad usada y el plan B cobra {f_(c)} fijos más {f_(b2 * 100)} por unidad. Si se usarán {n} unidades, ¿qué plan conviene?"
    cheaper = "A" if n < u else "B"
    ans = f"Plan {cheaper}, porque su costo con {n} unidades es menor"
    other = "B" if cheaper == "A" else "A"
    alts = [f"Plan {other}, porque su costo con {n} unidades es menor", f"Plan {cheaper}, porque su costo fijo es menor", f"Plan {other}, porque su precio por unidad es menor siempre", "Ambos cuestan lo mismo con esa cantidad de unidades"]
    ca, cb = a + b1 * 100 * n, c + b2 * 100 * n
    return make(stem, fig, ans, alts, Q_MOD, f"Costo A = {f_(ca)} y costo B = {f_(cb)} con {n} unidades: conviene el plan {cheaper}.")


def t_mix_pose(r, l):
    a, b = r.choice([(30, 50), (20, 40), (10, 30), (25, 60), (12, 20)]), None
    a, b = a
    q = r.choice([100, 200, 300, 500])
    fig = card([f"Solución 1: sal al {a}%", f"Solución 2: sal al {b}%", f"Se quieren {q} L con {(a + b) // 2}% de sal" if False else f"Total de mezcla: {q} L"], 150, 18)
    stem = f"Se mezclan x litros de una solución con {a}% de sal e y litros de otra con {b}% de sal para obtener {q} litros en total. ¿Qué ecuación representa la cantidad total de mezcla?"
    ans = f"x + y = {q}"
    alts = [f"{a}x + {b}y = {q}", f"x · y = {q}", f"x − y = {q}", f"{a}x + {b}y = 100"]
    return make(stem, fig, ans, alts, Q_MOD, "La suma de los volúmenes de las dos soluciones es el volumen total de la mezcla.")


# ---------------------------------------------------------------- Representar
def t_graph_plans(r, l):
    u = r.randint(2, 8)
    b1, b2 = r.randint(2, 4), r.randint(1, 2)
    if b1 <= b2:
        raise Reject
    c = r.randint(4, 10)
    a = c - (b1 - b2) * u
    if a <= 0:
        raise Reject
    top = max(c + b2 * 10, a + b1 * 10)
    p = Plot(560, 300, 0, 10, 0, 40)
    p.axes(2, 10)
    p.curve(lambda t: a + b1 * t, 0, 10, ACC, 4.5)
    p.curve(lambda t: c + b2 * t, 0, 10, NAVY, 4.5)
    fig = p.svg("Costo de dos planes según el uso").replace("</svg>", tag(330, 22, "Costo (miles de $) según unidades", 15) + "</svg>")
    kind = r.choice(["eq", "which"])
    if kind == "eq":
        stem = "El gráfico muestra el costo (en miles de pesos) de dos planes según las unidades usadas: el rojo es el plan A y el azul el plan B. ¿Con cuántas unidades ambos planes cuestan lo mismo?"
        ans = str(u)
        alts = [u + 1, u - 1 if u > 1 else u + 2, c, a, u * 2]
        al = [str(x) for x in dict.fromkeys(alts) if x != u and x > 0]
        ex = "El costo es igual donde se cruzan las dos rectas."
        return make(stem, fig, ans, al[:4], Q_REP, ex)
    n = u + r.choice([2, 3])
    if n > 10:
        n = u + 1
    stem = f"El gráfico muestra el costo (en miles de pesos) de dos planes según las unidades usadas: el rojo es el plan A y el azul el plan B. ¿Qué plan es más barato si se usan {n} unidades?"
    ans = "Plan B" if n > u else "Plan A"
    alts = ["Plan A" if ans == "Plan B" else "Plan B", "Ambos cuestan lo mismo", "No se puede saber con el gráfico", "Depende de las unidades fijas"]
    return make(stem, fig, ans, alts, Q_REP, f"A la derecha del punto de cruce (x = {u}) la recta roja está más arriba, por lo que el plan azul es más barato.")


def t_context_table(r, l):
    p = sprob(r, r.choice(["tickets", "mix", "coins"]))
    (n1, v1), (n2, v2) = p["asks"]
    kind = p["kind"]
    rows = []
    if kind == "tickets":
        m1, m2 = p["sys"][1].split(" + ")
        rows = [["Adulto", "a", m1.split("a")[0] + "a"], ["Niño", "n", m2.split("n")[0] + "n"]]
        head = ["Tipo", "Cantidad", "Dinero"]
    elif kind == "mix":
        m1, m2 = p["sys"][1].split(" + ")
        rows = [["Primer café", "x", m1], ["Segundo café", "y", m2.split(" =")[0]]]
        head = ["Tipo", "Kg", "Costo"]
    else:
        m1, m2 = p["sys"][1].split(" + ")
        rows = [["$100", "x", m1], ["$500", "y", m2.split(" =")[0]]]
        head = ["Moneda", "Cantidad", "Dinero"]
    fig = viz.table_fig(head, rows)
    stem = f"{p['text']} La tabla resume las cantidades y el dinero de cada tipo. ¿Cuál de las siguientes ecuaciones sale de sumar el dinero de ambos tipos?"
    import re
    ans = p["sys"][1]
    mm = re.match(r"(\d+)(\w) \+ (\d+)(\w) = (\d+)", ans)
    if not mm:
        raise Reject
    c1, v1_, c2, v2_, T_ = mm.groups()
    N_ = p["sys"][0].split("= ")[1]
    alts = [f"{c2}{v1_} + {c1}{v2_} = {T_}", f"{c1}{v1_} + {c2}{v2_} = {N_}", f"{c1}{v1_} − {c2}{v2_} = {T_}", f"{int(c1) + int(c2)}{v1_} = {T_}"]
    return make(stem, fig, ans, alts[:4], Q_REP, "Dinero total = dinero de un tipo + dinero del otro.")


# ---------------------------------------------------------------- Argumentar
def t_decision_arg(r, l):
    u = r.randint(3, 9)
    b1, b2 = r.randint(2, 5), r.randint(1, 3)
    if b1 <= b2:
        raise Reject
    c = r.randint(6, 20) * 100
    a = c - (b1 - b2) * u * 100
    if a <= 0:
        raise Reject
    fig = card([f"Plan A: {f_(a)} + {f_(b1 * 100)} por unidad", f"Plan B: {f_(c)} + {f_(b2 * 100)} por unidad"], 130, 18)
    stem = f"Un cliente afirma: «El plan B siempre conviene, porque su precio por unidad es menor». ¿Es correcta la afirmación?"
    ans = f"No: el plan A es más barato con menos de {u} unidades, porque su costo fijo es menor"
    alts = [f"Sí: el plan B es más barato con cualquier cantidad de unidades usadas", f"No: el plan A es más barato con más de {u} unidades, porque su precio por unidad es menor", f"Sí: con {u} unidades el plan B es más barato que el plan A", f"No: ambos planes cuestan lo mismo con cualquier cantidad de unidades"]
    return make(stem, fig, ans, alts, Q_ARG, f"Los planes cuestan lo mismo con {u} unidades; antes conviene A (menor costo fijo) y después B (menor precio por unidad).")


def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 6), r.randint(2, 9)
    if k == 0:
        return [f"«La suma de dos números es {a + b} y su diferencia es {a - b}»", f"Sistema: x + y = {a - b} ; x − y = {a + b}"], "Intercambió los datos: la suma corresponde a x + y y la diferencia a x − y, cada una con su valor", \
            ["Usó el producto de los números en lugar de su suma en la primera ecuación", "Escribió la diferencia como y − x sin cambiar el valor indicado en el enunciado", "Igualó la suma al doble de uno de los números sin otro dato del enunciado", "Planteó una sola ecuación porque los dos datos son equivalentes entre sí"]
    if k == 1:
        return [f"«{a} kg de A y B cuestan $1.000; A cuesta el doble de B»", f"Sistema: {a}x + y = 1000 ; y = 2x"], "Asignó el doble al precio equivocado: si A cuesta el doble de B, debió escribir A = 2B", \
            ["Sumó los kilos en lugar de multiplicarlos por el precio de cada tipo de producto", "Igualó el precio total con el precio de un solo kilo del primer tipo", "Escribió el precio total como el producto de ambos precios unitarios", "Planteó las dos ecuaciones con el mismo coeficiente para ambos precios"]
    if k == 2:
        return ["Un sistema da x = 3, y = −2 donde x e y son cantidades de personas", "Conclusión: hay 3 personas de un tipo y −2 del otro"], "Una cantidad de personas no puede ser negativa: la solución no es válida en el contexto y hay que revisar el planteo", \
            ["La solución es válida siempre que la ecuación se haya resuelto correctamente", "Basta con tomar el valor absoluto de −2 para que la solución sea válida", "El signo negativo indica que las personas de ese tipo salieron del lugar", "La solución es válida porque las dos ecuaciones se cumplen al reemplazar"]
    return ["Sistema de dos rectas paralelas distintas", "Conclusión: tiene infinitas soluciones"], "Rectas paralelas distintas no se cruzan: el sistema no tiene solución; infinitas soluciones ocurre con rectas coincidentes", \
        ["Las rectas paralelas distintas se cruzan en el origen del plano cartesiano siempre", "Un sistema de dos rectas distintas siempre tiene exactamente una solución única", "Las rectas paralelas tienen infinitas soluciones porque nunca dejan de crecer", "Las rectas paralelas se cruzan en un punto muy alejado del origen del plano"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 42 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["Un problema con dos incógnitas y dos datos independientes se puede modelar con un sistema 2x2", "La solución de un sistema debe interpretarse en el contexto del problema",
        "Dos planes de costo lineal cuestan lo mismo en el punto donde se cruzan sus gráficas", "Un plan con menor costo fijo puede ser más barato con poco uso aunque su precio por unidad sea mayor",
        "Si un sistema tiene solución negativa para una cantidad de personas, hay que revisar el planteo", "Definir qué representa cada incógnita ayuda a plantear el sistema"]
FALSE = ["Todo problema con dos incógnitas tiene solución única y válida en el contexto", "El plan con menor precio por unidad es siempre el más barato", "Dos planes de costo lineal siempre cuestan lo mismo para alguna cantidad de unidades positiva",
         "Una solución negativa para una cantidad de personas es válida si cumple las ecuaciones", "Basta una ecuación para determinar dos incógnitas independientes", "Las gráficas de dos planes se cruzan siempre en el origen"]


def _fig(r):
    return card(["Sistemas y decisiones", "Modelar · resolver · interpretar en el contexto"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre problemas con sistemas de ecuaciones es verdadera?", "Sobre modelar con dos incógnitas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el modelo de sistema y con la interpretación de resultados.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre problemas con sistemas de ecuaciones es falsa?", "Sobre modelar con dos incógnitas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el modelo de sistema.")


BY_SKILL = {
    Q_RES: [t_solve_problem, t_equal_cost],
    Q_MOD: [t_pose_system, t_decide, t_mix_pose],
    Q_REP: [t_graph_plans, t_context_table],
    Q_ARG: [t_decision_arg, t_error, t_true, t_false],
}
