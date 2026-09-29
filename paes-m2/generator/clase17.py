"""Clase 17 · Homotecia: dilatación y contracción de figuras en el plano."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO

import geo


def pt(p):
    return f"({fs(p[0])}, {fs(p[1])})"


def hom(O, k, P):
    return (O[0] + k * (P[0] - O[0]), O[1] + k * (P[1] - O[1]))


def isint(p):
    return F(p[0]).denominator == 1 and F(p[1]).denominator == 1


def kstr(k):
    return f"k = {fs(k)}"


def plane(pts_all, pad=2, step=None):
    xs = [float(p[0]) for p in pts_all]; ys = [float(p[1]) for p in pts_all]
    x0, x1 = min(xs + [0]) - pad, max(xs + [0]) + pad
    y0, y1 = min(ys + [0]) - pad, max(ys + [0]) + pad
    span = max(x1 - x0, y1 - y0)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    x0, x1 = cx - span * 0.8, cx + span * 0.8
    y0, y1 = cy - span / 2, cy + span / 2
    x0, x1, y0, y1 = int(x0 // 1), int(-(-x1 // 1)), int(y0 // 1), int(-(-y1 // 1))
    pl = Plot(560, 300, x0, x1, y0, y1)
    pl.axes(1 if x1 - x0 <= 16 else 2, 1 if y1 - y0 <= 10 else 2)
    return pl


def dpoly(pl, pts, fill, stroke=NAVY):
    pl.parts.append(P([(pl.X(float(x)), pl.Y(float(y))) for x, y in pts], fill, stroke, 3))


def dray(pl, A, B, col=ACC):
    pl.parts.append(L(pl.X(float(A[0])), pl.Y(float(A[1])), pl.X(float(B[0])), pl.Y(float(B[1])), col, 2.5, "8 6"))


def label(pl, p, s, dx=0, dy=-18, color_pt=True):
    x, y = pl.X(float(p[0])), pl.Y(float(p[1]))
    pl.parts.append(C(x, y, 6, ACC if color_pt else INK, INK, 2) + tag(x + dx, y + dy, s, 15))


# ---------------------------------------------------------------- Resolver
def choose_k(r, l):
    if l == 0:
        return r.choice([F(2), F(3), F(1, 2), F(4)])
    if l == 1:
        return r.choice([F(2), F(3), F(-1), F(-2), F(1, 2), F(-3), F(3, 2)])
    return r.choice([F(-1, 2), F(3, 2), F(-3, 2), F(2, 3), F(-2, 3), F(-3), F(5, 2), F(-1)])


def t_image_point(r, l):
    for _ in range(200):
        O = (0, 0) if l == 0 else (r.randint(-4, 4), r.randint(-4, 4))
        k = choose_k(r, l)
        P = (r.randint(-6, 6), r.randint(-6, 6))
        if P == O: continue
        Pp = hom(O, k, P)
        if isint(Pp) and abs(Pp[0]) <= 12 and abs(Pp[1]) <= 12 and Pp != P:
            break
    else:
        raise Reject
    dx, dy = P[0] - O[0], P[1] - O[1]
    cands = [(k * P[0], k * P[1]), (O[0] - k * dx, O[1] - k * dy), (O[0] + dx / k, O[1] + dy / k), (P[0] + k, P[1] + k), (O[0] + k * dy, O[1] + k * dx), (k * dx, k * dy), (P[0] + k * dx, P[1] + k * dy)]
    cs = [pt((F(c[0]), F(c[1]))) for c in cands if (F(c[0]), F(c[1])) != Pp]
    ans = pt(Pp)
    pl = plane([O, P, Pp])
    label(pl, O, "O", 18, -18, False); label(pl, P, "P", 18, -18)
    dray(pl, O, P)
    stem = f"Se aplica una homotecia de centro O{pt(O)} y razón {kstr(k)}. ¿Cuáles son las coordenadas de la imagen P' del punto P{pt(P)}?" if l else f"Se aplica una homotecia de centro el origen y razón {kstr(k)}. ¿Cuáles son las coordenadas de la imagen P' del punto P{pt(P)}?"
    return make(stem, pl.svg("Centro de homotecia y punto"), ans, pick4(ans, cs), Q_RES, f"P' = O + k·(P − O) = {pt(O)} + {fs(k)}·{pt((dx, dy))} = {ans}.")


def t_find(r, l):
    for _ in range(200):
        O = (0, 0) if l == 0 else (r.randint(-4, 4), r.randint(-4, 4))
        k = choose_k(r, 1 if l < 2 else 2)
        P = (r.randint(-6, 6), r.randint(-6, 6))
        if P == O: continue
        Pp = hom(O, k, P)
        if isint(Pp) and abs(Pp[0]) <= 12 and abs(Pp[1]) <= 12 and k not in (1,) and Pp != P: break
    else:
        raise Reject
    if l < 2:
        ans = kstr(k)
        cands = [kstr(-k), kstr(1 / k), kstr(-1 / k), kstr(k + 1), kstr(k - 1) if k != 1 else kstr(k + 2), kstr(2 * k)]
        stem = (f"Una homotecia de centro {'el origen' if l == 0 else 'O' + pt(O)} transforma P{pt(P)} en P'{pt(Pp)}. ¿Cuál es su razón?")
        ex = f"(P' − O) = k·(P − O) ⟹ k = {fs(k)}."
        pl = plane([O, P, Pp])
        label(pl, O, "O", 18, -18, False); label(pl, P, "P", 18, -18); label(pl, Pp, "P'", 18, -18)
        dray(pl, O, P if abs(P[0]) + abs(P[1]) > abs(Pp[0]) + abs(Pp[1]) else Pp)
        dray(pl, O, Pp)
    else:
        ans = pt(O)
        d = 1 - k
        cands = [pt(((Pp[0] - P[0]) / (1 + k), (Pp[1] - P[1]) / (1 + k))) if k != -1 else pt((1, 1)), pt(((Pp[0] + k * P[0]) / (1 + k), (Pp[1] + k * P[1]) / (1 + k))) if k != -1 else pt((2, 2)), pt(((k * P[0] - Pp[0]) / (k - 1), (k * P[1] - Pp[1]) / (k - 1))) if False else pt((O[1], O[0])),
                 pt((-O[0], -O[1])) if O != (0, 0) else pt((1, 0)), pt(((Pp[0] - k * P[0]), (Pp[1] - k * P[1]))), pt(((P[0] + Pp[0]) / 2, (P[1] + Pp[1]) / 2)), pt((O[0] + 1, O[1]))]
        stem = f"Una homotecia de razón {kstr(k)} transforma P{pt(P)} en P'{pt(Pp)}. ¿Cuáles son las coordenadas del centro de homotecia?"
        ex = f"O = (P' − k·P)/(1 − k) = {ans}."
        pl = plane([O, P, Pp])
        label(pl, P, "P", 18, -18); label(pl, Pp, "P'", 18, -18)
        dray(pl, P, Pp)
    cs = [c for c in dict.fromkeys(cands) if c != ans]
    return make(stem, pl.svg("Puntos P y P'"), ans, pick4(ans, cs), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_lamp(r, l):
    if l == 0:
        s, d1, d2 = r.choice([(4, 20, 60), (5, 30, 90), (6, 40, 80), (10, 50, 150), (8, 25, 100), (3, 15, 60), (12, 60, 120), (6, 20, 100)])
        S = F(s * d2, d1)
        stem = f"Una lámpara (centro de homotecia) ilumina un objeto de {s} cm de alto ubicado a {d1} cm de ella. Sobre una pantalla situada a {d2} cm de la lámpara, ¿qué altura tiene la sombra?"
        ans = f"{fs(S)} cm"
        cands = [F(s * d1, d2), s + d2 - d1, s * (d2 - d1) // d1 if (s * (d2 - d1)) % d1 == 0 else s + 2, F(s * d2, d2 - d1), s * d2 // 1 if False else s * (d2 - d1), S + s]
        ex = f"Razón de homotecia = {d2}/{d1}: altura = {s}·{d2}/{d1} = {fs(S)} cm."
    elif l == 1:
        s, d1, d2 = r.choice([(4, 30, 90), (2, 10, 50), (3, 20, 60), (5, 25, 100), (6, 30, 60), (2, 15, 90)])
        k = F(d2, d1)
        A = (s * k) ** 2
        stem = f"Una lámpara ilumina una placa cuadrada de {s} cm de lado ubicada a {d1} cm de ella. Sobre una pantalla situada a {d2} cm de la lámpara, ¿qué área tiene la sombra cuadrada?"
        ans = f"{fs(A)} cm²"
        cands = [s * k, s * k ** 3, (s * F(d1, d2)) ** 2, s * s * k, s * s + d2 - d1, (s * k) ** 2 + s * s]
        ex = f"Lado de la sombra = {s}·{d2}/{d1} = {fs(s * k)} cm; área = ({fs(s * k)})² = {fs(A)} cm²."
        S = A
    else:
        h, d, f = r.choice([(180, 600, 3), (170, 500, 5), (120, 300, 2), (200, 400, 4), (150, 300, 6), (90, 180, 2)])
        Ih = F(h * f, d)
        stem = f"En una cámara oscura (homotecia de centro el orificio), un objeto de {h} cm de alto está a {d} cm del orificio. Si la pantalla está a {f} cm del orificio, ¿cómo es la imagen?"
        ans = f"{fs(Ih)} cm de alto, invertida"
        cands = [f"{fs(Ih)} cm de alto, derecha", f"{fs(F(h * d, f))} cm de alto, invertida", f"{fs(F(h * d, f))} cm de alto, derecha", f"{fs(F(h * (d + f), d))} cm de alto, invertida", f"{fs(F(h, f))} cm de alto, invertida", f"{fs(Ih + 1)} cm de alto, invertida"]
        ex = f"Razón = −{f}/{d} (negativa: invierte). Altura = {h}·{f}/{d} = {fs(Ih)} cm."
        cs = [c for c in cands if c != ans]
        d1, d2, s = d, f, h
    if l < 2:
        cs = [f"{fs(F(c_))} {'cm²' if l == 1 else 'cm'}" for c_ in cands if F(c_) != (S if l == 0 else A) and F(c_) > 0]
    # figura: lámpara O, objeto y pantalla
    x1, x2 = 130, 430
    hs = 40
    body = C(50, 130, 10, FILL2, INK, 3) + tag(50, 165, "O", 15) + L(x1, 130 - hs / 2, x1, 130 + hs / 2, ACC, 8) + L(x2, 130 - hs * 1.6, x2, 130 + hs * 1.6, NAVY, 8)
    body += L(50, 130, x2, 130 - hs * 1.6, "#64748B", 2.5, "8 6") + L(50, 130, x2, 130 + hs * 1.6, "#64748B", 2.5, "8 6")
    body += tag(x1, 200, f"{d1 if l < 2 else d1} cm", 15) + tag(x2, 220, f"{d2} cm", 15) + tag(x1, 70, "objeto", 15) + tag(x2, 60, "pantalla" if l < 2 else "imagen", 15)
    if l == 2:
        body = body.replace("x2", "x2")
    fig = wrap(560, 245, body, "Lámpara, objeto y pantalla")
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def t_logo(r, l):
    w, h = r.choice([(2, 3), (3, 4), (4, 5), (2, 5), (3, 5), (5, 6)])
    k = r.choice([2, 3, 4, 5]) if l == 0 else r.choice([F(3, 2), F(5, 2), F(1, 2), F(2, 3), F(3, 4), 2, 3]) if l == 1 else r.choice([F(3, 2), F(5, 2), F(3, 4), F(4, 3), 3, 4])
    if l == 0:
        stem = f"Un logo rectangular de {w} cm × {h} cm se amplía mediante una homotecia de razón {fs(k)}. ¿Cuál es el perímetro del logo ampliado, en cm?"
        val = 2 * (w + h) * k
        cands = [2 * (w + h) * k * k, 2 * (w + h), w * h * k, 2 * (w + h) + k, 2 * (w + h) * k + 2, (w + h) * k, w * h * k * k]
        unit = "cm"
    elif l == 1:
        stem = f"Un logo rectangular de {w} cm × {h} cm se transforma mediante una homotecia de razón {fs(k)}. ¿Cuál es el área del logo resultante, en cm²?"
        val = w * h * k * k
        cands = [w * h * k, w * h * k ** 3, w * h + k, (w + h) * k, w * h * (1 / k) ** 2, w * h * k * k + w, 2 * (w + h) * k]
        unit = "cm²"
    else:
        c = r.choice([20, 25, 40, 50, 100])
        stem = f"Un logo de {w} cm × {h} cm se transforma mediante una homotecia de razón {fs(k)}. Imprimir cuesta ${c} por cm². ¿Cuánto cuesta imprimir el logo resultante?"
        val = w * h * k * k * c
        cands = [w * h * k * c, w * h * k ** 3 * c, w * h * c + k, 2 * (w + h) * k * c, w * h * k * k, w * h * (1 / k) ** 2 * c, w * h * k * k * c + c]
        unit = "$"
    def fmtv(v):
        v = F(v)
        t = f"{int(v):,}".replace(",", ".") if v.denominator == 1 else fs(v)
        return f"${t}" if unit == "$" else f"{t} {unit}"
    ans = fmtv(F(val))
    cs = [fmtv(F(c_)) for c_ in cands if F(c_) != F(val) and F(c_) > 0]
    x, y = 50, 60
    s1 = 40
    sk = min(float(k), 2.4) if k > 1 else float(k) * 1.0
    body = R(x, y, s1 * w / 2, s1 * h / 2 + 30, FILL) if False else ""
    O = (70, 215)
    a1 = (50 + 60, 200 - 30)
    def rect(k_, fill):
        return P([(O[0] + (70 - 0) * k_ * 0 + 0, 0)] , fill) if False else ""
    rw, rh = 55 * w / max(w, h), 55 * h / max(w, h)
    P1 = [(O[0] + 40, O[1] - 35), (O[0] + 40 + rw, O[1] - 35), (O[0] + 40 + rw, O[1] - 35 - rh), (O[0] + 40, O[1] - 35 - rh)]
    kk = min(float(k), 2.6) if k > 1 else max(float(k), 0.5) if k > 0 else 1
    P2 = [(O[0] + (p[0] - O[0]) * kk, O[1] + (p[1] - O[1]) * kk) for p in P1]
    body = P(P2, FILL2) + P(P1, FILL) + C(O[0], O[1], 7, ACC, INK, 2) + tag(O[0] - 10, O[1] + 26, "O", 15)
    for a, b in zip(P1, P2):
        body += L(O[0], O[1], b[0], b[1], "#64748B", 2, "7 6")
    body += tag(150, 260 if False else 24, f"{w} cm × {h} cm", 15)
    return make(stem, wrap(560, 250, body, "Rectángulo y su imagen por homotecia"), ans, pick4(ans, cs), Q_MOD, f"Perímetro ∝ k, área ∝ k²: resultado {ans}.")


# ---------------------------------------------------------------- Representar
def tri_case(r, l):
    for _ in range(300):
        O = (r.randint(-3, 3), r.randint(-3, 3))
        if l == 0:
            k = r.choice([F(2), F(3), F(1, 2)])
        elif l == 1:
            k = r.choice([F(2), F(3), F(-1), F(-2), F(1, 2), F(-1, 2), F(3, 2)])
        else:
            k = r.choice([F(-1), F(-2), F(-1, 2), F(3, 2), F(2, 3), F(-3, 2), F(-3), F(4, 3), F(-2, 3)])
        A = (O[0] + r.choice([1, 2, 3, 4]) * (1 if k > 0 else 1) * r.choice([-1, 1]), O[1] + r.choice([1, 2, 3]) * r.choice([-1, 1]))
        B = (A[0] + r.choice([2, 3, 4]), A[1] + r.choice([-1, 0, 1]))
        C_ = (A[0] + r.choice([0, 1, 2]), A[1] + r.choice([2, 3]))
        pts_ = [A, B, C_]
        img = [hom(O, k, p) for p in pts_]
        if not all(isint(p) for p in img): continue
        if any(abs(v) > 11 for p in img + pts_ for v in p): continue
        if len({*pts_}) < 3 or O in pts_: continue
        # área positiva (no colineales)
        ar = (B[0] - A[0]) * (C_[1] - A[1]) - (B[1] - A[1]) * (C_[0] - A[0])
        if ar == 0: continue
        return O, k, pts_, img
    raise Reject


def fig_tri(O, pts_, img, names=("A", "B", "C")):
    pl = plane([O] + pts_ + img)
    dpoly(pl, pts_, FILL); dpoly(pl, img, FILL2)
    for p, q in zip(pts_, img):
        dray(pl, p, q)
    label(pl, O, "O", 18, -18, False)
    for i, (p, q) in enumerate(zip(pts_, img)):
        pl.parts.append(C(pl.X(float(p[0])), pl.Y(float(p[1])), 5, INK, INK, 1) + C(pl.X(float(q[0])), pl.Y(float(q[1])), 5, INK, INK, 1))
        pl.parts.append(T(pl.X(float(p[0])) - 14, pl.Y(float(p[1])) - 8, names[i], 16) + T(pl.X(float(q[0])) + 16, pl.Y(float(q[1])) - 8, names[i] + "'", 16))
    return pl


def t_ratio_fig(r, l):
    O, k, pts_, img = tri_case(r, l)
    ans = kstr(k)
    cands = [kstr(-k), kstr(1 / k), kstr(-1 / k), kstr(k + 1), kstr(k * 2), kstr(k - 1) if k != 1 else kstr(3)]
    pl = fig_tri(O, pts_, img)
    stem = "En la figura, el triángulo A'B'C' (amarillo) es la imagen del triángulo ABC (azul) por una homotecia de centro O. ¿Cuál es la razón de la homotecia?"
    return make(stem, pl.svg("Triángulo, su imagen por homotecia y su centro"), ans, pick4(ans, cands), Q_REP, f"Se compara OA' con OA en la cuadrícula: k = {fs(k)}.")


CLASS = ["Ampliación (k > 1)", "Reducción (0 < k < 1)", "Ampliación con inversión (k < −1)", "Reducción con inversión (−1 < k < 0)", "Isometría (k = 1 o k = −1)"]


def t_classify(r, l):
    O, k, pts_, img = tri_case(r, 1 if l == 0 else 2)
    if k > 1: idx = 0
    elif 0 < k < 1: idx = 1
    elif k < -1: idx = 2
    elif -1 < k < 0: idx = 3
    else: idx = 4
    pl = fig_tri(O, pts_, img)
    return make("La figura muestra un triángulo ABC y su imagen A'B'C' por una homotecia de centro O. ¿Cómo se clasifica esa homotecia?", pl.svg("Triángulo, imagen y centro de homotecia"), CLASS[idx], [c for i, c in enumerate(CLASS) if i != idx], Q_REP,
                "El signo de k indica si la imagen está del mismo lado del centro (k > 0) o del opuesto (k < 0); su valor absoluto, si amplía o reduce.")


# ---------------------------------------------------------------- Argumentar
TRUE_H = ["Una homotecia conserva la medida de los ángulos", "Una homotecia transforma cada recta en una recta paralela a ella", "El centro de homotecia es un punto que se transforma en sí mismo",
          "Si la razón de una homotecia es k, las áreas se multiplican por k²", "Una homotecia de razón −1 equivale a una simetría central respecto del centro"]
FALSE_H = ["Una homotecia de razón distinta de 1 conserva la longitud de los segmentos", "Si la razón es k, las áreas se multiplican por k", "El centro de homotecia siempre pertenece a la figura original",
           "Una homotecia de razón negativa es una reflexión respecto de un eje", "Una homotecia multiplica por k la medida de los ángulos", "Toda homotecia con k ≠ 1 es una isometría",
           "Una homotecia de razón 2 duplica el área de la figura"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_H), r.sample(FALSE_H, 4)
        stem = "Sobre las homotecias, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_H), r.sample(TRUE_H, 4)
        stem = "Sobre las homotecias, ¿cuál de las siguientes afirmaciones es FALSA?"
    O, k, pts_, img = tri_case(r, 1)
    pl = fig_tri(O, pts_, img)
    return make(stem, pl.svg("Homotecia de un triángulo"), good, bad, Q_ARG, "Una homotecia produce figuras semejantes: conserva ángulos y paralelismo, multiplica longitudes por |k| y áreas por k².")


def t_compose(r, l):
    if l == 0:
        k = r.choice([F(2), F(3), F(4), F(1, 2), F(1, 3), F(2, 3), F(3, 2)])
        stem = f"La homotecia h de centro O y razón {fs(k)} transforma la figura F en F'. ¿Cuál es la razón de la homotecia de centro O que transforma F' en F?"
        ans = 1 / k
        cands = [-k, -1 / k, k, k + 1, 1 - k, 2 * k]
        ex = "La inversa de una homotecia de razón k (mismo centro) es una homotecia de razón 1/k."
    elif l == 1:
        k1, k2 = r.choice([(F(2), F(3)), (F(2), F(1, 2)), (F(3), F(1, 3)), (F(3, 2), F(2)), (F(1, 2), F(1, 3)), (F(2), F(5)), (F(3), F(2, 3))])
        stem = f"Se aplica a una figura una homotecia de centro O y razón {fs(k1)} y luego otra de centro O y razón {fs(k2)}. ¿Cuál es la razón de la homotecia compuesta?"
        ans = k1 * k2
        cands = [k1 + k2, k1 / k2, k2 / k1, k1 - k2, (k1 + k2) / 2, k1 * k2 + 1]
        ex = f"Las razones se multiplican: {fs(k1)}·{fs(k2)} = {fs(ans)}."
    else:
        k1, k2 = r.choice([(F(-2), F(3)), (F(-1, 2), F(4)), (F(-2), F(-3)), (F(3), F(-1, 3)), (F(-3, 2), F(2)), (F(-1), F(-2)), (F(2), F(-5))])
        stem = f"Se aplica a una figura una homotecia de centro O y razón {fs(k1)} y luego otra de centro O y razón {fs(k2)}. ¿Cuál es la razón de la homotecia compuesta y qué efecto tiene?"
        k = k1 * k2
        eff = ("una ampliación" if k > 1 else "una reducción" if 0 < k < 1 else "una ampliación con inversión" if k < -1 else "una reducción con inversión" if -1 < k < 0 else "la figura queda igual" if k == 1 else "una simetría central")
        ans = f"k = {fs(k)}: {eff}"
        def eff_of(v):
            return ("una ampliación" if v > 1 else "una reducción" if 0 < v < 1 else "una ampliación con inversión" if v < -1 else "una reducción con inversión" if -1 < v < 0 else "la figura queda igual" if v == 1 else "una simetría central")
        alts = [k1 + k2, -k, 1 / k, k1 / k2, k + 1]
        cands = [f"k = {fs(v)}: {eff_of(v)}" for v in alts if v != 0]
        cands += [f"k = {fs(k)}: {eff_of(-k) if k != -k else 'una reducción'}", f"k = {fs(-k)}: {eff}"]
        ex = f"k = {fs(k1)}·{fs(k2)} = {fs(k)}: {eff}."
        cs = [c for c in dict.fromkeys(cands) if c != ans]
        fig = card([f"F —(k = {fs(k1)})→ F₁ —(k = {fs(k2)})→ F₂", "Mismo centro O", "Razón compuesta = ?"], 210, 20)
        return make(stem, fig, ans, pick4(ans, cs), Q_ARG, ex)
    cs = [fs(c) for c in cands if c != ans]
    fig = card(["F —(k)→ F'" if l == 0 else f"F —(k = {fs(k1)})→ F₁ —(k = {fs(k2)})→ F₂", "Mismo centro O", "Razón pedida = ?"], 210, 20)
    return make(stem, fig, fs(ans), pick4(fs(ans), cs), Q_ARG, ex)


ERR = ["Multiplicó las coordenadas por k sin considerar que el centro no es el origen", "Ignoró el signo negativo de la razón", "Multiplicó el área por k en lugar de por k²",
       "Sumó k a las coordenadas en lugar de multiplicar la distancia al centro", "Usó la razón inversa (dividió en vez de multiplicar por k)"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    a, b = r.randint(1, 3), r.randint(1, 3)
    P = (a + 2, b + 3)
    kk = r.choice([2, 3])
    if k == 0:
        O = (a, b)
        lines = [f"Centro O{pt(O)}, razón {kk}, punto P{pt(P)}", f"P' = {kk}·P", f"P' = {pt((kk * P[0], kk * P[1]))}"]
    elif k == 1:
        O = (0, 0)
        lines = [f"Centro el origen, razón −{kk}, punto P{pt(P)}", f"P' = {kk}·P", f"P' = {pt((kk * P[0], kk * P[1]))}"]
    elif k == 2:
        A = r.choice([6, 8, 10, 12])
        lines = [f"Homotecia de razón {kk}; área de la figura = {A}", f"Área de la imagen = {A}·{kk}", f"Área = {A * kk}"]
    elif k == 3:
        O = (0, 0)
        lines = [f"Centro el origen, razón {kk}, punto P{pt(P)}", f"P' = P + {kk}", f"P' = {pt((P[0] + kk, P[1] + kk))}"]
    else:
        O = (0, 0)
        lines = [f"Centro el origen, razón {kk}, punto P{pt(P)}", f"P' = P/{kk}", f"P' = {pt((F(P[0], kk), F(P[1], kk)))}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 230, 18), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_lengths(r, l):
    if l == 0:
        a, b, c = r.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
        k = r.choice([F(2), F(3), F(1, 2), F(4), F(5), F(-2), F(-3)])
        AB = c
        A = (1, 1); B = (1 + a, 1 + b)
        stem = f"Una homotecia de razón {fs(k)} transforma el segmento AB, con A{pt(A)} y B{pt(B)}, en A'B'. ¿Cuánto mide A'B'?"
        ans = abs(k) * AB
        cands = [k * AB if k > 0 else AB * k, AB * k * k, AB + abs(k), AB / abs(k) if True else 0, a * abs(k) + b, abs(k) * (a + b), AB * abs(k) + 1]
        ex = f"AB = {AB}; A'B' = |k|·AB = {fs(abs(k))}·{AB} = {fs(ans)}."
    elif l == 1:
        OA, k = r.choice([5, 6, 8, 10, 12, 15, 20]), r.choice([F(3, 5), F(-3, 5), F(-1, 2), F(2, 3), F(-2, 5), F(3, 2), F(-3, 4)])
        OA = OA * k.denominator // (1 if True else 1)
        ans = abs(k) * OA
        stem = f"Una homotecia de centro O y razón {fs(k)} transforma A en A'. Si OA = {OA} cm, ¿cuánto mide OA'?"
        cands = [k * OA, OA / abs(k), OA + abs(k), OA * k * k, OA * abs(k) + OA, OA - abs(k) * OA, abs(k) * OA + 1]
        ex = f"OA' = |k|·OA = {fs(abs(k))}·{OA} = {fs(ans)} cm."
    else:
        k = r.choice([F(2), F(3), F(-2), F(-3), F(1, 2), F(-1, 2), F(3, 2)])
        V = r.choice([[(0, 0), (4, 0), (0, 3)], [(0, 0), (6, 0), (0, 4)], [(1, 1), (5, 1), (1, 4)], [(0, 0), (2, 0), (2, 5)]])
        area = abs((V[1][0] - V[0][0]) * (V[2][1] - V[0][1]) - (V[1][1] - V[0][1]) * (V[2][0] - V[0][0])) / 2
        stem = f"Un triángulo con vértices {', '.join(pt(v) for v in V)} se transforma con una homotecia de razón {fs(k)}. ¿Cuál es el área del triángulo imagen?"
        ans = F(area) * k * k
        cands = [F(area) * abs(k), F(area) * k * k * abs(k), F(area) / (k * k), F(area) + k * k, F(area) * k * k * 2, F(area) * abs(k) * 2, F(area) * k * k + 1]
        ex = f"Área original = {fs(F(area))}; imagen = {fs(F(area))}·k² = {fs(ans)}."
        cs = [fs(c) for c in cands if c != ans and c > 0]
        O = (-1, -1)
        pl = plane(V)
        dpoly(pl, V, FILL)
        for i, v in enumerate(V): label(pl, v, "ABC"[i], 16, -16)
        return make(stem, pl.svg("Triángulo original"), fs(ans), pick4(fs(ans), cs), Q_PRO, ex)
    fig = card([("A' = h(A)"), f"razón k = {fs(k)}", "Longitud pedida = ?"], 200, 22)
    cs = [fs(c) for c in cands if F(c) != F(ans) and F(c) > 0]
    return make(stem, fig, fs(ans), pick4(fs(ans), cs), Q_PRO, ex)


def t_mid(r, l):
    """Aplicar: punto medio / vértice de la imagen de un segmento."""
    for _ in range(200):
        O = (0, 0) if l == 0 else (r.randint(-3, 3), r.randint(-3, 3))
        k = choose_k(r, 0 if l == 0 else 1)
        A = (r.randint(-5, 5), r.randint(-5, 5)); B = (r.randint(-5, 5), r.randint(-5, 5))
        if A == B: continue
        M = (F(A[0] + B[0], 2), F(A[1] + B[1], 2))
        Mp = hom(O, k, M)
        if not (isint(Mp) or l == 2): continue
        if abs(Mp[0]) > 14 or abs(Mp[1]) > 14: continue
        break
    else:
        raise Reject
    cands = [(k * M[0], k * M[1]), hom(O, -k, M), (hom(O, k, A)[0] + hom(O, k, B)[0], hom(O, k, A)[1] + hom(O, k, B)[1]), (hom(O, k, A)[0], hom(O, k, A)[1]), (M[0] + k, M[1] + k), hom(O, 1 / k, M)]
    Ap, Bp = hom(O, k, A), hom(O, k, B)
    ans = pt(Mp)
    cs = [pt(c) for c in cands if c != Mp]
    stem = f"Una homotecia de centro {'el origen' if l == 0 else 'O' + pt(O)} y razón {fs(k)} transforma el segmento AB, con A{pt(A)} y B{pt(B)}, en A'B'. ¿Cuáles son las coordenadas del punto medio de A'B'?"
    pl = plane([O, A, B, Ap, Bp])
    label(pl, O, "O", 16, -16, False); label(pl, A, "A", 16, -16); label(pl, B, "B", 16, -16)
    return make(stem, pl.svg("Segmento AB"), ans, pick4(ans, cs), Q_PRO, f"El punto medio de A'B' es la imagen del punto medio de AB: {ans}.")


BY_SKILL = {
    Q_RES: [t_image_point, t_find],
    Q_MOD: [t_lamp, t_logo],
    Q_REP: [t_ratio_fig, t_classify],
    Q_ARG: [t_props, t_compose, t_error],
    Q_PRO: [t_lengths, t_mid],
}
