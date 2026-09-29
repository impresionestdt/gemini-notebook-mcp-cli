"""Clase 8 · Sistemas de inecuaciones lineales: intersección de conjuntos solución e intervalos."""
from fractions import Fraction as F
from math import floor, ceil
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO


# ---------------------------------------------------------------- intervalos
class I:
    def __init__(s, lo, lc, hi, hc):
        s.lo = None if lo is None else F(lo)
        s.hi = None if hi is None else F(hi)
        s.lc, s.hc = lc, hc


def empty(a):
    if a.lo is None or a.hi is None: return False
    return a.lo > a.hi or (a.lo == a.hi and not (a.lc and a.hc))


def inter(a, b):
    if a is None or b is None: return None
    if a.lo is None: lo, lc = b.lo, b.lc
    elif b.lo is None: lo, lc = a.lo, a.lc
    elif a.lo > b.lo: lo, lc = a.lo, a.lc
    elif b.lo > a.lo: lo, lc = b.lo, b.lc
    else: lo, lc = a.lo, a.lc and b.lc
    if a.hi is None: hi, hc = b.hi, b.hc
    elif b.hi is None: hi, hc = a.hi, a.hc
    elif a.hi < b.hi: hi, hc = a.hi, a.hc
    elif b.hi < a.hi: hi, hc = b.hi, b.hc
    else: hi, hc = a.hi, a.hc and b.hc
    res = I(lo, lc, hi, hc)
    return None if empty(res) else res


def union(a, b):
    xs = sorted([a, b], key=lambda i: (i.lo is not None, i.lo if i.lo is not None else 0))
    p, q = xs
    touch = p.hi is None or q.lo is None or p.hi > q.lo or (p.hi == q.lo and (p.hc or q.lc))
    if not touch: return [p, q]
    lo, lc = p.lo, p.lc
    if p.lo is not None and q.lo is not None and q.lo == p.lo: lc = p.lc or q.lc
    if p.hi is None or q.hi is None: hi, hc = None, False
    elif p.hi > q.hi: hi, hc = p.hi, p.hc
    elif q.hi > p.hi: hi, hc = q.hi, q.hc
    else: hi, hc = p.hi, p.hc or q.hc
    if p.lo is None or q.lo is None: lo, lc = None, False
    return [I(lo, lc, hi, hc)]


def fi(a):
    if a is None: return "∅"
    if a.lo is not None and a.hi is not None and a.lo == a.hi: return "{" + fs(a.lo) + "}"
    l = "]−∞" if a.lo is None else ("[" if a.lc else "]") + fs(a.lo)
    h = "+∞[" if a.hi is None else fs(a.hi) + ("]" if a.hc else "[")
    return l + ", " + h


def fu(x):
    if x is None or isinstance(x, I): return fi(x)
    return " ∪ ".join(fi(i) for i in x)


def contains(a, v):
    if a is None: return False
    if a.lo is not None and (v < a.lo or (v == a.lo and not a.lc)): return False
    if a.hi is not None and (v > a.hi or (v == a.hi and not a.hc)): return False
    return True


def solve_lin(a, b, op, c):
    """a·x + b (op) c  →  intervalo."""
    r = F(c - b, a) if not isinstance(c, F) else (c - b) / a
    r = F(r)
    if a < 0: op = {"<": ">", "≤": "≥", ">": "<", "≥": "≤"}[op]
    return {"<": I(None, False, r, False), "≤": I(None, False, r, True), ">": I(r, False, None, False), "≥": I(r, True, None, False)}[op]


def lx(a, b, var="x"):
    s = ("" if a == 1 else "−" if a == -1 else str(a)) + var
    if b > 0: s += f" + {b}"
    elif b < 0: s += f" − {abs(b)}"
    return s.replace("-", "−")


def mutants(a):
    out = []
    if a is None: return out
    if a.lo is not None: out.append(I(a.lo, not a.lc, a.hi, a.hc))
    if a.hi is not None: out.append(I(a.lo, a.lc, a.hi, not a.hc))
    out.append(I(None if a.hi is None else -a.hi, a.hc, None if a.lo is None else -a.lo, a.lc))
    if a.lo is None or a.hi is None:
        out.append(I(a.hi, a.hc, None, False) if a.lo is None else I(None, False, a.lo, a.lc))
    else:
        out.append([I(None, False, a.lo, not a.lc), I(a.hi, not a.hc, None, False)])
    for d in (1, -1):
        out.append(I(None if a.lo is None else a.lo + d, a.lc, None if a.hi is None else a.hi + d, a.hc))
    return out


# ---------------------------------------------------------------- figuras
def nrow(y, ivs, lo, hi, label=None):
    x0, x1 = 55, 525
    sc = (x1 - x0) / (hi - lo)
    X = lambda v: x0 + (float(v) - lo) * sc
    body = L(x0 - 20, y, x1 + 20, y, INK, 3)
    step = 1 if hi - lo <= 14 else 2
    for t in range(int(lo), int(hi) + 1):
        body += L(X(t), y - 6, X(t), y + 6, INK, 2)
        if (t - int(lo)) % step == 0:
            body += T(X(t), y + 26, fs(t), 14)
    for iv in ivs:
        if iv is None: continue
        a = x0 - 20 if iv.lo is None else X(iv.lo)
        b = x1 + 20 if iv.hi is None else X(iv.hi)
        body += L(a, y, b, y, ACC, 8)
        if iv.lo is None: body += P([(x0 - 22, y), (x0 - 10, y - 9), (x0 - 10, y + 9)], ACC, ACC, 1)
        if iv.hi is None: body += P([(x1 + 22, y), (x1 + 10, y - 9), (x1 + 10, y + 9)], ACC, ACC, 1)
        for v, cl in ((iv.lo, iv.lc), (iv.hi, iv.hc)):
            if v is not None:
                body += C(X(v), y, 9, ACC if cl else WHITE, ACC if not cl else INK, 4 if not cl else 2)
    if label:
        w = len(label) * 15 * 0.62 + 16
        body += tag(8 + w / 2, y - 30, label, 15)
    return body


def nl_fig(rows, lo, hi):
    h = 40 + 85 * len(rows)
    body = "".join(nrow(75 + 85 * i, ivs, lo, hi, lab) for i, (lab, ivs) in enumerate(rows))
    return wrap(560, h, body, "Rectas numéricas con conjuntos solución")


def view(*sets):
    vals = [v for s_ in sets if s_ is not None for v in (s_.lo, s_.hi) if v is not None]
    if not vals: return -5, 5
    lo, hi = floor(min(vals)) - 2, ceil(max(vals)) + 2
    return lo, max(hi, lo + 6)


# ---------------------------------------------------------------- Resolver
def rand_ineq(r, l, sol=None):
    op = r.choice(["<", "≤", ">", "≥"])
    a = r.choice([1, 2, 3, 4, 5]) if l == 0 else r.choice([-1, -2, -3, -4, -5, 2, 3])
    if l >= 1 and r.random() < 0.7: a = -abs(a)
    b = r.randint(-9, 9)
    rt = r.randint(-8, 8)
    c = a * rt + b
    return a, b, op, c, solve_lin(a, b, op, c)


def t_solve1(r, l):
    if l < 2:
        a, b, op, c, S = rand_ineq(r, l)
        stem = f"Resuelve la inecuación {lx(a, b)} {op} {c}.".replace("-", "−")
        eq = f"{lx(a, b)} {op} {c}".replace("-", "−")
    else:
        a, d = r.choice([(2, 5), (1, 4), (3, 6), (-2, 1), (4, 7), (-3, 2), (5, 2)])
        b, e = r.randint(-8, 8), r.randint(-8, 8)
        op = r.choice(["<", "≤", ">", "≥"])
        S = solve_lin(a - d, 0, op, e - b)
        stem = f"Resuelve la inecuación {lx(a, b)} {op} {lx(d, e)}.".replace("-", "−")
        eq = f"{lx(a, b)} {op} {lx(d, e)}".replace("-", "−")
    ans = fi(S)
    cands = [fu(m) for m in mutants(S)]
    lo, hi = view(S)
    fig = wrap(560, 190, nrow(80, [], lo, hi) + tag(280, 30, eq, 20), "Recta numérica y la inecuación")
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, f"Al despejar (y cambiar el sentido si se divide por un número negativo) se obtiene x ∈ {ans}.")


def rand_side(r, l):
    op = r.choice(["<", "≤", ">", "≥"])
    a = r.choice([1, 2, 3]) if l == 0 else r.choice([-3, -2, -1, 1, 2, 3, 4])
    b, rt = r.randint(-6, 6), r.randint(-6, 6)
    return a, b, op, a * rt + b


def t_system(r, l):
    for _ in range(50):
        p1, p2 = rand_side(r, l), rand_side(r, l)
        S1, S2 = solve_lin(*p1), solve_lin(*p2)
        S = inter(S1, S2)
        if l < 2 and S is None: continue
        if l >= 2 and S is None and r.random() < 0.7: continue
        break
    else:
        raise Reject
    e1, e2 = f"{lx(p1[0], p1[1])} {p1[2]} {p1[3]}".replace("-", "−"), f"{lx(p2[0], p2[1])} {p2[2]} {p2[3]}".replace("-", "−")
    ans = fi(S)
    un = union(S1, S2)
    cands = [fu(un), fi(S1), fi(S2)] + [fu(m) for m in (mutants(S) if S else mutants(S1))]
    if S is None: cands += [fu(un)]
    lo, hi = view(S1, S2)
    rows = [("A", [S1]), ("B", [S2])] if l == 0 else None
    if rows:
        fig = nl_fig(rows, lo, hi)
    else:
        fig = card(["Sistema de inecuaciones:", e1, e2, "¿Conjunto solución común?"], 230, 21)
    return make(f"¿Cuál es el conjunto solución del sistema {{ {e1} ; {e2} }}?", fig, ans, pick4(ans, cands), Q_RES,
                f"Se resuelve cada inecuación (A: {fi(S1)}, B: {fi(S2)}) y se intersectan: {ans}.")


# ---------------------------------------------------------------- Modelar
def t_budget(r, l):
    p = r.choice([1000, 1500, 2000, 2500, 3000, 4000, 5000])
    q = r.randint(1, 6)
    f = p * q
    h1, h2 = sorted(r.sample(range(1, 16), 2))
    if h2 - h1 < 2: raise Reject
    if l == 0:
        B1, B2, cl = f + p * h1, f + p * h2, True
        S = I(h1, True, h2, True)
    elif l == 1:
        B1, B2, cl = f + p * h1, f + p * h2, False
        S = I(h1, False, h2, False)
    else:
        sl1, sl2 = r.choice([0, 300, 500, 700]), r.choice([0, 200, 400, 900])
        B1, B2, cl = f + p * h1 + sl1, f + p * h2 + sl2, True
        S = I(F(B1 - f, p), True, F(B2 - f, p), True)
    words = "ambos incluidos" if cl else "sin incluir los extremos"
    if l < 2:
        stem = f"Un taller cobra ${f:,} fijos más ${p:,} por hora de trabajo. Se dispone de un presupuesto total entre ${B1:,} y ${B2:,} ({words}). ¿Cuántas horas h se pueden contratar?".replace(",", ".")
        ans = fmt_h(S)
        cands = [fmt_h(I(h1 + q, S.lc, h2 + q, S.hc)), fmt_h(I(h1 - q, S.lc, h2 - q, S.hc)), fmt_h(I(h1, not S.lc, h2, not S.hc)), fmt_h(I(h1, S.lc, h2 + 1, S.hc)), fmt_h(I(h1 - 1, S.lc, h2, S.hc)), fmt_h(I(h1 + 1, S.lc, h2 - 1, S.hc))]
    else:
        stem = f"Un taller cobra ${f:,} fijos más ${p:,} por hora de trabajo. Se dispone de entre ${B1:,} y ${B2:,} (ambos incluidos). ¿Cuántas horas enteras se pueden contratar?".replace(",", ".")
        cnt = sum(1 for h in range(0, 40) if contains(S, F(h)))
        ans = f"{cnt} horas distintas"
        cands = [f"{cnt + 1} horas distintas", f"{max(1, cnt - 1)} horas distintas", f"{cnt + 2} horas distintas", f"{max(1, cnt - 2)} horas distintas", f"{h2 - h1} horas distintas", f"{h2 - h1 + 1} horas distintas"]
    H = h2 + 3
    ymax = (f + p * H) / 1000
    pl = Plot(560, 280, 0, H, 0, ymax)
    pl.axes(max(1, H // 8), max(1, round(ymax / 6)))
    pl.parts.append(R(pl.X(0), pl.Y(B2 / 1000), pl.X(H) - pl.X(0), pl.Y(B1 / 1000) - pl.Y(B2 / 1000), FILL2, "none", 0))
    pl.curve(lambda x: (f + p * x) / 1000, 0, H)
    pl.parts.append(tag(pl.X(H * 0.72), pl.Y(B2 / 1000) - 24, "zona del presupuesto", 15) + T(pl.X(H) - 6, pl.Y(0) - 8, "horas", 13, "end") + T(pl.ml + 6, pl.mt + 10, "costo (miles de $)", 13, "start"))
    return make(stem, pl.svg("Costo según las horas contratadas"), ans, pick4(ans, cands), Q_MOD, f"{B1:,} ≤ {f:,} + {p:,}h ≤ {B2:,} ⟹ {ans}.".replace(",", "."))


def fmt_h(S):
    lo = fs(S.lo); hi = fs(S.hi)
    return f"{lo} {'≤' if S.lc else '<'} h {'≤' if S.hc else '<'} {hi}"


def tri_fig(a, b, c):
    body = P([(70, 190), (470, 190), (330, 40)], FILL) + tag(270, 220, a, 17) + tag(175, 105, b, 17) + tag(430, 105, c, 17)
    return wrap(560, 245, body, "Triángulo con lados dados")


def t_triangle(r, l):
    if l == 0:
        a, b = sorted(r.sample(range(2, 15), 2))
        if b - a < 2: raise Reject
        S = I(b - a, False, a + b, False)
        stem = f"Los lados de un triángulo miden {a} cm, {b} cm y x cm. ¿Qué valores puede tomar x?"
        fig = tri_fig(f"{a} cm", f"{b} cm", "x cm")
        cands = [fu(I(b - a, True, a + b, True)), fu(I(0, False, a + b, False)), fu(I(a, False, b, False)), fu(I(b - a, False, None, False)), fu(I(None, False, a + b, False)), fu(I(a + b, False, None, False))]
    elif l == 1:
        m = r.choice([2, 3, 4]); c = r.choice([6, 8, 9, 10, 12, 15, 18, 20, 24])
        S = I(F(c, 1 + m), False, F(c, m - 1), False)
        stem = f"Los lados de un triángulo miden x, {m}x y {c} cm. ¿Qué valores puede tomar x?"
        fig = tri_fig(f"{c} cm", "x", f"{m}x")
        cands = [fu(I(F(c, 1 + m), True, F(c, m - 1), True)), fu(I(F(c, m - 1), False, F(c, m + 1), False)), fu(I(0, False, F(c, m - 1), False)), fu(I(F(c, 1 + m), False, None, False)), fu(I(F(c, m), False, F(c, m - 1), False)), fu(I(F(c, m + 1), False, F(c, m), False))]
    else:
        m = r.choice([2, 3]); c = r.choice([6, 8, 9, 10, 12, 15, 18, 20, 24]); Pm = r.choice([30, 36, 40, 45, 50, 60])
        lo_, hi_ = F(c, 1 + m), F(c, m - 1)
        hi2 = F(Pm - c, 1 + m)
        S = inter(I(lo_, False, hi_, False), I(None, False, hi2, False))
        if S is None or not (hi2 < hi_ and hi2 > lo_): raise Reject
        stem = f"Los lados de un triángulo miden x, {m}x y {c} cm, y su perímetro es menor que {Pm} cm. ¿Qué valores puede tomar x?"
        fig = tri_fig(f"{c} cm", "x", f"{m}x")
        cands = [fu(I(lo_, False, hi_, False)), fu(I(lo_, False, hi2, True)), fu(I(0, False, hi2, False)), fu(I(hi2, False, hi_, False)), fu(I(lo_, False, None, False)), fu(I(None, False, hi2, False))]
    ans = fu(S)
    return make(stem, fig, ans, pick4(ans, cands), Q_MOD, "Se aplica la desigualdad triangular (cada lado menor que la suma de los otros dos) y se intersectan las condiciones.")


# ---------------------------------------------------------------- Representar
def rand_iv(r, l):
    a, b = sorted(r.sample(range(-7, 8), 2))
    if b - a < 2: raise Reject
    if l == 0:
        v = r.choice([a, b])
        cl = r.choice([True, False])
        return r.choice([I(None, False, v, cl), I(v, cl, None, False)])
    return I(a, r.choice([True, False]), b, r.choice([True, False]))


def t_read(r, l):
    if l < 2:
        S = rand_iv(r, l)
        lo, hi = view(S)
        fig = nl_fig([("Conjunto solución", [S])], lo, hi)
        ans = fi(S)
        cands = [fu(m) for m in mutants(S)]
        stem = "¿Qué conjunto está representado en la recta numérica? (círculo lleno: extremo incluido; círculo vacío: extremo excluido)"
    else:
        A, B = rand_iv(r, 1), rand_iv(r, 1)
        oper = r.choice(["∩", "∪"])
        lo, hi = view(A, B)
        fig = nl_fig([("A", [A]), ("B", [B])], lo, hi)
        if oper == "∩":
            R_ = inter(A, B); ans = fi(R_)
            cands = [fu(union(A, B)), fi(A), fi(B)] + [fu(m) for m in (mutants(R_) if R_ else mutants(A))]
        else:
            R_ = union(A, B); ans = fu(R_)
            cands = [fi(inter(A, B)), fi(A), fi(B)] + [fu(m) for m in mutants(A)]
        stem = f"Se representan los conjuntos A y B en las rectas numéricas. ¿Cuál es A {oper} B?"
    return make(stem, fig, ans, pick4(ans, cands), Q_REP, "Se lee cada extremo y si está incluido (círculo lleno) o excluido (círculo vacío).")


def t_count_int(r, l):
    a = F(r.randint(-9, 4)) + (F(r.choice([0, 1, 2, 3, 4]), 5) if l >= 1 else 0)
    b = a + r.randint(2, 9) + (F(r.choice([0, 1, 2, 3]), 4) if l >= 1 else 0)
    S = I(a, r.choice([True, False]), b, r.choice([True, False]))
    if l == 2 and r.random() < 0.5:
        S2 = I(b + 1, r.choice([True, False]), b + 1 + r.randint(2, 4), r.choice([True, False]))
    else:
        S2 = None
    cnt = sum(1 for v in range(-30, 40) if contains(S, F(v)) or contains(S2, F(v)))
    if cnt == 0: raise Reject
    lo, hi = view(S, S2)
    fig = nl_fig([("Conjunto solución", [S] + ([S2] if S2 else []))], lo, hi)
    ans = str(cnt)
    cands = [str(cnt + 1), str(max(0, cnt - 1)), str(cnt + 2), str(max(0, cnt - 2)), str(cnt + 3)]
    return make("En la recta numérica se representa un conjunto solución. ¿Cuántos números enteros pertenecen a él?", fig, ans, pick4(ans, cands), Q_REP,
                "Se cuentan los enteros dentro del intervalo, respetando los extremos incluidos o excluidos.")


# ---------------------------------------------------------------- Argumentar
NATURE = ["El sistema no tiene solución", "El sistema tiene exactamente una solución", "El conjunto solución es un intervalo acotado", "El conjunto solución es un intervalo no acotado", "Todo número real es solución del sistema"]


def nature_of(S, U):
    if U == "R": return 4
    if S is None: return 0
    if S.lo is not None and S.hi is not None:
        return 1 if S.lo == S.hi else 2
    return 3


def t_nature(r, l):
    for _ in range(80):
        a, b = r.randint(-6, 6), r.randint(-6, 6)
        op1, op2 = r.choice(["<", "≤", ">", "≥"]), r.choice(["<", "≤", ">", "≥"])
        A, B = solve_lin(1, 0, op1, a), solve_lin(1, 0, op2, b)
        conj = r.random() < (1 if l < 2 else 0.6)
        if conj:
            S = inter(A, B); k = nature_of(S, None)
        else:
            u = union(A, B)
            k = 4 if (len(u) == 1 and u[0].lo is None and u[0].hi is None) else 3 if len(u) == 1 else None
            if k is None: continue
        if l == 0 and k == 1: continue
        want = r.randint(0, 4) if False else None
        break
    else:
        raise Reject
    e1, e2 = f"x {op1} {a}".replace("-", "−"), f"x {op2} {b}".replace("-", "−")
    rows = [("A: " + e1, [A]), ("B: " + e2, [B])]
    lo, hi = view(A, B)
    conn = "y" if conj else "o"
    fig = nl_fig(rows, lo, hi)
    return make(f"Se consideran las condiciones A: {e1} {conn} B: {e2}. ¿Qué se puede afirmar del conjunto solución?", fig, NATURE[k], [x for i, x in enumerate(NATURE) if i != k], Q_ARG,
                f"{'Intersección' if conj else 'Unión'} de A y B: " + (fi(S) if conj else fu(u)) + ".")


TRUE_I = ["Si a < b y c < 0, entonces a·c > b·c", "Si a < b, entonces a + c < b + c para todo c", "Si 0 < a < b, entonces 1/a > 1/b", "Si a < b, entonces −a > −b", "Si a < b y b < c, entonces a < c"]
FALSE_I = ["Si a < b, entonces a² < b² para todos a, b", "Si a < b, entonces a·c < b·c para todo c", "Si a < b, entonces 1/a > 1/b para todos a, b no nulos", "Si a < b y c < d, entonces a − c < b − d",
           "Si a < b, entonces |a| < |b|", "Si a·c < b·c, entonces a < b", "Si a < b y c < d, entonces a·c < b·d para todos los reales"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_I), r.sample(FALSE_I, 4)
        stem = "¿Cuál de las siguientes afirmaciones sobre desigualdades entre números reales es verdadera?"
    else:
        good, bad = r.choice(FALSE_I), r.sample(TRUE_I, 4)
        stem = "¿Cuál de las siguientes afirmaciones sobre desigualdades entre números reales es FALSA?"
    a, b = sorted(r.sample(range(-6, 7), 2))
    fig = nl_fig([("a < b", [])], -8, 8)
    sh = 16 if b - a <= 2 else 0
    fig = fig.replace("</svg>", C(55 + (a + 8) * 470 / 16, 75, 9, ACC) + tag(55 + (a + 8) * 470 / 16 - sh, 45, "a", 16) + C(55 + (b + 8) * 470 / 16, 75, 9, ACC) + tag(55 + (b + 8) * 470 / 16 + sh, 45, "b", 16) + "</svg>")
    return make(stem, fig, good, bad, Q_ARG, "Se prueba cada afirmación con casos: al multiplicar o elevar al cuadrado el orden puede cambiar.")


ERR = ["No invirtió el sentido de la desigualdad al dividir por un número negativo", "Cambió mal el signo de un término al pasarlo al otro lado",
       "Consideró cerrado un extremo que debía ser abierto", "Calculó la unión en vez de la intersección de las soluciones", "Cometió un error de cálculo al dividir por el coeficiente"]


def t_error(r, l):
    kind = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 4])
    if kind == 0:
        a, rt = r.randint(2, 6), r.randint(-6, 6)
        c = -a * rt
        op = r.choice(["<", ">"])
        wrong = {"<": "<", ">": ">"}[op]
        lines = [f"−{a}x {op} {c}", f"x {wrong} {rt}"]
        rows = ["Resolución de un estudiante:", *lines]
    elif kind == 1:
        a, b = r.randint(2, 9), r.randint(1, 9)
        op = r.choice(["<", ">", "≤", "≥"])
        c = r.randint(-9, 9)
        lines = [f"x + {b} {op} {c}", f"x {op} {c + b}"]
        rows = ["Resolución de un estudiante:", *lines]
    elif kind == 2:
        a = r.randint(-5, 2); b = a + r.randint(3, 8)
        lines = [f"x > {a}  y  x < {b}", f"Solución: [{a}, {b}]".replace("[", "]", 1)[:0] + f"Solución: ]{a}, {b}]"]
        rows = ["Resolución de un estudiante:", *lines]
    elif kind == 3:
        a = r.randint(-4, 2); b = a + r.randint(3, 8)
        lines = [f"x > {a}  y  x < {b}", "Solución: ]−∞, +∞["]
        rows = ["Resolución de un estudiante:", *lines]
    else:
        a, rt = r.randint(2, 7), r.randint(2, 9)
        c = a * rt
        op = r.choice(["<", ">", "≤", "≥"])
        lines = [f"{a}x {op} {c}", f"x {op} {rt + r.choice([-1, 1, 2])}"]
        rows = ["Resolución de un estudiante:", *lines]
    rows = [x.replace("-", "−") for x in rows]
    return make("Observa el procedimiento del estudiante. ¿Qué error cometió?", card(rows, 230, 22), ERR[kind], [x for i, x in enumerate(ERR) if i != kind], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[kind].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_solve_proc(r, l):
    if l == 0:
        a, b, op, c, S = rand_ineq(r, 0)
        eq = f"{lx(a, b)} {op} {c}"
    elif l == 1:
        d = r.choice([2, 3, 4]); k = r.randint(1, 5); e = r.randint(-6, 6); rt = r.randint(-5, 5)
        op = r.choice(["<", "≤", ">", "≥"])
        s_ = r.choice([1, -1])
        # d(kx + m) op rhs  → forma con paréntesis
        m = r.randint(-5, 5)
        rhs = d * (s_ * k * rt + m)
        S = solve_lin(d * s_ * k, d * m, op, rhs)
        eq = f"{d}({lx(s_ * k, m)}) {op} {rhs}"
    else:
        a, b1, c1, rt = r.choice([2, 3, 4, 5]), r.randint(-6, 6), r.randint(-6, 6), r.randint(-4, 4)
        lo_, hi_ = a * rt + b1, a * rt + b1 + r.randint(4, 12)
        op1, op2 = r.choice(["<", "≤"]), r.choice(["<", "≤"])
        S = inter(solve_lin(a, b1, "≥" if op1 == "≤" else ">", lo_), solve_lin(a, b1, op2, hi_))
        eq = f"{lo_} {op1} {lx(a, b1)} {op2} {hi_}"
        if S is None: raise Reject
    eq = eq.replace("-", "−")
    ans = fi(S)
    cands = [fu(m) for m in mutants(S)]
    lo, hi = view(S)
    fig = wrap(560, 190, nrow(80, [], lo, hi) + tag(280, 30, eq, 20), "Recta numérica y la inecuación")
    return make(f"Resuelve la inecuación {eq}.", fig, ans, pick4(ans, cands), Q_PRO, f"Se despeja x cuidando el sentido de la desigualdad: {ans}.")


def rand_iv2(r, k=None):
    a, b = sorted(r.sample(range(-8, 9), 2))
    if b - a < 2: raise Reject
    return I(a, r.choice([True, False]), b, r.choice([True, False]))


def t_sets(r, l):
    A, B = rand_iv2(r), rand_iv2(r)
    if l == 0:
        R_ = inter(A, B)
        if R_ is None: raise Reject
        stem = f"Si A = {fi(A)} y B = {fi(B)}, ¿cuál es A ∩ B?"
        ans = fi(R_)
        cands = [fu(union(A, B)), fi(A), fi(B)] + [fu(m) for m in mutants(R_)]
        fig = nl_fig([("A", [A]), ("B", [B])], *view(A, B))
    elif l == 1:
        R_ = union(A, B)
        stem = f"Si A = {fi(A)} y B = {fi(B)}, ¿cuál es A ∪ B?"
        ans = fu(R_)
        cands = [fi(inter(A, B)), fi(A), fi(B)] + [fu(m) for m in mutants(A)]
        fig = nl_fig([("A", [A]), ("B", [B])], *view(A, B))
    else:
        Cc = rand_iv2(r)
        R_ = inter(inter(A, B), Cc)
        if R_ is None: raise Reject
        stem = f"Si A = {fi(A)}, B = {fi(B)} y C = {fi(Cc)}, ¿cuál es A ∩ B ∩ C?"
        ans = fi(R_)
        cands = [fi(inter(A, B)), fi(inter(B, Cc)), fi(inter(A, Cc))] + [fu(m) for m in mutants(R_)]
        fig = nl_fig([("A", [A]), ("B", [B]), ("C", [Cc])], *view(A, B, Cc))
    return make(stem, fig, ans, pick4(ans, cands), Q_PRO, "Se comparan los extremos, cuidando los círculos llenos y vacíos.")


BY_SKILL = {
    Q_RES: [t_solve1, t_system],
    Q_MOD: [t_budget, t_triangle],
    Q_REP: [t_read, t_count_int],
    Q_ARG: [t_nature, t_props, t_error],
    Q_PRO: [t_solve_proc, t_sets],
}
