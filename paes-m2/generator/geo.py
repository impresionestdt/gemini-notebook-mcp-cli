"""Utilidades de dibujo geométrico (alto contraste, etiquetas sobre píldoras blancas)."""
from svgkit import *


def lerp(P_, Q_, t):
    return (P_[0] + (Q_[0] - P_[0]) * t, P_[1] + (Q_[1] - P_[1]) * t)


def mid(P_, Q_):
    return lerp(P_, Q_, 0.5)


def letter(x, y, s, size=20):
    return T(x, y + 6, s, size, "middle", INK, 800)


def thales_tri(names, lAD, lDB, lAE, lEC, t, lBC=None, lDE=None, ttl=None):
    """Triángulo ABC con DE ∥ BC; D en AB, E en AC, AD/AB = t."""
    a, b, c, d, e = names
    A, B, C = (280, 40), (80, 235), (480, 235)
    D, E = lerp(A, B, t), lerp(A, C, t)
    body = P([A, B, C], FILL) + L(D[0], D[1], E[0], E[1], ACC, 4, "9 6")
    for P_ in (A, B, C, D, E):
        body += C_pt(P_)
    for lb, pos in ((lAD, shift(mid(A, D), -38, 0)), (lDB, shift(mid(D, B), -38, 0)), (lAE, shift(mid(A, E), 38, 0)), (lEC, shift(mid(E, C), 38, 0))):
        if lb: body += tag(*pos, lb, 16)
    if lBC: body += tag(280, 262, lBC, 16)
    if lDE: body += tag(mid(D, E)[0], mid(D, E)[1] - 20, lDE, 16)
    body += letter(A[0], A[1] - 14, a) + letter(B[0] - 20, B[1] + 8, b) + letter(C[0] + 20, C[1] + 8, c) + letter(D[0] - 24, D[1], d) + letter(E[0] + 24, E[1], e)
    return wrap(560, 285, body, "Triángulo con una paralela a un lado")


def C_pt(P_):
    return C(P_[0], P_[1], 5, INK, INK, 1)


def shift(P_, dx, dy):
    return (P_[0] + dx, P_[1] + dy)


def par_fig(a, b, c, d, names=("A", "B", "C", "D", "E", "F")):
    """Tres paralelas horizontales cortadas por dos transversales: segmentos a,b (izq.) y c,d (der.)."""
    n1, n2, n3 = names[:3]
    ys = [40, 40 + 150 * (a[1] / (a[1] + b[1])), 190]
    body = ""
    Lx = lambda y: 120 + 0.14 * (y - 40)
    Rx = lambda y: 440 - 0.10 * (y - 40)
    for y in ys:
        body += L(40, y, 520, y, NAVY, 3)
    body += L(Lx(20), 20, Lx(215), 215, INK, 3) + L(Rx(20), 20, Rx(215), 215, INK, 3)
    for y in ys:
        body += C_pt((Lx(y), y)) + C_pt((Rx(y), y))
    body += tag(Lx((ys[0] + ys[1]) / 2) - 40, (ys[0] + ys[1]) / 2, a[0], 16) + tag(Lx((ys[1] + ys[2]) / 2) - 40, (ys[1] + ys[2]) / 2, b[0], 16)
    body += tag(Rx((ys[0] + ys[1]) / 2) + 40, (ys[0] + ys[1]) / 2, c[0], 16) + tag(Rx((ys[1] + ys[2]) / 2) + 40, (ys[1] + ys[2]) / 2, d[0], 16)
    return wrap(560, 235, body, "Paralelas cortadas por dos transversales")


def right_tri(p, q, labs, names=("A", "B", "C", "D")):
    """Triángulo rectángulo en C con altura CD sobre la hipotenusa AB (AD=p, DB=q)."""
    na, nb, nc, nd = names
    s = 420 / (p + q)
    A, B = (70, 225), (70 + 420, 225)
    Dp = (70 + p * s, 225)
    h = (p * q) ** 0.5 * s
    Cp = (Dp[0], 225 - h)
    body = P([A, B, Cp], FILL) + L(Cp[0], Cp[1], Dp[0], Dp[1], ACC, 4, "9 6")
    # marcas de ángulo recto en C y D
    u = 14
    body += f'<polyline fill="none" stroke="{INK}" stroke-width="2.5" points="{Dp[0] - u},{225} {Dp[0] - u},{225 - u} {Dp[0]},{225 - u}"/>'
    v1 = (A[0] - Cp[0], A[1] - Cp[1]); v2 = (B[0] - Cp[0], B[1] - Cp[1])
    n1 = (v1[0] ** 2 + v1[1] ** 2) ** 0.5; n2 = (v2[0] ** 2 + v2[1] ** 2) ** 0.5
    e1 = (v1[0] / n1 * 16, v1[1] / n1 * 16); e2 = (v2[0] / n2 * 16, v2[1] / n2 * 16)
    body += f'<polyline fill="none" stroke="{INK}" stroke-width="2.5" points="{Cp[0] + e1[0]},{Cp[1] + e1[1]} {Cp[0] + e1[0] + e2[0]},{Cp[1] + e1[1] + e2[1]} {Cp[0] + e2[0]},{Cp[1] + e2[1]}"/>'
    for P_ in (A, B, Cp, Dp):
        body += C_pt(P_)
    body += tag((A[0] + Dp[0]) / 2, 252, labs.get("p", ""), 16) if labs.get("p") else ""
    body += tag((Dp[0] + B[0]) / 2, 252, labs.get("q", ""), 16) if labs.get("q") else ""
    body += tag(Dp[0] + 24, (Cp[1] + 225) / 2, labs.get("h", ""), 16) if labs.get("h") else ""
    body += tag(*shift(mid(A, Cp), -30, -6), labs.get("a", ""), 16) if labs.get("a") else ""
    body += tag(*shift(mid(B, Cp), 30, -6), labs.get("b", ""), 16) if labs.get("b") else ""
    body += tag(280 if False else (A[0] + B[0]) / 2, 280, labs.get("c", ""), 16) if labs.get("c") else ""
    body += letter(A[0] - 16, A[1] + 6, na) + letter(B[0] + 16, B[1] + 6, nb) + letter(Cp[0], Cp[1] - 16, nc) + letter(Dp[0] + 2, 225 + 26 if False else 246, nd, 18)
    return wrap(560, 300, body, "Triángulo rectángulo con la altura sobre la hipotenusa")
