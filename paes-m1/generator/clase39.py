"""Clase 39 (M1) · Semejanza de figuras y triángulos."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase35 import _lt, _alts
from num import dstr
import geo
import viz

RATIOS = [(2, 1), (3, 1), (3, 2), (4, 1), (5, 2), (4, 3), (5, 3)]


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is not None and a not in seen:
            seen.add(a); out.append(a)
    return out


def rt(p, q):
    return f"{p} : {q}"


def tri_sides(r, q, lo=2, hi=7):
    while True:
        s = sorted(r.randint(lo, hi) * q for _ in range(3))
        if s[0] + s[1] > s[2]:
            r.shuffle(s)
            return s


# ---------------------------------------------------------------- Resolver problemas
def t_side(r, l):
    p, q = r.choice(RATIOS if l else RATIOS[:3])
    s = tri_sides(r, q)
    big = [x // q * p for x in s]
    unk_big = r.random() < 0.6
    i = r.randrange(3)
    u = r.choice(["cm", "m"])
    keys = ["base", "left", "right"]
    sm = {k: f"{x}" for k, x in zip(keys, s)}
    bg = {k: f"{x}" for k, x in zip(keys, big)}
    if unk_big:
        bg[keys[i]] = "x"; val = big[i]; other = s[i]
    else:
        sm[keys[i]] = "x"; val = s[i]; other = big[i]
    fig = geo.sim_tris(F(p, q), sm, bg)
    ans = f"{val} {u}"
    d = abs(big[i] - s[i])
    al = uq(ans, [f"{other} {u}", f"{s[i] + d if unk_big else max(1, big[i] - d)} {u}", f"{val + q} {u}", f"{val * 2} {u}", f"{val + 2} {u}", f"{max(1, val - 2)} {u}"])
    return make(f"Los dos triángulos de la figura son semejantes (medidas en {u}). ¿Cuál es el valor de x?", fig, ans, al[:4], Q_RES, f"La razón de semejanza es {p} : {q}; se aplica al lado correspondiente: x = {val} {u}.")


def t_perim_area(r, l):
    p, q = r.choice([(2, 1), (3, 1), (3, 2), (4, 1), (5, 2)])
    kind = r.choice(["per", "area"])
    if kind == "per":
        P0 = q * r.randint(4, 12)
        val = P0 // q * p
        stem = f"Dos triángulos semejantes tienen razón de semejanza {p} : {q} (grande : pequeño). Si el perímetro del pequeño es {P0} cm, ¿cuál es el perímetro del grande?"
        ans = f"{val} cm"
        al = uq(ans, [f"{P0 * p * p // (q * q) if (P0 * p * p) % (q * q) == 0 else val + 7} cm", f"{P0 + p - q} cm", f"{P0 * p} cm", f"{val + p} cm", f"{P0 // q * (p + q)} cm"])
        ex = f"El perímetro se multiplica por la razón de semejanza {p}/{q}: {val} cm."
    else:
        A0 = q * q * r.randint(2, 9)
        val = A0 // (q * q) * p * p
        stem = f"Dos figuras semejantes tienen razón de semejanza {p} : {q} (grande : pequeña). Si el área de la pequeña es {A0} cm², ¿cuál es el área de la grande?"
        ans = f"{val} cm²"
        al = uq(ans, [f"{A0 // q * p} cm²" if A0 % q == 0 else f"{val + 5} cm²", f"{A0 + p * p - q * q} cm²", f"{A0 * p} cm²", f"{val + p} cm²", f"{A0 // (q * q) * p * p * 2} cm²"])
        ex = f"El área se multiplica por el cuadrado de la razón: ({p}/{q})² → {val} cm²."
    fig = card([f"Razón de semejanza: {p} : {q}", "Figura grande : figura pequeña", "Dato: " + (f"perímetro pequeño = {P0} cm" if kind == "per" else f"área pequeña = {A0} cm²")], 150, 18)
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_squares(r, l):
    k = r.choice([2, 3, 4, 5])
    a = r.randint(2, 9)
    kind = r.choice(["area", "per"])
    fig = geo.two_squares(k, f"lado {a} cm", f"lado {k * a} cm")
    if kind == "area":
        ans = f"{k * k} veces el área del menor"
        al = [f"{k} veces el área del menor", f"{2 * k} veces el área del menor", f"{k + 1} veces el área del menor", f"{k * k * k} veces el área del menor"]
        stem = "El lado del cuadrado mayor mide " + f"{k} veces el del menor. ¿Cuántas veces mayor es su área?".replace("¿Cuántas veces mayor es su área?", "¿Cómo es su área comparada con la del menor?")
        ex = f"El área varía con el cuadrado de la razón: {k}² = {k * k}."
    else:
        ans = f"{k} veces el perímetro del menor"
        al = [f"{k * k} veces el perímetro del menor", f"{2 * k} veces el perímetro del menor", f"{k + 1} veces el perímetro del menor", f"{k * k * k} veces el perímetro del menor"]
        stem = f"El lado del cuadrado mayor mide {k} veces el del menor. ¿Cómo es su perímetro comparado con el del menor?"
        ex = f"El perímetro varía linealmente con la razón: {k} veces."
    return make(stem, fig, ans, al, Q_RES, ex)


def t_tri_prop(r, l):
    p, q = r.choice(RATIOS)
    s = tri_sides(r, q)
    big = [x // q * p for x in s]
    fig = geo.sim_tris(F(p, q), {"base": f"{s[0]}", "left": f"{s[1]}", "right": f"{s[2]}"}, {"base": f"{big[0]}", "left": "?", "right": f"{big[2]}"})
    val = big[1]
    ans = f"{val} cm"
    al = uq(ans, [f"{s[1]} cm", f"{s[1] + big[0] - s[0]} cm", f"{val + 2} cm", f"{val * 2} cm", f"{max(1, val - 3)} cm"])
    return make(f"Los triángulos de la figura son semejantes (medidas en cm) y los lados se corresponden en el mismo orden. ¿Cuánto mide el lado marcado con «?»", fig, ans, al[:4], Q_RES, f"Razón {p} : {q}: {s[1]}·{p}/{q} = {val} cm.")


# ---------------------------------------------------------------- Modelar
def _shadow_fig(h, s, H, S, unk):
    body = L(30, 240, 530, 240, INK, 3)
    x0 = 80
    body += P([(x0, 240), (x0 + 70, 240), (x0, 240 - 60)], FILL, NAVY, 3) + L(x0, 240, x0, 180, ACC, 5)
    X0 = 300
    body += P([(X0, 240), (X0 + 190, 240), (X0, 240 - 160)], FILL2, NAVY, 3) + L(X0, 240, X0, 80, ACC, 5)
    body += tag(x0 - 40, 210, h, 15) + tag(x0 + 35, 264, s, 15) + tag(X0 - 44, 160, H, 15) + tag(X0 + 95, 264, S, 15)
    return wrap(560, 285, body, "Sombras de dos objetos")


def t_shadow(r, l):
    h100 = r.choice([120, 150, 160, 180])
    s100 = r.choice([60, 80, 90, 100, 120, 150])
    k = r.randint(4, 15)
    S = F(s100 * k, 100)
    H = F(h100 * k, 100)
    hm, sm = F(h100, 100), F(s100, 100)
    ans = _lt(H, " m"); 
    if ans is None or S.denominator not in (1, 2, 4, 5, 10, 20, 25, 50, 100):
        raise Reject
    Hs, Ss = _lt(H, ""), _lt(S, "")
    if Ss is None:
        raise Reject
    obj = r.choice(["un árbol", "un poste", "un edificio"])
    fig = _shadow_fig(f"{_lt(hm, '')} m", f"{_lt(sm, '')} m", "H", f"{Ss} m", True)
    al = _alts([H + (S - sm), H / 2, S * hm, H * 2, H + 1, sm / hm * S], " m", ans)
    stem = f"En un mismo instante, una persona de {_lt(hm, '')} m de estatura proyecta una sombra de {_lt(sm, '')} m y {obj} proyecta una sombra de {Ss} m. ¿Cuál es la altura de {obj}?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Los triángulos son semejantes: H/{Ss} = {_lt(hm, '')}/{_lt(sm, '')}, luego H = {Hs} m.")


def t_map(r, l):
    N = r.choice([1000, 2000, 5000, 10000, 20000, 25000, 50000, 100000])
    d = r.randint(2, 12)
    cm = d * N
    real_m = F(cm, 100)
    if real_m >= 1000:
        ans_v, u = real_m / 1000, " km"
    else:
        ans_v, u = real_m, " m"
    ans = _lt(ans_v, u)
    if ans is None:
        raise Reject
    fig = card([f"Escala del mapa: 1 : {N:,}".replace(",", "."), f"Distancia en el mapa: {d} cm", "Distancia real = ?"], 150, 19)
    al = _alts([ans_v * 10, ans_v / 10, ans_v * 100, F(d * N, 1000) if u == " m" else F(d * N, 1000000), ans_v + d], u, ans)
    stem = f"Un mapa está a escala 1 : {N:,}. Dos ciudades están a {d} cm en el mapa. ¿Cuál es la distancia real entre ellas?".replace(",", ".")
    return make(stem, fig, ans, al[:4], Q_MOD, f"{d} cm · {N:,} = {cm:,} cm = {_lt(ans_v, u)}.".replace(",", "."))


def t_photo(r, l):
    w, h = r.choice([(10, 15), (12, 18), (15, 20), (9, 12), (10, 14), (20, 30)])
    k = F(r.choice([2, 3, 4, 5, 3, 6]), 1)
    nw = w * k
    nh = h * k
    kind = r.choice(["w", "h"])
    if kind == "w":
        stem = f"Una fotografía de {w} cm × {h} cm se amplía manteniendo sus proporciones, de modo que su ancho pasa a ser {fs(nw)} cm. ¿Cuánto mide el nuevo alto?"
        val = nh; other = h; wrong = nh - nw + w
    else:
        stem = f"Una fotografía de {w} cm × {h} cm se amplía manteniendo sus proporciones, de modo que su alto pasa a ser {fs(nh)} cm. ¿Cuánto mide el nuevo ancho?"
        val = nw; other = w; wrong = nw - nh + h
    ans = f"{fs(val)} cm"
    al = uq(ans, [f"{fs(wrong)} cm" if wrong > 0 else None, f"{fs(other)} cm", f"{fs(val + 2)} cm", f"{fs(val * 2)} cm", f"{fs(val - 2)} cm", f"{fs(val + k)} cm"])
    fig = card([f"Original: {w} cm × {h} cm", f"Ampliación: {fs(nw)} cm × ?" if kind == "w" else f"Ampliación: ? × {fs(nh)} cm", "Se mantienen las proporciones"], 150, 18)
    return make(stem, fig, ans, al[:4], Q_MOD, f"Las razones se conservan: el factor de ampliación es {fs(k)}.")


def t_model_pool(r, l):
    a, b = r.choice([(2, 3), (3, 4), (2, 5), (3, 5)])
    m = r.randint(3, 9)
    L_ = F(m * a * 10, 1)
    real = F(a * m * 100, 100)
    scale = r.choice([20, 25, 50, 100])
    mlen = r.randint(8, 30)
    real_cm = mlen * scale
    fig = card([f"Maqueta a escala 1 : {scale}", f"Largo de la maqueta: {mlen} cm", "Largo real del edificio = ?"], 150, 19)
    real_m = F(real_cm, 100)
    ans = _lt(real_m, " m")
    if ans is None:
        raise Reject
    al = _alts([real_m * 10, real_m / 10, F(mlen, scale), mlen + scale, real_m * 2], " m", ans)
    return make(f"Una maqueta de un edificio está a escala 1 : {scale}. Si el largo de la maqueta es {mlen} cm, ¿cuál es el largo real del edificio?", fig, ans, al[:4], Q_MOD, f"{mlen}·{scale} = {real_cm} cm = {_lt(real_m, ' m')}.")


# ---------------------------------------------------------------- Representar
def t_read_sim(r, l):
    p, q = r.choice(RATIOS)
    s = tri_sides(r, q)
    big = [x // q * p for x in s]
    keys = ["base", "left", "right"]
    fig = geo.sim_tris(F(p, q), {k: f"{x}" for k, x in zip(keys, s)}, {k: f"{x}" for k, x in zip(keys, big)}, ttl=("Menor", "Mayor"))
    ans = rt(p, q)
    al = uq(ans, [rt(q, p), rt(p * p, q * q), rt(p - q, q), rt(p + 1, q), rt(p, q + 1), rt(p * 2, q)])
    return make("Los dos triángulos de la figura son semejantes. ¿Cuál es la razón de semejanza del triángulo mayor al menor?", fig, ans, al[:4], Q_REP, f"Se dividen lados correspondientes: {big[0]}/{s[0]} = {p}/{q}.")


def t_expr(r, l):
    a, b, c, d, e, f = r.choice([("a", "b", "c", "d", "e", "f"), ("p", "q", "r", "x", "y", "z"), ("m", "n", "s", "u", "v", "w")])
    fig = geo.sim_tris(2, {"base": a, "left": b, "right": c}, {"base": d, "left": e, "right": f}, ttl=("Menor", "Mayor"))
    ans = f"{a}/{d} = {b}/{e} = {c}/{f}"
    al = [f"{a}/{d} = {b}/{f} = {c}/{e}", f"{a}/{e} = {b}/{d} = {c}/{f}", f"{a}·{d} = {b}·{e} = {c}·{f}", f"{a}/{b} = {d}/{f} = {c}/{e}", f"{a} + {d} = {b} + {e} = {c} + {f}"]
    return make("Los triángulos de la figura son semejantes y sus lados se corresponden por posición (base con base, izquierdo con izquierdo, derecho con derecho). ¿Qué proporción es correcta?", fig, ans, al[:4], Q_REP, "Los lados correspondientes están en la misma razón.")


def t_table(r, l):
    p, q = r.choice(RATIOS)
    s = tri_sides(r, q)
    big = [x // q * p for x in s]
    i = r.randrange(3)
    rows = [["Figura menor"] + [str(x) for x in s], ["Figura mayor"] + [str(x) if j != i else "?" for j, x in enumerate(big)]]
    fig = viz.table_fig(["Lado", "1.º", "2.º", "3.º"], rows)
    ans = str(big[i])
    al = uq(ans, [str(s[i]), str(s[i] + big[(i + 1) % 3] - s[(i + 1) % 3]), str(big[i] + 2), str(big[i] * 2), str(max(1, big[i] - 3))])
    return make("La tabla muestra los lados correspondientes de dos triángulos semejantes. ¿Qué número corresponde a «?»", fig, ans, al[:4], Q_REP, f"Razón {p}/{q}: {s[i]}·{p}/{q} = {big[i]}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Triángulos semejantes, lados 3, 4, 5 y x, 8, 10", "La diferencia 8 − 4 = 4, luego x = 3 + 4 = 7"], "Usó una diferencia aditiva: debía usar la razón, 8 : 4 = 2, luego x = 3·2 = 6", \
            ["Usó bien la razón de semejanza, pero cometió un error al multiplicar los valores", "Igualó x con el lado correspondiente del segundo triángulo sin usar la razón", "Aplicó la razón de semejanza a un lado que no es correspondiente al buscado", "Dividió 3 por la razón en lugar de multiplicarlo por ella al hallar el valor de x"]
    if k == 1:
        return ["Razón de semejanza 2 : 1; área menor 5 cm²", "Área mayor = 5·2 = 10 cm²"], "Multiplicó por la razón: las áreas se relacionan con el cuadrado, 5·2² = 20 cm²", \
            ["Sumó la razón al área menor en lugar de multiplicarla por la razón de semejanza", "Dividió el área menor por la razón en vez de multiplicarla por su cuadrado", "Multiplicó por la razón al cubo, como si se tratara de volúmenes de cuerpos", "Calculó bien el área mayor, pero se equivocó al escribir la unidad de medida"]
    if k == 2:
        return ["Un rectángulo de 2 × 3 y otro de 4 × 9", "Son semejantes porque ambos son rectángulos"], "Ser rectángulos no basta: 4/2 = 2 pero 9/3 = 3, los lados no son proporcionales", \
            ["Son semejantes porque los lados son proporcionales con razón constante entre ellos", "No son semejantes porque tienen distinto perímetro y distinta área entre sí", "No son semejantes porque los ángulos de un rectángulo cambian al ampliarlo", "Son semejantes porque los dos rectángulos tienen los ángulos rectos de 90° cada uno"]
    return ["Triángulo A: ángulos 40° y 60°", "Triángulo B: ángulos 60° y 80° → no son semejantes"], "Sí son semejantes (AA): el tercer ángulo de A es 80° y el de B es 40°, por lo que hay tres ángulos iguales", \
        ["No lo son, porque las medidas de los ángulos deben ser exactamente las mismas en ambos", "Sí lo son, porque ambos triángulos tienen un ángulo de 60° y con eso basta", "No lo son, porque para ser semejantes deben tener lados de igual longitud", "Sí lo son, porque la suma de los ángulos de cada triángulo es 180° en ambos casos"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_crit(r, l):
    kind = r.choice(["AA", "LLL", "LAL", "no"])
    OPT = ["Sí, por criterio AA", "Sí, por criterio LLL", "Sí, por criterio LAL", "No son semejantes"]
    if kind == "AA":
        a, b = r.choice([(40, 60), (50, 70), (30, 80), (45, 65), (35, 75)])
        c = 180 - a - b
        lines = [f"Triángulo 1: ángulos de {a}° y {b}°", f"Triángulo 2: ángulos de {b}° y {c}°"]
        ans = OPT[0]
    elif kind == "LLL":
        k = r.choice([2, 3])
        s = tri_sides(r, 1, 3, 8)
        lines = ["Triángulo 1: lados " + ", ".join(map(str, s)) + " cm", "Triángulo 2: lados " + ", ".join(str(k * x) for x in s) + " cm"]
        ans = OPT[1]
    elif kind == "LAL":
        k = r.choice([2, 3])
        a, b = r.randint(3, 8), r.randint(4, 9)
        ang = r.choice([40, 50, 60, 70])
        lines = [f"Triángulo 1: lados {a} y {b} cm, ángulo entre ellos {ang}°", f"Triángulo 2: lados {k * a} y {k * b} cm, ángulo entre ellos {ang}°"]
        ans = OPT[2]
    else:
        a, b = r.choice([(40, 60), (50, 70), (30, 80)])
        lines = [f"Triángulo 1: ángulos de {a}° y {b}°", f"Triángulo 2: ángulos de {a + 10}° y {b}°"]
        ans = OPT[3]
    fig = card(["Datos de dos triángulos:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    al = [o for o in OPT if o != ans] + ["Son congruentes, pero no semejantes"]
    return make("Con los datos de la figura, ¿son semejantes los dos triángulos y por qué?", fig, ans, al[:4], Q_ARG, "Se aplica el criterio de semejanza que corresponde a los datos disponibles.")


TRUE = ["Dos figuras semejantes tienen la misma forma y sus lados correspondientes son proporcionales", "Si la razón de semejanza es k, la razón entre las áreas es k²", "Dos triángulos con dos ángulos respectivamente iguales son semejantes",
        "Todos los cuadrados son semejantes entre sí", "Dos figuras congruentes son semejantes con razón 1", "Si la razón de semejanza es k, la razón entre los perímetros es k"]
FALSE = ["Dos figuras semejantes tienen siempre el mismo tamaño", "Si la razón de semejanza es k, la razón entre las áreas es k", "Dos rectángulos cualesquiera son siempre semejantes entre sí",
         "Dos triángulos con un solo ángulo igual siempre son semejantes", "Dos figuras semejantes tienen ángulos correspondientes distintos", "Si la razón de semejanza es k, la razón entre los perímetros es k²"]


def _fig(r):
    return geo.sim_tris(2, {"base": "", "left": "", "right": ""}, {"base": "", "left": "", "right": ""})


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre semejanza es verdadera?", "Sobre semejanza de figuras, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de la semejanza.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre semejanza es falsa?", "Sobre semejanza de figuras, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de la semejanza.")


BY_SKILL = {
    Q_RES: [t_side, t_perim_area, t_squares, t_tri_prop],
    Q_MOD: [t_shadow, t_map, t_photo, t_model_pool],
    Q_REP: [t_read_sim, t_expr, t_table],
    Q_ARG: [t_error, t_crit, t_true, t_false],
}
