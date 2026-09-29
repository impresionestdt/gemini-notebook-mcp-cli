"""Clase 27 (M1) · Ecuación cuadrática: intersecciones con el eje X e interpretación de raíces."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
from clase25 import quad, pair, M, rr
import viz


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        if a not in seen:
            seen.add(a); out.append(a)
    return out


def roots_txt(m, n):
    if m == n:
        return M(f"x = {m}")
    lo, hi = sorted((m, n))
    return M(f"x = {lo} y x = {hi}")


def eq0(a, b, c, v="x"):
    return f"{quad(a, b, c, v)} = 0"


# ---------------------------------------------------------------- Resolver problemas
def t_solve(r, l):
    m, n = rr(r, -7, 8), rr(r, -7, 8)
    if m == n:
        raise Reject
    a = 1 if l < 2 else r.choice([2, 3])
    b, c = -a * (m + n), a * m * n
    if l == 0:
        fac = f"(x {'−' if m > 0 else '+'} {abs(m)})(x {'−' if n > 0 else '+'} {abs(n)}) = 0"
        disp = fac
    else:
        disp = eq0(a, b, c)
    fig = card(["Resuelve la ecuación:", M(disp)], 130, 22)
    ans = roots_txt(m, n)
    alts = [roots_txt(-m, -n), roots_txt(m, -n), roots_txt(-m, n), roots_txt(m + 1, n), roots_txt(m, n + 1), roots_txt(m + n, m * n)]
    al = uq(ans, alts)
    return make("¿Cuál es el conjunto solución de la ecuación de la figura?", fig, ans, al[:4], Q_RES, M(f"Las soluciones son x = {m} y x = {n}."))


def t_discriminant(r, l):
    a = rr(r, -3, 3)
    b = rr(r, -8, 8)
    c = rr(r, -8, 8)
    D = b * b - 4 * a * c
    fig = card(["Ecuación:", M(eq0(a, b, c)), M(f"Δ = b² − 4ac")], 170, 22)
    kind = r.choice(["D", "n"])
    if kind == "D":
        stem = f"Para la ecuación {M(eq0(a, b, c))}, ¿cuál es el valor del discriminante Δ = b² − 4ac?"
        ans = str(D).replace("-", "−")
        alts = [b * b + 4 * a * c, b * b - 2 * a * c, -b * b - 4 * a * c, b - 4 * a * c, D + 4]
        al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != D]
        return make(M(stem), fig, ans, al[:4], Q_RES, M(f"Δ = ({b})² − 4·({a})·({c}) = {D}."))
    n = 2 if D > 0 else 1 if D == 0 else 0
    stem = f"¿Cuántas soluciones reales tiene la ecuación {M(eq0(a, b, c))}?"
    ans = str(n)
    al = [str(x) for x in (0, 1, 2, 3, 4) if x != n][:4]
    return make(M(stem), fig, ans, al, Q_RES, f"Δ = {D}: {'dos soluciones' if D > 0 else 'una solución' if D == 0 else 'ninguna solución real'}.".replace("-", "−"))


def t_from_roots(r, l):
    m, n = rr(r, -6, 7), rr(r, -6, 7)
    if m == n:
        raise Reject
    fig = card(["Una ecuación cuadrática tiene", M(f"soluciones x = {m} y x = {n}")], 130, 21)
    ans = M(eq0(1, -(m + n), m * n))
    alts = [eq0(1, m + n, m * n), eq0(1, -(m + n), -m * n), eq0(1, m + n, -m * n), eq0(1, -(m * n), m + n), eq0(1, -(m + n), m * n + 1)]
    al = uq(ans, [M(x) for x in alts])
    return make("¿Cuál es una ecuación cuadrática con las soluciones de la figura?", fig, ans, al[:4], Q_RES, M(f"(x − {m})(x − {n}) = 0 se desarrolla como {ans}."))


# ---------------------------------------------------------------- Modelar
def t_ground(r, l):
    T = r.choice([2, 3, 4, 5, 6])
    v0 = 5 * T
    h0 = 0
    fig = card(["Altura de una pelota (m):", f"h(t) = −5t² + {5 * T}t", "t en segundos"], 150, 21)
    stem = f"La altura de una pelota se modela con h(t) = −5t² + {5 * T}t (h en metros, t en segundos desde el lanzamiento). ¿Después de cuántos segundos vuelve al suelo?"
    ans = f"{T} s"
    alts = [f"0 s", f"{T // 2 if T % 2 == 0 else T + 1} s", f"{5 * T} s", f"{T + 1} s", f"{2 * T} s"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"h(t) = 0 ⟹ 5t(−t + {T}) = 0 ⟹ t = 0 (lanzamiento) o t = {T}: vuelve al suelo a los {T} s.")


def t_rect_area(r, l):
    k = r.randint(1, 6)
    x = r.randint(2, 9)
    A = x * (x + k)
    body = R(140, 40, 260, 110, FILL, NAVY, 3) + tag(270, 165, f"x + {k}", 18) + tag(110, 95, "x", 18) + T(270, 105, f"Área = {A}", 22)
    fig = wrap(560, 200, body, "Rectángulo de lados x y x + k")
    stem = f"Un rectángulo tiene lados de x cm y (x + {k}) cm y su área es {A} cm². ¿Cuánto mide el lado menor?"
    ans = f"{x} cm"
    alts = [f"{x + k} cm", f"{-(x + k)} cm".replace("-", "−"), f"{A - k} cm", f"{x + 1} cm", f"{k} cm"]
    al = [t for t in dict.fromkeys(alts) if t != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"x(x + {k}) = {A} ⟹ x² + {k}x − {A} = 0 ⟹ x = {x} (la solución negativa no sirve como longitud).")


def t_numbers(r, l):
    x = r.randint(3, 15)
    P = x * (x + 1)
    fig = card(["Dos números enteros consecutivos", f"positivos tienen producto {P}"], 130, 21)
    stem = f"El producto de dos números enteros consecutivos positivos es {P}. ¿Cuál es la suma de ambos números?"
    val = 2 * x + 1
    ans = str(val)
    alts = [x + 1, x * 2, P, val + 2, val - 2]
    al = [str(t) for t in dict.fromkeys(alts) if t != val and t > 0]
    return make(stem, fig, ans, al[:4], Q_MOD, f"x(x + 1) = {P} ⟹ x = {x}; los números son {x} y {x + 1}: suman {val}.")


# ---------------------------------------------------------------- Representar
def t_graph_roots(r, l):
    m, n = sorted(r.sample(range(-5, 6), 2))
    if n - m < 2:
        raise Reject
    a = r.choice([1, -1])
    p = Plot(560, 300, -6, 6, -10, 10)
    p.axes(2, 2)
    p.curve(lambda x: a * (x - m) * (x - n), -6, 6, ACC, 4.5)
    fig = p.svg("Gráfico de una parábola")
    kind = r.choice(["roots", "eq"])
    if kind == "roots":
        stem = "La parábola del gráfico es la función f. ¿Cuáles son las soluciones de la ecuación f(x) = 0?"
        ans = roots_txt(m, n)
        alts = [roots_txt(-m, -n), roots_txt(m, -n), roots_txt(m + n, m * n), roots_txt(m - 1, n + 1), roots_txt(0, m + n)]
        al = uq(ans, alts)
        return make(stem, fig, ans, al[:4], Q_REP, "Las soluciones de f(x) = 0 son las abscisas de los puntos donde la parábola corta al eje X.")
    stem = "La parábola del gráfico corta al eje X en dos puntos. ¿Cuál es su ecuación?"
    ans = M(f"f(x) = {quad(a, -a * (m + n), a * m * n)}")
    alts = [f"f(x) = {quad(a, a * (m + n), a * m * n)}", f"f(x) = {quad(-a, -a * (m + n), a * m * n)}", f"f(x) = {quad(a, -a * (m + n), -a * m * n)}", f"f(x) = {quad(a, -a * (m - n), a * m * n)}", f"f(x) = {quad(a, -a * (m + n), a * (m + n))}"]
    al = uq(ans, [M(x) for x in alts])
    if len(al) < 4:
        raise Reject
    return make(stem, fig, ans, al[:4], Q_REP, M(f"f(x) = {a}(x − {m})(x − {n}) = {ans[7:]}."))


def t_graph_count(r, l):
    a = r.choice([1, -1])
    kind = r.choice([2, 1, 0])
    h = r.randint(-3, 3)
    if kind == 2:
        k = -a * r.randint(1, 4)
    elif kind == 1:
        k = 0
    else:
        k = a * r.randint(1, 4)
    p = Plot(560, 300, -6, 6, -8, 8)
    p.axes(2, 2)
    p.curve(lambda x: a * (x - h) ** 2 + k, -6, 6, ACC, 4.5)
    fig = p.svg("Gráfico de una parábola")
    stem = "La parábola del gráfico representa una función f. ¿Cuántas soluciones reales tiene la ecuación f(x) = 0?"
    ans = {2: "Dos soluciones reales distintas", 1: "Exactamente una solución real", 0: "Ninguna solución real"}[kind]
    opts = ["Dos soluciones reales distintas", "Exactamente una solución real", "Ninguna solución real", "Infinitas soluciones reales", "Tres soluciones reales"]
    return make(stem, fig, ans, [o for o in opts if o != ans], Q_REP, "Las soluciones son los cortes con el eje X: dos, uno (tangente) o ninguno.")


def t_table_zero(r, l):
    m, n = sorted(r.sample(range(-3, 6), 2))
    if n - m < 2:
        raise Reject
    xs = list(range(min(m, n) - 2, max(m, n) + 3))
    ys = [(x - m) * (x - n) for x in xs]
    fig = viz.table_fig(["x"] + [str(x).replace("-", "−") for x in xs], [["f(x)"] + [str(y).replace("-", "−") for y in ys]])
    stem = "La tabla muestra valores de una función cuadrática f. Según la tabla, ¿cuáles son las soluciones de f(x) = 0?"
    ans = roots_txt(m, n)
    alts = [roots_txt(-m, -n), roots_txt(m, n + 1), roots_txt(m - 1, n), roots_txt(0, m + n), roots_txt(m + 1, n - 1)]
    al = uq(ans, alts)
    return make(stem, fig, ans, al[:4], Q_REP, "Se buscan los valores de x cuya imagen es 0.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 6), r.randint(1, 6)
    if a == b:
        b += 1
    if k == 0:
        return [f"(x − {a})(x + {b}) = 0", f"x = −{a}  o  x = {b}"], "Cambió el signo de las dos soluciones: (x − a)(x + b) = 0 tiene soluciones x = a y x = −b", \
            ["Igualó a cero solo el primer factor y descartó la solución del segundo", "Sumó los números de los factores para obtener una única solución", "Multiplicó los números de los factores para obtener las soluciones", "Escribió las soluciones correctas pero intercambió su orden en el resultado"]
    if k == 1:
        return [f"x² − {a}x = 0", f"x(x − {a}) = 0  →  x = {a}"], "Perdió la solución x = 0: si un producto es cero, cada factor puede ser cero, incluido x", \
            ["Dividió ambos lados por x y no verificó si x = 0 también era solución", "Sumó las dos soluciones en lugar de escribirlas por separado en la respuesta", "Igualó el segundo factor a cero pero cambió el signo de la solución obtenida", "Consideró que x = 0 no puede ser solución de ninguna ecuación cuadrática"]
    if k == 2:
        return [f"(x − 1)(x − 2) = 6", "x − 1 = 6  o  x − 2 = 6"], "Solo se puede igualar cada factor a cero cuando el producto es cero: aquí primero hay que llevar la ecuación a la forma = 0", \
            ["Debió igualar el producto a 1 antes de separar los dos factores de la ecuación", "Debió dividir por seis cada factor antes de separarlos y resolver cada uno", "Igualó bien los factores a seis pero debió sumar las dos soluciones halladas", "Debió multiplicar los dos factores por seis antes de plantear las soluciones"]
    return [f"x² = {a * a}", f"x = {a}"], f"Omitió la solución negativa: x² = {a * a} tiene dos soluciones, x = {a} y x = −{a}", \
        [f"Debió dividir {a * a} por dos para encontrar el valor de x que cumple", "Debió sumar 1 a la solución encontrada antes de escribirla como respuesta", f"Debió escribir x = {a * a} porque no se puede sacar raíz a los dos lados", "Debió escribir dos soluciones iguales porque la ecuación es de segundo grado"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_valid_root(r, l):
    k = r.randint(1, 6)
    x = r.randint(2, 9)
    A = x * (x + k)
    fig = card([f"x(x + {k}) = {A}", M(f"Soluciones: x = {x} y x = {-(x + k)}"), "x es la medida de un lado en cm"], 170, 19)
    stem = f"Al resolver el problema de un rectángulo de lados x y (x + {k}) con área {A} cm², se obtienen las soluciones x = {x} y x = {-(x + k)}. ¿Qué solución es válida para la medida del lado y por qué?".replace("-", "−")
    ans = f"x = {x}, porque una longitud no puede ser negativa".replace("-", "−")
    alts = [f"x = {-(x + k)}, porque es la solución de mayor valor absoluto".replace("-", "−"), "Ambas, porque las dos cumplen la ecuación cuadrática planteada", f"Ninguna, porque el área no puede ser {A} cm²", f"x = {x}, porque es la solución que se obtiene primero"]
    return make(stem, fig, ans, alts, Q_ARG, "Toda solución debe interpretarse en el contexto: una longitud es positiva.")


def t_discr_claim(r, l):
    a, b, c = r.choice([(1, 2, 1), (1, 4, 4), (2, 4, 2), (1, 6, 9)]) if r.random() < 0.4 else (rr(r, 1, 3), r.randint(-2, 2), rr(r, 1, 5))
    D = b * b - 4 * a * c
    n = 2 if D > 0 else 1 if D == 0 else 0
    fig = card(["Ecuación:", M(eq0(a, b, c))], 130, 22)
    ans = {2: f"Tiene dos soluciones reales distintas, porque Δ = {D} es positivo", 1: "Tiene una solución real doble, porque Δ = 0", 0: f"No tiene soluciones reales, porque Δ = {D} es negativo"}[n]
    opts = [f"Tiene dos soluciones reales distintas, porque Δ = {D} es positivo", "Tiene una solución real doble, porque Δ = 0", f"No tiene soluciones reales, porque Δ = {D} es negativo"]
    alts = [o for o in opts if o != ans] + [f"Tiene dos soluciones reales, porque el coeficiente de x² es {'positivo' if a > 0 else 'negativo'}", "Tiene infinitas soluciones, porque es una ecuación de segundo grado"]
    alts = [M(x) for x in alts]
    return make(M("¿Qué se puede afirmar sobre las soluciones de la ecuación de la figura?"), fig, M(ans), alts[:4], Q_ARG, "El signo del discriminante determina la cantidad de soluciones reales.")


TRUE = ["Si un producto de factores es cero, al menos uno de los factores es cero", "Si Δ > 0, la ecuación cuadrática tiene dos soluciones reales distintas", "Las soluciones de f(x) = 0 son las abscisas de los cortes de la parábola con el eje X",
        "Si Δ < 0, la parábola no corta al eje X", "Si Δ = 0, la parábola toca al eje X en un solo punto", "x² = 25 tiene dos soluciones: x = 5 y x = −5"]
FALSE = ["Si un producto de factores es 6, uno de los factores debe ser 6", "Si Δ < 0, la ecuación cuadrática tiene dos soluciones reales distintas", "Las soluciones de f(x) = 0 son las ordenadas de los cortes con el eje X",
         "Si Δ > 0, la parábola no corta al eje X", "Si Δ = 0, la ecuación cuadrática no tiene soluciones", "x² = 25 tiene una única solución: x = 5"]


def _fig(r):
    m, n = sorted(r.sample(range(-4, 5), 2))
    p = Plot(560, 260, -6, 6, -8, 8)
    p.axes(2, 2)
    p.curve(lambda x: (x - m) * (x - n), -6, 6, ACC, 4.5)
    return p.svg("Gráfico de una parábola")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ecuaciones cuadráticas es verdadera?", "Sobre soluciones y discriminante, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la propiedad del producto nulo y el discriminante.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ecuaciones cuadráticas es falsa?", "Sobre soluciones y discriminante, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las ecuaciones cuadráticas.")


BY_SKILL = {
    Q_RES: [t_solve, t_discriminant, t_from_roots],
    Q_MOD: [t_ground, t_rect_area, t_numbers],
    Q_REP: [t_graph_roots, t_graph_count, t_table_zero],
    Q_ARG: [t_error, t_valid_root, t_discr_claim, t_true, t_false],
}
