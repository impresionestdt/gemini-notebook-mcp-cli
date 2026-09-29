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
    body = f'<path d="M 50 50 L 50 200 Q 50 240 90 240 L 330 240 Q 370 240 370 200 L 370 50" fill="#F8FAFC" stroke="{NAVY}" stroke-width="4"/>'
    i = 0
    for nm, n in counts:
        col = COLMAP.get(nm, "#E5E7EB")
        for _ in range(n):
            r_, c_ = divmod(i, per_row)
            body += C(85 + c_ * 45, 212 - r_ * 38, 16, col, INK, 2)
            i += 1
    for k, (nm, n) in enumerate(counts):
        y = 70 + 40 * k
        body += C(408, y, 10, COLMAP.get(nm, "#E5E7EB"), INK, 2) + T(424, y + 5, f"{nm}: {n}", 15, "start")
    if title: body += tag(210, 20, title, 15)
    return wrap(560, 265, body, "Urna con bolitas de colores")


def pick_fig(n, chosen, ordered, names=None):
    """Fila de n elementos; los elegidos se resaltan. ordered=True numera la elección (orden importa)."""
    names = names or [chr(65 + i) for i in range(n)]
    w = min(60, 500 / n)
    x0 = (560 - w * n) / 2
    body = ""
    for i in range(n):
        x = x0 + i * w + w / 2
        sel = i in chosen
        body += C(x, 110, w * 0.36, FILL3 if sel else WHITE, ACC if sel else NAVY, 4 if sel else 2.5) + T(x, 116, names[i], 18)
        if sel and ordered:
            body += tag(x, 62, str(chosen.index(i) + 1), 15)
    cap = "El orden de elección importa (1.º, 2.º, …)" if ordered else "Solo importa qué elementos se eligen"
    body += tag(280, 175, cap, 15)
    return wrap(560, 205, body, "Elementos y elección")


def pascal_fig(rows, hide=None, hl=()):
    """Triángulo de Pascal con filas 0..rows-1. hide=(fila, col) muestra '?'; hl: celdas resaltadas."""
    from math import comb
    body = ""
    dy = min(38, 240 / rows)
    w = min(50, 520 / rows)
    for n in range(rows):
        for k in range(n + 1):
            x = 280 + (k - n / 2) * w
            y = 30 + n * dy
            txt = "?" if hide == (n, k) else str(comb(n, k))
            fill = FILL2 if (hide == (n, k)) else (FILL3 if (n, k) in hl else FILL)
            body += R(x - w * 0.42, y - dy * 0.42, w * 0.84, dy * 0.84, fill, NAVY, 1.5) + T(x, y + 6, txt, 14 if len(txt) > 2 else 16)
    return wrap(560, 50 + rows * dy, body, "Triángulo de Pascal")


def two_way_fig(rlabs, clabs, cells, hl_num=(), hl_den_col=None, hl_den_row=None, hide=None, show_totals=True, corner=""):
    """Tabla de doble entrada. cells[i][j] enteros. hl_num: celdas resaltadas en naranja; hl_den_col/row: columna o fila resaltada en azul."""
    nr, nc = len(rlabs), len(clabs)
    tot_r = [sum(row) for row in cells]
    tot_c = [sum(cells[i][j] for i in range(nr)) for j in range(nc)]
    N = sum(tot_r)
    cols = nc + (1 if show_totals else 0)
    w0 = 130
    w = (500 - w0) / cols
    h = 44
    body = R(30, 30, 500, h, "#E0F2FE") + T(30 + w0 / 2, 30 + h * 0.65, corner, 16)
    for j, t in enumerate(clabs + (["Total"] if show_totals else [])):
        body += T(30 + w0 + w * (j + 0.5), 30 + h * 0.65, t, 17)
    rows = nr + (1 if show_totals else 0)
    for i in range(rows):
        y = 30 + h * (i + 1)
        lab = rlabs[i] if i < nr else "Total"
        body += R(30, y, 500, h, WHITE) + T(30 + w0 / 2, y + h * 0.65, lab, 17)
        for j in range(cols):
            if i < nr and j < nc: val = cells[i][j]
            elif i < nr: val = tot_r[i]
            elif j < nc: val = tot_c[j]
            else: val = N
            x = 30 + w0 + w * j
            fill = None
            if (i, j) in hl_num: fill = FILL2
            elif hl_den_col is not None and j == hl_den_col and i < nr + (1 if show_totals else 0): fill = FILL3 if False else "#DBEAFE"
            elif hl_den_row is not None and i == hl_den_row: fill = "#DBEAFE"
            if fill: body += R(x, y, w, h, fill, NAVY, 1)
            txt = "?" if hide == (i, j) else str(val)
            body += T(x + w / 2, y + h * 0.65, txt, 18)
    for j in range(cols + 2):
        xx = 30 + (0 if j == 0 else w0 + w * (j - 1))
        body += L(xx, 30, xx, 30 + h * (rows + 1), NAVY, 2)
    for i in range(rows + 2):
        body += L(30, 30 + h * i, 530, 30 + h * i, NAVY, 1.5)
    return wrap(560, 60 + h * (rows + 1), body, "Tabla de doble entrada")


def ptree_fig(first, second, hide=None):
    """Árbol con probabilidades. first=[(nombre, prob_texto)], second=[[(nombre, prob_texto),...] por rama].
    hide=(i,None) oculta la prob de la rama i del 1.er nivel; (i,j) oculta la j-ésima del 2.º nivel."""
    n1 = len(first)
    per = [len(s) for s in second]
    L_ = sum(per)
    dy = min(46, 240 / max(L_, 1))
    top = 140 - dy * (L_ - 1) / 2
    body = ""
    root = (40, 140)
    leaf_i = 0
    for i, (nm, pr) in enumerate(first):
        ys = [top + dy * (leaf_i + j) for j in range(per[i])]
        leaf_i += per[i]
        my = sum(ys) / len(ys)
        body += L(root[0], root[1], 200, my, NAVY, 2.5)
        txt = "?" if hide == (i, None) else pr
        body += tag((root[0] + 200) / 2, (root[1] + my) / 2 - 14, txt, 14) + C(200, my, 8, FILL3, INK, 2) + T(200, my - 16 if False else my - 14, nm, 15, "middle")
        for j, ((nm2, pr2), yy) in enumerate(zip(second[i], ys)):
            body += L(200, my, 430, yy, NAVY, 2.5) + C(430, yy, 6, ACC, INK, 1.5)
            t2 = "?" if hide == (i, j) else pr2
            body += tag(315, (my + yy) / 2 - 12, t2, 14) + T(444, yy + 5, nm2, 15, "start")
    body += C(root[0], root[1], 9, WHITE, INK, 2.5)
    return wrap(560, 290, body, "Árbol de probabilidades")
