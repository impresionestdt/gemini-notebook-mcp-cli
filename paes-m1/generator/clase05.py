"""Clase 5 (M1) · Razones y proporciones: proporcionalidad directa e inversa, escalas."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import frac_bars
import viz


def n_(x):
    return f"{int(x):,}".replace(",", ".")


def uq(ans, alts, fmt=lambda v: fs(F(v))):
    seen, out = {ans}, []
    for a in alts:
        if a is None or a <= 0:
            continue
        s = fmt(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def money(x):
    return "$" + n_(x)


# ---------------------------------------------------------------- Resolver problemas
def t_ratio_split(r, l):
    parts = r.choice([(2, 3), (3, 5), (1, 4), (2, 5), (3, 4), (4, 5)]) if l < 2 else r.choice([(1, 2, 3), (2, 3, 5), (1, 3, 4), (2, 2, 3)])
    tot = sum(parts)
    N = tot * r.choice([20, 30, 40, 50, 60, 80, 100, 120, 200]) * (1000 if r.random() < 0.5 else 1)
    names = r.choice([("Ana", "Bruno", "Carla"), ("Luis", "Marta", "Pablo"), ("Sofía", "Diego", "Elena")])[:len(parts)]
    who = r.randrange(len(parts))
    val = N * parts[who] // tot
    body = ""
    w0 = 440
    x = 60
    fills = [FILL, FILL2, FILL3]
    for i, p in enumerate(parts):
        wseg = w0 * p / tot
        body += R(x, 40, wseg, 56, fills[i]) + tag(x + wseg / 2, 68, f"{names[i]}: {p}", 16)
        x += wseg
    body += tag(280, 20, f"Total: {money(N)}", 16)
    fig = wrap(560, 120, body, "Reparto proporcional")
    stem = f"Se reparten {money(N)} entre {' y '.join(names)} en la razón {' : '.join(map(str, parts))}, respectivamente. ¿Cuánto recibe {names[who]}?"
    alts = [N // len(parts), N * parts[who] // (tot + 1), N // parts[who], N - val, val + N // 10, N * parts[who] // max(parts)]
    ans = money(val)
    al = [x for x in dict.fromkeys(money(a) for a in alts if a > 0 and a != val)]
    return make(stem, fig, ans, al[:4], Q_RES, f"Cada parte vale {money(N // tot)}; {names[who]} recibe {parts[who]} partes = {ans}.")


def t_prop_solve(r, l):
    a, b = r.choice([(4, 6800), (5, 3500), (6, 4200), (8, 9600), (3, 2700), (12, 9000)])
    c = r.choice([x for x in range(2, 25) if x != a and (b * x) % a == 0])
    kind = r.choice(["dir", "inv"]) if l else "dir"
    if kind == "dir":
        val = F(b * c, a)
        head = ["Cantidad", str(a), str(c)]
        rows = [["Precio", money(b), "?"]]
        stem = f"{a} kg de un producto cuestan {money(b)}. Si el precio es proporcional a la cantidad, ¿cuánto cuestan {c} kg?"
        alts = [b + (c - a) * 100, b * c, F(b, c), val + b, F(b * a, c)]
        ex = f"Razón constante: {money(b)}/{a} kg; por {c} kg: {money(val)}."
        ans = money(val)
        al = [x for x in dict.fromkeys(money(a_) for a_ in alts if F(a_).denominator == 1 and a_ > 0 and a_ != val)]
    else:
        obr, dias = r.choice([(6, 10), (4, 12), (8, 15), (5, 12), (10, 6)])
        nw = r.choice([x for x in range(2, 21) if x != obr and (obr * dias) % x == 0])
        val = F(obr * dias, nw)
        head = ["Obreros", str(obr), str(nw)]
        rows = [["Días", str(dias), "?"]]
        stem = f"{obr} obreros terminan una obra en {dias} días, trabajando al mismo ritmo. ¿En cuántos días la terminarían {nw} obreros?"
        alts = [F(dias * nw, obr), dias + (nw - obr), dias - (nw - obr) if dias > nw - obr else dias + 3, obr * dias, F(dias, nw)]
        ans = f"{fs(val)} días"
        al = [x for x in dict.fromkeys(f"{fs(F(a_))} días" for a_ in alts if a_ > 0 and F(a_) != val)]
        ex = f"Es proporcionalidad inversa: {obr}·{dias} = {nw}·x, luego x = {fs(val)}."
    fig = viz.table_fig(head, rows)
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_compound(r, l):
    obr, dias, m = r.choice([(6, 8, 120), (4, 10, 80), (5, 6, 90), (8, 5, 160)])
    obr2, dias2 = r.choice([(9, 10), (10, 12), (3, 4), (6, 15), (12, 6)])
    val = F(m * obr2 * dias2, obr * dias)
    if val.denominator != 1:
        raise Reject
    head = ["Obreros", "Días", "Metros"]
    rows = [[str(obr), str(dias), str(m)], [str(obr2), str(dias2), "?"]]
    fig = viz.table_fig(head, rows)
    stem = f"{obr} obreros construyen {m} m de muro en {dias} días. Al mismo ritmo, ¿cuántos metros construyen {obr2} obreros en {dias2} días?"
    ans = f"{val} m"
    alts = [F(m * obr2, obr), F(m * dias2, dias), F(m * obr * dias, obr2 * dias2), m + obr2 + dias2, F(m * obr2 * dias, obr * dias2)]
    al = [f"{fs(F(a))} m" for a in alts if a > 0 and F(a) != val]
    al = list(dict.fromkeys(al))
    return make(stem, fig, ans, al[:4], Q_RES, f"Los metros son proporcionales al número de obreros y a los días: {m}·({obr2}/{obr})·({dias2}/{dias}) = {val}.")


# ---------------------------------------------------------------- Modelar
def map_fig(cm, scale, label="A", label2="B"):
    body = R(30, 30, 500, 170, "#ECFCCB", "#3F6212", 3)
    body += L(120, 130, 440, 130, ACC, 5) + C(120, 130, 8, INK, INK, 1) + C(440, 130, 8, INK, INK, 1)
    body += tag(120, 100, label, 17) + tag(440, 100, label2, 17) + tag(280, 160, f"{cm} cm en el mapa", 17)
    body += tag(440, 58, f"Escala 1 : {n_(scale)}", 17)
    return wrap(560, 220, body, "Mapa con dos puntos y su escala")


def t_scale(r, l):
    k = r.choice([1000, 5000, 20000, 25000, 50000, 100000, 250000])
    cm = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    kind = r.choice(["real", "map"]) if l else "real"
    if kind == "real":
        real_cm = cm * k
        if real_cm >= 100000:
            val, unit = F(real_cm, 100000), "km"
        else:
            val, unit = F(real_cm, 100), "m"
        stem = f"En un mapa a escala 1 : {n_(k)}, la distancia entre A y B mide {cm} cm. ¿Cuál es la distancia real entre A y B?"
        ans = f"{fs(val)} {unit}"
        alts = [(val * 10), val / 10, F(cm * k, 1000), F(cm, k), val * 100]
        al = list(dict.fromkeys(f"{fs(F(a))} {unit}" for a in alts if a > 0 and F(a) != val))
        al += [f"{fs(val * 1000 if unit == 'km' else val / 1000)} {'m' if unit == 'km' else 'km'}"]
        al = [x for x in dict.fromkeys(al) if x != ans]
        ex = f"{cm} cm × {n_(k)} = {n_(cm * k)} cm = {ans}."
        fig = map_fig(cm, k)
        return make(stem, fig, ans, al[:4], Q_MOD, ex)
    km = r.choice([2, 3, 5, 8, 10, 12, 15])
    real_cm = km * 100000
    val = F(real_cm, k)
    if val.denominator != 1 or val > 60:
        raise Reject
    stem = f"En un mapa a escala 1 : {n_(k)}, ¿cuántos centímetros del mapa representan una distancia real de {km} km?"
    ans = f"{val} cm"
    alts = [val * 10, val / 10 if (val / 10).denominator == 1 else val + 1, F(km * 1000, k), km * k, val + km]
    al = list(dict.fromkeys(f"{fs(F(a))} cm" for a in alts if a > 0 and F(a) != val))
    return make(stem, map_fig("?", k), ans, al[:4], Q_MOD, f"{km} km = {n_(real_cm)} cm; dividido por {n_(k)} da {val} cm.")


def t_plan_area(r, l):
    k = r.choice([50, 100, 200, 500])
    a, b = r.choice([(2, 3), (4, 5), (3, 3), (5, 6), (2, 4), (4, 4)])
    body = R(140, 40, 60 * a, 30 * b, FILL, NAVY, 3) + tag(140 + 30 * a, 40 + 30 * b + 24, f"{a} cm", 17) + tag(120, 40 + 15 * b, f"{b} cm", 17) + tag(430, 40, f"Escala 1 : {k}", 17)
    fig = wrap(560, 40 + 30 * b + 50, body, "Plano de un terreno rectangular")
    real = F(a * k, 100) * F(b * k, 100)
    stem = f"El plano de un terreno rectangular, a escala 1 : {k}, muestra un rectángulo de {a} cm por {b} cm. ¿Cuál es el área real del terreno?"
    ans = f"{fs(real)} m²"
    alts = [F(a * b * k, 100), real * k, real / k if False else F(a * b, 100) * k, a * b, real * 10]
    al = list(dict.fromkeys(f"{fs(F(x))} m²" for x in alts if x > 0 and F(x) != real))
    return make(stem, fig, ans, al[:4], Q_MOD, f"Lados reales: {fs(F(a * k, 100))} m y {fs(F(b * k, 100))} m; el área usa la razón al cuadrado.")


def t_mixture(r, l):
    a, b = r.choice([(1, 4), (1, 3), (2, 3), (1, 5), (3, 5), (2, 5)])
    tot = r.choice([2, 3, 4, 5, 6, 8, 10]) * (a + b) // (1 if l else 1)
    ing = r.choice([("concentrado", "agua"), ("pintura", "diluyente"), ("cloro", "agua")])
    fig = frac_bars([("Mezcla", a, a + b)])
    kind = r.choice(["A", "B"])
    if kind == "A":
        val = F(tot * a, a + b)
        stem = f"Una mezcla usa {ing[0]} y {ing[1]} en la razón {a} : {b}. Si se preparan {tot} litros de mezcla, ¿cuántos litros de {ing[0]} se necesitan?"
    else:
        val = F(tot * b, a + b)
        stem = f"Una mezcla usa {ing[0]} y {ing[1]} en la razón {a} : {b}. Si se preparan {tot} litros de mezcla, ¿cuántos litros de {ing[1]} se necesitan?"
    if val.denominator != 1:
        raise Reject
    ans = f"{val} L"
    alts = [F(tot, a + b), F(tot * a, b), F(tot * b, a), tot - val, F(tot, 2)]
    al = list(dict.fromkeys(f"{fs(F(x))} L" for x in alts if x > 0 and F(x) != val))
    return make(stem, fig, ans, al[:4], Q_MOD, f"La mezcla tiene {a + b} partes iguales; cada una vale {fs(F(tot, a + b))} L.")


# ---------------------------------------------------------------- Representar
def t_table_missing(r, l):
    kind = r.choice(["dir", "inv"])
    k = r.choice([3, 4, 5, 6, 8, 12])
    xs = sorted(r.sample([1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20], 4))
    if kind == "dir":
        ys = [k * x for x in xs]
    else:
        K = r.choice([60, 120, 24, 48, 36])
        xs = [x for x in xs if K % x == 0][:4]
        if len(xs) < 3:
            raise Reject
        ys = [K // x for x in xs]
    h = r.randrange(len(xs))
    val = ys[h]
    ys_s = [str(y) if i != h else "?" for i, y in enumerate(ys)]
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [["y"] + ys_s])
    stem = f"La tabla muestra valores de dos magnitudes x e y que son {'directamente' if kind == 'dir' else 'inversamente'} proporcionales. ¿Qué valor corresponde a «?»"
    ans = str(val)
    j = (h + 1) % len(xs)
    alts = [ys[j] + (xs[h] - xs[j]) if True else 0, xs[h] * ys[j] // max(xs[j], 1), ys[j] * 2, val + xs[h], xs[h] + ys[j]]
    al = [x for x in dict.fromkeys(str(a) for a in alts if a > 0 and a != val)]
    if len(al) < 4:
        al += [str(val + d) for d in (1, 2, 3, -1) if val + d > 0 and str(val + d) not in al]
    return make(stem, fig, ans, [x for x in al if x != ans][:4], Q_REP, "Directa: y/x constante. Inversa: x·y constante.")


def t_graph_prop(r, l):
    k = r.choice([2, 3, 4, 5])
    x1 = r.choice([1, 2])
    x2 = r.choice([x for x in (3, 4, 5, 6) if x != x1])
    p = Plot(560, 300, 0, 7, 0, 30 if k >= 4 else 21)
    p.axes(1, 5 if k >= 4 else 3)
    p.curve(lambda x: k * x, 0, 7, ACC, 4.5)
    p.pt(x1, k * x1, f"({x1}, {k * x1})", 0, -26)
    fig = p.svg("Gráfico de una relación proporcional")
    y0 = k * x2
    if y0 > (30 if k >= 4 else 21):
        raise Reject
    stem = f"El gráfico muestra una relación de proporcionalidad directa entre x e y. ¿Cuál es el valor de y cuando x = {x2}?"
    ans = str(y0)
    alts = [y0 + k, y0 - k, k * x1 + x2, x2 * x2, k + x2]
    al = [x for x in dict.fromkeys(str(a) for a in alts if a > 0 and a != y0)]
    return make(stem, fig, ans, al[:4], Q_REP, f"La constante es {k}; y = {k}·{x2} = {y0}.")


def t_ratio_dots(r, l):
    a, b = r.choice([(2, 3), (3, 4), (2, 5), (4, 6), (6, 9), (3, 5), (4, 10), (8, 12)])
    body = ""
    for row, (n, col, lab) in enumerate(((a, FILL3, "Rojos"), (b, FILL2, "Azules"))):
        y = 40 + row * 60
        body += tag(60, y, lab, 15)
        for i in range(n):
            body += C(140 + i * 36, y, 14, col, NAVY, 2.5)
    fig = wrap(560, 150, body, "Dos filas de círculos")
    from math import gcd
    g = gcd(a, b)
    ask = r.choice(["ab", "ba"])
    if ask == "ab":
        stem = "En la figura hay círculos rojos y azules. ¿Cuál es la razón entre rojos y azules, en su forma más simple?"
        val = (a // g, b // g)
    else:
        stem = "En la figura hay círculos rojos y azules. ¿Cuál es la razón entre azules y rojos, en su forma más simple?"
        val = (b // g, a // g)
    ans = f"{val[0]} : {val[1]}"
    alts = [f"{val[1]} : {val[0]}", f"{a} : {b}" if (a, b) != val else f"{val[0]} : {val[1] + 1}", f"{val[0]} : {val[0] + val[1]}", f"{a + b} : {val[1]}", f"{val[0] + 1} : {val[1]}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"{a} : {b} se simplifica dividiendo por {g}.")


# ---------------------------------------------------------------- Argumentar
def t_which_type(r, l):
    kind = r.choice(["dir", "inv", "none"])
    xs = sorted(r.sample([1, 2, 3, 4, 5, 6, 8, 10, 12], 4))
    if kind == "dir":
        k = r.choice([2, 3, 4, 5])
        ys = [k * x for x in xs]
        ans = f"Directamente proporcionales, con constante {k}"
        const = k
    elif kind == "inv":
        K = r.choice([24, 60, 120, 48])
        xs = [x for x in xs if K % x == 0]
        if len(xs) < 3:
            raise Reject
        xs = xs[:4]
        ys = [K // x for x in xs]
        ans = f"Inversamente proporcionales, con constante {K}"
        const = K
    else:
        ys = [x * x + r.randint(1, 3) for x in xs]
        ans = "No son directa ni inversamente proporcionales"
        const = None
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [["y"] + [str(y) for y in ys]])
    stem = "La tabla muestra los valores de dos magnitudes x e y. ¿Cuál de las siguientes afirmaciones es correcta?"
    pool = []
    if kind != "dir":
        pool.append(f"Directamente proporcionales, con constante {xs[0] and ys[0] // xs[0] or 1}")
    if kind != "inv":
        pool.append(f"Inversamente proporcionales, con constante {xs[0] * ys[0]}")
    if kind != "none":
        pool.append("No son directa ni inversamente proporcionales")
    pool += [f"Directamente proporcionales, con constante {ys[-1] - ys[0]}", f"Inversamente proporcionales, con constante {xs[-1] + ys[-1]}"]
    al = [x for x in dict.fromkeys(pool) if x != ans]
    return make(stem, fig, ans, al[:4], Q_ARG, "Directa: y/x es constante. Inversa: x·y es constante.")


TRUE = ["En una proporcionalidad directa, el cociente y/x es constante", "En una proporcionalidad inversa, el producto x·y es constante", "Si dos razones son iguales, sus productos cruzados también son iguales",
        "Si una magnitud se duplica en una proporcionalidad inversa, la otra se reduce a la mitad", "Una razón 3 : 5 indica que el total se divide en 8 partes iguales", "La gráfica de una proporcionalidad directa es una recta que pasa por el origen"]
FALSE = ["En una proporcionalidad directa, si una magnitud aumenta, la otra disminuye", "En una proporcionalidad inversa, el cociente y/x es constante", "Una razón 3 : 5 significa que la primera parte es 3/5 del total",
         "Si dos magnitudes aumentan, entonces siempre son directamente proporcionales", "La gráfica de una proporcionalidad directa es una recta que no pasa por el origen", "Al duplicar una magnitud en proporcionalidad directa, la otra se reduce a la mitad"]


def _fig(r):
    return card(["Proporcionalidad", "Directa: y/x = k   ·   Inversa: x·y = k"], 120, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre razones y proporciones es verdadera?", "Sobre proporcionalidad directa e inversa, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las definiciones de proporcionalidad directa e inversa.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre razones y proporciones es falsa?", "Sobre proporcionalidad directa e inversa, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones de proporcionalidad.")


def _err(r):
    k = r.randrange(4)
    a, b, c = r.sample(range(2, 9), 3)
    if k == 0:
        return [f"{a} obreros hacen una obra en {b * 2} días", f"{a + c} obreros la harán en {b * 2 + c} días"], "Trató como directa una relación inversa: más obreros implican menos días, no más", \
            ["Sumó los obreros adicionales a los días sin considerar el ritmo de trabajo", "Dividió los días por la cantidad de obreros que se agregaron al equipo", "Multiplicó los días por la razón directa entre los obreros iniciales y finales", "Restó los obreros nuevos a los días sin plantear ninguna proporción"]
    if k == 1:
        return [f"Repartir 120 en razón {a} : {b}", f"Parte de la primera = 120 · {a}/{b}"], f"Dividió por {b} en lugar de por la suma de las partes ({a} + {b})", \
            ["Multiplicó el total por la razón inversa en lugar de repartir en partes", "Restó las partes entre sí en lugar de sumarlas para obtener el total", "Repartió el total en partes iguales sin considerar la razón entregada", "Usó solo la segunda parte de la razón y descartó completamente la primera"]
    if k == 2:
        return [f"Escala 1 : 1.000; {a} cm en el mapa", f"Distancia real = {a}·1.000 = {a * 1000} cm = {a * 10} m"], "Convirtió mal las unidades: 1 m son 100 cm, así que el resultado real debía ser distinto", \
            ["Multiplicó por la escala pero olvidó pasar de centímetros a metros al final", "Dividió por la escala en lugar de multiplicar la medida del mapa por ella", "Sumó la escala a la medida del mapa y luego cambió de unidad", "Usó la razón de áreas en lugar de la razón de longitudes"]
    return [f"Razón {a} : {b} → fracción {a}/{b} del total"], "La fracción del total es a/(a + b), no a/b: la razón compara partes, no parte con total", \
        ["La fracción del total es b/(a + b), porque se toma la segunda parte primero", "La razón debe dividirse por la suma de las partes y luego multiplicarse por dos", "La razón es directamente la fracción del total, pero simplificada al máximo", "Debe restarse la segunda parte a la primera antes de formar la fracción"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 42 * (len(lines) + 1), 19)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


BY_SKILL = {
    Q_RES: [t_ratio_split, t_prop_solve, t_compound],
    Q_MOD: [t_scale, t_plan_area, t_mixture],
    Q_REP: [t_table_missing, t_graph_prop, t_ratio_dots],
    Q_ARG: [t_which_type, t_true, t_false, t_error],
}
