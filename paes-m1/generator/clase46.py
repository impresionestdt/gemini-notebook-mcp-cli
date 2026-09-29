"""Clase 46 (M1) · Gráficos estadísticos: barras, circular, histograma y líneas."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from num import dstr
from figs import pie_chart, hbars_pct
from sfigs import bar_chart, hist, line_chart
import viz
from clase45 import CATS, uq

MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun"]
QUANT = [("Ventas de helados", "helados"), ("Visitas a la biblioteca", "visitas"), ("Entradas vendidas", "entradas"), ("Libros prestados", "libros"), ("Botellas recicladas", "botellas")]
HISTV = [("Estatura (cm)", [140, 150, 160, 170, 180], "estudiantes"), ("Tiempo de estudio (min)", [0, 20, 40, 60, 80], "estudiantes"), ("Edad (años)", [10, 20, 30, 40, 50], "personas"), ("Puntaje", [0, 20, 40, 60, 80], "estudiantes")]


def bars(r, k=5, lo=1, hi=8, step=None):
    step = step or r.choice([5, 10])
    title, cats = r.choice(CATS)
    cats = r.sample(cats, k)
    vals = [step * r.randint(lo, hi) for _ in range(k)]
    return title, cats, vals, step


def ymax_of(vals, step):
    m = max(vals)
    return (m // step + 1) * step if m % step == 0 else (m // step + 2) * step


# ---------------------------------------------------------------- Resolver problemas
def t_bar_read(r, l):
    title, cats, vals, step = bars(r)
    if len(set(vals)) < 4:
        raise Reject
    ym = ymax_of(vals, step)
    k = r.randrange(5)
    kind = r.choice(["val", "diff", "sum"] if l else ["val", "diff"])
    fig = bar_chart(cats, vals, ym, step, show=(kind != "val"), hl=k if kind == "val" else None, ylab="Personas")
    if kind == "val":
        stem = f"El gráfico muestra {title.lower()} en un grupo de personas. ¿Cuántas personas eligieron «{cats[k]}» (barra destacada)?"
        val = vals[k]
        al = [val + step, val - step if val > step else val + 2 * step, val + step // 2, val * 2, sum(vals)]
    elif kind == "diff":
        i, j = r.sample(range(5), 2)
        val = abs(vals[i] - vals[j])
        if val == 0: raise Reject
        stem = f"El gráfico muestra {title.lower()} en un grupo de personas. ¿Cuál es la diferencia entre las personas que eligieron «{cats[i]}» y las que eligieron «{cats[j]}»?"
        al = [vals[i] + vals[j], val + step, max(1, val - step), max(vals[i], vals[j]), val * 2]
    else:
        i, j = r.sample(range(5), 2)
        val = vals[i] + vals[j]
        stem = f"El gráfico muestra {title.lower()} en un grupo de personas. ¿Cuántas personas eligieron «{cats[i]}» o «{cats[j]}»?"
        al = [abs(vals[i] - vals[j]), val + step, val - step, sum(vals), max(vals[i], vals[j])]
    ans = str(val)
    return make(stem, fig, ans, uq(ans, [str(a) for a in al if a > 0])[:4], Q_RES, "Se leen las alturas de las barras y se opera con ellas.")


def t_pie(r, l):
    title, cats = r.choice(CATS)
    k = r.choice([4, 5])
    cats = r.sample(cats, k)
    while True:
        ps = [5 * r.randint(2, 8) for _ in range(k - 1)]
        last = 100 - sum(ps)
        if last >= 5 and last % 5 == 0 and last <= 40:
            ps.append(last); break
    fig = pie_chart([(c, f"{p}%", p) for c, p in zip(cats, ps)])
    n = r.choice([40, 60, 80, 100, 120, 200, 400])
    i = r.randrange(k)
    kind = r.choice(["count", "sum"] if l else ["count"])
    if kind == "count":
        if (n * ps[i]) % 100: raise Reject
        val = n * ps[i] // 100
        stem = f"El gráfico circular muestra {title.lower()} de {n} personas. ¿Cuántas personas eligieron «{cats[i]}»?"
        al = [ps[i], n - val, val + n // 10, val * 2, n // ps[i] if n % ps[i] == 0 else val + 3]
    else:
        j = (i + 1 + r.randrange(k - 1)) % k
        pc_ = ps[i] + ps[j]
        if (n * pc_) % 100: raise Reject
        val = n * pc_ // 100
        stem = f"El gráfico circular muestra {title.lower()} de {n} personas. ¿Cuántas personas eligieron «{cats[i]}» o «{cats[j]}»?"
        al = [pc_, n - val, val + n // 10, abs(ps[i] - ps[j]) * n // 100, val * 2]
    ans = str(val)
    return make(stem, fig, ans, uq(ans, [str(a) for a in al if a > 0])[:4], Q_RES, "Se aplica el porcentaje de cada sector al total de personas.")


def _hist(r):
    t, edges, unit = r.choice(HISTV)
    vals = [r.randint(1, 8) * 2 for _ in range(4)]
    return t, edges, unit, vals


def t_hist(r, l):
    t, edges, unit, vals = _hist(r)
    fig = hist(edges, vals, 20, 2, ylab="Frecuencia")
    kind = r.choice(["total", "range", "atleast"] if l else ["total", "range"])
    if kind == "total":
        val = sum(vals)
        stem = f"El histograma muestra la variable «{t}» en un grupo. ¿Cuántos {unit} se consideraron en total?"
        al = [max(vals), val + 2, val - 2, val // 2, val + vals[0]]
    elif kind == "range":
        i = r.randrange(4)
        val = vals[i]
        stem = f"El histograma muestra la variable «{t}». ¿Cuántos {unit} hay en el intervalo [{edges[i]}, {edges[i + 1]}[?"
        al = [vals[(i + 1) % 4], val + 2, val - 2 if val > 2 else val + 4, sum(vals), edges[i]]
    else:
        i = r.randrange(1, 4)
        val = sum(vals[i:])
        stem = f"El histograma muestra la variable «{t}». ¿Cuántos {unit} tienen un valor de {edges[i]} o más?"
        al = [sum(vals[:i]), sum(vals[i + 1:]) if i < 3 else val + 2, vals[i], val + 2, sum(vals)]
    ans = str(val)
    return make(stem, fig, ans, uq(ans, [str(a) for a in al if a > 0])[:4], Q_RES, "Se suman las frecuencias de las barras indicadas.")


def t_line(r, l):
    t, unit = r.choice(QUANT)
    vals = [20 * r.randint(1, 7) for _ in range(6)]
    if len(set(vals)) < 5: raise Reject
    ym = ymax_of(vals, 20)
    fig = line_chart(MONTHS, vals, ym, 20, show=False, ylab=unit.capitalize())
    kind = r.choice(["val", "change", "max"] if l else ["val", "change"])
    if kind == "val":
        i = r.randrange(6); val = vals[i]
        stem = f"El gráfico muestra la evolución de «{t.lower()}». ¿Cuántas {unit} hubo en {MONTHS[i]}?"
        al = [val + 20, val - 20 if val > 20 else val + 40, val + 10, vals[(i + 1) % 6], sum(vals)]
    elif kind == "change":
        i = r.randrange(5); val = vals[i + 1] - vals[i]
        if val == 0: raise Reject
        stem = f"El gráfico muestra la evolución de «{t.lower()}». ¿Cuál fue la variación entre {MONTHS[i]} y {MONTHS[i + 1]}? (Un aumento es positivo y una disminución, negativa.)"
        ans = f"{'+' if val > 0 else '−'}{abs(val)}"
        al = [f"{'+' if -val > 0 else '−'}{abs(val)}", f"{'+' if val > 0 else '−'}{abs(val) + 10}", f"{'+' if val > 0 else '−'}{abs(val) + 20}", f"{vals[i + 1]}", f"{vals[i]}"]
        return make(stem, fig, ans, uq(ans, al)[:4], Q_RES, "Variación = valor final − valor inicial.")
    else:
        diffs = [vals[i + 1] - vals[i] for i in range(5)]
        i = max(range(5), key=lambda k: diffs[k])
        if sorted(diffs)[-1] == sorted(diffs)[-2]: raise Reject
        ans = f"Entre {MONTHS[i]} y {MONTHS[i + 1]}"
        al = [f"Entre {MONTHS[j]} y {MONTHS[j + 1]}" for j in range(5) if j != i]
        return make(f"El gráfico muestra la evolución de «{t.lower()}». ¿En qué período hubo el mayor aumento?", fig, ans, al[:4], Q_RES, "Se busca el tramo de mayor pendiente ascendente.")
    ans = str(val)
    return make(stem, fig, ans, uq(ans, [str(a) for a in al if a > 0])[:4], Q_RES, "Se lee el valor del punto sobre el eje vertical.")


# ---------------------------------------------------------------- Modelar
def t_more(r, l):
    title, cats, vals, step = bars(r, 4, 1, 6)
    i, j = r.sample(range(4), 2)
    if vals[i] % vals[j] or vals[i] == vals[j]:
        raise Reject
    fig = bar_chart(cats, vals, ymax_of(vals, step), step, ylab="Personas")
    k = vals[i] // vals[j]
    ans = f"{k} veces"
    al = uq(ans, [f"{k + 1} veces", f"{k * 2} veces", f"{max(1, k - 1)} veces", f"{vals[i] - vals[j]} veces"])
    return make(f"El gráfico muestra {title.lower()}. ¿Cuántas veces más personas eligieron «{cats[i]}» que «{cats[j]}»?", fig, ans, al[:4], Q_MOD, f"{vals[i]} : {vals[j]} = {k}.")


def t_pie_ctx(r, l):
    title, cats = r.choice(CATS)
    cats = r.sample(cats, 4)
    ps = r.choice([[40, 30, 20, 10], [25, 35, 15, 25], [50, 20, 20, 10], [30, 30, 25, 15], [45, 25, 20, 10]])
    fig = pie_chart([(c, f"{p}%", p) for c, p in zip(cats, ps)])
    n = r.choice([80, 120, 200, 240, 400, 500])
    i, j = r.sample(range(4), 2)
    stem = f"En una encuesta a {n} personas sobre {title.lower()} se obtuvo el gráfico circular. ¿Cuántas más eligieron «{cats[i]}» que «{cats[j]}»?"
    d = n * abs(ps[i] - ps[j]) // 100
    if ps[i] <= ps[j] or (n * abs(ps[i] - ps[j])) % 100: raise Reject
    ans = str(d)
    al = uq(ans, [str(abs(ps[i] - ps[j])), str(n * ps[i] // 100), str(n * ps[j] // 100), str(d + n // 20), str(d * 2)])
    return make(stem, fig, ans, al[:4], Q_MOD, f"({ps[i]} % − {ps[j]} %) de {n} = {d}.")


def t_line_pct(r, l):
    t, unit = r.choice(QUANT)
    a = r.choice([100, 200, 400, 50, 80])
    p = r.choice([10, 20, 25, 50, 5])
    if (a * p) % 100: raise Reject
    b = a + a * p // 100
    vals = [a, b] + [a + 20 * r.randint(0, 5) for _ in range(2)]
    fig = line_chart(["Mar", "Abr"], [a, b], ymax_of([a, b], 50 if a >= 100 else 20), 50 if a >= 100 else 20, show=True, ylab=unit.capitalize())
    ans = f"{p} %"
    al = uq(ans, [f"{b - a} %", f"{p + 10} %", f"{p // 2 if p % 2 == 0 else p + 5} %", f"{100 * b // a} %" if (100 * b) % a == 0 else f"{p * 2} %", f"{p + 5} %"])
    return make(f"El gráfico muestra las {unit} de marzo y abril. ¿Qué porcentaje aumentaron de marzo a abril?", fig, ans, al[:4], Q_MOD, f"({b} − {a})/{a} = {dstr(F(b - a, a))} = {p} %.")


def t_hist_pct(r, l):
    t, edges, unit, vals = _hist(r)
    n = sum(vals)
    i = r.randrange(4)
    p = F(100 * vals[i], n)
    if p.denominator != 1: raise Reject
    fig = hist(edges, vals, 20, 2, ylab="Frecuencia")
    ans = f"{p} %"
    al = uq(ans, [f"{vals[i]} %", f"{F(100 * (n - vals[i]), n)} %" if (100 * (n - vals[i])) % n == 0 else None, f"{p + 5} %", f"{p - 5} %", f"{p * 2} %"])
    return make(f"El histograma muestra «{t}». ¿Qué porcentaje del total se ubica en el intervalo [{edges[i]}, {edges[i + 1]}[?", fig, ans, al[:4], Q_MOD, f"{vals[i]}/{n} = {p} %.")


# ---------------------------------------------------------------- Representar
CH = ["Gráfico de barras", "Histograma", "Gráfico de líneas", "Gráfico circular"]


def t_which(r, l):
    kinds = [
        ("Tabla: deporte favorito y número de estudiantes", "Gráfico de barras", "categorías sin orden natural", ["Fútbol 12", "Tenis 8", "Natación 5", "Vóleibol 9"]),
        ("Tabla: estatura agrupada en intervalos y frecuencia", "Histograma", "variable numérica agrupada en intervalos", ["[150, 160[   6", "[160, 170[   11", "[170, 180[   8", "[180, 190[   3"]),
        ("Tabla: mes y temperatura media", "Gráfico de líneas", "evolución de un dato en el tiempo", ["Enero 24", "Febrero 23", "Marzo 20", "Abril 16"]),
        ("Tabla: partes de un presupuesto (% del total)", "Gráfico circular", "partes de un todo que suman 100 %", ["Arriendo 40 %", "Comida 30 %", "Transporte 20 %", "Otros 10 %"]),
    ]
    t, ans, why, rows = r.choice(kinds)
    fig = viz.table_fig(["Dato", "Valor"], [x.rsplit(" ", 1) if "%" not in x else [x[:-4].strip(), x[-4:].strip()] for x in rows])
    al = [c for c in CH if c != ans] + ["Diagrama de caja y bigotes"]
    return make(f"Para representar los datos de la tabla, ¿qué gráfico es el más adecuado? ({t})", fig, ans, al, Q_REP, f"Se trata de {why}.")


def t_read_hbars(r, l):
    title, cats = r.choice(CATS)
    cats = r.sample(cats, 4)
    ps = [5 * r.randint(2, 12) for _ in range(4)]
    if len(set(ps)) < 4: raise Reject
    fig = hbars_pct(list(zip(cats, ps)), top=max(ps) + 10)
    i = r.randrange(4)
    ans = f"{ps[i]} %"
    al = uq(ans, [f"{ps[i] + 5} %", f"{ps[i] - 5} %", f"{ps[(i + 1) % 4]} %", f"{ps[i] // 5} %", f"{ps[i] + 10} %"])
    return make(f"El gráfico de barras horizontales muestra los porcentajes de preferencia. ¿Qué porcentaje corresponde a «{cats[i]}»?", fig, ans, al[:4], Q_REP, "Se lee el valor rotulado en la barra.")


def t_pie_frac(r, l):
    title, cats = r.choice(CATS)
    cats = r.sample(cats, 4)
    ps = r.choice([[50, 25, 15, 10], [25, 25, 30, 20], [40, 30, 20, 10], [20, 50, 20, 10], [30, 30, 30, 10]])
    fig = pie_chart([(c, f"{p}%", p) for c, p in zip(cats, ps)])
    i = r.randrange(4)
    fr = F(ps[i], 100)
    ans = f"{fr.numerator}/{fr.denominator}"
    al = uq(ans, [f"{ps[i]}/{100 - ps[i]}" if F(ps[i], 100 - ps[i]) != fr else None, f"{fr.denominator}/{fr.numerator}", f"{fr.numerator}/{fr.denominator + 1}", f"{fr.numerator + 1}/{fr.denominator}", f"{ps[i]}/10"])
    return make(f"En el gráfico circular, ¿qué fracción del total (simplificada) representa «{cats[i]}»?", fig, ans, al[:4], Q_REP, f"{ps[i]} % = {ps[i]}/100 = {ans}.")


def t_angle_pie(r, l):
    title, cats = r.choice(CATS)
    cats = r.sample(cats, 4)
    ps = r.choice([[50, 25, 15, 10], [25, 25, 30, 20], [40, 30, 20, 10], [20, 50, 20, 10], [30, 30, 30, 10], [45, 25, 20, 10]])
    fig = pie_chart([(c, f"{p}%", p) for c, p in zip(cats, ps)])
    i = r.randrange(4)
    ang = F(360 * ps[i], 100)
    if ang.denominator != 1: raise Reject
    ans = f"{ang}°"
    al = uq(ans, [f"{ps[i]}°", f"{360 - ang}°", f"{ang + 18}°", f"{ang - 18}°", f"{ang * 2}°"])
    return make(f"En el gráfico circular, ¿cuántos grados mide el ángulo del sector «{cats[i]}»?", fig, ans, al[:4], Q_REP, f"360°·{ps[i]}/100 = {ang}°.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    if k == 0:
        return ["Gráfico circular de 4 sectores", "Sectores: 40 %, 30 %, 20 %, 25 %"], "Los porcentajes suman 115 %: en un gráfico circular deben sumar 100 %", \
            ["Los porcentajes son correctos, porque cada sector es menor que el 50 %", "Falta un quinto sector para que la suma de los porcentajes sea 100 %", "El sector de 25 % debería ser el mayor porque es el último de la lista", "Los sectores deben ser todos iguales en un gráfico circular de cuatro partes"]
    if k == 1:
        return ["Gráfico de barras: ventas de 120 y 130", "La barra de 130 es el doble de alta que la de 120"], "El eje vertical no parte de 0, lo que exagera la diferencia; 130 es solo un poco más que 120", \
            ["La barra de 130 es el doble porque 130 es el doble de 65 en la escala", "Las barras no se pueden comparar porque tienen colores distintos", "La conclusión es correcta porque la barra mayor siempre es el doble de la menor", "La diferencia es de 30 unidades, por lo que una barra es el triple de la otra"]
    if k == 2:
        return ["Histograma: [0, 10[ → 6, [10, 20[ → 9", "Hay 15 personas con valor exacto 10"], "El histograma agrupa datos en intervalos: no permite saber cuántos tienen exactamente el valor 10", \
            ["Hay 9 personas con valor exacto 10, que es la frecuencia de su intervalo", "Hay 6 personas con valor exacto 10, que es la frecuencia del intervalo anterior", "La conclusión es correcta porque 6 + 9 = 15 y todos los datos valen 10 exacto", "No se puede saber nada porque los histogramas no muestran frecuencias en absoluto"]
    return ["Gráfico de líneas: 100 en enero y 150 en febrero", "El aumento fue de 150 %"], "El aumento fue de 50 unidades sobre 100, es decir, de 50 %, no de 150 %", \
        ["El aumento fue de 100 %, porque 150 − 50 = 100 según su cálculo del cambio", "El aumento fue de 30 %, porque 50 es el 30 % de 150 según la proporción", "El aumento fue de 150 %, porque el valor final es 150 y eso es el aumento", "El aumento fue de 50 unidades, pero no se puede expresar como porcentaje jamás"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_claim(r, l):
    title, cats, vals, step = bars(r)
    order = sorted(range(5), key=lambda i: -vals[i])
    if vals[order[0]] == vals[order[1]] or vals[order[-1]] == vals[order[-2]]:
        raise Reject
    fig = bar_chart(cats, vals, ymax_of(vals, step), step, ylab="Personas")
    top, low = order[0], order[-1]
    i, j = r.sample(range(5), 2)
    ans = r.choice([f"«{cats[top]}» es la opción más elegida", f"«{cats[low]}» es la opción menos elegida", f"«{cats[i]}» y «{cats[j]}» suman {vals[i] + vals[j]} personas"])
    al = [f"«{cats[low]}» es la opción más elegida", f"«{cats[top]}» es la opción menos elegida", f"«{cats[i]}» y «{cats[j]}» suman {vals[i] + vals[j] + step} personas", f"«{cats[top]}» y «{cats[low]}» tienen igual número de personas", f"Todas las opciones fueron elegidas por {vals[i]} personas"]
    return make("Según el gráfico de barras, ¿cuál afirmación es verdadera?", fig, ans, al[:4], Q_ARG, "Se verifica cada afirmación con las alturas de las barras.")


TRUE = ["Un gráfico circular representa partes de un todo que suman 100 %", "Un histograma agrupa datos numéricos en intervalos", "Un gráfico de líneas es adecuado para mostrar la evolución en el tiempo",
        "En un gráfico de barras, la altura de cada barra representa una frecuencia", "En un gráfico circular, un sector del 25 % mide 90°", "En un gráfico de barras, las barras deben partir desde el valor cero"]
FALSE = ["Un gráfico circular es el mejor para mostrar la evolución de datos en el tiempo", "En un histograma, las barras están siempre separadas por espacios", "En un gráfico circular, un sector del 25 % mide 25°",
         "Un gráfico de barras solo puede representar datos numéricos agrupados", "Los sectores de un gráfico circular pueden sumar cualquier porcentaje", "En un histograma, cada barra corresponde a una categoría sin orden"]


def _fig(r):
    title, cats, vals, step = bars(r)
    return bar_chart(cats, vals, ymax_of(vals, step), step, ylab="Personas")


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre gráficos estadísticos es verdadera?", "Sobre gráficos estadísticos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las características de cada gráfico.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre gráficos estadísticos es falsa?", "Sobre gráficos estadísticos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las características de los gráficos.")


BY_SKILL = {
    Q_RES: [t_bar_read, t_pie, t_hist, t_line],
    Q_MOD: [t_more, t_pie_ctx, t_line_pct, t_hist_pct],
    Q_REP: [t_which, t_read_hbars, t_pie_frac, t_angle_pie],
    Q_ARG: [t_error, t_claim, t_true, t_false],
}
