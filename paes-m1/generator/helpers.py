"""Utilidades compartidas para las plantillas de preguntas (Plot, card, make, pick4, fs...)."""
from fractions import Fraction as F
from functools import reduce
from math import gcd, log, log10
from svgkit import *
from common import Reject, make as _make


def make(stem, svg, correct, dists, skill, expl):
    m = lambda t: t.replace('-', '−')
    return _make(m(stem), m(svg) if False else svg, m(correct), [m(d) for d in dists], skill, m(expl))

Q_RES, Q_MOD, Q_REP, Q_ARG = ("Resolver problemas", "Modelar", "Representar", "Argumentar")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def lg(b):
    return "log" + str(b).translate(SUB)


def dec(x):
    return f"{x:.2f}".replace(".", ",")


def fs(x):
    x = F(x)
    return (str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}").replace("-", "−")


def pick4(correct, cands):
    out = []
    for c in cands:
        if c != correct and c not in out:
            out.append(c)
        if len(out) == 4:
            return out
    raise Reject


def lc(terms):
    """Combinación lineal de símbolos ('a','b','' = constante)."""
    terms = [(F(c), s) for c, s in terms if c != 0]
    if not terms:
        return "0"
    d = reduce(lambda x, y: x * y // gcd(x, y), [c.denominator for c, _ in terms])
    nums = [int(c * d) for c, _ in terms]
    g = reduce(gcd, [abs(x) for x in nums] + [d])
    nums = [x // g for x in nums]
    d //= g
    out = []
    for i, (x, (_, s)) in enumerate(zip(nums, terms)):
        core = (str(abs(x)) if (abs(x) != 1 or s == "") else "") + s
        out.append(("−" if x < 0 else "") + core if i == 0 else (" − " if x < 0 else " + ") + core)
    body = "".join(out)
    return body if d == 1 else (f"{body}/{d}" if len(terms) == 1 else f"({body})/{d}")


# ---------------------------------------------------------------- figuras
class Plot:
    def __init__(s, w, h, x0, x1, y0, y1, ml=44, mb=30, mt=14, mr=14):
        s.w, s.h, s.x0, s.x1, s.y0, s.y1, s.ml, s.mb, s.mt, s.mr = w, h, x0, x1, y0, y1, ml, mb, mt, mr
        s.parts = []

    def X(s, x): return s.ml + (x - s.x0) / (s.x1 - s.x0) * (s.w - s.ml - s.mr)
    def Y(s, y): return s.h - s.mb - (y - s.y0) / (s.y1 - s.y0) * (s.h - s.mb - s.mt)

    def axes(s, sx, sy):
        g = ""
        x = int(s.x0 // sx * sx)
        while x <= s.x1 + 1e-9:
            if x >= s.x0:
                g += L(s.X(x), s.Y(s.y0), s.X(x), s.Y(s.y1), "#CBD5E1", 1) + T(s.X(x), s.h - 8, fs(x), 14)
            x += sx
        y = int(s.y0 // sy * sy)
        while y <= s.y1 + 1e-9:
            if y >= s.y0:
                g += L(s.X(s.x0), s.Y(y), s.X(s.x1), s.Y(y), "#CBD5E1", 1) + T(s.ml - 8, s.Y(y) + 5, fs(y), 14, "end")
            y += sy
        g += L(s.X(s.x0), s.Y(0), s.X(s.x1), s.Y(0), INK, 2.5) + L(s.X(0), s.Y(s.y0), s.X(0), s.Y(s.y1), INK, 2.5)
        s.parts.append(g)

    def curve(s, f, xa, xb, color=ACC, sw=4, n=300):
        segs, cur = [], []
        for i in range(n + 1):
            x = xa + (xb - xa) * i / n
            try:
                y = f(x)
            except (ValueError, ZeroDivisionError, OverflowError):
                y = None
            if y is not None and s.y0 <= y <= s.y1:
                cur.append((s.X(x), s.Y(y)))
            elif cur:
                segs.append(cur); cur = []
        if cur: segs.append(cur)
        for sg in segs:
            if len(sg) > 1:
                s.parts.append('<polyline fill="none" stroke="%s" stroke-width="%s" points="%s"/>' % (color, sw, " ".join(f"{a:.1f},{b:.1f}" for a, b in sg)))

    def pt(s, x, y, label=None, dx=0, dy=-26):
        s.parts.append(C(s.X(x), s.Y(y), 7, ACC))
        if label: s.parts.append(tag(s.X(x) + dx, s.Y(y) + dy, label.replace("-", "−"), 16))

    def vline(s, x, dash="8 6"): s.parts.append(L(s.X(x), s.Y(s.y0), s.X(x), s.Y(s.y1), NAVY, 2.5, dash))
    def hline(s, y, dash="8 6"): s.parts.append(L(s.X(s.x0), s.Y(y), s.X(s.x1), s.Y(y), NAVY, 2.5, dash))
    def svg(s, label): return wrap(s.w, s.h, "".join(s.parts), label)


def pow_strip(b, cells, final):
    """Cajas con las primeras potencias y una última caja con la incógnita."""
    n = len(cells) + 1
    w = 96
    gap = (520 - n * w) / (n - 1)
    body = ""
    for i, c in enumerate(cells + [final]):
        x = 20 + i * (w + gap)
        last = i == n - 1
        body += R(x, 60, w, 70, FILL2 if last else FILL) + T(x + w / 2, 102, c, 19 if len(c) < 7 else 15)
        if i:
            body += L(x - gap + 2, 95, x - 2, 95, ACC, 3)
    return wrap(560, 190, body + tag(280, 30, f"Cada paso multiplica por {b}", 16), "Sucesión de potencias")


def card(lines, h=200, size=22):
    body = R(30, 25, 500, h - 50, "#F1F5F9")
    n = len(lines)
    for i, t in enumerate(lines):
        body += T(280, 25 + (h - 50) * (i + 1) / (n + 1) + 7, t, size)
    return wrap(560, h, body, " ".join(lines))


def z(n):
    """Entero (o Fraction) como texto con signo menos tipográfico."""
    return fs(n)


def par(n):
    """Entero entre paréntesis si es negativo."""
    return f"({fs(n)})" if n < 0 else fs(n)


def sgn_term(n, first=False):
    """Término con su signo para sumas: ' + 5', ' − 3' (o sin espacio inicial si first)."""
    s = fs(abs(n))
    if first:
        return ("−" if n < 0 else "") + s
    return (" − " if n < 0 else " + ") + s
