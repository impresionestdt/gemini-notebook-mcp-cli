"""Clase 51 (M1) · Regla de la suma: sucesos excluyentes y no excluyentes."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from sfigs import venn
from clase50 import fr, alts_fr, urn_counts, COLS
import viz
from clase45 import uq


def venn_data(r, nmax=60):
    while True:
        a, b, c, d = r.randint(2, 20), r.randint(2, 14), r.randint(2, 20), r.randint(2, 20)
        if a + b + c + d <= nmax and b < min(a + b, b + c):
            return a, b, c, d


# ---------------------------------------------------------------- Resolver problemas
def t_excl(r, l):
    ev = [("un número par o un 5", [2, 4, 6, 5]), ("un 1 o un 6", [1, 6]), ("un número menor que 3 o mayor que 4", [1, 2, 5, 6]), ("un múltiplo de 3 o un 4", [3, 6, 4]), ("un 2 o un número impar", [2, 1, 3, 5])]
    txt, fav = r.choice(ev)
    p = F(len(fav), 6)
    cells = "".join(R(60 + 70 * i, 60, 60, 60, WHITE, NAVY, 3) + T(90 + 70 * i, 100, str(i + 1), 28) for i in range(6))
    fig = wrap(560, 170, cells + tag(280, 150, "Cara del dado: 1, 2, 3, 4, 5 o 6", 15), "Dado de seis caras")
    ans = fr(p)
    al = alts_fr(p, [F(len(fav) - 1, 6), F(len(fav), 5), F(len(fav) + 1, 6)])
    return make(f"Se lanza un dado común. ¿Cuál es la probabilidad de obtener {txt}?", fig, ans, al[:4], Q_RES, f"Los casos favorables son {', '.join(map(str, sorted(fav)))} ({len(fav)} de 6).")


def t_urn_or(r, l):
    cs = urn_counts(r, 3, 2, 7, 20)
    n = sum(v for _, v in cs)
    i, j = r.sample(range(3), 2)
    fig = viz.urn_fig(cs)
    p = F(cs[i][1] + cs[j][1], n)
    ans = fr(p)
    al = alts_fr(p, [F(cs[i][1], n) * F(cs[j][1], n), F(cs[i][1], n), F(cs[j][1], n)])
    stem = f"Se extrae una bolita al azar de la urna. ¿Cuál es la probabilidad de que sea {cs[i][0][:-1] + 'a'} o {cs[j][0][:-1] + 'a'}?"
    return make(stem, fig, ans, al[:4], Q_RES, "Los colores son sucesos excluyentes: se suman sus probabilidades.")


def t_venn_union(r, l):
    a, b, c, d = venn_data(r)
    n = a + b + c + d
    fig = venn(a, b, c, d)
    kind = r.choice(["union", "inter", "only_a", "none"] if l else ["union", "inter"])
    if kind == "union":
        p = F(a + b + c, n); q = "A o B (al menos uno de los dos)"; wrong = [F(a + 2 * b + c, n), F(a + c, n), F(a + b, n) + F(b + c, n) if False else F(a + b + c + 1, n)]
    elif kind == "inter":
        p = F(b, n); q = "A y B a la vez"; wrong = [F(a + b + c, n), F(a, n), F(b, a + b + c)]
    elif kind == "only_a":
        p = F(a, n); q = "A pero no B"; wrong = [F(a + b, n), F(c, n), F(a, a + b)]
    else:
        p = F(d, n); q = "ni A ni B"; wrong = [F(a + b + c, n), F(d, a + b + c), F(1, n)]
    ans = fr(p)
    al = alts_fr(p, wrong)
    stem = f"El diagrama muestra cuántos de {n} elementos cumplen los sucesos A y B. Si se elige uno al azar, ¿cuál es la probabilidad de {q}?"
    return make(stem, fig, ans, al[:4], Q_RES, f"Se suman las regiones correspondientes y se divide por {n}.")


def t_inclusion(r, l):
    d = r.choice([10, 20, 12, 8, 5])
    pa = F(r.randint(2, d - 2), d); pb = F(r.randint(2, d - 2), d)
    pi_ = F(r.randint(1, d // 2), d)
    if pi_ > min(pa, pb): raise Reject
    u = pa + pb - pi_
    if u > 1: raise Reject
    kind = r.choice(["union", "inter"]) if l else "union"
    if kind == "union":
        ans = fr(u)
        fig = card([f"P(A) = {fr(pa)}", f"P(B) = {fr(pb)}", f"P(A ∩ B) = {fr(pi_)}", "P(A ∪ B) = ?"], 190, 18)
        al = alts_fr(u, [pa + pb if pa + pb <= 1 else None, pa + pb - 2 * pi_ if pa + pb - 2 * pi_ >= 0 else None, pa * pb])
        stem = f"Si P(A) = {fr(pa)}, P(B) = {fr(pb)} y P(A ∩ B) = {fr(pi_)}, ¿cuál es P(A ∪ B)?"
    else:
        ans = fr(pi_)
        fig = card([f"P(A) = {fr(pa)}", f"P(B) = {fr(pb)}", f"P(A ∪ B) = {fr(u)}", "P(A ∩ B) = ?"], 190, 18)
        al = alts_fr(pi_, [pa + pb - 2 * u if False else None, u - pa, pa * pb if pa * pb != pi_ else None, pa + pb - u + pi_ if pa + pb - u + pi_ <= 1 else None])
        stem = f"Si P(A) = {fr(pa)}, P(B) = {fr(pb)} y P(A ∪ B) = {fr(u)}, ¿cuál es P(A ∩ B)?"
    return make(stem, fig, ans, al[:4], Q_RES, "P(A ∪ B) = P(A) + P(B) − P(A ∩ B).")


def t_excl_prob(r, l):
    d = r.choice([10, 20, 12, 15, 8])
    pa = F(r.randint(1, d // 2 - 1), d) if d // 2 - 1 >= 1 else F(1, d)
    pb = F(r.randint(1, d // 2 - 1), d) if d // 2 - 1 >= 1 else F(1, d)
    u = pa + pb
    if u >= 1: raise Reject
    fig = card([f"P(A) = {fr(pa)}", f"P(B) = {fr(pb)}", "A y B son excluyentes", "P(A ∪ B) = ?"], 190, 18)
    ans = fr(u)
    al = alts_fr(u, [pa * pb, pa, pb, abs(pa - pb) if pa != pb else None])
    return make(f"Los sucesos A y B son mutuamente excluyentes, con P(A) = {fr(pa)} y P(B) = {fr(pb)}. ¿Cuál es P(A ∪ B)?", fig, ans, al[:4], Q_RES, "Si A y B son excluyentes, P(A ∩ B) = 0 y las probabilidades se suman.")


# ---------------------------------------------------------------- Modelar
def t_survey(r, l):
    a, b, c, d = venn_data(r, 50)
    n = a + b + c + d
    sports = r.choice([("fútbol", "básquetbol"), ("inglés", "francés"), ("guitarra", "piano"), ("ajedrez", "damas")])
    fa, fb = a + b, b + c
    fig = card([f"{n} estudiantes", f"{sports[0].capitalize()}: {fa}", f"{sports[1].capitalize()}: {fb}", f"Ambos: {b}"], 190, 18)
    kind = r.choice(["atleast", "none", "one"]) if l else "atleast"
    if kind == "atleast":
        p = F(fa + fb - b, n); q = f"practique {sports[0]} o {sports[1]} (al menos uno)"
        wrong = [F(fa + fb, n) if fa + fb <= n else None, F(fa + fb - 2 * b, n), F(b, n)]
    elif kind == "none":
        p = F(n - (fa + fb - b), n); q = f"no practique ninguno de los dos"
        wrong = [F(fa + fb - b, n), F(n - fa - fb + 2 * b, n) if n - fa - fb + 2 * b >= 0 else None, F(n - fa, n)]
    else:
        p = F(fa + fb - 2 * b, n); q = "practique exactamente uno de los dos"
        wrong = [F(fa + fb - b, n), F(fa + fb, n) if fa + fb <= n else None, F(b, n)]
    ans = fr(p)
    al = alts_fr(p, wrong)
    stem = f"En un curso de {n} estudiantes, {fa} practican {sports[0]}, {fb} practican {sports[1]} y {b} practican ambos. Si se elige un estudiante al azar, ¿cuál es la probabilidad de que {q}?"
    return make(stem, fig, ans, al[:4], Q_MOD, "Se usa P(A ∪ B) = P(A) + P(B) − P(A ∩ B) y el complemento cuando corresponde.")


def t_cards(r, l):
    a = r.choice([("un as", 4), ("un rey", 4), ("una figura (sota, caballo o rey)", 12)])
    b = r.choice([("una carta de copas", 10), ("una carta de oros", 10), ("una carta de espadas", 10)])
    both = 1 if a[1] == 4 else 3
    n = 40
    fig = card(["Baraja española: 40 cartas", "4 palos con 10 cartas cada uno", "Se extrae una carta al azar"], 140, 18)
    p = F(a[1] + b[1] - both, n)
    ans = fr(p)
    al = alts_fr(p, [F(a[1] + b[1], n), F(a[1] * b[1], n * n), F(a[1], n), F(b[1], n)])
    return make(f"En una baraja española de 40 cartas se extrae una al azar. ¿Cuál es la probabilidad de obtener {a[0]} o {b[0]}?", fig, ans, al[:4], Q_MOD, f"{a[1]} + {b[1]} − {both} (contada dos veces) = {a[1] + b[1] - both} casos favorables de {n}.")


def t_table_or(r, l):
    while True:
        a, b, c, d = [r.randint(3, 20) for _ in range(4)]
        n = a + b + c + d
        if n <= 80: break
    fig = viz.two_way_fig(["Hombres", "Mujeres"], ["Con mascota", "Sin mascota"], [[a, b], [c, d]])
    kind = r.choice(["h_or_m", "m_or_f", "notboth"])
    if kind == "h_or_m":
        p = F(a + b + c, n); q = "sea hombre o tenga mascota"; wrong = [F(a + b + a + c, n), F(a, n), F(a + b, n) + F(a + c, n) if False else F(a + b + c + 1, n)]
    elif kind == "m_or_f":
        p = F(c + d + a, n); q = "sea mujer o tenga mascota"; wrong = [F(c + d + a + c, n), F(c, n), F(a + c, n)]
    else:
        p = F(d + b + c, n) if False else F(n - a, n); q = "no sea hombre con mascota"; wrong = [F(a, n), F(b + c, n), F(n - a - d, n) if n - a - d >= 0 else None]
    ans = fr(p)
    al = alts_fr(p, wrong)
    return make(f"La tabla muestra a {n} personas. Si se elige una al azar, ¿cuál es la probabilidad de que {q}?", fig, ans, al[:4], Q_MOD, "Se cuentan las celdas favorables sin repetir la intersección.")


def t_neither(r, l):
    d = r.choice([10, 20, 12, 8, 5])
    pa, pb = F(r.randint(1, d - 3), d), F(r.randint(1, d - 3), d)
    pi_ = F(r.randint(0, 1), d)
    u = pa + pb - pi_
    if u >= 1 or pi_ > min(pa, pb): raise Reject
    ans = fr(1 - u)
    fig = card([f"P(A) = {fr(pa)}", f"P(B) = {fr(pb)}", f"P(A ∩ B) = {fr(pi_)}", "P(ni A ni B) = ?"], 190, 18)
    al = alts_fr(1 - u, [u, 1 - pa - pb if 1 - pa - pb >= 0 and 1 - pa - pb != 1 - u else None, (1 - pa) * (1 - pb)])
    return make(f"Si P(A) = {fr(pa)}, P(B) = {fr(pb)} y P(A ∩ B) = {fr(pi_)}, ¿cuál es la probabilidad de que no ocurra ni A ni B?", fig, ans, al[:4], Q_MOD, f"P(A ∪ B) = {fr(u)}; el complemento es {ans}.")


# ---------------------------------------------------------------- Representar
def t_read_venn(r, l):
    a, b, c, d = venn_data(r)
    n = a + b + c + d
    fig = venn(a, b, c, d)
    k = r.choice([("ocurra A", F(a + b, n)), ("ocurra B", F(b + c, n)), ("ocurra solo B", F(c, n)), ("no ocurra A", F(c + d, n)), ("ocurra A y B", F(b, n))])
    p = k[1]
    ans = fr(p)
    al = alts_fr(p, [F(a, n), F(b, n), F(c, n), F(d, n), F(a + b + c, n)])
    return make(f"En el diagrama de Venn hay {n} elementos en total. Si se elige uno al azar, ¿cuál es la probabilidad de que {k[0]}?", fig, ans, al[:4], Q_REP, "Se suman los recuentos de las regiones que cumplen la condición.")


def t_formula(r, l):
    ex = r.choice([True, False])
    fig = venn(6, 0 if ex else 3, 5, 9) if False else (venn(6, 0, 5, 9) if ex else venn(6, 3, 5, 9))
    if ex:
        ans = "P(A ∪ B) = P(A) + P(B)"
        al = ["P(A ∪ B) = P(A) + P(B) + P(A ∩ B)", "P(A ∪ B) = P(A) · P(B)", "P(A ∪ B) = P(A) − P(B)", "P(A ∪ B) = 1 − P(A) − P(B) + P(A ∩ B)"]
        stem = "En el diagrama, A y B no tienen elementos comunes. ¿Qué expresión permite calcular P(A ∪ B)?"
    else:
        ans = "P(A ∪ B) = P(A) + P(B) − P(A ∩ B)"
        al = ["P(A ∪ B) = P(A) + P(B)", "P(A ∪ B) = P(A) · P(B)", "P(A ∪ B) = P(A) + P(B) + P(A ∩ B)", "P(A ∪ B) = P(A) − P(B) + P(A ∩ B)"]
        stem = "En el diagrama, A y B tienen elementos comunes. ¿Qué expresión permite calcular P(A ∪ B)?"
    return make(stem, fig, ans, al, Q_REP, "Si hay intersección, se resta para no contarla dos veces.")


def t_which_region(r, l):
    a, b, c, d = venn_data(r)
    fig = venn(a, b, c, d)
    n = a + b + c + d
    ans_map = {"solo A": a, "A ∩ B": b, "solo B": c, "A ∪ B": a + b + c, "ni A ni B": d}
    k = r.choice(list(ans_map))
    val = ans_map[k]
    ans = str(val)
    al = uq(ans, [str(x) for x in (a, b, c, d, a + b + c, a + b, b + c) if x != val])
    return make(f"En el diagrama de Venn, ¿cuántos elementos pertenecen al suceso «{k}»?", fig, ans, al[:4], Q_REP, "Se identifican las regiones del diagrama que forman el suceso.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["P(A) = 3/5, P(B) = 1/2, P(A ∩ B) = 1/5", "P(A ∪ B) = 3/5 + 1/2 = 11/10"], "No restó P(A ∩ B): además, una probabilidad no puede superar 1; el resultado correcto es 9/10", \
            ["Restó P(A ∩ B) dos veces, por lo que obtuvo un valor menor que el correcto", "Multiplicó las probabilidades de A y de B en lugar de sumarlas entre sí", "Sumó bien, pero no simplificó la fracción, que es el único error cometido", "Usó la probabilidad del complemento de A en lugar de la probabilidad de A"]
    if k == 1:
        return ["Dado: P(par) = 1/2, P(mayor que 3) = 1/2", "P(par o mayor que 3) = 1/2 + 1/2 = 1"], "Los sucesos no son excluyentes (4 y 6 cumplen ambos): hay que restar P(A ∩ B) = 1/3, luego 2/3", \
            ["El resultado correcto es 1/4, que se obtiene multiplicando las dos probabilidades", "Sumó bien: como cada suceso tiene probabilidad 1/2, la unión es segura", "Debía restar 1/2 al resultado, obteniendo así una probabilidad final de 1/2", "El resultado correcto es 5/6, porque solo el 6 pertenece a ambos sucesos"]
    if k == 2:
        return ["A y B excluyentes, P(A) = 0,3, P(B) = 0,4", "P(A ∪ B) = 0,3 · 0,4 = 0,12"], "Multiplicó: para sucesos excluyentes se suman las probabilidades, 0,3 + 0,4 = 0,7", \
            ["Sumó y restó al mismo tiempo, por lo que el resultado debería ser 0,1", "Calculó P(A ∩ B) y no P(A ∪ B), ya que P(A ∩ B) sería 0,12", "Debió restar P(A) a P(B), lo que da una probabilidad de 0,1 para la unión", "Debía sumar las probabilidades y restar 0,12, obteniendo así 0,58 finalmente"]
    return ["A y B excluyentes", "Luego P(A ∩ B) = P(A) · P(B)"], "Si son excluyentes no pueden ocurrir juntos: P(A ∩ B) = 0", \
        ["Es correcto: la intersección de dos sucesos siempre es el producto de sus probabilidades", "Si son excluyentes, P(A ∩ B) = P(A) + P(B), porque se suman sus probabilidades", "Si son excluyentes, P(A ∩ B) = 1, porque siempre ocurre alguno de los dos", "Si son excluyentes, P(A ∩ B) = P(A ∪ B), porque no comparten elementos entre sí"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    a, b, c, d = venn_data(r)
    n = a + b + c + d
    fig = venn(a, b, c, d)
    ans = r.choice([f"P(A ∩ B) = {fr(F(b, n))}", f"P(A ∪ B) = {fr(F(a + b + c, n))}", f"P(ni A ni B) = {fr(F(d, n))}"])
    al = [f"P(A ∪ B) = {fr(F(a + 2 * b + c, n))}" if F(a + 2 * b + c, n) <= 1 else f"P(A ∪ B) = {fr(F(a + b + c + 1, n))}", f"P(A ∩ B) = {fr(F(a + b, n))}" if a + b != b else "P(A ∩ B) = 0", f"P(ni A ni B) = {fr(F(a + b + c, n))}" if a + b + c != d else "P(ni A ni B) = 1/2", f"A y B son excluyentes" if b else "A y B no son excluyentes", f"P(A) = {fr(F(a, n))}" if a != a + b else "P(A) = 1"]
    return make("Según el diagrama de Venn, ¿cuál afirmación es verdadera?", fig, ans, [x for x in al if x != ans][:4], Q_ARG, "Se calcula cada probabilidad a partir de los recuentos del diagrama.")


TRUE = ["Si A y B son excluyentes, P(A ∩ B) = 0", "Para cualquier par de sucesos, P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", "P(A ∪ B) nunca puede ser mayor que 1",
        "Si A y B son excluyentes, P(A ∪ B) = P(A) + P(B)", "P(A ∪ B) es mayor o igual que P(A)", "La probabilidad de que no ocurra ni A ni B es 1 − P(A ∪ B)"]
FALSE = ["Si A y B son excluyentes, P(A ∩ B) = 1", "Para cualquier par de sucesos, P(A ∪ B) = P(A) · P(B)", "P(A ∪ B) siempre es menor que P(A)",
         "Si A y B no son excluyentes, se suman P(A) y P(B) sin restar nada", "P(A ∪ B) puede valer 1,5", "La probabilidad de que no ocurra ni A ni B es P(A) + P(B)"]


def _fig(r):
    a, b, c, d = venn_data(r)
    return venn(a, b, c, d)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre la regla de la suma es verdadera?", "Sobre la probabilidad de la unión de sucesos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la regla de la suma.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre la regla de la suma es falsa?", "Sobre la probabilidad de la unión de sucesos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la regla de la suma.")


BY_SKILL = {
    Q_RES: [t_excl, t_urn_or, t_venn_union, t_inclusion, t_excl_prob],
    Q_MOD: [t_survey, t_cards, t_table_or, t_neither],
    Q_REP: [t_read_venn, t_formula, t_which_region],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
