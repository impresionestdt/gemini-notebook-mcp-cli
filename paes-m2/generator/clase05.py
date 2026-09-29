"""Clase 5 · Ecuación cuadrática avanzada: discriminante y naturaleza de las raíces."""
from fractions import Fraction as F
from math import isqrt, gcd
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO


def poly(a, b, c, var="x"):
    parts = []
    for co, pw in ((a, f"{var}²"), (b, var), (c, "")):
        co = F(co)
        if co == 0:
            continue
        mag = fs(abs(co))
        core = (mag if (abs(co) != 1 or pw == "") else "") + pw
        parts.append(("−" if co < 0 else "") + core if not parts else (" − " if co < 0 else " + ") + core)
    return "".join(parts) or "0"


def sgn(v, sym):
    return f"{sym} {'>' if v > 0 else '<' if v < 0 else '='} 0"


def parab(f, x0, x1, marks=(), label=None, extra=None, yr=None):
    xs = [x0 + (x1 - x0) * i / 60 for i in range(61)]
    ys = [f(x) for x in xs]
    lo, hi = (yr if yr else (min(-1, min(ys) - 1), max(1, max(ys) + 1)))
    pad = max(2, 0.14 * (hi - lo))
    lo, hi = min(lo, -pad), max(hi, pad)
    pl = Plot(560, 270, x0, x1, lo, hi)
    pl.axes(max(1, round((x1 - x0) / 8)), max(1, round((hi - lo) / 6)))
    pl.curve(f, x0, x1)
    if extra:
        extra(pl)
    xs_m = [m[0] for m in marks if m[1] == 0]
    for (x, y, lab, dy) in marks:
        dx = 0
        if y == 0 and len(xs_m) == 2 and abs(xs_m[0] - xs_m[1]) <= 2:
            dx = -34 if x == min(xs_m) else 34
        if x == 0 and x0 >= -0.5:
            dx = 45
        pl.pt(x, y, lab, dx=dx, dy=dy)
    return pl


def _int_roots(r, lo=-6, hi=6):
    while True:
        a, b = r.randint(lo, hi), r.randint(lo, hi)
        if a != b and a != 0 and b != 0:
            return (a, b) if a < b else (b, a)


# ---------------------------------------------------------------- Resolver
def t_param_disc(r, l):
    if l == 0:
        b = r.choice([-12, -10, -8, -6, -4, -2, 2, 4, 6, 8, 10, 12])
        k = b * b // 4
        stem = f"¿Para qué valor de k la ecuación x² {'−' if b < 0 else '+'} {abs(b)}x + k = 0 tiene una única solución real?"
        ans = str(k)
        cands = [str(b * b), str(b * b // 2), str(abs(b) // 2), str(-k), str(2 * abs(b)), str(k + 1)]
        pl = parab(lambda x: x * x + b * x + k, -b / 2 - 4, -b / 2 + 4, [(-b / 2, 0, "única raíz", -28)])
        ex = f"Δ = {b}² − 4·1·k = 0 ⟹ k = {b*b}/4 = {k}."
    elif l == 1:
        m, n = r.choice([1, 2, 3]), r.randint(1, 4)
        a, c, k = m * m, n * n, 2 * m * n
        stem = f"¿Para qué valores de k la ecuación {poly(a, 'k', c).replace('k', 'kx', 1) if False else (str(a) if a != 1 else '')}x² + kx + {c} = 0 tiene exactamente una solución real?"
        ans = f"k = ±{k}"
        cands = [f"k = ±{m * n}", f"k = ±{4 * m * n}", f"k = {k}", f"k = −{k}", f"k = ±{a * c}", f"k = ±{m + n}"]
        f1 = lambda x: a * x * x + k * x + c
        f2 = lambda x: a * x * x - k * x + c
        pl = parab(f1, -4, 4, yr=(-1, c + 3), extra=lambda p: p.curve(f2, -4, 4, NAVY))
        ex = f"Δ = k² − 4·{a}·{c} = 0 ⟹ k² = {k*k}, o sea k = ±{k}."
    else:
        m, n = r.choice([1, 2, 3]), r.randint(1, 4)
        a, c, k = m * m, n * n, 2 * m * n
        stem = f"¿Para qué valores de k la ecuación {(str(a) if a != 1 else '')}x² + kx + {c} = 0 NO tiene soluciones reales?"
        ans = f"−{k} < k < {k}"
        cands = [f"k < −{k} o k > {k}", f"−{m * n} < k < {m * n}", f"k < {k}", f"−{2 * k} < k < {2 * k}", f"k > {k}"]
        pl = parab(lambda x: a * x * x + 0.5 * k * x + c, -4, 4, yr=(-1, c + 4))
        ex = f"Se pide Δ < 0: k² − {4*a*c} < 0 ⟹ −{k} < k < {k}."
    return make(stem, pl.svg("Parábola y eje X"), ans, pick4(ans, cands), Q_RES, ex)


def t_vieta(r, l):
    if l == 0:
        r1, r2 = r.sample(range(-6, 8), 2)
        S, P = r1 + r2, r1 * r2
        a = 1
        stem = f"Sean x₁ y x₂ las raíces de la ecuación {poly(1, -S, P)} = 0. ¿Cuánto valen x₁ + x₂ y x₁·x₂?"
    elif l == 1:
        r1, r2 = r.sample(range(-6, 8), 2)
        a = r.choice([2, 3, 4])
        S, P = F(r1 + r2), F(r1 * r2)
        stem = f"Sean x₁ y x₂ las raíces de la ecuación {poly(a, -a * (r1 + r2), a * r1 * r2)} = 0. ¿Cuánto valen x₁ + x₂ y x₁·x₂?"
    else:
        r1 = r.choice([2, 3, 4, 5, -2, -3])
        r2 = r.choice([x for x in range(-6, 8) if x not in (0, r1)])
        S, P = r1 + r2, r1 * r2
        stem = f"Una raíz de la ecuación x² − kx + ({P}) = 0 es {r1}. ¿Cuál es el valor de k y cuál es la otra raíz?".replace("+ (-", "− (").replace("+ (", "+ (")
        stem = f"Una raíz de la ecuación x² − kx {'+' if P > 0 else '−'} {abs(P)} = 0 es {r1}. ¿Cuál es el valor de k y cuál es la otra raíz?"
        ans = f"k = {S} y otra raíz {r2}"
        cands = [f"k = {-S} y otra raíz {r2}", f"k = {S} y otra raíz {-r2}", f"k = {P} y otra raíz {S}", f"k = {S} y otra raíz {r2 + 1}", f"k = {S + 1} y otra raíz {r2}"]
        fig = parab(lambda x: (x - r1) * (x - r2), min(r1, r2) - 3, max(r1, r2) + 3, [(r1, 0, f"x = {r1}", 28)]).svg("Parábola con una raíz conocida")
        return make(stem, fig, ans, pick4(ans, cands), Q_RES, f"Producto: {r1}·x₂ = {P} ⟹ x₂ = {r2}; k = suma = {S}.")
    ans = f"suma = {fs(S)}; producto = {fs(P)}"
    cands = [f"suma = {fs(-S)}; producto = {fs(P)}", f"suma = {fs(S)}; producto = {fs(-P)}", f"suma = {fs(P)}; producto = {fs(S)}", f"suma = {fs(-S)}; producto = {fs(-P)}", f"suma = {fs(S * a)}; producto = {fs(P * a)}"]
    fig = parab(lambda x: (x - r1) * (x - r2), min(r1, r2) - 3, max(r1, r2) + 3, [(r1, 0, "x₁", 30), (r2, 0, "x₂", 30)]).svg("Parábola con sus raíces")
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, f"Suma = −b/a = {fs(S)}; producto = c/a = {fs(P)}.")


# ---------------------------------------------------------------- Modelar
def rect_path(L_, W_, x):
    x0, y0, s = 150, 30, 12
    body = (R(x0, y0, (L_ + 2 * x) * s, (W_ + 2 * x) * s, FILL2) + R(x0 + x * s, y0 + x * s, L_ * s, W_ * s, FILL)
            + tag(x0 + (L_ + 2 * x) * s / 2, y0 + (W_ + 2 * x) * s / 2, f"jardín {L_} × {W_} m", 16)
            + tag(x0 + (L_ + 2 * x) * s / 2, y0 + (W_ + 2 * x) * s + 22, "camino de ancho x", 15))
    return wrap(560, max(200, y0 + (W_ + 2 * x) * s + 50), body, "Jardín rodeado por un camino")


def t_quad_model(r, l):
    if l == 0:
        w, d = r.randint(2, 14), r.randint(2, 9)
        A = w * (w + d)
        stem = f"El largo de un rectángulo excede en {d} m a su ancho y su área es {A} m². ¿Cuánto mide el ancho?"
        ans = f"{w} m"
        cands = [f"{w + d} m", f"{d} m", f"{w + 1} m", f"{max(1, w - 1)} m", f"{-(w + d)} m", f"{A // d} m"]
        body = R(150, 40, 260, 110, FILL) + tag(280, 95, f"Área = {A} m²", 18) + tag(280, 170, f"largo = ancho + {d}", 16) + tag(95, 95, "ancho = ?", 16)
        fig, ex = wrap(560, 200, body, "Rectángulo"), f"w(w + {d}) = {A} ⟹ w² + {d}w − {A} = 0, y la raíz positiva es {w}."
    elif l == 1:
        x, L_, W_ = r.randint(1, 4), r.randint(6, 18), r.randint(4, 12)
        A = 2 * x * (L_ + W_) + 4 * x * x
        stem = f"Un jardín de {L_} m × {W_} m se rodea con un camino de ancho uniforme x. El área del camino es {A} m². ¿Cuánto mide x?"
        ans = f"{x} m"
        other = F(-(L_ + W_), 2) - x
        cands = [f"{x + 1} m", f"{max(1, x - 1)} m", f"{2 * x} m", f"{fs(other)} m", f"{A // (2 * (L_ + W_))} m" if A // (2 * (L_ + W_)) != x else f"{x + 2} m"]
        fig, ex = rect_path(L_, W_, x), f"(L+2x)(W+2x) − L·W = {A} ⟹ 4x² + {2*(L_+W_)}x − {A} = 0; la raíz positiva es {x}."
    else:
        t2, m = r.randint(2, 6), r.randint(1, 3)
        v, h0 = 5 * (t2 - m), 5 * t2 * m
        if v <= 0: raise Reject
        stem = f"Un objeto se lanza y su altura (en m) es h(t) = −5t² + {v}t + {h0}, con t en segundos. ¿En qué instante llega al suelo?"
        ans = f"{t2} s"
        cands = [f"{m} s", f"{t2 + m} s", f"{t2 - m} s", f"{-m} s", f"{t2 + 1} s", f"{h0 // v if v else 1} s"]
        hm = max(-5 * t * t + v * t + h0 for t in [i / 10 for i in range(0, t2 * 10 + 1)])
        pl = parab(lambda t: -5 * t * t + v * t + h0, 0, t2 + 1, [(0, h0, f"h₀ = {h0}", 28)], yr=(-1, hm + 4))
        fig, ex = pl.svg("Trayectoria del objeto"), f"h = 0 ⟹ −5(t − {t2})(t + {m}) = 0; solo t = {t2} es válido (t > 0)."
    return make(stem, fig, ans, pick4(ans, [c for c in cands if c != ans]), Q_MOD, ex)


def t_model2(r, l):
    if l == 0:
        n = r.randint(3, 15)
        N = n * (n + 1)
        stem = f"El producto de dos números enteros positivos consecutivos es {N}. ¿Cuáles son esos números?"
        ans = f"{n} y {n + 1}"
        cands = [f"{n - 1} y {n + 2}", f"{n + 1} y {n + 2}", f"{-n - 1} y {-n}", f"{n - 1} y {n}", f"{n} y {n + 2}"]
        body = (R(60, 60, 190, 90, FILL) + T(155, 115, "n", 30) + R(310, 60, 190, 90, FILL) + T(405, 115, "n + 1", 30)
                + tag(280, 30, f"Producto = {N}", 18) + T(280, 112, "×", 34))
        fig, ex = wrap(560, 190, body, "Dos números consecutivos"), f"n(n + 1) = {N} ⟹ n² + n − {N} = 0; n = {n} (la raíz {-n-1} no es positiva)."
    elif l == 1:
        tri = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (20, 21, 29), (7, 24, 25), (9, 40, 41)])
        k = r.choice([1, 2, 3]) if tri[2] < 20 else 1
        x, y, h = (tri[0] * k, tri[1] * k, tri[2] * k)
        d = y - x
        stem = f"Un triángulo rectángulo tiene catetos x y x + {d}, e hipotenusa {h} cm. ¿Cuánto mide el cateto menor?"
        ans = f"{x} cm"
        other = -x - d
        cands = [f"{y} cm", f"{h - d} cm", f"{other} cm", f"{x + 1} cm", f"{h - x} cm"]
        body = P([(110, 170), (430, 170), (110, 40)], FILL) + tag(270, 200, f"x + {d}", 17) + tag(65, 105, "x", 17) + tag(300, 92, f"{h} cm", 17)
        fig, ex = wrap(560, 220, body, "Triángulo rectángulo"), f"x² + (x + {d})² = {h}² ⟹ x² + {d}x − {(h*h - d*d)//2} = 0 ⟹ x = {x}."
    else:
        p0, n0, dd = r.choice([10, 20, 50]), r.choice([60, 80, 100, 120]), r.choice([2, 4, 5])
        byR = {}
        for x in range(0, n0 // dd):
            byR.setdefault((p0 + x) * (n0 - dd * x), []).append(x)
        pairs = [(R_, v) for R_, v in byR.items() if len(v) == 2 and v[0] > 0]
        if not pairs: raise Reject
        R_, (x1, x2) = r.choice(pairs)
        stem = (f"Una entrada cuesta ${p0} y se venden {n0} entradas. Por cada $1 de aumento se venden {dd} entradas menos. "
                f"Si el ingreso fue de ${R_}, ¿cuál es el mayor aumento posible?")
        ans = f"${x2}"
        cands = [f"${x1}", f"${x1 + x2}", f"${x2 + 1}", f"${x2 - 1}", f"${(x1 + x2) // 2}", f"${n0 // dd}"]
        fig, ex = card([f"({p0} + x)({n0} − {dd}x) = {R_}", "¿Mayor valor de x?"], 190, 22), f"−{dd}x² + {n0 - dd*p0}x + {p0*n0 - R_} = 0 tiene raíces {x1} y {x2}; el mayor aumento es ${x2}."
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_graph_signs(r, l):
    s = r.choice([1, -1])
    kind = r.choice(["pos", "zero", "neg"])
    if kind == "pos":
        r1, r2 = _int_roots(r, -5, 5)
        if l == 2 and r1 + r2 == 0: raise Reject
        f = lambda x: s * (x - r1) * (x - r2)
        a, b, c = s, -s * (r1 + r2), s * r1 * r2
        marks = [(r1, 0, f"({r1}, 0)", 28), (r2, 0, f"({r2}, 0)", 28)]
        xa, xb = min(r1, r2) - 3, max(r1, r2) + 3
    elif kind == "zero":
        rr = r.choice([x for x in range(-5, 6) if x])
        f = lambda x: s * (x - rr) ** 2
        a, b, c = s, -2 * s * rr, s * rr * rr
        marks, xa, xb = [], rr - 4, rr + 4
    else:
        h, q = r.choice([x for x in range(-4, 5) if x]), r.randint(1, 3)
        f = lambda x: s * ((x - h) ** 2 + q)
        a, b, c = s, -2 * s * h, s * (h * h + q)
        marks, xa, xb = [], h - 4, h + 4
    D = b * b - 4 * a * c
    pl = parab(f, xa, xb, marks)
    if l == 0:
        attrs = [("a", a), ("Δ", D)]
    elif l == 1:
        attrs = [("a", a), ("c", c), ("Δ", D)]
    else:
        attrs = [("a", a), ("b", b), ("Δ", D)]
    fmtc = lambda vals: ", ".join(sgn(v, n) for (n, _), v in zip(attrs, vals))
    truth = tuple(v for _, v in attrs)
    sg = lambda v: (v > 0) - (v < 0)
    truth = tuple(sg(v) for v in truth)
    if l == 0:
        truth_last = truth[-1]
    ans = fmtc(truth)
    cands = []
    for i in range(len(truth)):
        for alt in (-1, 0, 1):
            if alt != truth[i] and (attrs[i][0] != "a" or alt != 0) and (attrs[i][0] != "c" or True):
                t2 = list(truth); t2[i] = alt; cands.append(fmtc(t2))
    r.shuffle(cands)
    cands = [c for c in cands if c != ans]
    names = ", ".join(n for n, _ in attrs)
    return make(f"El gráfico corresponde a f(x) = ax² + bx + c. ¿Cuál es el signo de {names.replace(', ', ' y ', 1) if len(attrs) == 2 else names}?".replace("de a, c, Δ", "de a, c y Δ").replace("de a, b, Δ", "de a, b y Δ"),
                pl.svg("Gráfico de una parábola"), ans, pick4(ans, cands), Q_REP,
                f"Abre {'hacia arriba' if a > 0 else 'hacia abajo'} (a {'>' if a > 0 else '<'} 0); el número de cortes con el eje X da el signo de Δ = {D if False else ''}".rstrip(" = ") + "; c es la ordenada en el origen y b se deduce de la posición del vértice (x = −b/2a).")


def t_read_eq(r, l):
    if l == 0:
        r1, r2 = _int_roots(r, -6, 6)
        a = 1
        f = lambda x: (x - r1) * (x - r2)
        marks = [(r1, 0, f"({r1}, 0)", 28), (r2, 0, f"({r2}, 0)", 28)]
        coef = (1, -(r1 + r2), r1 * r2)
        cands = [(1, r1 + r2, r1 * r2), (1, -(r1 + r2), -r1 * r2), (1, r1 + r2, -r1 * r2), (1, -r1 * r2, r1 + r2), (-1, r1 + r2, -r1 * r2)]
        xa, xb = min(r1, r2) - 3, max(r1, r2) + 3
    elif l == 1:
        r1, r2 = _int_roots(r, -5, 5)
        a = r.choice([2, -1, -2, 3])
        f = lambda x: a * (x - r1) * (x - r2)
        c = a * r1 * r2
        marks = [(r1, 0, f"({r1}, 0)", 28), (r2, 0, f"({r2}, 0)", 28), (0, c, f"(0, {c})", -28 if a < 0 else 28)]
        coef = (a, -a * (r1 + r2), c)
        cands = [(1, -(r1 + r2), r1 * r2), (a, a * (r1 + r2), c), (-a, -a * (r1 + r2), -c), (a, -a * (r1 + r2), r1 * r2), (a, -(r1 + r2), c)]
        xa, xb = min(r1, r2) - 3, max(r1, r2) + 3
    else:
        rr = r.choice([x for x in range(-4, 5) if x])
        a = r.choice([1, 2, -1, -2, 3])
        f = lambda x: a * (x - rr) ** 2
        c = a * rr * rr
        marks = [(rr, 0, f"({rr}, 0)", 28 if a > 0 else -28), (0, c, f"(0, {c})", -28 if a < 0 else 28)]
        coef = (a, -2 * a * rr, c)
        cands = [(a, 2 * a * rr, c), (1, -2 * rr, rr * rr), (a, -2 * a * rr, -c), (a, -a * rr, c), (-a, -2 * a * rr, c)]
        xa, xb = rr - 4, rr + 4
    ys = [f(x) for x in [xa + (xb - xa) * i / 40 for i in range(41)]]
    pl = parab(f, xa, xb, marks, yr=(max(-25, min(-1, min(ys) - 1)), min(25, max(1, max(ys) + 1))))
    ans = "y = " + poly(*coef)
    ds = ["y = " + poly(*c) for c in cands]
    return make("La figura muestra la gráfica de una función cuadrática con los puntos indicados. ¿Cuál es su ecuación?", pl.svg("Gráfico de función cuadrática"), ans, pick4(ans, ds), Q_REP,
                f"Se usa la forma factorizada con las raíces y el punto (0, c): y = {poly(*coef)}.")


# ---------------------------------------------------------------- Argumentar
NAT = ["Dos raíces reales racionales distintas", "Dos raíces reales irracionales", "Una raíz real doble", "Dos raíces complejas conjugadas", "Una raíz real y una compleja"]


def t_nature(r, l):
    kind = r.choice(["rac", "irr", "dbl", "cx"])
    a = 1 if l == 0 else r.choice([1, 2, 3])
    if kind == "rac":
        r1, r2 = r.sample(range(-6, 7), 2)
        b, c = -a * (r1 + r2), a * r1 * r2
    elif kind == "dbl":
        rr = r.randint(-6, 6)
        b, c = -2 * a * rr, a * rr * rr
    else:
        b, c = r.randint(-9, 9), r.randint(-9, 9)
    D = b * b - 4 * a * c
    if kind == "irr" and (D <= 0 or isqrt(D) ** 2 == D): raise Reject
    if kind == "cx" and D >= 0: raise Reject
    idx = {"rac": 0, "irr": 1, "dbl": 2, "cx": 3}[kind]
    if l == 2:
        stem = f"Sin resolverla, ¿qué se puede afirmar de las soluciones de {poly(a, b, 0)} = {fs(-c)}?"
        eq = f"{poly(a, b, 0)} = {fs(-c)}"
    else:
        stem = f"¿Qué se puede afirmar de las soluciones de la ecuación {poly(a, b, c)} = 0?"
        eq = f"{poly(a, b, c)} = 0"
    fig = card([eq, "Δ = b² − 4ac", "¿Naturaleza de las raíces?"], 210, 22)
    return make(stem, fig, NAT[idx], [x for i, x in enumerate(NAT) if i != idx], Q_ARG,
                f"Δ = ({b})² − 4·{a}·({c}) = {D}: {NAT[idx].lower()}.")


TRUE_A = ["Si a·c < 0, la ecuación tiene dos raíces reales distintas", "Si Δ = 0, las dos raíces son reales e iguales", "Si Δ < 0, la parábola no corta al eje X",
          "Si Δ > 0, la parábola corta al eje X en dos puntos", "Si b = 0 y a·c < 0, hay dos raíces reales opuestas"]
FALSE_A = ["Si a·c > 0, la ecuación no tiene raíces reales", "Si b = 0, la ecuación siempre tiene raíces reales", "Si Δ = 0, las raíces son complejas conjugadas",
           "Si Δ < 0, la parábola es tangente al eje X", "Si a > 0, la ecuación siempre tiene dos raíces reales", "Si c = 0, la ecuación no tiene raíces reales",
           "Si Δ > 0, las raíces son siempre enteras", "Si b² = 4ac, hay dos raíces reales distintas"]


def mini_par(x0, kind):
    yv = {"pos": 185, "zero": 150, "neg": 115}[kind]
    pts = []
    for i in range(41):
        u = -1 + i / 20
        pts.append((x0 + 85 + 70 * u, yv - 90 * u * u))
    pts = [(x, y) for x, y in pts if 30 <= y <= 200]
    d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    cap = {"pos": "Δ > 0", "zero": "Δ = 0", "neg": "Δ < 0"}[kind]
    return (L(x0 + 5, 150, x0 + 165, 150, INK, 3) + f'<polyline fill="none" stroke="{ACC}" stroke-width="4" points="{d}"/>'
            + tag(x0 + 85, 235, cap, 20))


def t_true_false(r, l):
    if l < 2:
        good = r.choice(TRUE_A)
        bad = r.sample(FALSE_A, 4)
        stem = "Sea la ecuación ax² + bx + c = 0, con a, b, c reales y a ≠ 0. ¿Cuál de las siguientes afirmaciones es verdadera?"
        ex = "Es una consecuencia directa del signo del discriminante."
    else:
        good = r.choice(FALSE_A)
        bad = r.sample(TRUE_A, 4)
        stem = "Sea la ecuación ax² + bx + c = 0, con a, b, c reales y a ≠ 0. ¿Cuál de las siguientes afirmaciones es FALSA?"
        ex = "Existen contraejemplos: por eso la afirmación no siempre se cumple."
    fig = wrap(560, 260, mini_par(0, "pos") + mini_par(185, "zero") + mini_par(370, "neg"), "Tres parábolas según el discriminante")
    return make(stem, fig, good, bad, Q_ARG, ex)


def t_counter_quad(r, l):
    def eq(a, b, c): return poly(a, b, c) + " = 0"
    if l == 0:
        claim, cond = "Si c > 0, la ecuación x² + bx + c = 0 no tiene soluciones reales.", lambda a, b, c: a == 1 and c > 0
        gen = lambda: (1, r.randint(-9, 9), r.randint(1, 20))
    elif l == 1:
        claim, cond = "Si a > 0 y c > 0, la ecuación ax² + bx + c = 0 no tiene soluciones reales.", lambda a, b, c: a > 0 and c > 0
        gen = lambda: (r.randint(1, 4), r.randint(-12, 12), r.randint(1, 12))
    else:
        claim, cond = "Si a + b + c > 0, la ecuación ax² + bx + c = 0 no tiene soluciones reales.", lambda a, b, c: a + b + c > 0
        gen = lambda: (r.randint(1, 3), r.randint(-9, 9), r.randint(-6, 9))
    good = bad = None
    goods, bads = [], []
    for _ in range(400):
        a, b, c = gen()
        if not cond(a, b, c) or a + b + c == 0 or b == 0 and l == 2:
            continue
        D = b * b - 4 * a * c
        (goods if D >= 0 else bads).append(eq(a, b, c))
    goods, bads = sorted(set(goods)), sorted(set(bads))
    if not goods or len(bads) < 4: raise Reject
    good = r.choice(goods)
    bad = r.sample(bads, 4)
    fig = card(["Afirmación de una estudiante:", claim.split(", la ecuación")[0].rstrip(".") + " ⟹ Δ < 0", "¿Cuál ecuación la refuta?"], 210, 20)
    return make(f"Una estudiante afirma: «{claim}» ¿Cuál de las siguientes ecuaciones sirve como contraejemplo?", fig, good, bad, Q_ARG,
                "Un contraejemplo cumple la condición de la afirmación pero tiene Δ ≥ 0, es decir, sí tiene soluciones reales.")


# ---------------------------------------------------------------- Aplicar procedimientos
def _root_str(a, b, D):
    """Soluciones de ax²+bx+c con discriminante D>0 no cuadrado perfecto."""
    s = 1
    t = D
    f = 2
    while f * f <= t:
        while t % (f * f) == 0:
            t //= f * f; s *= f
        f += 1
    d = 2 * a
    g = gcd(gcd(abs(b), s), abs(d))
    p, q, d = -b // g, s // g, d // g
    if d < 0:
        p, d = -p, -d
    rt = f"√{t}" if q == 1 else f"{q}√{t}"
    if d == 1:
        return f"x = {p} ± {rt}"
    return f"x = ({p} ± {rt})/{d}" if p != 0 else f"x = ±{rt}/{d}"


def t_solve(r, l):
    if l == 0:
        r1, r2 = r.sample(range(-8, 9), 2)
        a = 1
        b, c = -(r1 + r2), r1 * r2
        opts = lambda x, y: f"x = {min(x, y)} o x = {max(x, y)}"
        ans = opts(min(r1, r2), max(r1, r2))
        cands = [opts(-min(r1, r2), -max(r1, r2)), opts(r1 + 1, r2), opts(r1, -r2), opts(r1 + r2, r1 * r2) if len({r1 + r2, r1 * r2}) == 2 else opts(r1, r2 + 2), opts(r1 - 1, r2 - 1)]
        cands = [c_ for c_ in cands if c_ != ans and len(set(c_.split(" o "))) == 2]
        cands = list(dict.fromkeys(cands))
    else:
        a = r.choice([1, 2, 3]) if l == 1 else r.choice([2, 3, 4, 5])
        b, c = r.randint(-9, 9), r.randint(-8, 4)
        D = b * b - 4 * a * c
        if D <= 0 or isqrt(D) ** 2 == D: raise Reject
        ans = _root_str(a, b, D)
        cands = [_root_str(a, -b, D), _root_str(a, b, b * b + 4 * a * c) if b * b + 4 * a * c > 0 and isqrt(b * b + 4 * a * c) ** 2 != b * b + 4 * a * c else _root_str(a, b, D + 1),
                 _root_str(1, b, D) if a != 1 else _root_str(2, b, D), _root_str(a, b, b * b - 4 * c) if b * b - 4 * c > 0 and isqrt(b * b - 4 * c) ** 2 != b * b - 4 * c else _root_str(a, b, D + 2),
                 _root_str(a, b, D + a)]
        cands = [x for x in cands if x != ans]
    fig = card([f"{poly(a, b, c)} = 0", "x = (−b ± √(b² − 4ac)) / (2a)"], 190, 22)
    return make(f"Resuelve la ecuación {poly(a, b, c)} = 0.", fig, ans, pick4(ans, cands), Q_PRO, f"Δ = {b*b - 4*a*c}; se aplica x = (−b ± √Δ)/(2a): {ans}.")


def t_delta_calc(r, l):
    if l == 0:
        a, b, c = r.randint(1, 5), r.randint(-9, 9), r.randint(-9, 9)
        D = b * b - 4 * a * c
        stem, eq = f"¿Cuál es el discriminante de la ecuación {poly(a, b, c)} = 0?", f"{poly(a, b, c)} = 0"
        cands = [b * b + 4 * a * c, b * b - 4 * c, 4 * a * c - b * b, b * b - a * c, (b - 4 * a * c) ** 2 if abs(b - 4 * a * c) < 12 else D + 4, D + 2 * a]
        ans = str(D)
    elif l == 1:
        a, b, c = r.randint(1, 4), r.randint(-9, 9), r.randint(-9, 9)
        D = b * b - 4 * a * c
        eq = f"{poly(a, b, 0)} = {fs(c)}"
        stem = f"¿Cuál es el discriminante de la ecuación {eq}?"
        cands = [b * b - 4 * a * (-c), b * b + 4 * a * c if b * b + 4 * a * c != D else D + 8, b * b - 4 * a * c * 2, -D, b * b - 4 * c]
        ans = str(D)
    else:
        a = r.choice([1, 2])
        b, c = r.randint(-9, 9), r.randint(-9, 9)
        S, P = F(-b, a), F(c, a)
        val = S * S - 2 * P
        stem = f"Sin resolver la ecuación {poly(a, b, c)} = 0, ¿cuánto vale x₁² + x₂², donde x₁ y x₂ son sus raíces?"
        eq = f"{poly(a, b, c)} = 0"
        ans = fs(val)
        cands = [fs(S * S + 2 * P), fs(S * S - P), fs(S * S), fs(S * S - 2 * P + 1), fs(-S * S + 2 * P), fs(S * S - 4 * P)]
    fig = card([eq, "Δ = b² − 4ac" if l < 2 else "x₁² + x₂² = (x₁ + x₂)² − 2·x₁·x₂"], 190, 22)
    ans_s = ans
    cands = [c_ if isinstance(c_, str) else str(c_) for c_ in cands]
    return make(stem, fig, ans_s, pick4(ans_s, cands), Q_PRO, "Se aplican las fórmulas de discriminante y de Vieta: resultado " + ans_s + ".")


BY_SKILL = {
    Q_RES: [t_param_disc, t_vieta],
    Q_MOD: [t_quad_model, t_model2],
    Q_REP: [t_graph_signs, t_read_eq],
    Q_ARG: [t_nature, t_true_false, t_counter_quad],
    Q_PRO: [t_solve, t_delta_calc],
}
