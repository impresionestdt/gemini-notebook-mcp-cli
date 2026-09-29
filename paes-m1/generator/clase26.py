"""Clase 26 (M1) · Función cuadrática II: vértice, máximos, mínimos y optimización."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co
from clase25 import quad, qf, pair, parab_plot, M, rr
import viz


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def gen(r, l, signs=(1, -1)):
    a = r.choice(signs) * r.choice([1, 2] if l else [1])
    h = rr(r, -5, 6)
    k = r.randint(-8, 9)
    b, c = -2 * a * h, a * h * h + k
    return a, b, c, h, k


# ---------------------------------------------------------------- Resolver problemas
def t_vertex(r, l):
    a, b, c, h, k = gen(r, l)
    fig = card(["Función:", M(qf(a, b, c))], 130, 24)
    ans = pair(h, k)
    alts = [pair(-h, k), pair(h, -k), pair(2 * h, k), pair(h, c), pair(k, h)]
    return make(M(f"¿Cuáles son las coordenadas del vértice de la parábola {qf(a, b, c)}?"), fig, ans, pick4(ans, uq(ans, [M(x) if isinstance(x, str) else x for x in alts])), Q_RES, M(f"x = −b/(2a) = {h}; f({h}) = {k}."))


def t_extreme_value(r, l):
    a, b, c, h, k = gen(r, l)
    kind = r.choice(["val", "arg"])
    ext = "máximo" if a < 0 else "mínimo"
    fig = card(["Función:", M(qf(a, b, c))], 130, 24)
    if kind == "val":
        stem = f"¿Cuál es el valor {ext} de la función {qf(a, b, c)}?"
        val = k
        alts = [h, c, -k, k + a, k - 1]
    else:
        stem = f"¿Para qué valor de x la función {qf(a, b, c)} alcanza su valor {ext}?"
        val = h
        alts = [-h, k, c, 2 * h, h + 1]
    ans = str(val).replace("-", "−")
    al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != val]
    return make(M(stem), fig, ans, al[:4], Q_RES, M(f"El vértice es ({h}, {k}): el {ext} es {k} y se alcanza en x = {h}."))


def t_concave_value(r, l):
    a, b, c, h, k = gen(r, l)
    xs = [x for x in range(h - 3, h + 4)]
    x = r.choice([x for x in xs if x != h])
    v = a * x * x + b * x + c
    fig = card(["Parábola con vértice " + pair(h, k), f"y ecuación {M(qf(a, b, c))}"], 130, 19)
    ext = "menor" if a > 0 else "mayor"
    stem = f"Una parábola tiene vértice en {pair(h, k)} y su ecuación es {M(qf(a, b, c))}. ¿Cuál es su valor en x = {x}?"
    ans = str(v).replace("-", "−")
    alts = [k, v + a, v - a, a * x * x + c, -v]
    al = [str(t).replace("-", "−") for t in dict.fromkeys(alts) if t != v]
    return make(M(stem), fig, ans, al[:4], Q_RES, M(f"f({x}) = {a}·({x})² + ({b})·({x}) + ({c}) = {v}."))


# ---------------------------------------------------------------- Modelar
def t_projectile(r, l):
    T = r.choice([2, 3, 4, 5, 6])
    hmax = r.choice([10, 20, 30, 45, 60, 80])
    # h(t) = -5(t - T)^2 + hmax con h(0) = hmax - 5 T^2 >= 0
    h0 = hmax - 5 * T * T
    if h0 < 0:
        raise Reject
    b = 10 * T
    fig = card(["Trayectoria de un proyectil:", f"h(t) = −5t² + {b}t" + (f" + {h0}" if h0 else ""), "h en metros, t en segundos"], 170, 19)
    kind = r.choice(["hmax", "tmax"])
    expr = f"h(t) = −5t² + {b}t" + (f" + {h0}" if h0 else "")
    if kind == "hmax":
        stem = f"La altura de un proyectil se modela con {expr} (h en metros, t en segundos). ¿Cuál es la altura máxima que alcanza?"
        val = hmax
        alts = [h0, b, hmax + h0, hmax - 5, 5 * T]
        ans = f"{val} m"
        al = list(dict.fromkeys(f"{x} m" for x in alts if x > 0 and x != val))
        ex = f"t = −b/(2a) = {T}; h({T}) = {hmax}."
    else:
        stem = f"La altura de un proyectil se modela con {expr} (h en metros, t en segundos). ¿En qué instante alcanza su altura máxima?"
        val = T
        alts = [b, 2 * T, T + 1, T - 1 if T > 1 else 7, hmax]
        ans = f"{val} s"
        al = list(dict.fromkeys(f"{x} s" for x in alts if x > 0 and x != val))
        ex = f"t = −{b}/(2·(−5)) = {T}."
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_profit_max(r, l):
    a = r.choice([1, 2, 3])
    q = r.randint(3, 15)
    G = r.randint(20, 150)
    b = 2 * a * q
    c0 = a * q * q - G
    if c0 < 0:
        c0 = -c0
        sign = "−"
    con = a * q * q - G
    expr = "G(x) = " + co(-a, "x²", True) + co(b, "x", False) + co(-con, "", False)
    fig = card(["Ganancia en función de las unidades x:", M(expr)], 150, 19)
    kind = r.choice(["q", "G"])
    if kind == "q":
        stem = f"La ganancia de una empresa (en miles de pesos) al producir x unidades es {expr}. ¿Cuántas unidades debe producir para maximizar su ganancia?"
        val = q
        alts = [b, 2 * q, q + 1, G, q - 1 if q > 1 else q + 3]
        ans = str(val)
        al = [str(x) for x in dict.fromkeys(alts) if x != val and x > 0]
        ex = f"x = −b/(2a) = {q}."
    else:
        stem = f"La ganancia de una empresa (en miles de pesos) al producir x unidades es {expr}. ¿Cuál es la ganancia máxima?"
        val = G
        alts = [q, b, G + a, -con, G - a]
        ans = str(val)
        al = [str(x) for x in dict.fromkeys(alts) if x != val and x > 0]
        ex = f"El vértice está en x = {q} y G({q}) = {G}."
    return make(M(stem), fig, M(ans), [M(x) for x in al[:4]], Q_MOD, M(ex))


def t_fence(r, l):
    L = r.choice([20, 24, 30, 40, 60])
    x = L // 4
    kind = r.choice(["wall", "free"])
    if kind == "wall":
        if L % 4:
            raise Reject
        body = R(140, 40, 260, 120, FILL, NAVY, 3) + L_line() + tag(140, 100, "x", 17) + tag(270, 180, f"{L} − 2x", 17)
        stem = f"Se dispone de {L} m de cerca para cercar un terreno rectangular adosado a un muro (el lado del muro no lleva cerca). Si los dos lados perpendiculares al muro miden x m, ¿qué valor de x maximiza el área?"
        val = L // 4
        alts = [L // 2, L // 4 + 2, L // 3, L, val - 1]
        ans = str(val)
        ex = f"A(x) = x({L} − 2x); el vértice está en x = {L}/4 = {val}."
    else:
        x = L // 4
        if L % 4:
            raise Reject
        body = R(140, 40, 260, 120, FILL, NAVY, 3) + tag(140, 100, "x", 17) + tag(270, 180, f"{L // 2} − x", 17)
        stem = f"Con {L} m de cerca se forma un rectángulo cuyos lados miden x y ({L // 2} − x) metros. ¿Qué valor de x maximiza el área?"
        val = L // 4
        alts = [L // 2, L // 4 + 2, L, L // 3, val - 1]
        ans = str(val)
        ex = f"A(x) = x({L // 2} − x); el vértice está en x = {L // 4}."
    fig = wrap(560, 210, body, "Rectángulo cercado")
    al = [str(t) for t in dict.fromkeys(alts) if t != val and t > 0]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def L_line():
    return L(100, 30, 440, 30, ACC, 5)


# ---------------------------------------------------------------- Representar
def t_graph_vertex(r, l):
    a, b, c, h, k = gen(r, l)
    if abs(k) > 7:
        raise Reject
    p = Plot(560, 300, -6, 6, -8, 8)
    p.axes(2, 2)
    p.curve(lambda x: a * (x - h) ** 2 + k, -6, 6, ACC, 4.5)
    fig = p.svg("Gráfico de una parábola")
    kind = r.choice(["v", "ext"])
    ext = "máximo" if a < 0 else "mínimo"
    if kind == "v":
        stem = "¿Cuáles son las coordenadas del vértice de la parábola del gráfico?"
        ans = pair(h, k)
        alts = [pair(-h, k), pair(h, -k), pair(k, h), pair(h + 1, k), pair(h, k + 1)]
        ex = "El vértice es el punto más alto (o más bajo) de la parábola."
        return make(stem, fig, ans, pick4(ans, uq(ans, [M(x) for x in alts])), Q_REP, ex)
    stem = f"El gráfico muestra una parábola. ¿Cuál es su valor {ext} y en qué valor de x se alcanza?"
    ans = M(f"{k} en x = {h}")
    alts = [f"{h} en x = {k}", f"{-k} en x = {h}", f"{k} en x = {-h}", f"{k + 1} en x = {h}", f"{k} en x = {h + 1}"]
    al = uq(ans, [M(x) for x in alts])
    return make(stem, fig, ans, al[:4], Q_REP, f"El {ext} corresponde a la ordenada del vértice.")


def t_graph_traj(r, l):
    T = r.choice([1, 2, 3, 4])
    H = r.choice([10, 20, 30, 40])
    a = -H / (T * T)
    p = Plot(560, 300, 0, 2 * T + 1, 0, 50)
    p.axes(1 if T < 4 else 2, 10)
    p.curve(lambda t: max(H - H * (t - T) ** 2 / (T * T), -1), 0, 2 * T, ACC, 4.5)
    fig = p.svg("Altura de un objeto según el tiempo").replace("</svg>", tag(300, 22, "Altura (m) según el tiempo (s)", 15) + "</svg>")
    kind = r.choice(["max", "when"])
    if kind == "max":
        stem = "El gráfico muestra la altura de un objeto lanzado en función del tiempo. ¿Cuál es la altura máxima alcanzada y en qué instante?"
        ans = f"{H} m a los {T} s"
        alts = [f"{T} m a los {H} s", f"{H} m a los {2 * T} s", f"{H // 2} m a los {T} s", f"{H + 10} m a los {T} s"]
        return make(stem, fig, ans, alts, Q_REP, "El punto más alto de la curva es el vértice.")
    stem = "El gráfico muestra la altura de un objeto lanzado en función del tiempo. ¿En qué instante vuelve al suelo?"
    ans = f"{2 * T} s"
    alts = [f"{T} s", f"{H} s", f"{T + 1} s", f"{3 * T} s"]
    return make(stem, fig, ans, alts, Q_REP, "La curva es simétrica respecto del vértice: el objeto sube y baja en el mismo tiempo.")


def t_table_min(r, l):
    a, b, c, h, k = gen(r, l, (1,)) if r.random() < 0.5 else gen(r, l, (-1,))
    xs = list(range(h - 3, h + 4))
    ys = [a * (x - h) ** 2 + k for x in xs]
    fig = viz.table_fig(["x"] + [str(x).replace("-", "−") for x in xs], [["f(x)"] + [str(y).replace("-", "−") for y in ys]])
    ext = "mínimo" if a > 0 else "máximo"
    kind = r.choice(["x", "val"])
    if kind == "x":
        stem = f"La tabla muestra valores de una función cuadrática. Según la tabla, ¿en qué valor de x se alcanza el valor {ext}?"
        val = h
        alts = [xs[0], xs[-1], k, h + 1, h - 1]
    else:
        stem = f"La tabla muestra valores de una función cuadrática. Según la tabla, ¿cuál es el valor {ext}?"
        val = k
        alts = [h, ys[0], ys[-1], k + a, -k]
    ans = str(val).replace("-", "−")
    al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != val]
    return make(stem, fig, ans, al[:4], Q_REP, f"Los valores de la tabla son simétricos respecto de x = {h}, donde está el vértice.".replace("-", "−"))


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, h = r.randint(1, 3), r.randint(2, 6)
    b = -2 * a * h
    if k == 0:
        return [f"f(x) = {a}x² − {2 * a * h}x + 5", f"Vértice en x = −b/a = {2 * h}"], f"Usó −b/a en lugar de −b/(2a): la coordenada x del vértice es {h}", \
            [f"Dividió el coeficiente lineal por el término independiente en vez de por 2a", "Cambió el signo del coeficiente lineal pero dividió por el coeficiente equivocado", "Calculó bien la fórmula pero reemplazó b por el término independiente", "Usó la fórmula de las raíces en lugar de la del vértice de la parábola"]
    if k == 1:
        return [f"f(x) = {a}x² − {2 * a * h}x + 5", "«Tiene un máximo porque el término", "independiente es positivo»"], "Como a > 0 la parábola abre hacia arriba: tiene un mínimo, no un máximo", \
            ["Tiene un máximo porque el vértice es el punto más alto de toda parábola", "Tiene un máximo porque el coeficiente lineal es negativo en la ecuación", "No tiene ni máximo ni mínimo porque abre hacia los dos lados del eje", "Tiene un mínimo pero solo si el término independiente es negativo"]
    if k == 2:
        return [f"f(x) = −x² + {2 * h}x", f"«El valor máximo es {h}, porque el vértice está en x = {h}»"], f"Confundió la coordenada x con el valor máximo: el máximo es f({h}) = {h * h}", \
            ["El valor máximo es el coeficiente lineal de la función, que es " + str(2 * h), "El valor máximo es el término independiente, que en este caso es cero", "El valor máximo es la abscisa del vértice dividida por dos", "El valor máximo se obtiene reemplazando x = 0 en la función cuadrática"]
    return [f"h(t) = −5t² + {10 * h}t", f"«La altura máxima ocurre cuando h = 0»"], "Cuando h = 0 el objeto está en el suelo; la altura máxima ocurre en el vértice, t = −b/(2a)", \
        ["La altura máxima ocurre en t = 0, que es el instante en que se lanza", "La altura máxima ocurre cuando t es el mayor valor posible del dominio", "La altura máxima ocurre en el instante en que el objeto toca el suelo", "La altura máxima se obtiene igualando el coeficiente de t² a cero"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 17)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_max_or_min(r, l):
    a, b, c, h, k = gen(r, l)
    fig = card(["Función:", M(qf(a, b, c))], 130, 24)
    ext = "máximo" if a < 0 else "mínimo"
    other = "mínimo" if a < 0 else "máximo"
    ans = f"Tiene un valor {ext}, porque el coeficiente de x² es {'negativo' if a < 0 else 'positivo'}"
    alts = [f"Tiene un valor {other}, porque el coeficiente de x² es {'negativo' if a < 0 else 'positivo'}", f"Tiene un valor {other}, porque el término independiente es {'positivo' if c > 0 else 'negativo'}", "Tiene un valor máximo y un valor mínimo a la vez", "No tiene ni valor máximo ni valor mínimo"]
    return make("¿Qué se puede afirmar sobre los valores extremos de la función de la figura?", fig, ans, alts, Q_ARG, "Si a > 0 la parábola tiene un mínimo en el vértice; si a < 0, un máximo.")


TRUE = ["El vértice de f(x) = ax² + bx + c tiene abscisa x = −b/(2a)", "Si a > 0, el vértice es el punto más bajo de la parábola", "Si a < 0, la función tiene un valor máximo en el vértice",
        "El eje de simetría de la parábola pasa por su vértice", "Para maximizar una ganancia cuadrática con a < 0 se busca el vértice", "El valor máximo de una función cuadrática con a < 0 es la ordenada del vértice"]
FALSE = ["El vértice de f(x) = ax² + bx + c tiene abscisa x = −b/a", "Si a > 0, el vértice es el punto más alto de la parábola", "Si a < 0, la función cuadrática no tiene valor máximo",
         "El eje de simetría de la parábola no pasa por su vértice", "Toda función cuadrática tiene simultáneamente un máximo y un mínimo", "El valor máximo de una función cuadrática es la abscisa del vértice"]


def _fig(r):
    a, b, c, h, k = gen(r, 1)
    return parab_plot(a, h, k, label_pts=False)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el vértice y los extremos de una parábola es verdadera?", "Sobre optimización con funciones cuadráticas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades del vértice.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el vértice y los extremos de una parábola es falsa?", "Sobre optimización con funciones cuadráticas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades del vértice.")


BY_SKILL = {
    Q_RES: [t_vertex, t_extreme_value, t_concave_value],
    Q_MOD: [t_projectile, t_profit_max, t_fence],
    Q_REP: [t_graph_vertex, t_graph_traj, t_table_min],
    Q_ARG: [t_error, t_max_or_min, t_true, t_false],
}
