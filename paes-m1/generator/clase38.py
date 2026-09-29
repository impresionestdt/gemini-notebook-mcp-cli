"""Clase 38 (M1) · Isometrías: rotación."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase36 import M, pt_, uq, plot, arr, dot, rp
from clase37 import tri_pts, draw_poly, fits, refl, NAMES


def rot(pt, ang, c=(0, 0)):
    """Rotación antihoraria de ang grados (múltiplo de 90) alrededor de c."""
    x, y = pt[0] - c[0], pt[1] - c[1]
    for _ in range((ang // 90) % 4):
        x, y = -y, x
    return (x + c[0], y + c[1])


def ang_txt(a):
    a %= 360
    return {90: "90° en sentido antihorario", 180: "180°", 270: "90° en sentido horario"}[a]


def regular(cx, cy, R, n, off=-90):
    return [(cx + R * math.cos(math.radians(off + 360 * i / n)), cy + R * math.sin(math.radians(off + 360 * i / n))) for i in range(n)]


# ---------------------------------------------------------------- Resolver problemas
def t_rot_pt(r, l):
    x, y = rp(r, 4), rp(r, 3)
    a = r.choice([90, 180, 270] if l else [90, 180])
    rx, ry = rot((x, y), a)
    if not fits([(rx, ry)]) or abs(x) == abs(y):
        raise Reject
    p = plot(); dot(p, x, y, "P")
    ans = pt_(rx, ry)
    al = uq(ans, [pt_(*rot((x, y), a + 180)), pt_(*rot((x, y), 90 if a != 90 else 180)), pt_(y, x), pt_(x, -y), pt_(-x, y), pt_(*rot((x, y), 270 if a != 270 else 90))])
    stem = f"El punto P = {pt_(x, y)} se rota {ang_txt(a)} con centro en el origen. ¿Cuáles son las coordenadas de su imagen P′?"
    return make(stem, p.svg("Punto P"), ans, al[:4], Q_RES, f"Al rotar 90° antihorario, (x, y) → (−y, x); 180°: (−x, −y); 90° horario: (y, −x). Resultado: {ans}.")


def t_rot_center(r, l):
    cx, cy = rp(r, 2), rp(r, 2)
    x, y = rp(r, 4), rp(r, 3)
    if (x, y) == (cx, cy) or x == cx or y == cy:
        raise Reject
    a = r.choice([90, 180, 270])
    rx, ry = rot((x, y), a, (cx, cy))
    if not fits([(rx, ry)]):
        raise Reject
    p = plot(); dot(p, x, y, "P"); dot(p, cx, cy, "C", -14, 16)
    ans = pt_(rx, ry)
    al = uq(ans, [pt_(*rot((x, y), a)), pt_(*rot((x, y), a + 180, (cx, cy))), pt_(*rot((x, y), 90 if a != 90 else 270, (cx, cy))), pt_(2 * cx - x, y), pt_(x + cx, y + cy)])
    stem = f"El punto P = {pt_(x, y)} se rota {ang_txt(a)} con centro en C = {pt_(cx, cy)}. ¿Cuáles son las coordenadas de P′?"
    return make(stem, p.svg("Punto P y centro C"), ans, al[:4], Q_RES, f"Se traslada el centro al origen: ({fs(x - cx)}, {fs(y - cy)}) gira y luego se suma C: {ans}.".replace("-", "−"))


def t_rot_angle(r, l):
    x, y = rp(r, 4), rp(r, 3)
    a = r.choice([90, 180, 270])
    rx, ry = rot((x, y), a)
    if not fits([(rx, ry)]) or abs(x) == abs(y):
        raise Reject
    p = plot(); dot(p, x, y, "P"); dot(p, rx, ry, "P′")
    ans = f"Rotación de {ang_txt(a)}"
    al = uq(ans, [f"Rotación de {ang_txt(b)}" for b in (90, 180, 270) if b != a] + ["Reflexión respecto del eje Y", "Reflexión respecto del eje X"])
    return make("El punto P′ es la imagen de P mediante una rotación con centro en el origen. ¿Cuál es esa rotación?", p.svg("Puntos P y P′"), ans, al[:4], Q_RES, "Se compara el giro que lleva P hasta P′ alrededor del origen.")


def t_two_rot(r, l):
    x, y = rp(r, 4), rp(r, 3)
    a, b = r.choice([90, 180, 270]), r.choice([90, 180, 270])
    tot = (a + b) % 360
    if tot == 0 or abs(x) == abs(y):
        raise Reject
    fx, fy = rot((x, y), tot)
    if not fits([(fx, fy)]):
        raise Reject
    p = plot(); dot(p, x, y, "P")
    ans = pt_(fx, fy)
    al = uq(ans, [pt_(*rot((x, y), a)), pt_(*rot((x, y), b)), pt_(*rot((x, y), tot + 180)), pt_(*rot((x, y), (a - b) % 360)), pt_(y, x), pt_(x, -y), pt_(-x, y), pt_(x + 1, y)])
    return make(f"El punto P = {pt_(x, y)} se rota {ang_txt(a)} y luego su imagen se rota {ang_txt(b)}, ambas veces con centro en el origen. ¿Dónde queda finalmente?", p.svg("Punto P"), ans, al[:4], Q_RES, f"Dos rotaciones con el mismo centro equivalen a una de {a}° + {b}° = {a + b}° antihorario en total (mod 360°).".replace("(mod 360°)", ""))


# ---------------------------------------------------------------- Modelar
def t_blades(r, l):
    n = r.choice([3, 4, 5, 6, 8, 9, 10, 12])
    step = 360 // n
    k = r.randint(2, n - 1)
    ans = f"{step * k}°"
    al = uq(ans, [f"{step}°", f"{360 - step * k + step}°", f"{n * k}°", f"{step * (k + 1)}°", f"{step * (k - 1)}°", f"{360 // k}°"])
    p = Plot(560, 300, -7, 7, -5, 5); 
    cx, cy = 280, 150
    body = ""
    for i in range(n):
        a = math.radians(-90 + 360 * i / n)
        body += L(cx, cy, cx + 105 * math.cos(a), cy + 105 * math.sin(a), NAVY, 6)
    body += C(cx, cy, 9, ACC)
    fig = wrap(560, 300, body, f"Molino con {n} aspas iguales")
    obj = r.choice(["molino de viento", "ventilador", "hélice"])
    stem = f"Un {obj} tiene {n} aspas iguales, distribuidas uniformemente alrededor del centro. ¿Cuántos grados debe girar para que cada aspa ocupe el lugar de la que está {k} posiciones más adelante?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Entre aspas consecutivas hay 360° : {n} = {step}°; para avanzar {k} posiciones: {k}·{step}° = {step * k}°.")


def t_clock(r, l):
    mins = r.choice([5, 10, 15, 20, 25, 40, 45, 50])
    ang = 6 * mins
    body = C(280, 150, 105, "#FFFFFF", NAVY, 4)
    for i in range(12):
        a = math.radians(-90 + 30 * i)
        body += L(280 + 92 * math.cos(a), 150 + 92 * math.sin(a), 280 + 104 * math.cos(a), 150 + 104 * math.sin(a), INK, 3)
    body += L(280, 150, 280, 65, ACC, 5) + C(280, 150, 7, INK)
    fig = wrap(560, 300, body, "Reloj con el minutero en las 12")
    ans = f"{ang}°"
    al = uq(ans, [f"{mins * 30}°", f"{360 - ang}°", f"{mins}°", f"{ang + 30}°", f"{ang * 2}°", f"{ang // 2}°"])
    return make(f"El minutero de un reloj marca las 12. ¿Cuántos grados gira (en sentido horario) al transcurrir {mins} minutos?", fig, ans, al[:4], Q_MOD, f"En 60 minutos gira 360°, es decir, 6° por minuto: {mins}·6° = {ang}°.")


def t_wheel(r, l):
    R = r.choice([3, 4, 5, 6])
    k = r.choice([90, 180, 270])
    x, y = R, 0
    rx, ry = rot((x, y), k)
    p = Plot(560, 340, -7, 7, -5, 5); p.axes(1, 1)
    p.parts.append(ELL(p.X(0), p.Y(0), p.X(R) - p.X(0), p.Y(0) - p.Y(R), "none", NAVY, 3))
    dot(p, x, y, "A")
    ans = pt_(rx, ry)
    al = uq(ans, [pt_(*rot((x, y), a)) for a in (90, 180, 270) if a != k] + [pt_(R, R), pt_(0, R + 1)])
    obj = r.choice(["una cabina de una rueda de la fortuna", "un asiento de un carrusel", "una pieza de una ruleta"])
    stem = f"Con centro en el origen, {obj} parte en A = ({R}, 0) y gira {ang_txt(k)}. ¿En qué coordenadas queda?"
    return make(stem, p.svg("Trayectoria circular y punto A"), ans, al[:4], Q_MOD, f"Rotación de {ang_txt(k)} del punto ({R}, 0): {ans}.")


def t_turns(r, l):
    turn = r.choice([90, 180, 270])
    n = r.randint(2, 7)
    tot = turn * n
    fin = tot % 360
    fig = card([f"Giro repetido de {ang_txt(turn)}", f"Se repite {n} veces", "Posición final respecto de la inicial = ?"], 150, 18)
    labs = {0: "Vuelve a la posición inicial", 90: "Queda girada 90° en sentido antihorario", 180: "Queda girada 180° respecto de la inicial", 270: "Queda girada 270° en sentido antihorario"}
    ans = labs[fin]
    al = [v for k_, v in labs.items() if k_ != fin]
    al.append(f"Queda girada {tot}° pero en sentido horario")
    return make(f"Una figura gira {ang_txt(turn)} respecto de su centro y el giro se repite {n} veces seguidas, siempre en el mismo sentido. ¿Cuál es su posición final?", fig, ans, al[:4], Q_MOD, f"Giro total: {n}·{turn}° = {tot}°, que equivale a {fin}° al quitar vueltas completas.")


# ---------------------------------------------------------------- Representar
def _pair(r):
    pts = tri_pts(r)
    a = r.choice([90, 180, 270])
    img = [rot(q, a) for q in pts]
    if not fits(img) or set(pts) & set(img):
        raise Reject
    p = plot(); draw_poly(p, pts, "ABC", FILL2); draw_poly(p, img, ["A′", "B′", "C′"], FILL3)
    return pts, img, a, p


def t_which_rot(r, l):
    pts, img, a, p = _pair(r)
    ans = f"Rotación de {ang_txt(a)}"
    al = uq(ans, [f"Rotación de {ang_txt(b)}" for b in (90, 180, 270) if b != a] + ["Reflexión respecto del eje X", "Reflexión respecto del eje Y"])
    return make("En la figura, A′B′C′ es la imagen de ABC mediante una rotación con centro en el origen. ¿Cuál es esa rotación?", p.svg("Triángulo ABC y su imagen"), ans, al[:4], Q_REP, "Se sigue el giro de un vértice alrededor del origen.")


def t_read_rot(r, l):
    pts, img, a, p = _pair(r)
    k = r.randrange(3)
    ans = pt_(*img[k])
    x, y = pts[k]
    al = uq(ans, [pt_(x, y), pt_(*rot(pts[k], a + 180)), pt_(*rot(pts[k], 270 if a == 90 else 90)), pt_(y, x), pt_(-x, y)])
    return make(f"El triángulo A′B′C′ es la imagen de ABC mediante una rotación. ¿Cuáles son las coordenadas del vértice {'ABC'[k]}′?", p.svg("Triángulo ABC y su imagen"), ans, al[:4], Q_REP, f"Se lee en el plano el vértice {'ABC'[k]}′: {ans}.")


def t_sym(r, l):
    n = r.choice([3, 4, 5, 6, 8, 9, 10, 12])
    star = l == 2 and r.random() < 0.5 and n >= 5
    outer = regular(280, 150, 110, n)
    if star:
        inner = regular(280, 150, 55, n, -90 + 180 / n)
        pts = [q for pair in zip(outer, inner) for q in pair]
    else:
        pts = outer
    fig = wrap(560, 300, P(pts, FILL2, NAVY, 3), f"Figura con {n} {'puntas' if star else 'lados'}")
    step = 360 // n
    ans = f"{step}°"
    al = uq(ans, [f"{step * 2}°", f"{180 // n if 180 % n == 0 else step + 10}°", f"{n}°", f"{360 - step}°", "180°"])
    what = f"estrella de {n} puntas iguales" if star else f"polígono regular de {n} lados"
    return make(f"La figura es un {what}. ¿Cuál es el menor ángulo positivo de rotación, con centro en su centro, que la deja exactamente igual?", fig, ans, al[:4], Q_REP, f"360° : {n} = {step}°.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Rotar A(2, 3) en 90° antihorario", "A′ = (3, −2)"], "Aplicó la regla de la rotación horaria: la antihoraria es (x, y) → (−y, x), luego A′ = (−3, 2)", \
            ["Intercambió las coordenadas sin cambiar ningún signo, lo que refleja respecto de y = x", "Cambió el signo de ambas coordenadas, que corresponde a una rotación de 180°", "Cambió el signo de la abscisa, que corresponde a reflejar respecto del eje Y", "Sumó 90 a cada coordenada del punto en lugar de aplicar la regla de giro"]
    if k == 1:
        return ["Rotar A(4, −1) en 180° respecto del origen", "A′ = (−4, −1)"], "Cambió el signo solo de x: una rotación de 180° cambia el signo de ambas coordenadas", \
            ["Cambió el signo solo de y, lo que corresponde a reflejar respecto del eje X", "Intercambió las coordenadas, lo que corresponde a reflejar respecto de y = x", "Rotó correctamente, pero olvidó anotar el apóstrofo en la imagen del punto", "Sumó 180 a la primera coordenada en lugar de aplicar la regla de la rotación"]
    if k == 2:
        return ["Un cuadrado se rota 90° respecto de su centro", "El área de la imagen es la mitad"], "Una rotación conserva el área: la imagen tiene la misma área que la figura original", \
            ["El área de la imagen es el doble porque el cuadrado gira dos veces sobre sí mismo", "El área depende del ángulo de giro: a mayor ángulo, mayor es el área de la imagen", "El área cambia solo si el centro de la rotación está fuera de la figura original", "El área se reduce porque los vértices se acercan al centro durante el giro realizado"]
    return ["Un triángulo equilátero", "Gira 90° y coincide consigo mismo"], "Su menor giro de coincidencia es 120°, no 90°: 360° : 3 = 120°", \
        ["Su menor giro de coincidencia es 60°, porque 360° dividido por 6 lados da 60°", "Su menor giro de coincidencia es 180°, como ocurre en toda figura simétrica", "Su menor giro de coincidencia es 90°, porque todas las figuras coinciden con 90°", "No coincide consigo mismo con ningún giro menor que 360° de rotación completa"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_prop(r, l):
    pts, img, a, p = _pair(r)
    ans = "Los lados y los ángulos de ambos triángulos son congruentes"
    al = ["Los lados de A′B′C′ son el doble de largos que los de ABC", "El perímetro de A′B′C′ cambia según el ángulo de rotación", "Los ángulos de A′B′C′ son distintos a los de ABC", "El área de A′B′C′ es distinta del área de ABC"]
    return make("El triángulo A′B′C′ es la imagen de ABC mediante una rotación. ¿Cuál afirmación es siempre verdadera?", p.svg("Triángulo ABC y su imagen"), ans, al, Q_ARG, "Toda isometría conserva longitudes, ángulos y áreas.")


TRUE = ["Una rotación conserva la medida de los lados de la figura", "Una rotación de 180° con centro en el origen transforma (x, y) en (−x, −y)", "Un cuadrado coincide consigo mismo al rotarlo 90° respecto de su centro",
        "El centro de una rotación permanece fijo", "Una rotación es una isometría", "Una rotación de 360° deja cualquier figura en su posición original"]
FALSE = ["Una rotación modifica el área de la figura que se gira", "Una rotación de 180° con centro en el origen transforma (x, y) en (y, x)", "Un triángulo equilátero coincide consigo mismo al rotarlo 90° respecto de su centro",
         "Todos los puntos de la figura se mantienen fijos al rotarla", "Una rotación cambia la forma de la figura", "Una rotación de 180° deja cualquier figura en su posición original"]


def _fig(r):
    pts = tri_pts(r); p = plot(); draw_poly(p, pts, "ABC", FILL2)
    return p.svg("Triángulo ABC")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre rotaciones es verdadera?", "Sobre rotaciones en el plano, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de las rotaciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre rotaciones es falsa?", "Sobre rotaciones en el plano, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las rotaciones.")


BY_SKILL = {
    Q_RES: [t_rot_pt, t_rot_center, t_rot_angle, t_two_rot],
    Q_MOD: [t_blades, t_clock, t_wheel, t_turns],
    Q_REP: [t_which_rot, t_read_rot, t_sym],
    Q_ARG: [t_error, t_prop, t_true, t_false],
}
