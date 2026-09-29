"""Clase 50 (M1) · Probabilidad clásica (regla de Laplace)."""
from fractions import Fraction as F
from math import gcd
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from sfigs import spinner
from num import dstr
import viz
from clase45 import uq

COLS = ["rojas", "azules", "verdes", "amarillas", "negras", "blancas", "naranjas", "moradas"]
SPCOL = ["#FCA5A5", "#93C5FD", "#86EFAC", "#FDE68A", "#DDD6FE", "#FDBA74"]


def fr(x):
    x = F(x)
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def pct(x):
    x = F(x) * 100
    try:
        return (dstr(x) if x.denominator != 1 else str(x.numerator)) + " %"
    except ValueError:
        raise Reject


def alts_fr(p, extra=()):
    """Distractores fraccionarios con valor distinto al de p."""
    p = F(p)
    out = []
    for c in list(extra) + [1 - p, F(p.numerator, p.denominator + 1), F(p.numerator + 1, p.denominator), F(1, p.denominator), F(p.numerator, max(1, p.denominator - 1)) if p.denominator > 1 else None, p / 2, p * 2 if p * 2 <= 1 else None]:
        if c is None or c == p or c < 0 or c > 1:
            continue
        s = fr(c)
        if s not in out:
            out.append(s)
    return out


def urn_counts(r, k=None, lo=2, hi=6, nmax=20):
    k = k or r.choice([2, 3, 4])
    while True:
        cs = r.sample(COLS, k)
        ns = [r.randint(lo, hi) for _ in range(k)]
        if sum(ns) <= nmax and len(set(ns)) >= 2:
            return list(zip(cs, ns))


# ---------------------------------------------------------------- Resolver problemas
def t_urn(r, l):
    cs = urn_counts(r)
    n = sum(v for _, v in cs)
    i = r.randrange(len(cs))
    fig = viz.urn_fig(cs)
    kind = r.choice(["one", "not", "two"] if l else ["one", "not"])
    if kind == "one":
        p = F(cs[i][1], n); txt = f"sea de color {cs[i][0][:-1] + 'a'}"
        stem = f"En la urna de la figura se extrae una bolita al azar. ¿Cuál es la probabilidad de que {txt}?"
    elif kind == "not":
        p = F(n - cs[i][1], n)
        stem = f"En la urna de la figura se extrae una bolita al azar. ¿Cuál es la probabilidad de que NO sea de color {cs[i][0][:-1] + 'a'}?"
    else:
        j = (i + 1) % len(cs)
        p = F(cs[i][1] + cs[j][1], n)
        stem = f"En la urna de la figura se extrae una bolita al azar. ¿Cuál es la probabilidad de que sea de color {cs[i][0][:-1] + 'a'} o {cs[j][0][:-1] + 'a'}?"
    ans = fr(p)
    al = alts_fr(p, [F(cs[i][1], n - cs[i][1]) if cs[i][1] < n - cs[i][1] else None, F(cs[i][1], n + 1)])
    return make(stem, fig, ans, al[:4], Q_RES, f"Casos favorables / casos posibles = {ans}.")


def t_dice(r, l):
    ev = [("un número par", [2, 4, 6]), ("un número mayor que 4", [5, 6]), ("un número primo", [2, 3, 5]), ("un múltiplo de 3", [3, 6]), ("un número menor que 3", [1, 2]), ("un número impar", [1, 3, 5]), ("el número 6", [6]), ("un número distinto de 1", [2, 3, 4, 5, 6]), ("un número menor o igual que 4", [1, 2, 3, 4])]
    txt, fav = r.choice(ev)
    p = F(len(fav), 6)
    cells = "".join(R(60 + 70 * i, 60, 60, 60, WHITE, NAVY, 3) + T(90 + 70 * i, 100, str(i + 1), 28) for i in range(6))
    fig = wrap(560, 170, cells + tag(280, 150, "Cara del dado: 1, 2, 3, 4, 5 o 6", 15), "Dado de seis caras")
    ans = fr(p)
    al = alts_fr(p, [F(len(fav), 5), F(len(fav), 3)] if len(fav) != 1 else [F(1, 3)])
    return make(f"Se lanza un dado común de seis caras. ¿Cuál es la probabilidad de obtener {txt}?", fig, ans, al[:4], Q_RES, f"Casos favorables: {', '.join(map(str, fav))} ({len(fav)}); posibles: 6.")


def t_numbers(r, l):
    N = r.choice([10, 12, 15, 20, 24, 25, 30, 40, 50])
    k = r.choice([2, 3, 4, 5, 6, 7, 10])
    fav = N // k
    if fav == 0: raise Reject
    p = F(fav, N)
    body = ""
    fig = card([f"Papeles numerados del 1 al {N}", "Se elige uno al azar"], 110, 20)
    ans = fr(p)
    al = alts_fr(p, [F(fav, N - 1), F(fav + 1, N), F(k, N)])
    return make(f"En una caja hay {N} papeles numerados del 1 al {N}. Se extrae uno al azar. ¿Cuál es la probabilidad de que el número sea múltiplo de {k}?", fig, ans, al[:4], Q_RES, f"Hay {fav} múltiplos de {k} entre 1 y {N}: {fav}/{N} = {ans}.")


def t_spin(r, l):
    n = r.choice([4, 5, 6, 8, 10, 12])
    vals = list(range(1, n + 1))
    items = [(str(v), SPCOL[i % len(SPCOL)]) for i, v in enumerate(vals)]
    fig = spinner(items)
    ev = [("un número par", [v for v in vals if v % 2 == 0]), ("un número mayor que " + str(n // 2), [v for v in vals if v > n // 2]), ("un múltiplo de 3", [v for v in vals if v % 3 == 0]),
          ("un número menor o igual que 3", [v for v in vals if v <= 3]), ("un número impar", [v for v in vals if v % 2])]
    txt, fav = r.choice(ev)
    if not fav or len(fav) == n: raise Reject
    p = F(len(fav), n)
    ans = fr(p)
    al = alts_fr(p, [F(len(fav), n - 1), F(len(fav), n + 1)])
    return make(f"Se gira la ruleta de la figura, que tiene {n} sectores iguales. ¿Cuál es la probabilidad de obtener {txt}?", fig, ans, al[:4], Q_RES, f"{len(fav)} casos favorables de {n} posibles.")


# ---------------------------------------------------------------- Modelar
def t_raffle(r, l):
    n = r.choice([50, 100, 200, 250, 500, 1000])
    k = r.choice([1, 2, 5, 10, 20, 25])
    if k >= n: raise Reject
    p = F(k, n)
    ans = fr(p)
    fig = card([f"Rifa con {n} números", f"Compras {k} números", "Probabilidad de ganar el premio = ?"], 150, 18)
    al = alts_fr(p, [F(k, n - k), F(1, n)])
    return make(f"En una rifa se venden {n} números y hay un solo premio. Si compras {k} número{'s' if k > 1 else ''}, ¿cuál es la probabilidad de ganar?", fig, ans, al[:4], Q_MOD, f"{k} casos favorables de {n} posibles.")


def t_table_prob(r, l):
    rows = ["Hombres", "Mujeres"]
    cols = ["Tienen mascota", "No tienen"]
    while True:
        a, b, c, d = [r.randint(4, 20) for _ in range(4)]
        n = a + b + c + d
        if n <= 100: break
    fig = viz.table_fig(["", cols[0], cols[1]], [[rows[0], str(a), str(b)], [rows[1], str(c), str(d)]])
    kind = r.choice(["mascota", "mujer_no", "hombre"])
    if kind == "mascota":
        p = F(a + c, n); stem = f"La tabla muestra a {n} personas encuestadas. Si se elige una al azar, ¿cuál es la probabilidad de que tenga mascota?"
    elif kind == "mujer_no":
        p = F(d, n); stem = f"La tabla muestra a {n} personas encuestadas. Si se elige una al azar, ¿cuál es la probabilidad de que sea mujer y no tenga mascota?"
    else:
        p = F(a + b, n); stem = f"La tabla muestra a {n} personas encuestadas. Si se elige una al azar, ¿cuál es la probabilidad de que sea hombre?"
    ans = fr(p)
    al = alts_fr(p, [F(a, n), F(d, n), F(a + c, n - 1)])
    return make(stem, fig, ans, al[:4], Q_MOD, f"Casos favorables / total ({n}) = {ans}.")


def t_complement(r, l):
    p = r.choice([F(1, 5), F(3, 10), F(1, 4), F(2, 5), F(7, 10), F(1, 10), F(3, 4)])
    ctx = r.choice([("llueva mañana", "no llueva"), ("un producto salga defectuoso", "salga sin defecto"), ("un jugador acierte un tiro", "falle el tiro"), ("un tren llegue atrasado", "llegue a tiempo")])
    fig = card([f"P({ctx[0]}) = {fr(p)}", f"P({ctx[1]}) = ?"], 110, 20)
    ans = fr(1 - p)
    al = alts_fr(1 - p, [p, F(1, p.denominator)])
    return make(f"La probabilidad de que {ctx[0]} es {fr(p)}. ¿Cuál es la probabilidad de que {ctx[1]}?", fig, ans, al[:4], Q_MOD, f"P(no A) = 1 − {fr(p)} = {ans}.")


def t_pct(r, l):
    cs = urn_counts(r, 3, 2, 6, 20)
    n = sum(v for _, v in cs)
    if n not in (4, 5, 8, 10, 20, 25): raise Reject
    i = r.randrange(3)
    p = F(cs[i][1], n)
    fig = viz.urn_fig(cs)
    ans = pct(p)
    al = uq(ans, [pct(1 - p), pct(F(cs[i][1], n + 1)) if (n + 1) in (4, 5, 8, 10, 20, 25) else str(cs[i][1]) + " %", str(cs[i][1]) + " %", pct(p / 2), pct(F(1, n))])
    return make(f"En la urna de la figura se extrae una bolita al azar. ¿Cuál es la probabilidad, expresada como porcentaje, de que sea de color {cs[i][0][:-1] + 'a'}?", fig, ans, al[:4], Q_MOD, f"{cs[i][1]}/{n} = {ans}.")


# ---------------------------------------------------------------- Representar
def t_read_urn(r, l):
    cs = urn_counts(r, 3, 1, 7, 20)
    n = sum(v for _, v in cs)
    fig = viz.urn_fig(cs)
    i = r.randrange(3)
    p = F(cs[i][1], n)
    ans = fr(p)
    al = alts_fr(p, [F(cs[i][1], n - cs[i][1]) if cs[i][1] != n - cs[i][1] else None, F(n - cs[i][1], n)])
    return make(f"Según la urna de la figura, ¿cuál es la probabilidad de extraer una bolita {cs[i][0][:-1] + 'a'}? (Fracción simplificada.)", fig, ans, al[:4], Q_REP, f"{cs[i][1]} de {n} bolitas.")


def t_impossible(r, l):
    cs = urn_counts(r, 2, 2, 8, 16)
    fig = viz.urn_fig(cs)
    other = [c for c in COLS if c not in [x for x, _ in cs]][0]
    n = sum(v for _, v in cs)
    kinds = [(f"que sea {other[:-1] + 'a'}", "0"), (f"que sea {cs[0][0][:-1] + 'a'} o {cs[1][0][:-1] + 'a'}", "1")]
    txt, ans = r.choice(kinds)
    al = ["1/2", fr(F(cs[0][1], n)), fr(F(cs[1][1], n)), "0" if ans == "1" else "1", "2"]
    return make(f"En la urna de la figura se extrae una bolita al azar. ¿Cuál es la probabilidad {txt}?", fig, ans, uq(ans, al)[:4], Q_REP, "Un suceso imposible tiene probabilidad 0 y un suceso seguro, 1.")


def t_convert(r, l):
    n = r.choice([4, 5, 8, 10, 20, 25])
    k = r.randint(1, n - 1)
    p = F(k, n)
    cs = [("rojas", k), ("azules", n - k)]
    fig = viz.urn_fig(cs)
    kind = r.choice(["pct", "dec"])
    if kind == "pct":
        ans = pct(p)
        al = uq(ans, [pct(1 - p), str(k) + " %", pct(p * 2 if p * 2 <= 1 else p / 2), pct(F(1, n))])
        stem = "En la urna se extrae una bolita al azar. ¿Qué porcentaje representa la probabilidad de que sea roja?"
    else:
        ans = dstr(p) if p.denominator != 1 else str(p.numerator)
        al = uq(ans, [dstr(1 - p), str(k), dstr(F(1, n)), dstr(p / 2), dstr(p * 2 if p * 2 <= 1 else p / 4)])
        stem = "En la urna se extrae una bolita al azar. ¿Cuál es la probabilidad de que sea roja, expresada como número decimal?"
    return make(stem, fig, ans, al[:4], Q_REP, f"{k}/{n} = {dstr(p)} = {pct(p)}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Urna: 3 bolitas rojas y 5 azules", "P(roja) = 3/5"], "Dividió por los casos desfavorables: debía dividir por el total de bolitas, 3/8", \
            ["Dividió por la cantidad de bolitas azules, sin considerar el total de la urna", "Sumó los casos favorables y los desfavorables antes de dividir por dos", "Calculó la probabilidad de sacar azul en lugar de la de sacar roja", "Simplificó mal la fracción 3/8 y obtuvo un resultado erróneo"]
    if k == 1:
        return ["Dado común", "P(número par) = 3/3 = 1"], "Dividió por los casos favorables: los casos posibles son 6, luego P = 3/6 = 1/2", \
            ["Consideró solo los números pares como casos posibles del lanzamiento", "Contó dos casos favorables en lugar de tres al escribir la fracción", "Calculó bien la probabilidad, pero la expresó como decimal incorrecto", "Confundió la probabilidad del suceso con la de su complemento, que es 1/2"]
    if k == 2:
        return ["P(A) = 2/5", "P(no A) = 2/5 − 1 = −3/5"], "Restó al revés: P(no A) = 1 − 2/5 = 3/5; una probabilidad nunca es negativa", \
            ["Sumó las probabilidades en lugar de restarlas al calcular el complemento", "Calculó bien, pero una probabilidad puede ser negativa en algunos casos", "Usó como complemento la fracción inversa 5/2 en vez de restar a 1", "Dividió 2/5 por 2 para obtener la probabilidad del suceso contrario"]
    return ["Moneda: sale cara 3 veces seguidas", "Ahora es más probable que salga sello"], "Los lanzamientos son independientes: cada vez P(sello) sigue siendo 1/2", \
        ["Como ya salieron 3 caras, ahora es imposible que vuelva a salir cara", "Después de 3 caras, la probabilidad de cara pasa a ser 0", "La probabilidad de sello aumenta a 3/4 porque el azar compensa lo ocurrido", "La moneda está trucada, por lo que siempre saldrá cara en los siguientes"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    cs = urn_counts(r, 3, 1, 7, 20)
    n = sum(v for _, v in cs)
    order = sorted(range(3), key=lambda i: -cs[i][1])
    if cs[order[0]][1] == cs[order[1]][1] or cs[order[1]][1] == cs[order[2]][1]: raise Reject
    fig = viz.urn_fig(cs)
    hi, lo = cs[order[0]][0][:-1] + "a", cs[order[2]][0][:-1] + "a"
    ans = r.choice([f"Es más probable sacar una bolita {hi} que una {lo}", f"La probabilidad de sacar una bolita {lo} es la menor de las tres"])
    al = [f"Es más probable sacar una bolita {lo} que una {hi}", f"Las tres probabilidades son iguales", f"La probabilidad de sacar una bolita {hi} es la menor de las tres", "La suma de las tres probabilidades es mayor que 1", f"Es imposible sacar una bolita {lo}"]
    return make("Según la urna de la figura, ¿cuál afirmación es verdadera?", fig, ans, al[:4], Q_ARG, "Mayor cantidad de bolitas implica mayor probabilidad.")


TRUE = ["La probabilidad de un suceso es un número entre 0 y 1", "La probabilidad de un suceso imposible es 0", "La probabilidad de un suceso seguro es 1", "La regla de Laplace divide los casos favorables por los casos posibles",
        "La probabilidad de que un suceso no ocurra es 1 menos la probabilidad de que ocurra", "En un dado común, la probabilidad de obtener 6 es 1/6"]
FALSE = ["La probabilidad de un suceso puede ser mayor que 1", "La probabilidad de un suceso imposible es 1", "La probabilidad de un suceso seguro es 0", "La regla de Laplace divide los casos posibles por los casos favorables",
         "La probabilidad de que un suceso no ocurra es igual a la probabilidad de que ocurra", "En un dado común, la probabilidad de obtener 6 es 1/2"]


def _fig(r):
    return viz.urn_fig(urn_counts(r))


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre probabilidad es verdadera?", "Sobre la regla de Laplace, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones de probabilidad.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre probabilidad es falsa?", "Sobre la regla de Laplace, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones de probabilidad.")


BY_SKILL = {
    Q_RES: [t_urn, t_dice, t_numbers, t_spin],
    Q_MOD: [t_raffle, t_table_prob, t_complement, t_pct],
    Q_REP: [t_read_urn, t_impossible, t_convert],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
