"""Clase 25 (M1) · Función cuadrática I: gráfica, concavidad e interceptos."""
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


def M(s):
    return s.replace("-", "−")


def quad(a, b, c, v="x"):
    """a v² + b v + c."""
    return co(a, v + "²", True) + (co(b, v, False) if b else "") + (co(c, "", False) if c else "")


def qf(a, b, c):
    return f"f(x) = {quad(a, b, c)}"


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


def gen_parab(r, l):
    a = r.choice([1, -1, 2, -2]) if l else r.choice([1, -1])
    h = r.randint(-3, 3)
    k = r.randint(-4, 4)
    if abs(a * h * h + k) > 9 or abs(-2 * a * h) > 12:
        raise Reject
    return a, -2 * a * h, a * h * h + k, h, k


# ---------------------------------------------------------------- Resolver problemas
def t_eval(r, l):
    a, b, c = rr(r, -3, 3), rr(r, -5, 5), rr(r, -6, 6)
    x = rr(r, -4, 4)
    v = a * x * x + b * x + c
    fig = card(["Función:", M(qf(a, b, c))], 130, 24)
    alts = [-a * x * x + b * x + c, a * x * x - b * x + c, a * (x * x) + b + c, (a * x) ** 2 + b * x + c, v + c]
    ans = fs(F(v))
    return make(f"Sea {M(qf(a, b, c))}. ¿Cuál es el valor de f({x})?".replace("-", "−") if False else M(f"Sea {qf(a, b, c)}. ¿Cuál es el valor de f({x})?"), fig, ans, pick4(ans, uq(ans, alts)), Q_RES, M(f"f({x}) = {a}·({x})² + ({b})·({x}) + ({c}) = {v}."))


def t_axis_sym(r, l):
    h = r.randint(-3, 5)
    d = r.randint(1, 4)
    a, b, c = rr(r, -2, 2), 0, 0
    k = r.randint(-5, 5)
    v = a * d * d + k
    fig = card([M(f"f({h - d}) = {v}"), M(f"f({h + d}) = {v}"), "f es una función cuadrática"], 170, 21)
    stem = f"Una función cuadrática cumple f({h - d}) = {v} y f({h + d}) = {v}. ¿Cuál es la ecuación del eje de simetría de su gráfico?"
    ans = M(f"x = {h}")
    alts = [f"x = {h + d}", f"x = {h - d}", f"x = {v}", f"x = {d}", f"x = {h + 1}"]
    al = uq(ans, [M(x) for x in alts])
    return make(M(stem), fig, ans, al[:4], Q_RES, f"El eje de simetría pasa por el punto medio: ({h - d} + {h + d})/2 = {h}.".replace("-", "−"))


def t_features(r, l):
    a, b, c = rr(r, -3, 3), rr(r, -5, 5), rr(r, -6, 6)
    fig = card(["Función:", M(qf(a, b, c))], 130, 24)
    kind = r.choice(["conc", "yint"])
    if kind == "conc":
        stem = f"¿Hacia dónde abre la parábola de {M(qf(a, b, c))}?"
        ans = "Hacia arriba, porque el coeficiente de x² es positivo" if a > 0 else "Hacia abajo, porque el coeficiente de x² es negativo"
        alts = ["Hacia abajo, porque el coeficiente de x² es positivo" if a > 0 else "Hacia arriba, porque el coeficiente de x² es negativo", f"Hacia {'arriba' if b > 0 else 'abajo'}, porque el coeficiente de x es {'positivo' if b > 0 else 'negativo'}",
                f"Hacia {'arriba' if c > 0 else 'abajo'}, porque el término independiente es {'positivo' if c > 0 else 'negativo'}", "No abre hacia ningún lado porque no tiene vértice"]
        al = [x for x in alts if x != ans]
        if len(al) < 4:
            raise Reject
        return make(M(stem), fig, ans, al[:4], Q_RES, "El signo del coeficiente de x² determina la concavidad.")
    stem = f"¿En qué punto corta al eje Y la parábola de {M(qf(a, b, c))}?"
    ans = pair(0, c)
    alts = [pair(c, 0), pair(0, b), pair(0, a), pair(0, -c), pair(b, 0)]
    return make(M(stem), fig, ans, pick4(ans, uq(ans, alts)), Q_RES, "Con x = 0, f(0) es el término independiente.")


# ---------------------------------------------------------------- Modelar
def t_ball(r, l):
    v0 = r.choice([10, 15, 20, 25, 30])
    a = 5
    h0 = r.choice([0, 0, 10, 15])
    t = r.randint(1, 3)
    H = h0 + v0 * t - a * t * t
    if H <= 0:
        raise Reject
    fig = card(["Altura de una pelota (metros):", f"h(t) = −5t² + {v0}t" + (f" + {h0}" if h0 else ""), "t en segundos"], 170, 20)
    stem = f"La altura de una pelota se modela con h(t) = −5t² + {v0}t" + (f" + {h0}" if h0 else "") + f", con t en segundos. ¿Cuál es su altura a los {t} segundos?"
    ans = f"{H} m"
    alts = [h0 + v0 * t + a * t * t, h0 + v0 - a * t, v0 * t - a * t, H + a, H - a * 2, (h0 + v0 * t - a) * t]
    al = list(dict.fromkeys(f"{x} m" for x in alts if x > 0 and x != H))
    return make(stem, fig, ans, al[:4], Q_MOD, f"h({t}) = −5·{t}² + {v0}·{t}" + (f" + {h0}" if h0 else "") + f" = {H}.")


def t_area_pair(r, l):
    S = r.choice([10, 12, 14, 16, 20])
    x = r.randint(2, S // 2 - 1)
    fig = card([f"Rectángulo de perímetro {2 * S}", f"Un lado mide x; el otro mide {S} − x"], 130, 20)
    kind = r.choice(["expr", "val"])
    if kind == "expr":
        stem = f"Un rectángulo tiene perímetro {2 * S} cm y un lado de x cm. ¿Qué función representa su área A en función de x?"
        ans = f"A(x) = x({S} − x)"
        alts = [f"A(x) = x({2 * S} − x)", f"A(x) = x + ({S} − x)", f"A(x) = 2x({S} − x)", f"A(x) = x² − {S}"]
        return make(stem, fig, ans, alts, Q_MOD, f"El otro lado es {S} − x (semiperímetro menos x); el área es el producto de los lados.")
    stem = f"El área de un rectángulo de perímetro {2 * S} cm en función de un lado x es A(x) = x({S} − x). ¿Cuál es el área cuando x = {x}?"
    val = x * (S - x)
    ans = f"{val} cm²"
    alts = [x + (S - x), x * S - x, 2 * x * (S - x), val + x, val - S]
    al = list(dict.fromkeys(f"{v} cm²" for v in alts if v > 0 and v != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"A({x}) = {x}·({S} − {x}) = {val}.")


def t_profit(r, l):
    p = r.choice([10, 12, 15, 20])
    c1 = r.choice([2, 3, 4, 5])
    cf = r.choice([20, 30, 50, 100])
    n = r.randint(3, 12)
    kind = r.choice(["expr", "val"])
    fig = card([f"Venta: {p} por unidad, cantidad x", f"Costo: {cf} fijos + {c1}x² total"], 130, 19)
    if kind == "expr":
        stem = f"Una empresa vende x unidades a ${p} cada una y su costo total es {cf} + {c1}x². ¿Qué función representa su ganancia G(x)?"
        ans = f"G(x) = −{c1}x² + {p}x − {cf}"
        alts = [f"G(x) = {c1}x² + {p}x − {cf}", f"G(x) = −{c1}x² + {p}x + {cf}", f"G(x) = {c1}x² − {p}x + {cf}", f"G(x) = −{c1}x² − {p}x − {cf}"]
        return make(stem, fig, M(ans), [M(a) for a in alts], Q_MOD, "Ganancia = ingresos − costos = px − (c₀ + c₁x²).")
    G = p * n - cf - c1 * n * n
    stem = f"Una empresa vende x unidades a ${p} cada una y su costo total es {cf} + {c1}x². ¿Cuál es su ganancia si vende {n} unidades?"
    ans = str(G)
    alts = [p * n + cf + c1 * n * n, p * n - cf - c1 * n, G + cf, -G, p * n - cf]
    al = [str(a).replace("-", "−") for a in dict.fromkeys(alts) if a != G]
    return make(stem, fig, str(G).replace("-", "−"), al[:4], Q_MOD, f"G({n}) = {p}·{n} − ({cf} + {c1}·{n}²) = {G}.".replace("-", "−"))


# ---------------------------------------------------------------- Representar
def parab_plot(a, h, k, label_pts=True):
    p = Plot(560, 300, -6, 6, -8, 8)
    p.axes(2, 2)
    p.curve(lambda x: a * (x - h) ** 2 + k, -6, 6, ACC, 4.5)
    if label_pts:
        for x in (h - 1, h, h + 1):
            y = a * (x - h) ** 2 + k
            if -8 <= y <= 8:
                if x == h:
                    p.pt(x, y, pair(x, y), 0, 30 if a > 0 else -30)
                else:
                    p.pt(x, y, pair(x, y), -58 if x < h else 58, -14 if a > 0 else 14)
    return p.svg("Gráfico de una parábola")


def t_equation_from_graph(r, l):
    a, b, c, h, k = gen_parab(r, l)
    fig = parab_plot(a, h, k)
    ans = M(qf(a, b, c))
    alts = [qf(-a, b, c), qf(a, -b, c), qf(a, b, -c), qf(a, b, k), qf(a, 2 * b, c)]
    al = uq(ans, [M(x) for x in alts])
    if len(al) < 4:
        raise Reject
    return make("El gráfico muestra una parábola con tres de sus puntos. ¿Cuál es la ecuación de la función?", fig, ans, al[:4], Q_REP, f"Vértice ({h}, {k}) y a = {a}: f(x) = {a}(x − {h})² + {k} = {ans[7:]}.".replace("-", "−"))


def t_read_features(r, l):
    a, b, c, h, k = gen_parab(r, l)
    fig = parab_plot(a, h, k)
    conc = "arriba" if a > 0 else "abajo"
    other = "abajo" if a > 0 else "arriba"
    ans = f"Abre hacia {conc}, su eje de simetría es x = {h} y corta al eje Y en (0, {c})"
    alts = [f"Abre hacia {other}, su eje de simetría es x = {h} y corta al eje Y en (0, {c})", f"Abre hacia {conc}, su eje de simetría es x = {-h} y corta al eje Y en (0, {c})", f"Abre hacia {conc}, su eje de simetría es x = {h} y corta al eje Y en (0, {k})",
            f"Abre hacia {conc}, su eje de simetría es x = {h} y corta al eje X en ({c}, 0)"]
    if h == 0:
        alts[1] = f"Abre hacia {conc}, su eje de simetría es x = {k} y corta al eje Y en (0, {c})"
    if k == c:
        alts[2] = f"Abre hacia {conc}, su eje de simetría es x = {h} y corta al eje Y en (0, {c + 1})"
    if h == 0 and False:
        raise Reject
    al = uq(M(ans), [M(x) for x in alts])
    if len(al) < 4:
        raise Reject
    return make("¿Cuál de las siguientes afirmaciones describe correctamente la parábola del gráfico?", fig, M(ans), al[:4], Q_REP, "Se leen la concavidad, la recta vertical que pasa por el vértice y el corte con el eje Y.")


def t_table_sym(r, l):
    h = r.randint(-1, 3)
    a = rr(r, -2, 2)
    k = r.randint(-4, 5)
    xs = [h - 3, h - 2, h - 1, h, h + 1, h + 2, h + 3]
    ys = [a * (x - h) ** 2 + k for x in xs]
    hide = r.choice([0, 1, 2, 4, 5, 6])
    shown = [str(y).replace("-", "−") if i != hide else "?" for i, y in enumerate(ys)]
    fig = viz.table_fig(["x"] + [str(x).replace("-", "−") for x in xs], [["f(x)"] + shown])
    ans = str(ys[hide]).replace("-", "−")
    mirror = 2 * (len(xs) // 2) - hide
    alts = [ys[hide] + 1, ys[hide] - 1, ys[3], -ys[hide], ys[hide] + a]
    al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != ys[hide]]
    stem = "La tabla muestra valores de una función cuadrática con un dato oculto. Usando la simetría de la parábola, ¿qué valor corresponde a «?»"
    return make(stem, fig, ans, al[:4], Q_REP, f"Los valores de x equidistantes de x = {h} tienen la misma imagen: {ans}.".replace("-", "−"))


# ---------------------------------------------------------------- Argumentar
def t_wider(r, l):
    a = r.sample([F(1, 2), F(1, 3), 1, 2, 3, F(-1, 2), -1, -2, -3, F(-1, 3)], 5)
    eqs = [("y = " + ("−" if v < 0 else "") + (fs(abs(F(v))) if abs(F(v)) != 1 else "") + "x²").replace("y = 1/2x²", "y = x²/2").replace("y = −1/2x²", "y = −x²/2").replace("y = 1/3x²", "y = x²/3").replace("y = −1/3x²", "y = −x²/3") for v in a]
    kind = r.choice(["narrow", "wide"])
    vals = [abs(F(v)) for v in a]
    if len(set(vals)) < 5:
        raise Reject
    idx = max(range(5), key=lambda i: vals[i]) if kind == "narrow" else min(range(5), key=lambda i: vals[i])
    fig = card(["Parábolas y = ax²", "Mayor |a| → más estrecha"], 130, 22)
    stem = f"Se comparan cinco parábolas de la forma y = ax². ¿Cuál de ellas es la más {'estrecha' if kind == 'narrow' else 'ancha'}?"
    ans = eqs[idx]
    al = [e for i, e in enumerate(eqs) if i != idx]
    return make(stem, fig, ans, al, Q_ARG, "Mientras mayor es el valor absoluto de a, más se cierra la parábola; mientras menor, más se abre.")


def _err(r):
    k = r.randrange(4)
    c = r.randint(2, 9)
    if k == 0:
        return [f"f(x) = −x² + {c}", "«Abre hacia arriba porque el término", "independiente es positivo»"], "La concavidad depende del coeficiente de x², que aquí es −1: la parábola abre hacia abajo", \
            ["La parábola abre hacia arriba porque el coeficiente del término lineal es cero", "La concavidad depende del término independiente, por lo que abre hacia arriba", "La parábola no tiene concavidad porque solo tiene dos términos en su ecuación", "La parábola abre hacia abajo porque el término independiente es positivo"]
    if k == 1:
        return [f"f(x) = x² − {c}x + {c * 2}", f"«Corta al eje Y en (−{c}, 0)»"], f"El corte con el eje Y es (0, f(0)) = (0, {c * 2}): el coeficiente de x no es una coordenada del corte", \
            [f"Corta al eje Y en (0, −{c}) porque se toma el coeficiente del término lineal", f"Corta al eje Y en ({c * 2}, 0) porque se invierten las coordenadas del punto", f"Corta al eje Y en (0, 1) porque es el coeficiente del término cuadrático", "No corta al eje Y porque la parábola tiene concavidad hacia arriba"]
    if k == 2:
        return [f"f(x) = x² + {c}", f"«Corta al eje X en x = ±{c}»"], f"Con x = ±{c} resulta f(x) = {c * c + c} ≠ 0: la parábola abre hacia arriba y está sobre el eje X, por lo que no lo corta", \
            [f"Corta al eje X en x = ±{c}, porque las raíces son los valores de la constante", f"Corta al eje X solo en x = {c}, porque la parábola es simétrica respecto de él", "Corta al eje X en el origen porque el término lineal es cero siempre", f"Corta al eje X en x = −{c}, porque la constante cambia de signo"]
    return ["Dos puntos de una parábola: (1, 4) y (5, 4)", "«El eje de simetría es x = 4»"], "El eje de simetría pasa por el punto medio de x = 1 y x = 5, es decir x = 3, no por el valor de y", \
        ["El eje de simetría es x = 5 porque es la coordenada mayor de los dos puntos", "El eje de simetría es x = 1 porque es la coordenada menor de los dos puntos", "No existe eje de simetría porque los dos puntos tienen la misma ordenada", "El eje de simetría es x = 9 porque es la suma de las abscisas"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["Si el coeficiente de x² es positivo, la parábola abre hacia arriba", "El gráfico de una función cuadrática es simétrico respecto de una recta vertical", "En f(x) = ax² + bx + c, la parábola corta al eje Y en (0, c)",
        "Si a < 0, la parábola abre hacia abajo", "Dos puntos de una parábola con la misma altura son simétricos respecto del eje de simetría", "En y = ax², mientras mayor es |a|, más estrecha es la parábola"]
FALSE = ["Si el coeficiente de x² es positivo, la parábola abre hacia abajo", "El gráfico de una función cuadrática es una recta", "En f(x) = ax² + bx + c, la parábola corta al eje Y en (c, 0)",
         "Si a < 0, la parábola abre hacia arriba", "El eje de simetría de una parábola siempre es el eje Y", "En y = ax², mientras mayor es |a|, más ancha es la parábola"]


def _fig(r):
    a, b, c, h, k = gen_parab(r, 1)
    return parab_plot(a, h, k, label_pts=False)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones cuadráticas es verdadera?", "Sobre la parábola y su gráfico, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de la parábola.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre funciones cuadráticas es falsa?", "Sobre la parábola y su gráfico, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de la parábola.")


BY_SKILL = {
    Q_RES: [t_eval, t_axis_sym, t_features],
    Q_MOD: [t_ball, t_area_pair, t_profit],
    Q_REP: [t_equation_from_graph, t_read_features, t_table_sym],
    Q_ARG: [t_wider, t_error, t_true, t_false],
}
