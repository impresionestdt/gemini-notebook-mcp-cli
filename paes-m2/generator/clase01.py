"""Clase 1 · Números reales e irracionales: propiedades y racionalización."""
from fractions import Fraction as F
from math import sqrt, gcd
from mathfmt import E, Raw, fmt, val, rs, sqfree
from svgkit import *
from common import Reject, distinct, make

NONSQ = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15]
Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO = ("Resolver problemas", "Modelar", "Representar",
                                     "Argumentar", "Aplicar procedimientos")


def rect_fig(base, side, center, w=300, h=120):
    x, y = 130, 50
    return wrap(560, 240, R(x, y, w, h) + tag(x + w / 2, y + h + 28, base) + tag(x - 55, y + h / 2, side)
                + tag(x + w / 2, y + h / 2, center), f"Rectángulo con {center}")


# ---------------------------------------------------------------- Resolver
def t_rect_height(r, l):
    if l == 0:
        a, m, k = r.choice([2, 3, 5, 7]), 1, r.randint(1, 9)
    elif l == 1:
        a, m, k = r.choice([2, 3, 5, 6, 7, 10, 11, 13]), 1, r.randint(2, 24)
    else:
        a, m, k = r.choice([2, 3, 5, 6, 7]), r.choice([2, 3, 4]), r.randint(3, 30)
    base = rs(m, a)
    q = F(k, m * a)
    ans = E((q, a))
    cands = [E((F(k, m), a)), E((F(m * a, k), a)), E((q, 1)), E((F(k, m * a * a), a)), E((F(k * a, m), a)), E((F(k, m * a), a * a * a))]
    d = distinct(ans, cands)
    stem = f"Un rectángulo tiene área {k} cm² y base {base} cm. ¿Cuál es su altura, en cm?"
    return make(stem, rect_fig(f"base = {base} cm", "h = ?", f"Área = {k} cm²"), fmt(ans), d, Q_RES,
                f"h = {k}/{base}. Al multiplicar numerador y denominador por √{a} queda {fmt(ans)}.")


def t_conj(r, l):
    if l == 0:
        p, a, b = 1, r.choice([2, 3, 5, 6, 7, 10, 11]), 1
    elif l == 1:
        p, a, b = 1, r.choice([3, 5, 6, 7, 10, 11, 13]), r.choice([2, 3, 5])
    else:
        p, a, b = r.choice([2, 3]), r.choice([2, 3, 5, 6]), r.choice([2, 3, 5, 7])
    if a <= b and l != 0:
        raise Reject
    D = p * p * a - b
    if D <= 0:
        raise Reject
    k = r.choice([2, 3, 4, 6, 8, 10, 12, 15])
    ans = E((F(k * p, D), a), (F(-k, D), b))
    S = p * p * a + b
    cands = [E((F(k * p, D), a), (F(k, D), b)), E((k * p, a), (-k, b)), E((F(k * p, S), a), (F(-k, S), b)),
             E((F(k, D), a), (F(-k * p, D), b)), E((F(k * p, D), a), (F(-k, D), b), (0, 1)) if False else E((F(k, D), a), (F(-k, D), b)),
             E((F(k * p, p * a - b), a), (F(-k, p * a - b), b)) if p * a - b > 0 and p > 1 else E((F(k, D + 1), a))]
    d = distinct(ans, cands)
    base = f"{rs(p, a)} + {rs(1, b)}"
    stem = f"Un rectángulo tiene área {k} cm² y base ({base}) cm. ¿Cuál es su altura, en cm?"
    return make(stem, rect_fig(f"base = ({base}) cm", "h = ?", f"Área = {k} cm²"), fmt(ans), d, Q_RES,
                f"Se racionaliza con el conjugado ({rs(p, a)} − {rs(1, b)}): el denominador queda {D}.")


def t_ratio(r, l):
    if l == 0:
        p, a, b = 1, r.choice([2, 3, 5, 6, 7, 10, 11, 13]), 1
    elif l == 1:
        p = 1
        a, b = r.sample([2, 3, 5, 6, 7, 10], 2)
    else:
        p, a, b = r.choice([2, 3]), r.choice([2, 3, 5, 6]), r.choice([2, 3, 5, 7])
    if p * p * a <= b:
        raise Reject
    dn = p * p * a - b
    S = p * p * a + b
    ans = E((F(S, dn), 1), (F(2 * p, dn), a * b))
    cands = [E((F(S, dn), 1), (F(-2 * p, dn), a * b)), E((F(S, dn), 1)), E((F(S, S), 1), (F(2 * p, S), a * b)),
             E((F(S, dn), 1), (F(p, dn), a * b)), E((F(2 * p, dn), a * b)), E((F(S, dn), 1), (F(2 * p, dn), a + b))]
    d = distinct(ans, cands)
    u, v = rs(p, a), rs(1, b)
    x0, y0, W = 90, 0, 380
    ub = W
    lb = W * (p * sqrt(a) - sqrt(b)) / (p * sqrt(a) + sqrt(b))
    body = (R(x0, 50, ub, 40, FILL) + R(x0, 130, lb, 40, FILL2) + tag(x0 - 40, 70, "AB") + tag(x0 - 40, 150, "CD")
            + tag(x0 + ub / 2, 70, f"{u} + {v}") + tag(x0 + lb / 2, 150, f"{u} − {v}", 16))
    stem = f"El segmento AB mide ({u} + {v}) cm y el segmento CD mide ({u} − {v}) cm. ¿Cuál es el valor de AB/CD?"
    return make(stem, wrap(560, 220, body, "Dos barras: AB y CD"), fmt(ans), d, Q_RES,
                f"AB/CD = ({u}+{v})/({u}−{v}); se multiplica por el conjugado y el denominador queda {dn}.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_segments(r, l):
    m = r.choice([2, 3, 5, 6, 7])
    if l == 0:
        cs = [r.randint(1, 5) for _ in range(3)]
        ms = [m] * 3
    elif l == 1:
        cs = [r.randint(1, 7) for _ in range(4)]
        ms = [m] * 4
    else:
        m2 = r.choice([x for x in [2, 3, 5, 7] if x != m])
        cs = [r.randint(1, 6) for _ in range(4)]
        ms = [m, m2, m, m2]
    Ns = [c * c * mm for c, mm in zip(cs, ms)]
    ans = E(*[(c, mm) for c, mm in zip(cs, ms)])
    tot = sum(cs)
    sN = sum(Ns)
    cands = [E((1, sN)), E((tot, sqfree(m * len(cs))[1] * sqfree(m * len(cs))[0] ** 2)), E((cs[0] + 1, ms[0]), *[(c, mm) for c, mm in zip(cs[1:], ms[1:])]),
             E((cs[0] - 1, ms[0]), *[(c, mm) for c, mm in zip(cs[1:], ms[1:])]), E(*[(c, mm) for c, mm in zip(cs[:-1], ms[:-1])]),
             E((tot, ms[0] * ms[1])), E((tot, sum(set(ms))))]
    d = distinct(ans, cands)
    vals = [sqrt(n) for n in Ns]
    W = 500.0
    x = 30.0
    pts = [x]
    for v in vals:
        x += W * v / sum(vals)
        pts.append(x)
    body = L(30, 120, pts[-1], 120, NAVY, 4)
    for i, px in enumerate(pts):
        body += C(px, 120, 7, ACC) + tag(px, 165, "ABCDE"[i], 18)
    for i, n in enumerate(Ns):
        body += tag((pts[i] + pts[i + 1]) / 2, 75, f"√{n}", 17)
    last = "ABCDE"[len(Ns)]
    stem = f"En la figura, los puntos están alineados. ¿Cuánto mide el segmento A{last}, en cm, si cada tramo mide lo indicado (en cm)?"
    return make(stem, wrap(560, 200, body, "Segmentos consecutivos con longitudes radicales"), fmt(ans), d, Q_PRO,
                "Se extrae el factor cuadrado de cada raíz y se suman las raíces semejantes: " + fmt(ans) + ".")


def t_area_prod(r, l):
    m, n = r.sample([2, 3, 5, 6, 7], 2)
    p, q = r.randint(2, 7), r.randint(2, 7)
    if l == 0:
        s1, s2 = rs(p, m), rs(q, m)
        ans = E((p * q * m, 1))
        cands = [E((p * q, 1)), E((p + q, m)), E((p * q, m)), E((p * q * m, m)), E((p + q + m, 1)), E((p * q * m * m, 1))]
    elif l == 1:
        s1, s2 = rs(p, m), rs(q, n)
        ans = E((p * q, m * n))
        cands = [E((p * q, m + n)), E((p + q, m * n)), E((p * q * m * n, 1)), E((p + q, m + n)), E((p * q, m), (0, 1)), E((p * q * m, n))]
    else:
        s1, s2 = f"{rs(p, m)} + {rs(q, n)}", rs(1, m)
        ans = E((p * m, 1), (q, m * n))
        cands = [E((p * m, 1), (q, n)), E((p, 1), (q, m * n)), E((p * m, 1), (q, m + n)), E((p * m + q, m * n)), E((p * m, 1), (q * m, n)), E((p, m), (q, m * n))]
    d = distinct(ans, cands)
    L1, L2 = ("(" + s1 + ")" if "+" in s1 else s1), s2
    body = R(120, 40, 320, 130) + tag(280, 195, f"{s1} cm") + tag(70, 105, f"{s2} cm", 16) + tag(280, 105, "Área = ?")
    stem = f"Un rectángulo tiene lados de {s1} cm y {s2} cm. ¿Cuál es su área, en cm²?"
    return make(stem, wrap(560, 230, body, "Rectángulo con lados radicales"), fmt(ans), d, Q_PRO,
                "Se multiplican coeficientes y radicandos y luego se simplifica: " + fmt(ans) + ".")


# ---------------------------------------------------------------- Modelar
def cube_fig(face):
    s, dx = 110, 42
    x, y = 190, 95
    body = (R(x, y, s, s, FILL) + P([(x, y), (x + dx, y - dx), (x + s + dx, y - dx), (x + s, y)], FILL3)
            + P([(x + s, y), (x + s + dx, y - dx), (x + s + dx, y + s - dx), (x + s, y + s)], FILL2)
            + tag(x + s / 2, y + s / 2, f"Cara = {face} cm²", 15) + tag(x + s / 2, y + s + 30, "arista = ?", 16))
    return wrap(560, 250, body, "Cubo")


def sq_fig(area, lab_side, fillc=FILL):
    body = R(190, 30, 170, 170, fillc) + tag(275, 115, area) + tag(275, 222, lab_side, 17)
    return wrap(560, 250, body, "Cuadrado")


def t_square(r, l):
    m = r.choice([2, 3, 5, 6, 7, 10])
    if l == 0:
        k = r.randint(2, 8)
        N = k * k * m
        ans = E((k, m))
        cands = [E((m, k * k * 1)) if False else E((m, k)), E((F(N, 2), 1)), E((k * k, m)), E((2 * k, m)), E((k, m * m * 1)) if False else E((F(N, 4), 1)), E((k + 1, m))]
        stem = f"Un jardín cuadrado tiene un área de {N} m². ¿Cuánto mide cada lado, en metros?"
        fig = sq_fig(f"Área = {N} m²", "lado = ?")
        ex = f"lado = √{N} = √({k*k}·{m}) = {fmt(ans)}."
    elif l == 1:
        k = r.randint(3, 10)
        N = k * k * m
        ans = E((4 * k, m))
        cands = [E((k, m)), E((2 * k, m)), E((4 * k * k, m)), E((4 * m, k)), E((8 * k, m)), E((F(N, 4), 1)), E((4, N * 1 + 0)) if False else E((k * m, m))]
        stem = f"Un terreno cuadrado tiene un área de {N} m². ¿Cuántos metros de malla se necesitan para cercarlo por completo?"
        fig = sq_fig(f"Área = {N} m²", "perímetro = ?")
        ex = f"lado = {fmt(E((k, m)))} m, perímetro = 4·lado = {fmt(ans)} m."
    else:
        k = r.randint(2, 6)
        N = k * k * m
        ans = E((k ** 3 * m, m))
        cands = [E((k ** 3, m)), E((k * k * m, m)), E((3 * k * m, m)), E((k ** 3 * m * m, 1)), E((k ** 3 * m, 1)), E((k * m, m)), E((3 * k * k * m, m))]
        stem = f"Cada cara de un cubo tiene un área de {N} cm². ¿Cuál es el volumen del cubo, en cm³?"
        fig = cube_fig(N)
        ex = f"arista = {fmt(E((k, m)))}; volumen = arista³ = {fmt(ans)}."
    d = distinct(ans, cands)
    return make(stem, fig, fmt(ans), d, Q_MOD, ex)


def t_diag(r, l):
    if l == 0:
        s = r.randint(2, 20)
        ans = E((s, 2))
        cands = [E((2, s)), E((2 * s, 1)), E((s, 3)), E((s * s, 2)), E((s + 1, 2)), E((s, 1), (1, 2))]
        w = h = 140
        lab = (f"{s} m", f"{s} m")
        stem = f"Una cancha cuadrada tiene {s} m de lado. ¿Cuánto mide su diagonal, en metros?"
    elif l == 1:
        s = r.randint(2, 9)
        m = r.choice([3, 5, 7, 11])
        ans = E((s, 2 * m))
        cands = [E((2 * s, m)), E((s, m + 2)), E((s * s, 2 * m)), E((s, m)), E((2 * s * m, 1)), E((s, 2), (0, 1)) if False else E((s, 2 * m * m))]
        w = h = 140
        lab = (f"{rs(s, m)} m", f"{rs(s, m)} m")
        stem = f"Un cuadrado tiene lado de {rs(s, m)} m. ¿Cuánto mide su diagonal, en metros?"
    else:
        m = r.choice([2, 3, 5, 7])
        p, q = r.sample(range(1, 8), 2)
        ans = E((1, m * (p * p + q * q)))
        cands = [E((p + q, m)), E((1, m * (p + q))), E((p * p + q * q, m)), E((p + q, 2 * m)), E((1, m * (p * p + q * q) + 1)), E((p * q, m))]
        w, h = 240, 130
        lab = (f"{rs(p, m)} m", f"{rs(q, m)} m")
        stem = f"Un rectángulo tiene lados de {rs(p, m)} m y {rs(q, m)} m. ¿Cuánto mide su diagonal, en metros?"
    d = distinct(ans, cands)
    x, y = 280 - w / 2, 30
    body = (R(x, y, w, h) + L(x, y + h, x + w, y, ACC, 4, "8 6") + tag(x + w / 2, y + h + 28, lab[0], 16)
            + tag(x - 55, y + h / 2, lab[1], 16) + tag(x + w / 2 + 6, y + h / 2 - 4, "d = ?", 16))
    return make(stem, wrap(560, 230, body, "Figura con diagonal"), fmt(ans), d, Q_MOD,
                "Por Pitágoras d² = suma de los cuadrados de los lados; luego se simplifica: " + fmt(ans) + ".")


# ---------------------------------------------------------------- Representar
def t_binom_sq(r, l):
    if l == 0:
        p, a, b = 1, r.choice([2, 3, 5, 6, 7]), r.choice([2, 3, 5, 7])
    elif l == 1:
        p = 1
        a, b = r.sample([2, 3, 5, 6, 7, 8, 10, 12, 14, 15], 2)
    else:
        p, a, b = r.choice([2, 3]), r.choice([2, 3, 5, 6]), r.choice([2, 3, 5, 7])
    if a == b or sqfree(a * b)[1] == 1:
        raise Reject
    tot = a + p * p * b
    ans = E((tot, 1), (2 * p, a * b))
    cands = [E((tot, 1)), E((tot, 1), (p, a * b)), E((tot, 1), (-2 * p, a * b)), E((tot + 2 * p * a * b, 1)), E((tot, 1), (2 * p, a + b)), E((F(tot, 1), 1), (4 * p, a * b))]
    d = distinct(ans, cands)
    x0, y0, S = 170, 20, 220
    fa = sqrt(a) / (sqrt(a) + p * sqrt(b))
    w1 = S * fa
    w2 = S - w1
    cross = rs(p, a * b)
    body = (R(x0, y0, w1, w1, FILL) + R(x0 + w1, y0, w2, w1, FILL2) + R(x0, y0 + w1, w1, w2, FILL2) + R(x0 + w1, y0 + w1, w2, w2, FILL)
            + tag(x0 + w1 / 2, y0 + w1 / 2, str(a), 17) + tag(x0 + w1 + w2 / 2, y0 + w1 / 2, cross, 15)
            + tag(x0 + w1 / 2, y0 + w1 + w2 / 2, cross, 15) + tag(x0 + w1 + w2 / 2, y0 + w1 + w2 / 2, str(p * p * b), 17)
            + tag(x0 + S / 2, y0 + S + 26, f"lado = {rs(1, a)} + {rs(p, b)}", 16))
    stem = f"El cuadrado de la figura tiene lado ({rs(1, a)} + {rs(p, b)}) cm y sus regiones tienen las áreas indicadas (en cm²). ¿Cuál es el área total del cuadrado?"
    return make(stem, wrap(560, 290, body, "Cuadrado dividido en cuatro regiones"), fmt(ans), d, Q_REP,
                f"Se suman las cuatro regiones: {a} + {p*p*b} + 2·{cross} = {fmt(ans)}.")


def _line_fig(val_, M, label="P"):
    x0, sc = 30, 500 / M
    body = L(x0, 130, x0 + 500, 130, INK, 3)
    for i in range(M + 1):
        body += L(x0 + i * sc, 120, x0 + i * sc, 140, INK, 3) + T(x0 + i * sc, 168, str(i), 17)
    px = x0 + val_ * sc
    body += C(px, 130, 8, ACC) + tag(px, 85, label, 18)
    return wrap(560, 190, body, f"Recta numérica con el punto {label}")


def _fam(r, l):
    if l == 0:
        n = r.choice([x for x in range(2, 31) if sqfree(x)[1] == x])
        e = E((1, n)); return fmt(e), val(e), 6
    if l == 1:
        p, n = r.randint(1, 3), r.choice([2, 3, 5, 6, 7, 8, 10])
        e = E((p, 1), (1, n)); return fmt(e), val(e), 7
    p, n, q = r.randint(1, 6), r.choice([2, 3, 5, 6, 7]), r.choice([1, 2, 3])
    e = E((F(p, q), n)); return fmt(e), val(e), 8


def t_numline(r, l):
    fam = [_fam(r, l) for _ in range(80)]
    M = fam[0][2]
    pool = {}
    for s, v, _ in fam:
        if 0.6 < v < M - 0.6:
            pool[s] = v
    items = list(pool.items())
    if len(items) < 6:
        raise Reject
    ts, tv = r.choice(items)
    others = sorted([(abs(v - tv), s, v) for s, v in items if s != ts])
    chosen = []
    for _, s, v in others:
        if abs(v - tv) >= 0.45 and all(abs(v - c[1]) >= 0.45 for c in chosen):
            chosen.append((s, v))
        if len(chosen) == 4:
            break
    if len(chosen) < 4:
        raise Reject
    d = [s for s, _ in chosen]
    return make("¿Cuál de los siguientes números está representado por el punto P en la recta numérica?",
                _line_fig(tv, M), ts, d, Q_REP, f"{ts} ≈ {tv:.2f}, que es la posición de P en la recta.")


# ---------------------------------------------------------------- Argumentar
VENN_OPTS = ["Natural (ℕ)", "Entero no natural (ℤ)", "Racional no entero (ℚ)", "Irracional (I)", "No real (ℂ, no ℝ)"]


def venn_fig(expr):
    b = tag(280, 24, f"x = {expr}", 18)
    body = (R(4, 4, 552, 277, "#F1F5F9", NAVY, 3) + R(18, 46, 524, 222, WHITE, NAVY, 3)
            + ELL(200, 160, 170, 95, "#E0F2FE") + ELL(150, 160, 110, 65, "#BAE6FD") + ELL(115, 160, 60, 38, "#7DD3FC")
            + ELL(440, 160, 85, 80, FILL2)
            + T(28, 40, "ℂ", 20, "start") + T(532, 66, "ℝ", 20, "end") + T(115, 166, "ℕ", 22) + T(218, 166, "ℤ", 22) + T(315, 166, "ℚ", 22)
            + T(440, 166, "I", 22) + T(440, 195, "(irracionales)", 14) + b)
    return wrap(560, 285, body, "Diagrama de conjuntos numéricos")


def _x(r, l):
    ks = r.randint(2, 15)
    a, b = r.sample([2, 3, 5, 6, 7, 10, 11], 2)
    if l == 0:
        return r.choice([
            (f"√{ks*ks}", 0), (f"−√{ks*ks}", 1), (f"{r.randint(1,9)}/{r.choice([4,8,9,11])}", 2),
            (f"√{a*ks*ks if False else a}", 3), (f"{r.randint(2,5)}√{a}", 3), (f"√(−{ks})", 4),
            (f"√({a}−{a+ks})", 4), (f"√({ks*ks}/9)".replace("9", "9") if ks % 3 else f"√({ks*ks}/9)", 2 if ks % 3 else 0)])
    if l == 1:
        return r.choice([
            (f"√{ks*ks*a}/√{a}", 0), (f"√{a}·√{a}", 0), (f"(√{b} − √{a})(√{b} + √{a})" if b > a else f"(√{a} − √{b})(√{a} + √{b})", 0),
            (f"(√{a} − √{b})(√{a} + √{b})" if a < b else f"(√{b} − √{a})(√{b} + √{a})", 1), (f"√{a}·√{b}", 3),
            (f"{ks}/√{a}", 3), (f"√{ks*ks*a}/√{2*a}", 3 if sqfree(ks*ks*a*2)[1] != 1 else 0),
            (f"√{a}/√{b}", 3), (f"(√{a})²/{b}", 2 if a % b else 0)])
    return r.choice([
        (f"(1 + √{a})²", 3), (f"√{a} − (√{a} + {ks})", 1), (f"(√{a} + √{b})² − {a+b}", 3),
        (f"(√{a} + {ks})(√{a} − {ks})", 1 if a < ks * ks else 0), (f"√{a} + (5 − √{a})", 0),
        (f"(2√{a})² / {b}", 2 if (4 * a) % b else 0), (f"√{a}·√({a}·{ks*ks})", 0), (f"√({a} − {b}·{a})", 4),
        (f"(√{a} + √{b})(√{a} − √{b}) + {ks}" if a > b else f"(√{b} + √{a})(√{b} − √{a}) + {ks}", 0)])


def t_venn(r, l):
    ex, k = _x(r, l)
    o = list(VENN_OPTS)
    correct = o[k]
    d = [x for i, x in enumerate(o) if i != k]
    return make("Observa el diagrama de conjuntos numéricos. ¿A qué conjunto pertenece el número x?", venn_fig(ex), correct, d, Q_ARG,
                f"Al calcular el valor de x se obtiene un número que pertenece a: {correct}.")


def _pair(a, b):
    return f"{a} y {b}"


def t_counter(r, l):
    a, b = r.sample([2, 3, 5, 6, 7, 10, 11], 2)
    p, q = r.randint(1, 5), r.randint(1, 5)
    if l == 0:
        claim = "La suma de dos números irracionales es siempre un número irracional."
        good = _pair(f"√{a}", f"−√{a}")
        bad = [_pair(f"√{a}", f"√{b}"), _pair(f"√{a}", f"{p+1}√{a}"), _pair(f"π", f"{q}"), _pair(f"√{b}", f"2√{b}")]
        sk, sub, ex = "a + b", "suma", "√a + (−√a) = 0, que es racional."
    elif l == 1:
        claim = "La suma de dos números irracionales es siempre un número irracional."
        good = _pair(f"{p} + √{a}", f"{q} − √{a}")
        bad = [_pair(f"{p} + √{a}", f"{q} + √{a}"), _pair(f"{p} + √{a}", f"{q} − √{b}"), _pair(f"{p}√{a}", f"{q}√{b}"), _pair(f"√{a} − {p}", f"√{a} + {q}")]
        sk, sub, ex = "a + b", "suma", f"({p} + √{a}) + ({q} − √{a}) = {p+q}, racional."
    else:
        claim = "El producto de dos números irracionales es siempre un número irracional."
        good = r.choice([_pair(f"√{a}", f"√{a}"), _pair(f"1 + √{a}", f"1 − √{a}"), _pair(f"√{a}", f"{2}√{a}")])
        bad = [_pair(f"√{a}", f"√{b}"), _pair(f"√{a}", f"1 + √{b}"), _pair(f"√{a}", f"1 + √{a}"), _pair(f"{p}√{a}", f"√{b}")]
        sk, sub, ex = "a · b", "producto", "El producto resulta racional, lo que refuta la afirmación."
    if len(set(bad + [good])) != 5:
        raise Reject
    sk_svg = (R(60, 40, 440, 60, "#F1F5F9") + T(280, 78, f"a, b ∈ I  ⟹  {sk} ∈ I", 22)
              + T(280, 150, "¿Siempre se cumple?", 20) + tag(280, 190, "Se busca un contraejemplo", 18))
    return make(f"Una estudiante afirma: «{claim}» ¿Cuál de los siguientes pares de números sirve como contraejemplo?",
                wrap(560, 230, sk_svg, "Conjetura sobre irracionales"), good, bad, Q_ARG, ex)


def t_denest(r, l):
    if l == 0:
        p, a, b = 1, r.choice([2, 3, 5, 6, 7, 10, 11]), r.choice([1, 2, 3, 5])
    elif l == 1:
        p = 1
        a, b = r.sample([2, 3, 5, 6, 7, 10, 11, 13], 2)
    else:
        p, a, b = r.choice([2, 3]), r.choice([2, 3, 5, 6, 7]), r.choice([2, 3, 5, 7])
    if a == b or sqfree(a * b)[1] != a * b:
        raise Reject
    tot = a + p * p * b
    area = fmt(E((tot, 1), (2 * p, a * b)))
    good = f"√{a} + {rs(p, b)}"
    bad_c = [f"√{tot} + √{4 * p * p * a * b}", f"√{a + 1} + {rs(p, b)}", f"√{a} + {rs(p, b + 1)}", f"√{tot} + {rs(1, 2)}", f"√{a * b} + {p}", f"{rs(p, a)} + √{b}"]
    bad = []
    for c in bad_c:
        if c != good and c not in bad:
            bad.append(c)
    if len(bad) < 4:
        raise Reject
    bad = bad[:4]
    body = sq_fig(f"Área = ({area}) cm²", "lado = ?")
    return make(f"Un cuadrado tiene un área de ({area}) cm². ¿Cuál de las siguientes expresiones representa la medida de su lado, en cm?",
                body, good, bad, Q_ARG, f"({good})² = {a} + {p*p*b} + 2·{rs(p, a*b)} = {area}, por lo que el lado es {good}.")


BY_SKILL = {
    Q_RES: [t_rect_height, t_conj, t_ratio],
    Q_MOD: [t_square, t_diag],
    Q_REP: [t_binom_sq, t_numline],
    Q_ARG: [t_venn, t_counter, t_denest],
    Q_PRO: [t_segments, t_area_prod],
}
