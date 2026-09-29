"""Clase 52 (M1) · Regla del producto: sucesos independientes y dependientes; árboles de probabilidad."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase50 import fr, alts_fr, COLS
import viz
from clase45 import uq

CN = {"rojas": "roja", "azules": "azul", "verdes": "verde", "amarillas": "amarilla", "negras": "negra", "blancas": "blanca"}
CL = list(CN)


def two_col(r, nlo=5, nhi=12):
    while True:
        c1, c2 = r.sample(CL, 2)
        a, b = r.randint(2, 7), r.randint(2, 7)
        if nlo <= a + b <= nhi and a != b and c1[0] != c2[0]:
            return (c1, a), (c2, b)


def tree(cs, repl, hide=None):
    (c1, a), (c2, b) = cs
    n = a + b
    f = [(c1[0].upper(), fr(F(a, n))), (c2[0].upper(), fr(F(b, n)))]
    if repl:
        s = [[(c1[0].upper(), fr(F(a, n))), (c2[0].upper(), fr(F(b, n)))]] * 2
    else:
        s = [[(c1[0].upper(), fr(F(a - 1, n - 1))), (c2[0].upper(), fr(F(b, n - 1)))], [(c1[0].upper(), fr(F(a, n - 1))), (c2[0].upper(), fr(F(b - 1, n - 1)))]]
    return viz.ptree_fig(f, s, hide)


# ---------------------------------------------------------------- Resolver problemas
def t_indep(r, l):
    ctxs = [("Se lanza una moneda y un dado", "obtener cara y un número par", F(1, 2), F(1, 2)), ("Se lanza una moneda y un dado", "obtener sello y un 6", F(1, 2), F(1, 6)),
            ("Se lanzan dos dados", "obtener un 6 en ambos", F(1, 6), F(1, 6)), ("Se lanzan dos dados", "obtener un número par en el primero y un número mayor que 4 en el segundo", F(1, 2), F(1, 3)),
            ("Se lanzan dos monedas", "obtener dos caras", F(1, 2), F(1, 2)), ("Se lanza un dado y se gira una ruleta de 4 sectores iguales numerados", "obtener un 3 en el dado y un 1 en la ruleta", F(1, 6), F(1, 4)),
            ("Se lanza un dado y se gira una ruleta de 5 sectores iguales numerados", "obtener un número impar en el dado y un 5 en la ruleta", F(1, 2), F(1, 5))]
    intro, ev, pa, pb = r.choice(ctxs)
    fig = card([f"P(1.er suceso) = {fr(pa)}", f"P(2.º suceso) = {fr(pb)}", "Los sucesos son independientes"], 150, 18)
    p = pa * pb
    ans = fr(p)
    al = alts_fr(p, [pa + pb if pa + pb <= 1 else None, pa, pb, F(1, 6), pa * pb * 2])
    return make(f"{intro}. ¿Cuál es la probabilidad de {ev}?", fig, ans, al[:4], Q_RES, f"Sucesos independientes: {fr(pa)}·{fr(pb)} = {ans}.")


def t_repl(r, l):
    cs = two_col(r)
    (c1, a), (c2, b) = cs
    n = a + b
    kind = r.choice(["same", "diff"])
    fig = viz.urn_fig([cs[0], cs[1]])
    if kind == "same":
        p = F(a, n) ** 2; q = f"ambas sean {CN[c1]}s"
    else:
        p = F(a, n) * F(b, n); q = f"la primera sea {CN[c1]} y la segunda {CN[c2]}"
    ans = fr(p)
    al = alts_fr(p, [F(a, n) * F(a - 1, n - 1) if kind == "same" else F(a, n) * F(b, n - 1), F(a, n) + F(a, n) if kind == "same" else F(a + b, n), F(a, n), F(b, n)])
    stem = f"Se extraen dos bolitas de la urna, CON reposición (se devuelve la primera antes de sacar la segunda). ¿Cuál es la probabilidad de que {q}?"
    return make(stem, fig, ans, al[:4], Q_RES, "Con reposición los sucesos son independientes: se multiplican las probabilidades de cada extracción.")


def t_norepl(r, l):
    cs = two_col(r, 5, 12)
    (c1, a), (c2, b) = cs
    n = a + b
    if a < 2: raise Reject
    kind = r.choice(["same", "diff"])
    fig = viz.urn_fig([cs[0], cs[1]])
    if kind == "same":
        p = F(a, n) * F(a - 1, n - 1); q = f"ambas sean {CN[c1]}s"
        wrong = [F(a, n) ** 2, F(a, n) * F(a, n - 1), F(a * a, n)]
    else:
        p = F(a, n) * F(b, n - 1); q = f"la primera sea {CN[c1]} y la segunda {CN[c2]}"
        wrong = [F(a, n) * F(b, n), F(a, n) * F(b - 1, n - 1) if b > 1 else None, F(a + b, n)]
    ans = fr(p)
    al = alts_fr(p, wrong)
    stem = f"Se extraen dos bolitas de la urna, SIN reposición. ¿Cuál es la probabilidad de que {q}?"
    return make(stem, fig, ans, al[:4], Q_RES, "Sin reposición cambian las cantidades en la segunda extracción: el segundo suceso depende del primero.")


def t_three(r, l):
    kinds = [("Una moneda se lanza tres veces. ¿Cuál es la probabilidad de obtener tres caras?", F(1, 8)), ("Un dado se lanza tres veces. ¿Cuál es la probabilidad de obtener un 6 las tres veces?", F(1, 216)),
             ("Una moneda se lanza tres veces. ¿Cuál es la probabilidad de obtener cara, sello y cara, en ese orden?", F(1, 8)), ("Un dado se lanza dos veces. ¿Cuál es la probabilidad de obtener un número par las dos veces?", F(1, 4)),
             ("Una ruleta con 4 sectores iguales se gira tres veces. ¿Cuál es la probabilidad de obtener el mismo sector marcado las tres veces?", F(1, 64)), ("Un dado se lanza tres veces. ¿Cuál es la probabilidad de obtener un número impar las tres veces?", F(1, 8))]
    txt, p = r.choice(kinds)
    fig = card(["Sucesos independientes", "Se multiplican las probabilidades de cada intento"], 110, 18)
    ans = fr(p)
    al = alts_fr(p, [F(3, 2) * F(1, 6) if False else F(1, 3), F(1, 2), p * 3 if p * 3 < 1 else None, F(1, 6), F(1, 4), F(3, 8)])
    return make(txt, fig, ans, al[:4], Q_RES, "Se multiplica la probabilidad de cada intento.")


# ---------------------------------------------------------------- Modelar
def t_shots(r, l):
    p = r.choice([F(3, 5), F(1, 2), F(4, 5), F(7, 10), F(2, 3), F(3, 4)])
    n = r.choice([2, 3])
    who = r.choice(["Una jugadora de básquetbol", "Un arquero", "Un jugador de tenis (en su saque)"])
    kind = r.choice(["all", "atleast"]) if l else "all"
    if kind == "all":
        val = p ** n; q = f"acierte los {n} intentos"
        wrong = [p * n if p * n <= 1 else None, p, p ** (n - 1), 1 - p ** n]
    else:
        val = 1 - (1 - p) ** n; q = "acierte al menos un intento"
        wrong = [p ** n, p, (1 - p) ** n if val != (1 - p) ** n else None, min(F(1), p * n) if p * n != 1 else None, 1 - p]
    fig = card([f"Probabilidad de acertar: {fr(p)}", f"Intentos independientes: {n}", ""], 150, 18) if False else card([f"Probabilidad de acertar cada intento: {fr(p)}", f"Número de intentos independientes: {n}"], 130, 18)
    ans = fr(val)
    al = alts_fr(val, wrong)
    return make(f"{who} acierta cada intento con probabilidad {fr(p)}, de forma independiente. Si realiza {n} intentos, ¿cuál es la probabilidad de que {q}?", fig, ans, al[:4], Q_MOD, "Se multiplican las probabilidades; 'al menos uno' se calcula con el complemento.")


def t_defect(r, l):
    n = r.choice([8, 10, 12, 15])
    d = r.randint(2, 4)
    repl = r.choice([True, False])
    if repl:
        p = F(d, n) ** 2; extra = " (se devuelve cada pieza)" if False else ""
        stem = f"En un lote de {n} piezas hay {d} defectuosas. Se revisan dos piezas al azar, devolviendo la primera al lote antes de revisar la segunda. ¿Cuál es la probabilidad de que ambas sean defectuosas?"
        wrong = [F(d, n) * F(d - 1, n - 1), F(2 * d, n), F(d, n)]
    else:
        p = F(d, n) * F(d - 1, n - 1)
        stem = f"En un lote de {n} piezas hay {d} defectuosas. Se revisan dos piezas al azar, sin devolver la primera. ¿Cuál es la probabilidad de que ambas sean defectuosas?"
        wrong = [F(d, n) ** 2, F(2 * d, n), F(d, n)]
    fig = card([f"Lote: {n} piezas", f"Defectuosas: {d}", "Con reposición" if repl else "Sin reposición"], 150, 18)
    ans = fr(p)
    al = alts_fr(p, wrong)
    return make(stem, fig, ans, al[:4], Q_MOD, "Se multiplican las probabilidades de cada revisión, ajustando las cantidades si no hay reposición.")


def t_weather(r, l):
    p1 = r.choice([F(3, 10), F(1, 2), F(2, 5), F(1, 4)])
    p2 = r.choice([F(7, 10), F(3, 5), F(1, 2), F(4, 5)])
    fig = card([f"Llueve el lunes: {fr(p1)}", f"Si llueve el lunes, llueve el martes: {fr(p2)}", "P(llueve ambos días) = ?"], 150, 17)
    p = p1 * p2
    ans = fr(p)
    al = alts_fr(p, [p1 + p2 if p1 + p2 <= 1 else None, p1, p2, (1 - p1) * p2])
    return make(f"La probabilidad de que llueva el lunes es {fr(p1)}. Si llueve el lunes, la probabilidad de que llueva el martes es {fr(p2)}. ¿Cuál es la probabilidad de que llueva ambos días?", fig, ans, al[:4], Q_MOD, f"{fr(p1)}·{fr(p2)} = {ans}.")


def t_cards2(r, l):
    a = r.choice([("ases", 4), ("reyes", 4), ("copas", 10), ("oros", 10)])
    p = F(a[1], 40) * F(a[1] - 1, 39)
    fig = card(["Baraja española de 40 cartas", f"Hay {a[1]} {a[0]}", "Se extraen 2 cartas sin reposición"], 150, 18)
    ans = fr(p)
    al = alts_fr(p, [F(a[1], 40) ** 2, F(a[1], 40) * F(a[1], 39), F(2 * a[1], 40), F(a[1], 40)])
    return make(f"De una baraja española de 40 cartas se extraen dos cartas sin reposición. ¿Cuál es la probabilidad de que ambas sean {a[0]}?", fig, ans, al[:4], Q_MOD, f"{a[1]}/40 · {a[1] - 1}/39 = {ans}.")


# ---------------------------------------------------------------- Representar
def t_read_tree(r, l):
    cs = two_col(r, 5, 10)
    (c1, a), (c2, b) = cs
    if a < 2: raise Reject
    n = a + b
    repl = r.choice([True, False])
    fig = tree(cs, repl)
    i, j = r.randrange(2), r.randrange(2)
    cnt = [a, b]
    if repl:
        p = F(cnt[i], n) * F(cnt[j], n)
    else:
        p = F(cnt[i], n) * F((cnt[j] - (1 if i == j else 0)), n - 1)
    nm = [c1[0].upper(), c2[0].upper()]
    ans = fr(p)
    al = alts_fr(p, [F(cnt[i], n) * F(cnt[j], n) if not repl else F(cnt[i], n) * F(cnt[j] - (1 if i == j else 0), n - 1), F(cnt[i], n) + F(cnt[j], n) if F(cnt[i], n) + F(cnt[j], n) <= 1 else None, F(cnt[i], n), F(cnt[j], n)])
    stem = f"El árbol de probabilidades corresponde a dos extracciones {'con' if repl else 'sin'} reposición de una urna con bolitas de dos colores (R y A son las iniciales). ¿Cuál es la probabilidad de la rama {nm[i]} y luego {nm[j]}?"
    stem = stem.replace("R y A son las iniciales", f"{nm[0]} y {nm[1]} son las iniciales de los colores")
    return make(stem, fig, ans, al[:4], Q_REP, "Se multiplican las probabilidades a lo largo de la rama.")


def t_hide_tree(r, l):
    cs = two_col(r, 5, 10)
    (c1, a), (c2, b) = cs
    if a < 2: raise Reject
    n = a + b
    fig_h = tree(cs, False, hide=(0, 0))
    ans = fr(F(a - 1, n - 1))
    al = alts_fr(F(a - 1, n - 1), [F(a, n), F(a, n - 1), F(a - 1, n), F(b, n - 1)])
    return make("En el árbol de dos extracciones sin reposición, ¿qué probabilidad corresponde a «?» en la rama de la segunda extracción que sigue a la primera bolita sacada del primer color?", fig_h, ans, al[:4], Q_REP, "Tras sacar una bolita de ese color, queda una menos de ese color y una menos en total.")


def t_expr(r, l):
    cs = two_col(r, 5, 10)
    (c1, a), (c2, b) = cs
    n = a + b
    if a < 2: raise Reject
    fig = viz.urn_fig([cs[0], cs[1]])
    ans = f"{a}/{n} · {a - 1}/{n - 1}"
    al = [f"{a}/{n} · {a}/{n}", f"{a}/{n} + {a - 1}/{n - 1}", f"{a}/{n} · {a}/{n - 1}", f"{a - 1}/{n} · {a - 1}/{n - 1}"]
    return make(f"Se extraen dos bolitas SIN reposición de la urna. ¿Qué expresión representa la probabilidad de que ambas sean {CN[c1]}s?", fig, ans, al, Q_REP, "Segunda extracción: una bolita de ese color menos y una bolita menos en total.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Dos dados, P(6 en ambos)", "1/6 + 1/6 = 1/3"], "Sumó: para que ocurran ambos sucesos independientes se multiplican, 1/6 · 1/6 = 1/36", \
            ["Multiplicó 1/6 por 2 en lugar de multiplicar las dos probabilidades entre sí", "Dividió 1/6 por 2 porque hay dos dados en el experimento planteado", "Calculó bien la probabilidad, pero la expresó en forma de porcentaje", "Usó 1/3, que es la probabilidad de obtener un 6 en el primer o el segundo dado"]
    if k == 1:
        return ["Urna: 4 rojas y 6 azules; dos extracciones sin reposición", "P(2 rojas) = 4/10 · 4/10 = 4/25"], "En la segunda extracción quedan 3 rojas de 9 bolitas: P = 4/10 · 3/9 = 2/15", \
            ["Debía sumar las probabilidades de cada extracción en lugar de multiplicarlas", "Debía usar 4/10 · 3/10, porque el total de bolitas no cambia entre las extracciones", "Debía usar 4/10 · 4/9, porque la cantidad de rojas no cambia al sacar una", "El planteamiento es correcto, pues sin reposición las extracciones son independientes"]
    if k == 2:
        return ["Una moneda sale cara 3 veces seguidas", "P(sello en el 4.º) es mayor que 1/2, pues «toca» sello"], "Los lanzamientos son independientes: la probabilidad de sello sigue siendo 1/2", \
            ["La probabilidad es menor que 1/2, porque ya salieron cara en las tres ocasiones", "La probabilidad de sello es 0, porque la moneda ya tiene una racha de caras", "La probabilidad de sello es 3/4, porque la moneda compensa las caras anteriores", "La probabilidad de sello es 1/8, porque hay que multiplicar por las tres caras"]
    return ["P(A) = 0,5, P(B) = 0,4, sucesos independientes", "P(A ∩ B) = 0,5 + 0,4 = 0,9"], "Sumó en lugar de multiplicar: P(A ∩ B) = 0,5 · 0,4 = 0,2", \
        ["Restó las probabilidades en lugar de multiplicarlas, obteniendo el valor 0,1", "Debía dividir 0,5 por 0,4 para obtener la probabilidad de la intersección", "Calculó P(A ∪ B) bien, por lo que solo debe cambiar el nombre del resultado", "Debía multiplicar y luego sumar 0,1 porque los sucesos son independientes"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_indep_claim(r, l):
    cases = [("Se lanza una moneda dos veces", "Independientes", "El resultado del primer lanzamiento no afecta al segundo"),
             ("Dos extracciones de una urna sin reposición", "Dependientes", "La composición de la urna cambia tras la primera extracción"),
             ("Dos extracciones de una urna con reposición", "Independientes", "La urna queda igual antes de la segunda extracción"),
             ("Se lanzan un dado y una moneda a la vez", "Independientes", "Ningún resultado influye en el otro"),
             ("Dos cartas de una baraja, sin devolver la primera", "Dependientes", "Al sacar la primera cambia el mazo restante")]
    txt, ans_t, why = r.choice(cases)
    fig = card(["Situación:", txt], 110, 16)
    ans = ans_t
    al = ["Dependientes" if ans_t == "Independientes" else "Independientes", "Excluyentes", "Imposibles", "Seguros"]
    return make(f"Situación: «{txt}». ¿Cómo son los dos sucesos (el resultado del primero y el del segundo)?", fig, ans, al, Q_ARG, why + ".")


TRUE = ["Si A y B son independientes, P(A ∩ B) = P(A) · P(B)", "Con reposición, las extracciones sucesivas son independientes", "Sin reposición, la segunda extracción depende de la primera",
        "En un árbol de probabilidades se multiplican las probabilidades a lo largo de una rama", "La suma de las probabilidades de las ramas que salen de un mismo nodo es 1", "El resultado de lanzar una moneda no influye en el siguiente lanzamiento"]
FALSE = ["Si A y B son independientes, P(A ∩ B) = P(A) + P(B)", "Sin reposición, las extracciones sucesivas son independientes", "Con reposición, la segunda extracción depende de la primera",
         "En un árbol de probabilidades se suman las probabilidades a lo largo de una rama", "La suma de las probabilidades de las ramas que salen de un mismo nodo es 2", "Después de una racha de caras, sale sello con mayor probabilidad"]


def _fig(r):
    cs = two_col(r, 5, 10)
    return tree(cs, r.choice([True, False]))


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre la regla del producto es verdadera?", "Sobre sucesos independientes y árboles de probabilidad, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la regla del producto.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre la regla del producto es falsa?", "Sobre sucesos independientes y árboles de probabilidad, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la regla del producto.")


BY_SKILL = {
    Q_RES: [t_indep, t_repl, t_norepl, t_three],
    Q_MOD: [t_shots, t_defect, t_weather, t_cards2],
    Q_REP: [t_read_tree, t_hide_tree, t_expr],
    Q_ARG: [t_error, t_indep_claim, t_true, t_false],
}
