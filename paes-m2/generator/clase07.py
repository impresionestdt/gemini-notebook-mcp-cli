"""Clase 7 · Función potencia: gráficas, paridad y traslaciones."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO

SUP = str.maketrans("0123456789-−", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁻")


def sup(n):
    return str(n).translate(SUP)


def ft(n, a=1, h=0, k=0):
    """Texto de a·(x − h)^n + k (exponentes negativos como cociente)."""
    m = abs(n)
    base = "x" if h == 0 else f"(x {'−' if h > 0 else '+'} {abs(h)})"
    if n > 0:
        pw = base if m == 1 else base + sup(m)
        if m == 1 and h != 0 and a == 1:
            pw = base[1:-1]
        pre = "" if a == 1 else "−" if a == -1 else str(a)
        body = pre + pw
    else:
        pw = base if m == 1 else base + sup(m)
        body = ("−" if a < 0 else "") + str(abs(a)) + "/" + pw
    if k > 0: body += f" + {k}"
    elif k < 0: body += f" − {abs(k)}"
    return body


def legend(pl, items):
    y = pl.h - pl.mb - 20 - 30 * (len(items) - 1)
    x = pl.w - pl.mr - 200
    for c, t in items:
        pl.parts.append(f'<rect x="{x}" y="{y - 12}" width="190" height="26" rx="6" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/>'
                        + L(x + 6, y + 1, x + 36, y + 1, c, 4) + T(x + 44, y + 6, t, 15, "start"))
        y += 30


def plot(f, x0, x1, y0, y1, marks=(), extra=None, sx=1, sy=1, color=ACC):
    pl = Plot(560, 280, x0, x1, y0, y1)
    pl.axes(sx, sy)
    if extra: extra(pl)
    pl.curve(f, x0, x1, color)
    for (x, y, lab, dx, dy) in marks:
        pl.pt(x, y, lab, dx=dx, dy=dy)
    return pl


def pw(x, n):
    try:
        return F(x) ** n
    except ZeroDivisionError:
        return F(0)


# ---------------------------------------------------------------- Resolver
def t_find_k(r, l):
    if l == 0:
        n, k, p = r.choice([2, 3]), r.randint(2, 7), r.choice([2, 3, -2])
        q = k * F(p) ** n
        cands = [F(q, p), F(q, n), q - p, F(q, p * p) if n == 3 else F(q, p ** 3), q, k + 1]
        ans, stem, kind = k, f"La función f(x) = k·x{sup(n)} pasa por el punto ({p}, {fs(q)}). ¿Cuál es el valor de k?", 1
    elif l == 1:
        n, k, p = r.choice([-1, -2]), r.choice([2, 3, 4, 6, 8, 12]), r.choice([2, 3, 4, -2, -3])
        q = k * F(p) ** n
        cands = [q * p, q * p * p, F(q, p), q * abs(p) ** 2, -k, k + 1, q]
        ans = k
        stem = f"La función f(x) = k/x{sup(-n) if n != -1 else ''} pasa por el punto ({p}, {fs(q)}). ¿Cuál es el valor de k?"
    else:
        n = r.choice([-4, -3, -2, -1, 2, 3, 4, 5])
        p = r.choice([2, -2, 3, -3]) if abs(n) <= 3 else r.choice([2, -2])
        q = F(p) ** n
        cands = [-n, n + 1, n - 1, abs(n) + 1, F(q), 2 * n, n + 2 if n > 0 else n - 2]
        ans = n
        stem = f"La función f(x) = xⁿ, con n entero, pasa por el punto ({p}, {fs(q)}). ¿Cuál es el valor de n?"
    fq = float(q)
    ymax = max(4, abs(fq) * 1.3) if abs(fq) < 60 else 12
    pl = plot(lambda x: float(ans) * x ** n if l < 2 and False else (float(ans) * float(F(x).limit_denominator(10 ** 6)) ** n if l < 2 else x ** n), -4, 4, -ymax, ymax, [(p, fq, f"({p}, {fs(q)})", 0, -28)], sy=max(1, round(ymax / 5)))
    ex = f"Se reemplaza el punto: {fs(q)} = k·({p}){sup(n)} ⟹ k = {fs(ans)}." if l < 2 else f"({p}){sup(n)} = {fs(q)} ⟹ n = {n}."
    return make(stem, pl.svg("Gráfico con el punto dado"), fs(ans), pick4(fs(ans), [fs(c) for c in cands]), Q_RES, ex)


def t_intersect(r, l):
    if l == 0:
        n, m = r.choice([(2, 1), (3, 1), (4, 2), (3, 2), (4, 1)])
    elif l == 1:
        n, m = r.choice([(2, -1), (3, -1), (1, -1), (2, -2), (3, -3), (4, -2), (2, -3), (1, -2)])
    else:
        n, m = r.sample([-3, -2, -1, 1, 2, 3, 4, 5], 2)
    if n == m: raise Reject
    d = abs(n - m)
    xs = ([-1, 1] if d % 2 == 0 else [1]) + ([0] if n > 0 and m > 0 else [])
    xs = sorted(xs)
    pts = [(x, F(x) ** n) for x in xs]
    ps = lambda L_: ", ".join(f"({fs(x)}, {fs(y)})" for x, y in L_)
    ans = ps(pts)
    cands = []
    if len(pts) > 1:
        cands.append(ps([p for p in pts if p[0] != 0]) if any(p[0] == 0 for p in pts) else ps(pts[:-1]))
        cands.append(ps(pts[1:]))
    cands.append(ps([(x, -abs(y)) if x < 0 else (x, y) for x, y in pts]))
    cands.append(ps([(x, y) for x, y in pts if x != 1] + [(2, F(2) ** n)]) if len(pts) > 1 else ps(pts + [(0, 0)]))
    cands.append(ps(sorted(set(pts + [(0, F(0))])) if not any(p[0] == 0 for p in pts) and n > 0 and m > 0 else pts + [(-1, F(-1) ** n * -1)]))
    cands.append(ps([(-x, y) for x, y in pts] if any(x != -x for x, _ in pts) and len(pts) == 1 else [(x, y + 1) for x, y in pts]))
    cands.append(ps([(x, F(x) ** m + 1) for x, _ in pts]))
    cands = [c for c in dict.fromkeys(cands) if c != ans]
    f1, f2 = (lambda x: x ** n), (lambda x: x ** m)
    pl = plot(f1, -3, 3, -6, 6, extra=lambda p: p.curve(f2, -3, 3, NAVY), sx=1, sy=2)
    legend(pl, [(ACC, f"y = {ft(n)}"), (NAVY, f"y = {ft(m)}")])
    return make(f"Se grafican y = {ft(n)} (rojo) e y = {ft(m)} (azul). ¿En qué puntos se intersectan sus gráficas?", pl.svg("Dos funciones potencia"), ans, pick4(ans, cands), Q_RES,
                f"{ft(n)} = {ft(m)} ⟹ x^({n - m}) = 1 (si x ≠ 0), y se revisa x = 0 cuando ambos exponentes son positivos.")


# ---------------------------------------------------------------- Modelar
def solid(k, n):
    body = ""
    if n == 2:
        body += R(60, 130, 40, 40, FILL) + R(200, 130 - 0, 40 * k, 40 * k, FILL2) if False else R(60, 190 - 40, 40, 40, FILL) + R(200, 190 - 40 * k, 40 * k, 40 * k, FILL2)
    else:
        for (x0, s, fill) in ((60, 40, FILL), (200, 40 * k, FILL2)):
            d = s * 0.35
            body += (R(x0, 190 - s, s, s, fill) + P([(x0, 190 - s), (x0 + d, 190 - s - d), (x0 + s + d, 190 - s - d), (x0 + s, 190 - s)], FILL3)
                     + P([(x0 + s, 190 - s), (x0 + s + d, 190 - s - d), (x0 + s + d, 190 - d), (x0 + s, 190)], "#BFDBFE"))
    body += tag(80, 218, "lado L", 15) + tag(200 + 20 * k, 218, f"lado {k}L", 15)
    return wrap(560, 240, body, "Figuras semejantes")


def discs(k):
    rr = min(k, 4)
    body = C(110, 150, 22, FILL, NAVY, 4) + C(330, 150, 22 * rr, FILL2, NAVY, 4) + tag(110, 200, "radio r", 15) + tag(330, 200 + 0, f"radio {k}r", 15)
    return wrap(560, 240, body, "Dos círculos de radios distintos")


SHAPES = [("el lado de un cuadrado", "el área del cuadrado", 2, "sq"), ("el lado de un cubo", "el volumen del cubo", 3, "cu"),
          ("el radio de un círculo", "el área del círculo", 2, "ci"), ("el radio de una esfera", "el volumen de la esfera", 3, "ci")]
INV = ["la intensidad de la luz de una lámpara", "la intensidad de un sonido", "la fuerza de atracción gravitacional entre dos cuerpos", "la intensidad de la señal de una antena"]


def t_scale(r, l):
    if l == 0:
        k = r.choice([2, 3, 4, 5, 6, 10])
        who, what, n, fig_ = r.choice(SHAPES)
        verb = {2: "duplica", 3: "triplica", 4: "cuadruplica", 5: "quintuplica", 6: "sextuplica", 10: "multiplica por 10"}[k]
        stem = f"Si se {verb} {who}, ¿cuántas veces mayor queda {what}?"
        ans = f"{k ** n} veces"
        cands = [f"{k} veces", f"{k * n} veces", f"{k ** (5 - n)} veces" if k ** (5 - n) != k ** n else f"{k + n} veces", f"{n ** k} veces" if n ** k != k ** n else f"{k + 1} veces", f"{k ** n + k} veces", f"{k ** n // 2} veces"]
        fig = discs(k) if fig_ == "ci" else solid(min(k, 4), n)
        ex = f"{what.capitalize()} es proporcional a la potencia {n} de la medida: {k}{sup(n)} = {k**n}."
    elif l == 1:
        k = r.choice([2, 3, 4, 5, 10])
        who = r.choice(INV)
        shrink = r.random() < 0.4
        if not shrink:
            stem = f"{who.capitalize()} es inversamente proporcional al cuadrado de la distancia a la fuente. Si la distancia se multiplica por {k}, ¿qué ocurre?"
            ans = f"Queda 1/{k * k} de la inicial"
            cands = [f"Queda 1/{k} de la inicial", f"Queda 1/{2 * k} de la inicial", f"Se multiplica por {k * k}", f"Queda 1/{k ** 3} de la inicial", f"Se multiplica por {k}"]
            ex = f"I ∝ 1/d²: con distancia {k}d, I' = I/{k}² = I/{k*k}."
            body = C(70, 120, 16, FILL2, INK, 3) + L(86, 120, 250, 120, ACC, 4) + tag(160, 95, "d", 16) + L(86, 150, 470, 150, NAVY, 4) + tag(280, 180, f"{k}d", 16)
        else:
            stem = f"{who.capitalize()} es inversamente proporcional al cuadrado de la distancia a la fuente. Si la distancia se reduce a la {k}-ésima parte, ¿qué ocurre?".replace("a la 2-ésima parte", "a la mitad").replace("a la 3-ésima parte", "a la tercera parte").replace("a la 4-ésima parte", "a la cuarta parte").replace("a la 5-ésima parte", "a la quinta parte").replace("a la 10-ésima parte", "a la décima parte")
            ans = f"Se multiplica por {k * k}"
            cands = [f"Se multiplica por {k}", f"Queda 1/{k * k} de la inicial", f"Se multiplica por {2 * k}", f"Se multiplica por {k ** 3}", f"Queda 1/{k} de la inicial"]
            ex = f"I ∝ 1/d²: con distancia d/{k}, I' = {k}²·I = {k*k}·I."
            body = C(70, 120, 16, FILL2, INK, 3) + L(86, 120, 470, 120, ACC, 4) + tag(280, 95, "d", 16) + L(86, 150, 250, 150, NAVY, 4) + tag(170, 180, f"d/{k}", 16)
        fig = wrap(560, 210, body, "Fuente y dos distancias")
    else:
        n = r.choice([2, 3])
        p = r.choice([10, 20, 30, 50, -10, -20, -30, -40])
        f = (1 + F(p, 100)) ** n
        pct = (f - 1) * 100
        what = "el área de un cuadrado" if n == 2 else "el volumen de un cubo"
        stem = f"El lado de un {'cuadrado' if n == 2 else 'cubo'} {'aumenta' if p > 0 else 'disminuye'} un {abs(p)}%. ¿Qué ocurre con {what}?"
        alt = lambda v: f"{'Aumenta' if v > 0 else 'Disminuye'} {abs(float(v)):g}%".replace(".", ",")
        ans = alt(pct)
        cands = [alt(n * p), alt(p), alt(-pct), alt(F(p * (n + 1))), alt(pct + (5 if pct > 0 else -5)), alt(p * n // 2 + 3)]
        fig = solid(2, n).replace("lado 2L", f"lado {100 + p}%")
        ex = f"Factor = {(100 + p) / 100:g}{sup(n)} = {float(f):g}, o sea {ans.lower()}.".replace(".", ",", 0)
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


def table_fig(xs, ys, qx):
    n = len(xs) + 1
    w = 500 / (n + 1)
    body = R(30, 50, 500, 50, "#E0F2FE") + R(30, 100, 500, 50, WHITE)
    body += T(30 + w / 2, 83, "x", 22) + T(30 + w / 2, 133, "y", 22)
    for i, (x, y) in enumerate(zip(xs, ys)):
        body += T(30 + w * (i + 1.5), 83, fs(x), 20) + T(30 + w * (i + 1.5), 133, fs(y), 20)
    body += R(30 + w * n, 50, w, 100, FILL2) + T(30 + w * (n + 0.5), 83, fs(qx), 20) + T(30 + w * (n + 0.5), 133, "?", 22)
    for i in range(n + 2):
        body += L(30 + w * i, 50, 30 + w * i, 150, NAVY, 2)
    return wrap(560, 190, body, "Tabla de valores")


def t_table(r, l):
    if l == 0:
        n, k, q = 2, r.randint(2, 9), r.choice([4, 5, 6])
        xs = [1, 2, 3]
    elif l == 1:
        n = r.choice([3, -1])
        k = r.randint(2, 9) if n > 0 else r.choice([2, 3, 4, 5, 6, 8, 12])
        xs, q = ([1, 2, 3], r.choice([4, 5])) if n > 0 else ([1, 2, 4], r.choice([5, 8, 10]))
    else:
        n = r.choice([3, -2, 4])
        k = r.randint(2, 7)
        xs, q = ([1, 2, 3], r.choice([4, 5])) if n > 0 else ([1, 2, 4], r.choice([5, 8, 10]))
    ys = [k * F(x) ** n for x in xs]
    yq = k * F(q) ** n
    ans = fs(yq)
    lin = ys[-1] + (ys[-1] - ys[-2]) * (q - xs[-1]) / (xs[-1] - xs[-2])
    prop = ys[0] * q
    cands = [fs(lin), fs(prop), fs(k * q), fs(yq + k), fs(k * F(q) ** (n + 1 if n > 0 else n - 1)), fs(yq * 2), fs(k * F(q) ** (abs(n))) if n < 0 else fs(k * F(q) ** (n - 1))]
    stem = f"Los datos de la tabla siguen un modelo de potencia y = k·xⁿ. ¿Cuál es el valor de y cuando x = {q}?"
    return make(stem, table_fig(xs, ys, q), ans, pick4(ans, cands), Q_MOD, f"Con x = 1 se obtiene k = {k}; los cocientes dan n = {n}; luego y = {k}·{q}{sup(n)} = {ans}.")


# ---------------------------------------------------------------- Representar
def t_match(r, l):
    if l == 0:
        pool = [(1, 1), (1, 2), (1, 3), (1, -1)]
    elif l == 1:
        pool = [(1, n) for n in (1, 2, 3, 4, -1, -2, -3, -4)]
    else:
        pool = [(a, n) for a in (1, -1) for n in (1, 2, 3, 4, -1, -2, -3)]
    a, n = r.choice(pool)
    p = r.choice([2, -2, 3, -3]) if n % 2 else r.choice([2, 3])
    q = a * F(p) ** n
    fq = float(q)
    ymax = 6 if abs(fq) <= 5 else min(30, abs(fq) * 1.6)
    f = lambda x: a * x ** n
    pl = plot(f, -4, 4, -ymax, ymax, [(p, fq, f"({p}, {fs(q)})", -50 if fq > 0 else 50, 28 if fq > 0 else -28)], sy=max(1, round(ymax / 5)))
    ans = "f(x) = " + ft(n, a)
    cands = []
    for (a2, n2) in [(a, n + 2 if n > 0 else n - 2), (a, n - 2 if n > 2 else n + 1), (-a, n), (a, -n), (-a, -n), (a, n + 1 if n != -1 else 1), (a, n - 1 if n != 1 else 2)]:
        if n2 == 0: continue
        cands.append("f(x) = " + ft(n2, a2))
    cands = [c for c in dict.fromkeys(cands) if c != ans]
    return make("La gráfica corresponde a una función de la forma f(x) = a·xⁿ (a = 1 o a = −1). ¿Cuál es f?", pl.svg("Gráfica de una función potencia"), ans, pick4(ans, cands), Q_REP,
                f"El punto ({p}, {fs(q)}) y la simetría de la curva determinan a = {a} y n = {n}.")


def t_shift(r, l):
    if l == 0:
        n = r.choice([2, 3]); a = 1
        h, k = (r.choice([x for x in range(-4, 5) if x]), 0) if r.random() < 0.5 else (0, r.choice([x for x in range(-5, 6) if x]))
    elif l == 1:
        n = r.choice([2, 3, -1]); a = 1
        h, k = r.choice([x for x in range(-3, 4) if x]), r.choice([x for x in range(-4, 5) if x])
    else:
        n = r.choice([2, 3, -1, -2]); a = r.choice([1, -1])
        h, k = r.choice([x for x in range(-3, 4) if x]), r.choice([x for x in range(-4, 5) if x])
    g = lambda x: a * (x - h) ** n + k
    def extra(p):
        if n < 0:
            p.vline(h); p.hline(k)
    x0, x1 = h - 4, h + 4
    pl = plot(g, x0, x1, k - 7, k + 7, [(h, k, f"({h}, {k})", 0, 30 if (a > 0 and n > 0) else -30)], extra=extra, sy=2)
    ans = "g(x) = " + ft(n, a, h, k)
    cands = ["g(x) = " + ft(n, a, -h, k), "g(x) = " + ft(n, a, h, -k), "g(x) = " + ft(n, a, -h, -k), "g(x) = " + ft(n, -a, h, k), "g(x) = " + ft(n, a, k, h) if (h, k) != (k, h) else "g(x) = " + ft(n, a, h + 1, k),
             "g(x) = " + ft(n, a, h + 1, k), "g(x) = " + ft(n, a, h, k + 1), "g(x) = " + ft(n + 2 if n > 0 else n - 2, a, h, k)]
    return make("La figura muestra la gráfica de g, obtenida al trasladar (y a veces reflejar) una función potencia. ¿Cuál es la ecuación de g?", pl.svg("Gráfica trasladada"), ans, pick4(ans, cands), Q_REP,
                f"El centro de la curva es ({h}, {k}): g(x) = {ft(n, a, h, k)}" + (" (con asíntotas x = h e y = k)." if n < 0 else "."))


# ---------------------------------------------------------------- Argumentar
def term(e):
    return "1" if e == 0 else "x" if e == 1 else "x" + sup(e)


def par_expr(r, l):
    if l == 0:
        e = r.randint(1, 8)
        return term(e), [e]
    if l == 1:
        es = r.sample(range(0, 7), r.choice([2, 3]))
        es.sort(reverse=True)
        return " + ".join(term(e) for e in es), es
    a, b, c = r.randint(1, 4), r.randint(0, 5), r.randint(0, 5)
    if b == c: raise Reject
    inner = " + ".join(term(e) for e in sorted([b, c], reverse=True))
    return (term(a) + "(" + inner + ")"), [a + b, a + c]


def parity(es):
    if all(e % 2 == 0 for e in es): return "par"
    if all(e % 2 == 1 for e in es): return "impar"
    return "ninguna"


def sym_fig():
    ev = Plot(180, 170, -3, 3, 0, 9, ml=10, mr=10, mt=10, mb=10)
    ev.axes(10, 10) if False else None
    body = ""
    for x0, kind in ((30, "even"), (310, "odd")):
        pts = []
        for i in range(41):
            x = -2 + i / 10
            y = x * x if kind == "even" else x ** 3 / 2
            pts.append((x0 + 80 + 35 * x, 95 - (14 * y if kind == "even" else 22 * y / 1.0 * 0.5)))
        d = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts if 10 <= b <= 185)
        body += L(x0, 95, x0 + 160, 95, INK, 2) + L(x0 + 80, 10, x0 + 80, 185, INK, 2) + f'<polyline fill="none" stroke="{ACC}" stroke-width="4" points="{d}"/>'
    body += tag(110, 215, "Simetría respecto del eje Y", 14) + tag(390, 215, "Simetría respecto del origen", 14)
    return wrap(560, 240, body, "Funciones par e impar")


def t_parity(r, l):
    want = r.choice(["par", "impar"])
    good = bad = None
    pool = {"par": [], "impar": [], "ninguna": []}
    for _ in range(80):
        try:
            s, es = par_expr(r, l)
        except Reject:
            continue
        pool[parity(es)].append(s)
    for k in pool: pool[k] = sorted(set(pool[k]))
    others = [x for k, v in pool.items() if k != want for x in v]
    if not pool[want] or len(others) < 4: raise Reject
    good = "f(x) = " + r.choice(pool[want])
    bad = ["f(x) = " + x for x in r.sample(others, 4)]
    return make(f"¿Cuál de las siguientes funciones es {want}? (f es par si f(−x) = f(x); es impar si f(−x) = −f(x))", sym_fig(), good, bad, Q_ARG,
                "Se comparan los exponentes: todos pares ⟹ función par; todos impares ⟹ función impar; mezcla ⟹ ninguna de las dos.")


TF = {
    "pos_even": (["Su gráfica es simétrica respecto del eje Y", "Se cumple f(−a) = f(a) para todo a", "Su gráfica pasa por (−1, 1) y por (1, 1)", "Su recorrido es y ≥ 0", "Es decreciente para x < 0"],
                 ["Su gráfica es simétrica respecto del origen", "Se cumple f(−a) = −f(a) para todo a", "Su gráfica pasa por (−1, −1)", "Su recorrido son todos los reales", "Es creciente en todo su dominio", "No pasa por el origen"]),
    "pos_odd": (["Su gráfica es simétrica respecto del origen", "Se cumple f(−a) = −f(a) para todo a", "Su gráfica pasa por (−1, −1) y por (1, 1)", "Su recorrido son todos los reales", "Es creciente en todo su dominio"],
                ["Su gráfica es simétrica respecto del eje Y", "Se cumple f(−a) = f(a) para todo a", "Su gráfica pasa por (−1, 1)", "Su recorrido es y ≥ 0", "Es decreciente para x < 0", "No pasa por el origen"]),
    "neg_even": (["Su gráfica es simétrica respecto del eje Y", "Su dominio son los reales distintos de 0", "Su recorrido es y > 0", "Tiene como asíntotas los ejes coordenados", "No corta a ningún eje"],
                 ["Su gráfica pasa por el origen", "Su dominio son todos los reales", "Su recorrido son todos los reales", "Su gráfica es simétrica respecto del origen", "Corta al eje Y en (0, 1)", "Su recorrido es y ≥ 0"]),
    "neg_odd": (["Su gráfica es simétrica respecto del origen", "Su dominio son los reales distintos de 0", "Su recorrido son los reales distintos de 0", "Tiene como asíntotas los ejes coordenados", "No corta a ningún eje"],
                ["Su gráfica pasa por el origen", "Su dominio son todos los reales", "Su recorrido son todos los reales", "Su gráfica es simétrica respecto del eje Y", "Su recorrido es y > 0", "Corta al eje X en (1, 0)"]),
}


def t_props(r, l):
    cats = ["pos_even", "pos_odd"] if l == 0 else list(TF)
    cat = r.choice(cats)
    n = {"pos_even": r.choice([2, 4, 6]), "pos_odd": r.choice([1, 3, 5]), "neg_even": r.choice([-2, -4]), "neg_odd": r.choice([-1, -3])}[cat]
    T_, F_ = TF[cat]
    if l < 2:
        good, bad = r.choice(T_), r.sample(F_, 4)
        stem = f"Sea f(x) = {ft(n)}. ¿Cuál de las siguientes afirmaciones es verdadera?"
        ex = "Se deduce de la paridad y del signo del exponente."
    else:
        good, bad = r.choice(F_), r.sample(T_, 4)
        stem = f"Sea f(x) = {ft(n)}. ¿Cuál de las siguientes afirmaciones es FALSA?"
        ex = "Las otras cuatro afirmaciones se deducen de la paridad y del signo del exponente."
    f = lambda x: x ** n
    ymax = 8
    pl = plot(f, -4, 4, -ymax, ymax, sy=2)
    return make(stem, pl.svg("Gráfica de la función potencia"), good, bad, Q_ARG, ex)


def t_counter_pow(r, l):
    if l == 0:
        claim = "Toda función de la forma f(x) = xⁿ, con n entero no nulo, es creciente en todo su dominio."
        goods = [ft(n) for n in (2, 4, 6, -1, -2, -3)]
        bads = [ft(n) for n in (1, 3, 5, 7, 9)]
        head = ["f(x) = xⁿ, n entero no nulo", "es creciente en todo su dominio", "¿Con cuál se refuta?"]
        good, bad = "f(x) = " + r.choice(goods), ["f(x) = " + x for x in r.sample(bads, 4)]
    elif l == 1:
        claim = "Si n es un entero impar, la función f(x) = xⁿ está definida para todos los números reales."
        goods = [ft(n) for n in (-1, -3, -5)]
        bads = [ft(n) for n in (1, 3, 5, 7, 9)]
        head = ["n impar ⟹ f(x) = xⁿ", "definida para todo real", "¿Con cuál se refuta?"]
        good, bad = "f(x) = " + r.choice(goods), ["f(x) = " + x for x in r.sample(bads, 4)]
    else:
        claim = "El producto de dos funciones impares es siempre una función impar."
        head = ["f impar y g impar", "⟹ f·g impar", "¿Con qué par se refuta?"]
        odd = [1, 3, 5, 7]
        ev = [2, 4, 6]
        pa = r.sample(odd, 2)
        good = f"f(x) = {ft(pa[0])} y g(x) = {ft(pa[1])}"
        bad = []
        for _ in range(30):
            e_, o_ = r.choice(ev), r.choice(odd)
            s_ = f"f(x) = {ft(e_)} y g(x) = {ft(o_)}" if r.random() < 0.5 else f"f(x) = {ft(o_)} y g(x) = {ft(e_)}"
            if s_ not in bad: bad.append(s_)
            if len(bad) == 4: break
    if len(bad) < 4: raise Reject
    return make(f"Un estudiante afirma: «{claim}» ¿Cuál de las siguientes opciones sirve como contraejemplo?", card(["Afirmación de un estudiante:"] + head, 220, 19), good, bad, Q_ARG,
                "Un contraejemplo cumple la hipótesis de la afirmación pero no su conclusión.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_eval(r, l):
    if l == 0:
        n = r.choice([-3, -2, -1, 2, 3, 4]); a = r.choice([-3, -2, 2, 3, 4])
        v = F(a) ** n
        stem = f"Si f(x) = {ft(n)}, ¿cuánto vale f({a})?"
        cands = [-v, F(a) ** abs(n) if n < 0 else F(1, a ** n), F(a * n), F(n) ** a if abs(n) ** abs(a) < 200 else v + 1, v + 1, -1 / v if v else 1]
        eq = f"f(x) = {ft(n)}"
        ex = f"f({a}) = ({a}){sup(n)} = {fs(v)}."
    elif l == 1:
        n = r.choice([2, 3, 4, -1, -2]); h = r.choice([x for x in range(-3, 4) if x]); k = r.randint(-4, 5)
        x0 = h + r.choice([x for x in (-2, -1, 1, 2, 3) if (h + x) != h])
        v = F(x0 - h) ** n + k
        stem = f"Si g(x) = {ft(n, 1, h, k)}, ¿cuánto vale g({x0})?"
        cands = [pw(x0 + h, n) + k, pw(x0 - h, n) - k, pw(x0, n) + k - h, pw(x0 - h, n), F(x0 - h) * n + k, pw(x0 + h, n) - k, v + 1]
        eq = f"g(x) = {ft(n, 1, h, k)}"
        ex = f"g({x0}) = ({x0 - h}){sup(n)} + ({k}) = {fs(v)}."
    else:
        n = r.choice([2, 3, -1, -2]); k = r.choice([2, 3, 4, 5, 6]); p = r.choice([1, 2]); c = r.choice([x for x in (2, 3, 4, -2) if x != p])
        qv = k * F(p) ** n
        v = k * F(c) ** n
        stem = f"La función f(x) = k·x{sup(n) if n != 1 else ''} cumple f({p}) = {fs(qv)}. ¿Cuánto vale f({c})?".replace("k·x⁻¹", "k/x").replace("k·x⁻²", "k/x²")
        cands = [qv * c, qv * F(c, p), qv * F(c, p) ** abs(n), v + 1, F(c) ** n, qv + c - p]
        eq = f"f(x) = k · xⁿ,  f({p}) = {fs(qv)}"
        ex = f"k = {k}; f({c}) = {k}·({c}){sup(n)} = {fs(v)}."
    ans = fs(v)
    cands = [fs(F(c_).limit_denominator(10 ** 6)) for c_ in cands]
    return make(stem, card([eq, "Reemplaza y calcula"], 190, 22), ans, pick4(ans, cands), Q_PRO, ex)


def t_solve_pow(r, l):
    if l == 0:
        n = r.choice([3, 5]); m = r.choice([-3, -2, 2, 3, 4]) if n == 3 else r.choice([-2, -1, 1, 2])
        c = m ** n
        stem, eq = f"Resuelve la ecuación x{sup(n)} = {c}.", f"x{sup(n)} = {c}"
        ans = f"x = {m}"
        cands = [f"x = {-m}", f"x = ±{abs(m)}", f"x = {c // n if c % n == 0 else c + 1}", f"x = {m * n}", f"x = {c}", f"x = {m + 1}"]
    elif l == 1:
        n = r.choice([2, 4, 6]); m = r.randint(2, 4)
        c = m ** n
        stem, eq = f"Resuelve la ecuación x{sup(n)} = {c}.", f"x{sup(n)} = {c}"
        ans = f"x = ±{m}"
        cands = [f"x = {m}", f"x = {-m}", f"x = ±{c // n if c % n == 0 else c + 1}", f"x = ±{m * n}", f"x = ±{m + 1}", f"x = ±{c}"]
    else:
        n = r.choice([2, 3, 4]); h = r.choice([x for x in range(-3, 4) if x]); m = r.randint(1, 3)
        base = f"(x {'−' if h > 0 else '+'} {abs(h)})"
        c = m ** n
        stem, eq = f"Resuelve la ecuación {base}{sup(n)} = {c}.", f"{base}{sup(n)} = {c}"
        if n % 2:
            ans = f"x = {h + m}"
            cands = [f"x = {-h + m}", f"x = {h - m}", f"x = {m}", f"x = {h + m} o x = {h - m}", f"x = {m - h - 1}"]
        else:
            ans = f"x = {h - m} o x = {h + m}"
            cands = [f"x = {h + m}", f"x = {-h - m} o x = {-h + m}", f"x = {-m} o x = {m}", f"x = {h - m}", f"x = {h - m + 1} o x = {h + m + 1}"]
    return make(stem, card([eq, "Toma raíz n-ésima en ambos lados"], 190, 22), ans, pick4(ans, cands), Q_PRO,
                f"Se aplica la raíz n-ésima" + (" (con dos signos si n es par)" if n % 2 == 0 else "") + f": {ans}.")


BY_SKILL = {
    Q_RES: [t_find_k, t_intersect],
    Q_MOD: [t_scale, t_table],
    Q_REP: [t_match, t_shift],
    Q_ARG: [t_parity, t_props, t_counter_pow],
    Q_PRO: [t_eval, t_solve_pow],
}
