"""Clase 9 · Concepto de función inversa y biyectividad."""
from fractions import Fraction as F
from math import sqrt
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase08 import lx, I, fi

INV = "f⁻¹"


def invlin(m, b):
    if m > 0:
        num = lx(1, -b)
        s = f"({num})/{m}" if (m != 1 and b != 0) else (num if m == 1 else f"x/{m}")
    else:
        num = lx(-1, b)
        s = num if m == -1 else f"({num})/{abs(m)}"
        if b == 0 and m != -1: s = f"−x/{abs(m)}"
    return s


def machine(top, mid, bot, arrow_in="x", arrow_out="y"):
    body = (R(40, 40, 110, 50, FILL) + T(95, 72, top[0], 20) + L(150, 65, 210, 65, ACC, 4) + R(210, 40, 140, 50, FILL2) + T(280, 72, mid, 20)
            + L(350, 65, 410, 65, ACC, 4) + R(410, 40, 110, 50, FILL) + T(465, 72, top[1], 20)
            + R(410, 130, 110, 50, FILL) + T(465, 162, bot[0], 20) + L(410, 155, 350, 155, NAVY, 4) + R(210, 130, 140, 50, "#E0F2FE") + T(280, 162, f"{INV}", 22)
            + L(210, 155, 150, 155, NAVY, 4) + R(40, 130, 110, 50, FILL) + T(95, 162, bot[1], 20)
            + P([(210, 65), (198, 58), (198, 72)], ACC, ACC, 1) + P([(410, 65), (398, 58), (398, 72)], ACC, ACC, 1)
            + P([(350, 155), (362, 148), (362, 162)], NAVY, NAVY, 1) + P([(150, 155), (162, 148), (162, 162)], NAVY, NAVY, 1))
    return wrap(560, 210, body, "Función y su inversa como máquinas")


def map_fig(A, B, pairs, ttl=("A", "B")):
    n = max(len(A), len(B))
    h = 70 + 46 * n
    body = ELL(150, h / 2 + 10, 70, 30 + 23 * n, "#E0F2FE") + ELL(410, h / 2 + 10, 70, 30 + 23 * n, FILL2) + tag(150, 22, ttl[0], 16) + tag(410, 22, ttl[1], 16)
    ya = {a: 52 + 46 * i + (h - 70 - 46 * len(A)) / 2 + 20 for i, a in enumerate(A)}
    yb = {b: 52 + 46 * i + (h - 70 - 46 * len(B)) / 2 + 20 for i, b in enumerate(B)}
    for a, b in pairs:
        body += L(190, ya[a], 370, yb[b], NAVY, 3)
    for a in A: body += tag(150, ya[a], str(a), 16)
    for b in B: body += tag(410, yb[b], str(b), 16)
    return wrap(560, h + 30, body, "Diagrama de flechas de una función")


# ---------------------------------------------------------------- Resolver
def t_inv_value(r, l):
    if l == 0:
        a = r.choice([2, 3, 4, 5, -2, -3]); b = r.randint(-9, 9); x0 = r.randint(-6, 8)
        k = a * x0 + b
        stem = f"Sea f(x) = {lx(a, b)}. ¿Cuánto vale {INV}({k})?"
        cands = [a * k + b, F(k - b, a) + 1 if True else 0, (k + b) // a if (k + b) % a == 0 else k + b, a * (k - b), k - b, -x0, x0 + 1]
        fx = f"f(x) = {lx(a, b)}"
    elif l == 1:
        if r.random() < 0.5:
            b, x0 = r.choice([2, 3, 4]), r.randint(-6, 8); a = r.randint(-5, 8)
            k = F(x0 + a, b)
            if k.denominator != 1: raise Reject
            fx = f"f(x) = (x {'+' if a >= 0 else '−'} {abs(a)})/{b}"
            cands = [b * k - a if False else b * int(k) + a, int(k) * b, int(k) + a, x0 + 1, -x0, int(k) * b - a + 1]
            k = int(k)
        else:
            c, x0 = r.randint(-9, 9), r.randint(-4, 4)
            k = x0 ** 3 + c
            fx = f"f(x) = x³ {'+' if c >= 0 else '−'} {abs(c)}"
            cands = [k ** 3 + c, k - c, x0 + 1, -x0, k + c, (k - c) // 3 if (k - c) % 3 == 0 else k - c + 1]
        stem = f"Sea {fx}. ¿Cuánto vale {INV}({k})?"
    else:
        for _ in range(60):
            a, b, x0 = r.randint(-5, 6), r.randint(-4, 5), r.randint(-6, 8)
            if x0 == b or a == -b: continue
            k = F(x0 + a, x0 - b)
            if k.denominator == 1 and k != 1: break
        else:
            raise Reject
        k = int(k)
        fx = f"f(x) = (x {'+' if a >= 0 else '−'} {abs(a)})/(x {'−' if b > 0 else '+'} {abs(b)})".replace("(x − 0)", "x").replace("(x + 0)", "x")
        stem = f"Sea {fx}. ¿Cuánto vale {INV}({k})?"
        cands = [F(k + a, k - b) if k != b else x0 + 2, x0 + 1, x0 - 1, -x0, b, a, k]
    ans = str(x0)
    cands = [fs(c) if not isinstance(c, str) else c for c in cands]
    return make(stem, machine(("x", "y"), "f", ("x", "y")), ans, pick4(ans, cands), Q_RES, f"{INV}({k}) = x cumple f(x) = {k}; resolviendo se obtiene x = {x0}.")


def t_table(r, l):
    n = 4 if l < 2 else 5
    els = sorted(r.sample(range(1, 15), n))
    img = els[:]
    while img == els or (l == 0 and False):
        r.shuffle(img)
    f = dict(zip(els, img))
    inv = {v: k for k, v in f.items()}
    txt = ", ".join(f"f({a}) = {b}" for a, b in f.items())
    if l == 0:
        y = r.choice(els)
        ans, q = inv[y], f"{INV}({y})"
        stem = f"La función f: A → A es biyectiva y sus valores son: {txt}. ¿Cuánto vale {q}?"
        cands = [f[y], y, r.choice([e for e in els if e != inv[y]]), inv[y] + 1, max(f.values()) + 1, els[0] if els[0] != inv[y] else els[-1]]
    elif l == 1:
        a, b = r.choice(els), r.choice(els)
        ans = f[inv[a]] + inv[f[b]]
        q = f"f({INV}({a})) + {INV}(f({b}))"
        stem = f"La función f: A → A es biyectiva y sus valores son: {txt}. ¿Cuánto vale {q}?"
        cands = [a + f[b], f[a] + inv[b], a + b + 1, inv[a] + f[b], a + inv[b], f[a] + f[b]]
    else:
        y = r.choice(els)
        ans = inv[inv[y]]
        q = f"{INV}({INV}({y}))"
        stem = f"La función f: A → A es biyectiva y sus valores son: {txt}. ¿Cuánto vale {q}?"
        cands = [f[f[y]], f[y], inv[y], y, inv[inv[inv[y]]], f[inv[y]] + 1]
    cands = [str(c) for c in cands]
    return make(stem, map_fig(els, els, list(f.items())), str(ans), pick4(str(ans), cands), Q_RES, f"Se lee el diagrama al revés: {INV}(b) = a cuando f(a) = b.")


# ---------------------------------------------------------------- Modelar
def mm(n):
    return f"{int(n):,}".replace(",", ".")


def t_context(r, l):
    if l == 0:
        f_, p, d = r.choice([500, 800, 1000, 1200, 1500, 2000]), r.choice([300, 400, 500, 600, 700, 800]), r.randint(2, 20)
        T = f_ + p * d
        stem = f"Un taxi cobra ${mm(f_)} de bajada de bandera más ${mm(p)} por kilómetro. Si un viaje costó ${mm(T)}, ¿cuántos kilómetros se recorrieron?"
        ans = f"{d} km"
        cands = [f"{T // p} km", f"{d + f_ // p} km" if f_ % p == 0 else f"{d + 1} km", f"{d - 1} km", f"{(T + f_) // p} km" if (T + f_) % p == 0 else f"{d + 2} km", f"{d + 2} km", f"{T // (f_ + p)} km"]
        fig = machine(("km", "$"), "tarifa", ("$", "km"))
        ex = f"T = {f_} + {p}d ⟹ d = (T − {f_})/{p} = {d}."
    elif l == 1:
        if r.random() < 0.5:
            C = r.randint(-10, 40)
            Fh = F(9 * C, 5) + 32
            if Fh.denominator != 1: raise Reject
            stem = f"La temperatura en grados Fahrenheit se calcula con F = (9/5)·C + 32, donde C es la temperatura en °C. ¿Cuántos °C corresponden a {int(Fh)} °F?"
            ans = f"{C} °C"
            cands = [f"{F(9 * int(Fh), 5) + 32:g} °C" if False else f"{int(F(9 * int(Fh), 5)) + 32} °C" if (9 * int(Fh)) % 5 == 0 else f"{C + 5} °C", f"{int(Fh) - 32} °C", f"{C - 5} °C", f"{-C} °C", f"{(int(Fh) + 32) * 5 // 9} °C", f"{C + 9} °C"]
            fig = machine(("°C", "°F"), "9/5·C + 32", ("°F", "°C"))
            ex = f"C = (F − 32)·5/9 = {C}."
        else:
            rate, fee, d = r.choice([800, 900, 950, 1000]), r.choice([1000, 2000, 3000]), r.randint(3, 40)
            X = rate * d - fee
            stem = f"Una casa de cambio entrega ${mm(rate)} por cada dólar, pero descuenta una comisión fija de ${mm(fee)}. Si un cliente recibió ${mm(X)}, ¿cuántos dólares cambió?"
            ans = f"{d} dólares"
            cands = [f"{(X - fee) // rate} dólares" if (X - fee) % rate == 0 else f"{d - 1} dólares", f"{X // rate} dólares" if X % rate == 0 else f"{d + 1} dólares", f"{d - 2} dólares", f"{d + 2} dólares", f"{d + fee // rate} dólares", f"{d - 3} dólares"]
            fig = machine(("US$", "$"), "cambio", ("$", "US$"))
            ex = f"X = {rate}d − {fee} ⟹ d = (X + {fee})/{rate} = {d}."
    else:
        p = r.choice([10000, 20000, 25000, 40000, 50000, 80000, 100000, 125000])
        dsc = r.choice([20, 25, 40])
        Fp = p * F(100 - dsc, 100) * F(119, 100)
        if Fp.denominator != 1: raise Reject
        stem = f"Un artículo tiene un {dsc}% de descuento y luego se le suma 19% de IVA. Si el cliente pagó ${mm(Fp)}, ¿cuál era el precio original?"
        ans = f"${p:,}".replace(",", ".")
        alts = [Fp * F(100 + dsc, 100) / F(119, 100), Fp / F(119, 100), Fp * F(100, 100 - dsc), Fp * (1 + F(dsc, 100)) * F(81, 100), Fp / F(100 - dsc, 100), Fp - Fp * F(19 - dsc, 100)]
        cands = [f"${int(x):,}".replace(",", ".") if F(x).denominator == 1 else f"${p + 5000:,}".replace(",", ".") for x in alts]
        fig = machine(("p", "F"), "×0,8·1,19".replace("0,8", f"{(100 - dsc) / 100:g}".replace(".", ",")), ("F", "p"))
        ex = f"F = p·{(100 - dsc) / 100:g}·1,19 ⟹ p = F/{float((100 - dsc) * 119) / 10000:g}.".replace(".", ",")
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


def t_phys(r, l):
    if l == 0:
        if r.random() < 0.5:
            s = r.randint(2, 15)
            stem = f"El área de un cuadrado es {s * s} cm². ¿Cuánto mide su lado?"
            ans = f"{s} cm"
            cands = [f"{s * s // 2} cm" if (s * s) % 2 == 0 else f"{s + 1} cm", f"{s * 2} cm", f"{s + 1} cm", f"{s - 1} cm", f"{s * s} cm", f"{4 * s} cm"]
            fig = machine(("lado", "área"), "A = s²", ("área", "lado"))
        else:
            s = r.randint(2, 8)
            stem = f"El volumen de un cubo es {s ** 3} cm³. ¿Cuánto mide su arista?"
            ans = f"{s} cm"
            cands = [f"{s ** 3 // 3} cm" if s ** 3 % 3 == 0 else f"{s + 2} cm", f"{s * 3} cm", f"{s + 1} cm", f"{s - 1} cm", f"{s ** 2} cm", f"{s ** 3 // 6} cm" if s ** 3 % 6 == 0 else f"{s + 3} cm"]
            fig = machine(("arista", "vol."), "V = a³", ("vol.", "arista"))
        ex = "Se invierte la relación de potencia con una raíz."
    elif l == 1:
        t = r.randint(2, 9)
        d = 5 * t * t
        stem = f"La distancia (en m) que cae un objeto en t segundos es d = 5t². ¿Cuántos segundos tarda en caer {d} m?"
        ans = f"{t} s"
        cands = [f"{d // 5} s", f"{d // 10} s" if d % 10 == 0 else f"{t + 1} s", f"{t + 1} s", f"{t - 1} s", f"{d // 25} s" if d % 25 == 0 else f"{t + 2} s", f"{2 * t} s"]
        fig = machine(("t", "d"), "d = 5t²", ("d", "t"))
        ex = f"t = √(d/5) = √{d // 5} = {t}."
    else:
        c = r.choice([4, 5, 6, 7, 8, 10])
        x0 = r.randint(1, c - 1)
        Rv = x0 * (2 * c - x0)
        stem = f"El ingreso de una empresa es R(x) = −x² + {2 * c}x, con 0 ≤ x ≤ {c} (x en miles de unidades). Si el ingreso fue {Rv}, ¿cuál fue el valor de x?"
        ans = str(x0)
        cands = [str(2 * c - x0), str(x0 + 1), str(x0 - 1) if x0 > 1 else str(x0 + 2), str(Rv // c), str(c + (c - x0)), str(Rv // (2 * c) + 1), str(x0 + 2)]
        pl = Plot(560, 270, 0, 2 * c, 0, c * c + 4)
        pl.axes(1 if c <= 5 else 2, max(1, round((c * c + 4) / 6)))
        pl.curve(lambda x: -x * x + 2 * c * x, 0, 2 * c, "#94A3B8", 3)
        pl.curve(lambda x: -x * x + 2 * c * x, 0, c, ACC, 5)
        pl.parts.append(tag(pl.X(c), pl.Y(c * c * 0.4), f"0 ≤ x ≤ {c} (invertible)", 15))
        fig, ex = pl.svg("Ingreso con dominio restringido"), f"−x² + {2 * c}x = {Rv} ⟹ x = {x0} o x = {2 * c - x0}; solo {x0} cumple x ≤ {c}."
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
FOUR = ["Es biyectiva", "Es inyectiva, pero no sobreyectiva", "Es sobreyectiva, pero no inyectiva", "No es inyectiva ni sobreyectiva", "No es una función"]


def hline(pl, y):
    pl.hline(y)


def t_bij_graph(r, l):
    opts = []
    a = r.choice([1, 2, -1, -2]); b = r.randint(-3, 3)
    opts.append(("ℝ", "ℝ", lambda x: a * x + b, -4, 4, 0, (-9, 9)))
    opts.append(("ℝ", "ℝ", lambda x: (x - b) ** 3 / 3, -4, 4, 0, (-9, 9)))
    opts.append(("ℝ", "ℝ", lambda x: x * x - 4 + b, -4, 4, 3, (-6, 9)))
    if l >= 1:
        opts.append(("ℝ", "ℝ", lambda x: 2 ** x, -4, 4, 3, (-4, 9)))
        opts.append(("ℝ", "ℝ", lambda x: x ** 3 / 2 - 3 * x / 2, -3, 3, 1, (-6, 6)))
    if l == 0:
        opts = opts[:3]
    idx = r.randrange(len(opts))
    ans_i = [0, 0, 3, 1, 2][idx] if l else [0, 0, 3][idx]
    dom, cod, f, x0, x1, _, yr = opts[idx]
    pl = Plot(560, 270, x0, x1, yr[0], yr[1])
    pl.axes(1, max(1, round((yr[1] - yr[0]) / 6)))
    pl.curve(f, x0, x1)
    yline = r.choice([2, 3]) if idx in (2, 3) else 2
    pl.hline(yline)
    pl.parts.append(tag(pl.X(x1) - 55, pl.Y(yline) - 18, f"y = {yline}", 14))
    stem = f"La gráfica corresponde a una función f: {dom} → {cod}. La línea punteada es una recta horizontal de prueba. ¿Cuál afirmación es correcta?"
    return make(stem, pl.svg("Gráfica con recta horizontal de prueba"), FOUR[ans_i], [x for i, x in enumerate(FOUR) if i != ans_i], Q_REP,
                "Una función es inyectiva si toda recta horizontal la corta a lo más una vez, y sobreyectiva si toda recta horizontal (dentro del codominio) la corta al menos una vez.")


def t_bij_domain(r, l):
    cases = [
        ("[0, +∞[", "ℝ", lambda x: x * x, 0, 4, (-2, 9), 1),         # inj no sobre
        ("[0, +∞[", "[0, +∞[", lambda x: x * x, 0, 4, (-2, 9), 0),   # biyectiva
        ("ℝ", "[0, +∞[", lambda x: x * x, -4, 4, (-2, 9), 2),        # sobre no inj
        ("ℝ", "[0, +∞[", lambda x: abs(x), -5, 5, (-2, 6), 2),
        ("ℝ", "ℝ", lambda x: abs(x), -5, 5, (-2, 6), 3),
        ("ℝ", "]0, +∞[", lambda x: 2 ** x, -4, 4, (-1, 9), 0),
        ("ℝ", "ℝ", lambda x: 2 ** x, -4, 4, (-1, 9), 1),
        ("[0, +∞[", "[0, +∞[", lambda x: sqrt(x), 0, 9, (-1, 5), 0),
        ("[0, +∞[", "ℝ", lambda x: sqrt(x), 0, 9, (-3, 5), 1),
    ]
    dom, cod, f, x0, x1, yr, k = r.choice(cases)
    h = r.choice([0, 0, 1, 2]) if False else 0
    pl = Plot(560, 270, min(x0, -1), x1 + 0.5, yr[0], yr[1])
    pl.axes(1, max(1, round((yr[1] - yr[0]) / 6)))
    pl.curve(f, x0, x1)
    pl.hline(2)
    pl.parts.append(tag(pl.X(x1) - 40, pl.Y(2) - 18, "y = 2", 14))
    stem = f"Se grafica la función f: {dom} → {cod}, con la regla que se muestra. ¿Cuál afirmación es correcta?"
    return make(stem, pl.svg("Gráfica de una función con dominio y codominio dados"), FOUR[k], [x for i, x in enumerate(FOUR) if i != k], Q_REP,
                "Se analiza si la gráfica cubre todo el codominio (sobreyectiva) y si cada horizontal la corta una sola vez (inyectiva).")


def t_inv_graph(r, l):
    if l < 2:
        m = r.choice([1, 2, 3, -1, -2]) if l == 0 else r.choice([2, 3, -2, -3, 1, -1, 4])
        b = r.randint(-4, 4)
        f = lambda x: m * x + b
        pl = Plot(560, 280, -6, 6, -6, 6)
        pl.axes(2, 2)
        pl.curve(lambda x: x, -6, 6, "#64748B", 2.5)
        pl.curve(f, -6, 6)
        pl.pt(0, b, f"(0, {b})", dx=45, dy=-24)
        pl.pt(1, m + b, f"(1, {m + b})", dx=-40 if m > 0 else 45, dy=-24 if m > 0 else 24)
        ans = f"{INV}(x) = " + invlin(m, b)
        cands = [f"{INV}(x) = " + x for x in (invlin(m, -b) if m > 0 else lx(-1, -b), f"{m}({lx(1, -b)})" if b else f"{m}x", lx(1, -b).replace("x", f"x/{m}") if m > 0 else lx(-1, b) + f"/{-m}", lx(m, -b), f"1/({lx(m, b)})", invlin(-m, b) if m != -m else lx(1, b))]
        cands = [c for c in cands]
        stem = "La figura muestra la gráfica de una función lineal f (roja) y la recta y = x (gris). ¿Cuál es la ecuación de la función inversa?"
        ex = f"f(x) = {lx(m, b)}; se despeja x en y = {lx(m, b)} y se intercambian las variables."
    else:
        h, k = r.randint(1, 5), r.randint(-4, 3)
        f = lambda x: (x - h) ** 2 + k
        pl = Plot(560, 280, -1, 9, -2, 9)
        pl.axes(1, 1)
        pl.curve(lambda x: x, -1, 9, "#64748B", 2.5)
        pl.curve(f, h, 9, ACC, 5)
        pl.pt(h, k, f"({h}, {k})", dx=50, dy=26)
        inner = lx(1, -k)
        ans = f"{INV}(x) = {h} + √({inner})" if k != 0 else f"{INV}(x) = {h} + √x"
        rad = lambda s_: f"√({s_})" if s_ != "x" else "√x"
        cands = [f"{INV}(x) = {h} − {rad(inner)}", f"{INV}(x) = −{h} + {rad(inner)}", f"{INV}(x) = {h} + {rad(lx(1, k))}", f"{INV}(x) = {rad(lx(1, -h))} + {k}", f"{INV}(x) = {h} + {rad('x')} − {k}" if k else f"{INV}(x) = {h} + {rad('x + 1')}"]
        stem = f"La función f, de gráfica roja, es un tramo de una parábola con vértice en ({h}, {k}) y dominio x ≥ {h}. ¿Cuál es la ecuación de su inversa?"
        ex = f"y = (x − {h})² + {k} con x ≥ {h} ⟹ x = {h} + √(y − {k})."
    return make(stem, pl.svg("Función y la recta y = x"), ans, pick4(ans, cands), Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
def gen_fun(r, l, inv):
    if inv:
        c = r.choice(["lin", "cub", "cub2", "cub3"] + (["tri1", "tri2"] if l == 2 else []))
        if c == "lin":
            a = r.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]); return lx(a, r.randint(-9, 9))
        if c == "cub":
            b = r.randint(-9, 9); return "x³" + (f" + {b}" if b > 0 else f" − {-b}" if b < 0 else "")
        if c == "cub2":
            h = r.choice([x for x in range(-4, 5) if x]); k = r.randint(-5, 5)
            return f"(x {'−' if h > 0 else '+'} {abs(h)})³" + (f" + {k}" if k > 0 else f" − {-k}" if k < 0 else "")
        if c == "cub3":
            a = r.randint(2, 9); return f"{a} − x³"
        if c == "tri1":
            a = r.randint(1, 4); return f"x³ + {a}x"
        return f"x|x| + {r.randint(1, 5)}"
    c = r.choice(["quad", "quad2", "abs", "const"] + (["quart", "cub"] if l >= 1 else []) + (["cubb", "even"] if l == 2 else []))
    if c == "quad":
        h = r.randint(-5, 5); k = r.randint(-5, 5)
        return (f"(x {'−' if h > 0 else '+'} {abs(h)})²" if h else "x²") + (f" + {k}" if k > 0 else f" − {-k}" if k < 0 else "")
    if c == "quad2":
        b, cc = r.choice([-6, -4, -2, 2, 4, 6]), r.randint(-6, 6)
        return f"x² {'+' if b > 0 else '−'} {abs(b)}x" + (f" + {cc}" if cc > 0 else f" − {-cc}" if cc < 0 else "")
    if c == "abs":
        h = r.randint(-4, 4); return f"|x {'−' if h > 0 else '+'} {abs(h)}|" if h else "|x|"
    if c == "const":
        return str(r.randint(-5, 9))
    if c == "quart":
        return f"x⁴ + {r.randint(1, 9)}"
    if c == "cub":
        cc = r.choice([1, 2, 3, 4]); return "x³ − " + ("" if cc == 1 else str(cc)) + "x²"
    if c == "cubb":
        a = r.randint(1, 5); return f"x³ − {a}x"
    return f"x²|x| + {r.randint(1, 4)}"


def t_which_inv(r, l):
    goods, bads = set(), set()
    for _ in range(80):
        goods.add("f(x) = " + gen_fun(r, l, True)); bads.add("f(x) = " + gen_fun(r, l, False))
    good = r.choice(sorted(goods)); bad = r.sample(sorted(bads), 4)
    fig = machine(("x", "y"), "f", ("y", "x"))
    return make("¿Cuál de las siguientes funciones f: ℝ → ℝ es biyectiva y, por lo tanto, tiene función inversa en todo ℝ?", fig, good, bad, Q_ARG,
                "Una función es invertible si es inyectiva y sobreyectiva: las que tienen tramos crecientes y decrecientes o valores repetidos no lo son.")


def t_restrict(r, l):
    h = r.randint(2, 9)
    if l == 0:
        k = 0; eq = f"(x − {h})²"
    elif l == 1:
        k = r.randint(-5, 5); eq = f"(x − {h})²" + (f" + {k}" if k > 0 else f" − {-k}" if k < 0 else "")
    else:
        b = -2 * h; c = h * h + r.randint(-5, 5)
        k = c - h * h; eq = f"x² − {2 * h}x" + (f" + {c}" if c > 0 else f" − {-c}" if c < 0 else "")
    side = r.choice(["≥", "≤"])
    ans = f"x {side} {h}"
    cands = [f"x {'≤' if side == '≥' else '≥'} 0" if False else "x ≥ 0", f"x ≥ {h - 2}", f"x ≤ {h + 2}", "x ∈ ℝ", f"x ≠ {h}", f"x ≥ {k}" if k != h else f"x ≥ {h - 1}"]
    if side == "≥": cands = [c_ for c_ in cands if c_ != "x ≤ 0"]
    fx = f"f(x) = {eq}"
    pl = Plot(560, 250, -1, 2 * h + 1, min(-2, k - 2), max((h + 1) ** 2 + k, 8) if h < 5 else 26)
    pl.axes(max(1, (2 * h + 2) // 8), max(1, round((pl.y1 - pl.y0) / 6)))
    pl.curve(lambda x: (x - h) ** 2 + k, -1, 2 * h + 1)
    pl.parts.append(tag(pl.X(h), pl.Y(k) - 34, f"vértice ({h}, {k})".replace("-", "−"), 15))
    return make(f"Sea {fx}. ¿Cuál de los siguientes dominios hace que f sea inyectiva y, por lo tanto, invertible sobre su recorrido?", pl.svg("Parábola y su vértice"), ans, pick4(ans, cands), Q_ARG,
                f"El vértice está en x = {h}: se elige una de las dos ramas, x {side} {h}, para que no haya valores repetidos.")


TRUE_F = ["Si f es biyectiva, f⁻¹ también es biyectiva", "Si f(a) = b, entonces f⁻¹(b) = a", "El dominio de f⁻¹ es el recorrido de f",
          "Las gráficas de f y f⁻¹ son simétricas respecto de la recta y = x", "(f⁻¹∘f)(x) = x para todo x del dominio de f", "Una función estrictamente creciente es inyectiva"]
FALSE_F = ["f⁻¹(x) = 1/f(x) para toda función invertible", "Toda función real tiene función inversa", "Si f(a) = b, entonces f⁻¹(a) = b",
           "Las gráficas de f y f⁻¹ son simétricas respecto del eje Y", "Si f no es inyectiva, f⁻¹ existe igualmente", "El recorrido de f⁻¹ es el recorrido de f",
           "Si f es par y no constante, entonces f es inyectiva"]


def t_inv_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_F), r.sample(FALSE_F, 4)
        stem = "Sea f una función invertible. ¿Cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_F), r.sample(TRUE_F, 4)
        stem = "Sea f una función invertible. ¿Cuál de las siguientes afirmaciones es FALSA?"
        stem = stem.replace("Sea f una función invertible.", "Sobre las funciones y sus inversas,")
    a, b = r.sample(range(1, 9), 2)
    fig = map_fig([a], [b], [(a, b)], ("dominio de f", "recorrido de f"))
    return make(stem, fig, good, bad, Q_ARG, "Se revisa cada afirmación con la definición de función inversa y ejemplos simples.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_find_inv(r, l):
    if l == 0:
        m = r.choice([2, 3, 4, 5, -1, -2, -3]); b = r.randint(-8, 8)
        fx, ans, cands = f"f(x) = {lx(m, b)}", f"{INV}(x) = " + invlin(m, b), None
        cands = [f"{INV}(x) = " + x for x in (invlin(m, -b) if m > 0 else lx(-1, -b), f"{m}({lx(1, -b)})" if b else f"{m}x", lx(1, -b) + f"/{m}" if False else (f"x/{m} − {b}" if b > 0 else f"x/{m} + {-b}" if b < 0 else f"x/{m} + 1"), lx(m, -b), f"1/({lx(m, b)})", invlin(-m, b) if m != -m else lx(1, b))]
    elif l == 1:
        c = r.choice([x for x in range(-8, 9) if x]); n = r.choice([3, 5])
        exp = "³" if n == 3 else "⁵"
        fx = f"f(x) = x{exp} {'+' if c > 0 else '−'} {abs(c)}"
        root = "∛" if n == 3 else "⁵√"
        ans = f"{INV}(x) = {root}({lx(1, -c)})"
        cands = [f"{INV}(x) = {root}({lx(1, c)})", f"{INV}(x) = {root}x {'+' if c > 0 else '−'} {abs(c)}", f"{INV}(x) = ({lx(1, -c)}){exp}", f"{INV}(x) = 1/(x{exp} {'+' if c > 0 else '−'} {abs(c)})", f"{INV}(x) = {root}({lx(1, -c)})".replace(root, "√") if n == 3 else f"{INV}(x) = √({lx(1, -c)})"]
    else:
        a, d = r.randint(-4, 5), r.randint(-4, 5)
        bb = r.randint(-5, 5)
        if a * d + bb == 0 or a == 0: raise Reject
        # f(x) = (a x + b)/(x + d) → f⁻¹(x) = (b − d x)/(x − a)
        fx = f"f(x) = ({lx(a, bb)})/({lx(1, d)})"
        num = lx(-d, bb)
        den = lx(1, -a)
        ans = f"{INV}(x) = ({num})/({den})"
        cands = [f"{INV}(x) = ({lx(d, bb)})/({den})", f"{INV}(x) = ({num})/({lx(1, a)})", f"{INV}(x) = ({lx(d, -bb)})/({den})", f"{INV}(x) = ({lx(1, d)})/({lx(a, bb)})", f"{INV}(x) = ({lx(-a, bb)})/({lx(1, -d)})"]
    return make(f"Determina la función inversa de {fx}.", card([fx, "Se despeja x en y = f(x) y se intercambian x e y"], 190, 20), ans, pick4(ans, cands), Q_PRO,
                "Se despeja x en términos de y y luego se intercambian las variables.")


def t_domain_inv(r, l):
    if l == 0:
        a = r.randint(1, 9)
        fx, kind = f"f(x) = √(x − {a})", ("dom", f"x ≥ 0")
        dom_f, rec_f = I(a, True, None, False), I(0, True, None, False)
    elif l == 1:
        a, k = r.randint(-4, 6), r.choice([x for x in range(-5, 6) if x])
        fx = f"f(x) = √({lx(1, -a)}) {'+' if k > 0 else '−'} {abs(k)}".replace("√(x)", "√x")
        dom_f, rec_f = I(a, True, None, False), I(k, True, None, False)
    else:
        h, k = r.randint(1, 8), r.randint(-5, 5)
        side = r.choice(["≥", "≤"])
        fx = f"f(x) = (x − {h})² {'+' if k >= 0 else '−'} {abs(k)}, con x {side} {h}"
        dom_f = I(h, True, None, False) if side == "≥" else I(None, False, h, True)
        rec_f = I(k, True, None, False)
    ask_dom = r.random() < 0.6
    target = rec_f if ask_dom else dom_f
    what = "el dominio" if ask_dom else "el recorrido"
    ans = fi(target)
    cands = [fi(dom_f if ask_dom else rec_f), fi(I(target.lo, not target.lc, target.hi, target.hc)) if target.lo is not None else fi(I(target.lo, False, target.hi, not target.hc)),
             fi(I(None, False, target.lo, True)) if target.lo is not None else fi(I(target.hi, True, None, False)), "ℝ", fi(I(None if target.lo is None else -target.lo, target.lc, None, False)) if target.lo is not None else fi(I(None, False, -target.hi, True))]
    return make(f"Sea {fx}. ¿Cuál es {what} de la función inversa {INV}?", card([fx, f"{what.capitalize()} de {INV} = " + ("recorrido de f" if ask_dom else "dominio de f")], 200, 20), ans, pick4(ans, cands), Q_PRO,
                f"{what.capitalize()} de {INV} coincide con el {'recorrido' if ask_dom else 'dominio'} de f: {ans}.")


BY_SKILL = {
    Q_RES: [t_inv_value, t_table],
    Q_MOD: [t_context, t_phys],
    Q_REP: [t_bij_graph, t_bij_domain, t_inv_graph],
    Q_ARG: [t_which_inv, t_restrict, t_inv_props],
    Q_PRO: [t_find_inv, t_domain_inv],
}
