"""Clase 45 (M1) · Tablas de frecuencia: absoluta, relativa, porcentual y acumulada."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from num import dstr
import viz

CATS = [("Deporte favorito", ["Fútbol", "Básquetbol", "Tenis", "Natación", "Vóleibol"]),
        ("Medio de transporte", ["Bus", "Metro", "Auto", "Bicicleta", "A pie"]),
        ("Mascota preferida", ["Perro", "Gato", "Ave", "Pez", "Conejo"]),
        ("Asignatura favorita", ["Matemática", "Lenguaje", "Historia", "Ciencias", "Arte"]),
        ("Fruta preferida", ["Manzana", "Plátano", "Naranja", "Uva", "Frutilla"]),
        ("Género musical", ["Pop", "Rock", "Cumbia", "Reguetón", "Clásica"])]
NUMV = [("Número de hermanos", "hermanos", [0, 1, 2, 3, 4]), ("Libros leídos en el mes", "libros", [0, 1, 2, 3, 4]),
        ("Miembros del hogar", "personas", [2, 3, 4, 5, 6]), ("Goles por partido", "goles", [0, 1, 2, 3, 4])]
NS = [20, 25, 40, 50, 100, 200]


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is not None and a not in seen:
            seen.add(a); out.append(a)
    return out


def pc(fi, n):
    return dstr(F(100 * fi, n)) + " %"


def dec(fi, n):
    return dstr(F(fi, n))


def split(r, n, k, lo=2):
    while True:
        cuts = sorted(r.sample(range(1, n), k - 1))
        fis = [b - a for a, b in zip([0] + cuts, cuts + [n])]
        if min(fis) >= lo and len(set(fis)) >= k - 1:
            return fis


def cat_table(r, n=None, k=None, cols="f"):
    title, cats = r.choice(CATS)
    k = k or r.choice([4, 5])
    n = n or r.choice(NS)
    cats = r.sample(cats, k)
    fis = split(r, n, k, max(2, n // 10))
    return title, cats, fis, n


def table(title, cats, fis, n, cols=("fi",), hide=None):
    """cols: subconjunto ordenado de fi, fr, pct, Fi."""
    head = {"fi": "fi", "fr": "fr", "pct": "%", "Fi": "Fi"}
    hs = [title if len(cols) == 1 else "Categoría"] + [head[c] for c in cols]
    rows = []
    acc = 0
    for i, (c, f) in enumerate(zip(cats, fis)):
        acc += f
        row = [c]
        for cl in cols:
            v = {"fi": str(f), "fr": dec(f, n), "pct": pc(f, n), "Fi": str(acc)}[cl]
            if hide == (i, cl):
                v = "?"
            row.append(v)
        rows.append(row)
    tot = ["Total"]
    for cl in cols:
        tot.append({"fi": str(n), "fr": "1", "pct": "100 %", "Fi": ""}[cl])
    rows.append(tot)
    return viz.table_fig(hs, rows)


# ---------------------------------------------------------------- Resolver problemas
def t_count(r, l):
    title, unit, vals = r.choice(NUMV)
    n = r.choice([16, 20, 25])
    data = [r.choice(vals) for _ in range(n)]
    v = r.choice(vals)
    f = data.count(v)
    if f < 2 or f > n // 2:
        raise Reject
    lines = [", ".join(map(str, data[:n // 2])) + ",", ", ".join(map(str, data[n // 2:]))]
    fig = card([f"{title} ({n} datos):"] + lines, 60 + 40 * 3, 18)
    kind = r.choice(["fi", "fr"] if l else ["fi"])
    if kind == "fi":
        ans = str(f)
        al = uq(ans, [str(f + 1), str(f - 1), str(n - f), dec(f, n), str(v), str(f + 2)])
        stem = f"Se registró la variable «{title.lower()}» en {n} personas (datos de la figura). ¿Cuál es la frecuencia absoluta del valor {v}?"
        ex = f"Se cuentan las veces que aparece el {v}: {f}."
    else:
        ans = pc(f, n)
        al = uq(ans, [pc(f + 1, n), dec(f, n), str(f), pc(n - f, n), pc(f, n + 5) if False else pc(f + 2, n)])
        stem = f"Se registró la variable «{title.lower()}» en {n} personas (datos de la figura). ¿Qué porcentaje de las personas tiene el valor {v}?"
        ex = f"{f}/{n} = {dec(f, n)} = {pc(f, n)}."
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_fr(r, l):
    title, cats, fis, n = cat_table(r)
    k = r.randrange(len(cats))
    fig = table(title, cats, fis, n, ("fi",))
    kind = r.choice(["dec", "pct"]) if l else "pct"
    f = fis[k]
    if kind == "pct":
        ans = pc(f, n)
        al = uq(ans, [dec(f, n), str(f) + " %", pc(n - f, n), dec(f, n) + " %", pc(f + 1, n)])
        what = "el porcentaje"
    else:
        ans = dec(f, n)
        al = uq(ans, [pc(f, n), str(f), dec(n - f, n), dec(f + 1, n), dec(f + 2, n)])
        what = "la frecuencia relativa (como decimal)"
    return make(f"La tabla muestra las preferencias de {n} personas. ¿Cuál es {what} de «{cats[k]}»?", fig, ans, al[:4], Q_RES, f"fr = {f}/{n} = {dec(f, n)} = {pc(f, n)}.")


def t_cum(r, l):
    title, cats, fis, n = cat_table(r)
    k = r.randrange(1, len(cats) - 1)
    fig = table(title, cats, fis, n, ("fi",))
    Fk = sum(fis[:k + 1])
    kind = r.choice(["abs", "pct"]) if l else "abs"
    if kind == "abs":
        ans = str(Fk)
        al = uq(ans, [str(fis[k]), str(n - Fk), str(Fk + fis[k + 1]), str(Fk - fis[0]), str(sum(fis[k:]))])
        stem = f"La tabla muestra los datos de {n} personas. ¿Cuántas personas eligieron alguna de las categorías desde «{cats[0]}» hasta «{cats[k]}» (ambas incluidas)?"
    else:
        ans = pc(Fk, n)
        al = uq(ans, [pc(fis[k], n), pc(n - Fk, n), str(Fk) + " %", pc(sum(fis[:k]), n), pc(Fk + fis[k + 1], n)])
        stem = f"La tabla muestra los datos de {n} personas. ¿Qué porcentaje eligió alguna de las categorías desde «{cats[0]}» hasta «{cats[k]}» (ambas incluidas)?"
    return make(stem, fig, ans, al[:4], Q_RES, "Se suman las frecuencias de las categorías indicadas.")


def t_missing(r, l):
    title, cats, fis, n = cat_table(r)
    k = r.randrange(len(cats))
    shown = [str(f) if i != k else "?" for i, f in enumerate(fis)]
    rows = [[c, s] for c, s in zip(cats, shown)] + [["Total", str(n)]]
    fig = viz.table_fig([title, "fi"], rows)
    ans = str(fis[k])
    al = uq(ans, [str(n - sum(fis) + fis[k] + 5), str(fis[k] + 1), str(fis[k] - 1), str(n // len(cats)), str(sum(f for i, f in enumerate(fis) if i != k)), str(fis[k] + 2)])
    return make(f"La tabla resume una encuesta a {n} personas. ¿Qué frecuencia corresponde a «?»", fig, ans, al[:4], Q_RES, f"Falta {n} − {sum(f for i, f in enumerate(fis) if i != k)} = {fis[k]}.")


# ---------------------------------------------------------------- Modelar
def t_survey(r, l):
    n = r.choice(NS)
    p = r.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45]) if l else r.choice([10, 20, 25, 30, 40, 50])
    if (n * p) % 100:
        raise Reject
    f = n * p // 100
    what = r.choice(["prefiere estudiar en la mañana", "usa bicicleta para venir al colegio", "practica un deporte", "tiene mascota"])
    fig = card([f"Personas encuestadas: {n}", f"Porcentaje que {what.split(' ')[0]}…: {p} %", "Cantidad = ?"], 150, 18) if False else card([f"Personas encuestadas: {n}", f"Porcentaje de respuestas afirmativas: {p} %", "Número de personas = ?"], 150, 18)
    ans = str(f)
    al = uq(ans, [str(p), str(f + n // 10), str(n - f), str(f * 2), str(n // p if n % p == 0 else f + 3), str(f + 1)])
    return make(f"En una encuesta a {n} personas, el {p} % respondió que {what}. ¿Cuántas personas respondieron eso?", fig, ans, al[:4], Q_MOD, f"{p} % de {n} = {n}·{dec(p, 100)} = {f}.")


def t_total(r, l):
    n = r.choice([20, 40, 50, 80, 100, 200, 250])
    p = r.choice([10, 20, 25, 40, 50, 5, 30])
    if (n * p) % 100:
        raise Reject
    f = n * p // 100
    fig = card([f"{f} personas corresponden al {p} %", "Total de personas = ?"], 120, 19)
    ans = str(n)
    al = uq(ans, [str(f * p if f * p != n else n + 10), str(f + p), str(100 - p), str(f * 2), str(f * 10), str(n + 20)])
    return make(f"En un curso, {f} estudiantes representan el {p} % del total. ¿Cuántos estudiantes hay en el curso?", fig, ans, al[:4], Q_MOD, f"Si {p} % es {f}, el 100 % es {f}·100/{p} = {n}.")


def t_atleast(r, l):
    title, unit, vals = r.choice(NUMV)
    n = r.choice([20, 25, 40, 50])
    fis = split(r, n, 5, 2)
    fig = viz.table_fig([title, "fi"], [[str(v), str(f)] for v, f in zip(vals, fis)] + [["Total", str(n)]])
    k = r.randrange(1, 4)
    kind = r.choice(["least", "most"])
    if kind == "least":
        cnt = sum(fis[k:])
        txt = f"al menos {vals[k]} {unit}"
        alt = sum(fis[k + 1:])
    else:
        cnt = sum(fis[:k + 1])
        txt = f"a lo más {vals[k]} {unit}"
        alt = sum(fis[:k])
    if l == 2:
        ans = pc(cnt, n)
        al = uq(ans, [pc(alt, n), pc(fis[k], n), pc(n - cnt, n), str(cnt) + " %", pc(cnt + 1, n)])
        stem = f"La tabla muestra la variable «{title.lower()}» en {n} personas. ¿Qué porcentaje de ellas tiene {txt}?"
    else:
        ans = str(cnt)
        al = uq(ans, [str(alt), str(fis[k]), str(n - cnt), str(cnt + fis[k]), str(cnt + 1)])
        stem = f"La tabla muestra la variable «{title.lower()}» en {n} personas. ¿Cuántas de ellas tienen {txt}?"
    return make(stem, fig, ans, al[:4], Q_MOD, "Se suman las frecuencias que cumplen la condición.")


def t_compare(r, l):
    (na, fa), (nb, fb) = [(r.choice([20, 25, 40, 50]), 0), (r.choice([20, 25, 40, 50, 100]), 0)]
    if na == nb:
        raise Reject
    fa = r.randint(3, na - 3); fb = r.randint(3, nb - 3)
    pa, pb = F(fa, na), F(fb, nb)
    if pa == pb:
        raise Reject
    fig = viz.table_fig(["Curso", "Aprobados", "Total"], [["A", str(fa), str(na)], ["B", str(fb), str(nb)]])
    ans = "El curso A" if pa > pb else "El curso B"
    al = ["El curso B" if pa > pb else "El curso A", "Ambos tienen el mismo porcentaje", "El curso con más estudiantes en total", "No se puede saber con esos datos"]
    if (fa > fb) == (pa > pb):
        al[2] = "El curso con menos aprobados"
    stem = f"En dos cursos se registró cuántos estudiantes aprobaron. ¿Cuál curso tiene mayor porcentaje de aprobación?"
    return make(stem, fig, ans, al, Q_MOD, f"A: {pc(fa, na)}; B: {pc(fb, nb)}. Se compara con frecuencias relativas, no absolutas.")


# ---------------------------------------------------------------- Representar
def t_read(r, l):
    title, cats, fis, n = cat_table(r)
    fig = table(title, cats, fis, n, ("fi", "fr", "pct"))
    k = r.randrange(len(cats))
    f = fis[k]
    kind = r.choice(["pct", "fi", "fr"])
    if kind == "pct":
        ans = pc(f, n)
        al = uq(ans, [dec(f, n), str(f), pc(f + 1, n), pc(fis[(k + 1) % len(cats)], n)])
        stem = f"En la tabla, ¿qué porcentaje de las personas eligió «{cats[k]}»?"
    elif kind == "fi":
        ans = str(f)
        al = uq(ans, [pc(f, n), dec(f, n), str(f + 1), str(fis[(k + 1) % len(cats)])])
        stem = f"En la tabla, ¿cuántas personas eligieron «{cats[k]}»?"
    else:
        ans = dec(f, n)
        al = uq(ans, [pc(f, n), str(f), dec(f + 1, n), dec(fis[(k + 1) % len(cats)], n)])
        stem = f"En la tabla, ¿cuál es la frecuencia relativa de «{cats[k]}»?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se lee la columna correspondiente a la categoría.")


def t_complete(r, l):
    title, cats, fis, n = cat_table(r)
    k = r.randrange(1, len(cats))
    col = r.choice(["Fi", "pct", "fr"])
    fig = table(title, cats, fis, n, ("fi", col), hide=(k, col))
    acc = sum(fis[:k + 1])
    if col == "Fi":
        ans = str(acc)
        al = uq(ans, [str(fis[k]), str(acc - fis[0]), str(acc + 1), str(n - acc), str(sum(fis[:k]))])
        what = "frecuencia acumulada (Fi)"
    elif col == "pct":
        ans = pc(fis[k], n)
        al = uq(ans, [dec(fis[k], n), str(fis[k]) + " %", pc(fis[k] + 1, n), pc(acc, n), pc(n - fis[k], n)])
        what = "porcentaje"
    else:
        ans = dec(fis[k], n)
        al = uq(ans, [pc(fis[k], n), str(fis[k]), dec(fis[k] + 1, n), dec(acc, n), dec(n - fis[k], n)])
        what = "frecuencia relativa"
    return make(f"La tabla muestra una distribución de {n} datos. ¿Qué valor corresponde a «?» en la columna de {what}?", fig, ans, al[:4], Q_REP, f"Se calcula a partir de la frecuencia absoluta y el total {n}.")


def t_angle(r, l):
    title, cats, fis, n = cat_table(r)
    k = r.randrange(len(cats))
    ang = F(360 * fis[k], n)
    if ang.denominator != 1:
        raise Reject
    fig = table(title, cats, fis, n, ("fi",))
    ans = f"{ang}°"
    al = uq(ans, [f"{F(100 * fis[k], n)}°" if F(100 * fis[k], n).denominator == 1 else None, f"{fis[k]}°", f"{360 - ang}°", f"{ang // 2}°" if ang % 2 == 0 else f"{ang + 10}°", f"{ang + 20}°", f"{ang * 2}°"])
    return make(f"Con los datos de la tabla se construirá un gráfico circular. ¿Qué ángulo debe tener el sector de «{cats[k]}»?", fig, ans, al[:4], Q_REP, f"Ángulo = 360°·{fis[k]}/{n} = {ang}°.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["40 estudiantes, 8 eligen «Tenis»", "fr = 40/8 = 5"], "Invirtió el cociente: la frecuencia relativa es 8/40 = 0,2", \
            ["Dividió bien, pero olvidó multiplicar por 100 para expresarlo como porcentaje", "Restó la frecuencia al total en lugar de dividirla por el total", "Usó la frecuencia acumulada en lugar de usar la frecuencia absoluta", "Sumó las frecuencias de todas las categorías antes de calcular la razón"]
    if k == 1:
        return ["fi: 6, 9, 5, 10 (n = 30)", "Fi: 6, 9, 5, 10"], "Copió la frecuencia absoluta: la acumulada es 6, 15, 20, 30", \
            ["Sumó todas las frecuencias en cada fila, por lo que repitió el total en cada una", "Restó cada frecuencia de la anterior en lugar de sumarlas de forma sucesiva", "Calculó bien las frecuencias acumuladas, pero olvidó anotar la última fila", "Acumuló las frecuencias desde el último dato hacia el primero de la tabla"]
    if k == 2:
        return ["Frecuencias relativas: 0,25 · 0,30 · 0,35 · 0,20", "Suman 1,10, pero está bien"], "Las frecuencias relativas deben sumar 1: hay un error en al menos una de ellas", \
            ["Las frecuencias relativas deben sumar 100, no 1, por lo que hay un error", "Las frecuencias relativas pueden sumar cualquier valor mayor que 1 sin problema", "Solo las frecuencias absolutas deben sumar el total de datos de la muestra", "La suma es correcta porque cada frecuencia relativa es menor que uno por sí sola"]
    return ["Curso A: 12 de 20 aprueban; curso B: 15 de 30", "B tiene más aprobados, luego mejor porcentaje"], "Comparó frecuencias absolutas; debía comparar 12/20 = 60 % con 15/30 = 50 %", \
        ["Comparó bien los porcentajes, pero interpretó al revés cuál curso es mejor", "Sumó los aprobados de ambos cursos antes de comparar sus resultados", "Dividió los aprobados por el total del otro curso al calcular el porcentaje", "Consideró que 15 de 30 es mayor que 12 de 20 al comparar las fracciones"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    title, cats, fis, n = cat_table(r, k=5)
    fig = table(title, cats, fis, n, ("fi",))
    order = sorted(range(5), key=lambda i: -fis[i])
    top, low = order[0], order[-1]
    if fis[order[0]] == fis[order[1]] or fis[order[-1]] == fis[order[-2]]:
        raise Reject
    i, j = r.sample(range(5), 2)
    true_pool = [f"«{cats[top]}» es la categoría más frecuente", f"«{cats[low]}» es la categoría menos frecuente", f"«{cats[i]}» y «{cats[j]}» reúnen el {pc(fis[i] + fis[j], n)} de los datos"]
    wrong_j = (fis[i] + fis[j] + max(2, n // 10))
    false_pool = [f"«{cats[low]}» es la categoría más frecuente", f"«{cats[top]}» es la categoría menos frecuente", f"«{cats[i]}» y «{cats[j]}» reúnen el {pc(wrong_j, n)} de los datos",
                  f"«{cats[top]}» tiene una frecuencia relativa mayor que 1", f"«{cats[low]}» tiene más de la mitad de los datos" if 2 * fis[low] <= n else f"«{cats[top]}» tiene menos de un décimo de los datos",
                  f"Las frecuencias absolutas suman {n + 5}"]
    ans = r.choice(true_pool)
    al = false_pool[:]
    r.shuffle(al)
    return make("Con la información de la tabla, ¿cuál de las siguientes afirmaciones es verdadera?", fig, ans, al[:4], Q_ARG, "Se verifica cada afirmación con las frecuencias de la tabla.")


TRUE = ["La suma de las frecuencias relativas de una distribución es 1", "La frecuencia acumulada de la última categoría es igual al total de datos", "La frecuencia relativa se obtiene dividiendo la frecuencia absoluta por el total de datos",
        "El porcentaje de una categoría es su frecuencia relativa multiplicada por 100", "La frecuencia acumulada nunca disminuye al avanzar en la tabla", "Las frecuencias absolutas suman el total de datos"]
FALSE = ["La suma de las frecuencias relativas de una distribución es igual al total de datos", "La frecuencia acumulada de la primera categoría es igual al total de datos", "La frecuencia relativa se obtiene multiplicando la frecuencia absoluta por el total",
         "El porcentaje de una categoría es su frecuencia absoluta dividida por 100", "La frecuencia acumulada puede disminuir al avanzar en la tabla", "Las frecuencias relativas pueden ser negativas"]


def _fig(r):
    title, cats, fis, n = cat_table(r)
    return table(title, cats, fis, n, ("fi", "fr"))


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre tablas de frecuencia es verdadera?", "Sobre tablas de frecuencia, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones de frecuencia.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre tablas de frecuencia es falsa?", "Sobre tablas de frecuencia, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones de frecuencia.")


BY_SKILL = {
    Q_RES: [t_count, t_fr, t_cum, t_missing],
    Q_MOD: [t_survey, t_total, t_atleast, t_compare],
    Q_REP: [t_read, t_complete, t_angle],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
