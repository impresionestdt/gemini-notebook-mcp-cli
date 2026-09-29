"""Clase 37 (M1) · Isometrías: traslación y reflexión."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase36 import M, pt_, uq, plot, arr, dot, rp, quad_of


def tri_pts(r, mx=4, my=3):
    while True:
        p = [(r.randint(-mx, mx), r.randint(-my, my)) for _ in range(3)]
        (a, b), (c, d), (e, f) = p
        if len(set(p)) == 3 and abs((c - a) * (f - b) - (e - a) * (d - b)) >= 4:
            return p


def draw_poly(p, pts, names, fill, stroke=NAVY, lab_dx=0):
    p.parts.append(P([(p.X(a), p.Y(b)) for a, b in pts], fill, stroke, 3))
    cx = sum(a for a, _ in pts) / len(pts); cy = sum(b for _, b in pts) / len(pts)
    for (a, b), n in zip(pts, names):
        sx = 1 if a >= cx else -1
        sy = 1 if b >= cy else -1
        p.parts.append(C(p.X(a), p.Y(b), 5, ACC))
        p.parts.append(tag(p.X(a) + 15 * sx, p.Y(b) - 15 * sy, n, 14))


def fits(pts, mx=6, my=4):
    return all(abs(a) <= mx and abs(b) <= my for a, b in pts)


def refl(pt, kind, k=0):
    x, y = pt
    return {"X": (x, -y), "Y": (-x, y), "O": (-x, -y), "x=k": (2 * k - x, y), "y=k": (x, 2 * k - y)}[kind]


NAMES = {"X": "el eje X", "Y": "el eje Y", "O": "el origen"}


# ---------------------------------------------------------------- Resolver problemas
def t_translate(r, l):
    ax, ay = rp(r, 4), rp(r, 3)
    a, b = rp(r, 4), rp(r, 3)
    if not fits([(ax + a, ay + b)]):
        raise Reject
    p = plot(); dot(p, ax, ay, "A"); arr(p, ax, ay, ax + a, ay + b, NAVY, 3)
    ans = pt_(ax + a, ay + b)
    al = uq(ans, [pt_(ax - a, ay - b), pt_(ax + b, ay + a), pt_(a, b), pt_(ax * a, ay * b), pt_(ax + a, ay - b)])
    return make(f"El punto A = {pt_(ax, ay)} se traslada según el vector v = {pt_(a, b)}. ¿Cuáles son las coordenadas de A′?", p.svg("Punto A y su traslación"), ans, al[:4], Q_RES, f"A′ = ({fs(ax)} + {fs(a)}, {fs(ay)} + {fs(b)}) = {ans}.".replace("-", "−"))


def t_reflect_pt(r, l):
    x, y = rp(r, 5), rp(r, 3)
    kinds = ["X", "Y"] + (["O"] if l else []) + (["x=k", "y=k"] if l == 2 else [])
    kd = r.choice(kinds); k = 0
    p = plot()
    if kd in ("x=k", "y=k"):
        k = r.choice([-2, -1, 1, 2])
        if kd == "x=k":
            p.vline(k); nm = f"la recta x = {M(k)}"
        else:
            p.hline(k); nm = f"la recta y = {M(k)}"
    else:
        nm = NAMES[kd]
    rx, ry = refl((x, y), kd, k)
    if not fits([(rx, ry)]) or (rx, ry) == (x, y):
        raise Reject
    dot(p, x, y, "P")
    ans = pt_(rx, ry)
    al = uq(ans, [pt_(x, -y), pt_(-x, y), pt_(-x, -y), pt_(y, x), pt_(x, y), pt_(2 * k + x, y), pt_(x, 2 * k + y)])
    return make(f"¿Cuáles son las coordenadas de la imagen del punto P = {pt_(x, y)} al reflejarlo respecto de {nm}?", p.svg("Punto P"), ans, al[:4], Q_RES, f"La reflexión conserva la distancia al eje de simetría y cambia de lado: {ans}.")


def t_find_img(r, l):
    (ax, ay), (bx, by), (cx, cy) = tri_pts(r)
    a, b = rp(r, 3), rp(r, 2)
    pts = [(ax, ay), (bx, by), (cx, cy)]
    if not fits([(x + a, y + b) for x, y in pts]):
        raise Reject
    p = plot(); draw_poly(p, pts, "ABC", FILL2)
    dot(p, ax + a, ay + b, "A′")
    k = r.choice([1, 2])
    tx, ty = pts[k]
    nm = "BC"[k - 1]
    ans = pt_(tx + a, ty + b)
    al = uq(ans, [pt_(tx - a, ty - b), pt_(tx, ty), pt_(tx + b, ty + a), pt_(a, b), pt_(tx + a, ty - b)])
    stem = f"El triángulo ABC se traslada y A = {pt_(ax, ay)} pasa a A′ = {pt_(ax + a, ay + b)}. Si {nm} = {pt_(tx, ty)}, ¿cuáles son las coordenadas de {nm}′?"
    return make(stem, p.svg("Triángulo ABC y el punto A′"), ans, al[:4], Q_RES, f"El vector de traslación es {pt_(a, b)}; se aplica a {nm}.")


def t_compose(r, l):
    x, y = rp(r, 3), rp(r, 2)
    a, b = rp(r, 3), rp(r, 2)
    kd = r.choice(["X", "Y"])
    rx, ry = refl((x, y), kd)
    fx, fy = rx + a, ry + b
    if not fits([(fx, fy)]):
        raise Reject
    p = plot(); dot(p, x, y, "P")
    ans = pt_(fx, fy)
    al = uq(ans, [pt_(x + a, y + b) if False else pt_(refl((x + a, y + b), kd)[0], refl((x + a, y + b), kd)[1]), pt_(x + a, y + b), pt_(-x + a, -y + b), pt_(fx, -fy), pt_(fx + 1, fy)])
    return make(f"El punto P = {pt_(x, y)} se refleja respecto de {NAMES[kd]} y luego la imagen se traslada según el vector {pt_(a, b)}. ¿Dónde queda finalmente?", p.svg("Punto P"), ans, al[:4], Q_RES, f"Primero P′ = {pt_(rx, ry)} y luego se suma el vector: {ans}.")


# ---------------------------------------------------------------- Modelar
def t_perim(r, l):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15), (8, 15, 17)])
    u = r.choice(["cm", "m"])
    kind = r.choice(["traslada", "refleja"])
    per = a + b + c
    fig = card([f"Triángulo de lados {a}, {b} y {c} {u}", f"Se {kind}: obtiene su imagen", "Perímetro de la imagen = ?"], 150, 19)
    ans = f"{per} {u}"
    al = uq(ans, [f"{2 * per} {u}", f"{per // 2 if per % 2 == 0 else per + 3} {u}", f"{a * b // 2 if (a * b) % 2 == 0 else a * b} {u}", f"{per + a} {u}", f"{a + b} {u}"])
    return make(f"Un triángulo de lados {a} {u}, {b} {u} y {c} {u} se {kind}. ¿Cuál es el perímetro de la figura imagen?", fig, ans, al[:4], Q_MOD, "Una isometría conserva las longitudes, por lo que el perímetro no cambia.")


def t_mirror(r, l):
    x, y = r.randint(-5, 5), r.randint(1, 4)
    if l == 0 or r.random() < 0.5:
        d = y
        p = plot(); dot(p, x, y, "A"); dot(p, x, -y, "A′")
        p.parts.append(L(p.X(x), p.Y(y), p.X(x), p.Y(-y), NAVY, 2, "6 5"))
        sc = r.choice([10, 20, 50])
        ans = f"{2 * d * sc} m"
        al = uq(ans, [f"{d * sc} m", f"{2 * d} m", f"{(2 * d + 1) * sc} m", f"{4 * d * sc} m", f"{d * sc * sc} m"])
        stem = f"Un poste (punto A = {pt_(x, y)}) se refleja en un lago cuya orilla es el eje X. Cada unidad equivale a {sc} m. ¿A qué distancia está el poste de su reflejo A′?"
        return make(stem, p.svg("Poste y reflejo"), ans, al[:4], Q_MOD, f"Cada punto está a {d} unidades del eje: la distancia es 2·{d}·{sc} = {2 * d * sc} m.")
    k = r.randint(1, 3)
    if y == k:
        raise Reject
    ry = 2 * k - y
    p = plot(); p.hline(k); dot(p, x, y, "A"); dot(p, x, ry, "A′") if fits([(x, ry)]) else None
    if not fits([(x, ry)]):
        raise Reject
    ans = f"{abs(2 * (y - k))} unidades"
    al = uq(ans, [f"{abs(y - k)} unidades", f"{abs(y - ry) + 1} unidades", f"{abs(y + ry)} unidades", f"{2 * y} unidades", f"{abs(y - k) + 2} unidades"])
    stem = f"Un punto A = {pt_(x, y)} se refleja respecto de la recta y = {k} (un espejo horizontal). ¿A qué distancia queda A de su imagen A′?"
    return make(stem, p.svg("Espejo horizontal y punto A"), ans, al[:4], Q_MOD, f"La imagen queda al otro lado del espejo, a igual distancia: 2·|{y} − {k}|.")


def t_tiles(r, l):
    x0, y0 = rp(r, 3), rp(r, 2)
    a, b = r.randint(1, 3), r.choice([0, 1, -1]) if l else 0
    n = r.randint(4, 8)
    fx, fy = x0 + (n - 1) * a, y0 + (n - 1) * b
    fig = card([f"1.ª baldosa en {pt_(x0, y0)}", f"Cada baldosa se traslada {pt_(a, b)}", f"Posición de la baldosa n.° {n} = ?"], 150, 19)
    ans = pt_(fx, fy)
    al = uq(ans, [pt_(x0 + n * a, y0 + n * b), pt_(x0 + (n - 2) * a, y0 + (n - 2) * b), pt_(fy, fx), pt_(x0 + a, y0 + b), pt_(n * a, n * b)])
    stem = f"Un patrón se forma trasladando una baldosa siempre según el vector {pt_(a, b)}. Si la primera baldosa está en {pt_(x0, y0)}, ¿en qué punto está la baldosa número {n}?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Hay {n - 1} traslaciones: {pt_(x0, y0)} + {n - 1}·{pt_(a, b)} = {ans}.")


def t_slide(r, l):
    x, y = rp(r, 4), rp(r, 3)
    a, b, c, d = rp(r, 3), rp(r, 2), rp(r, 3), rp(r, 2)
    fx, fy = x + a + c, y + b + d
    if not fits([(fx, fy)]) or (a + c, b + d) == (0, 0):
        raise Reject
    obj = r.choice(["Un cursor", "Un personaje", "Una pieza"])
    fig = card([f"Inicio: {pt_(x, y)}", f"1.º movimiento: {pt_(a, b)}", f"2.º movimiento: {pt_(c, d)}", "Un solo movimiento equivalente = ?"], 190, 19)
    ans = pt_(a + c, b + d)
    al = uq(ans, [pt_(a - c, b - d), pt_(fx, fy), pt_(b + d, a + c), pt_(a * c, b * d), pt_(-a - c, -b - d)])
    stem = f"{obj} parte de {pt_(x, y)}, se traslada según {pt_(a, b)} y luego según {pt_(c, d)}. ¿Qué único vector de traslación produce el mismo resultado?"
    return make(stem, fig, ans, al[:4], Q_MOD, "Dos traslaciones consecutivas equivalen a una con la suma de los vectores.")


# ---------------------------------------------------------------- Representar
def t_which(r, l):
    pts = tri_pts(r)
    kd = r.choice(["T", "X", "Y"])
    if kd == "T":
        a, b = rp(r, 4), rp(r, 3)
        img = [(x + a, y + b) for x, y in pts]
        ans = f"Traslación según {pt_(a, b)}"
        al = ["Reflexión respecto del eje X", "Reflexión respecto del eje Y", "Simetría respecto del origen", f"Traslación según {pt_(-a, -b)}", f"Traslación según {pt_(b, a)}"]
    else:
        img = [refl(q, kd) for q in pts]
        ans = f"Reflexión respecto de {NAMES[kd]}"
        o = "Y" if kd == "X" else "X"
        a, b = rp(r, 3), rp(r, 3)
        al = [f"Reflexión respecto de {NAMES[o]}", "Simetría respecto del origen", f"Traslación según {pt_(a, b)}", f"Traslación según {pt_(b, a)}"]
    if not fits(img) or any(abs(x) < 1 for x, _ in pts + img if kd == "Y") or any(abs(y) < 1 for _, y in pts + img if kd == "X") or set(pts) & set(img):
        raise Reject
    p = plot(); draw_poly(p, pts, "ABC", FILL2); draw_poly(p, img, ["A′", "B′", "C′"], FILL3)
    return make("En la figura, el triángulo A′B′C′ es la imagen de ABC. ¿Qué transformación isométrica lo produjo?", p.svg("Triángulo ABC y su imagen"), ans, uq(ans, al)[:4], Q_REP, "Se comparan las posiciones de los vértices correspondientes.")


def t_read_img(r, l):
    pts = tri_pts(r)
    a, b = rp(r, 4), rp(r, 3)
    kd = r.choice(["T", "X", "Y"])
    img = [(x + a, y + b) for x, y in pts] if kd == "T" else [refl(q, kd) for q in pts]
    if not fits(img) or set(pts) & set(img):
        raise Reject
    p = plot(); draw_poly(p, pts, "ABC", FILL2); draw_poly(p, img, ["A′", "B′", "C′"], FILL3)
    k = r.randrange(3)
    ans = pt_(*img[k])
    x, y = pts[k]
    al = uq(ans, [pt_(x, y), pt_(-x, -y), pt_(x + a, y - b), pt_(y, x), pt_(img[k][0], img[k][1] + 1)])
    nm = "ABC"[k]
    return make(f"El triángulo A′B′C′ es la imagen de ABC en el plano. ¿Cuáles son las coordenadas del vértice {nm}′?", p.svg("Triángulo ABC y su imagen"), ans, al[:4], Q_REP, f"Se lee la posición de {nm}′ en el plano: {ans}.")


def t_rule(r, l):
    a, b = rp(r, 4), rp(r, 3)
    x, y = rp(r, 3), rp(r, 2)
    p = plot(); dot(p, x, y, "P"); dot(p, x + a, y + b, "P′") if fits([(x + a, y + b)]) else None
    if not fits([(x + a, y + b)]):
        raise Reject
    sg = lambda v: ("+ " + str(v)) if v > 0 else ("− " + str(-v))
    ans = M(f"(x, y) → (x {sg(a)}, y {sg(b)})")
    al = uq(ans, [M(f"(x, y) → (x {sg(-a)}, y {sg(-b)})"), M(f"(x, y) → (x {sg(b)}, y {sg(a)})"), M(f"(x, y) → (x {sg(a)}, y {sg(-b)})"), M(f"(x, y) → ({sg(a)[0]}x, {sg(b)[0]}y)") if False else M(f"(x, y) → (−x {sg(a)}, y {sg(b)})"), M(f"(x, y) → (x·{abs(a)}, y·{abs(b)})")])
    return make(f"En la figura, P′ es la imagen de P = {pt_(x, y)} mediante una traslación. ¿Cuál regla describe esa traslación?", p.svg("Punto P y su imagen P′"), ans, al[:4], Q_REP, f"P′ − P = {pt_(a, b)}, es decir, se suma {fs(a)} a x y {fs(b)} a y.".replace("-", "−"))


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Reflejar A(3, 2) respecto del eje X", "A′ = (−3, 2)"], "Cambió el signo de x; en una reflexión respecto del eje X cambia el signo de y", \
            ["Cambió el signo de ambas coordenadas, lo que corresponde a una simetría central", "Intercambió las coordenadas x e y, lo que refleja respecto de la recta y = x", "Reflejó correctamente, pero olvidó escribir el punto imagen con el apóstrofo", "Sumó 3 a la abscisa en lugar de reflejar el punto respecto del eje X"]
    if k == 1:
        return ["Trasladar A(1, 2) según (3, −1)", "A′ = (1 − 3, 2 + 1) = (−2, 3)"], "Restó el vector: en una traslación se suman las componentes a las coordenadas", \
            ["Sumó solo la primera componente y dejó la segunda coordenada sin cambiar", "Intercambió las componentes del vector antes de sumarlas a las coordenadas", "Multiplicó las coordenadas por las componentes del vector de traslación", "Trasladó bien el punto, pero dibujó el resultado en el cuadrante equivocado"]
    if k == 2:
        return ["Un triángulo de área 12 cm² se refleja", "El área de la imagen es 24 cm²"], "Una reflexión conserva las áreas: la imagen también tiene 12 cm²", \
            ["Una reflexión reduce el área a la mitad porque solo se dibuja un lado", "El área de la imagen depende de la distancia entre el eje y la figura", "Una reflexión invierte el signo del área, por lo que la imagen mide −12 cm²", "El área de la imagen aumenta o disminuye según el eje de simetría elegido"]
    return ["Una figura se traslada según (2, 0)", "La imagen queda girada 90° respecto de la original"], "Una traslación no gira la figura: conserva su orientación y su tamaño", \
        ["Una traslación siempre gira la figura en un ángulo igual a la primera componente", "La imagen queda girada porque la traslación cambia el sentido de los vértices", "La imagen queda girada solo cuando la segunda componente del vector vale cero", "Toda isometría gira la figura, por lo que la conclusión del estudiante es correcta"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_prop(r, l):
    pts = tri_pts(r)
    kd = r.choice(["T", "X", "Y"])
    a, b = rp(r, 4), rp(r, 3)
    img = [(x + a, y + b) for x, y in pts] if kd == "T" else [refl(q, kd) for q in pts]
    if not fits(img) or set(pts) & set(img):
        raise Reject
    p = plot(); draw_poly(p, pts, "ABC", FILL2); draw_poly(p, img, ["A′", "B′", "C′"], FILL3)
    ans = "Los lados y los ángulos de ambos triángulos son congruentes"
    al = ["Los lados de A′B′C′ miden el doble que los de ABC", "El perímetro de A′B′C′ es menor que el de ABC", "Los ángulos de A′B′C′ son distintos a los de ABC", "El área de A′B′C′ es mayor que el área de ABC"]
    return make("El triángulo A′B′C′ es la imagen de ABC mediante una isometría. ¿Cuál afirmación es siempre verdadera?", p.svg("Triángulo ABC y su imagen"), ans, al, Q_ARG, "Toda isometría conserva longitudes, ángulos y áreas.")


TRUE = ["Una traslación conserva la longitud de los lados de la figura", "Una reflexión conserva el área de la figura", "Al reflejar respecto del eje Y cambia el signo de la abscisa", "Al trasladar según (a, b) se suma a a la abscisa y b a la ordenada",
        "En una reflexión, el eje de simetría es la mediatriz del segmento que une un punto con su imagen", "Una traslación y una reflexión son isometrías"]
FALSE = ["Una traslación modifica la medida de los ángulos de la figura", "Una reflexión duplica el área de la figura original", "Al reflejar respecto del eje Y cambia el signo de la ordenada", "Al trasladar según (a, b) se multiplica la abscisa por a y la ordenada por b",
         "En una reflexión, un punto y su imagen siempre están a distinta distancia del eje", "Las isometrías cambian la forma de las figuras"]


def _fig(r):
    pts = tri_pts(r); p = plot(); draw_poly(p, pts, "ABC", FILL2)
    return p.svg("Triángulo ABC")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre traslaciones y reflexiones es verdadera?", "Sobre isometrías, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de las isometrías.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre traslaciones y reflexiones es falsa?", "Sobre isometrías, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las isometrías.")


BY_SKILL = {
    Q_RES: [t_translate, t_reflect_pt, t_find_img, t_compose],
    Q_MOD: [t_perim, t_mirror, t_tiles, t_slide],
    Q_REP: [t_which, t_read_img, t_rule],
    Q_ARG: [t_error, t_prop, t_true, t_false],
}
