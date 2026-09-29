"""Clase 6 (M1) · Porcentajes I: concepto y cálculo rápido; lectura de gráficos."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import pie_chart, hbars_pct, grid_shaded
from num import dstr


def pf(x):
    x = F(x)
    s = dstr(x) if (x.denominator in (1, 2, 4, 5, 8, 10, 20, 25, 50, 100)) else fs(x)
    return s + "%"


def n_(x):
    return f"{int(x):,}".replace(",", ".")


def uqs(ans, alts, fmt):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        try:
            s = fmt(a)
        except Exception:
            continue
        if s not in seen and not ("/" in s and "/" not in ans and "%" in s):
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver problemas
def t_pct_of(r, l):
    kind = r.choice(["of", "what", "whole"] if l else ["of", "what"])
    if l == 2 and r.random() < 0.3:
        kind = "chain"
    if kind == "of":
        x = r.choice([10, 20, 25, 50, 5, 15, 30, 40, 75] if l == 0 else [12, 15, 35, 45, 60, 8, 2, 65])
        N = r.choice([40, 60, 80, 120, 160, 200, 240, 300, 400, 500, 800])
        val = F(N * x, 100)
        if val.denominator != 1:
            raise Reject
        txt = f"{x}% de {N}"
        fig = card(["Calcula:", txt], 120, 24)
        alts = [N * x, F(N, x), N + val, N - val, val * 10, val / 10, x + N]
        fm = lambda a: fs(F(a))
        ans = fs(val)
        return make("¿Cuál es el valor de lo pedido en la figura?", fig, ans, pick4(ans, uqs(ans, alts, fm)), Q_RES, f"{x}% de {N} = {N}·{x}/100 = {ans}.")
    if kind == "what":
        b = r.choice([20, 40, 50, 60, 80, 120, 150, 200, 250, 400])
        pct = r.choice([5, 10, 15, 20, 25, 30, 40, 60, 75, 80] if l < 2 else [12.5, 37.5, 62.5, 6, 45, 35])
        a = F(b) * F(str(pct)) / 100
        if a.denominator != 1:
            raise Reject
        fig = card([f"{a} es una parte de {b}"], 110, 24)
        alts = [F(b, a) * 100, F(a, b), a * b / 100, 100 - F(str(pct)), F(str(pct)) * 2]
        ans = pf(F(str(pct)))
        return make(f"¿Qué porcentaje de {b} es {a}?", fig, ans, pick4(ans, uqs(ans, [F(x) if not isinstance(x, F) else x for x in [F(b, a) * 100, a / b, a * b / 100, 100 - F(str(pct)), F(str(pct)) * 2]], lambda v: pf(F(v)))), Q_RES, f"{a}/{b} = {pf(F(str(pct)))}.")
    if kind == "whole":
        x = r.choice([10, 20, 25, 40, 50, 5, 30, 60, 75, 12, 15])
        W = r.choice([80, 120, 160, 200, 240, 300, 400, 500, 600])
        a = F(W * x, 100)
        if a.denominator != 1:
            raise Reject
        fig = card([f"{a} es el {x}% de un número"], 110, 24)
        alts = [a * x / 100, a + x, a * x, F(a, x), W - a, W * 2]
        ans = str(W)
        return make(f"El {x}% de un número es {a}. ¿Cuál es el número?", fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_RES, f"Número = {a}·100/{x} = {W}.")
    x1, x2 = r.choice([(20, 50), (50, 40), (25, 60), (10, 50), (40, 25)])
    N = r.choice([400, 600, 800, 1000, 1200])
    val = F(N * x1 * x2, 10000)
    if val.denominator != 1:
        raise Reject
    fig = card(["Calcula:", f"El {x1}% del {x2}% de {N}"], 130, 22)
    alts = [F(N * (x1 + x2), 100), F(N * x1, 100), F(N * x2, 100), val * 10, F(N * x1 * x2, 100)]
    ans = fs(val)
    return make("¿Cuál es el valor de lo pedido en la figura?", fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_RES, f"Primero el {x2}% de {N} = {fs(F(N * x2, 100))}; luego el {x1}% de eso = {ans}.")


def t_pct_conv(r, l):
    kind = r.choice(["p2f", "f2p", "d2p"])
    if kind == "p2f":
        p = r.choice([25, 40, 60, 75, 12.5, 37.5, 5, 35, 45, 8] if l else [25, 40, 60, 75, 5, 20, 50, 80])
        x = F(str(p)) / 100
        ans = fs(x)
        alts = [F(str(p)), F(1, int(p)) if float(p).is_integer() else F(str(p)) / 10, F(str(p)) / 10, F(str(p)) / 1000, F(100, 1) / F(str(p))]
        stem = f"¿Qué fracción irreductible equivale a {pf(F(str(p)))}?"
        fig = card([f"Porcentaje: {pf(F(str(p)))}"], 110, 26)
        return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_RES, f"{pf(F(str(p)))} = {p}/100 = {ans}.")
    if kind == "f2p":
        n, d = r.choice([(3, 4), (2, 5), (1, 8), (3, 8), (7, 20), (9, 50), (5, 8), (4, 25), (11, 20)])
        x = F(n, d) * 100
        ans = pf(x)
        alts = [F(n, d), F(d, n) * 100, x / 10, x * 10, F(n * d, 10)]
        stem = f"¿A qué porcentaje equivale la fracción {n}/{d}?"
        fig = card([f"Fracción: {n}/{d}"], 110, 26)
        return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: pf(F(v)))), Q_RES, f"{n}/{d} = {ans}.")
    d = r.choice([F(45, 100), F(7, 100), F(125, 1000), F(3, 10), F(8, 10), F(12, 10), F(5, 1000), F(6, 100)])
    x = d * 100
    ans = pf(x)
    alts = [d, d * 10, d * 1000, d / 10, x / 10 if x / 10 != x else x + 1]
    stem = f"¿A qué porcentaje equivale el número decimal {dstr(d)}?"
    fig = card([f"Decimal: {dstr(d)}"], 110, 26)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: pf(F(v)))), Q_RES, f"{dstr(d)} · 100 = {ans}.")


# ---------------------------------------------------------------- Modelar
def t_class_comp(r, l):
    N = r.choice([20, 25, 30, 40, 50, 60, 80, 120, 200])
    x = r.choice([20, 25, 30, 35, 40, 45, 55, 60, 65, 75])
    who = r.choice([("mujeres", "hombres"), ("aprobados", "reprobados"), ("hinchas de A", "hinchas de B")])
    val_x = F(N * x, 100)
    if val_x.denominator != 1:
        raise Reject
    fig = hbars_pct([(who[0], x), ("(el resto)", 100 - x)])
    ask = r.choice([0, 1])
    stem = f"En un grupo de {N} personas, el {x}% son {who[0]} y el resto son {who[1]}. ¿Cuántos son {who[ask]}?"
    val = val_x if ask == 0 else N - val_x
    alts = [N - val, F(N * (100 - x), 100) if ask == 0 else val_x, x if ask == 0 else 100 - x, F(N, x), val + 5, val * 2]
    ans = str(val)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_MOD, f"{x}% de {N} = {val_x}; el resto es {N - val_x}.")


def t_alloy(r, l):
    m = r.choice([200, 250, 400, 500, 800, 1000])
    p = r.choice([20, 25, 30, 35, 40, 60, 65, 70, 75])
    g = F(m * p, 100)
    if g.denominator != 1:
        raise Reject
    comp = r.choice([("cobre", "zinc"), ("oro", "plata"), ("sal", "agua")])
    fig = pie_chart([(comp[0], f"{p}%", p), (comp[1], "?", 100 - p)])
    ask = r.choice([0, 1])
    stem = f"Una mezcla de {m} g contiene {p}% de {comp[0]} y el resto de {comp[1]}. ¿Cuántos gramos de {comp[ask]} tiene?"
    val = g if ask == 0 else m - g
    alts = [m - val, F(m * (100 - p), 100) if ask == 0 else g, p if ask == 0 else 100 - p, val + 50, F(m, p)]
    ans = f"{val} g"
    al = list(dict.fromkeys(f"{fs(F(a))} g" for a in alts if a > 0 and F(a) != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"{p}% de {m} = {g} g; el resto = {m - g} g.")


def t_exam(r, l):
    tot = r.choice([40, 45, 50, 60, 80, 100])
    kind = r.choice(["pct", "min"])
    if kind == "pct":
        cor = r.choice([x for x in range(10, tot) if (x * 100) % tot == 0 or (x * 200) % tot == 0])
        val = F(cor * 100, tot)
        fig = card([f"Preguntas de la prueba: {tot}", f"Respuestas correctas: {cor}"], 130, 21)
        stem = f"En una prueba de {tot} preguntas, una estudiante respondió correctamente {cor}. ¿Qué porcentaje de respuestas correctas obtuvo?"
        alts = [F(cor, tot), F(tot, cor) * 100, tot - cor, val / 10, 100 - val]
        ans = pf(val)
        return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: pf(F(v)))), Q_MOD, f"{cor}/{tot} = {ans}.")
    p = r.choice([50, 55, 60, 65, 70, 75])
    val = F(tot * p, 100)
    if val.denominator != 1:
        raise Reject
    fig = card([f"Puntaje total: {tot} puntos", f"Para aprobar: {p}% del total"], 130, 21)
    stem = f"Para aprobar una prueba de {tot} puntos se necesita al menos el {p}% del puntaje total. ¿Cuántos puntos se necesitan como mínimo?"
    alts = [tot - val, F(tot, p), p, val + 5, F(tot * (p + 10), 100)]
    ans = str(val)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_MOD, f"{p}% de {tot} = {val}.")


# ---------------------------------------------------------------- Representar
CATS = [["Fútbol", "Tenis", "Natación", "Básquet"], ["Rojo", "Azul", "Verde", "Amarillo"], ["Bus", "Metro", "Auto", "Bicicleta"], ["Pizza", "Sushi", "Pasta", "Ensalada"]]


def t_pie_read(r, l):
    names = r.choice(CATS)
    while True:
        ps = [r.choice([10, 15, 20, 25, 30, 35, 40]) for _ in range(3)]
        rest = 100 - sum(ps)
        if 10 <= rest <= 40 and rest % 5 == 0:
            ps.append(rest)
            break
    N = r.choice([200, 240, 400, 500, 600, 800, 1000])
    fig = pie_chart([(n_, f"{p}%", p) for n_, p in zip(names, ps)])
    i, j = r.sample(range(4), 2)
    kind = r.choice(["one", "two"] if l else ["one"])
    if kind == "one":
        val = F(N * ps[i], 100)
        stem = f"El gráfico circular muestra las preferencias de {n_(N)} personas encuestadas. ¿Cuántas personas eligieron {names[i]}?"
        alts = [F(N, ps[i]), ps[i], N - val, F(N * ps[j], 100), val + 10, val * 2]
        ex = f"{ps[i]}% de {N} = {fs(val)}."
    else:
        val = F(N * (ps[i] + ps[j]), 100)
        stem = f"El gráfico circular muestra las preferencias de {n_(N)} personas encuestadas. ¿Cuántas personas eligieron {names[i]} o {names[j]}?"
        alts = [F(N * ps[i], 100), F(N * ps[j], 100), F(N * abs(ps[i] - ps[j]), 100), ps[i] + ps[j], val + 20, N - val]
        ex = f"({ps[i]}% + {ps[j]}%) de {N} = {fs(val)}."
    if val.denominator != 1:
        raise Reject
    ans = fs(val)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, lambda v: fs(F(v)))), Q_REP, ex)


def t_bars_read(r, l):
    names = r.sample(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"], 4 if l else 3)
    vals = [r.choice(range(10, 95, 5)) for _ in names]
    if len(set(vals)) < len(vals):
        raise Reject
    fig = hbars_pct(list(zip(names, vals)), top=100)
    i, j = r.sample(range(len(names)), 2)
    kind = r.choice(["diff", "sum"] if l else ["diff"])
    if kind == "diff":
        if vals[i] < vals[j]:
            i, j = j, i
        stem = f"El gráfico muestra el porcentaje de asistencia por día. ¿Cuántos puntos porcentuales más asistió el {names[i].lower()} que el {names[j].lower()}?"
        val = vals[i] - vals[j]
        alts = [vals[i] + vals[j], vals[j], vals[i], val + 5, F(vals[i], vals[j]) * 100]
        fmt = lambda v: f"{fs(F(v))} puntos"
    else:
        stem = f"El gráfico muestra el porcentaje de asistencia por día. ¿Cuál es el promedio de asistencia del {names[i].lower()} y el {names[j].lower()}?"
        val = F(vals[i] + vals[j], 2)
        alts = [vals[i] + vals[j], abs(vals[i] - vals[j]), max(vals[i], vals[j]), val + 5, val - 5]
        fmt = lambda v: pf(F(v))
    ans = fmt(val)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, fmt)), Q_REP, f"Se leen los valores de las barras y se opera: {ans}.")


def t_grid100(r, l):
    n = r.choice([5, 10, 12, 15, 20, 25, 30, 35, 40, 45, 48, 50, 55, 60, 64, 65, 70, 75, 80, 85])
    fig = grid_shaded(10, 10, n, cell=24)
    ask = r.choice(["sh", "fr", "un"]) if l else r.choice(["sh", "un"])
    if ask == "sh":
        stem, val, fm = "La cuadrícula tiene 100 cuadraditos iguales. ¿Qué porcentaje está sombreado?", F(n), pf
        alts = [n / 10, F(100, n) if n else 1, 100 - n, n + 10, n * 2]
    elif ask == "un":
        stem, val, fm = "La cuadrícula tiene 100 cuadraditos iguales. ¿Qué porcentaje NO está sombreado?", F(100 - n), pf
        alts = [n, (100 - n) / 10, n + 10, 100 - n + 10, F(100, n)]
    else:
        stem, val, fm = "La cuadrícula tiene 100 cuadraditos iguales. ¿Qué fracción irreductible de la figura está sombreada?", F(n, 100), lambda v: fs(F(v))
        alts = [F(n, 10), F(100 - n, 100), F(n, 99), F(1, n), F(n, 200)]
    ans = fm(val)
    return make(stem, fig, ans, pick4(ans, uqs(ans, alts, fm)), Q_REP, f"Hay {n} cuadraditos sombreados de 100.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.choice([(20, 50), (15, 80), (30, 60), (25, 40)])
    if k == 0:
        return [f"{a}% de {b} = {a} · {b} = {a * b}"], "Multiplicó por el porcentaje sin dividir por 100: el porcentaje es una razón sobre 100", \
            ["Multiplicó el número por el porcentaje y luego dividió por 10 solamente", "Dividió el número por el porcentaje en lugar de multiplicarlo por él", "Sumó el porcentaje al número sin convertirlo antes a una fracción", "Restó el porcentaje del número y llamó al resultado el porcentaje"]
    if k == 1:
        return ["Precio sube de $40 a $50", "Aumento = 10%"], "Calculó la diferencia sobre 100 en lugar de dividirla por el valor inicial: el aumento es 25%", \
            ["Comparó el precio final con el inicial y tomó la razón como aumento", "Dividió la diferencia por el precio final en lugar del inicial", "Sumó los dos precios antes de calcular la diferencia porcentual", "Restó los precios y luego lo multiplicó por 100 sin dividir por nada"]
    if k == 2:
        return [f"{a} es el {b}% de 100 → {a} es el {b}% de 200"], "Mantuvo el mismo porcentaje al cambiar el total: el porcentaje depende de la cantidad total", \
            ["Duplicó el porcentaje al duplicar el total de la comparación siguiente", "Dividió el total por dos sin cambiar la parte que se compara", "Consideró que el porcentaje es una cantidad fija que no depende del total", "Sumó 100 al total y calculó el porcentaje sobre ese nuevo valor"]
    if k == 3:
        return ["50% de 50% = 50%"], "Confundió el porcentaje de un porcentaje con una suma: 50% de 50% equivale a 25%", \
            ["Sumó los dos porcentajes y luego los dividió por dos para simplificar", "Multiplicó ambos porcentajes sin convertirlos previamente a fracciones", "Restó los dos porcentajes y obtuvo el valor de la parte pedida", "Tomó el mayor de los dos porcentajes y descartó el otro por redundancia"]
    return [f"{a}% = 0,{a}" if a < 10 else f"{a}% = {a / 10}".replace(".", ",")], "Pasó de porcentaje a decimal dividiendo por 10 en vez de por 100, corriendo mal la coma", \
        ["Pasó de porcentaje a decimal multiplicando por 100 en lugar de dividir", "Pasó de porcentaje a fracción pero olvidó simplificar el resultado obtenido", "Dividió por 1.000 para dejar el resultado en la forma más simplificada", "Dejó el porcentaje sin cambio y solo le agregó una coma al inicio"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 19)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_compare(r, l):
    for _ in range(100):
        vals = {}
        for _ in range(5):
            x = r.choice([5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75])
            N = r.choice([40, 60, 80, 100, 120, 150, 200, 240, 300])
            vals[f"{x}% de {N}"] = F(x * N, 100)
        if len(set(vals.values())) == 5:
            break
    else:
        raise Reject
    big = max(vals, key=vals.get)
    fig = card(["Compara las cantidades", "Cada opción es un porcentaje de un total"], 130, 20)
    return make("¿Cuál de las siguientes cantidades es la mayor?", fig, big, [k for k in vals if k != big], Q_ARG, f"{big} = {fs(vals[big])}, mayor que las demás.")


TRUE = ["El 50% de una cantidad equivale a su mitad", "Un aumento de 100% duplica la cantidad", "El 25% de una cantidad equivale a su cuarta parte", "El 10% de una cantidad se obtiene dividiéndola por 10",
        "El 50% de 50% de una cantidad equivale al 25% de ella", "Un porcentaje es una razón cuyo consecuente es 100"]
FALSE = ["El 50% de una cantidad equivale a sus dos tercios", "Un aumento de 50% duplica la cantidad", "El 25% de una cantidad equivale a su quinta parte", "El 10% de una cantidad se obtiene dividiéndola por 100",
         "El 20% de 80 es mayor que el 40% de 80", "Un porcentaje no puede ser mayor que 100%"]


def _fig(r):
    return card(["Porcentajes", "50% = 1/2  ·  25% = 1/4  ·  10% = 1/10"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre porcentajes es verdadera?", "Sobre porcentajes y su cálculo, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con la definición de porcentaje como razón sobre 100.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre porcentajes es falsa?", "Sobre porcentajes y su cálculo, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice la definición de porcentaje.")


BY_SKILL = {
    Q_RES: [t_pct_of, t_pct_conv],
    Q_MOD: [t_class_comp, t_alloy, t_exam],
    Q_REP: [t_pie_read, t_bars_read, t_grid100],
    Q_ARG: [t_error, t_compare, t_true, t_false],
}
