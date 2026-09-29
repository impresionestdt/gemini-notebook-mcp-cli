"""Clase 47 (M1) · Medidas de tendencia central en datos no agrupados: media, mediana y moda."""
from fractions import Fraction as F
from collections import Counter
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from num import dstr
from sfigs import bar_chart
import viz
from clase45 import uq


def nf(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    try:
        return dstr(x)
    except ValueError:
        raise Reject


def dl(data):
    return ", ".join(map(str, data))


def data_card(data, head="Datos:"):
    h = (len(data) + 1) // 2
    lines = [head, dl(data[:h]) + ("," if len(data) > h else ""), dl(data[h:])] if len(data) > 5 else [head, dl(data)]
    return card(lines, 60 + 40 * len(lines), 18)


def median(d):
    s = sorted(d); n = len(s)
    return F(s[n // 2]) if n % 2 else F(s[n // 2 - 1] + s[n // 2], 2)


def mean(d):
    return F(sum(d), len(d))


def uni_mode(d):
    c = Counter(d).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return None
    return c[0][0]


def rdata(r, n, lo=1, hi=15):
    return [r.randint(lo, hi) for _ in range(n)]


# ---------------------------------------------------------------- Resolver problemas
def t_mean(r, l):
    n = r.choice([4, 5, 6, 8, 10])
    d = rdata(r, n, 2, 20)
    m = mean(d)
    ans = nf(m)
    md = median(d)
    al = uq(ans, [nf(md), nf(sum(d)), nf(m + 1), nf(m - 1) if m > 1 else nf(m + 2), nf(F(sum(d), n + 1)) if (sum(d) % (n + 1) == 0 or (n + 1) in (4, 5, 8, 10)) else nf(m + F(1, 2)), nf(max(d))])
    return make("¿Cuál es la media aritmética (promedio) de los datos de la figura?", data_card(d), ans, al[:4], Q_RES, f"Suma = {sum(d)}; media = {sum(d)}/{n} = {ans}.")


def t_median(r, l):
    n = r.choice([5, 7, 9, 6, 8, 10] if l else [5, 7, 6, 8])
    d = rdata(r, n, 1, 20)
    m = median(d)
    ans = nf(m)
    s = sorted(d)
    al = uq(ans, [nf(mean(d)), nf(d[n // 2]), nf(s[0]), nf(s[-1]), nf(s[n // 2 - 1] if n % 2 == 0 else s[n // 2 + 1]), nf(m + 1)])
    return make("¿Cuál es la mediana de los datos de la figura?", data_card(d), ans, al[:4], Q_RES, f"Ordenados: {dl(s)}; la mediana es {ans}.")


def t_mode(r, l):
    n = r.choice([8, 10, 12])
    while True:
        d = rdata(r, n, 1, 9)
        m = uni_mode(d)
        if m is not None and Counter(d)[m] >= 3:
            break
    ans = str(m)
    al = uq(ans, [nf(median(d)), nf(mean(d)) if (sum(d) % n == 0 or n in (8, 10)) else str(max(d)), str(Counter(d)[m]), str(max(d)), str(min(d)), str(m + 1)])
    return make("¿Cuál es la moda de los datos de la figura?", data_card(d), ans, al[:4], Q_RES, f"El valor {m} se repite {Counter(d)[m]} veces, más que cualquier otro.")


def t_mean_table(r, l):
    vals = sorted(r.sample(range(1, 8), 4))
    n = r.choice([10, 20, 25, 40])
    from clase45 import split
    fis = split(r, n, 4, 1)
    S = sum(v * f for v, f in zip(vals, fis))
    ans = nf(F(S, n))
    fig = viz.table_fig(["Valor", "fi"], [[str(v), str(f)] for v, f in zip(vals, fis)] + [["Total", str(n)]])
    al = uq(ans, [nf(F(sum(vals), 4)) if sum(vals) % 4 == 0 or True else None, str(vals[fis.index(max(fis))]), nf(F(S, n) + 1), nf(F(S, sum(fis) + 1)) if (sum(fis) + 1) else None, str(S), nf(F(S, 4))])
    return make("La tabla muestra la distribución de una variable en un grupo. ¿Cuál es la media de los datos?", fig, ans, al[:4], Q_RES, f"Media = Σ valor·fi / n = {S}/{n} = {ans}.")


# ---------------------------------------------------------------- Modelar
def t_new_value(r, l):
    n = r.choice([4, 5, 9])
    S = r.randint(3 * n, 6 * n)
    x = r.randint(2, 7)
    m0, m1 = F(S, n), F(S + x, n + 1)
    a0, a1 = nf(m0), nf(m1)
    fig = card([f"{n} notas con promedio {a0}", f"Se agrega una nota: nuevo promedio {a1}", "Nota agregada = ?"], 150, 18)
    ans = nf(x)
    al = uq(ans, [nf(m1), nf(m1 - m0), nf(x + 1), nf(x - 1) if x > 1 else nf(x + 2), nf(F(S, n) + x if False else x + 2), nf(m1 + m0 - x if (m1 + m0 - x) > 0 else x + 3)])
    stem = f"El promedio de {n} notas es {a0}. Al agregar una nota más, el promedio pasa a ser {a1}. ¿Cuál es la nota agregada?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Suma nueva − suma anterior = {(n + 1)}·{a1} − {n}·{a0} = {x}.")


def t_needed(r, l):
    k = r.choice([3, 4])
    notes = [F(r.randint(8, 13), 2) for _ in range(k)]
    goal = F(r.choice([5, 11, 12, 10, 9]), 2) if False else F(r.randint(9, 12), 2)
    x = goal * (k + 1) - sum(notes)
    if not (1 <= x <= 7):
        raise Reject
    ns = ", ".join(nf(v) for v in notes)
    fig = card([f"Notas obtenidas: {ns}", f"Promedio buscado: {nf(goal)}", "Nota necesaria en la última prueba = ?"], 150, 17)
    ans = nf(x)
    al = uq(ans, [nf(goal), nf(x + F(1, 2)), nf(x - F(1, 2)), nf(goal * 2 - mean(notes) if goal * 2 - mean(notes) > 0 else x + 1), nf(x + 1), nf(mean(notes))])
    stem = f"Una estudiante tiene las notas {ns}. ¿Qué nota debe obtener en la última prueba para que su promedio de las {k + 1} notas sea {nf(goal)}?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Necesita una suma de {nf(goal * (k + 1))}; ya tiene {nf(sum(notes))}, luego le faltan {ans}.")


def t_leave(r, l):
    n = r.choice([5, 6, 9, 10])
    x = r.randint(2, 15)
    S = r.randint(6 * n, 12 * n)
    m0 = F(S, n)
    m1 = F(S - x, n - 1)
    a0, a1 = nf(m0), nf(m1)
    ans = a1
    fig = card([f"{n} personas, edad promedio {a0} años", f"Se retira una persona de {x} años", "Nuevo promedio = ?"], 150, 18)
    al = uq(ans, [a0, nf(m0 - x), nf(F(S, n - 1)), nf(m0 + F(x, n)), nf(m1 + 1), nf(m0 - F(x, n))])
    stem = f"El promedio de edad de {n} personas es {a0} años. Se retira una persona de {x} años. ¿Cuál es el nuevo promedio?"
    return make(stem, fig, ans, al[:4], Q_MOD, f"Suma original = {S}; sin la persona: {S - x}; nuevo promedio = {S - x}/{n - 1} = {a1}.")


CTX = [
    ("Los sueldos (en miles de $) de una empresa son 500, 520, 480, 510 y 4.500 (el gerente). Se quiere describir el sueldo típico.", "La mediana"),
    ("Una zapatería quiere decidir qué talla pedir más para el próximo mes, según las tallas vendidas.", "La moda"),
    ("Las alturas de 30 plantas de un mismo cultivo tienen una distribución simétrica y sin valores extremos. Se quiere el valor central de las alturas.", "La media"),
    ("Los precios de 6 casas de un barrio son similares, salvo una mansión mucho más cara. Se desea un precio representativo.", "La mediana"),
    ("Un restaurante desea saber cuál plato es el más pedido del menú.", "La moda"),
    ("Un profesor quiere resumir con un solo valor las notas de un curso, que no tienen valores extremos.", "La media"),
]


def t_measure(r, l):
    txt, ans = r.choice(CTX)
    fig = card(["Situación:", "elige la medida más adecuada", "(media, mediana o moda)"], 130, 18)
    al = [x for x in ["La media", "La mediana", "La moda", "El rango", "La suma"] if x != ans]
    return make(f"{txt} ¿Qué medida de tendencia central conviene usar?", fig, ans, al[:4], Q_MOD, "La mediana resiste valores extremos; la moda sirve para lo más frecuente; la media para datos simétricos.")


# ---------------------------------------------------------------- Representar
def _chart(r):
    labels = [str(v) for v in range(1, 7)]
    while True:
        f = [r.randint(1, 8) for _ in range(6)]
        m = uq_mode(f)
        if m is not None:
            return labels, f


def uq_mode(f):
    c = sorted(f, reverse=True)
    return None if c[0] == c[1] else f.index(c[0])


def t_read_chart(r, l):
    labels, f = _chart(r)
    fig = bar_chart(labels, f, (max(f) // 2 + 1) * 2, 2, ylab="Frecuencia")
    vals = list(range(1, 7))
    data = [v for v, k in zip(vals, f) for _ in range(k)]
    kind = r.choice(["mode", "median", "n"] if l else ["mode", "n"])
    if kind == "mode":
        ans = str(vals[f.index(max(f))])
        al = uq(ans, [str(max(f)), nf(median(data)), nf(mean(data)) if len(data) in (4, 5, 8, 10, 20, 25, 40, 50) or sum(data) % len(data) == 0 else str(vals[0]), str(vals[-1]), str(min(f))])
        stem = "El gráfico muestra la frecuencia de cada valor de una variable. ¿Cuál es la moda?"
    elif kind == "median":
        ans = nf(median(data))
        al = uq(ans, [str(vals[f.index(max(f))]), nf(F(sum(vals), 6)), str(len(data)), nf(median(data) + 1), nf(median(data) - 1)])
        stem = "El gráfico muestra la frecuencia de cada valor de una variable. ¿Cuál es la mediana de los datos?"
    else:
        ans = str(sum(f))
        al = uq(ans, [str(max(f)), str(sum(f) + 1), str(sum(f) - 1), str(sum(vals)), str(6 * max(f))])
        stem = "El gráfico muestra la frecuencia de cada valor de una variable. ¿Cuántos datos hay en total?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se lee cada barra como el número de veces que aparece cada valor.")


def t_table_med(r, l):
    vals = sorted(r.sample(range(1, 10), 4))
    n = r.choice([9, 11, 10, 12, 20])
    from clase45 import split
    fis = split(r, n, 4, 1)
    data = [v for v, k in zip(vals, fis) for _ in range(k)]
    fig = viz.table_fig(["Valor", "fi"], [[str(v), str(f)] for v, f in zip(vals, fis)] + [["Total", str(n)]])
    kind = r.choice(["median", "mode"])
    if kind == "median":
        ans = nf(median(data))
        al = uq(ans, [nf(F(sum(vals), 4)), str(vals[fis.index(max(fis))]), str(vals[1]), str(vals[2]), nf(median(data) + 1), str(n // 2)])
        stem = "La tabla muestra la distribución de un conjunto de datos. ¿Cuál es su mediana?"
    else:
        if uni_mode(data) is None: raise Reject
        ans = str(uni_mode(data))
        al = uq(ans, [str(max(fis)), nf(median(data)), str(vals[-1]), str(vals[0]), nf(F(sum(vals), 4))])
        stem = "La tabla muestra la distribución de un conjunto de datos. ¿Cuál es su moda?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se usan las frecuencias para ubicar la posición central y el valor más repetido.")


def t_match(r, l):
    while True:
        d = sorted(r.randint(1, 9) for _ in range(5))
        if mean(d).denominator == 1 and median(d) != mean(d):
            break
    m, md = mean(d), median(d)
    goods = dl(r.sample(d, 5))
    sets = [goods]
    for _ in range(60):
        e = [r.randint(1, 9) for _ in range(5)]
        s = dl(e)
        if s not in sets and not (mean(e) == m and median(e) == md) and (mean(e) == m or median(e) == md):
            sets.append(s)
        if len(sets) == 5:
            break
    if len(sets) < 5: raise Reject
    fig = card(["Conjunto de 5 datos:", f"Media = {nf(m)}", f"Mediana = {nf(md)}"], 130, 19)
    return make(f"¿Cuál de los siguientes conjuntos de 5 datos tiene media {nf(m)} y mediana {nf(md)}?", fig, goods, sets[1:], Q_REP, "Se verifican ambas medidas en cada conjunto.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Datos: 3, 9, 4, 8, 6", "Mediana = 4 (el dato del centro de la lista)"], "No ordenó los datos: ordenados son 3, 4, 6, 8, 9 y la mediana es 6", \
            ["Ordenó bien los datos, pero eligió el segundo valor en lugar del central", "Calculó el promedio de los dos primeros datos de la lista original", "Tomó el menor valor de la lista como si fuera la mediana de los datos", "Sumó todos los datos y dividió por dos para obtener el valor central"]
    if k == 1:
        return ["Datos: 2, 4, 4, 6, 9", "Moda = 2, porque es el menor"], "La moda es el valor que más se repite: el 4, que aparece dos veces", \
            ["La moda es el promedio de los datos, que en este caso vale 5", "La moda es el valor central de los datos ordenados, es decir, el 4", "La moda es el mayor valor de la lista, que en este caso es el 9", "La moda es la cantidad de veces que se repite un valor, es decir, 2"]
    if k == 2:
        return ["Datos: 4, 6, 8, 10", "Media = 4 + 6 + 8 + 10 = 28"], "Sumó los datos pero no dividió por la cantidad de datos: la media es 28/4 = 7", \
            ["Dividió la suma por 2 en lugar de dividirla por el número de datos", "Calculó la suma correctamente y también la media, pero olvidó la unidad", "Dividió la suma por el mayor valor de los datos en vez de por su cantidad", "Restó los datos en lugar de sumarlos antes de dividir por la cantidad"]
    return ["Sueldos: 400, 420, 450, 5.000", "Como la media es 1.567,5, es lo que gana una persona típica"], "La media está muy afectada por el valor extremo 5.000; la mediana (435) representa mejor el sueldo típico", \
        ["La media es siempre la mejor medida, porque usa todos los datos disponibles", "La moda representa mejor el sueldo típico porque es el valor de mayor frecuencia", "Ninguna medida sirve, porque hay un valor extremo entre los datos del conjunto", "La conclusión es correcta porque la media no depende de los valores extremos"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_effect(r, l):
    d = sorted(rdata(r, 5, 3, 12))
    if uni_mode(d) is not None and Counter(d)[uni_mode(d)] >= 2 and False: pass
    big = r.choice([50, 80, 100])
    fig = card([f"Datos: {dl(d)}", f"Se agrega el dato {big}"], 110, 19)
    ans = "La media aumenta bastante y la mediana casi no cambia"
    al = ["La media casi no cambia y la mediana aumenta bastante", "Tanto la media como la mediana aumentan en la misma cantidad", "La media y la mediana no cambian porque solo se agregó un dato", "La mediana aumenta mucho y la moda también aumenta"]
    return make("¿Qué ocurre con la media y la mediana al agregar el dato extremo indicado?", fig, ans, al, Q_ARG, "Un dato extremo afecta mucho a la media, pero poco a la mediana.")


TRUE = ["La media es la suma de los datos dividida por la cantidad de datos", "La mediana es el valor central de los datos ordenados", "La moda es el valor que más se repite", "Un conjunto de datos puede tener más de una moda",
        "La media se ve afectada por los valores extremos", "Si todos los datos son iguales, la media, la mediana y la moda coinciden"]
FALSE = ["La media es el valor que más se repite en un conjunto de datos", "La mediana se calcula sin ordenar los datos", "La moda es siempre el promedio de los datos", "Todo conjunto de datos tiene exactamente una moda",
         "La mediana se ve muy afectada por los valores extremos", "La media siempre es uno de los datos del conjunto"]


def _fig(r):
    return data_card(rdata(r, 8, 1, 15))


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre medidas de tendencia central es verdadera?", "Sobre media, mediana y moda, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre medidas de tendencia central es falsa?", "Sobre media, mediana y moda, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones.")


BY_SKILL = {
    Q_RES: [t_mean, t_median, t_mode, t_mean_table],
    Q_MOD: [t_new_value, t_needed, t_leave, t_measure],
    Q_REP: [t_read_chart, t_table_med, t_match],
    Q_ARG: [t_error, t_effect, t_true, t_false],
}
