"""Figuras estadísticas: barras, histograma, polígono, caja y bigotes."""
from svgkit import *
from helpers import fs


def _axis(ymax, step, ml, mt, ph, w, mr=16):
    g = ""
    y = 0
    while y <= ymax + 1e-9:
        py = mt + ph - ph * y / ymax
        g += L(ml, py, w - mr, py, "#CBD5E1", 1) + T(ml - 8, py + 5, fs(y), 14, "end")
        y += step
    return g


def bar_chart(labels, vals, ymax, step, w=560, h=300, show=True, hl=None, ylab="", colors=None):
    ml, mb, mt, mr = 52, 46, 26, 16
    ph, pw = h - mb - mt, w - ml - mr
    n = len(vals)
    g = _axis(ymax, step, ml, mt, ph, w)
    bw = pw / n * 0.6
    for i, (lb, v) in enumerate(zip(labels, vals)):
        cx = ml + pw * (i + 0.5) / n
        top = mt + ph - ph * v / ymax
        fill = FILL2 if hl is not None and i == hl else FILL3
        g += R(cx - bw / 2, top, bw, mt + ph - top, fill, NAVY, 3)
        if show:
            g += tag(cx, top - 14, fs(v), 14)
        g += T(cx, h - 22, lb, 14 if len(lb) < 9 else 12)
    g += L(ml, mt, ml, mt + ph, INK, 2.5) + L(ml, mt + ph, w - mr, mt + ph, INK, 2.5)
    if ylab:
        g += T(ml + 4, 14, ylab, 13, "start")
    return wrap(w, h, g, "Gráfico de barras")


def hist(edges, vals, ymax, step, w=560, h=300, show=True, ylab=""):
    ml, mb, mt, mr = 52, 46, 26, 20
    ph, pw = h - mb - mt, w - ml - mr
    n = len(vals)
    g = _axis(ymax, step, ml, mt, ph, w, mr)
    bw = pw / n
    for i, v in enumerate(vals):
        x = ml + bw * i
        top = mt + ph - ph * v / ymax
        g += R(x, top, bw, mt + ph - top, FILL3, NAVY, 3)
        if show:
            g += tag(x + bw / 2, top - 14, fs(v), 14)
    for i, e in enumerate(edges):
        g += T(ml + bw * i, h - 22, fs(e), 14)
    g += L(ml, mt, ml, mt + ph, INK, 2.5) + L(ml, mt + ph, w - mr, mt + ph, INK, 2.5)
    if ylab:
        g += T(ml + 4, 14, ylab, 13, "start")
    return wrap(w, h, g, "Histograma")


def line_chart(labels, vals, ymax, step, w=560, h=300, show=True, ylab=""):
    ml, mb, mt, mr = 52, 46, 26, 20
    ph, pw = h - mb - mt, w - ml - mr
    n = len(vals)
    g = _axis(ymax, step, ml, mt, ph, w, mr)
    pts = [(ml + pw * (i + 0.5) / n, mt + ph - ph * v / ymax) for i, v in enumerate(vals)]
    g += '<polyline fill="none" stroke="%s" stroke-width="4" points="%s"/>' % (NAVY, " ".join(f"{a:.1f},{b:.1f}" for a, b in pts))
    for (x, y), lb, v in zip(pts, labels, vals):
        g += C(x, y, 6, ACC) + T(x, h - 22, lb, 14)
        if show:
            g += tag(x, y - 18, fs(v), 14)
    g += L(ml, mt, ml, mt + ph, INK, 2.5) + L(ml, mt + ph, w - mr, mt + ph, INK, 2.5)
    if ylab:
        g += T(ml + 4, 14, ylab, 13, "start")
    return wrap(w, h, g, "Gráfico de líneas")


def boxplot(five, lo, hi, step, w=560, show=False, unit=""):
    mn, q1, md, q3, mx = five
    ml, mr = 40, 30
    X = lambda v: ml + (w - ml - mr) * (v - lo) / (hi - lo)
    y0, hh = 70, 70
    g = ""
    v = lo
    while v <= hi + 1e-9:
        g += L(X(v), 30, X(v), 175, "#CBD5E1", 1) + T(X(v), 198, fs(v), 14)
        v += step
    g += L(X(lo), 170, X(hi), 170, INK, 2.5)
    g += L(X(mn), y0 + hh / 2, X(q1), y0 + hh / 2, NAVY, 3) + L(X(q3), y0 + hh / 2, X(mx), y0 + hh / 2, NAVY, 3)
    g += L(X(mn), y0 + 15, X(mn), y0 + hh - 15, NAVY, 3) + L(X(mx), y0 + 15, X(mx), y0 + hh - 15, NAVY, 3)
    g += R(X(q1), y0, X(q3) - X(q1), hh, FILL2, NAVY, 3) + L(X(md), y0, X(md), y0 + hh, ACC, 5)
    if show:
        for val, dy in ((mn, 0), (q1, 0), (md, 0), (q3, 0), (mx, 0)):
            g += tag(X(val), 46 if val != md else 18, fs(val), 13)
    return wrap(w, 215, g, "Diagrama de caja y bigotes")


def spinner(items, w=560, r=105):
    """Ruleta con sectores iguales: items = [(rótulo, relleno)]."""
    import math
    cx, cy = 280, r + 30
    n = len(items)
    g = ""
    for i, (lab, fill) in enumerate(items):
        a0 = -math.pi / 2 + 2 * math.pi * i / n
        a1 = -math.pi / 2 + 2 * math.pi * (i + 1) / n
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        g += f'<path d="M {cx} {cy} L {x0:.1f} {y0:.1f} A {r} {r} 0 0 1 {x1:.1f} {y1:.1f} Z" fill="{fill}" stroke="{NAVY}" stroke-width="3"/>'
    for i, (lab, fill) in enumerate(items):
        am = -math.pi / 2 + 2 * math.pi * (i + 0.5) / n
        g += T(cx + r * 0.66 * math.cos(am), cy + r * 0.66 * math.sin(am) + 6, lab, 18)
    g += f'<polygon points="{cx},{cy - r - 4} {cx - 10},{cy - r - 24} {cx + 10},{cy - r - 24}" fill="{ACC}" stroke="{INK}" stroke-width="2"/>' + C(cx, cy, 7, INK)
    return wrap(w, 2 * r + 50, g, "Ruleta con sectores iguales")


def venn(a_only, both, b_only, out, names=("A", "B"), w=560, hl=None):
    """Diagrama de Venn con recuentos. hl: región resaltada 'A','B','AB','union' o None (solo sombrea el contorno)."""
    g = R(40, 16, 480, 200, WHITE, NAVY, 3)
    g += f'<circle cx="220" cy="116" r="78" fill="{FILL}" fill-opacity="0.85" stroke="{NAVY}" stroke-width="3"/>'
    g += f'<circle cx="340" cy="116" r="78" fill="{FILL2}" fill-opacity="0.75" stroke="{NAVY}" stroke-width="3"/>'
    g += T(160, 30, names[0], 18) if False else tag(150, 40, names[0], 16) + tag(410, 40, names[1], 16)
    g += T(175, 124, str(a_only), 22) + T(280, 124, str(both), 22) + T(385, 124, str(b_only), 22) + T(485, 200, str(out), 20)
    return wrap(w, 235, g, "Diagrama de Venn")
