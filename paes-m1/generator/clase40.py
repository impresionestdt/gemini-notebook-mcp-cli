"""Clase 40 (M1) · Proporcionalidad de trazos: teorema de Thales."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase35 import _lt, _alts
import geo
import viz


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is not None and a not in seen:
            seen.add(a); out.append(a)
    return out


def four(r):
    """(p, q, k, j): AD = kp, DB = kq, AE = jp, EC = jq."""
    while True:
        p, q = r.randint(1, 4), r.randint(1, 4)
        k, j = r.randint(1, 4), r.randint(1, 4)
        if p != q and k != j:
            return p, q, k, j


NM = ("A", "B", "C", "D", "E")


# ---------------------------------------------------------------- Resolver problemas
def t_ec(r, l):
    p, q, k, j = four(r)
    u = r.choice(["cm", "m"])
    vals = {"AD": k * p, "DB": k * q, "AE": j * p, "EC": j * q}
    hide = r.choice(list(vals) if l else ["EC", "DB"])
    labs = {n: f"{v}" for n, v in vals.items()}
    val = vals[hide]
    labs[hide] = "x"
    fig = geo.thales_tri(NM, labs["AD"], labs["DB"], labs["AE"], labs["EC"], p / (p + q))
    ans = f"{val} {u}"
    other = {"AD": "AE", "DB": "EC", "AE": "AD", "EC": "DB"}[hide]
    al = uq(ans, [f"{vals[other]} {u}", f"{val + 1} {u}", f"{val + 2} {u}", f"{val * 2} {u}", f"{max(1, val - 1)} {u}", f"{val + abs(k - j)} {u}", f"{val + abs(k * p - j * p) + 1} {u}"])
    stem = f"En el triángulo ABC de la figura, DE es paralelo a BC (medidas en {u}). ¿Cuál es el valor de x?"
    return make(stem, fig, ans, al[:4], Q_RES, "Por el teorema de Thales, AD/DB = AE/EC; se despeja x.")


def t_de(r, l):
    p, q = r.choice([(1, 1), (1, 2), (2, 1), (2, 3), (3, 2), (1, 3), (3, 1)])
    k = r.randint(1, 4)
    m = r.randint(2, 6)
    BC = m * (p + q)
    DE = m * p
    labs = (f"{k * p}", f"{k * q}")
    fig = geo.thales_tri(NM, labs[0], labs[1], "", "", p / (p + q), "BC = " + str(BC), "x")
    ans = f"{DE}"
    al = uq(ans, [f"{BC - k * p}", f"{DE + k}", f"{m * q}", f"{BC // 2 if BC % 2 == 0 else DE + 2}", f"{DE + 1}", f"{max(1, DE - 1)}"])
    stem = f"En el triángulo ABC, DE es paralelo a BC. Se sabe que AD = {k * p}, DB = {k * q} y BC = {BC}. ¿Cuánto mide DE?"
    return make(stem, fig, ans, al[:4], Q_RES, f"DE/BC = AD/AB = {p}/{p + q}, luego DE = {BC}·{p}/{p + q} = {DE}.")


def t_par3(r, l):
    p, q, k, j = four(r)
    vals = [k * p, k * q, j * p, j * q]
    hide = r.randrange(4)
    labs = [str(v) for v in vals]
    ans_v = vals[hide]
    labs[hide] = "x"
    fig = geo.par_fig((labs[0], p), (labs[1], q), (labs[2], p), (labs[3], q))
    u = r.choice(["cm", "m"])
    ans = f"{ans_v} {u}"
    opp = vals[hide ^ 2]
    al = uq(ans, [f"{opp} {u}", f"{ans_v + 1} {u}", f"{ans_v + 2} {u}", f"{ans_v * 2} {u}", f"{max(1, ans_v - 1)} {u}"])
    return make(f"En la figura, las tres rectas horizontales son paralelas (medidas en {u}). ¿Cuál es el valor de x?", fig, ans, al[:4], Q_RES, "Tres paralelas cortadas por dos transversales determinan segmentos proporcionales.")


def t_ab(r, l):
    p, q, k, j = four(r)
    AB = k * (p + q)
    AC = j * (p + q)
    hide = r.choice(["AB", "AC"])
    fig = geo.thales_tri(NM, f"{k * p}", "", f"{j * p}", "", p / (p + q))
    if hide == "AB":
        stem = f"En el triángulo ABC, DE es paralelo a BC. Si AD = {k * p}, AE = {j * p} y AC = {AC}, ¿cuánto mide AB?"
        val = AB
    else:
        stem = f"En el triángulo ABC, DE es paralelo a BC. Si AD = {k * p}, AE = {j * p} y AB = {AB}, ¿cuánto mide AC?"
        val = AC
    ans = f"{val}"
    al = uq(ans, [f"{k * p + j * p}", f"{val + k}", f"{val + 1}", f"{val * 2}", f"{max(1, val - 2)}"])
    return make(stem, fig, ans, al[:4], Q_RES, "AD/AB = AE/AC por el teorema de Thales.")


# ---------------------------------------------------------------- Modelar
def t_river(r, l):
    p, q = r.choice([(1, 2), (2, 3), (1, 3), (2, 1), (3, 2)])
    k = r.randint(2, 5)
    m = r.randint(2, 8)
    DE = m * p
    BC = m * (p + q)
    fig = geo.thales_tri(NM, f"{k * p}", f"{k * q}", "", "", p / (p + q), "x", f"{DE}")
    ans = f"{BC} m"
    al = uq(ans, [f"{DE + k * q} m", f"{DE * 2} m", f"{m * q} m", f"{DE + k} m", f"{BC + m} m"])
    stem = f"Para estimar el ancho x de un río (BC) se marcan puntos A, D y E de modo que DE es paralelo a BC. Se miden AD = {k * p} m, DB = {k * q} m y DE = {DE} m. ¿Cuál es el ancho del río?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"DE/BC = AD/AB → {DE}/x = {p}/{p + q} → x = {BC} m.")


def t_streets(r, l):
    p, q, k, j = four(r)
    a, b, c, d = k * p, k * q, j * p, j * q
    hide = r.choice([1, 3, 2])
    vals = [a, b, c, d]
    ansv = vals[hide]
    labs = [str(v) if i != hide else "x" for i, v in enumerate(vals)]
    fig = geo.par_fig((labs[0], p), (labs[1], q), (labs[2], p), (labs[3], q))
    known = [v for i, v in enumerate(vals) if i != hide]
    names = ["el 1.er tramo de la calle izquierda", "el 2.º tramo de la calle izquierda", "el 1.er tramo de la calle derecha", "el 2.º tramo de la calle derecha"]
    stem = "Tres avenidas paralelas cortan a dos calles. Las medidas de los tramos son: " + ", ".join(f"{names[i]} {v} m" for i, v in enumerate(vals) if i != hide) + f". ¿Cuánto mide {names[hide]}?"
    ans = f"{ansv} m"
    al = uq(ans, [f"{vals[hide ^ 2]} m", f"{ansv + 1} m", f"{ansv + 2} m", f"{ansv * 2} m", f"{max(1, ansv - 1)} m"])
    return make(stem, fig, ans, al[:4], Q_MOD, "Los tramos determinados por paralelas son proporcionales.")


def t_split(r, l):
    m, n = r.choice([(1, 2), (2, 3), (1, 3), (3, 2), (2, 1), (3, 5), (1, 4)])
    t = r.randint(2, 9) * (m + n)
    body = L(60, 130, 500, 130, NAVY, 5)
    xm = 60 + 440 * m / (m + n)
    for x in (60, xm, 500):
        body += C(x, 130, 7, ACC)
    body += tag(60, 170, "A", 16) + tag(xm, 170, "P", 16) + tag(500, 170, "B", 16) + tag(280, 90, f"AB = {t} m", 16)
    fig = wrap(560, 210, body, "Segmento AB dividido por P")
    val = t // (m + n) * m
    ans = f"{val} m"
    other = t // (m + n) * n
    al = uq(ans, [f"{other} m", f"{t // 2} m", f"{val + m} m", f"{t - m} m", f"{val + 1} m"])
    stem = f"Un cable AB de {t} m se corta en un punto P tal que AP : PB = {m} : {n}. ¿Cuánto mide el tramo AP?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"AB se reparte en {m + n} partes iguales: AP = {t}/{m + n}·{m} = {val} m.")


def t_pole(r, l):
    a, b = r.choice([(2, 3), (3, 4), (1, 2), (2, 5)])
    k = r.randint(2, 5)
    m = r.randint(2, 6)
    stem = f"En un terreno, tres rectas paralelas dividen una calle en tramos de {k * a} m y {k * b} m. En la calle vecina, los tramos correspondientes suman {m * (a + b)} m. ¿Cuánto mide el primer tramo de la calle vecina?"
    val = m * a
    fig = geo.par_fig((f"{k * a}", a), (f"{k * b}", b), ("x", a), (f"{m * (a + b)} en total", b))
    ans = f"{val} m"
    al = uq(ans, [f"{m * b} m", f"{k * a} m", f"{val + m} m", f"{val * 2} m", f"{val + 1} m"])
    return make(stem, fig, ans, al[:4], Q_MOD, f"El tramo es la fracción {a}/{a + b} del total: {val} m.")


# ---------------------------------------------------------------- Representar
OK = ["AD/DB = AE/EC", "AD/AB = AE/AC", "DB/AB = EC/AC", "AD/AE = DB/EC", "DE/BC = AD/AB", "DE/BC = AE/AC"]
BAD = ["AD/DB = AE/AC", "AD/AB = AE/EC", "AD/DB = EC/AE", "DB/AB = AE/AC", "DE/BC = AD/DB", "DE/BC = DB/AB", "AD/AB = DB/EC"]


def t_read_prop(r, l):
    p, q = r.choice([(1, 2), (2, 3), (1, 3), (3, 2), (2, 1)])
    fig = geo.thales_tri(NM, "", "", "", "", p / (p + q))
    ans = r.choice(OK)
    return make("En el triángulo ABC de la figura, DE es paralelo a BC. ¿Cuál de las siguientes proporciones es correcta?", fig, ans, r.sample(BAD, 4), Q_REP, "Por el teorema de Thales, los trazos correspondientes son proporcionales.")


def t_read_par(r, l):
    p, q = r.choice([(1, 2), (2, 3), (1, 3), (3, 2), (2, 1)])
    a, b, c, d = r.choice([("a", "b", "c", "d"), ("m", "n", "s", "t"), ("p", "q", "u", "v")])
    fig = geo.par_fig((a, p), (b, q), (c, p), (d, q))
    OKS = [f"{a}/{b} = {c}/{d}", f"{a}/{c} = {b}/{d}", f"({a} + {b})/{a} = ({c} + {d})/{c}"]
    BADS = [f"{a}/{b} = {d}/{c}", f"{a}/{c} = {d}/{b}", f"{a}·{b} = {c}·{d}", f"{a}/{d} = {b}/{c}", f"{a} + {b} = {c} + {d}", f"{a}/{b} = ({c} + {d})/{c}"]
    return make("Las tres rectas horizontales de la figura son paralelas. ¿Cuál proporción es correcta?", fig, r.choice(OKS), r.sample(BADS, 4), Q_REP, "Los segmentos determinados en una transversal son proporcionales a los de la otra.")


def t_table(r, l):
    p, q, k, j = four(r)
    vals = [k * p, k * q, j * p, j * q]
    hide = r.randrange(4)
    rows = [[str(v) if i != hide else "?" for i, v in enumerate(vals)]]
    fig = viz.table_fig(["AD", "DB", "AE", "EC"], rows)
    ans = str(vals[hide])
    al = uq(ans, [str(vals[hide ^ 2]), str(vals[hide] + 1), str(vals[hide] + 2), str(vals[hide] * 2), str(max(1, vals[hide] - 1))])
    return make("La tabla muestra las medidas (en cm) de los trazos de un triángulo ABC con DE ∥ BC, donde D está en AB y E en AC. ¿Qué número corresponde a «?»", fig, ans, al[:4], Q_REP, "Se cumple AD/DB = AE/EC.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["DE ∥ BC; AD = 3, DB = 6, AE = 4", "AE/EC = AD/DB → EC = 4 + (6 − 3) = 7"], "Usó una diferencia: debía usar la proporción 3/6 = 4/EC, de donde EC = 8", \
            ["Planteó bien la proporción, pero cometió un error al multiplicar en cruz", "Igualó EC con DB porque los dos trazos están en el lado inferior", "Usó AB en lugar de DB al plantear la proporción con el trazo dado", "Invirtió una de las razones y obtuvo un valor menor que el correcto"]
    if k == 1:
        return ["DE ∥ BC", "AD/DB = EC/AE"], "Invirtió una de las razones: la proporción correcta es AD/DB = AE/EC", \
            ["Confundió los trazos AD y AE, que no se corresponden entre sí", "Usó el trazo AB en lugar del trazo DB en el primer cociente", "Planteó una proporción correcta, pero la escribió de forma distinta", "Aplicó el teorema de Pitágoras en lugar del teorema de Thales"]
    if k == 2:
        return ["AD = 2, DB = 3, AE = 4, EC = 5", "Como hay proporción, DE ∥ BC"], "No hay proporción: 2/3 ≠ 4/5, por lo que no se puede asegurar el paralelismo", \
            ["Sí hay proporción, porque en ambos lados la diferencia entre trazos es 1", "Sí hay proporción, porque los números crecen de manera ordenada en la lista", "No se puede concluir nada, pues el teorema solo sirve con triángulos isósceles", "El paralelismo se cumple porque AD y AE son menores que DB y EC"]
    return ["AD = 3, AB = 9, DE = 4", "BC = 4·(3/9) = 4/3"], "Invirtió la razón: DE/BC = AD/AB, luego BC = 4·9/3 = 12", \
        ["Usó DB en lugar de AB en la razón de semejanza, obteniendo un valor distinto", "Sumó AD y AB antes de multiplicar por el valor de DE en la proporción", "Igualó BC con AB porque ambos trazos son los lados mayores del triángulo", "Calculó bien la razón, pero se equivocó al multiplicar por la longitud de DE"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_converse(r, l):
    p, q, k, j = four(r)
    good = f"AD = {k * p}, DB = {k * q}, AE = {j * p}, EC = {j * q}"
    bads = []
    for _ in range(30):
        a, b, c, d = k * p, k * q, j * p, j * q
        w = r.choice([(a, b, c, d + 1), (a, b, c + 1, d), (a, b, d, c), (a + 1, b, c, d), (a, b + 2, c, d)])
        s = f"AD = {w[0]}, DB = {w[1]}, AE = {w[2]}, EC = {w[3]}"
        if w[0] * w[3] != w[1] * w[2] and s not in bads and s != good:
            bads.append(s)
    if len(bads) < 4:
        raise Reject
    fig = geo.thales_tri(NM, "", "", "", "", p / (p + q))
    return make("D está en el lado AB y E en el lado AC del triángulo ABC. ¿Con cuáles medidas se puede asegurar que DE es paralelo a BC?", fig, good, bads[:4], Q_ARG, "Hay paralelismo si y solo si AD/DB = AE/EC.")


TRUE = ["Si DE ∥ BC en el triángulo ABC, entonces AD/DB = AE/EC", "Tres rectas paralelas cortadas por dos transversales determinan segmentos proporcionales", "Si AD/AB = AE/AC, entonces DE es paralelo a BC",
        "Al trazar una paralela a un lado de un triángulo se forma un triángulo semejante al original", "Si DE ∥ BC, entonces DE/BC = AD/AB", "El teorema de Thales relaciona trazos proporcionales determinados por paralelas"]
FALSE = ["Si DE ∥ BC en el triángulo ABC, entonces AD = AE", "Tres rectas paralelas siempre determinan segmentos de igual longitud en las transversales", "Si AD = DB, entonces DE no puede ser paralelo a BC",
         "Al trazar una paralela a un lado de un triángulo, el triángulo formado nunca es semejante", "Si DE ∥ BC, entonces DE = BC", "El teorema de Thales solo se aplica a triángulos rectángulos"]


def _fig(r):
    p, q = r.choice([(1, 2), (2, 3), (1, 3), (3, 2)])
    return geo.thales_tri(NM, "", "", "", "", p / (p + q))


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el teorema de Thales es verdadera?", "Sobre proporcionalidad de trazos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el teorema de Thales.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre el teorema de Thales es falsa?", "Sobre proporcionalidad de trazos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el teorema de Thales.")


BY_SKILL = {
    Q_RES: [t_ec, t_de, t_par3, t_ab],
    Q_MOD: [t_river, t_streets, t_split, t_pole],
    Q_REP: [t_read_prop, t_read_par, t_table],
    Q_ARG: [t_error, t_converse, t_true, t_false],
}
