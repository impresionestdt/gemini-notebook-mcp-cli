"""Clase 11 · Función logarítmica: gráfica y propiedades."""
import itertools
from fractions import Fraction as F
from math import log
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, lg, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase05 import poly
from clase08 import I, fi, fu, mutants, nl_fig
from clase10 import sp, nice


def lgb(b):
    b = F(b)
    return lg(int(b)) if b.denominator == 1 else f"log_({b.numerator}/{b.denominator})"


def flog(b, h=0, k=0, a=1):
    arg = "x" if h == 0 else f"x {'−' if h > 0 else '+'} {abs(h)}"
    core = f"{lgb(b)}({arg})"
    if a == -1: core = "−" + core
    if k > 0: core += f" + {k}"
    elif k < 0: core += f" − {abs(k)}"
    return core


def logf(b, h=0, k=0, a=1):
    return lambda x: a * log(x - h) / log(float(b)) + k


def dec(x):
    return f"{x:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def plot(f, x0, x1, y0, y1, marks=(), extra=None, sx=1, sy=1, color=ACC, xs_from=None):
    pl = Plot(560, 280, x0, x1, y0, y1)
    pl.axes(sx, nice(sy))
    if extra: extra(pl)
    pl.curve(f, xs_from if xs_from is not None else x0, x1, color)
    for (x, y, lab, dx, dy) in marks:
        pl.pt(x, y, lab, dx=dx, dy=dy)
    return pl


# ---------------------------------------------------------------- Resolver
def t_params(r, l):
    if l == 0:
        b = r.choice([F(2), F(3), F(4), F(5), F(10), F(1, 2), F(1, 3)])
        y0 = r.choice([2, 3, -1, -2, 1]) if b < 1 else r.choice([1, 2, 3, -1, -2])
        x0 = b ** y0
        stem = f"La función f(x) = log_b(x) pasa por el punto ({fs(x0)}, {y0}). ¿Cuál es el valor de b?"
        ans = fs(b)
        cands = [fs(1 / b), fs(F(x0) / y0 if y0 else 1), fs(b + 1), fs(F(abs(y0))), fs(x0), fs(b * 2), fs(F(1, 2) if b != F(1, 2) else F(2))]
        f = logf(b)
        xm = float(x0) * 1.3 if x0 > 1 else 6
        pl = plot(f, 0.01, max(6, xm), -4, 4, [(float(x0), y0, f"({fs(x0)}, {y0})", 0, -28 if y0 > 0 else 28)], sx=max(1, round(max(6, xm) / 8)))
        ex = f"{y0} = log_b({fs(x0)}) implica b^({y0}) = {fs(x0)}, luego b = {ans}."
    elif l == 1:
        b, q, a = r.choice([2, 3, 4]), r.choice([1, 2, 3]), r.randint(-3, 6)
        p = b ** q - a
        if p <= -a: raise Reject
        stem = f"La función f(x) = {lg(b)}(x + a) pasa por el punto ({p}, {q}). ¿Cuál es el valor de a?"
        ans = str(a)
        cands = [b ** q + p, p - b ** q, q * b - p, b ** q, -a, a + 1, b * q + p]
        f = logf(b, -a)
        pl = plot(f, -a + 0.01 - 1 if -a < 0 else -a - 1, max(p + 4, 8), -4, 5, [(p, q, f"({p}, {q})", 0, -28)], extra=lambda p_: p_.vline(-a), sx=1, xs_from=-a + 0.02)
        ex = f"{q} = {lg(b)}({p} + a) ⟹ {p} + a = {b}^{q} = {b ** q} ⟹ a = {a}."
        cands = [str(c) for c in cands]
    else:
        b, h, k, m = r.choice([2, 3, 4]), r.randint(-3, 3), r.randint(-3, 3), r.randint(1, 3)
        x0 = h + b ** m
        v = m + k
        stem = f"Sea f(x) = {flog(b, h, k)}. ¿Cuánto vale f({x0})?"
        ans = str(v)
        cands = [b ** m + k, m * b + k, m - k, v + 1, v - 1, x0 + k, m]
        f = logf(b, h, k)
        pl = plot(f, h - 2, max(x0 + 3, h + 8), k - 4, k + 5, [(x0, v, f"({x0}, ?)", 0, -28)], extra=lambda p_: p_.vline(h), xs_from=h + 0.02, sy=2)
        ex = f"f({x0}) = {lg(b)}({x0 - h}) + {k} = {m} + {k} = {v}."
        cands = [str(c) for c in cands]
    return make(stem, pl.svg("Gráfica de la función logarítmica"), ans, pick4(ans, cands), Q_RES, ex)


def t_ineq(r, l):
    if l == 0:
        b, k = r.choice([2, 3, 4, 5, 10]), r.randint(1, 4)
        gt = r.choice([True, False])
        S = I(F(b) ** k, False, None, False) if gt else I(0, False, F(b) ** k, False)
        stem = f"Resuelve la inecuación {lg(b)}(x) {'>' if gt else '<'} {k}."
        thr, base = F(b) ** k, F(b)
    elif l == 1:
        b, k = r.choice([F(1, 2), F(1, 3), F(1, 4)]), r.randint(1, 3)
        gt = r.choice([True, False])
        thr = b ** k
        S = I(0, False, thr, False) if gt else I(thr, False, None, False)
        stem = f"Resuelve la inecuación {lgb(b)}(x) {'>' if gt else '<'} {k}."
        base = b
    else:
        b = r.choice([F(2), F(3), F(1, 2), F(1, 3)])
        k1, k2 = r.choice([(0, 2), (1, 3), (1, 2), (0, 3), (-1, 1), (-2, 0)])
        lo_, hi_ = b ** k1, b ** k2
        S = I(min(lo_, hi_), b < 1, max(lo_, hi_), b > 1) if False else (I(lo_, False, hi_, True) if b > 1 else I(hi_, True, lo_, False))
        stem = f"Resuelve la inecuación {k1} < {lgb(b)}(x) ≤ {k2}."
        base, thr = b, hi_
    ans = fi(S)
    cands = [fu(m) for m in mutants(S)]
    cands += [fi(I(None, False, S.hi, S.hc)) if S.hi is not None else fi(I(None, False, S.lo, S.lc)), fi(I(S.lo, not S.lc, S.hi, S.hc)) if S.lo is not None else "ℝ"]
    f = logf(base)
    pl = plot(f, 0.01, 9, -4, 4, extra=lambda p_: p_.hline(0), sx=1)
    return make(stem, pl.svg("Función logarítmica"), ans, pick4(ans, cands), Q_RES, "Se pasa a forma exponencial recordando x > 0 y que, si la base es menor que 1, la desigualdad cambia de sentido.")


# ---------------------------------------------------------------- Modelar
def dl(x):
    return f"{x:.2f}".replace(".", ",")


def t_doubling(r, l):
    rates = {5: 0.02, 10: 0.04, 20: 0.08, 25: 0.10, 50: 0.18, 2: 0.01}
    tgts = {2: 0.30, 3: 0.48, 4: 0.60, 5: 0.70, 10: 1.0}
    if l == 0:
        rp, tg = r.choice([10, 20, 25]), 2
    elif l == 1:
        rp, tg = r.choice([2, 5, 10, 20, 25]), r.choice([2, 3, 5, 10])
    else:
        rp, tg = r.choice(list(rates)), r.choice(list(tgts))
    lr, lt = rates[rp], tgts[tg]
    t = lt / lr
    word = {2: "se duplique", 3: "se triplique", 4: "se cuadruplique", 5: "se quintuplique", 10: "se multiplique por 10"}[tg]
    stem = (f"Un capital crece {rp}% anual (interés compuesto). Usa log {1 + rp / 100:g} = {dl(lr)} y log {tg} = {dl(lt)}: "
            f"¿aproximadamente en cuántos años {word}?").replace(".", ",")
    ans = f"{dec(t)} años"
    cands = [f"{dec(lr / lt)} años", f"{dec(lt * lr)} años", f"{dec(lt - lr)} años", f"{dec(lt / (1 + lr))} años", f"{dec(tg / rp * 100)} años", f"{dec(t * 2)} años", f"{dec(t / 2)} años"]
    fig = card([f"{1 + rp / 100:g}ᵗ = {tg}".replace(".", ","), f"t = log {tg} / log {1 + rp / 100:g}".replace(".", ",")], 200, 22)
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, f"{1 + rp/100:g}ᵗ = {tg} ⟹ t = log {tg} / log {1 + rp/100:g} = {dl(lt)}/{dl(lr)} ≈ {dec(t)}.".replace(".", ","))


def t_decibel(r, l):
    if l == 0:
        L1, L2 = sorted(r.sample(range(30, 121, 10), 2), reverse=True)
        d = (L1 - L2) // 10
        if d < 1: raise Reject
        stem = (f"El nivel sonoro en decibeles es L = 10·log(I/I₀). Una máquina produce {L1} dB y otra {L2} dB. ¿Cuántas veces mayor es la intensidad de la primera?")
        ans = f"{10 ** d:,} veces".replace(",", ".")
        cands = [f"{d:,} veces", f"{10 * d:,} veces", f"{L1 // L2:,} veces", f"{10 ** (d + 1):,} veces", f"{10 ** (d - 1) if d > 1 else 2:,} veces", f"{(L1 - L2):,} veces"]
        cands = [c.replace(",", ".") for c in cands if not c.startswith("1 veces")]
        body = R(80, 200 - L1 * 1.4, 130, L1 * 1.4, FILL) + R(340, 200 - L2 * 1.4, 130, L2 * 1.4, FILL2) + tag(145, 200 - L1 * 1.4 - 16, f"{L1} dB", 16) + tag(405, 200 - L2 * 1.4 - 16, f"{L2} dB", 16) + L(40, 200, 520, 200, INK, 3)
        fig = wrap(560, 235, body, "Dos niveles sonoros")
        ex = f"Diferencia = {L1 - L2} dB ⟹ I₁/I₂ = 10^({L1 - L2}/10) = 10^{d}."
    elif l == 1:
        d = r.choice([2, 3, 4, 5, 6, 7, 8])
        if r.random() < 0.5:
            stem = f"El nivel sonoro es L = 10·log(I/I₀) decibeles. Si la intensidad de un sonido se multiplica por {10 ** d:,}, ¿en cuántos decibeles aumenta su nivel?".replace(",", ".")
            ans = f"{10 * d} dB"
            cands = [f"{d} dB", f"{10 ** d} dB", f"{10 * d + 10} dB", f"{100 * d} dB", f"{10 * (d - 1)} dB", f"{20 * d} dB"]
            fig = card(["ΔL = 10·log(I₂/I₁)", f"I₂/I₁ = {10 ** d:,}".replace(",", "."), "ΔL = ?"], 210, 22)
            ex = f"ΔL = 10·log(10^{d}) = {10 * d} dB."
        else:
            stem = f"El nivel sonoro es L = 10·log(I/I₀) decibeles. Si el nivel de un sonido aumenta en {10 * d} dB, ¿por cuánto se multiplica su intensidad?"
            ans = f"Por {10 ** d:,}".replace(",", ".")
            cands = [f"Por {d}", f"Por {10 * d}", f"Por {10 ** (d + 1):,}".replace(",", "."), f"Por {10 ** (d - 1):,}".replace(",", "."), f"Por {d * d}", f"Por {100 * d}"]
            fig = card(["ΔL = 10·log(I₂/I₁)", f"ΔL = {10 * d} dB", "I₂/I₁ = ?"], 210, 22)
            ex = f"{10 * d} = 10·log(I₂/I₁) ⟹ I₂/I₁ = 10^{d}."
    else:
        k = r.choice([2, 4, 5, 10]); L0 = r.choice([50, 60, 65, 70, 75, 80])
        lg_ = {2: 0.30, 4: 0.60, 5: 0.70, 10: 1.0}[k]
        v = L0 + 10 * lg_
        stem = f"Una máquina produce {L0} dB. Si funcionan juntas {k} máquinas idénticas, la intensidad total se multiplica por {k}. Usando log {k} = {dec(lg_)}, ¿cuál es el nivel sonoro total?"
        ans = f"{dec(v)} dB"
        cands = [f"{dec(L0 * k)} dB", f"{dec(L0 + k)} dB", f"{dec(L0 + lg_)} dB", f"{dec(L0 + 10 * k)} dB", f"{dec(L0 + 100 * lg_)} dB", f"{dec(L0 + 20 * lg_)} dB"]
        fig = card([f"L = {L0} + 10·log {k}", f"log {k} = {dec(lg_)}", "L = ?"], 210, 22)
        ex = f"L = {L0} + 10·log {k} = {L0} + {dec(10 * lg_)} = {dec(v)} dB."
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_graph_formula(r, l):
    b = r.choice([F(2), F(3), F(4), F(1, 2), F(1, 3)])
    h = 0 if l == 0 else r.choice([x for x in range(-3, 4) if x])
    k = 0 if l < 2 else r.choice([x for x in range(-3, 4) if x])
    f = logf(b, h, k)
    p1 = (h + 1, k)
    p2 = (h + (int(b) if b > 1 else int(1 / b)), k + (1 if b > 1 else -1))
    if b < 1 and False: pass
    x1 = max(p2[0] + 3, h + 8)
    pl = plot(f, h - 2 if h < 0 else -2, x1, k - 5, k + 5, [(p1[0], p1[1], f"({p1[0]}, {p1[1]})", 0, 28), (p2[0], p2[1], f"({p2[0]}, {p2[1]})", 0, -28)], extra=lambda p_: (p_.vline(h) if h else None), xs_from=h + 0.02, sy=2)
    ans = "f(x) = " + flog(b, h, k)
    cands = ["f(x) = " + flog(1 / b, h, k), "f(x) = " + flog(b, -h, k), "f(x) = " + flog(b, h, -k), "f(x) = " + flog(b + 1 if b > 1 else b * 2 if b == F(1, 2) else F(1, 4), h, k), "f(x) = " + flog(b, h + 1, k), "f(x) = " + flog(b, h, k + 1)]
    cands = [c for c in dict.fromkeys(cands)]
    return make("La figura muestra la gráfica de una función logarítmica f (con su asíntota vertical punteada, si la hay) y dos de sus puntos. ¿Cuál es su ecuación?", pl.svg("Gráfica de una función logarítmica"), ans, pick4(ans, cands), Q_REP,
                f"Los puntos ({p1[0]}, {p1[1]}) y ({p2[0]}, {p2[1]}) dan h, k y la base: f(x) = {flog(b, h, k)}.")


def t_match_curves(r, l):
    if l == 0:
        fs_ = r.sample([(F(2), 0, 0), (F(3), 0, 0), (F(1, 2), 0, 0), (F(4), 0, 0), (F(1, 3), 0, 0)], 3)
    elif l == 1:
        fs_ = r.sample([(F(2), 0, 0), (F(2), 2, 0), (F(2), -2, 0), (F(3), 0, 0), (F(1, 2), 0, 0)], 3)
    else:
        fs_ = r.sample([(F(2), 0, 0), (F(2), 2, 0), (F(2), 0, 2), (F(2), 0, -2), (F(1, 2), 0, 0), (F(2), 3, 1)], 3)
    names = [flog(b, h, k) for (b, h, k) in fs_]
    order = list(range(3)); r.shuffle(order)
    fun = [logf(b, h, k) for (b, h, k) in fs_]
    cols = [ACC, NAVY, "#475569"]
    pl = Plot(560, 290, -3, 9, -5, 5)
    pl.axes(1, 1)
    for i, idx in enumerate(order):
        pl.curve(fun[idx], fs_[idx][1] + 0.02, 9, cols[i], 4)
    for i, idx in enumerate(order):
        b_, h_, k_ = fs_[idx]
        xl = 8.4 - 0.9 * i
        pl.parts.append(tag(pl.X(xl), pl.Y(fun[idx](xl)) + (-18 if b_ > 1 else 18), "ABC"[i], 16))
    labs = "ABC"
    perm = lambda p: "; ".join(f"{labs[i]}: {names[p[i]]}" for i in range(3))
    truth = tuple(order)
    ans = perm(truth)
    others = [perm(p) for p in itertools.permutations(range(3)) if p != truth]
    r.shuffle(others)
    return make("Se grafican tres funciones logarítmicas. ¿Qué expresión corresponde a cada curva (A, B y C)?", pl.svg("Tres curvas logarítmicas"), ans, others[:4], Q_REP,
                "Se comparan la asíntota vertical, el punto de corte con el eje X y si la curva crece o decrece.")


# ---------------------------------------------------------------- Argumentar
def t_props(r, l):
    grow = r.random() < 0.6
    b = r.choice([F(2), F(3), F(5), F(10)]) if grow else r.choice([F(1, 2), F(1, 3), F(1, 5)])
    T = ["Su gráfica pasa por el punto (1, 0)", "Su dominio es ]0, +∞[", "Su recorrido son todos los números reales", "Su gráfica tiene como asíntota vertical el eje Y",
         "Es una función inyectiva", "Es " + ("creciente" if grow else "decreciente") + " en todo su dominio", f"Su gráfica pasa por el punto ({fs(b)}, 1)"]
    Fl = ["Su gráfica pasa por el punto (0, 1)", "Su dominio son todos los números reales", "Su recorrido es ]0, +∞[", "Su gráfica tiene como asíntota horizontal el eje X",
          "Es " + ("decreciente" if grow else "creciente") + " en todo su dominio", "Es una función par", "Su gráfica corta al eje Y", f"Su gráfica pasa por el punto (1, {fs(b)})"]
    fx = f"f(x) = {lgb(b)}(x)"
    if l < 2:
        good, bad = r.choice(T), r.sample(Fl, 4)
        stem = f"Sea {fx}. ¿Cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(Fl), r.sample(T, 4)
        stem = f"Sea {fx}. ¿Cuál de las siguientes afirmaciones es FALSA?"
    pl = plot(logf(b), 0.01, 8, -4, 4, sx=1)
    return make(stem, pl.svg("Gráfica de la función logarítmica"), good, bad, Q_ARG, "Propiedades de log_b(x): dominio ]0, +∞[, recorrido ℝ, pasa por (1, 0) y (b, 1), asíntota x = 0.")


def t_domain(r, l):
    b = r.choice([2, 3, 5, 10])
    if l == 0:
        kind = r.choice(["a", "b", "c"])
        c = r.randint(-8, 8)
        if kind == "a":
            expr, S = f"x {'−' if c > 0 else '+'} {abs(c)}", I(c, False, None, False)
        elif kind == "b":
            expr, S = f"{c} − x" if c else "−x", I(None, False, c, False)
        else:
            a_ = r.choice([2, 3, 4, 5])
            expr, S = f"{a_}x {'−' if c > 0 else '+'} {abs(c) * a_}", I(c, False, None, False)
        if c == 0 and kind == "a": expr = "x"
        ans = fi(S)
        cands = [fu(m) for m in mutants(S)]
    elif l == 1:
        a, c = sorted(r.sample(range(-6, 7), 2))
        neg = r.random() < 0.5
        expr = f"(x {'−' if a > 0 else '+'} {abs(a)})/(x {'−' if c > 0 else '+'} {abs(c)})".replace("(x + 0)", "x").replace("(x − 0)", "x")
        S = [I(None, False, a, False), I(c, False, None, False)]
        ans = fu(S)
        cands = [fi(I(a, False, c, False)), fu([I(None, False, a, True), I(c, False, None, False)]), fi(I(None, False, a, False)), fi(I(c, False, None, False)), fu([I(None, False, -c, False), I(-a, False, None, False)]), "ℝ"]
    else:
        r1, r2 = sorted(r.sample(range(-5, 6), 2))
        a = r.choice([1, -1])
        bb, cc = -a * (r1 + r2), a * r1 * r2
        expr = poly(a, bb, cc)
        if a == 1:
            S = [I(None, False, r1, False), I(r2, False, None, False)]
            ans = fu(S)
            cands = [fi(I(r1, False, r2, False)), fu([I(None, False, r1, True), I(r2, True, None, False)]), fi(I(None, False, r1, False)), fi(I(r2, False, None, False)), fu([I(None, False, -r2, False), I(-r1, False, None, False)])]
        else:
            S = I(r1, False, r2, False)
            ans = fi(S)
            cands = [fu([I(None, False, r1, False), I(r2, False, None, False)]), fi(I(r1, True, r2, True)), fi(I(None, False, r2, False)), fi(I(r1, False, None, False)), fi(I(-r2, False, -r1, False))]
    stem = f"¿Cuál es el dominio de la función f(x) = {lg(b)}({expr})?"
    fig = card([f"f(x) = {lg(b)}({expr})", "Se necesita que el argumento sea positivo"], 190, 21)
    return make(stem, fig, ans, pick4(ans, cands), Q_ARG, f"Se resuelve ({expr}) > 0: {ans}.")


def t_counter(r, l):
    if l == 0:
        claim = "Para todo x real distinto de 0, log_b(x²) = 2·log_b(x)."
        b = r.choice([2, 3, 5, 10])
        goods = [f"x = {v}" for v in (-1, -2, -3, -4, -5, -10, -8)]
        bads = [f"x = {v}" for v in (1, 2, 3, 4, 5, 8, 10, 16, 9)]
        head = ["x ≠ 0 ⟹ log(x²) = 2·log(x)", "¿Con qué valor de x se refuta?"]
        stem = f"Una estudiante afirma: «{claim}» (con b > 1). ¿Con cuál de los siguientes valores de x la igualdad NO se cumple?".replace("(con b > 1)", f"(con b = {b})")
    elif l == 1:
        b = r.choice([2, 3, 5, 10])
        claim = f"Si f(x) = {lg(b)}(x), entonces f(x) > 0 para todo x en su dominio."
        goods = [f"x = {v}" for v in ("1/2", "1/3", "1/4", "1", "1/5", "1/10", "1/8")]
        bads = [f"x = {v}" for v in (b, b * b, b ** 3, 2 * b, 3 * b, b + 1, 5 * b)]
        head = [f"f(x) = {lg(b)}(x)", "⟹ f(x) > 0 siempre", "¿Con qué valor de x se refuta?"]
        stem = f"Un estudiante afirma: «{claim}» ¿Con cuál de los siguientes valores de x se refuta?"
    else:
        claim = "Toda función de la forma f(x) = log_b(x), con b > 0 y b ≠ 1, es creciente."
        goods = [f"f(x) = {lgb(F(1, k))}(x)" for k in (2, 3, 4, 5)] + [f"f(x) = {lgb(F(2, 3))}(x)", f"f(x) = {lgb(F(1, 10))}(x)"]
        bads = [f"f(x) = {lg(k)}(x)" for k in (2, 3, 4, 5, 10, 7)]
        head = ["f(x) = log_b(x), b > 0, b ≠ 1", "⟹ f es creciente", "¿Cuál función la refuta?"]
        stem = f"Una estudiante afirma: «{claim}» ¿Cuál de las siguientes funciones sirve como contraejemplo?"
    good = r.choice(goods)
    bad = r.sample(bads, 4)
    if good in bad: raise Reject
    return make(stem, card(["Afirmación de un estudiante:"] + head, 220, 20), good, bad, Q_ARG, "Un contraejemplo cumple la hipótesis pero no la conclusión de la afirmación.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_eval(r, l):
    if l == 0:
        b, m = r.choice([2, 3, 4, 5, 10]), r.randint(-2, 4)
        x0 = F(b) ** m
        stem = f"Sea f(x) = {lg(b)}(x). ¿Cuánto vale f({fs(x0)})?"
        v = m
        cands = [b * m, F(x0) / b if b else 1, m + 1, -m, x0, m - 1, b ** m if m > 0 else b + m]
        fx = f"f(x) = {lg(b)}(x)"
    elif l == 1:
        b, h, m = r.choice([2, 3, 5]), r.randint(-4, 5), r.randint(0, 3)
        k = r.randint(-3, 4)
        x0 = h + b ** m
        stem = f"Sea f(x) = {flog(b, h, k)}. ¿Cuánto vale f({x0})?"
        v = m + k
        cands = [b ** m + k, m * b + k, m - k, v + 1, v - 1, x0 + k, m]
        fx = f"f(x) = {flog(b, h, k)}"
    else:
        b, m = r.choice([F(1, 2), F(1, 3), F(1, 4)]), r.randint(1, 3)
        h, k = r.randint(-3, 3), r.randint(-3, 3)
        x0 = h + b ** m
        stem = f"Sea f(x) = {flog(b, h, k)}. ¿Cuánto vale f({fs(x0)})?"
        v = -m + k
        cands = [m + k, b ** m + k, -m - k, v + 1, m * b + k, k]
        fx = f"f(x) = {flog(b, h, k)}"
    ans = fs(v)
    return make(stem, card([fx, "Escribe el argumento como potencia de la base"], 190, 20), ans, pick4(ans, [fs(F(c).limit_denominator(10 ** 6)) for c in cands]), Q_PRO,
                f"El argumento es una potencia de la base: se aplica {lg(2)}(bⁿ) = n y se suma el desplazamiento vertical.")


def t_inverse(r, l):
    b = r.choice([2, 3, 4, 5, 10])
    if l == 0:
        fx = f"f(x) = {lg(b)}(x)"
        ans = f"f⁻¹(x) = {b}ˣ"
        cands = [f"f⁻¹(x) = {b}·x", f"f⁻¹(x) = x{sp(str(b))}".replace("ˣ", "x") if False else f"f⁻¹(x) = x^{b}", f"f⁻¹(x) = (1/{b})ˣ", f"f⁻¹(x) = {b}⁻ˣ", f"f⁻¹(x) = {lg(b)}(x)", f"f⁻¹(x) = x/{b}"]
    elif l == 1:
        k = r.choice([x for x in range(-4, 5) if x])
        fx = f"f(x) = {flog(b, 0, k)}"
        ex_ = f"x{'−' if k > 0 else '+'}{abs(k)}"
        ans = f"f⁻¹(x) = {b}{sp(ex_)}"
        cands = [f"f⁻¹(x) = {b}{sp('x' + ('+' if k > 0 else '−') + str(abs(k)))}", f"f⁻¹(x) = {b}ˣ {'+' if k > 0 else '−'} {abs(k)}", f"f⁻¹(x) = {b}ˣ {'−' if k > 0 else '+'} {abs(k)}", f"f⁻¹(x) = {b}·(x {'−' if k > 0 else '+'} {abs(k)})", f"f⁻¹(x) = {b}ˣ"]
    else:
        h, k = r.choice([x for x in range(-4, 5) if x]), r.choice([x for x in range(-4, 5) if x])
        fx = f"f(x) = {flog(b, h, k)}"
        ex_ = f"x{'−' if k > 0 else '+'}{abs(k)}"
        ans = f"f⁻¹(x) = {b}{sp(ex_)} {'+' if h > 0 else '−'} {abs(h)}"
        cands = [f"f⁻¹(x) = {b}{sp(ex_)} {'−' if h > 0 else '+'} {abs(h)}", f"f⁻¹(x) = {b}{sp('x' + ('+' if k > 0 else '−') + str(abs(k)))} {'+' if h > 0 else '−'} {abs(h)}", f"f⁻¹(x) = {b}{sp('x')} {'+' if h > 0 else '−'} {abs(h)}", f"f⁻¹(x) = {b}{sp('x' + ('−' if k > 0 else '+') + str(abs(h)))} {'+' if k > 0 else '−'} {abs(k)}", f"f⁻¹(x) = {b}{sp(ex_)}"]
    return make(f"¿Cuál es la función inversa de {fx}?", card([fx, "y = f(x) ⟹ se despeja x y se intercambian x e y"], 190, 20), ans, pick4(ans, cands), Q_PRO,
                "Se pasa a forma exponencial, se despeja x y se intercambian las variables.")


BY_SKILL = {
    Q_RES: [t_params, t_ineq],
    Q_MOD: [t_doubling, t_decibel],
    Q_REP: [t_graph_formula, t_match_curves],
    Q_ARG: [t_props, t_domain, t_counter],
    Q_PRO: [t_eval, t_inverse],
}
