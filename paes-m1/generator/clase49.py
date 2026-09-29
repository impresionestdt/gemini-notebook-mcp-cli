"""Clase 49 (M1) · Cuartiles, percentiles y diagrama de cajón (caja y bigotes)."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from sfigs import boxplot
import viz
from clase45 import uq
from clase47 import nf, dl, median, data_card


def quartiles(d):
    s = sorted(d); n = len(s)
    lo = s[:n // 2]
    hi = s[(n + 1) // 2:]
    return median(lo), median(s), median(hi)


def five(d):
    s = sorted(d)
    q1, q2, q3 = quartiles(d)
    return s[0], q1, q2, q3, s[-1]


def rdata(r, n, lo=2, hi=40):
    while True:
        d = [r.randint(lo, hi) for _ in range(n)]
        if len(set(d)) >= n - 1:
            return d


def box_vals(r):
    while True:
        v = sorted(r.sample(range(1, 11), 5))
        return tuple(5 * x for x in v)


# ---------------------------------------------------------------- Resolver problemas
def t_quart(r, l):
    n = r.choice([8, 12] if l == 0 else [8, 12, 7, 11])
    d = rdata(r, n)
    q = quartiles(d)
    k = r.randrange(3)
    ans = nf(q[k])
    s = sorted(d)
    al = uq(ans, [nf(q[(k + 1) % 3]), nf(q[(k + 2) % 3]), nf(s[n // 4 * (k + 1) - 1]) if n // 4 * (k + 1) - 1 < n else None, nf(F(sum(d), n)) if (n in (8,) or sum(d) % n == 0) else None, nf(q[k] + 1), nf(q[k] - 1), nf(s[0] if k == 0 else s[-1])])
    note = "" if n % 2 == 0 else " (en cantidad impar de datos, la mediana no se incluye en ninguna mitad)"
    stem = f"¿Cuál es el cuartil {k + 1} (Q{k + 1}) de los datos de la figura?{note}"
    return make(stem, data_card(d), ans, al[:4], Q_RES, f"Ordenados: {dl(s)}. Q1, Q2, Q3 = {nf(q[0])}, {nf(q[1])}, {nf(q[2])}.")


def t_iqr(r, l):
    n = r.choice([8, 12, 16])
    d = rdata(r, n)
    q = quartiles(d)
    iqr = q[2] - q[0]
    ans = nf(iqr)
    s = sorted(d)
    al = uq(ans, [nf(s[-1] - s[0]), nf(q[2]), nf(q[2] + q[0]), nf(q[1] - q[0]), nf(iqr + 1), nf(q[2] - q[1])])
    return make("¿Cuál es el rango intercuartil (Q3 − Q1) de los datos de la figura?", data_card(d), ans, al[:4], Q_RES, f"Q3 − Q1 = {nf(q[2])} − {nf(q[0])} = {ans}.")


def t_range_five(r, l):
    n = r.choice([8, 12])
    d = rdata(r, n)
    f = five(d)
    kind = r.choice(["range", "min", "max"])
    if kind == "range":
        ans = nf(f[4] - f[0])
        al = uq(ans, [nf(f[3] - f[1]), nf(f[4]), nf(f[0]), nf(f[4] + f[0]), nf(f[2])])
        stem = "¿Cuál es el rango (máximo − mínimo) de los datos de la figura?"
    else:
        ans = nf(f[0] if kind == "min" else f[4])
        al = uq(ans, [nf(f[1]), nf(f[2]), nf(f[3]), nf(f[4] if kind == "min" else f[0])])
        stem = f"¿Cuál es el valor {'mínimo' if kind == 'min' else 'máximo'} de los datos de la figura?"
    return make(stem, data_card(d), ans, al[:4], Q_RES, "Se ordenan los datos y se toman los extremos.")


def t_pct_count(r, l):
    n = r.choice([40, 50, 60, 80, 100, 200, 400])
    p = r.choice([10, 20, 25, 50, 75, 90] if l else [25, 50, 75])
    if (n * p) % 100: raise Reject
    val = n * p // 100
    fig = card([f"Total de estudiantes: {n}", f"Un puntaje corresponde al percentil {p}", "Estudiantes con puntaje menor = ?"], 150, 18)
    ans = str(val)
    al = uq(ans, [str(n - val), str(p), str(val + n // 10), str(n // p if n % p == 0 else val + 2), str(val * 2 if val * 2 < n else val + 5)])
    return make(f"Un estudiante obtuvo un puntaje que corresponde al percentil {p} en un grupo de {n} estudiantes. Aproximadamente, ¿cuántos estudiantes obtuvieron un puntaje menor?", fig, ans, al[:4], Q_RES, f"El percentil {p} deja bajo sí al {p} % de los datos: {p} % de {n} = {val}.")


# ---------------------------------------------------------------- Modelar
def t_pct_rank(r, l):
    n = r.choice([200, 400, 500, 1000])
    p = r.choice([10, 20, 30, 40, 60, 70, 80, 90])
    val = n * (100 - p) // 100
    fig = card([f"Postulantes: {n}", f"Tu puntaje está en el percentil {p}", "Postulantes con puntaje mayor = ?"], 150, 18)
    ans = str(val)
    al = uq(ans, [str(n * p // 100), str(100 - p), str(val + n // 10), str(n // 2), str(val - n // 20)])
    return make(f"Un postulante está en el percentil {p} entre {n} postulantes. Aproximadamente, ¿cuántos obtuvieron un puntaje mayor que el suyo?", fig, ans, al[:4], Q_MOD, f"Superan su puntaje el {100 - p} % de {n} = {val}.")


def t_wait(r, l):
    n = r.choice([8, 12, 16])
    d = rdata(r, n, 3, 40)
    q = quartiles(d)
    fig = data_card(d, "Tiempos de espera (min):")
    k = r.choice([0, 2])
    if k == 0:
        cnt = sum(1 for x in d if x < q[0]) if False else n // 4
        ans = str(n // 4)
        al = uq(ans, [str(n // 2), str(n * 3 // 4), str(n // 4 + 1), str(n // 4 - 1), str(n)])
        stem = f"Los tiempos de espera de {n} clientes se muestran en la figura. Aproximadamente, ¿cuántos clientes esperaron menos que el primer cuartil?"
    else:
        ans = str(n // 4)
        al = uq(ans, [str(n // 2), str(n * 3 // 4), str(n // 4 + 1), str(n // 4 - 1), str(n)])
        stem = f"Los tiempos de espera de {n} clientes se muestran en la figura. Aproximadamente, ¿cuántos clientes esperaron más que el tercer cuartil?"
    return make(stem, fig, ans, al[:4], Q_MOD, "Cada cuartil deja aproximadamente un cuarto de los datos a cada lado.")


def t_fence(r, l):
    n = r.choice([8, 12])
    while True:
        d = rdata(r, n, 10, 30)
        q = quartiles(d)
        iqr = q[2] - q[0]
        if iqr >= 2: break
    up = q[2] + F(3, 2) * iqr
    big = int(up) + r.randint(2, 8)
    d2 = d[:-1] + [big]
    q2 = quartiles(d2)
    if q2 != q: raise Reject
    up = q[2] + F(3, 2) * (q[2] - q[0])
    if big <= up: raise Reject
    fig = data_card(d2, "Datos:")
    ans = nf(up)
    al = uq(ans, [nf(q[2]), nf(q[2] + iqr), nf(q[2] + 3 * iqr), nf(up + 1), nf(big)])
    return make(f"Un dato se considera atípico si supera Q3 + 1,5·(Q3 − Q1). Con los datos de la figura, ¿cuál es ese límite superior?", fig, ans, al[:4], Q_MOD, f"Q1 = {nf(q[0])}, Q3 = {nf(q[2])}: límite = {nf(q[2])} + 1,5·{nf(iqr)} = {ans}.")


def t_compare_box(r, l):
    a = box_vals(r); b = box_vals(r)
    if a == b or a[2] == b[2]: raise Reject
    fig = boxplot(a, 0, 55, 5)
    body = ""
    ans = "El grupo A tiene mayor mediana" if a[2] > b[2] else "El grupo B tiene mayor mediana"
    rows = [["Grupo A"] + [str(x) for x in a], ["Grupo B"] + [str(x) for x in b]]
    fig = viz.table_fig(["", "Mín", "Q1", "Q2", "Q3", "Máx"], rows)
    al = ["El grupo B tiene mayor mediana" if a[2] > b[2] else "El grupo A tiene mayor mediana", "Ambos grupos tienen la misma mediana", "El grupo con mayor máximo tiene mayor mediana"] if False else ["El grupo B tiene mayor mediana" if a[2] > b[2] else "El grupo A tiene mayor mediana", "Ambos grupos tienen la misma mediana", "El grupo con menor rango tiene mayor mediana", "No se puede comparar con esos datos"]
    return make("La tabla resume las puntuaciones de dos grupos (mínimo, cuartiles y máximo). ¿Cuál afirmación es correcta?", fig, ans, al, Q_MOD, "La mediana de cada grupo es su Q2.")


# ---------------------------------------------------------------- Representar
def t_read_box(r, l):
    v = box_vals(r)
    fig = boxplot(v, 0, 55, 5)
    names = ["el valor mínimo", "el primer cuartil (Q1)", "la mediana", "el tercer cuartil (Q3)", "el valor máximo"]
    kind = r.choice(["val", "val", "iqr", "range"] if l else ["val"])
    if kind == "val":
        k = r.randrange(5)
        ans = str(v[k])
        al = uq(ans, [str(x) for x in v if x != v[k]] + [str(v[k] + 5)])
        stem = f"En el diagrama de caja y bigotes, ¿cuál es {names[k]}?"
    elif kind == "iqr":
        ans = str(v[3] - v[1])
        al = uq(ans, [str(v[4] - v[0]), str(v[3]), str(v[3] - v[2]), str(v[2] - v[1]), str(v[3] - v[1] + 5)])
        stem = "En el diagrama de caja y bigotes, ¿cuál es el rango intercuartil?"
    else:
        ans = str(v[4] - v[0])
        al = uq(ans, [str(v[3] - v[1]), str(v[4]), str(v[0]), str(v[4] - v[0] + 5), str(v[2])])
        stem = "En el diagrama de caja y bigotes, ¿cuál es el rango de los datos?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se leen los extremos y los bordes de la caja sobre el eje.")


def t_box_pct(r, l):
    v = box_vals(r)
    fig = boxplot(v, 0, 55, 5)
    kind = r.choice([("entre Q1 y Q3", 50), ("entre el mínimo y la mediana", 50), ("por debajo de Q1", 25), ("por encima de Q3", 25), ("por encima de la mediana", 50), ("entre Q1 y la mediana", 25)])
    ans = f"{kind[1]} %"
    al = uq(ans, ["25 %", "50 %", "75 %", "100 %", "10 %"])
    return make(f"En un diagrama de caja y bigotes, ¿qué porcentaje aproximado de los datos se ubica {kind[0]}?", fig, ans, al[:4], Q_REP, "Cada tramo entre cuartiles consecutivos reúne aproximadamente el 25 % de los datos.")


def t_summary(r, l):
    n = r.choice([8, 12])
    d = rdata(r, n, 2, 30)
    f = five(d)
    ans = " · ".join(nf(x) for x in f)
    s = sorted(d)
    al = []
    for _ in range(40):
        g = list(f)
        i = r.randrange(1, 4)
        g[i] = g[i] + r.choice([-2, -1, 1, 2])
        if g[0] <= g[1] <= g[2] <= g[3] <= g[4]:
            t = " · ".join(nf(x) for x in g)
            if t != ans and t not in al: al.append(t)
    al.append(" · ".join(nf(x) for x in (f[0], f[3], f[2], f[1], f[4])) if f[1] != f[3] else "")
    al = [x for x in al if x]
    return make("¿Cuál es el resumen de cinco números (mínimo · Q1 · mediana · Q3 · máximo) de los datos de la figura?", data_card(d), ans, al[:4], Q_REP, f"Datos ordenados: {dl(s)}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Datos: 2, 5, 7, 9, 12, 14, 15, 20", "Q1 = 2 (el menor dato)"], "Confundió Q1 con el mínimo: Q1 es la mediana de la mitad inferior, (5 + 7)/2 = 6", \
            ["Tomó el primer dato de la mitad superior de los datos ordenados como valor de Q1", "Calculó la mediana de todos los datos en lugar de la mediana de la mitad inferior", "Sumó el mínimo y el máximo y lo dividió por dos, obteniendo el punto medio", "Tomó el segundo dato de la lista, pero debía elegir el tercer dato de ella"]
    if k == 1:
        return ["Percentil 80 de un puntaje", "Significa que el 80 % obtuvo más puntaje"], "El percentil 80 deja bajo sí al 80 %: solo el 20 % obtuvo un puntaje mayor", \
            ["Significa que obtuvo el 80 % del puntaje máximo posible en la prueba realizada", "Significa que el 80 % de los datos son iguales al puntaje de esa persona", "La conclusión es correcta, porque un percentil alto indica que hubo más puntaje", "Significa que el 20 % obtuvo un puntaje menor que el de esa persona evaluada"]
    if k == 2:
        return ["Diagrama de caja: Q1 = 10, Q3 = 30", "La caja contiene el 25 % de los datos"], "La caja va de Q1 a Q3, por lo que contiene aproximadamente el 50 % de los datos", \
            ["La caja contiene el 75 % de los datos, porque abarca tres cuartos de ellos", "La caja contiene el 100 % de los datos, porque los bigotes son parte de ella", "La conclusión es correcta, ya que cada cuartil contiene el 25 % de los datos", "La caja contiene el 20 % de los datos, porque su ancho es de 20 unidades"]
    return ["Rango intercuartil de los datos", "IQR = máximo − mínimo"], "El rango intercuartil es Q3 − Q1; máximo − mínimo es el rango", \
        ["El rango intercuartil es Q3 − mediana, que mide solo la mitad superior de la caja", "El rango intercuartil es la mediana − Q1, que mide solo la mitad inferior de la caja", "El rango intercuartil es la suma de Q1 y Q3, dividida por dos, que es el promedio", "La definición del estudiante es correcta porque el rango incluye a todos los datos"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    v = box_vals(r)
    fig = boxplot(v, 0, 55, 5)
    ans = r.choice([f"La mediana es {v[2]}", f"El 50 % central de los datos está entre {v[1]} y {v[3]}", f"El rango de los datos es {v[4] - v[0]}"])
    al = [f"La mediana es {v[3]}", f"El 50 % central de los datos está entre {v[0]} y {v[4]}", f"El rango de los datos es {v[3] - v[1]}", f"El primer cuartil es {v[0]}", f"El tercer cuartil es {v[4]}"]
    return make("Según el diagrama de caja y bigotes, ¿cuál afirmación es verdadera?", fig, ans, al[:4], Q_ARG, "Se lee cada valor en el eje horizontal.")


TRUE = ["La mediana coincide con el segundo cuartil", "Entre Q1 y Q3 se ubica aproximadamente el 50 % de los datos", "El percentil 50 es la mediana", "El rango intercuartil se calcula como Q3 − Q1",
        "El percentil 90 deja bajo sí aproximadamente al 90 % de los datos", "Los bigotes de un diagrama de caja llegan hasta los valores mínimo y máximo"]
FALSE = ["El primer cuartil es siempre el menor dato del conjunto", "Entre Q1 y Q3 se ubica aproximadamente el 25 % de los datos", "El percentil 50 es el valor máximo",
         "El rango intercuartil se calcula como máximo − mínimo", "El percentil 90 deja bajo sí aproximadamente al 10 % de los datos", "La mediana siempre está exactamente en el centro de la caja"]


def _fig(r):
    return boxplot(box_vals(r), 0, 55, 5)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre cuartiles y percentiles es verdadera?", "Sobre cuartiles, percentiles y cajas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre cuartiles y percentiles es falsa?", "Sobre cuartiles, percentiles y cajas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones.")


BY_SKILL = {
    Q_RES: [t_quart, t_iqr, t_range_five, t_pct_count],
    Q_MOD: [t_pct_rank, t_wait, t_fence, t_compare_box],
    Q_REP: [t_read_box, t_box_pct, t_summary],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
