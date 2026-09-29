"""Clase 13 (M1) · Lenguaje algebraico y evaluación de expresiones."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
import viz

SUP2 = "²"


def co(c, v, first=True):
    """Término c·v con signo: primer término sin espacio; los demás con ' + ' o ' − '."""
    a = abs(c)
    body = (str(a) if a != 1 or not v else "") + v
    if first:
        return ("−" if c < 0 else "") + body
    return (" − " if c < 0 else " + ") + body


def lin(a, b, v="x"):
    """a·v + b bien escrito."""
    parts = ""
    if a:
        parts += co(a, v, True)
    if b or not a:
        parts += co(b, "", not a)
    return parts


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def rr(r, lo, hi):
    while True:
        x = r.randint(lo, hi)
        if x:
            return x


# ---------------------------------------------------------------- Resolver problemas
def t_eval_expr(r, l):
    a, b = rr(r, -5, 5), rr(r, -5, 5)
    p, q, s = r.randint(2, 6), r.randint(2, 6), r.randint(2, 4)
    if l == 0:
        forms = [(f"{p}a + {q}", "p*a+q", ["p*(a+q)", "p+a+q", "p*a-q"]), (f"{p}a − {q}", "p*a-q", ["p*(a-q)", "p*a+q", "p-a-q"]),
                 (f"{p} − {q}a", "p-q*a", ["(p-q)*a", "p+q*a", "q*a-p"])]
    elif l == 1:
        forms = [(f"{p}a − {q}b", "p*a-q*b", ["p*a+q*b", "p*(a-q)*b", "(p*a-q)*b"]), (f"a² + {p}b", "a**2+p*b", ["(a+p*b)**2", "a*2+p*b", "-a**2+p*b"]),
                 (f"{p}ab − {q}a", "p*a*b-q*a", ["p*(a+b)-q*a", "p*a*b+q*a", "(p*a*b-q)*a"])]
    else:
        forms = [(f"(a − b)² − {s}ab", "(a-b)**2-s*a*b", ["a**2-b**2-s*a*b", "(a-b)**2+s*a*b", "a**2+b**2-s*a*b"]), (f"{p}(a − {q}b) + {s}a²", "p*(a-q*b)+s*a**2", ["p*a-q*b+s*a**2", "p*(a-q*b)+(s*a)**2", "p*(a+q*b)+s*a**2"]),
                 (f"a² − b² − {s}(a + b)", "a**2-b**2-s*(a+b)", ["(a-b)**2-s*(a+b)", "a**2-b**2-s*a+b", "a**2-b**2+s*(a+b)"])]
    disp, ok, bad = r.choice(forms)
    v = dict(a=a, b=b, p=p, q=q, s=s)
    val = eval(ok, {}, v)
    alts = [eval(x, {}, v) for x in bad] + [-val, val + 2, val - 2]
    if abs(val) > 300:
        raise Reject
    fig = card(["Expresión: " + disp, (f"a = {a}" + (f",  b = {b}" if "b" in disp else "")).replace("-", "−")], 130, 21)
    ans = fs(val)
    return make("¿Cuál es el valor numérico de la expresión con los valores indicados en la figura?", fig, ans, pick4(ans, uq(ans, alts)), Q_RES, f"Se reemplazan las letras por sus valores respetando paréntesis y signos: {ans}.")


def t_given_sum(r, l):
    kind = r.choice(["sq", "sqdiff", "dbl"] if l else ["dbl", "sq"])
    x, y = rr(r, 1, 8), rr(r, 1, 8)
    if x == y:
        raise Reject
    if kind == "sq":
        s, pr = x + y, x * y
        val = x * x + y * y
        alts = [s * s, s * s + 2 * pr, s + pr, s * s - pr, 2 * pr]
        lines = [f"x + y = {s}", f"x·y = {pr}"]
        stem = "Se sabe que x + y y x·y tienen los valores de la figura. ¿Cuál es el valor de x² + y²?"
        ex = f"x² + y² = (x + y)² − 2xy = {s * s} − {2 * pr} = {val}."
    elif kind == "sqdiff":
        s, d = x + y, abs(x - y)
        val = s * d
        big, small = max(x, y), min(x, y)
        val = big * big - small * small
        lines = [f"x + y = {s}", f"x − y = {big - small}"]
        stem = "Se sabe que x + y y x − y tienen los valores de la figura (x > y). ¿Cuál es el valor de x² − y²?"
        alts = [s + (big - small), s * s - (big - small) ** 2, s - (big - small), (s - (big - small)) ** 2, val + s]
        ex = f"x² − y² = (x + y)(x − y) = {s}·{big - small} = {val}."
    else:
        c, d = r.randint(2, 6), r.randint(1, 9)
        val = c * x + d
        lines = [f"x = {x}", f"Expresión: {c}x + {d}"]
        alts = [c + x + d, c * (x + d), x + c * d, val + c, c * x - d]
        stem = "Con el valor de x de la figura, ¿cuál es el valor de la expresión?"
        ex = f"{c}·{x} + {d} = {val}."
    fig = card(lines, 60 + 40 * len(lines), 20)
    ans = str(val)
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_cost_model(r, l):
    a, b = r.choice([500, 800, 1000, 1200, 1500, 2000]), r.choice([300, 400, 500, 600, 700, 900])
    ctx = r.choice([("Un taxi cobra", "de bajada", "por kilómetro", "km"), ("Un arriendo de bicicleta cobra", "de inscripción", "por hora", "horas"), ("Un servicio técnico cobra", "de visita", "por cada repuesto", "repuestos")])
    f = lambda x: "$" + f"{x:,}".replace(",", ".")
    x = "x"
    ans = f"C = {a} + {b}x"
    alts = [f"C = {a + b}x", f"C = {a}x + {b}", f"C = {b} + {a}x", f"C = {a}·{b}x", f"C = {a + b} + x"]
    fig = card([f"{ctx[0]} {f(a)} {ctx[1]}", f"y {f(b)} {ctx[2]}", f"x = número de {ctx[3]}"], 170, 20)
    stem = f"{ctx[0]} {f(a)} {ctx[1]} más {f(b)} {ctx[2]}. ¿Qué expresión representa el costo total C en función de x ({ctx[3]})?"
    return make(stem, fig, ans, alts[:4], Q_MOD, "Costo = parte fija + (precio por unidad)·(cantidad de unidades).")


def t_geometry_expr(r, l):
    k = r.randint(2, 7)
    kind = r.choice(["area", "perim"])
    body = R(140, 30, 260, 120, FILL) + tag(270, 165, f"x + {k}", 18) + tag(110, 90, "x", 18)
    fig = wrap(560, 190, body, "Rectángulo de lados x y x + k")
    if kind == "area":
        stem = f"Un rectángulo tiene lados x y x + {k}. ¿Qué expresión representa su área?"
        ans = f"x² + {k}x"
        alts = [f"2x + {k}", f"4x + {2 * k}", f"x² + {k}", f"2x² + {k}x", f"x + x + {k}"]
        ex = f"Área = x·(x + {k}) = x² + {k}x."
    else:
        stem = f"Un rectángulo tiene lados x y x + {k}. ¿Qué expresión representa su perímetro?"
        ans = f"4x + {2 * k}"
        alts = [f"2x + {k}", f"x² + {k}x", f"4x + {k}", f"2x + {2 * k}", f"x² + {2 * k}"]
        ex = f"Perímetro = 2·[x + (x + {k})] = 4x + {2 * k}."
    return make(stem, fig, ans, alts[:4], Q_MOD, ex)


def t_age_model(r, l):
    m = r.randint(2, 4)
    d = r.randint(1, 8)
    t = r.choice([3, 5, 10])
    fig = card(["Ana tiene x años", f"Luis tiene {m} veces la edad de Ana menos {d} años"], 130, 19)
    stem = f"Ana tiene x años y Luis tiene {m} veces la edad de Ana menos {d} años. ¿Qué expresión representa la suma de sus edades dentro de {t} años?"
    ans = f"{m + 1}x − {d} + {2 * t}"
    alts = [f"{m + 1}x − {d} + {t}", f"{m + 1}x − {d + 2 * t}", f"x + {m}(x − {d}) + {2 * t}", f"{m + 1}x + {d} + {2 * t}", f"{m}x − {d} + {2 * t}"]
    ex = f"Hoy suman x + ({m}x − {d}); en {t} años cada uno suma {t}: total {m + 1}x − {d} + {2 * t}."
    return make(stem, fig, ans, alts[:4], Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_verbal_to_alg(r, l):
    n1 = r.choice([2, 3, 4, 5])
    n2 = r.choice([2, 3, 5, 7])
    forms = [
        (f"El {['doble', 'triple', 'cuádruple', 'quíntuple'][n1 - 2]} de la suma de a y b", f"{n1}(a + b)", [f"{n1}a + b", f"{n1} + a + b", f"{n1}a·b", f"(a + b)^{n1}".replace("^2", "²").replace("^3", "³").replace("^4", "⁴").replace("^5", "⁵")]),
        (f"La diferencia entre el cuadrado de x y {n2} veces y", f"x² − {n2}y", [f"(x − {n2}y)²", f"x² − y{'²' if n2 == 2 else ''} + {n2}".replace(" + " + str(n2), ""), f"{n2}y − x²", f"(x − y)² − {n2}"]),
        (f"La mitad del producto de a y b, aumentada en {n2}", f"ab/2 + {n2}", [f"a/2 · b/2 + {n2}", f"(ab + {n2})/2", f"ab + {n2}/2", f"2ab + {n2}"]),
        (f"El cuadrado de la diferencia entre m y {n2}", f"(m − {n2})²", [f"m² − {n2}²", f"m² − {n2}", f"m − {n2}²", f"({n2} − m)² + {n2}"]),
        (f"El {['doble', 'triple', 'cuádruple', 'quíntuple'][n1 - 2]} de un número, disminuido en {n2}", f"{n1}n − {n2}", [f"{n1}(n − {n2})", f"{n2} − {n1}n", f"{n1}n + {n2}", f"n{['²', '³', '⁴', '⁵'][n1 - 2]} − {n2}"]),
        (f"La suma de un número y su consecutivo", "n + (n + 1)", ["n + 1", "n·(n + 1)", "n + (n − 1)", "2n"]),
    ]
    text, ans, alts = r.choice(forms)
    fig = card(["Enunciado:", text], 130, 19)
    al = [x for x in dict.fromkeys(alts) if x != ans]
    if len(al) < 4:
        raise Reject
    return make("¿Qué expresión algebraica representa el enunciado de la figura?", fig, ans, al[:4], Q_REP, "Se traduce cada frase a una operación respetando el orden en que se enuncian.")


def t_alg_to_verbal(r, l):
    n = r.choice([2, 3, 4, 5])
    m = r.choice([2, 3, 5, 7])
    forms = [
        (f"{n}(x + {m})", f"El {['doble', 'triple', 'cuádruple', 'quíntuple'][n - 2]} de la suma de un número y {m}", [f"La suma del {['doble', 'triple', 'cuádruple', 'quíntuple'][n - 2]} de un número y {m}", f"El {['doble', 'triple', 'cuádruple', 'quíntuple'][n - 2]} de un número, aumentado en {m}", f"La suma de {n} y {m} veces un número", f"El número aumentado en el producto de {n} y {m}"]),
        (f"x² − {m}", f"El cuadrado de un número, disminuido en {m}", [f"El cuadrado de la diferencia entre un número y {m}", f"El doble de un número, disminuido en {m}", f"La diferencia entre {m} y el cuadrado de un número", f"El número disminuido en {m}, elevado al cuadrado"]),
        (f"(x − {m})²", f"El cuadrado de la diferencia entre un número y {m}", [f"El cuadrado de un número, disminuido en {m}", f"La diferencia entre el cuadrado de un número y {m}", f"El doble de la diferencia entre un número y {m}", f"El número, disminuido en el cuadrado de {m}"]),
        (f"x/{n} + {m}", f"La {['mitad', 'tercera parte', 'cuarta parte', 'quinta parte'][n - 2]} de un número, aumentada en {m}", [f"La {['mitad', 'tercera parte', 'cuarta parte', 'quinta parte'][n - 2]} de la suma de un número y {m}", f"El número aumentado en {m}, dividido por {n}", f"{n} veces un número, aumentado en {m}", f"La suma de {n} y {m}, dividida por el número"]),
    ]
    expr, ans, alts = r.choice(forms)
    fig = card(["Expresión:", expr.replace("x²", "x²")], 130, 26)
    return make("¿Cuál de los siguientes enunciados corresponde a la expresión de la figura?", fig, ans, alts, Q_REP, "Se lee la expresión operación por operación: paréntesis y potencias indican qué se agrupa.")


def t_table_rule(r, l):
    a = r.choice([2, 3, 4, 5, -1, -2])
    b = r.choice([1, 2, 3, 5, -1, -3, 0])
    xs = [1, 2, 3, 4]
    ys = [a * x + b for x in xs]
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [["y"] + [str(y).replace("-", "−") for y in ys]])
    ans = lin(a, b)
    alts = [lin(b, a) if b else lin(a + 1, b), lin(a, -b) if b else lin(a, 1), lin(a + 1, b), lin(a, b + 1), lin(-a, b)]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    if len(al) < 4:
        al += [lin(a + 2, b), lin(a, b - 2)]
    return make("La tabla muestra los valores de una expresión algebraica para distintos valores de x. ¿Cuál es la expresión?", fig, ans, al[:4], Q_REP, f"La variación por cada aumento de 1 en x es {a} y para x = 1 el valor es {ys[0]}: {ans}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.sample(range(2, 8), 2)
    if k == 0:
        return [f"{a}(x + {b}) = {a}x + {b}"], "No multiplicó el segundo término del paréntesis: la propiedad distributiva multiplica ambos términos", \
            [f"Sumó {a} al segundo término del paréntesis en lugar de multiplicarlo por {a}", f"Multiplicó los dos términos por {a} pero olvidó escribir la variable x", "Multiplicó solo el segundo término y dejó el primero sin multiplicar", "Dividió el paréntesis por el número exterior en lugar de multiplicarlo"]
    if k == 1:
        return [f"−(x − {a}) = −x − {a}"], f"No cambió el signo del segundo término al quitar el paréntesis: debió quedar −x + {a}", \
            ["Cambió el signo solo del primer término y dejó el segundo con su signo original", "Sumó el signo negativo con la variable en lugar de multiplicarlo por ambos términos", "Multiplicó el paréntesis por menos uno dos veces seguidas por error de cálculo", "Restó el número exterior al valor de la variable sin considerar el paréntesis"]
    if k == 2:
        return [f"{a}x + {b}x = {a + b}x²"], "Sumó los exponentes: al reducir términos semejantes solo se suman los coeficientes y la parte literal no cambia", \
            [f"Multiplicó los coeficientes en lugar de sumarlos y agregó un exponente cuadrado", "Sumó los coeficientes y multiplicó también la variable por sí misma dos veces", "Sumó las letras entre sí y dejó los coeficientes sin operar entre ellos", "Restó los coeficientes y elevó al cuadrado la variable resultante del cálculo"]
    if k == 3:
        return [f"{a}x + {b} = {a + b}x"], "Sumó términos que no son semejantes: un término con x y un término numérico no se pueden reducir", \
            ["Multiplicó los dos términos en lugar de sumarlos para reducir la expresión", "Sumó los coeficientes de la variable pero olvidó el término numérico final", "Restó el término numérico al coeficiente de la variable sin justificación", "Dividió el término numérico por el coeficiente antes de reducir la expresión"]
    return [f"(x + {a})² = x² + {a * a}"], "Elevó al cuadrado cada término y omitió el doble producto: (x + a)² = x² + 2ax + a²", \
        [f"Multiplicó el binomio por {a} en lugar de elevarlo al cuadrado completo", "Elevó al cuadrado solo el segundo término y dejó la variable sin elevar", "Sumó los cuadrados y luego los multiplicó por dos en el último paso", "Restó el cuadrado del segundo término en lugar de sumarlo al primero"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 120, 22)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equiv(r, l):
    a, b, c = r.randint(2, 6), r.randint(1, 6), r.randint(1, 5)
    if a == c:
        raise Reject
    cx = "x" if c == 1 else f"{c}x"
    base = f"{a}(x + {b}) − {cx}"
    good = lin(a - c, a * b)
    eq = [good, f"{a}x + {a * b} − {cx}", f"{a * b}" + (co(a - c, "x", False) if a - c else ""), f"{a}x − {cx} + {a * b}"]
    bad = r.choice([lin(a - c, b), lin(a + c, a * b), lin(a - c, a + b), lin(a - c, -a * b)])
    if bad in eq:
        raise Reject
    eq = list(dict.fromkeys(eq))
    if len(eq) < 4:
        raise Reject
    fig = card(["Expresión:", base], 130, 24)
    return make("¿Cuál de las siguientes expresiones NO es equivalente a la expresión de la figura?", fig, bad, eq[:4], Q_ARG, f"Al desarrollar: {a}x + {a * b} − {cx} = {good}.")


TRUE = ["En el término 5xy², el coeficiente numérico es 5", "Los términos 3x²y y −7x²y son semejantes", "El valor de una expresión algebraica depende de los valores que se asignen a sus variables",
        "La expresión 2(x + 3) es equivalente a 2x + 6", "En 3a² el exponente 2 afecta solo a la letra a", "Una expresión con dos términos se llama binomio"]
FALSE = ["Los términos 3x y 3x² son semejantes porque tienen el mismo coeficiente", "La expresión 2(x + 3) es equivalente a 2x + 3", "En 3a² el exponente 2 afecta también al número 3",
         "El valor de la expresión 2x + 1 es siempre 3", "Los términos semejantes se distinguen por tener igual coeficiente numérico", "3x + 2x es igual a 5x²"]


def _fig(r):
    return card(["Lenguaje algebraico", "Coeficiente · parte literal · términos semejantes"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre expresiones algebraicas es verdadera?", "Sobre el lenguaje algebraico, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones de término, coeficiente y términos semejantes.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre expresiones algebraicas es falsa?", "Sobre el lenguaje algebraico, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones algebraicas básicas.")


BY_SKILL = {
    Q_RES: [t_eval_expr, t_given_sum],
    Q_MOD: [t_cost_model, t_geometry_expr, t_age_model],
    Q_REP: [t_verbal_to_alg, t_alg_to_verbal, t_table_rule],
    Q_ARG: [t_error, t_not_equiv, t_true, t_false],
}
