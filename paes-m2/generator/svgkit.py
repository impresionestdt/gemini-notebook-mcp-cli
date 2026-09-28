"""Utilidades SVG con paleta de alto contraste (texto siempre oscuro sobre fondo claro)."""
INK = "#0F172A"      # texto
NAVY = "#0B3D6E"     # trazos
FILL = "#DBEAFE"
FILL2 = "#FEF3C7"
FILL3 = "#93C5FD"
ACC = "#9A3412"      # acento (puntos, resaltes)
WHITE = "#FFFFFF"

TEXT_ON = [(INK, WHITE), (INK, FILL), (INK, FILL2), (INK, FILL3), (INK, "#E0F2FE"),
           (INK, "#BAE6FD"), (INK, "#7DD3FC"), (INK, "#F1F5F9")]


def lum(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def wrap(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img" '
            f'aria-label="{esc(label)}"><rect width="{w}" height="{h}" fill="{WHITE}"/>{body}</svg>')


def T(x, y, s, size=18, anchor="middle", fill=INK, weight=700):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="{fill}" font-family="Arial,Helvetica,sans-serif">{esc(s)}</text>')


def tag(cx, cy, s, size=18):
    """Etiqueta con píldora blanca: el texto nunca queda sobre un trazo."""
    w = len(s) * size * 0.62 + 16
    h = size + 12
    return (f'<rect x="{cx - w / 2:.1f}" y="{cy - h / 2:.1f}" width="{w:.1f}" height="{h}" rx="8" '
            f'fill="{WHITE}" stroke="{NAVY}" stroke-width="1.5"/>' + T(cx, cy + size * 0.35, s, size))


def R(x, y, w, h, fill=FILL, stroke=NAVY, sw=3):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def L(x1, y1, x2, y2, stroke=NAVY, sw=3, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{d}/>'


def P(pts, fill=FILL, stroke=NAVY, sw=3):
    p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def C(x, y, r, fill=ACC, stroke=INK, sw=2):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def ELL(cx, cy, rx, ry, fill, stroke=NAVY, sw=3):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
