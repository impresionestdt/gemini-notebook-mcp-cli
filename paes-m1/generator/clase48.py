"""Clase 48 (M1) · Medidas de tendencia central en datos agrupados: marca de clase, media, clase modal, intervalo de la mediana."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from sfigs import hist
import viz
from clase45 import uq, split
from clase47 import nf

VARS = [("Estatura (cm)", "estudiantes", [(140, 10), (150, 10), (160, 10)]), ("Tiempo de espera (min)", "clientes", [(0, 5), (5, 5), (10, 5)]),
        ("Edad (años)", "personas", [(20, 10), (30, 10), (40, 10)]), ("Puntaje en un ensayo", "estudiantes", [(200, 100), (300, 100), (400, 100)]),
        ("Peso (kg)", "personas", [(40, 10), (50, 10), (60, 10)]), ("Consumo eléctrico (kWh)", "hogares", [(100, 20), (120, 20), (140, 20)])]


def mk(r, k=None):
    name, unit, [(a, w), _, _] = r.choice(VARS)
    k = k or r.choice([4, 5])
    n = r.choice([20, 25, 40, 50])
    fis = split(r, n, k, 2)
    edges = [a + w * i for i in range(k + 1)]
    return name, unit, edges, fis, n, w


def iv(a, b):
    return f"[{a}, {b}["


def mc(edges, i):
    return F(edges[i] + edges[i + 1], 2)


def gtable(name, edges, fis, n, cols=("fi",), hide=None):
    hs = [name] + ["fi" if c == "fi" else "Fi" if c == "Fi" else "Marca" for c in cols]
    rows = []
    acc = 0
    for i, f in enumerate(fis):
        acc += f
        row = [iv(edges[i], edges[i + 1])]
        for c in cols:
            v = str(f) if c == "fi" else str(acc) if c == "Fi" else nf(mc(edges, i))
            if hide == (i, c): v = "?"
            row.append(v)
        rows.append(row)
    tot = ["Total"] + [str(n) if c == "fi" else "" for c in cols]
    rows.append(tot)
    return viz.table_fig(hs if len(name) < 22 else ["Variable"] + hs[1:], rows)


# ---------------------------------------------------------------- Resolver problemas
def t_mark(r, l):
    a = r.choice([0, 10, 20, 100, 140, 150, 200])
    w = r.choice([4, 5, 10, 20, 50])
    b = a + w
    m = F(a + b, 2)
    ans = nf(m)
    fig = card(["Intervalo de clase:", iv(a, b)], 110, 26)
    al = uq(ans, [nf(F(b - a, 2)), str(a), str(b), nf(m + F(w, 2)), nf(m - 1)])
    return make(f"¿Cuál es la marca de clase del intervalo {iv(a, b)}?", fig, ans, al[:4], Q_RES, f"({a} + {b})/2 = {ans}.")


def t_mean_g(r, l):
    name, unit, edges, fis, n, w = mk(r)
    fig = gtable(name, edges, fis, n)
    S = sum(mc(edges, i) * f for i, f in enumerate(fis))
    m = S / n
    ans = nf(m)
    lows = sum(F(edges[i]) * f for i, f in enumerate(fis)) / n
    al = uq(ans, [nf(lows), nf(F(sum(mc(edges, i) for i in range(len(fis))), len(fis))), nf(m + F(w, 2)), nf(m - F(w, 5)), nf(mc(edges, fis.index(max(fis)))), nf(m + w)])
    return make(f"La tabla muestra la variable «{name.lower()}» agrupada en intervalos. ¿Cuál es su media aproximada?", fig, ans, al[:4], Q_RES, f"Se usan las marcas de clase: Σ marca·fi / n = {nf(S)}/{n} = {ans}.")


def t_modal(r, l):
    name, unit, edges, fis, n, w = mk(r)
    if sorted(fis)[-1] == sorted(fis)[-2]: raise Reject
    i = fis.index(max(fis))
    fig = gtable(name, edges, fis, n)
    ans = iv(edges[i], edges[i + 1])
    al = uq(ans, [iv(edges[j], edges[j + 1]) for j in range(len(fis)) if j != i])
    return make(f"En la tabla, ¿cuál es la clase modal de «{name.lower()}»?", fig, ans, al[:4], Q_RES, "La clase modal es el intervalo con mayor frecuencia.")


def t_median_int(r, l):
    name, unit, edges, fis, n, w = mk(r)
    fig = gtable(name, edges, fis, n, ("fi", "Fi"))
    acc, half = 0, n / 2
    for i, f in enumerate(fis):
        acc += f
        if acc >= half:
            break
    ans = iv(edges[i], edges[i + 1])
    al = uq(ans, [iv(edges[j], edges[j + 1]) for j in range(len(fis)) if j != i])
    return make(f"En la tabla, ¿en cuál intervalo se encuentra la mediana de «{name.lower()}»?", fig, ans, al[:4], Q_RES, f"n/2 = {nf(F(n, 2))}; la primera Fi que lo alcanza está en {ans}.")


# ---------------------------------------------------------------- Modelar
def t_below(r, l):
    name, unit, edges, fis, n, w = mk(r)
    fig = gtable(name, edges, fis, n)
    k = r.randrange(1, len(fis))
    cnt = sum(fis[:k])
    x = edges[k]
    kind = r.choice(["cnt", "pct"]) if l else "cnt"
    if kind == "cnt":
        ans = str(cnt)
        al = uq(ans, [str(sum(fis[k:])), str(fis[k]), str(cnt + fis[k]), str(cnt - 1), str(n)])
        stem = f"La tabla agrupa a {n} {unit} según «{name.lower()}». ¿Cuántos tienen un valor menor que {x}?"
    else:
        p = F(100 * cnt, n)
        ans = nf(p) + " %"
        al = uq(ans, [nf(F(100 * sum(fis[k:]), n)) + " %", str(cnt) + " %", nf(F(100 * (cnt + fis[k]), n)) + " %", nf(F(100 * fis[k], n)) + " %"])
        stem = f"La tabla agrupa a {n} {unit} según «{name.lower()}». ¿Qué porcentaje tiene un valor menor que {x}?"
    return make(stem, fig, ans, al[:4], Q_MOD, "Se suman las frecuencias de los intervalos anteriores al valor indicado.")


def t_missing(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    k = r.randrange(4)
    shown = [str(f) if i != k else "?" for i, f in enumerate(fis)]
    rows = [[iv(edges[i], edges[i + 1]), s] for i, s in enumerate(shown)] + [["Total", str(n)]]
    fig = viz.table_fig([name if len(name) < 22 else "Variable", "fi"], rows)
    ans = str(fis[k])
    others = n - fis[k]
    al = uq(ans, [str(fis[k] + 1), str(fis[k] - 1), str(n // 4), str(others), str(fis[k] + 2)])
    return make(f"Se agrupó a {n} {unit} según «{name.lower()}». ¿Cuántos {unit} hay en el intervalo marcado con «?»", fig, ans, al[:4], Q_MOD, f"{n} − {others} = {fis[k]}.")


def t_est_total(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    S = sum(mc(edges, i) * f for i, f in enumerate(fis))
    m = S / n
    if l == 0 and m.denominator != 1: raise Reject
    fig = gtable(name, edges, fis, n, ("fi", "Marca"))
    tot = S
    ans = nf(tot)
    al = uq(ans, [nf(m), nf(S + w), nf(S - w), nf(sum(edges[:-1]) * 1), nf(n * w)])
    return make(f"La tabla muestra «{name.lower()}» de {n} {unit}, con sus marcas de clase. ¿Cuál es la suma aproximada de todos los valores?", fig, ans, al[:4], Q_MOD, "Suma aproximada = Σ marca·fi.")


def t_compare_g(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    m1 = sum(mc(edges, i) * f for i, f in enumerate(fis)) / n
    fis2 = split(r, n, 4, 2)
    m2 = sum(mc(edges, i) * f for i, f in enumerate(fis2)) / n
    if m1 == m2: raise Reject
    rows = [[iv(edges[i], edges[i + 1]), str(fis[i]), str(fis2[i])] for i in range(4)]
    fig = viz.table_fig([name if len(name) < 22 else "Variable", "Grupo A", "Grupo B"], rows + [["Total", str(n), str(n)]])
    ans = "Grupo A" if m1 > m2 else "Grupo B"
    al = ["Grupo B" if m1 > m2 else "Grupo A", "Ambos tienen la misma media", "No se puede saber sin conocer los datos originales"]
    return make(f"Dos grupos de {n} {unit} se agruparon en los mismos intervalos. ¿Cuál grupo tiene mayor media aproximada?", fig, ans, al + ["El que tiene mayor clase modal"], Q_MOD, f"A: {nf(m1)}; B: {nf(m2)} (usando marcas de clase).")


# ---------------------------------------------------------------- Representar
def t_read_hist(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    ym = (max(fis) // 5 + 1) * 5
    fig = hist(edges, fis, ym, 5, ylab="Frecuencia")
    kind = r.choice(["modal", "n", "mark"])
    if kind == "modal":
        if sorted(fis)[-1] == sorted(fis)[-2]: raise Reject
        i = fis.index(max(fis))
        ans = iv(edges[i], edges[i + 1])
        al = uq(ans, [iv(edges[j], edges[j + 1]) for j in range(4) if j != i])
        stem = f"El histograma muestra «{name.lower()}». ¿Cuál es la clase modal?"
    elif kind == "n":
        ans = str(n)
        al = uq(ans, [str(max(fis)), str(n + 5), str(n - 5), str(sum(edges)), str(fis[0] + fis[1])])
        stem = f"El histograma muestra «{name.lower()}». ¿Cuántos {unit} se consideran en total?"
    else:
        i = r.randrange(4)
        ans = nf(mc(edges, i))
        al = uq(ans, [str(edges[i]), str(edges[i + 1]), nf(mc(edges, i) + w), str(fis[i]), nf(mc(edges, i) - w // 2)])
        stem = f"En el histograma, ¿cuál es la marca de clase de la barra correspondiente al intervalo {iv(edges[i], edges[i + 1])}?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se lee el histograma: altura = frecuencia; marca = punto medio del intervalo.")


def t_mc_list(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    fig = gtable(name, edges, fis, n)
    ans = ", ".join(nf(mc(edges, i)) for i in range(4))
    al = uq(ans, [", ".join(nf(F(edges[i])) for i in range(4)), ", ".join(nf(F(edges[i + 1])) for i in range(4)), ", ".join(nf(mc(edges, i) + w // 2 if w % 2 == 0 else mc(edges, i) + 1) for i in range(4)), ", ".join(nf(F(w, 2) * (i + 1)) for i in range(4))])
    return make("¿Cuál lista contiene las marcas de clase de los cuatro intervalos de la tabla, en orden?", fig, ans, al[:4], Q_REP, "Marca de clase = (límite inferior + límite superior)/2.")


def t_Fi(r, l):
    name, unit, edges, fis, n, w = mk(r)
    k = r.randrange(1, len(fis) - 1)
    fig = gtable(name, edges, fis, n, ("fi", "Fi"), hide=(k, "Fi"))
    acc = sum(fis[:k + 1])
    ans = str(acc)
    al = uq(ans, [str(fis[k]), str(acc - fis[0]), str(acc + 1), str(n - acc), str(sum(fis[:k]))])
    return make("La tabla muestra una distribución agrupada. ¿Qué valor corresponde a «?» en la columna de frecuencia acumulada (Fi)?", fig, ans, al[:4], Q_REP, "Fi es la suma de las frecuencias hasta ese intervalo.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Intervalo [20, 30[", "Marca de clase = 30 − 20 = 10"], "Restó los límites: la marca de clase es el promedio (20 + 30)/2 = 25", \
            ["Usó el límite inferior 20 en lugar de calcular el punto medio del intervalo", "Usó el límite superior 30 en lugar de calcular el punto medio del intervalo", "Sumó los límites pero olvidó dividir por 2 al calcular la marca de clase", "Dividió la diferencia de los límites por 2 y obtuvo el ancho del intervalo"]
    if k == 1:
        return ["Intervalos con fi: 4, 10, 6", "Clase modal: el último intervalo, porque es el mayor"], "La clase modal es la de mayor frecuencia (10), no la de mayores valores", \
            ["La clase modal es la del centro, porque siempre corresponde al valor medio", "La clase modal es la de menor frecuencia, porque es la menos común", "La clase modal es la de mayor marca de clase, como indicó el estudiante", "La clase modal es la primera, porque los datos comienzan en ese intervalo"]
    if k == 2:
        return ["Marcas: 15, 25, 35 con fi: 2, 6, 2", "Media = (15 + 25 + 35)/3 = 25 con eso basta"], "Coincide por casualidad; en general debe ponderar cada marca por su frecuencia: Σ marca·fi/n", \
            ["Debe dividir por la suma de las marcas de clase en lugar de la cantidad", "Debe usar los límites inferiores de cada intervalo en lugar de las marcas", "Está correcto en general, porque la media siempre se calcula sin las frecuencias", "Debe multiplicar las marcas entre sí antes de dividir por la cantidad de clases"]
    return ["n = 30, Fi: 8, 20, 30", "El intervalo de la mediana es el 1.º, porque tiene Fi = 8"], "La mediana está en el primer intervalo cuya Fi alcanza n/2 = 15, que es el 2.º", \
        ["El intervalo de la mediana es el 3.º porque tiene la acumulada total de 30 datos", "El intervalo de la mediana es el 1.º, pues 8 es el menor de los valores acumulados", "El intervalo de la mediana es el de mayor frecuencia absoluta de la tabla dada", "La mediana no se puede ubicar en una tabla con datos agrupados en intervalos"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    name, unit, edges, fis, n, w = mk(r, 4)
    if sorted(fis)[-1] == sorted(fis)[-2]: raise Reject
    fig = gtable(name, edges, fis, n)
    i = fis.index(max(fis))
    j = r.choice([x for x in range(4) if x != i])
    ans = r.choice([f"La clase modal es {iv(edges[i], edges[i + 1])}", f"El {nf(F(100 * fis[j], n))} % de los datos está en {iv(edges[j], edges[j + 1])}"])
    al = [f"La clase modal es {iv(edges[j], edges[j + 1])}", f"El {nf(F(100 * fis[j] + 500, n))} % de los datos está en {iv(edges[j], edges[j + 1])}", f"La marca de clase de {iv(edges[j], edges[j + 1])} es {edges[j + 1]}", f"Hay {n + 5} datos en total", f"La marca de clase de {iv(edges[i], edges[i + 1])} es {edges[i]}"]
    return make("Según la tabla, ¿cuál de las siguientes afirmaciones es verdadera?", fig, ans, al[:4], Q_ARG, "Se verifica cada afirmación con la tabla.")


TRUE = ["La marca de clase es el punto medio de un intervalo", "La clase modal es el intervalo de mayor frecuencia", "La media de datos agrupados es una aproximación que usa las marcas de clase",
        "El intervalo de la mediana es el primero cuya frecuencia acumulada alcanza n/2", "La última frecuencia acumulada es igual al total de datos", "Al agrupar datos se pierde información sobre los valores exactos"]
FALSE = ["La marca de clase es el límite inferior de cada intervalo", "La clase modal es el intervalo con mayor marca de clase", "La media de datos agrupados es siempre igual a la media de los datos originales",
         "El intervalo de la mediana es siempre el intervalo central de la tabla", "La última frecuencia acumulada es siempre 1", "Al agrupar datos se puede recuperar cada valor exacto de la muestra"]


def _fig(r):
    name, unit, edges, fis, n, w = mk(r)
    return gtable(name, edges, fis, n)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre datos agrupados es verdadera?", "Sobre datos agrupados en intervalos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre datos agrupados es falsa?", "Sobre datos agrupados en intervalos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones.")


BY_SKILL = {
    Q_RES: [t_mark, t_mean_g, t_modal, t_median_int],
    Q_MOD: [t_below, t_missing, t_est_total, t_compare_g],
    Q_REP: [t_read_hist, t_mc_list, t_Fi],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
