"""Figuras para conteo y probabilidad: casillas, árboles, rutas, tablas y urnas."""
from svgkit import *


def slots_fig(items, title=None, ops="×"):
    """items: lista de (rótulo, cantidad|'?'). Casillas con cantidad de opciones por etapa."""
    n = len(items)
    w = min(120, (500 - 36 * (n - 1)) / n)
    total = n * w + 36 * (n - 1)
    x0 = (560 - total) / 2
    body = ""
    for i, (lab, cnt) in enumerate(items):
        x = x0 + i * (w + 36)
        body += R(x, 90, w, 70, FILL2 if str(cnt) == "?" else FILL) + T(x + w / 2, 135, str(cnt), 30) + tag(x + w / 2, 62, lab, 15)
        if i:
            body += T(x - 18, 135, ops, 28)
    if title:
        body += tag(280, 26, title, 16)
    return wrap(560, 200, body, "Casillas con la cantidad de opciones de cada etapa")


def tree_fig(children, l1="Etapa 1", l2="Etapa 2", names1=None, names2=None):
    """children: cantidad de ramas de cada nodo del primer nivel."""
    L_ = sum(children)
    dy = min(30, 220 / max(L_, 1))
    top = 140 - dy * (L_ - 1) / 2
    body = tag(120, 22, l1, 15) + tag(400, 22, l2, 15)
    root = (40, 140)
    y = top
    leaf_i = 0
    for i, ch in enumerate(children):
        ys = [top + dy * (leaf_i + j) for j in range(ch)]
        leaf_i += ch
        my = sum(ys) / len(ys)
        body += L(root[0], root[1], 210, my, NAVY, 2.5)
        for yy in ys:
            body += L(210, my, 420, yy, NAVY, 2.5) + C(420, yy, 6, ACC, INK, 1.5)
        body += C(210, my, 8, FILL3, INK, 2) + (T(196, my - 12, names1[i], 15, "end") if names1 else "")
    body += C(root[0], root[1], 9, WHITE, INK, 2.5)
    return wrap(560, 280, body, "Diagrama de árbol")


def roads_fig(n_ab, n_bc, n_ac=0, names=("A", "B", "C")):
    """Rutas: n_ab caminos A→B, n_bc caminos B→C y n_ac caminos directos A→C (arcos superiores)."""
    A, B, C_ = (70, 170), (280, 170), (490, 170)
    body = ""

    def arcs(P1, P2, n, up=False, base=0):
        out = ""
        for k in range(n):
            off = (k - (n - 1) / 2) * 26 if not up else -(70 + 34 * k)
            cx = (P1[0] + P2[0]) / 2
            cy = P1[1] + off * (1 if not up else 1) * 2 - (0 if not up else 0)
            if not up:
                cy = P1[1] + (k - (n - 1) / 2) * 44
            out += f'<path d="M {P1[0]} {P1[1]} Q {cx} {cy} {P2[0]} {P2[1]}" fill="none" stroke="{NAVY}" stroke-width="3"/>'
        return out

    body += arcs(A, B, n_ab) + arcs(B, C_, n_bc)
    if n_ac:
        for k in range(n_ac):
            cy = 170 - (110 + 40 * k)
            body += f'<path d="M {A[0]} {A[1]} Q 280 {cy} {C_[0]} {C_[1]}" fill="none" stroke="{ACC}" stroke-width="3"/>'
    for P_, nm in ((A, names[0]), (B, names[1]), (C_, names[2])):
        body += C(P_[0], P_[1], 22, FILL2, INK, 3) + T(P_[0], P_[1] + 7, nm, 20)
    return wrap(560, 260, body, "Rutas entre tres ciudades")


def table_fig(headers, rows):
    n = len(headers)
    w = 500 / n
    h = 42
    body = R(30, 30, 500, h, "#E0F2FE") + "".join(T(30 + w * (j + 0.5), 30 + h * 0.65, t, 17) for j, t in enumerate(headers))
    for i, row in enumerate(rows):
        body += R(30, 30 + h * (i + 1), 500, h, WHITE)
        for j, t in enumerate(row):
            body += T(30 + w * (j + 0.5), 30 + h * (i + 1) + h * 0.65, str(t), 17)
    for j in range(n + 1):
        body += L(30 + w * j, 30, 30 + w * j, 30 + h * (len(rows) + 1), NAVY, 2)
    for i in range(len(rows) + 2):
        body += L(30, 30 + h * i, 530, 30 + h * i, NAVY, 1.5)
    return wrap(560, 60 + h * (len(rows) + 1), body, "Tabla")


COLMAP = {"rojas": "#FCA5A5", "azules": "#93C5FD", "verdes": "#86EFAC", "amarillas": "#FDE68A", "negras": "#94A3B8", "blancas": "#FFFFFF", "naranjas": "#FDBA74", "moradas": "#DDD6FE"}


def urn_fig(counts, title=None, per_row=6):
    """Bolitas de colores en una urna: counts = [(nombre, n), ...] (nombre en COLMAP)."""
    body = f'<path d="M 120 50 L 120 200 Q 120 240 160 240 L 400 240 Q 440 240 440 200 L 440 50" fill="#F8FAFC" stroke="{NAVY}" stroke-width="4"/>'
    i = 0
    for nm, n in counts:
        col = COLMAP.get(nm, "#E5E7EB")
        for _ in range(n):
            r_, c_ = divmod(i, per_row)
            body += C(155 + c_ * 45, 212 - r_ * 38, 16, col, INK, 2)
            i += 1
    for k, (nm, n) in enumerate(counts):
        y = 70 + 40 * k
        body += C(478, y, 10, COLMAP.get(nm, "#E5E7EB"), INK, 2) + T(494, y + 5, f"{nm}: {n}", 15, "start")
    if title: body += tag(280, 20, title, 15)
    return wrap(560, 265, body, "Urna con bolitas de colores")
