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


def _tri_pts(x0, base, y0=215):
    return (x0, y0), (x0 + base, y0), (x0 + 0.34 * base, y0 - 0.78 * base)


def sim_tris(k, small, big, inside_s="", inside_b="", ttl=("", "")):
    """Dos triángulos semejantes (razón visual limitada). small/big: dict(base, left, right) con textos."""
    kv = min(float(k), 2.4)
    bs = 110
    bb = bs * kv
    A1, B1, C1 = _tri_pts(40, bs)
    A2, B2, C2 = _tri_pts(40 + bs + 60 + (300 - bb) * 0.0, bb)
    A2 = (A2[0] + 30, A2[1]); B2 = (B2[0] + 30, B2[1]); C2 = (C2[0] + 30, C2[1])
    body = P([A1, B1, C1], FILL) + P([A2, B2, C2], FILL2)
    if small.get("base"): body += tag((A1[0] + B1[0]) / 2, 242, small["base"], 15)
    if small.get("left"): body += tag(*shift(mid(A1, C1), -34, 0), small["left"], 15)
    if small.get("right"): body += tag(*shift(mid(B1, C1), 34, 0), small["right"], 15)
    if big.get("base"): body += tag((A2[0] + B2[0]) / 2, 242, big["base"], 15)
    if big.get("left"): body += tag(*shift(mid(A2, C2), -34, 0), big["left"], 15)
    if big.get("right"): body += tag(*shift(mid(B2, C2), 34, 0), big["right"], 15)
    if inside_s: body += tag(C1[0], C1[1] - 26, inside_s, 15)
    if inside_b: body += tag(C2[0], C2[1] - 26, inside_b, 15)
    if ttl[0]: body += tag(A1[0] + 55, 22, ttl[0], 15)
    if ttl[1]: body += tag(A2[0] + bb / 2, 22, ttl[1], 15)
    return wrap(560, 262, body, "Dos triángulos semejantes")


def cube(x, y, s, fill=FILL):
    d = s * 0.38
    return (R(x, y - s, s, s, fill) + P([(x, y - s), (x + d, y - s - d), (x + s + d, y - s - d), (x + s, y - s)], FILL3)
            + P([(x + s, y - s), (x + s + d, y - s - d), (x + s + d, y - d), (x + s, y)], "#BFDBFE"))


def two_cubes(k, lab_s, lab_b, info=("", "")):
    kv = min(float(k), 2.6)
    s1 = 60
    s2 = s1 * kv
    y = 215
    body = cube(60, y, s1, FILL) + cube(60 + s1 + 90, y, s2, FILL2)
    body += tag(60 + s1 / 2, y + 28, lab_s, 15) + tag(60 + s1 + 90 + s2 / 2, y + 28, lab_b, 15)
    if info[0]: body += tag(60 + s1 / 2, 22, info[0], 15)
    if info[1]: body += tag(60 + s1 + 90 + s2 / 2, 22, info[1], 15)
    return wrap(560, 268, body, "Dos cubos semejantes")


def two_discs(r1, r2, l1, l2, i1="", i2=""):
    sc = 90 / max(r1, r2)
    a, b = r1 * sc, r2 * sc
    body = C(150, 140, a, FILL, NAVY, 4) + C(400, 140, b, FILL2, NAVY, 4)
    body += tag(150, 250, l1, 15) + tag(400, 250, l2, 15)
    if i1: body += tag(150, 24, i1, 15)
    if i2: body += tag(400, 24, i2, 15)
    return wrap(560, 275, body, "Dos círculos")


def two_squares(k, lab_s, lab_b):
    kv = min(float(k), 2.6)
    s1 = 70
    s2 = s1 * kv
    y = 210
    body = R(80, y - s1, s1, s1, FILL) + R(80 + s1 + 100, y - s2, s2, s2, FILL2)
    body += tag(80 + s1 / 2, y + 28, lab_s, 15) + tag(80 + s1 + 100 + s2 / 2, y + 28, lab_b, 15)
    return wrap(560, 270, body, "Dos cuadrados")


def trig_tri(adj, opp, labs, ang="α", show_other=None, names=("A", "B", "C")):
    """Triángulo rectángulo en C (abajo a la derecha). α en A (abajo a la izquierda).
    adj: cateto adyacente a α (horizontal), opp: cateto opuesto (vertical). Sólo se usa la proporción."""
    na, nb, nc = names
    s = min(360 / adj, 175 / opp)
    W, H = adj * s, opp * s
    A, C_, B = (90, 235), (90 + W, 235), (90 + W, 235 - H)
    body = P([A, B, C_], FILL)
    # ángulo recto en C
    u = 14
    body += f'<polyline fill="none" stroke="{INK}" stroke-width="2.5" points="{C_[0] - u},{C_[1]} {C_[0] - u},{C_[1] - u} {C_[0]},{C_[1] - u}"/>'
    # arco de α en A
    import math
    th = math.atan2(H, W)
    r_ = 34
    body += f'<path d="M {A[0] + r_} {A[1]} A {r_} {r_} 0 0 0 {A[0] + r_ * math.cos(th):.1f} {A[1] - r_ * math.sin(th):.1f}" fill="none" stroke="{ACC}" stroke-width="3.5"/>'
    body += tag(A[0] + 58, A[1] - 12 - 6 * (H < 90), ang, 16)
    if show_other:
        th2 = math.pi / 2 - th
        body += f'<path d="M {B[0]} {B[1] + r_} A {r_} {r_} 0 0 0 {B[0] - r_ * math.sin(th):.1f} {B[1] + r_ * math.cos(th):.1f}" fill="none" stroke="{NAVY}" stroke-width="3.5"/>'
        body += tag(B[0] - 44, B[1] + 44, show_other, 16)
    for P_ in (A, B, C_):
        body += C(P_[0], P_[1], 5, INK, INK, 1)
    if labs.get("adj"): body += tag((A[0] + C_[0]) / 2, 268, labs["adj"], 16)
    if labs.get("opp"): body += tag(C_[0] + 40, (B[1] + C_[1]) / 2, labs["opp"], 16)
    if labs.get("hyp"): body += tag(*shift(mid(A, B), -34, -22), labs["hyp"], 16)
    body += letter(A[0] - 18, A[1] + 6, na) + letter(B[0] + 4, B[1] - 16, nb) + letter(C_[0] + 20, C_[1] + 8, nc)
    return wrap(560, 290, body, "Triángulo rectángulo con un ángulo agudo marcado")


def elev_fig(kind, dist, height, ang, eye=None, ang2=None, dist2=None):
    """Ángulo de elevación (kind='elev') o de depresión (kind='dep').
    dist, height, ang, eye: textos (pueden ser '' o '?'). ang2/dist2: segunda observación."""
    import math
    ground = 235
    body = L(20, ground, 540, ground, INK, 3)
    if kind == "elev":
        ox, tx = 90, 440
        H = 150
        eyey = ground - (28 if eye else 22)
        body += R(tx - 16, ground - H, 32, H, FILL2)  # torre
        body += C(ox, ground - 42, 9, FILL, INK, 2.5) + L(ox, ground - 33, ox, ground - 10, INK, 4) + L(ox, ground - 10, ox - 8, ground, INK, 3) + L(ox, ground - 10, ox + 8, ground, INK, 3)
        top = (tx, ground - H)
        eye_p = (ox + 10, ground - 42)
        body += L(eye_p[0], eye_p[1], tx + 0, top[1], ACC, 3.5)
        body += L(eye_p[0], eye_p[1], tx - 16, eye_p[1], INK, 2.5, "8 6")
        th = math.atan2(eye_p[1] - top[1], tx - eye_p[0])
        body += f'<path d="M {eye_p[0] + 60} {eye_p[1]} A 60 60 0 0 0 {eye_p[0] + 60 * math.cos(th):.1f} {eye_p[1] - 60 * math.sin(th):.1f}" fill="none" stroke="{NAVY}" stroke-width="3.5"/>'
        body += tag(eye_p[0] + 92, eye_p[1] - 14, ang, 16)
        if dist: body += tag((ox + tx) / 2, ground + 22, dist, 16)
        if height: body += tag(tx + 44, ground - H / 2, height, 16)
        if eye: body += tag(ox - 4, ground - 66, eye, 14)
        if ang2:
            ox2 = ox + 150
            eye2 = (ox2 + 10, ground - 42)
            body += C(ox2, ground - 42, 9, FILL, INK, 2.5) + L(ox2, ground - 33, ox2, ground - 10, INK, 4) + L(ox2, ground - 10, ox2 - 8, ground, INK, 3) + L(ox2, ground - 10, ox2 + 8, ground, INK, 3)
            body += L(eye2[0], eye2[1], tx, top[1], "#475569", 3, "9 6")
            th2 = math.atan2(eye2[1] - top[1], tx - eye2[0])
            body += f'<path d="M {eye2[0] + 44} {eye2[1]} A 44 44 0 0 0 {eye2[0] + 44 * math.cos(th2):.1f} {eye2[1] - 44 * math.sin(th2):.1f}" fill="none" stroke="{NAVY}" stroke-width="3.5"/>'
            body += tag(eye2[0] + 62, eye2[1] - 34, ang2, 15)
            if dist2: body += tag((ox + ox2) / 2, ground + 22 if not dist else ground + 50, dist2, 15)
        return wrap(560, 285, body, "Ángulo de elevación")
    # depresión
    cx, bx = 130, 450
    H = 150
    top = (cx, ground - H)
    body += R(cx - 60, ground - H, 60, H, FILL2) + R(20, ground, 520, 26, "#BFDBFE") if False else R(cx - 60, ground - H, 60, H, FILL2)
    body += C(cx + 10, top[1] - 9, 9, FILL, INK, 2.5) + L(cx + 10, top[1], cx + 10, top[1] + 0, INK, 1)
    src = (cx + 10, top[1] - 9)
    body += L(src[0], src[1], bx, ground - 8, ACC, 3.5) + L(src[0], src[1], bx, src[1], INK, 2.5, "8 6")
    # barco
    body += P([(bx - 26, ground - 8), (bx + 26, ground - 8), (bx + 16, ground + 4), (bx - 16, ground + 4)], FILL, NAVY, 3) + L(bx, ground - 8, bx, ground - 34, INK, 3)
    th = math.atan2(ground - 8 - src[1], bx - src[0])
    body += f'<path d="M {src[0] + 62} {src[1]} A 62 62 0 0 1 {src[0] + 62 * math.cos(th):.1f} {src[1] + 62 * math.sin(th):.1f}" fill="none" stroke="{NAVY}" stroke-width="3.5"/>'
    body += tag(src[0] + 100, src[1] + 30, ang, 16)
    if height: body += tag(cx - 90, ground - H / 2, height, 16)
    if dist: body += tag((cx + bx) / 2, ground + 30, dist, 16)
    return wrap(560, 285, body, "Ángulo de depresión")


def box3d(a, b, c, labs=None, diags=(), names=("A", "B", "C", "D", "E", "F", "G", "H"), dashed=(), letters=True):
    """Caja rectangular. Base ABCD (A frente-izq., B frente-der., C fondo-der., D fondo-izq.), techo EFGH sobre A,B,C,D.
    a: largo AB, b: ancho BC (profundidad), c: alto."""
    labs = labs or {}
    s = min(250 / a, 150 / c, 120 / (b * 0.5))
    w, h, dx = a * s, c * s, b * s * 0.5
    dy = b * s * 0.32
    x0, y0 = 90, 238
    A = (x0, y0); B = (x0 + w, y0); Cc = (x0 + w + dx, y0 - dy); D = (x0 + dx, y0 - dy)
    E, F_, G, H_ = (A[0], A[1] - h), (B[0], B[1] - h), (Cc[0], Cc[1] - h), (D[0], D[1] - h)
    pts = dict(zip(names, (A, B, Cc, D, E, F_, G, H_)))
    body = P([E, F_, G, H_], "#93C5FD") + P([A, B, F_, E], FILL) + P([B, Cc, G, F_], "#BFDBFE")
    for u, v in (("A", "D"), ("D", "C"), ("D", "H")):
        p1, p2 = pts[names[("ABCDEFGH").index(u)]], pts[names[("ABCDEFGH").index(v)]]
        body += L(p1[0], p1[1], p2[0], p2[1], "#64748B", 2, "6 5")
    for u, v in diags:
        p1, p2 = pts[names[("ABCDEFGH").index(u)]], pts[names[("ABCDEFGH").index(v)]]
        body += L(p1[0], p1[1], p2[0], p2[1], ACC, 4, "9 5" if (u, v) in dashed else None)
    if letters:
        for nm, key in zip(names, "ABCDEFGH"):
            p = pts[nm]
            off = {"A": (-16, 16), "B": (16, 16), "C": (18, 4), "D": (-14, 4), "E": (-16, -6), "F": (12, -12), "G": (16, -8), "H": (-14, -12)}[key]
            body += letter(p[0] + off[0], p[1] + off[1], nm, 18)
    if labs.get("a"): body += tag((A[0] + B[0]) / 2, y0 + 34, labs["a"], 15)
    if labs.get("b"): body += tag((B[0] + Cc[0]) / 2 + 30, (B[1] + Cc[1]) / 2 + 16, labs["b"], 15)
    if labs.get("c"): body += tag(A[0] - 36, (A[1] + E[1]) / 2, labs["c"], 15)
    return wrap(560, 300, body, "Caja rectangular con sus diagonales")
