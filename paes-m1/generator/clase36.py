"""Clase 36 (M1) · Plano cartesiano y vectores básicos."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG


def M(s):
    return str(s).replace("-", "−")


def pt_(x, y):
    return M(f"({fs(x)}, {fs(y)})")


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is not None and a not in seen:
            seen.add(a); out.append(a)
    return out


def plot(l=0):
    p = Plot(560, 340, -7, 7, -5, 5)
    p.axes(1, 1)
    return p


def arr(p, x1, y1, x2, y2, color=ACC, sw=4):
    X1, Y1, X2, Y2 = p.X(x1), p.Y(y1), p.X(x2), p.Y(y2)
    d = math.hypot(X2 - X1, Y2 - Y1) or 1
    ux, uy = (X2 - X1) / d, (Y2 - Y1) / d
    bx, by = X2 - 14 * ux, Y2 - 14 * uy
    head = f'<polygon points="{X2:.1f},{Y2:.1f} {bx - 7 * uy:.1f},{by + 7 * ux:.1f} {bx + 7 * uy:.1f},{by - 7 * ux:.1f}" fill="{color}" stroke="{color}"/>'
    p.parts.append(L(X1, Y1, bx, by, color, sw) + head)


def dot(p, x, y, label, dx=14, dy=-16):
    p.parts.append(C(p.X(x), p.Y(y), 6, ACC))
    p.parts.append(tag(p.X(x) + dx, p.Y(y) + dy, label, 15))


def quad_of(x, y):
    return "I" if x > 0 and y > 0 else "II" if x < 0 < y else "III" if x < 0 and y < 0 else "IV"


def rp(r, m):
    while True:
        v = r.randint(-m, m)
        if v:
            return v


def distinct_pts(r, n, mx=6, my=4, gap=2):
    pts = []
    for _ in range(200):
        c = (r.randint(-mx, mx), r.randint(-my, my))
        if all(abs(c[0] - q[0]) >= gap or abs(c[1] - q[1]) >= gap for q in pts):
            pts.append(c)
            if len(pts) == n:
                return pts
    raise Reject


# ---------------------------------------------------------------- Resolver problemas
def t_quadrant(r, l):
    if l == 0 or r.random() < 0.4:
        x, y = rp(r, 6), rp(r, 4)
        p = plot(); dot(p, x, y, "P")
        fig = p.svg("Plano cartesiano con el punto P")
        ans = f"Cuadrante {quad_of(x, y)}"
        al = [f"Cuadrante {q}" for q in ("I", "II", "III", "IV") if q != quad_of(x, y)] + ["Sobre uno de los ejes"]
        return make("¿En qué cuadrante del plano cartesiano se ubica el punto P?", fig, ans, al, Q_RES, f"P = {pt_(x, y)}: x {'>' if x > 0 else '<'} 0 e y {'>' if y > 0 else '<'} 0.")
    sa, sb = r.choice([(-1, 1), (1, -1), (-1, -1)])
    w = r.choice(["(b, a)", "(−a, b)", "(a, −b)", "(−b, −a)"])
    a_, b_ = sa, sb
    vals = {"(b, a)": (b_, a_), "(−a, b)": (-a_, b_), "(a, −b)": (a_, -b_), "(−b, −a)": (-b_, -a_)}
    x, y = vals[w]
    sg = lambda s: "positivo" if s > 0 else "negativo"
    p = plot()
    fig = p.svg("Plano cartesiano vacío")
    stem = f"Si a es {sg(sa)} y b es {sg(sb)}, ¿en qué cuadrante se ubica el punto {w}?"
    ans = f"Cuadrante {quad_of(x, y)}"
    al = [f"Cuadrante {q}" for q in ("I", "II", "III", "IV") if q != quad_of(x, y)] + ["Sobre uno de los ejes"]
    return make(stem, fig, ans, al, Q_RES, "Se reemplazan los signos de a y b en cada coordenada.")


def t_midpoint(r, l):
    if l < 2 or r.random() < 0.4:
        while True:
            (x1, y1), (x2, y2) = distinct_pts(r, 2, 6, 4, 3)
            if (x1 + x2) % 2 == 0 and (y1 + y2) % 2 == 0:
                break
        p = plot(); p.parts.append(L(p.X(x1), p.Y(y1), p.X(x2), p.Y(y2), NAVY, 3))
        dot(p, x1, y1, "A"); dot(p, x2, y2, "B")
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        ans = pt_(mx, my)
        al = uq(ans, [pt_(x1 + x2, y1 + y2), pt_(x2 - x1, y2 - y1), pt_(my, mx), pt_((x1 + x2) // 2, (y2 - y1) // 2), pt_(mx + 1, my)])
        return make("¿Cuáles son las coordenadas del punto medio del segmento AB?", p.svg("Segmento AB"), ans, al[:4], Q_RES, f"(({fs(x1)} + {fs(x2)})/2, ({fs(y1)} + {fs(y2)})/2) = {ans}.".replace("-", "−"))
    (ax, ay), (mx, my) = distinct_pts(r, 2, 4, 3, 2)
    bx, by = 2 * mx - ax, 2 * my - ay
    if abs(bx) > 12 or abs(by) > 12:
        raise Reject
    fig = card([f"A = {pt_(ax, ay)}", f"M = {pt_(mx, my)} es el punto medio de AB", "B = ?"], 150, 20)
    ans = pt_(bx, by)
    al = uq(ans, [pt_(mx - ax, my - ay), pt_(ax + mx, ay + my), pt_(by, bx), pt_(2 * mx + ax, 2 * my + ay), pt_(bx + 1, by)])
    return make(f"El punto M es el punto medio del segmento AB. Si A = {pt_(ax, ay)} y M = {pt_(mx, my)}, ¿cuáles son las coordenadas de B?", fig, ans, al[:4], Q_RES, "B = 2M − A en cada coordenada.")


TRIP = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20)]


def t_dist(r, l):
    dx, dy, h = r.choice(TRIP if l else TRIP[:3])
    if r.random() < 0.5:
        dx, dy = dy, dx
    if dx > 12 or dy > 8:
        dx, dy = min(dx, 12), min(dy, 8)
        if (dx, dy) not in [(t[0], t[1]) for t in TRIP] + [(t[1], t[0]) for t in TRIP]:
            raise Reject
    h = int(math.hypot(dx, dy))
    if h * h != dx * dx + dy * dy:
        raise Reject
    x1 = r.randint(-7, 7 - dx); y1 = r.randint(-5, 5 - dy)
    if r.random() < 0.5:
        x1, x2 = x1 + dx, x1
    else:
        x2 = x1 + dx
    y2 = y1 + dy
    p = plot()
    p.parts.append(L(p.X(x1), p.Y(y1), p.X(x2), p.Y(y2), NAVY, 3))
    dot(p, x1, y1, "A"); dot(p, x2, y2, "B")
    ans = f"{h} unidades"
    al = uq(ans, [f"{dx + dy} unidades", f"{dx * dy} unidades", f"{h + 1} unidades", f"{abs(dx - dy)} unidades", f"{dx * dx + dy * dy} unidades"])
    ex = f"d = √({dx}² + {dy}²) = √{dx * dx + dy * dy} = {h}."
    return make("¿Cuál es la distancia entre los puntos A y B del plano?", p.svg("Puntos A y B"), ans, al[:4], Q_RES, ex)


def t_vec_op(r, l):
    a, b, c, d = rp(r, 3), rp(r, 3), rp(r, 3), rp(r, 3)
    if (a, b) == (c, d):
        raise Reject
    p = plot()
    arr(p, 0, 0, a, b); arr(p, 0, 0, c, d, NAVY)
    p.parts.append(tag(p.X(a) + 16, p.Y(b) - 14, "u", 16)); p.parts.append(tag(p.X(c) + 16, p.Y(d) - 14, "v", 16))
    ops = [("u + v", lambda: (a + c, b + d), lambda: (a - c, b - d)), ("u − v", lambda: (a - c, b - d), lambda: (a + c, b + d))]
    if l:
        ops.append(("2u + v", lambda: (2 * a + c, 2 * b + d), lambda: (a + 2 * c, b + 2 * d)))
    if l == 2:
        ops.append(("u − 2v", lambda: (a - 2 * c, b - 2 * d), lambda: (2 * a - c, 2 * b - d)))
    nm, f, g = r.choice(ops)
    x, y = f(); gx, gy = g()
    ans = pt_(x, y)
    al = uq(ans, [pt_(gx, gy), pt_(y, x), pt_(-x, -y), pt_(x + 1, y), pt_(a * c, b * d)])
    return make(f"En la figura, u = {pt_(a, b)} y v = {pt_(c, d)}. ¿Cuál es el vector {nm}?", p.svg("Vectores u y v desde el origen"), ans, al[:4], Q_RES, f"Se opera componente a componente: {nm} = {ans}.")


# ---------------------------------------------------------------- Modelar
def t_route(r, l):
    n = 2 + l
    while True:
        x = y = 0
        pts = [(0, 0)]
        legs = []
        dirs = [("al este", 1, 0), ("al norte", 0, 1), ("al oeste", -1, 0), ("al sur", 0, -1)]
        last = -1
        for i in range(n + 1):
            k = r.randrange(4)
            while k == last or (last >= 0 and k == (last + 2) % 4):
                k = r.randrange(4)
            last = k
            s = r.randint(1, 5)
            nm, dx, dy = dirs[k]
            x += s * dx; y += s * dy
            legs.append(f"{s} unidades {nm}")
            pts.append((x, y))
        if all(abs(px) <= 6 and abs(py) <= 4 for px, py in pts) and (x, y) != (0, 0) and len(set(pts)) == len(pts):
            break
    p = plot()
    for (a, b), (c, d) in zip(pts, pts[1:]):
        arr(p, a, b, c, d)
    dot(p, 0, 0, "O", -14, 16)
    ans = pt_(x, y)
    al = uq(ans, [pt_(y, x), pt_(-x, y), pt_(x, -y), pt_(-x, -y), pt_(x + 1, y), pt_(x, y + 1)])
    obj = r.choice(["Un dron", "Un robot", "Una hormiga"])
    stem = f"{obj} parte del origen (0, 0) y avanza {', luego '.join(legs)}. ¿En qué punto del plano queda?"
    return make(stem, p.svg("Recorrido desde el origen"), ans, al[:4], Q_MOD, f"Se suman los desplazamientos en x y en y: {ans}.")


def t_map(r, l):
    dx, dy, h = r.choice(TRIP[:3] + TRIP[3:5] if l else TRIP[:3])
    if dx > 12 or dy > 8:
        raise Reject
    sc = r.choice([100, 50, 200])
    x1 = r.randint(-7, 7 - dx); y1 = r.randint(-5, 5 - dy)
    p = plot()
    p.parts.append(L(p.X(x1), p.Y(y1), p.X(x1 + dx), p.Y(y1), NAVY, 2, "6 5") + L(p.X(x1 + dx), p.Y(y1), p.X(x1 + dx), p.Y(y1 + dy), NAVY, 2, "6 5") + L(p.X(x1), p.Y(y1), p.X(x1 + dx), p.Y(y1 + dy), NAVY, 3))
    dot(p, x1, y1, "A"); dot(p, x1 + dx, y1 + dy, "B", 4, -22)
    ans = f"{h * sc} m"
    al = uq(ans, [f"{(dx + dy) * sc} m", f"{dx * dy * sc} m", f"{h} m", f"{(h + 1) * sc} m", f"{(dx * dx + dy * dy) * sc} m"])
    place = r.choice([("el colegio", "la plaza"), ("la casa", "el almacén"), ("la estación", "el parque")])
    stem = f"En un plano, {place[0]} (A) y {place[1]} (B) se ubican como muestra la figura. Cada unidad del plano equivale a {sc} m. ¿Cuál es la distancia en línea recta entre ambos?"
    return make(stem, p.svg("Puntos A y B con sus catetos"), ans, al[:4], Q_MOD, f"d = {h} unidades = {h}·{sc} = {h * sc} m.")


def t_area(r, l):
    b, h = r.randint(2, 6), r.randint(2, 4)
    x0, y0 = r.randint(-6, 6 - b), r.randint(-4, 4 - h)
    kind = r.choice(["tri", "rect"])
    p = plot()
    if kind == "tri":
        ap = r.randint(0, b)
        pts = [(x0, y0), (x0 + b, y0), (x0 + ap, y0 + h)]
        area = F(b * h, 2)
        nm = "triángulo"
    else:
        pts = [(x0, y0), (x0 + b, y0), (x0 + b, y0 + h), (x0, y0 + h)]
        area = F(b * h)
        nm = "rectángulo"
    p.parts.append(P([(p.X(a), p.Y(c)) for a, c in pts], FILL2, NAVY, 3))
    for (a, c), nn in zip(pts, "ABCD"):
        dot(p, a, c, nn, 12 if a >= x0 + b else -12, 8 if c == y0 else -14)
    sc = r.choice([1, 10, 20]) if l else r.choice([1, 10])
    u = "u²" if sc == 1 else "m²"
    val = area * sc * sc
    ans = f"{fs(val)} {u}"
    al = uq(ans, [f"{fs(area * sc * sc * 2)} {u}", f"{fs(F(b * h) * sc * sc if kind == 'tri' else F(b * h, 2) * sc * sc)} {u}", f"{fs((b + h) * sc * sc)} {u}", f"{fs(val * sc)} {u}", f"{fs(val + sc)} {u}"])
    verts = ", ".join(f"{nn} = {pt_(a, c)}" for (a, c), nn in zip(pts, "ABCD"))
    unit_txt = "" if sc == 1 else f" Cada unidad del plano equivale a {sc} m."
    stem = f"Los vértices de un {nm} son {verts}.{unit_txt} ¿Cuál es su área?"
    return make(stem, p.svg(f"Un {nm} en el plano"), ans, al[:4], Q_MOD, f"Base {b}, altura {h}: área = {fs(area)} u²" + ("" if sc == 1 else f", y {fs(area)}·{sc * sc} = {fs(val)} m²") + ".")


def t_disp(r, l):
    ax, ay = rp(r, 5), rp(r, 4)
    a, b, c, d = rp(r, 3), rp(r, 3), rp(r, 3), rp(r, 3)
    if l == 0:
        c = d = 0
    x, y = ax + a + c, ay + b + d
    if l == 0:
        stem = f"Una persona está en el punto A = {pt_(ax, ay)} y se desplaza según el vector u = {pt_(a, b)}. ¿En qué punto queda?"
        lines = [f"A = {pt_(ax, ay)}", f"Desplazamiento u = {pt_(a, b)}", "Llegada = ?"]
    else:
        stem = f"Una persona está en A = {pt_(ax, ay)}. Se desplaza según u = {pt_(a, b)} y luego según v = {pt_(c, d)}. ¿En qué punto queda?"
        lines = [f"A = {pt_(ax, ay)}", f"u = {pt_(a, b)}", f"v = {pt_(c, d)}", "Llegada = ?"]
    ans = pt_(x, y)
    al = uq(ans, [pt_(y, x), pt_(a + c, b + d), pt_(ax - a - c, ay - b - d), pt_(x + 1, y), pt_(ax + a - c, ay + b - d)])
    fig = card(lines, 40 + 36 * len(lines), 20)
    return make(stem, fig, ans, al[:4], Q_MOD, f"Se suma el desplazamiento total a las coordenadas de A: {ans}.")


# ---------------------------------------------------------------- Representar
def t_read_point(r, l):
    pts = distinct_pts(r, 4, 6, 4, 2)
    names = "PQRS"
    p = plot()
    for (a, b), n in zip(pts, names):
        dot(p, a, b, n)
    k = r.randrange(4)
    x, y = pts[k]
    if x == y or x == -y:
        raise Reject
    ans = pt_(x, y)
    al = uq(ans, [pt_(y, x), pt_(-x, y), pt_(x, -y), pt_(-x, -y), pt_(-y, -x)])
    return make(f"¿Cuáles son las coordenadas del punto {names[k]} en el plano cartesiano?", p.svg("Cuatro puntos en el plano"), ans, al[:4], Q_REP, f"Se lee primero el valor en x y luego en y: {ans}.")


def t_vec_fig(r, l):
    (ax, ay), (bx, by) = distinct_pts(r, 2, 5, 3, 2)
    dx, dy = bx - ax, by - ay
    if abs(dx) == abs(dy) or dx == 0 or dy == 0:
        raise Reject
    p = plot()
    arr(p, ax, ay, bx, by)
    dot(p, ax, ay, "A", -14, -16); dot(p, bx, by, "B", 14, -16)
    ans = pt_(dx, dy)
    al = uq(ans, [pt_(-dx, -dy), pt_(dy, dx), pt_(ax + bx, ay + by), pt_(bx, by), pt_(dx, -dy)])
    return make("¿Cuáles son las componentes del vector AB dibujado en la figura?", p.svg("Vector AB"), ans, al[:4], Q_REP, f"AB = B − A = ({fs(bx)} − {fs(ax)}, {fs(by)} − {fs(ay)}) = {ans}.".replace("-", "−"))


def t_reflect(r, l):
    x, y = rp(r, 5), rp(r, 3)
    if abs(x) == abs(y):
        raise Reject
    kinds = [("el eje X", (x, -y)), ("el eje Y", (-x, y))]
    if l:
        kinds.append(("el origen", (-x, -y)))
    nm, (rx, ry) = r.choice(kinds)
    p = plot(); dot(p, x, y, "P")
    ans = pt_(rx, ry)
    al = uq(ans, [pt_(x, -y), pt_(-x, y), pt_(-x, -y), pt_(y, x), pt_(x, y)])
    return make(f"El punto P = {pt_(x, y)} se refleja respecto de {nm}. ¿Cuáles son las coordenadas de su imagen?", p.svg("Punto P"), ans, al[:4], Q_REP, f"Reflejar respecto de {nm} cambia el signo de las coordenadas correspondientes.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Distancia entre A(0, 0) y B(3, 4)", "d = 3 + 4 = 7 unidades"], "Sumó las diferencias: debía usar el teorema de Pitágoras, d = √(3² + 4²) = 5", \
            ["Restó las coordenadas en lugar de sumarlas antes de calcular la distancia", "Multiplicó las diferencias de coordenadas en lugar de sumarlas", "Calculó bien la distancia, pero olvidó escribir la unidad de medida", "Usó la diferencia de las coordenadas y dividió el resultado por dos"]
    if k == 1:
        return ["Punto medio de A(2, 4) y B(6, 8)", "M = (2 + 6, 4 + 8) = (8, 12)"], "Sumó las coordenadas sin dividir por 2: el punto medio es (4, 6)", \
            ["Restó las coordenadas en lugar de sumarlas para obtener el punto medio", "Intercambió las coordenadas x e y al calcular el punto medio del segmento", "Dividió por dos solo la coordenada x y dejó la coordenada y sin dividir", "Multiplicó las coordenadas de ambos puntos en lugar de sumarlas entre sí"]
    if k == 2:
        return ["A(1, 2), B(4, 6)", "Vector AB = A − B = (−3, −4)"], "Restó en el orden inverso: AB = B − A = (3, 4)", \
            ["Sumó las coordenadas de A y B en lugar de restarlas para hallar el vector", "Intercambió las coordenadas: el vector correcto sería (4, 3) y no (3, 4)", "Calculó la distancia entre A y B y no las componentes del vector AB", "Restó bien las coordenadas, pero cambió el signo de la segunda componente"]
    return ["El punto (−3, 2)", "Está en el cuadrante IV"], "Confundió los signos: x < 0 e y > 0 corresponde al cuadrante II", \
        ["Ubicó primero la coordenada y y después la coordenada x sobre los ejes", "Consideró que el punto está sobre el eje Y porque su segunda coordenada es 2", "Contó los cuadrantes en el sentido de las agujas del reloj al ubicar el punto", "Pensó que el signo negativo indica que el punto está bajo el eje X"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    q = r.choice(["I", "II", "III", "IV"])
    sg = {"I": (1, 1), "II": (-1, 1), "III": (-1, -1), "IV": (1, -1)}
    ans_pt = (sg[q][0] * r.randint(1, 6), sg[q][1] * r.randint(1, 5))
    alts = []
    for k, (sx, sy) in sg.items():
        if k != q:
            alts.append(pt_(sx * r.randint(1, 6), sy * r.randint(1, 5)))
    alts.append(pt_(0, r.choice([-3, 2, 4])))
    p = plot()
    for txt, (sx, sy) in zip(["I", "II", "III", "IV"], [sg["I"], sg["II"], sg["III"], sg["IV"]]):
        p.parts.append(tag(p.X(sx * 4), p.Y(sy * 3), txt, 18))
    return make(f"¿Cuál de los siguientes puntos pertenece al cuadrante {q}?", p.svg("Cuadrantes I a IV"), pt_(*ans_pt), alts, Q_ARG, f"En el cuadrante {q}, x es {'positivo' if sg[q][0] > 0 else 'negativo'} e y es {'positivo' if sg[q][1] > 0 else 'negativo'}.")


TRUE = ["Todo punto del eje Y tiene abscisa igual a 0", "El punto (0, 0) es el origen del plano cartesiano", "En el cuadrante III ambas coordenadas son negativas",
        "El vector AB = B − A tiene componentes (xB − xA, yB − yA)", "Sumar vectores equivale a sumar sus componentes", "El punto medio de un segmento tiene por coordenadas el promedio de las de sus extremos"]
FALSE = ["Todo punto del eje X tiene ordenada distinta de 0", "El punto (3, 0) pertenece al cuadrante I", "En el cuadrante II ambas coordenadas son positivas",
         "Los vectores AB y BA son exactamente iguales", "La distancia entre dos puntos se obtiene sumando las diferencias de sus coordenadas", "El punto medio de un segmento se obtiene sumando las coordenadas de sus extremos"]


def _fig(r):
    p = plot()
    a, b = distinct_pts(r, 2, 6, 4, 3)
    dot(p, a[0], a[1], "A"); dot(p, b[0], b[1], "B")
    return p.svg("Plano cartesiano")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el plano cartesiano y los vectores es verdadera?", "Sobre plano cartesiano y vectores, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta cada afirmación con las definiciones de coordenadas y vectores.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el plano cartesiano y los vectores es falsa?", "Sobre plano cartesiano y vectores, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones.")


BY_SKILL = {
    Q_RES: [t_quadrant, t_midpoint, t_dist, t_vec_op],
    Q_MOD: [t_route, t_map, t_area, t_disp],
    Q_REP: [t_read_point, t_vec_fig, t_reflect],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
