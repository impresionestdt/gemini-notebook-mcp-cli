"""Figuras para Matemática M1: recta numérica, barras con signo, saltos."""
from svgkit import *


def numline(lo, hi, marks=None, step=1, jumps=None, hl=None, w=560, fmt=None):
    """Recta numérica de lo a hi. marks: {rótulo: valor} (círculo + píldora); jumps: [(desde, hasta, texto)] como arcos."""
    x0, x1, y = 40, w - 40, 130
    X = lambda v: x0 + float((v - lo) / (hi - lo)) * (x1 - x0)
    body = L(x0 - 14, y, x1 + 14, y, INK, 3.5)
    body += P([(x1 + 22, y), (x1 + 8, y - 7), (x1 + 8, y + 7)], INK, INK, 1) + P([(x0 - 22, y), (x0 - 8, y - 7), (x0 - 8, y + 7)], INK, INK, 1)
    v = lo
    while v <= hi + 1e-9:
        big = abs(v) < 1e-9
        body += L(X(v), y - (10 if big else 7), X(v), y + (10 if big else 7), INK, 3 if big else 2)
        body += T(X(v), y + 34, (fmt(v) if fmt else z_(v)), 15)
        v += step
    for i, (a, b, t) in enumerate(jumps or []):
        xa, xb = X(a), X(b)
        top = y - 52 - 34 * i
        body += f'<path d="M {xa:.1f} {y - 8} C {xa:.1f} {top - 14} {xb:.1f} {top - 14} {xb:.1f} {y - 8}" fill="none" stroke="{ACC}" stroke-width="3.5"/>'
        body += P([(xb, y - 6), (xb - 7, y - 20), (xb + 7, y - 20)], ACC, ACC, 1)
        body += tag((xa + xb) / 2, top - 6, t, 16)
    for lab, val in (marks or {}).items():
        body += C(X(val), y, 8, ACC, INK, 2) + tag(X(val), y - 34, lab, 17)
    return wrap(w, 190, body, "Recta numérica")


def z_(v):
    from fractions import Fraction as F
    x = F(v).limit_denominator(1000)
    s = str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"
    return s.replace("-", "−")


def signed_bars(vals, labels, unit="", w=560, h=260):
    """Barras hacia arriba (positivas) y hacia abajo (negativas) con una línea de cero."""
    n = len(vals)
    top = max(max(vals), 0)
    bot = min(min(vals), 0)
    span = (top - bot) or 1
    ptop, pbot = 40, h - 56
    sc = (pbot - ptop) / span
    y0 = ptop + top * sc
    bw = min(64, 440 // n)
    gap = (w - 80 - n * bw) / max(1, n - 1)
    body = ""
    for i, (v, lab) in enumerate(zip(vals, labels)):
        x = 40 + i * (bw + gap)
        hh = abs(v) * sc
        yy = y0 - hh if v >= 0 else y0
        body += R(x, yy, bw, hh, FILL if v >= 0 else FILL2)
        body += tag(x + bw / 2, (yy - 18) if v >= 0 else (yy + hh + 18), z_(v) + (" " + unit if unit else ""), 15)
        body += T(x + bw / 2, h - 12, lab, 16)
    body += L(20, y0, w - 20, y0, INK, 3)
    return wrap(w, h, body, "Gráfico de barras con valores positivos y negativos")


def timeline(rows, span, hl=None, w=560):
    """rows: [(rótulo, período)]. Puntos en los múltiplos del período hasta span; hl: valores resaltados con píldora."""
    x0, x1 = 60, w - 30
    X = lambda v: x0 + v / span * (x1 - x0)
    n = len(rows)
    h = 60 + 70 * n
    body = ""
    for i, (lab, per) in enumerate(rows):
        y = 60 + 70 * i
        tw = len(lab) * 15 * 0.62 + 16
        body += tag(14 + tw / 2, y - 26, lab, 15) + L(x0, y, x1 + 8, y, INK, 3)
        v = per
        while v <= span + 1e-9:
            body += C(X(v), y, 7, ACC, INK, 2)
            v += per
    yb = h - 18
    body += L(x0, yb - 14, x1 + 8, yb - 14, INK, 2)
    step = next(s for s in (1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30) if span / s <= 12)
    for v in range(0, int(span) + 1, step):
        body += L(X(v), yb - 20, X(v), yb - 8, INK, 2) + T(X(v), yb + 12, str(v), 14)
    return wrap(w, h + 12, body, "Eventos que se repiten periódicamente")


def factor_tree(primes, hide=None, w=560):
    """Árbol de factores: raíz = producto; a la izquierda cada primo y a la derecha el resto. hide: índice de nodo oculto (1..)."""
    k = len(primes)
    vals = []
    rem = 1
    for p in primes:
        rem *= p
    comp = [rem]
    for p in primes[:-2]:
        comp.append(comp[-1] // p)
    dy = 66
    h = 40 + dy * (k - 1) + 40
    nodes = []
    body = ""
    # posiciones: compuestos en diagonal
    pos_c = [(200 + 48 * i, 36 + dy * i) for i in range(k - 1)]
    idx = 0
    edges = ""
    circ = ""
    for i in range(k - 1):
        cx, cy = pos_c[i]
        val = comp[i]
        nodes.append((cx, cy, val, False))
        # hijo primo (izquierda)
        px, py = cx - 62, cy + dy
        nodes.append((px, py, primes[i], True))
        edges += L(cx, cy, px, py, NAVY, 3)
        if i < k - 2:
            nx, ny = pos_c[i + 1]
            edges += L(cx, cy, nx, ny, NAVY, 3)
        else:
            qx, qy = cx + 62, cy + dy
            nodes.append((qx, qy, primes[-1], True))
            edges += L(cx, cy, qx, qy, NAVY, 3)
    for j, (cx, cy, val, isp) in enumerate(nodes):
        hid = hide is not None and j == hide
        circ += f'<circle cx="{cx}" cy="{cy}" r="27" fill="{FILL2 if hid else (FILL3 if isp else FILL)}" stroke="{NAVY}" stroke-width="3"/>' + T(cx, cy + 7, "?" if hid else str(val), 19)
    return wrap(w, h + 30, edges + circ, "Árbol de factores primos"), nodes


def frac_bars(items, w=560):
    """items: [(rótulo, num, den)] barras divididas en den partes con num sombreadas."""
    body = ""
    h = 30 + 62 * len(items)
    for i, (lab, num, den) in enumerate(items):
        y = 20 + 62 * i
        bw = 360
        cw = bw / den
        body += tag(50, y + 24, lab, 17)
        for j in range(den):
            body += R(110 + j * cw, y, cw, 48, FILL3 if j < num else WHITE, NAVY, 2.5)
    return wrap(w, h, body, "Barras divididas en partes iguales")


def frac_pie(num, den, w=560, r=95, lab=None):
    import math
    cx, cy = 280, 20 + r + 6
    body = ""
    for j in range(den):
        a0 = -math.pi / 2 + 2 * math.pi * j / den
        a1 = -math.pi / 2 + 2 * math.pi * (j + 1) / den
        x0_, y0_ = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1_, y1_ = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if a1 - a0 > math.pi else 0
        d = f"M {cx} {cy} L {x0_:.1f} {y0_:.1f} A {r} {r} 0 {large} 1 {x1_:.1f} {y1_:.1f} Z"
        body += f'<path d="{d}" fill="{FILL3 if j < num else WHITE}" stroke="{NAVY}" stroke-width="2.5"/>'
    if lab:
        body += tag(cx + r + 90, cy, lab, 17)
    return wrap(w, 2 * r + 44, body, "Círculo dividido en partes iguales")


def grid_shaded(rows, cols, shaded, w=560, cell=36):
    """Cuadrícula rows x cols con `shaded` celdas sombreadas (por filas)."""
    x0 = (w - cols * cell) / 2
    body = ""
    for i in range(rows):
        for j in range(cols):
            body += R(x0 + j * cell, 16 + i * cell, cell, cell, FILL3 if i * cols + j < shaded else WHITE, NAVY, 2)
    return wrap(w, rows * cell + 32, body, "Cuadrícula con celdas sombreadas")


PIE_COLS = ["#93C5FD", "#FDE68A", "#BBF7D0", "#FBCFE8", "#DDD6FE", "#FED7AA"]


def pie_chart(parts, w=560, r=105):
    """parts: [(rótulo, valor_texto, valor_numérico)]; sectores con píldoras de rótulo."""
    import math
    cx, cy = 280, 20 + r + 8
    total = sum(p[2] for p in parts)
    a = -math.pi / 2
    body = ""
    tags = ""
    for i, (lab, txt, v) in enumerate(parts):
        da = 2 * math.pi * v / total
        a0, a1 = a, a + da
        x0_, y0_ = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1_, y1_ = cx + r * math.cos(a1), cy + r * math.sin(a1)
        large = 1 if da > math.pi else 0
        body += f'<path d="M {cx} {cy} L {x0_:.1f} {y0_:.1f} A {r} {r} 0 {large} 1 {x1_:.1f} {y1_:.1f} Z" fill="{PIE_COLS[i % 6]}" stroke="{NAVY}" stroke-width="2.5"/>'
        am = (a0 + a1) / 2
        rr = r * (0.62 if v / total > 0.12 else 0.74)
        tags += tag(cx + rr * math.cos(am), cy + rr * math.sin(am), f"{lab} {txt}".strip(), 14)
        a = a1
    return wrap(w, 2 * r + 44, body + tags, "Gráfico circular")


def hbars_pct(items, w=560, top=100):
    """Barras horizontales: items [(rótulo, valor)], escala 0..top."""
    body = ""
    h = 24 + 52 * len(items)
    for i, (lab, v) in enumerate(items):
        y = 16 + 52 * i
        body += T(120, y + 30, lab, 16, "end") + R(130, y, 380 * v / top, 40, FILL3) + tag(130 + 380 * v / top + 30, y + 20, f"{v}%", 15)
    body += L(130, 10, 130, h - 10, INK, 2.5)
    return wrap(w, h, body, "Barras horizontales con porcentajes")


def interval_line(lo, hi, a=None, b=None, a_closed=True, b_closed=True, w=560, step=1):
    """Recta numérica lo..hi con el intervalo sombreado entre a y b (None = infinito) y extremos abiertos/cerrados."""
    x0, x1, y = 40, w - 40, 110
    X = lambda v: x0 + float((v - lo) / (hi - lo)) * (x1 - x0)
    body = ""
    sa = x0 - 14 if a is None else X(a)
    sb = x1 + 14 if b is None else X(b)
    body += R(sa, y - 9, sb - sa, 18, "#93C5FD", "#93C5FD", 1)
    body += L(x0 - 14, y, x1 + 14, y, INK, 3.5)
    body += P([(x1 + 22, y), (x1 + 8, y - 7), (x1 + 8, y + 7)], INK, INK, 1) + P([(x0 - 22, y), (x0 - 8, y - 7), (x0 - 8, y + 7)], INK, INK, 1)
    v = lo
    while v <= hi + 1e-9:
        body += L(X(v), y - 8, X(v), y + 8, INK, 2.5 if v == 0 else 2) + T(X(v), y + 34, z_(v), 15)
        v += step
    for val, closed in ((a, a_closed), (b, b_closed)):
        if val is not None:
            body += C(X(val), y, 9, INK if closed else WHITE, INK, 3)
    return wrap(w, 170, body, "Recta numérica con un intervalo sombreado")


def arrow_diagram(A, B, pairs, w=560):
    """Diagrama sagital: conjuntos A y B (listas) y flechas (a, b) entre ellos."""
    n = max(len(A), len(B))
    h = 40 + 46 * n + 30
    ya = lambda i, m: 60 + (h - 100) * (i + 0.5) / m
    body = f'<ellipse cx="170" cy="{h / 2:.0f}" rx="80" ry="{h / 2 - 20:.0f}" fill="#F1F5F9" stroke="{NAVY}" stroke-width="3"/>'
    body += f'<ellipse cx="390" cy="{h / 2:.0f}" rx="80" ry="{h / 2 - 20:.0f}" fill="#FEF3C7" stroke="{NAVY}" stroke-width="3"/>'
    body += tag(170, 20, "Conjunto A", 15) + tag(390, 20, "Conjunto B", 15)
    posA = {a: (170, ya(i, len(A))) for i, a in enumerate(A)}
    posB = {b: (390, ya(i, len(B))) for i, b in enumerate(B)}
    for a, b in pairs:
        (x1, y1), (x2, y2) = posA[a], posB[b]
        body += L(x1 + 26, y1, x2 - 30, y2, ACC, 3) + P([(x2 - 26, y2), (x2 - 42, y2 - 7 + (y1 - y2) * 0.05), (x2 - 42, y2 + 7 + (y1 - y2) * 0.05)], ACC, ACC, 1)
    for a, (x, y) in posA.items():
        body += C(x, y, 22, WHITE, NAVY, 2.5) + T(x, y + 6, z_(a) if not isinstance(a, str) else a, 17)
    for b, (x, y) in posB.items():
        body += C(x, y, 22, WHITE, NAVY, 2.5) + T(x, y + 6, z_(b) if not isinstance(b, str) else b, 17)
    return wrap(w, h + 10, body, "Diagrama sagital de una relación")


# ---------------------------------------------------------------- geometría M1
POS_OFF = {"NW": (-48, -20), "NE": (48, -20), "SW": (-48, 22), "SE": (48, 22)}
REL = {}
for _u in ("NW", "NE", "SW", "SE"):
    REL[("U", _u, "U", _u)] = None
_PAIRS = {}
# relaciones entre (recta, cuadrante): sup=recta superior 'U', inferior 'D'
def _rel(l1, q1, l2, q2):
    if l1 == l2:
        opp = {("NW", "SE"), ("SE", "NW"), ("NE", "SW"), ("SW", "NE")}
        return "vertical" if (q1, q2) in opp else "adyacentes"
    if l1 == "D":
        l1, q1, l2, q2 = l2, q2, l1, q1
    if q1 == q2:
        return "correspondientes"
    if (q1, q2) in {("SE", "NW"), ("SW", "NE")}:
        return "alternos internos"
    if (q1, q2) in {("NW", "SE"), ("NE", "SW")}:
        return "alternos externos"
    if (q1, q2) in {("SE", "NE"), ("SW", "NW")}:
        return "conjugados internos"
    return "conjugados externos"


def par_transversal(labels, w=560):
    """Dos paralelas cortadas por una transversal. labels: {(recta 'U'/'D', 'NW'|'NE'|'SW'|'SE'): texto}."""
    yU, yD = 80, 180
    x0 = 250
    xu, xd = x0 + 0.45 * (yU - 30), x0 + 0.45 * (yD - 30)
    body = L(50, yU, 510, yU, NAVY, 3.5) + L(50, yD, 510, yD, NAVY, 3.5) + L(x0, 30, x0 + 0.45 * 200, 230, INK, 3.5)
    body += C(xu, yU, 5, INK, INK, 1) + C(xd, yD, 5, INK, INK, 1)
    for (ln, q), txt in labels.items():
        x, y = (xu, yU) if ln == "U" else (xd, yD)
        dx, dy = POS_OFF[q]
        body += tag(x + dx, y + dy, txt, 16)
    body += tag(470, yU - 20, "L₁", 15) + tag(470, yD - 20, "L₂", 15)
    return wrap(w, 260, body, "Dos rectas paralelas cortadas por una transversal")


def tri_angles(labs, ext=None, w=560, names=("A", "B", "C")):
    """Triángulo con tags en los ángulos: labs = {'A':..,'B':..,'C':..}; ext = texto del ángulo exterior en B."""
    A, B, C_ = (100, 220), (400, 220), (250, 50)
    body = P([A, B, C_], FILL)
    if ext:
        body += L(B[0], B[1], B[0] + 110, B[1], INK, 3.5)
        body += tag(B[0] + 52, B[1] - 28, ext, 16)
    body += tag(A[0] + 52, A[1] - 22, labs.get("A", ""), 16) if labs.get("A") else ""
    body += tag(B[0] - 52, B[1] - 22, labs.get("B", ""), 16) if labs.get("B") else ""
    body += tag(C_[0], C_[1] + 42, labs.get("C", ""), 16) if labs.get("C") else ""
    for P_, nm, dx, dy in ((A, names[0], -16, 8), (B, names[1], 16, 8), (C_, names[2], 0, -16)):
        body += C(P_[0], P_[1], 5, INK, INK, 1) + T(P_[0] + dx, P_[1] + dy + 6, nm, 20)
    return wrap(w, 270, body, "Triángulo con sus ángulos")


def tri_sides(a, b, c, labs=None, names=("A", "B", "C"), right=None, w=560):
    """Triángulo con lados a=BC, b=CA, c=AB (a partir de las medidas) y rótulos en los lados. right: vértice con ángulo recto ('A'/'B'/'C')."""
    import math
    x = (b * b + c * c - a * a) / (2 * c)
    y2 = b * b - x * x
    if y2 <= 0:
        raise ValueError("triángulo degenerado")
    y = math.sqrt(y2)
    s = min(400 / max(c, abs(x), c - x), 170 / y)
    lo_, hi_ = min(0, x) * s, max(c, x) * s
    A = ((w - (hi_ - lo_)) / 2 - lo_, 215)
    B = (A[0] + c * s, 215)
    Cc = (A[0] + x * s, 215 - y * s)
    body = P([A, B, Cc], FILL)
    labs = labs or {}
    mid_ = lambda p, q: ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)
    if labs.get("c"):
        m = mid_(A, B); body += tag(m[0], m[1] + 26, labs["c"], 16)
    if labs.get("a"):
        m = mid_(B, Cc); body += tag(m[0] + 28, m[1] - 4, labs["a"], 16)
    if labs.get("b"):
        m = mid_(A, Cc); body += tag(m[0] - 28, m[1] - 4, labs["b"], 16)
    if right:
        P_ = {"A": A, "B": B, "C": Cc}[right]
        o1 = {"A": B, "B": A, "C": A}[right]; o2 = {"A": Cc, "B": Cc, "C": B}[right]
        def unit(p, q):
            d = math.hypot(q[0] - p[0], q[1] - p[1]); return ((q[0] - p[0]) / d * 16, (q[1] - p[1]) / d * 16)
        e1, e2 = unit(P_, o1), unit(P_, o2)
        body += f'<polyline fill="none" stroke="{INK}" stroke-width="2.5" points="{P_[0] + e1[0]:.1f},{P_[1] + e1[1]:.1f} {P_[0] + e1[0] + e2[0]:.1f},{P_[1] + e1[1] + e2[1]:.1f} {P_[0] + e2[0]:.1f},{P_[1] + e2[1]:.1f}"/>'
    for P_, nm, dx, dy in ((A, names[0], -16, 8), (B, names[1], 16, 8), (Cc, names[2], 0, -16)):
        body += C(P_[0], P_[1], 5, INK, INK, 1) + T(P_[0] + dx, P_[1] + dy + 6, nm, 20)
    return wrap(w, 270, body, "Triángulo con las medidas de sus lados")


def polygon_fig(pts, labels=None, fill=None, w=560, h=280, unit_scale=None):
    """Polígono con vértices en unidades; labels: lista de texto por lado (None = sin rótulo)."""
    import math
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    s = unit_scale or min(400 / (max(xs) - min(xs)), (h - 100) / (max(ys) - min(ys)))
    ox = (w - (max(xs) - min(xs)) * s) / 2 - min(xs) * s
    oy = 50 + max(ys) * s
    P_ = [(ox + x * s, oy - y * s) for x, y in pts]
    body = P(P_, fill or FILL)
    n = len(P_)
    area2 = sum(P_[i][0] * P_[(i + 1) % n][1] - P_[(i + 1) % n][0] * P_[i][1] for i in range(n))
    sign = 1 if area2 > 0 else -1
    for i in range(n):
        if labels and labels[i]:
            p, q = P_[i], P_[(i + 1) % n]
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            dx, dy = q[0] - p[0], q[1] - p[1]
            d = math.hypot(dx, dy) or 1
            nx, ny = sign * dy / d, -sign * dx / d
            body += tag(mx + nx * 26, my + ny * 20, labels[i], 16)
    for (px, py) in P_:
        body += C(px, py, 4, INK, INK, 1)
    return wrap(w, h + 30, body, "Figura plana con las medidas de sus lados")


def cylinder_fig(r_lab, h_lab, w=560, hollow=False, fill_frac=None):
    """Cilindro con radio y altura rotulados; fill_frac (0-1) sombrea el nivel de líquido."""
    cx, top, hgt, rx, ry = 280, 60, 130, 80, 22
    body = ""
    if fill_frac is not None:
        ly = top + hgt * (1 - fill_frac)
        body += f'<path d="M {cx - rx} {ly} L {cx - rx} {top + hgt} A {rx} {ry} 0 0 0 {cx + rx} {top + hgt} L {cx + rx} {ly} A {rx} {ry} 0 0 1 {cx - rx} {ly} Z" fill="#93C5FD" stroke="none"/>'
    body += f'<path d="M {cx - rx} {top} L {cx - rx} {top + hgt} A {rx} {ry} 0 0 0 {cx + rx} {top + hgt} L {cx + rx} {top}" fill="{FILL if fill_frac is None else "none"}" stroke="{NAVY}" stroke-width="4"/>'
    body += f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="{FILL2 if fill_frac is None else "#F8FAFC"}" stroke="{NAVY}" stroke-width="4"/>'
    if r_lab:
        body += L(cx, top, cx + rx, top, ACC, 3.5) + C(cx, top, 4, INK, INK, 1) + tag(cx + rx / 2, top - 22, r_lab, 15)
    if h_lab:
        body += L(cx + rx + 26, top, cx + rx + 26, top + hgt, INK, 2.5) + tag(cx + rx + 26 + 44, top + hgt / 2, h_lab, 15)
    return wrap(w, 250, body, "Cilindro con su radio y su altura")
