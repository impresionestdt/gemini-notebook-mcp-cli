"""Clase 15 (M1) · Productos notables: cuadrado de binomio y suma por diferencia; áreas compuestas."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
import viz


def bin_(A, B, v="x"):
    """A·v + B como texto de binomio (para escribir dentro de paréntesis)."""
    return co(A, v, True) + co(B, "", False)


def sq_exp(A, B, v="x", w=""):
    """(A v + B)² desarrollado: A²v² + 2AB v + B²."""
    return co(A * A, v + "²", True) + co(2 * A * B, v, False) + co(B * B, "", False)


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver problemas
def t_expand(r, l):
    if l == 0:
        A = 1
    elif l == 1:
        A = r.choice([2, 3, 4, 5])
    else:
        A = r.choice([2, 3, 4])
    B = r.choice([-1, 1]) * r.randint(1, 9 if A == 1 else 6)
    kind = "sq" if l < 2 or r.random() < 0.6 else "dsum"
    if kind == "sq":
        disp = f"({bin_(A, B)})²"
        ans = sq_exp(A, B)
        alts = [co(A * A, "x²", True) + co(B * B, "", False), co(A * A, "x²", True) + co(2 * A * B, "x", False) + co(-B * B, "", False), co(A * A, "x²", True) + co(-2 * A * B, "x", False) + co(B * B, "", False),
                co(A * A, "x²", True) + co(A * B, "x", False) + co(B * B, "", False), co(A, "x²", True) + co(2 * A * B, "x", False) + co(B * B, "", False)]
        ex = f"(a ± b)² = a² ± 2ab + b²: {ans}."
    else:
        B = abs(B)
        disp = f"({bin_(A, B)})({bin_(A, -B)})"
        ans = co(A * A, "x²", True) + co(-B * B, "", False)
        alts = [co(A * A, "x²", True) + co(B * B, "", False), co(A, "x²", True) + co(-B * B, "", False), co(A * A, "x²", True) + co(-2 * A * B, "x", False) + co(B * B, "", False), co(A * A, "x²", True) + co(2 * A * B, "x", False) + co(B * B, "", False), co(A * A, "x²", True) + co(-B, "", False)]
        ex = f"(a + b)(a − b) = a² − b²: {ans}."
    fig = card(["Desarrolla:", disp], 130, 24)
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("¿Cuál es el desarrollo del producto notable de la figura?", fig, ans, al[:4], Q_RES, ex)


def t_numeric(r, l):
    kind = r.choice(["sum", "diff", "sd"])
    if kind == "sum":
        base, d = r.choice([(100, 3), (100, 2), (50, 1), (200, 5), (30, 2), (1000, 2), (100, 4), (40, 3)])
        n = base + d
        val = n * n
        disp = f"{n}²"
        alts = [base * base + d * d, base * base + d * d + d, (base + d) * 2, n * d, val + 2 * d]
        ex = f"{n}² = ({base} + {d})² = {base * base} + {2 * base * d} + {d * d} = {val}."
    elif kind == "diff":
        base, d = r.choice([(100, 3), (100, 2), (50, 1), (200, 5), (30, 2), (1000, 2), (100, 4), (40, 3)])
        n = base - d
        val = n * n
        disp = f"{n}²"
        alts = [base * base - d * d, base * base - 2 * base * d, base * base + 2 * base * d + d * d, val + d * d, val - 2 * d]
        ex = f"{n}² = ({base} − {d})² = {base * base} − {2 * base * d} + {d * d} = {val}."
    else:
        base, d = r.choice([(50, 1), (100, 1), (100, 2), (30, 1), (20, 1), (60, 2), (200, 3), (10, 1)])
        a, b = base - d, base + d
        val = a * b
        disp = f"{a} · {b}"
        alts = [base * base + d * d, base * base, val + d, val - d * d, base * base - 2 * d]
        ex = f"{a}·{b} = ({base} − {d})({base} + {d}) = {base}² − {d}² = {val}."
    if val < 1:
        raise Reject
    ans = f"{val:,}".replace(",", ".")
    al = [x for x in dict.fromkeys(f"{a:,}".replace(",", ".") for a in alts if a > 0) if x != ans]
    fig = card(["Calcula usando un producto notable:", disp], 130, 21)
    return make("¿Cuál es el resultado de la operación de la figura?", fig, ans, al[:4], Q_RES, ex)


def t_complete(r, l):
    A = 1 if l == 0 else r.choice([1, 2, 3, 4])
    B = r.randint(1, 9)
    sgn = r.choice([1, -1])
    mid = 2 * A * B
    disp = co(A * A, "x²", True) + co(sgn * mid, "x", False) + " + ?"
    ans = str(B * B)
    alts = [B, mid, B * B + A, B * B - 1, B * B + 2 * B, B * B + B]
    al = [str(a) for a in dict.fromkeys(alts) if str(a) != ans]
    fig = card(["Completa para un cuadrado perfecto:", disp], 130, 21)
    return make("¿Qué número debe reemplazar a «?» para que la expresión sea el desarrollo de un cuadrado de binomio?", fig, ans, al[:4], Q_RES, f"El término faltante es el cuadrado de la mitad del coeficiente de x dividido por A: {B}² = {B * B}.")


# ---------------------------------------------------------------- Modelar
def sq_fig(a_lab, x_lab="x"):
    body = R(80, 30, 160, 160, FILL, NAVY, 3) + R(240, 30, 80, 160, FILL2, NAVY, 3) + R(80, 190, 160, 80, FILL2, NAVY, 3) + R(240, 190, 80, 80, FILL3, NAVY, 3)
    body += T(160, 118, x_lab + "²", 26) + T(280, 118, a_lab + x_lab, 20) + T(160, 238, a_lab + x_lab, 20) + T(280, 238, a_lab + "²", 20)
    body += tag(160, 20, x_lab, 16) + tag(280, 20, a_lab, 16) + tag(60, 110, x_lab, 16) + tag(60, 230, a_lab, 16)
    return wrap(560, 290, body, "Cuadrado dividido en cuatro regiones")


GARD = [("Un jardín cuadrado", "un camino", "camino"), ("Una piscina cuadrada", "un borde", "borde"), ("Un patio cuadrado", "una vereda", "vereda"), ("Una cancha cuadrada", "una franja de pasto", "franja")]
MARC = [("Un cuadro cuadrado", "un marco", "marco"), ("Un espejo cuadrado", "un marco", "marco"), ("Una ventana cuadrada", "una moldura", "moldura"), ("Un azulejo cuadrado", "un borde", "borde")]


def t_garden(r, l):
    a = r.randint(1, 9)
    subj, pn_art, pn = r.choice(GARD)
    kind = r.choice(["path", "square"])
    if kind == "path":
        body = R(100, 30, 280, 280, FILL2, NAVY, 3) + R(100 + 40, 30 + 40, 200, 200, FILL, NAVY, 3) + T(240, 175, "x", 30) + tag(120, 60, str(a), 15) + tag(240, 50, "camino", 15)
        fig = wrap(560, 330, body, "Jardín cuadrado rodeado de un camino")
        stem = f"{subj} de lado x metros está rodeado por {pn_art} de {a} metros de ancho. ¿Qué expresión representa el área total (incluida la superficie del {pn})?"
        ans = sq_exp(1, 2 * a)
        alts = [f"x² + {2 * a}", f"x² + {a * a}", f"x² + {4 * a}x + {4 * a * a}".replace("+ -", "− ") if False else co(1, "x²", True) + co(4 * a, "x", False) + co(4 * a * a, "", False), sq_exp(1, a), f"x² + {2 * a}x"]
        ex = f"El lado total es x + {2 * a}: área = (x + {2 * a})² = {ans}."
    else:
        fig = sq_fig(str(a))
        stem = f"{subj} tiene lado (x + {a}) metros, como muestra la figura. ¿Qué expresión representa su área?"
        ans = sq_exp(1, a)
        alts = [f"x² + {a * a}", co(1, "x²", True) + co(a, "x", False) + co(a * a, "", False), f"2x + {2 * a}", co(1, "x²", True) + co(2 * a, "x", False) + co(a, "", False), f"x² + {a}x"]
        ex = f"Área = (x + {a})² = x² + {2 * a}x + {a * a}."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_frame(r, l):
    a = r.randint(1, 3)
    csubj, mn_art, mn = r.choice(MARC)
    un = r.choice(["cm", "m"]) if l else "cm"
    ext = f"x + {2 * a}"
    body = R(90, 20, 300, 220, FILL2, NAVY, 3) + R(90 + 24 * a, 20 + 24 * a, 300 - 48 * a, 220 - 48 * a, FILL, NAVY, 3) + T(240, 135, "interior", 20) + tag(240, 250, ext, 16)
    fig = wrap(560, 270, body, "Marco alrededor de una superficie")
    stem = f"{csubj} de lado x {un} tiene {mn_art} de {a} {un} de ancho por todos sus lados. ¿Qué expresión representa el área del {mn} solamente?"
    ans = co(4 * a, "x", True) + co(4 * a * a, "", False)
    alts = [co(4 * a, "x", True), co(4 * a * a, "", True), co(2 * a, "x", True) + co(a * a, "", False), sq_exp(1, 2 * a), co(4 * a, "x", True) + co(2 * a * a, "", False)]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Marco = (x + {2 * a})² − x² = {ans}.")


def t_swap(r, l):
    a = r.randint(2, 9)
    # suma por diferencia: rectángulo modificado
    body = R(80, 30, 160, 160, FILL, NAVY, 3) + T(160, 118, "x²", 26) + tag(160, 205, "x", 16) + tag(60, 110, "x", 16)
    body += R(300, 30, 160 + 0, 160, "#F1F5F9", NAVY, 3) + tag(380, 205, "x + a", 16)
    fig = card(["Un cuadrado de lado x se transforma en un rectángulo:", f"un lado aumenta {a} cm y el otro disminuye {a} cm"], 150, 18)
    stem = f"Un cuadrado de lado x cm se transforma en un rectángulo: un lado aumenta {a} cm y el otro disminuye {a} cm. ¿Qué expresión representa el área del rectángulo?"
    ans = f"x² − {a * a}"
    alts = [f"x² + {a * a}", f"x² − {2 * a}x + {a * a}", f"x² − {a}", f"(x − {a})²".replace("(", "(").replace(")", ")"), f"x² + {2 * a}x − {a * a}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"(x + {a})(x − {a}) = x² − {a * a}: el área disminuye respecto del cuadrado original.")


# ---------------------------------------------------------------- Representar
def t_area_read(r, l):
    a = r.randint(2, 12)
    v = r.choice("xmnt")
    fig = sq_fig(str(a), v)
    kind = r.choice(["read", "total"])
    if kind == "read":
        stem = f"La figura muestra un cuadrado de lado ({v} + {a}) dividido en cuatro regiones. ¿Qué expresión representa el área total sumando las cuatro regiones?"
        ans = sq_exp(1, a, v)
        alts = [f"{v}² + {a * a}", co(1, v + "²", True) + co(a, v, False) + co(a * a, "", False), f"{v}² + {2 * a}{v}", f"{v}² + {a}{v} + {a * a}"]
        ex = f"Suma de regiones: {v}² + {a}{v} + {a}{v} + {a}² = ({v} + {a})²."
    else:
        stem = f"En la figura, ¿qué producto notable representa el área total del cuadrado de lado ({v} + {a})?"
        ans = f"({v} + {a})²"
        alts = [f"{v}² + {a}²", f"({v}² + {a})", f"{v} + {a}²", f"2({v} + {a})"]
        ex = "El área de un cuadrado es el cuadrado de su lado."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, ex)


def t_cut_square(r, l):
    a = r.randint(1, 9)
    v = r.choice("xmnt")
    k = min(a, 4)
    body = R(90, 20, 240, 240, FILL2, NAVY, 3) + R(90, 20, 240 - 24 * k, 240 - 24 * k, FILL, NAVY, 3) + T(190 - 12 * k, 150 - 12 * k, f"({v} − {a})²", 20)
    body += tag(210 - 12 * k, 275, f"{v} − {a}", 16) + tag(350, 130, f"{a}", 16) + tag(210, 10, v, 16)
    fig = wrap(560, 300, body, "Cuadrado de lado v con un cuadrado interior de lado v − a")
    stem = f"En la figura, el cuadrado interior tiene lado ({v} − {a}). ¿Qué expresión representa su área desarrollada?"
    ans = sq_exp(1, -a, v)
    alts = [f"{v}² − {a * a}", co(1, v + "²", True) + co(-2 * a, v, False) + co(-a * a, "", False), f"{v}² − {a}{v} + {a * a}", f"{v}² − {2 * a}{v}", f"{v}² + {2 * a}{v} + {a * a}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"({v} − {a})² = {v}² − {2 * a}{v} + {a * a}.")


def t_verbal(r, l):
    A, B = r.choice([("a", "b"), ("m", "n"), ("p", "q"), ("x", "y"), ("u", "v"), ("r", "s")])
    forms = [("El cuadrado de la suma de §A y §B", "(§A + §B)²", ["§A² + §B²", "§A + §B²", "2(§A + §B)", "§A² + 2§B"]), ("El cuadrado de la diferencia entre §A y §B", "(§A − §B)²", ["§A² − §B²", "§A − §B²", "2(§A − §B)", "§A² − 2§B"]),
             ("La suma de los cuadrados de §A y §B", "§A² + §B²", ["(§A + §B)²", "§A + §B²", "§A² + 2§A§B + §B²", "2§A + 2§B"]), ("El producto de la suma por la diferencia de §A y §B", "(§A + §B)(§A − §B)", ["§A² + §B²", "(§A + §B)²", "(§A − §B)²", "§A² − 2§A§B + §B²"]),
             ("La diferencia de los cuadrados de §A y §B", "§A² − §B²", ["(§A − §B)²", "§A − §B²", "§A² + §B²", "(§A − §B)(§A − §B)"]),
             ("El cuadrado del doble de §A, aumentado en §B", "(2§A)² + §B", ["2§A² + §B", "(2§A + §B)²", "2(§A² + §B)", "4§A + §B"]),
             ("El doble del cuadrado de §A, disminuido en §B", "2§A² − §B", ["(2§A)² − §B", "(2§A − §B)²", "2(§A² − §B)", "2§A − §B²"])]
    text, ans, alts = r.choice(forms)
    sub = lambda t: t.replace("§A", A).replace("§B", B)
    fig = card(["Enunciado:", sub(text)], 130, 19)
    return make("¿Qué expresión algebraica representa el enunciado de la figura?", fig, sub(ans), [sub(x) for x in alts], Q_REP, "Se traduce cada frase respetando qué se eleva al cuadrado y qué se agrupa.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.sample(range(2, 9), 2)
    if k == 0:
        return [f"(x + {a})² = x² + {a * a}"], "Omitió el doble producto: (x + a)² = x² + 2ax + a²", \
            [f"Multiplicó el binomio por {a} en lugar de elevarlo al cuadrado por completo", "Elevó al cuadrado solo el segundo término y dejó la variable sin elevar", "Sumó los cuadrados y luego los multiplicó por dos en el último paso", "Restó el cuadrado del segundo término en lugar de sumarlo al primero"]
    if k == 1:
        return [f"(x − {a})² = x² − {a * a}"], "Aplicó la fórmula de suma por diferencia: el cuadrado de una resta tiene término central −2ax y último término +a²", \
            ["Cambió el signo del último término pero olvidó el doble producto central", "Restó el cuadrado de cada término por separado sin incluir el producto", "Multiplicó ambos términos por dos antes de elevarlos al cuadrado", "Sumó los términos del binomio antes de elevar y luego los restó"]
    if k == 2:
        return [f"(x + {a})(x − {a}) = x² + {a * a}"], "Puso signo positivo al último término: en suma por diferencia el resultado es x² − a²", \
            ["Desarrolló como cuadrado de binomio y agregó un doble producto central", "Multiplicó solo los primeros términos y luego sumó los segundos entre sí", "Cambió el signo del primer término en lugar del signo del segundo término", "Restó los términos de cada binomio antes de multiplicarlos entre sí"]
    if k == 3:
        return [f"(2x + {a})² = 4x² + {a * a}"], "Omitió el doble producto 2·(2x)·a y solo elevó al cuadrado cada término del binomio", \
            [f"Elevó al cuadrado solo el número {a} y dejó la variable con su coeficiente", f"Multiplicó el binomio por dos en lugar de elevarlo al cuadrado", "Elevó al cuadrado el coeficiente de x pero no la variable en el primer término", "Sumó el doble producto pero olvidó elevar al cuadrado el último término"]
    return [f"(x + {a})² = (x + {a})(x + {a}) = x² + {a}x + {a}"], f"Multiplicó cada término solo una vez: al distribuir aparecen dos términos {a}x y un término {a * a}", \
        ["Distribuyó bien los términos pero sumó los dos productos cruzados como uno solo", "Multiplicó solo los términos de la primera posición de cada binomio entre sí", "Elevó al cuadrado el segundo término pero lo dejó fuera del resultado final", "Sumó los dos binomios en lugar de multiplicarlos entre sí para desarrollarlos"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equal(r, l):
    a = r.randint(2, 9)
    good = [f"(x + {a})(x + {a})", f"x² + {2 * a}x + {a * a}", f"x² + {a * a} + {2 * a}x", f"x(x + {a}) + {a}(x + {a})"]
    bad = r.choice([f"x² + {a * a}", f"x² + {a}x + {a * a}", f"x² + {2 * a}x + {a}", f"x² + {2 * a}x − {a * a}"])
    fig = card(["Expresión:", f"(x + {a})²"], 130, 24)
    return make("¿Cuál de las siguientes expresiones NO es equivalente a la expresión de la figura?", fig, bad, good, Q_ARG, f"(x + {a})² = x² + {2 * a}x + {a * a}.")


TRUE = ["(a + b)² es igual a a² + 2ab + b²", "(a − b)² es igual a a² − 2ab + b²", "(a + b)(a − b) es igual a a² − b²", "(a + b)² y (−a − b)² son expresiones equivalentes", "Si a = 0, entonces (a + b)² = a² + b²", "(a − b)² nunca es negativo para números reales a y b"]
FALSE = ["(a + b)² es igual a a² + b² para cualesquiera a y b", "(a − b)² es igual a a² − b²", "(a + b)(a − b) es igual a a² + b²", "(a − b)² y (a + b)² son siempre iguales entre sí", "(a + b)² es igual a a² + ab + b²", "(a − b)² puede ser negativo si b es mayor que a"]


def _fig(r):
    return card(["Productos notables", "(a ± b)² = a² ± 2ab + b²  ·  (a + b)(a − b) = a² − b²"], 130, 17)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre productos notables es verdadera?", "Sobre cuadrados de binomio y suma por diferencia, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las fórmulas de productos notables.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre productos notables es falsa?", "Sobre cuadrados de binomio y suma por diferencia, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las fórmulas de productos notables.")


BY_SKILL = {
    Q_RES: [t_expand, t_numeric, t_complete],
    Q_MOD: [t_garden, t_frame, t_swap],
    Q_REP: [t_area_read, t_cut_square, t_verbal],
    Q_ARG: [t_error, t_not_equal, t_true, t_false],
}
