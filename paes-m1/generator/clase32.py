"""Clase 32 (M1) · Teorema de Pitágoras: tríos pitagóricos y distancias."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import tri_sides
from mathfmt import E, fmt, sqfree


TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10)]


def triple(r, l):
    a, b, c = r.choice(TRIP[:4] if l == 0 else TRIP)
    k = r.choice([1, 1, 2, 3] if l < 2 else [1, 2, 3, 4, 5])
    return a * k, b * k, c * k


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else str(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def sq(n):
    return f"√{n}" if n > 0 else "0"


def root_txt(n):
    """√n simplificada: 2√3, √13, 5."""
    return fmt(E((1, n)))


# ---------------------------------------------------------------- Resolver problemas
def t_pyth(r, l):
    if l == 2 and r.random() < 0.5:
        a, b = r.randint(2, 9), r.randint(2, 9)
        if math.isqrt(a * a + b * b) ** 2 == a * a + b * b:
            raise Reject
        c2 = a * a + b * b
        fig = tri_sides(math.sqrt(c2), b, a, {"c": str(a), "b": str(b), "a": "x"}, right="A")
        stem = f"En un triángulo rectángulo, los catetos miden {a} y {b}. ¿Cuánto mide la hipotenusa x?"
        ans = root_txt(c2)
        alts = [str(a + b), root_txt(abs(a * a - b * b)) if a != b else "0", str(c2), root_txt(c2 + 1), str(a * b)]
        return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, f"x² = {a}² + {b}² = {c2}, luego x = {ans}.")
    a, b, c = triple(r, l)
    kind = r.choice(["hyp", "leg"])
    if kind == "hyp":
        fig = tri_sides(c, b, a, {"c": str(a), "b": str(b), "a": "x"}, right="A")
        stem = f"En el triángulo rectángulo de la figura, los catetos miden {a} y {b}. ¿Cuánto mide la hipotenusa x?"
        val = c
        alts = [a + b, c + 1, c - 1, b - a if b != a else c + 2, a * b // 2]
        ex = f"x² = {a}² + {b}² = {a * a + b * b} ⟹ x = {c}."
    else:
        fig = tri_sides(c, b, a, {"c": str(a), "b": "x", "a": str(c)}, right="A")
        stem = f"En el triángulo rectángulo de la figura, la hipotenusa mide {c} y un cateto mide {a}. ¿Cuánto mide el otro cateto x?"
        val = b
        alts = [c - a, c + a, b + 1, b - 1, math.isqrt(c * c + a * a) if False else c * a // 2]
        ex = f"x² = {c}² − {a}² = {c * c - a * a} ⟹ x = {b}."
    ans = str(val)
    al = [x for x in dict.fromkeys(str(t) for t in alts if t > 0 and t != val)]
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_diag(r, l):
    a, b, c = triple(r, l)
    kind = r.choice(["rect", "sq"])
    if kind == "rect":
        body = R(140, 40, 260, 120, FILL, NAVY, 3) + L(140, 160, 400, 40, ACC, 4) + tag(270, 180, f"{a} cm", 17) + tag(112, 100, f"{b} cm", 17) + tag(290, 92, "d", 17)
        fig = wrap(560, 210, body, "Rectángulo con su diagonal")
        stem = f"Un rectángulo mide {a} cm de largo y {b} cm de ancho. ¿Cuánto mide su diagonal?"
        val = c
        alts = [a + b, c + 2, a * b, c - 1, F(a * b, 2)]
        ex = f"d² = {a}² + {b}² = {c * c} ⟹ d = {c} cm."
        ans = f"{val} cm"
        al = list(dict.fromkeys(f"{fs(F(t))} cm" for t in alts if F(t) > 0 and F(t) != val))
        return make(stem, fig, ans, al[:4], Q_RES, ex)
    s = r.randint(2, 12)
    body = R(190, 30, 150, 150, FILL, NAVY, 3) + L(190, 180, 340, 30, ACC, 4) + tag(265, 200, f"{s} cm", 17) + tag(285, 100, "d", 17)
    fig = wrap(560, 230, body, "Cuadrado con su diagonal")
    stem = f"Un cuadrado tiene lados de {s} cm. ¿Cuánto mide su diagonal?"
    ans = f"{s}√2 cm"
    alts = [f"{2 * s} cm", f"{s}√3 cm", f"{s * s}√2 cm", f"√{s} cm", f"{2 * s}√2 cm"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"d² = {s}² + {s}² = {2 * s * s} ⟹ d = {s}√2.")


def t_height_iso(r, l):
    m, h, s = r.choice([(3, 4, 5), (5, 12, 13), (4, 3, 5), (12, 5, 13), (6, 8, 10), (8, 6, 10)])
    k = r.choice([1, 2])
    m, h, s = m * k, h * k, s * k
    body = P([(120, 200), (440, 200), (280, 40)], FILL) + L(280, 40, 280, 200, ACC, 4, "9 6") + tag(200, 120, str(s), 16) + tag(360, 120, str(s), 16) + tag(200, 222, str(m), 16) + tag(360, 222, str(m), 16) + tag(300, 120, "h", 16)
    fig = wrap(560, 250, body, "Triángulo isósceles con su altura")
    stem = f"Un triángulo isósceles tiene lados iguales de {s} cm y base de {2 * m} cm. ¿Cuánto mide su altura sobre la base?"
    ans = f"{h} cm"
    alts = [f"{s - m} cm", f"{s + m} cm", f"{h + 1} cm", f"{m} cm", f"{2 * m} cm"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_RES, f"La altura divide la base en dos partes de {m}: h² = {s}² − {m}² = {h * h}.")


# ---------------------------------------------------------------- Modelar
def t_ladder(r, l):
    a, b, c = triple(r, 0)
    kind = r.choice(["height", "dist"])
    body = L(80, 220, 480, 220, INK, 4) + L(80, 220, 80, 40, INK, 4) + L(80, 60, 300, 220, ACC, 5)
    if kind == "height":
        body += tag(190, 232, f"{a} m", 16) + tag(190, 130, f"{c} m", 16) + tag(50, 130, "h", 16)
        stem = f"Una escalera de {c} m se apoya en un muro vertical con su base a {a} m del muro. ¿A qué altura del muro llega la parte superior de la escalera?"
        val = b
        alts = [a + c, c - a, b + 2, a * 2, c + 1]
    else:
        body += tag(190, 232, "d", 16) + tag(190, 130, f"{c} m", 16) + tag(50, 130, f"{b} m", 16)
        stem = f"Una escalera de {c} m llega a {b} m de altura en un muro vertical. ¿A qué distancia del muro está la base de la escalera?"
        val = a
        alts = [c - b, b + c, a + 2, b - 1, c + a]
    fig = wrap(560, 260, body, "Escalera apoyada en un muro")
    ans = f"{val} m"
    al = list(dict.fromkeys(f"{t} m" for t in alts if t > 0 and t != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Muro, suelo y escalera forman un triángulo rectángulo: {a}² + {b}² = {c}².")


def t_walk(r, l):
    a, b, c = triple(r, l)
    body = L(100, 200, 100 + 4 * a * 400 / max(a, b) / 4, 200, ACC, 5) if False else ""
    W = 320
    H = 320 * b / max(a, b) * 0.6
    body = L(100, 210, 100 + W, 210, ACC, 5) + L(100 + W, 210, 100 + W, 210 - H, ACC, 5) + L(100, 210, 100 + W, 210 - H, NAVY, 4, "9 6")
    body += tag(100 + W / 2, 235, f"{a} m al este", 16) + tag(100 + W + 60, 210 - H / 2, f"{b} m al norte", 16) + tag(100 + W / 2 - 30, 210 - H / 2 - 22, "d", 16)
    fig = wrap(560, 250, body, "Recorrido hacia el este y luego hacia el norte")
    stem = f"Una persona camina {a} m hacia el este y luego {b} m hacia el norte. ¿A qué distancia en línea recta está del punto de partida?"
    ans = f"{c} m"
    alts = [f"{a + b} m", f"{c + 1} m", f"{abs(b - a)} m", f"{c - 1} m", f"{a * b // 2} m"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"d² = {a}² + {b}² = {c * c} ⟹ d = {c} m.")


def t_shortcut(r, l):
    a, b, c = triple(r, 0)
    fig = card([f"Cancha rectangular: {a} m × {b} m", "Se puede ir por los bordes o en diagonal"], 130, 19)
    stem = f"Una cancha rectangular mide {a} m de largo y {b} m de ancho. ¿Cuántos metros se ahorran al ir en diagonal de una esquina a la opuesta en lugar de ir por los bordes?"
    val = a + b - c
    ans = f"{val} m"
    alts = [c, a + b, a + b + c, val + 2, abs(a - b)]
    al = list(dict.fromkeys(f"{t} m" for t in alts if t > 0 and t != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Por los bordes: {a + b} m; en diagonal: {c} m; se ahorran {val} m.")


# ---------------------------------------------------------------- Representar
def t_relation(r, l):
    a, b, c = triple(r, l)
    fig = tri_sides(c, b, a, {"c": str(a), "b": str(b), "a": str(c)}, right="A")
    ans = f"{a}² + {b}² = {c}²"
    alts = [f"{a}² + {c}² = {b}²", f"{b}² + {c}² = {a}²", f"{a} + {b} = {c}", f"{a}² − {b}² = {c}²"]
    return make("El triángulo de la figura es rectángulo en A. ¿Cuál de las siguientes igualdades relaciona correctamente las medidas de sus lados?", fig, ans, alts, Q_REP, "El cuadrado de la hipotenusa (lado opuesto al ángulo recto) es la suma de los cuadrados de los catetos.")


def t_is_right(r, l):
    a, b, c = r.choice(TRIP)
    ok = r.random() < 0.5
    if ok:
        sides = (a, b, c)
    else:
        d = r.choice([1, -1])
        sides = (a, b, c + d)
        if math.isqrt(a * a + b * b) ** 2 == sides[0] ** 2 + sides[1] ** 2 or sides[2] <= 0:
            raise Reject
    s = sorted(sides)
    if s[0] + s[1] <= s[2]:
        raise Reject
    fig = tri_sides(s[2], s[1], s[0], {"c": str(s[0]), "b": str(s[1]), "a": str(s[2])})
    isr = s[0] ** 2 + s[1] ** 2 == s[2] ** 2
    stem = f"El triángulo de la figura tiene lados de {s[0]}, {s[1]} y {s[2]} unidades. ¿Es un triángulo rectángulo?"
    if isr:
        ans = f"Sí, porque {s[0]}² + {s[1]}² = {s[2]}²"
        alts = [f"No, porque {s[0]} + {s[1]} ≠ {s[2]}", f"Sí, porque {s[0]} + {s[1]} > {s[2]}", f"No, porque {s[0]}² + {s[1]}² ≠ {s[2]}²", f"Sí, porque los tres lados son distintos"]
    else:
        ans = f"No, porque {s[0]}² + {s[1]}² = {s[0] ** 2 + s[1] ** 2}, distinto de {s[2]}² = {s[2] ** 2}"
        alts = [f"Sí, porque {s[0]}² + {s[1]}² = {s[2]}²", f"Sí, porque {s[0]} + {s[1]} > {s[2]}", f"No, porque los tres lados son distintos entre sí", f"Sí, porque el mayor de los lados es menor que la suma de los otros dos"]
    return make(stem, fig, ans, alts, Q_REP, "Un triángulo es rectángulo si y solo si el cuadrado del mayor lado es igual a la suma de los cuadrados de los otros dos.")


def t_grid(r, l):
    a, b, c = r.choice(TRIP[:2])
    x1, y1 = r.randint(-4, 0), r.randint(-4, 0)
    x2, y2 = x1 + a, y1 + b
    if x2 > 5 or y2 > 5 or abs(x1) > 6:
        raise Reject
    p = Plot(560, 300, -6, 6, -6, 6)
    p.axes(2, 2)
    p.parts.append(L(p.X(x1), p.Y(y1), p.X(x2), p.Y(y1), NAVY, 3, "8 6") + L(p.X(x2), p.Y(y1), p.X(x2), p.Y(y2), NAVY, 3, "8 6") + L(p.X(x1), p.Y(y1), p.X(x2), p.Y(y2), ACC, 4.5))
    p.pt(x1, y1, f"A({x1}, {y1})".replace("-", "−"), 0, 24)
    p.pt(x2, y2, f"B({x2}, {y2})".replace("-", "−"), 0, -24)
    fig = p.svg("Segmento AB en el plano cartesiano")
    stem = "En el plano cartesiano, ¿cuál es la distancia entre los puntos A y B?"
    ans = str(c)
    alts = [a + b, c + 1, c - 1, b - a if b != a else c + 2, a * b // 2]
    al = [x for x in dict.fromkeys(str(t) for t in alts if t > 0 and t != c)]
    return make(stem, fig, ans, al[:4], Q_REP, f"Los catetos miden {a} y {b} (diferencias de coordenadas): d = {c}.")


# ---------------------------------------------------------------- Argumentar
def t_which_triple(r, l):
    a, b, c = r.choice(TRIP)
    k = r.choice([1, 1, 2])
    good = f"{a * k}, {b * k} y {c * k}"
    bads = set()
    while len(bads) < 4:
        d = r.choice([(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0), (0, 0, -1), (-1, 0, 1)])
        x = (a * k + d[0], b * k + d[1], c * k + d[2])
        if x[0] > 0 and x[1] > 0 and x[2] > 0 and x[0] ** 2 + x[1] ** 2 != x[2] ** 2 and sorted(x) == list(x) is False or (x[0] ** 2 + x[1] ** 2 != x[2] ** 2 and x[2] > 0):
            bads.add(f"{x[0]}, {x[1]} y {x[2]}")
    fig = card(["Se buscan las medidas de los lados", "de un triángulo rectángulo"], 130, 20)
    return make("¿Cuál de las siguientes ternas puede corresponder a las medidas de los lados de un triángulo rectángulo?", fig, good, list(bads)[:4], Q_ARG, f"Solo {good} cumple a² + b² = c²: {(a * k) ** 2} + {(b * k) ** 2} = {(c * k) ** 2}.")


def _err(r):
    k = r.randrange(4)
    a, b, c = r.choice(TRIP[:3])
    if k == 0:
        return [f"Catetos {a} y {b}", f"Hipotenusa = {a} + {b} = {a + b}"], "Sumó los catetos: la hipotenusa se obtiene sumando sus cuadrados y sacando raíz cuadrada", \
            ["Multiplicó los catetos entre sí en lugar de sumar sus cuadrados y sacar raíz", "Restó los catetos entre sí y usó el resultado como hipotenusa del triángulo", "Sumó los cuadrados de los catetos pero no sacó la raíz cuadrada del resultado", "Usó el mayor de los catetos como si fuera la hipotenusa del triángulo"]
    if k == 1:
        return [f"Hipotenusa {c}, cateto {a}", f"Otro cateto = √({c}² + {a}²)"], "Sumó los cuadrados: para hallar un cateto se resta el cuadrado del cateto conocido al de la hipotenusa", \
            ["Restó los cuadrados en orden inverso y obtuvo un radicando negativo al final", "Sumó los lados sin elevar al cuadrado y luego sacó raíz cuadrada del total", "Dividió la hipotenusa por el cateto conocido para hallar el cateto faltante", "Aplicó la fórmula de la hipotenusa a los dos lados dados sin distinguirlos"]
    if k == 2:
        return [f"Catetos {a} y {b}", f"Hipotenusa = {a}² + {b}² = {c * c}"], f"Olvidó sacar la raíz cuadrada: {a}² + {b}² = {c * c} es el cuadrado de la hipotenusa, que mide {c}", \
            ["Debió restar los cuadrados de los catetos antes de sacar la raíz cuadrada", "Debió sumar los catetos sin elevarlos al cuadrado y luego dividir por dos", "Debió dividir por dos la suma de los cuadrados para obtener la hipotenusa", "Debió multiplicar los cuadrados de los catetos en lugar de sumarlos entre sí"]
    return [f"Lados {a}, {b} y {c + 1}", "«Es rectángulo porque 3 + 4 > 5»"], "Que la suma de dos lados supere al tercero solo asegura que el triángulo existe; para que sea rectángulo debe cumplirse a² + b² = c²", \
        ["Es rectángulo porque los tres lados son números enteros consecutivos", "Es rectángulo porque el mayor de los lados es menor que la suma de los otros", "No es rectángulo porque la suma de los dos lados menores es mayor que el tercero", "Es rectángulo siempre que la suma de dos lados supere al tercer lado"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["En un triángulo rectángulo, la hipotenusa es el lado más largo", "Si a² + b² = c², el triángulo de lados a, b y c es rectángulo", "3, 4 y 5 son las medidas de los lados de un triángulo rectángulo",
        "La diagonal de un cuadrado de lado a mide a√2", "La hipotenusa es el lado opuesto al ángulo recto", "Los tríos pitagóricos se pueden multiplicar por un número y siguen siéndolo"]
FALSE = ["En un triángulo rectángulo, la hipotenusa es la suma de los catetos", "Si a + b = c, el triángulo de lados a, b y c es rectángulo", "2, 3 y 4 son las medidas de los lados de un triángulo rectángulo",
         "La diagonal de un cuadrado de lado a mide 2a", "La hipotenusa es el lado más corto de un triángulo rectángulo", "El teorema de Pitágoras vale para cualquier tipo de triángulo"]


def _fig(r):
    a, b, c = r.choice(TRIP[:3])
    return tri_sides(c, b, a, {"c": "a", "b": "b", "a": "c"}, right="A")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el teorema de Pitágoras es verdadera?", "Sobre triángulos rectángulos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el teorema de Pitágoras y su recíproco.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el teorema de Pitágoras es falsa?", "Sobre triángulos rectángulos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el teorema de Pitágoras.")


BY_SKILL = {
    Q_RES: [t_pyth, t_diag, t_height_iso],
    Q_MOD: [t_ladder, t_walk, t_shortcut],
    Q_REP: [t_relation, t_is_right, t_grid],
    Q_ARG: [t_which_triple, t_error, t_true, t_false],
}
