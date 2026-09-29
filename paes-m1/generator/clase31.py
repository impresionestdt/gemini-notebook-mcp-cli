"""Clase 31 (M1) · Ángulos y triángulos: ángulos entre paralelas y suma de ángulos."""
import itertools
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import par_transversal, tri_angles, _rel
from clase13 import co


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else str(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def deg(v):
    return f"{v}°"


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


QUAD = ["NW", "NE", "SW", "SE"]


def rel_value(rel, given):
    """Valor del segundo ángulo dada la relación (iguales o suplementarios)."""
    return given if rel in ("correspondientes", "alternos internos", "alternos externos", "vertical") else 180 - given


# ---------------------------------------------------------------- Resolver problemas
def t_angle_calc(r, l):
    kind = r.choice(["supp", "comp", "vert"] if l == 0 else ["supp", "comp", "xsupp", "xcomp", "tri3"])
    if kind in ("supp", "comp"):
        a = r.randint(15, 165 if kind == "supp" else 80)
        tot = 180 if kind == "supp" else 90
        name = "suplementarios" if kind == "supp" else "complementarios"
        val = tot - a
        stem = f"Dos ángulos son {name} y uno de ellos mide {a}°. ¿Cuánto mide el otro?"
        alts = [a, tot - a + 10, 360 - a, (180 - a) if kind == "comp" else 90 - a if a < 90 else a - 90, val + 5]
        fig = card([f"Ángulos {name}", f"suman {tot}°", f"Uno mide {a}°"], 150, 21)
        ex = f"{tot}° − {a}° = {val}°."
    elif kind == "vert":
        a = r.randint(20, 160)
        val = a
        stem = f"Dos rectas se cortan formando un ángulo de {a}°. ¿Cuánto mide el ángulo opuesto por el vértice?"
        alts = [180 - a, 360 - a, 90 - a if a < 90 else a - 90, a + 10, 180 + a]
        fig = card(["Dos rectas que se cortan", f"Un ángulo mide {a}°"], 130, 21)
        ex = "Los ángulos opuestos por el vértice son iguales."
    elif kind in ("xsupp", "xcomp"):
        tot = 180 if kind == "xsupp" else 90
        k = r.randint(2, 4)
        m = r.randint(0, 20)
        x = r.randint(10, (tot - m) // (k + 1))
        val = x
        stem = f"Dos ángulos {'suplementarios' if kind == 'xsupp' else 'complementarios'} miden x° y ({k}x + {m})°. ¿Cuánto vale x?" if False else f"Dos ángulos {'suplementarios' if kind == 'xsupp' else 'complementarios'} miden x y {k}x + {m} grados. ¿Cuánto vale x?"
        tot_eq = tot
        # x + kx + m = tot -> x = (tot - m)/(k+1)
        if (tot - m) % (k + 1):
            raise Reject
        val = (tot - m) // (k + 1)
        alts = [val + 5, val - 5, tot - m, F(tot, k + 1), val * 2]
        fig = card([f"x + ({k}x + {m}) = {tot}"], 110, 22)
        ex = f"{k + 1}x + {m} = {tot} ⟹ x = {val}."
    else:
        k = r.randint(2, 4)
        x = r.choice([d for d in range(10, 40) if 180 % (1 + k + (k + 1)) == 0] or [10])
        # ángulos x, kx, (k+1)x suman 180
        tot_c = 1 + k + (k + 1)
        if 180 % tot_c:
            raise Reject
        x = 180 // tot_c
        val = (k + 1) * x
        stem = f"Los ángulos de un triángulo miden x, {k}x y {k + 1}x grados. ¿Cuánto mide el mayor de los ángulos?"
        alts = [x, k * x, 180 - x, val + 10, F(180, k + 1)]
        fig = card([f"Ángulos: x, {k}x, {k + 1}x", "suman 180°"], 130, 21)
        ex = f"{tot_c}x = 180 ⟹ x = {x}; el mayor es {k + 1}x = {val}°."
    unit = "°" if kind not in ("xsupp", "xcomp") else ""
    ans = f"{val}{unit}"
    al = list(dict.fromkeys(f"{fs(F(a))}{unit}" for a in alts if F(a) > 0 and F(a) != val))
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_triangle(r, l):
    kind = r.choice(["third", "ext", "iso"] if l else ["third", "ext"])
    if kind == "third":
        a, b = r.randint(25, 90), r.randint(25, 90)
        if a + b >= 170:
            raise Reject
        fig = tri_angles({"A": deg(a), "B": deg(b), "C": "x"})
        val = 180 - a - b
        stem = "En el triángulo de la figura, ¿cuánto mide el ángulo x?"
        alts = [a + b, 360 - a - b, 180 - a, 90 - a, val + 10]
        ex = f"x = 180° − {a}° − {b}° = {val}°."
    elif kind == "ext":
        a, b = r.randint(25, 85), r.randint(25, 85)
        if a + b >= 170:
            raise Reject
        fig = tri_angles({"A": deg(a), "C": deg(b)}, ext="x")
        val = a + b
        stem = "En el triángulo de la figura, el ángulo x es exterior. ¿Cuánto mide x?"
        alts = [180 - a - b, 180 - a, 180 - b, 360 - a - b, val + 10]
        ex = f"El ángulo exterior es la suma de los dos interiores no adyacentes: {a}° + {b}° = {val}°."
    else:
        a = r.randint(30, 80)
        fig = tri_angles({"A": "x", "B": "x", "C": deg(a)})
        if a % 2:
            raise Reject
        val = (180 - a) // 2
        stem = f"El triángulo de la figura es isósceles con ángulos basales iguales (x). ¿Cuánto mide x?"
        alts = [180 - a, a, F(180 - a, 3), 90 - a, val + 10]
        ex = f"2x + {a}° = 180° ⟹ x = {val}°."
    ans = f"{val}°"
    al = list(dict.fromkeys(f"{fs(F(v))}°" for v in alts if F(v) > 0 and F(v) != val))
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_parallel(r, l):
    """L1 ∥ L2: un ángulo dado; hallar otro."""
    q1, q2 = r.sample(QUAD, 2)
    ln1, ln2 = r.choice([("U", "D"), ("D", "U")])
    rel = _rel(ln1, q1, ln2, q2)
    a = r.choice([40, 50, 55, 65, 70, 75, 110, 115, 125, 130, 140])
    val = rel_value(rel, a)
    labels = {(ln1, q1): f"{a}°", (ln2, q2): "x"}
    fig = par_transversal(labels)
    if l >= 1 and r.random() < 0.5:
        k = r.choice([2, 3])
        # x dado por kx
        if val % k:
            raise Reject
        labels = {(ln1, q1): f"{a}°", (ln2, q2): f"{k}x"}
        fig = par_transversal(labels)
        stem = f"En la figura, L₁ ∥ L₂. Si un ángulo mide {a}° y el otro mide {k}x, ¿cuánto vale x?"
        res = F(val, k)
        ans = fs(res)
        alts = [F(180 - val, k), val, F(a, k), res + 10, F(val, 1) + k]
        return make(stem, fig, ans, pick4(ans, uq(ans, [fs(F(x)) for x in alts if F(x) > 0])), Q_RES, f"Son {rel}: {k}x = {val}° ⟹ x = {fs(res)}.")
    stem = f"En la figura, las rectas L₁ y L₂ son paralelas. Si un ángulo mide {a}°, ¿cuánto mide el ángulo x?"
    ans = deg(val)
    alts = [deg(a if val != a else 180 - a), deg(180 - val if val != 180 - val else 90), deg(90 - a if a < 90 else a - 90), deg(val + 10), deg(360 - a)]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_RES, f"Son ángulos {rel}: {'iguales' if val == a else 'suplementarios'}, luego x = {val}°.")


# ---------------------------------------------------------------- Modelar
def t_clock(r, l):
    h = r.randint(1, 11)
    kind = r.choice(["o", "h"]) if l else "o"
    if kind == "o":
        ang = min(30 * h, 360 - 30 * h)
        stem = f"A las {h}:00 horas, ¿qué ángulo forman las manecillas de un reloj? (Se considera el menor ángulo.)"
        alts = [30 * h if 30 * h != ang else 360 - ang, 6 * h, 12 * h, 15 * h, ang + 30]
    else:
        ang = abs(30 * h + 15 - 180) if False else abs(180 - (30 * h + 15)) if (30 * h + 15) <= 360 else 0
        m_hand = 180
        h_hand = 30 * h + 15
        ang = abs(m_hand - h_hand)
        ang = min(ang, 360 - ang)
        stem = f"A las {h}:30 horas, ¿qué ángulo forman las manecillas de un reloj? (El horario avanza 0,5° cada minuto.)"
        alts = [abs(180 - 30 * h), 30 * h, ang + 15, ang - 15 if ang > 15 else ang + 30, 6 * h]
    ans = deg(ang)
    al = list(dict.fromkeys(deg(int(a)) for a in alts if int(a) > 0 and int(a) != ang))
    fig = card([f"Reloj analógico", f"Hora: {h}:{'00' if kind == 'o' else '30'}", "Cada hora = 30°"], 150, 20)
    return make(stem, fig, ans, al[:4], Q_MOD, f"Cada número del reloj equivale a 30°; el ángulo pedido es {ang}°.")


def t_ladder(r, l):
    a = r.randint(55, 80)
    kind = r.choice(["wall", "ext"])
    body = L(80, 220, 480, 220, INK, 4) + L(80, 220, 80, 30, INK, 4) + L(80, 60, 280, 220, ACC, 5) + tag(205, 200, f"{a}°" if kind == "wall" else "?", 16) + tag(120, 100, "?" if kind == "wall" else f"{a}°", 16)
    fig = wrap(560, 250, body, "Escalera apoyada en un muro")
    if kind == "wall":
        stem = f"Una escalera apoyada en un muro vertical forma un ángulo de {a}° con el suelo (que es horizontal). ¿Qué ángulo forma la escalera con el muro?"
        val = 90 - a
        alts = [a, 180 - a, 90 + a, a - 45, val + 10]
    else:
        stem = f"Una escalera apoyada en un muro vertical forma un ángulo de {a}° con el muro. ¿Qué ángulo forma la escalera con el suelo horizontal?"
        val = 90 - a
        alts = [a, 180 - a, 90 + a, a + 10, val + 10]
    ans = deg(val)
    al = list(dict.fromkeys(deg(x) for x in alts if x > 0 and x != val))
    return make(stem, fig, ans, al[:4], Q_MOD, "Muro y suelo forman 90°: los dos ángulos de la escalera son complementarios.")


def t_roof(r, l):
    a = r.randint(20, 40)
    b = r.randint(20, 40)
    c = 180 - 2 * a if False else 180 - a - b
    fig = tri_angles({"A": deg(a), "B": deg(b), "C": "x"}, names=("P", "Q", "R"))
    ctx = r.choice(["El frontón triangular de una casa", "La cercha triangular de un techo", "Un cartel triangular"])
    stem = f"{ctx} tiene dos ángulos de {a}° y {b}°. ¿Cuánto mide el tercer ángulo?"
    ans = deg(c)
    alts = [a + b, 180 - a, 180 - b, 360 - a - b, c + 10]
    al = list(dict.fromkeys(deg(x) for x in alts if x > 0 and x != c))
    return make(stem, fig, ans, al[:4], Q_MOD, f"La suma de los ángulos de un triángulo es 180°: 180° − {a}° − {b}° = {c}°.")


# ---------------------------------------------------------------- Representar
RELS = ["correspondientes", "alternos internos", "alternos externos", "conjugados internos", "conjugados externos", "vertical", "adyacentes"]
REL_TXT = {"correspondientes": "Correspondientes: son iguales", "alternos internos": "Alternos internos: son iguales", "alternos externos": "Alternos externos: son iguales",
           "conjugados internos": "Conjugados internos: suman 180°", "conjugados externos": "Conjugados externos: suman 180°", "vertical": "Opuestos por el vértice: son iguales", "adyacentes": "Adyacentes: suman 180°"}


def t_relation(r, l):
    for _ in range(50):
        l1, l2 = r.choice(["U", "D"]), r.choice(["U", "D"])
        q1, q2 = r.sample(QUAD, 2) if l1 == l2 else (r.choice(QUAD), r.choice(QUAD))
        if (l1, q1) != (l2, q2):
            break
    rel = _rel(l1, q1, l2, q2)
    labels = {(l1, q1): "α", (l2, q2): "β"}
    fig = par_transversal(labels)
    ans = REL_TXT[rel]
    others = [REL_TXT[x] for x in RELS if x != rel]
    r.shuffle(others)
    stem = "En la figura, L₁ ∥ L₂. ¿Qué relación hay entre los ángulos α y β?"
    return make(stem, fig, ans, others[:4], Q_REP, f"α y β son ángulos {rel}.")


def t_sum_relation(r, l):
    a = r.choice([35, 45, 50, 60, 65, 72, 115, 125, 132])
    l1, l2 = r.choice(["U", "D"]), r.choice(["U", "D"])
    q1, q2 = r.choice(QUAD), r.choice(QUAD)
    if (l1, q1) == (l2, q2):
        raise Reject
    rel = _rel(l1, q1, l2, q2)
    val = rel_value(rel, a)
    fig = par_transversal({(l1, q1): f"{a}°", (l2, q2): "β"})
    stem = "En la figura, L₁ ∥ L₂. ¿Cuánto mide el ángulo β?"
    ans = deg(val)
    alts = [deg(180 - val if val != 90 else 100), deg(a if a != val else 180 - a), deg(90 - a if a < 90 else a - 90), deg(val + 10), deg(360 - a)]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_REP, f"Los ángulos son {rel}: {'iguales' if val == a else 'suplementarios'}.")


def t_tri_read(r, l):
    a, b = r.randint(30, 80), r.randint(30, 80)
    if a + b >= 165:
        raise Reject
    kind = r.choice(["int", "ext"])
    if kind == "int":
        fig = tri_angles({"A": deg(a), "B": f"{b}°"}, names=("A", "B", "C"))
        fig = tri_angles({"A": deg(a), "B": deg(b), "C": "x"})
        val = 180 - a - b
        stem = "¿Cuál es el valor de x en el triángulo de la figura?"
    else:
        fig = tri_angles({"A": deg(a), "C": deg(b)}, ext="x")
        val = a + b
        stem = "En el triángulo de la figura, ¿cuánto mide el ángulo exterior x?"
    ans = deg(val)
    alts = [deg(180 - val), deg(a + b if kind == "int" else 180 - a - b), deg(360 - val), deg(a), deg(val + 10)]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_REP, "La suma de los ángulos interiores es 180° y el ángulo exterior es la suma de los dos interiores no adyacentes.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a = r.randint(30, 70)
    if k == 0:
        return [f"Ángulos alternos internos entre paralelas", f"Uno mide {a}°; el otro mide {180 - a}°"], "Los ángulos alternos internos entre paralelas son iguales; los que suman 180° son los conjugados internos", \
            ["Los alternos internos suman 360° porque están en lados distintos de la transversal", "Los alternos internos son complementarios, es decir, suman 90° entre ambos", "Los alternos internos son iguales solo si la transversal es perpendicular a las paralelas", "Los alternos internos no guardan ninguna relación entre las medidas de sus ángulos"]
    if k == 1:
        return [f"Dos ángulos son complementarios y uno mide {a}°", f"El otro mide {180 - a}°"], "Los ángulos complementarios suman 90°, no 180°: el otro mide 90° − a", \
            ["Los ángulos complementarios son los que suman 360° alrededor de un mismo punto", "Los ángulos complementarios son iguales entre sí, por lo que el otro también mide igual", "Los ángulos complementarios suman 180° y el error está en la resta realizada", "Los ángulos complementarios se restan en lugar de sumarse para hallar el otro"]
    if k == 2:
        return [f"Triángulo con ángulos {a}°, {a + 10}° y 90°", "«Existe, porque hay un ángulo recto»"], f"Los ángulos suman {2 * a + 100}°, distinto de 180°: no puede ser un triángulo", \
            ["Existe siempre que uno de los ángulos sea recto, sin importar la suma total", "Existe porque los otros dos ángulos son agudos y distintos entre sí", "No existe porque un triángulo no puede tener un ángulo recto ni obtuso", "Existe porque la suma de dos de sus ángulos es menor que 180°"]
    return [f"Ángulo exterior de un triángulo = {a}°", f"Ángulos interiores no adyacentes: {a}° y {a}°"], f"El ángulo exterior es igual a la suma de los interiores no adyacentes: sería {2 * a}°, no {a}°", \
        ["El ángulo exterior es igual a uno solo de los ángulos interiores no adyacentes", "El ángulo exterior es igual a la diferencia de los interiores no adyacentes", "El ángulo exterior es suplementario de la suma de todos los interiores", "El ángulo exterior mide siempre 90° en cualquier triángulo cualquiera"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Afirmación de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la afirmación de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_exists(r, l):
    a, b, c = r.choice([(60, 60, 60), (90, 45, 45), (100, 40, 40), (70, 50, 60), (110, 35, 35), (30, 30, 120)]), None, None
    a, b, c = a
    ok = r.random() < 0.5
    if not ok:
        c += r.choice([10, 20, -10, 15])
        if a + b + c == 180:
            raise Reject
    fig = card([f"Ángulos: {a}°, {b}° y {c}°"], 110, 24)
    stem = f"Un estudiante afirma que existe un triángulo con ángulos interiores de {a}°, {b}° y {c}°. ¿Es correcta su afirmación?"
    if ok:
        ans = "Sí, porque los tres ángulos suman 180°"
        alts = ["No, porque un triángulo no puede tener un ángulo mayor que 90°", "No, porque los tres ángulos deben ser iguales entre sí", "Sí, porque cada uno de los ángulos es menor que 180°", "No, porque los tres ángulos deben sumar 360°"]
    else:
        tot = a + b + c
        ans = f"No, porque los tres ángulos suman {tot}° y deben sumar 180°"
        alts = ["Sí, porque cada uno de los ángulos es menor que 180°", "Sí, porque los ángulos son todos positivos y menores que 180°", f"No, porque los tres ángulos deben sumar 360° y suman {tot}°", "Sí, porque dos de los ángulos suman menos de 180°"]
    return make(stem, fig, ans, alts, Q_ARG, "La suma de los ángulos interiores de un triángulo es siempre 180°.")


TRUE = ["Los ángulos opuestos por el vértice son iguales", "Los ángulos alternos internos entre paralelas son iguales", "Los ángulos conjugados internos entre paralelas suman 180°",
        "Los ángulos interiores de un triángulo suman 180°", "Un ángulo exterior de un triángulo es igual a la suma de los dos interiores no adyacentes", "Los ángulos basales de un triángulo isósceles son iguales"]
FALSE = ["Los ángulos alternos internos entre paralelas suman 180°", "Los ángulos conjugados internos entre paralelas son iguales", "Los ángulos interiores de un triángulo suman 360°",
         "Los ángulos complementarios suman 180°", "Un ángulo exterior de un triángulo es igual a un ángulo interior cualquiera", "Los ángulos correspondientes entre paralelas suman 90°"]


def _fig(r):
    return par_transversal({("U", "SE"): "α", ("D", "NE"): "β"})


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ángulos es verdadera?", "Sobre ángulos entre paralelas y en triángulos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de ángulos entre paralelas y de triángulos.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre ángulos es falsa?", "Sobre ángulos entre paralelas y en triángulos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de los ángulos.")


BY_SKILL = {
    Q_RES: [t_angle_calc, t_triangle, t_parallel],
    Q_MOD: [t_clock, t_ladder, t_roof],
    Q_REP: [t_relation, t_sum_relation, t_tri_read],
    Q_ARG: [t_error, t_exists, t_true, t_false],
}
