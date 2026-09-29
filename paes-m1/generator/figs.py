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
