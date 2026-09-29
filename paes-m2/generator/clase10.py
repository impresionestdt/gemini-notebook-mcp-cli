"""Clase 10 · Función exponencial: modelos de crecimiento y decaimiento."""
from fractions import Fraction as F
from math import log
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO

SUPX = str.maketrans("0123456789+-−x()", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻ˣ⁽⁾")


def sp(s):
    return str(s).translate(SUPX)


def bs(b):
    b = F(b)
    return str(b.numerator) if b.denominator == 1 else f"({b.numerator}/{b.denominator})"


def fexp(a=1, b=2, c=0, h=0):
    """a·b^(x − h) + c."""
    e = "x" if h == 0 else f"x{'−' if h > 0 else '+'}{abs(h)}"
    pre = "" if a == 1 else "−" if a == -1 else f"{a}·"
    s = f"{pre}{bs(b)}{sp(e)}"
    if c > 0: s += f" + {c}"
    elif c < 0: s += f" − {abs(c)}"
    return s


def nice(v):
    for c in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000):
        if c >= v:
            return c
    return int(v)


def plot(f, x0, x1, y0, y1, marks=(), extra=None, sx=1, sy=1, color=ACC):
    pl = Plot(560, 280, x0, x1, y0, y1)
    pl.axes(sx, nice(sy))
    if extra: extra(pl)
    pl.curve(f, x0, x1, color)
    for (x, y, lab, dx, dy) in marks:
        pl.pt(x, y, lab, dx=dx, dy=dy)
    return pl


def num(x):
    return fs(F(x).limit_denominator(10 ** 6))


# ---------------------------------------------------------------- Resolver
def t_params(r, l):
    if l == 0:
        b = r.choice([F(2), F(3), F(4), F(5), F(1, 2), F(1, 3)])
        p = r.choice([2, 3, -1, -2]) if b > 1 else r.choice([2, 3, -1, -2])
        q = b ** p
        stem = f"La función f(x) = bˣ, con b > 0 y b ≠ 1, pasa por el punto ({p}, {fs(q)}). ¿Cuál es el valor de b?"
        ans = num(b)
        cands = [num(F(q) / p if p else q), num(q - p), num(1 / b), num(abs(p) + 0 if abs(p) != 1 else b + 1), num(q), num(b + 1), num(b * 2)]
        f = lambda x: float(b) ** x
        yv = float(q)
        pl = plot(f, -3, 3, -1, 9, [(p, yv, f"({p}, {fs(q)})", 0, -28)], sy=2)
        ex = f"{fs(q)} = b^({p}) ⟹ b = {fs(q)}^(1/{p}) = {ans}."
    elif l == 1:
        a, b = r.choice([2, 3, 4, 5]), r.choice([F(2), F(3), F(4), F(1, 2), F(1, 3)])
        f0, f1 = a, a * b
        tgt = r.choice([2, 3])
        v = a * b ** tgt
        stem = f"Sea f(x) = a·bˣ, con f(0) = {fs(f0)} y f(1) = {fs(f1)}. ¿Cuánto vale f({tgt})?"
        ans = num(v)
        cands = [num(f1 * tgt), num(f0 + tgt * (f1 - f0)), num(f1 ** tgt), num(f1 + (f1 - f0)) if tgt == 2 else num(f1 * b + b), num(a * tgt * b), num(v + a), num(v * b)]
        f = lambda x: float(a) * float(b) ** x
        pl = plot(f, -2, 3, -1, max(8, min(60, float(v) * 1.4)), [(0, float(f0), f"(0, {fs(f0)})", -50, -22), (1, float(f1), f"(1, {fs(f1)})", 50, -24)], sy=max(1, round(min(60, float(v) * 1.4) / 6)))
        ex = f"a = {fs(f0)} y b = {fs(f1)}/{fs(f0)} = {num(b)}; f({tgt}) = {fs(f0)}·{num(b)}^{tgt} = {ans}."
    else:
        a, b = r.choice([1, 2, 3, 4, 5]), r.choice([2, 3, 4])
        f1, f3 = a * b, a * b ** 3
        what = r.choice(["f(0)", "f(4)", "f(2)"])
        v = {"f(0)": a, "f(4)": a * b ** 4, "f(2)": a * b * b}[what]
        stem = f"Sea f(x) = a·bˣ, con b > 0, f(1) = {f1} y f(3) = {f3}. ¿Cuánto vale {what}?"
        ans = str(v)
        cands = [str(f1 + (f3 - f1) // 2 * (2 if what == 'f(4)' else 1)) if True else "", str(f3 * 2 - f1), str(f3 + (f3 - f1) // 2), str(f1 // b if f1 % b == 0 else f1 - 1), str(f3 * b + b), str(v + a), str(v * b) if what != "f(4)" else str(f3 + f1), str(f3 // b) if what == "f(2)" else str(a * b)]
        f = lambda x: a * b ** x
        pl = plot(f, -1, 4, -1, min(400, a * b ** 4 * 1.1), [(1, f1, f"(1, {f1})", -50, -22), (3, f3, f"(3, {f3})", -55, -22)], sy=max(1, round(min(400, a * b ** 4 * 1.1) / 6)))
        ex = f"b² = {f3}/{f1} = {b * b} ⟹ b = {b}; a = {f1}/{b} = {a}; {what} = {v}."
    return make(stem, pl.svg("Gráfico de la función exponencial"), ans, pick4(ans, cands), Q_RES, ex)


def t_solve_exp(r, l):
    if l == 0:
        b, k = r.choice([2, 3, 5, 10]), r.randint(-3, 5)
        rhs = F(b) ** k
        stem = f"¿Para qué valor de x se cumple {b}ˣ = {fs(rhs)}?"
        ans = str(k)
        cands = [str(-k), str(k + 1), str(k - 1), fs(F(rhs) / b) if rhs.denominator == 1 else str(k * 2), str(b * k) if b * k != k else str(k + 2), fs(rhs)]
        f1, f2 = (lambda x: float(b) ** x), (lambda x: float(rhs))
    elif l == 1:
        p, i, j = r.choice([2, 3]), r.choice([1, 2, 3]), r.randint(1, 5)
        neg = r.random() < 0.4
        if i == j: raise Reject
        lhs = F(p ** i) if not neg else F(1, p ** i)
        base_txt = bs(lhs)
        rhs = F(p) ** j
        x = F(j, i) * (-1 if neg else 1)
        stem = f"¿Para qué valor de x se cumple {base_txt}ˣ = {fs(rhs)}?"
        ans = fs(x)
        cands = [fs(-x), fs(F(i, j) * (-1 if neg else 1)), fs(j - i), fs(x + 1), fs(F(j * i)), fs(F(rhs) / lhs) if False else fs(x * 2)]
        f1, f2 = (lambda t: float(lhs) ** t), (lambda t: float(rhs))
    else:
        p = r.choice([2, 3])
        i, j = r.choice([(1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2), (1, 4)])
        a, b = r.randint(-3, 3), r.randint(-3, 3)
        x = F(j * b - i * a, i - j)
        stem = f"¿Para qué valor de x se cumple {p ** i}^(x {'+' if a >= 0 else '−'} {abs(a)}) = {p ** j}^(x {'+' if b >= 0 else '−'} {abs(b)})?".replace("^(x + 0)", "ˣ").replace("^(x − 0)", "ˣ")
        stem = stem.replace("^(", "⁽").replace(")", "⁾") if False else stem
        ans = fs(x)
        cands = [fs(F(i * a - j * b, i - j)), fs(F(j * b - i * a, j - i)), fs(F(a - b, 1)), fs(x + 1), fs(F(j * b + i * a, i + j)), fs(F(i * a + j * b, i - j))]
        f1, f2 = (lambda t: float(p) ** (i * (t + a))), (lambda t: float(p) ** (j * (t + b)))
    pl = plot(f1, -4, 4, -1, 12, extra=lambda p_: p_.curve(f2, -4, 4, NAVY), sy=2)
    return make(stem, pl.svg("Dos expresiones exponenciales"), ans, pick4(ans, cands), Q_RES,
                "Se escriben ambos lados con la misma base y se igualan los exponentes.")


# ---------------------------------------------------------------- Modelar
def bars(vals, labels, top=None, fills=None):
    top = top or max(vals)
    n = len(vals)
    bw = min(90, 440 // n)
    gap = (520 - n * bw) / max(1, n - 1)
    body = L(20, 200, 540, 200, INK, 3)
    for i, (v, lab) in enumerate(zip(vals, labels)):
        x = 20 + i * (bw + gap)
        hh = 150 * v / top
        body += R(x, 200 - hh, bw, hh, FILL2 if lab.endswith("?") else FILL) + tag(x + bw / 2, 200 - hh - 16, lab, 15)
    return wrap(560, 235, body, "Gráfico de barras")


def t_model(r, l):
    if l == 0:
        kind = r.choice(["dup", "pct", "pct"])
        if kind == "dup":
            T = r.choice([2, 3, 4, 5, 6]); n = r.randint(2, 6); P0 = r.choice([10, 20, 50, 100, 200, 500])
            stem = f"Una colonia de {P0} bacterias se duplica cada {T} horas. ¿Cuántas bacterias habrá después de {n * T} horas?"
            v = P0 * 2 ** n; b = 2
            cands = [P0 * 2 * n, P0 + n * P0, P0 * 2 ** (n + 1), P0 * 2 ** (n - 1), P0 * n * T, P0 * 2 ** n + P0, P0 * 2 ** T]
            vals = [P0 * 2 ** i for i in range(min(n, 3) + 1)]
        else:
            r_ = r.choice([10, 20, 50, 100]); n = r.randint(2, 4); P0 = r.choice([1000, 2000, 5000, 10000, 20000, 40000, 100000])
            v = P0 * (1 + F(r_, 100)) ** n
            if v.denominator != 1: raise Reject
            stem = f"Una población de {P0:,} habitantes crece {r_}% cada año. ¿Cuántos habitantes habrá después de {n} años?".replace(",", ".")
            cands = [P0 * (1 + F(r_ * n, 100)), P0 * (1 + F(r_, 100)) ** (n - 1), P0 * (1 + F(r_, 100)) ** (n + 1), P0 + P0 * F(r_, 100), P0 * F(r_, 100) ** n if (P0 * F(r_, 100) ** n).denominator == 1 else P0 + 1000, P0 * n * (1 + F(r_, 100))]
            vals = [float(P0 * (1 + F(r_, 100)) ** i) for i in range(min(n, 3) + 1)]
        ans = f"{int(v):,}".replace(",", ".")
        cands = [f"{int(c):,}".replace(",", ".") if F(c).denominator == 1 else f"{int(v) + 500:,}".replace(",", ".") for c in cands]
        labs = [f"{int(x):,}".replace(",", ".") for x in vals] + ["?"]
        fig = bars([float(x) for x in vals] + [float(v)], labs, float(v))
        ex = "Cada período se multiplica por el factor de crecimiento: resultado " + ans + "."
    elif l == 1:
        if r.random() < 0.5:
            T, n, M0 = r.choice([2, 3, 4, 5, 8, 10]), r.randint(2, 5), r.choice([64, 80, 96, 160, 320, 640, 1280])
            v = F(M0, 2 ** n)
            stem = f"Una sustancia radiactiva tiene una vida media de {T} años (cada {T} años su masa se reduce a la mitad). Si hoy hay {M0} g, ¿cuántos gramos quedarán dentro de {n * T} años?"
            ans = f"{fs(v)} g"
            cands = [f"{fs(F(M0, 2 * n))} g", f"{fs(F(M0, 2 ** (n - 1)))} g", f"{fs(F(M0, 2 ** (n + 1)))} g", f"{fs(M0 - n * T)} g", f"{fs(F(M0, n * T))} g", f"{fs(M0 // 2)} g"]
            vals = [float(F(M0, 2 ** i)) for i in range(min(n, 3) + 1)]
            labs = [f"{fs(F(M0, 2 ** i))}" for i in range(min(n, 3) + 1)] + ["?"]
            fig = bars(vals + [float(v)], labs, vals[0])
            ex = f"Después de {n} vidas medias: {M0}·(1/2)^{n} = {fs(v)} g."
        else:
            r_ = r.choice([10, 20, 25, 50]); n = r.randint(2, 4); V0 = r.choice([2000000, 4000000, 8000000, 10000000, 16000000])
            v = V0 * (1 - F(r_, 100)) ** n
            if v.denominator != 1: raise Reject
            stem = f"Un vehículo de ${V0:,} pierde {r_}% de su valor cada año. ¿Cuánto vale después de {n} años?".replace(",", ".")
            f_ = lambda c: f"${int(c):,}".replace(",", ".")
            ans = f_(v)
            alts = [V0 * (1 - F(r_ * n, 100)), V0 * (1 - F(r_, 100)) ** (n - 1), V0 * (1 - F(r_, 100)) ** (n + 1), V0 * (1 + F(r_, 100)) ** n, V0 - V0 * F(r_, 100), V0 * F(r_, 100) ** n]
            cands = [f_(c) if F(c).denominator == 1 else f_(v + 100000) for c in alts]
            vals = [float(V0 * (1 - F(r_, 100)) ** i) for i in range(min(n, 3) + 1)]
            labs = [f"{int(V0 * (1 - F(r_, 100)) ** i / 1000):,}".replace(",", ".") + " mil" if (V0 * (1 - F(r_, 100)) ** i).denominator == 1 else "…" for i in range(min(n, 3) + 1)] + ["?"]
            fig = bars(vals + [float(v)], labs, vals[0])
            ex = f"V = {V0:,}·{1 - r_ / 100:g}^{n} = {ans}.".replace(",", ".")
    else:
        T = r.choice([2, 3, 4, 5]); t1 = r.randint(1, 5) * T; k = r.randint(1, 3)
        N1 = r.choice([100, 200, 400, 800, 1200])
        t2 = t1 + k * T
        if r.random() < 0.5:
            stem = f"El número de bacterias es N(t) = N₀·2^(t/{T}), con t en horas. Si N({t1}) = {N1}, ¿cuánto vale N({t2})?"
            v = N1 * 2 ** k
            cands = [N1 * 2 * k, N1 + k * N1, N1 * 2 ** (k + 1), N1 * 2 ** (k - 1) if k > 1 else N1 * 3, N1 * (t2 // t1) if t2 % t1 == 0 else N1 * 5, N1 * 2 ** (t2 - t1) if t2 - t1 < 8 else N1 * 7]
            ex = f"N({t2})/N({t1}) = 2^(({t2} − {t1})/{T}) = 2^{k}."
        else:
            t2 = t1 + k * T
            stem = f"La masa de una sustancia es M(t) = M₀·(1/2)^(t/{T}), con t en años. Si M({t1}) = {N1 * 2 ** 3} g, ¿cuánto vale M({t2})?"
            N1 = N1 * 2 ** 3
            v = F(N1, 2 ** k)
            cands = [F(N1, 2 * k), N1 - k * (N1 // 2), F(N1, 2 ** (k + 1)), F(N1, 2 ** (k - 1)) if k > 1 else N1 * 2, F(N1, k * T), N1 - k * T]
            ex = f"M({t2})/M({t1}) = (1/2)^{k}."
        ans = fs(v)
        cands = [fs(c) for c in cands]
        xs = [t1, t2]
        pl = plot(lambda t: float(N1) * 2 ** ((t - t1) / T if isinstance(v, int) else -(t - t1) / T), max(0, t1 - 2 * T), t2 + T, 0, float(v) * 1.5 if isinstance(v, int) else N1 * 1.6, [(t1, float(N1), f"({t1}, {fs(N1)})", 0, -28)], sx=max(1, T), sy=max(1, round((float(v) * 1.5 if isinstance(v, int) else N1 * 1.6) / 6)))
        fig = pl.svg("Modelo exponencial")
        return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


def t_table_model(r, l):
    if l == 0:
        a = r.choice([1, 2, 3, 5, 10]); b = r.choice([2, 3])
        b_ = F(b)
    elif l == 1:
        a = r.choice([4, 8, 16, 32, 64, 100]); b_ = r.choice([F(1, 2), F(3, 2), F(1, 2), F(5, 2), F(1, 3) if a % 3 == 0 else F(1, 2)])
    else:
        a = r.choice([100, 200, 400, 1000]); b_ = r.choice([F(6, 5), F(11, 10), F(3, 5), F(9, 10), F(5, 4), F(3, 4)])
    ts = [0, 1, 2, 3]
    ys = [a * b_ ** t for t in ts]
    if any(v.denominator != 1 for v in ys[:3]): raise Reject
    ans = "f(t) = " + (f"{a}·" if a != 1 else "") + f"{bs(b_)}" + "ᵗ"
    d = b_ - 1
    cands = ["f(t) = " + (f"{a}·" if a != 1 else "") + f"{bs(1 / b_)}ᵗ", f"f(t) = {a} + {fs(a * d)}t".replace("+ −", "− "), f"f(t) = {a}·{bs(b_)}·t", f"f(t) = {fs(a * b_)}·{bs(b_)}ᵗ",
             f"f(t) = {a}·{bs(F(1) + d * 2)}ᵗ" if d * 2 + 1 != b_ and d * 2 + 1 > 0 else f"f(t) = {a}·{bs(b_ + 1)}ᵗ", f"f(t) = {a}·tᵇ".replace("tᵇ", f"t{'²' if True else ''}")]
    cands = [c.replace("f(t) = 1·", "f(t) = ") for c in cands]
    n = 3
    tb = R(30, 50, 500, 50, "#E0F2FE") + R(30, 100, 500, 50, WHITE)
    w = 500 / 5
    tb += T(30 + w / 2, 83, "t", 22) + T(30 + w / 2, 133, "f(t)", 20)
    for i, (t, y) in enumerate(zip(ts, ys)):
        tb += T(30 + w * (i + 1.5), 83, str(t), 20) + T(30 + w * (i + 1.5), 133, fs(y), 20)
    for i in range(6): tb += L(30 + w * i, 50, 30 + w * i, 150, NAVY, 2)
    stem = "La tabla muestra los valores de una magnitud que sigue un modelo exponencial f(t) = a·bᵗ. ¿Cuál es la función?"
    return make(stem, wrap(560, 190, tb, "Tabla de valores"), ans, pick4(ans, cands), Q_MOD,
                f"f(0) = a = {a} y el cociente entre valores consecutivos es b = {fs(b_)}.")


# ---------------------------------------------------------------- Representar
def t_graph_formula(r, l):
    if l == 0:
        a, b, c = 1, r.choice([F(2), F(3), F(1, 2), F(1, 3), F(4)]), 0
    elif l == 1:
        a, b, c = r.choice([2, 3, 4, 5]), r.choice([F(2), F(3), F(1, 2)]), 0
    else:
        a, b, c = r.choice([1, 2, 3]), r.choice([F(2), F(3), F(1, 2)]), r.choice([-3, -2, -1, 1, 2, 3])
    f = lambda x: float(a) * float(b) ** x + c
    y0v, y1v = a + c, a * b + c
    ymax = max(8, float(max(y0v, y1v)) * 1.6)
    ylo = min(-2, c - 2)
    def extra(p):
        if c != 0:
            p.hline(c)
            p.parts.append(tag(p.X(-2.6 + 0.0), p.Y(c) + (22 if c > 0 else -22), f"asíntota y = {c}".replace("-", "−"), 14))
    pl = plot(f, -3, 3, ylo, ymax, [(0, float(y0v), f"(0, {fs(y0v)})", 55, -6), (1, float(y1v), f"(1, {fs(y1v)})", 55, 16)], extra=extra, sy=max(1, round((ymax - ylo) / 6)))
    ans = "f(x) = " + fexp(a, b, c)
    cands = ["f(x) = " + fexp(a, 1 / b, c), "f(x) = " + fexp(a, b, -c) if c else "f(x) = " + fexp(a + 1, b, c), "f(x) = " + fexp(b if False else int(F(y1v - c)) if F(y1v - c).denominator == 1 else a + 1, F(1) if False else b, c), "f(x) = " + fexp(a, b + 1, c), "f(x) = " + fexp(a + c, b, 0) if c else "f(x) = " + fexp(a, F(b.numerator + 1, b.denominator) if b.denominator == 1 else b + 1, c), "f(x) = " + fexp(a, b, c + 1)]
    cands = [x for x in dict.fromkeys(cands)]
    return make("La figura muestra la gráfica de una función f(x) = a·bˣ + c, con los puntos indicados. ¿Cuál es su ecuación?", pl.svg("Gráfico de una función exponencial"), ans, pick4(ans, cands), Q_REP,
                f"El punto (0, {fs(y0v)}) y el (1, {fs(y1v)}) determinan a, b y c: f(x) = {fexp(a, b, c)}.")


def find_label(f, x0, x1, y0, y1, side):
    xs = [x0 + (x1 - x0) * i / 200 for i in range(201)]
    if side == "left": xs = xs[::1]
    else: xs = xs[::-1]
    for x in xs:
        try:
            y = f(x)
        except Exception:
            continue
        if y0 + 0.4 * (y1 - y0) * 0.1 < y < y1 * 0.85:
            return x, y
    return xs[0], f(xs[0])


def t_match_curves(r, l):
    if l == 0:
        fs_ = [(2, F(2), 0, 0), (3, F(3), 0, 0), (1, F(1, 2), 0, 0)]
    elif l == 1:
        fs_ = r.sample([(1, F(2), 0, 0), (1, F(4), 0, 0), (1, F(1, 2), 0, 0), (1, F(1, 4), 0, 0), (1, F(3), 0, 0)], 3)
    else:
        h, k = r.choice([1, 2, 3]), r.choice([1, 2, 3])
        fs_ = [(1, F(2), 0, 0), (1, F(2), 0, h), (1, F(2), k, 0)]
    if l == 0: fs_ = r.sample([(1, F(2), 0, 0), (1, F(3), 0, 0), (1, F(1, 2), 0, 0), (1, F(4), 0, 0), (1, F(1, 3), 0, 0)], 3)
    names = [fexp(a, b, c, h) for (a, b, c, h) in fs_]
    labs = ["A", "B", "C"]
    order = list(range(3)); r.shuffle(order)
    fun = [lambda x, a=a, b=b, c=c, h=h: float(a) * float(b) ** (x - h) + c for (a, b, c, h) in fs_]
    cols = [ACC, NAVY, "#475569"]
    pl = Plot(560, 290, -3, 5, -3, 9)
    pl.axes(1, 2)
    for i, idx in enumerate(order):
        pl.curve(fun[idx], -3, 5, cols[i], 4)
    for i, idx in enumerate(order):
        side = "left" if fs_[idx][1] < 1 else "right"
        x, y = find_label(fun[idx], -3, 5, -3, 9, side)
        pl.parts.append(tag(pl.X(x) + (20 if side == "left" else -20), pl.Y(y) + (-8 if side == "left" else -8) + 4 * i, ["A", "B", "C"][i], 16))
    perm = lambda p: "; ".join(f"{labs[i]}: {names[p[i]]}" for i in range(3))
    import itertools
    perms = list(itertools.permutations(range(3)))
    truth = tuple(order)
    ans = perm(truth)
    others = [perm(p) for p in perms if p != truth]
    stem = "Se grafican tres funciones exponenciales. ¿Qué expresión corresponde a cada curva (A, B y C)?"
    r.shuffle(others)
    return make(stem, pl.svg("Tres curvas exponenciales"), ans, others[:4], Q_REP, "Se comparan intersecciones con el eje Y, crecimiento o decaimiento y desplazamientos.")


# ---------------------------------------------------------------- Argumentar
def t_props(r, l):
    grow = r.random() < 0.5
    b = r.choice([F(2), F(3), F(5, 2), F(4)]) if grow else r.choice([F(1, 2), F(1, 3), F(2, 5), F(1, 4)])
    fx = f"f(x) = {bs(b)}ˣ"
    T = ["Su gráfica pasa por el punto (0, 1)", "Su dominio son todos los números reales", "Su recorrido es ]0, +∞[", "Su gráfica tiene como asíntota horizontal el eje X",
         "Es una función inyectiva", "Es " + ("creciente" if grow else "decreciente") + " en todo su dominio", "Nunca toma valores negativos"]
    Fl = ["Su gráfica corta al eje X", "Su recorrido son todos los números reales", "Es " + ("decreciente" if grow else "creciente") + " en todo su dominio", "Su gráfica pasa por el punto (1, 0)",
          "Es una función par", "Toma valores negativos para algún x", "Su gráfica es simétrica respecto del eje Y", "Su dominio es ]0, +∞["]
    if l < 2:
        good, bad = r.choice(T), r.sample(Fl, 4)
        stem = f"Sea {fx}. ¿Cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(Fl), r.sample(T, 4)
        stem = f"Sea {fx}. ¿Cuál de las siguientes afirmaciones es FALSA?"
    pl = plot(lambda x: float(b) ** x, -3, 3, -1, 9, sy=2)
    return make(stem, pl.svg("Gráfica de la función"), good, bad, Q_ARG, "Se aplican las propiedades de bˣ: dominio ℝ, recorrido ]0, +∞[, pasa por (0, 1) y su monotonía depende de b.")


def t_growth_compare(r, l):
    cfgs = {0: [(2, 2, 1), (2, 3, 1), (3, 2, 1)], 1: [(2, 2, 3), (3, 3, 1), (2, 3, 4), (3, 2, 5)], 2: [(2, 2, 10), (2, 3, 2), (3, 2, 20), (2, 4, 5), (3, 3, 8)]}
    b, n, c = r.choice(cfgs[l])
    good_x = [x for x in range(1, 13) if b ** x > c * x ** n]
    bad_x = [x for x in range(1, 13) if b ** x <= c * x ** n]
    if len(good_x) < 1 or len(bad_x) < 4: raise Reject
    gx = r.choice(good_x)
    bx = r.sample(bad_x, 4)
    ans = f"x = {gx}"
    cf = "" if c == 1 else f"{c}·"
    fig_ = plot(lambda x: float(b) ** x, 0, 8, -2, 60, extra=lambda p: p.curve(lambda x: c * x ** n, 0, 8, NAVY), sy=10)
    legend = [(ACC, f"y = {b}ˣ"), (NAVY, f"y = {cf}x{'²' if n == 2 else '³' if n == 3 else '⁴'}")]
    y = fig_.h - fig_.mb - 50
    x = fig_.w - fig_.mr - 180
    for col, t in legend:
        fig_.parts.append(f'<rect x="{x}" y="{y - 12}" width="170" height="26" rx="6" fill="#fff" stroke="{NAVY}" stroke-width="1.5"/>' + L(x + 6, y + 1, x + 36, y + 1, col, 4) + T(x + 44, y + 6, t, 15, "start"))
        y += 30
    return make(f"Se comparan f(x) = {b}ˣ (rojo) y g(x) = {cf}x{'²' if n == 2 else '³' if n == 3 else '⁴'} (azul). ¿Para cuál de los siguientes valores de x se cumple que f(x) > g(x)?", fig_.svg("Crecimiento exponencial frente a potencia"),
                ans, [f"x = {x}" for x in bx], Q_ARG, f"Se evalúa: {b}^{gx} = {b ** gx} > {c * gx ** n} = g({gx}); en los otros valores f(x) ≤ g(x).")


def t_counter_exp(r, l):
    if l == 0:
        claim = "Toda función de la forma f(x) = bˣ, con b > 0 y b ≠ 1, es creciente."
        goods = [fexp(1, b_) for b_ in (F(1, 2), F(1, 3), F(1, 4), F(2, 3), F(1, 5), F(3, 4))]
        bads = [fexp(1, b_) for b_ in (2, 3, 4, 5, 10, F(3, 2), F(5, 2))]
        head = ["f(x) = bˣ, con b > 0, b ≠ 1", "⟹ f es creciente"]
    elif l == 1:
        claim = "Si f(x) = a·bˣ + c, con a > 0 y b > 0, entonces f(x) > 0 para todo x real."
        goods = [fexp(a_, b_, c_) for a_ in (1, 2, 3) for b_ in (2, 3, F(1, 2)) for c_ in (-1, -2, -3)]
        bads = [fexp(a_, b_, c_) for a_ in (1, 2, 3) for b_ in (2, 3, F(1, 2)) for c_ in (1, 2, 3, 0)]
        head = ["a > 0, b > 0", "⟹ a·bˣ + c > 0 siempre"]
    else:
        claim = "Si f(x) = a·bˣ, con a ≠ 0 y b > 1, entonces f es creciente."
        goods = [fexp(a_, b_) for a_ in (-1, -2, -3, -5) for b_ in (2, 3, 4)]
        bads = [fexp(a_, b_) for a_ in (1, 2, 3, 5) for b_ in (2, 3, 4)]
        head = ["a ≠ 0 y b > 1", "⟹ f es creciente"]
    good = "f(x) = " + r.choice(goods)
    bad = ["f(x) = " + x for x in r.sample(sorted(set(bads)), 4)]
    return make(f"Un estudiante afirma: «{claim}» ¿Cuál de las siguientes funciones sirve como contraejemplo?", card(["Afirmación de un estudiante:"] + head + ["¿Cuál función la refuta?"], 230, 20), good, bad, Q_ARG,
                "Un contraejemplo cumple la hipótesis de la afirmación pero no su conclusión.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_eval(r, l):
    if l == 0:
        a, b, x = r.choice([1, 2, 3, 4, 5]), r.choice([F(2), F(3), F(1, 2), F(4)]), r.choice([-3, -2, -1, 2, 3, 4])
        v = a * b ** x
        fx = f"f(x) = {fexp(a, b)}"
        cands = [a * b * x, a * b ** abs(x), a * (1 / b) ** x, a + b ** x, a * x ** 1 * float(b) if False else (a * b) ** x, a * b ** (x + 1), a * b ** (x - 1)]
        stem = f"Si {fx}, ¿cuánto vale f({x})?".replace("(-", "(−")
    elif l == 1:
        a, b, x, c = r.choice([2, 3, 4, 5]), r.choice([F(2), F(3), F(1, 2), F(1, 3)]), r.choice([-2, -1, 2, 3]), r.choice([-4, -3, -1, 1, 2, 5])
        v = a * b ** x + c
        fx = f"f(x) = {fexp(a, b, c)}"
        cands = [a * b ** x - c, (a * b) ** x + c, a * b ** abs(x) + c, a * (1 / b) ** x + c, a * b * x + c, a * b ** x + c + 1, a * b ** x * c]
        stem = f"Si {fx}, ¿cuánto vale f({x})?".replace("(-", "(−")
    else:
        a, b, h, k = r.choice([1, 2, 3]), r.choice([F(2), F(3), F(1, 2)]), r.choice([1, 2, -1, -2]), r.choice([-2, -1, 1, 2])
        x = h + r.choice([-2, -1, 1, 2, 3])
        v = a * b ** (x - h) + k
        fx = f"f(x) = {fexp(a, b, k, h)}"
        cands = [a * b ** (x + h) + k, a * b ** (x - h) - k, a * b ** x + k, a * b ** (h - x) + k, a * b ** (x - h) + k + 1, a * b ** (x - h)]
        stem = f"Si {fx}, ¿cuánto vale f({x})?".replace("(-", "(−")
    ans = fs(v)
    cands = [fs(F(c).limit_denominator(10 ** 6)) for c in cands]
    return make(stem, card([fx, "Reemplaza y aplica propiedades de potencias"], 190, 20), ans, pick4(ans, cands), Q_PRO, f"Se reemplaza x y se calcula: f({x}) = {ans}.")


def t_simplify(r, l):
    b = r.choice([2, 3, 5])
    if l == 0:
        kind = r.choice(["diff", "quot", "sum"])
    else:
        kind = r.choice(["diff", "quot", "prod", "pow", "sum"])
    m = r.randint(1, 3)
    X = lambda e: f"{b}{sp(e)}"
    if kind == "diff":
        k = b ** m - 1
        expr = f"{X('x+' + str(m))} − {X('x')}"
        ans = f"{k}·{X('x')}"
        cands = [f"{b ** m}·{X('x')}", f"{X('x+' + str(m))}", f"{k + 2}·{X('x')}", f"{m}·{X('x')}", f"{b ** m + 1}·{X('x')}", f"{X('x')}"]
    elif kind == "sum":
        k = b ** m + 1
        expr = f"{X('x+' + str(m))} + {X('x')}"
        ans = f"{k}·{X('x')}"
        cands = [f"{b ** m}·{X('x')}", f"{X('x+' + str(m))}", f"{k + 1}·{X('x')}", f"{2 * b ** m}·{X('x')}", f"{m + 1}·{X('x')}", f"{b ** m - 1}·{X('x')}"]
    elif kind == "quot":
        expr = f"{X('x+' + str(m))}/{X('x')}"
        ans = str(b ** m)
        cands = [str(m), f"{X('m')}".replace("m", str(m)) if False else str(b * m), X("x+" + str(m)), str(b ** m - 1), str(b + m), f"{b}{sp('x')}"]
    elif kind == "prod":
        c = r.choice([x for x in (2, 3, 4, 5, 6, 8, 9) if x != b])
        expr = f"{b}{sp('x')}·{c}{sp('x')}"
        ans = f"{b * c}{sp('x')}"
        cands = [f"{b + c}{sp('x')}", f"{b * c}{sp('2x')}", f"{b}{sp('x')}{c}", f"{b * c}{sp('x²')}", f"{b ** 2 * c}{sp('x')}", f"{b * c}"]
    else:
        k = r.choice([2, 3])
        expr = f"({b}{sp('x')}){sp(k)}"
        ans = f"{b}{sp(str(k) + 'x')}"
        cands = [f"{b}{sp('x+' + str(k))}", f"{b * k}{sp('x')}", f"{b}{sp('x' + str(k))}", f"{b ** k}{sp('x')}" if b ** k != b else f"{b + k}{sp('x')}", f"{b}{sp(str(k) + 'x²')}"]
    cands = [c for c in cands]
    return make(f"¿Cuál expresión es equivalente a {expr}?", card([expr, "Aplica propiedades de las potencias"], 190, 22), ans, pick4(ans, cands), Q_PRO,
                "Se usan las propiedades: bᵃ⁺ᵐ = bᵃ·bᵐ, bᵃ/bᵐ = bᵃ⁻ᵐ, (bᵃ)ᵐ = bᵃᵐ y aˣ·bˣ = (ab)ˣ.")


BY_SKILL = {
    Q_RES: [t_params, t_solve_exp],
    Q_MOD: [t_model, t_table_model],
    Q_REP: [t_graph_formula, t_match_curves],
    Q_ARG: [t_props, t_growth_compare, t_counter_exp],
    Q_PRO: [t_eval, t_simplify],
}
