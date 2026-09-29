"""Clase 7 (M1) · Porcentajes II: intereses, aumentos y descuentos (descuentos sucesivos)."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import signed_bars
import viz


def n_(x):
    return f"{int(x):,}".replace(",", ".")


def m_(x):
    return "$" + n_(x)


def pc(x):
    s = f"{float(x):.2f}".rstrip("0").rstrip(".").replace(".", ",")
    return s + "%"


def uqs(ans, alts, fmt):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        try:
            s = fmt(a)
        except Exception:
            continue
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def money_opts(ans_v, alts):
    ans = m_(ans_v)
    return ans, uqs(ans, [a for a in alts if a is not None and F(a) > 0 and F(a).denominator == 1], lambda v: m_(v))


# ---------------------------------------------------------------- Resolver problemas
def t_discount(r, l):
    P = r.choice([20000, 25000, 40000, 50000, 60000, 80000, 100000, 120000, 200000])
    if l == 0:
        a = r.choice([10, 20, 25, 30, 40, 50])
        kind = r.choice(["down", "up"])
        val = F(P * (100 - a if kind == "down" else 100 + a), 100)
        lines = [f"Precio original: {m_(P)}", f"{'Descuento' if kind == 'down' else 'Aumento'}: {a}%"]
        stem = f"Un artículo tiene un precio original de {m_(P)}. Se le aplica un {'descuento' if kind == 'down' else 'aumento'} de {a}%. ¿Cuál es el precio final?"
        alts = [P * a // 100, P - a if kind == "down" else P + a, F(P * (100 + a if kind == "down" else 100 - a), 100), P - P * a // 200, val + P // 10]
        ex = f"Precio final = {m_(P)} · {fs(F(100 - a if kind == 'down' else 100 + a, 100))} = {m_(val)}."
    elif l == 1:
        a, b = r.choice([(20, 20), (10, 20), (20, 30), (30, 30), (10, 10), (25, 20), (50, 20)])
        val = F(P * (100 - a) * (100 - b), 10000)
        lines = [f"Precio original: {m_(P)}", f"1.er descuento: {a}%", f"2.º descuento: {b}% (sobre el precio ya rebajado)"]
        stem = f"Un artículo de {m_(P)} recibe un descuento de {a}% y, sobre el precio ya rebajado, otro de {b}%. ¿Cuál es el precio final?"
        alts = [F(P * (100 - a - b), 100), F(P * (100 - a), 100), F(P * (100 - b), 100), F(P * (a + b), 100), val + P // 20]
        ex = f"Se aplican en cadena: {m_(P)}·{fs(F(100 - a, 100))}·{fs(F(100 - b, 100))} = {m_(val)}."
    else:
        a, b = r.choice([(20, 20), (10, 20), (30, 10), (25, 20), (50, 10)])
        val = F(P * (100 + a) * (100 - b), 10000)
        lines = [f"Precio original: {m_(P)}", f"Primero sube {a}%", f"Luego baja {b}% (sobre el nuevo precio)"]
        stem = f"Un artículo de {m_(P)} sube {a}% y luego baja {b}% respecto del nuevo precio. ¿Cuál es el precio final?"
        alts = [F(P * (100 + a - b), 100), P, F(P * (100 - a) * (100 + b), 10000), F(P * (100 + a), 100), F(P * (100 - b), 100)]
        ex = f"{m_(P)}·{fs(F(100 + a, 100))}·{fs(F(100 - b, 100))} = {m_(val)}."
    if val.denominator != 1:
        raise Reject
    fig = card(lines, 60 + 36 * len(lines), 19)
    ans, al = money_opts(val, alts)
    return make(stem, fig, ans, al[:4], Q_RES, ex)


def t_reverse(r, l):
    orig = r.choice([20000, 40000, 50000, 80000, 100000, 120000, 200000])
    a = r.choice([10, 20, 25, 30, 40, 50] if l == 0 else [12, 15, 35, 45, 60, 8])
    kind = r.choice(["down", "up"])
    fin = F(orig * (100 - a if kind == "down" else 100 + a), 100)
    if fin.denominator != 1:
        raise Reject
    lines = [f"Precio final: {m_(fin)}", f"{'Descuento' if kind == 'down' else 'Aumento'} aplicado: {a}%"]
    fig = card(lines, 130, 21)
    stem = f"Después de un {'descuento' if kind == 'down' else 'aumento'} de {a}%, un artículo cuesta {m_(fin)}. ¿Cuál era su precio original?"
    alts = [F(fin * (100 + a if kind == "down" else 100 - a), 100), fin + F(fin * a, 100), fin - F(fin * a, 100), F(fin, a), fin * 2 - orig if False else orig + fin // 10]
    ans, al = money_opts(orig, alts)
    return make(stem, fig, ans, al[:4], Q_RES, f"Original = {m_(fin)} : {fs(F(100 - a if kind == 'down' else 100 + a, 100))} = {m_(orig)}.")


def t_interest(r, l):
    C = r.choice([100000, 200000, 250000, 400000, 500000, 1000000])
    i = r.choice([2, 4, 5, 8, 10] if l == 0 else [10, 5, 20])
    if l == 0:
        t = r.randint(2, 5)
        val = F(C * i * t, 100)
        kind = "simple"
        stem = f"Se invierte un capital de {m_(C)} a un interés simple de {i}% anual durante {t} años. ¿Cuánto interés se gana en total?"
        alts = [F(C * i, 100), F(C * (100 + i) ** t, 100 ** t) - C, C + val, val * 2, F(C * i, 100 * t)]
        ex = f"Interés simple = {m_(C)}·{i}%·{t} = {m_(val)}."
    else:
        t = 2 if l == 1 else 3
        fin = F(C * (100 + i) ** t, 100 ** t)
        if fin.denominator != 1:
            raise Reject
        val = fin
        stem = f"Se invierte un capital de {m_(C)} a un interés compuesto de {i}% anual. ¿Cuál es el monto acumulado después de {t} años?"
        alts = [C + F(C * i * t, 100), C + F(C * i, 100), F(C * (100 + i * t) ** 1, 100) - 0, C * i * t, F(C * (100 + i) ** (t - 1), 100 ** (t - 1))]
        ex = f"Monto = {m_(C)}·{fs(F(100 + i, 100))}^{t} = {m_(fin)}."
    fig = card([f"Capital: {m_(C)}", f"Tasa: {i}% anual", f"Tiempo: {t} años"], 170, 20)
    ans, al = money_opts(val, alts)
    return make(stem, fig, ans, al[:4], Q_RES, ex)


# ---------------------------------------------------------------- Modelar
NOUNS = ["un producto", "una entrada", "un pasaje", "un electrodoméstico", "un servicio"]


def t_model_expr(r, l):
    a, b = r.choice([(20, 20), (10, 30), (30, 20), (25, 10), (40, 10), (15, 20), (30, 30), (50, 10), (10, 10), (25, 20), (20, 30), (40, 20), (12, 10), (35, 20)])
    nm = lambda v: f"{v:.2f}".replace(".", ",")
    ga, gb, ua, ub = nm(1 - a / 100), nm(1 - b / 100), nm(1 + a / 100), nm(1 + b / 100)
    noun = r.choice(NOUNS)
    kind = r.choice(["dd", "ud", "uu"] if l else ["dd", "ud"])
    if kind == "dd":
        ans = f"P · {ga} · {gb}"
        exprs = {ans: (1 - a / 100) * (1 - b / 100), f"P · {nm(1 - a / 100 - b / 100)}": 1 - a / 100 - b / 100, f"P · {ga} − {nm(b / 100)}": (1 - a / 100) - b / 100 / 100 * 100 - 0.0001, f"P · {nm(a / 100 + b / 100)}": a / 100 + b / 100 + 0.0002,
                 f"P · {gb}": 1 - b / 100 + 0.0003}
        stem = f"El precio original de {noun} es P. Se le aplica un descuento de {a}% y luego, sobre el nuevo precio, otro de {b}%. ¿Qué expresión representa el precio final?"
        ex = "Cada descuento multiplica el precio por (1 − tasa); los descuentos sucesivos se multiplican."
        lines = ["Precio original: P", f"1.er cambio: −{a}%", f"2.º cambio: −{b}%"]
    elif kind == "ud":
        ans = f"P · {ua} · {gb}"
        exprs = {ans: (1 + a / 100) * (1 - b / 100), f"P · {ua} · {ub}": (1 + a / 100) * (1 + b / 100), f"P · ({ua} − {nm(b / 100)})": 1 + a / 100 - b / 100 + 0.0001, f"P · {ga} · {ub}": (1 - a / 100) * (1 + b / 100) + 0.0002,
                 f"P · {nm(1 + a / 100 - b / 100)}": 1 + a / 100 - b / 100 + 0.0003}
        stem = f"El precio original de {noun} es P. Sube {a}% y luego, sobre el nuevo precio, baja {b}%. ¿Qué expresión representa el precio final?"
        ex = "El aumento multiplica por (1 + tasa) y la baja por (1 − tasa)."
        lines = ["Precio original: P", f"1.er cambio: +{a}%", f"2.º cambio: −{b}%"]
    else:
        ans = f"P · {ua} · {ub}"
        exprs = {ans: (1 + a / 100) * (1 + b / 100), f"P · {nm(1 + a / 100 + b / 100)}": 1 + a / 100 + b / 100 + 0.0001, f"P · ({ua} + {nm(b / 100)})": 1 + a / 100 + b / 100 + 0.0002, f"P · {ua} · {gb}": (1 + a / 100) * (1 - b / 100) + 0.0003,
                 f"P · {nm(a / 100 * b / 100)}": a / 10000 + 0.0004}
        stem = f"El precio original de {noun} es P. Sube {a}% y luego, sobre el nuevo precio, sube otro {b}%. ¿Qué expresión representa el precio final?"
        ex = "Dos aumentos sucesivos se multiplican: (1 + a)(1 + b)."
        lines = ["Precio original: P", f"1.er cambio: +{a}%", f"2.º cambio: +{b}%"]
    if len({round(v, 6) for v in exprs.values()}) < 5 or len(exprs) < 5:
        raise Reject
    fig = card(lines, 150, 20)
    return make(stem, fig, ans, [k for k in exprs if k != ans][:4], Q_MOD, ex)


def t_iva(r, l):
    neto = r.choice(range(10000, 205000, 5000))
    kind = r.choice(["fwd", "back"])
    total = F(neto * 119, 100)
    fig = card(["IVA: 19% sobre el precio neto", f"Neto: {m_(neto)}" if kind == "fwd" else f"Total con IVA: {m_(total)}"], 130, 20)
    if kind == "fwd":
        stem = f"En Chile el IVA es 19% y se suma al precio neto. Si un producto tiene un precio neto de {m_(neto)}, ¿cuál es su precio con IVA?"
        val = total
        alts = [neto + 19, F(neto * 19, 100), neto * 119 // 10, neto - F(neto * 19, 100), total + neto // 100]
        ex = f"Total = neto·1,19 = {m_(total)}."
    else:
        stem = f"En Chile el IVA es 19% y se suma al precio neto. Si el precio con IVA de un producto es {m_(total)}, ¿cuál es su precio neto?"
        val = neto
        alts = [total - F(total * 19, 100), total * 81 // 100, F(total, 119), total - 19, neto + 1000]
        ex = f"Neto = total : 1,19 = {m_(neto)}; restar el 19% del total da un valor distinto."
    if F(val).denominator != 1:
        raise Reject
    ans, al = money_opts(val, alts)
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_growth_table(r, l):
    C = r.choice([100000, 150000, 200000, 250000, 400000, 500000, 800000, 1000000, 1200000])
    i = r.choice([5, 10, 20, 25, 15])
    yrs = [0, 1, 2, 3]
    vals = [F(C * (100 + i) ** y, 100 ** y) for y in yrs]
    if any(v.denominator != 1 for v in vals):
        raise Reject
    hide = 3
    rows = [[m_(v) if k != hide else "?" for k, v in enumerate(vals)]]
    fig = viz.table_fig(["Año"] + [str(y) for y in yrs], [["Monto"] + rows[0]]) if False else viz.table_fig(["Año", "0", "1", "2", "3"], [["Monto"] + rows[0]])
    stem = f"La tabla muestra el monto de una inversión con interés compuesto de {i}% anual. ¿Qué monto corresponde al año 3?"
    alts = [vals[2] + (vals[2] - vals[1]), vals[2] + F(C * i, 100), vals[0] + F(C * i * 3, 100), vals[2] * 2 - vals[0], vals[3] + C // 10]
    ans, al = money_opts(vals[3], alts)
    return make(stem, fig, ans, al[:4], Q_MOD, f"Cada año se multiplica por {fs(F(100 + i, 100))}: {m_(vals[3])}.")


# ---------------------------------------------------------------- Representar
def t_price_bars(r, l):
    a = r.choice([40, 50, 60, 80, 100, 120, 200])
    p = r.choice([10, 20, 25, 30, 40, 50, 60, 75])
    kind = r.choice(["up", "down"])
    b = F(a * (100 + p if kind == "up" else 100 - p), 100)
    if b.denominator != 1:
        raise Reject
    fig = signed_bars([a, int(b)], ["Antes", "Después"], "mil $")
    stem = f"El gráfico muestra el precio de un producto antes y después de un cambio, en miles de pesos. ¿Cuál es la variación porcentual del precio?"
    ans = f"{'Aumento' if kind == 'up' else 'Disminución'} de {p}%"
    other = "Disminución" if kind == "up" else "Aumento"
    wrong_p = F(abs(int(b) - a), int(b)) * 100 if kind == "up" else F(abs(int(b) - a), int(b)) * 100
    fm = lambda v: pc(float(v))
    alts = [f"{other} de {p}%", f"{'Aumento' if kind == 'up' else 'Disminución'} de {fm(wrong_p)}" if fm(wrong_p) != f"{p}%" else f"{'Aumento' if kind == 'up' else 'Disminución'} de {p + 5}%",
            f"{other} de {fm(wrong_p)}" if fm(wrong_p) != f"{p}%" else f"{other} de {p + 5}%", f"{'Aumento' if kind == 'up' else 'Disminución'} de {p * 2}%", f"{'Aumento' if kind == 'up' else 'Disminución'} de {abs(int(b) - a)}%"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"Variación = ({int(b)} − {a})/{a} = {'+' if kind == 'up' else '−'}{p}%; se calcula sobre el valor inicial.")


def t_growth_rate(r, l):
    C = r.choice([100000, 200000, 500000])
    i = r.choice([5, 10, 20, 25])
    kind = r.choice(["comp", "simple"])
    vals = [F(C * (100 + i) ** y, 100 ** y) if kind == "comp" else C + F(C * i * y, 100) for y in range(4)]
    if any(v.denominator != 1 for v in vals):
        raise Reject
    fig = viz.table_fig(["Año", "0", "1", "2", "3"], [["Monto"] + [m_(v) for v in vals]])
    stem = "La tabla muestra el monto de una inversión. ¿Qué afirmación describe correctamente su crecimiento?"
    if kind == "comp":
        ans = f"Crece {i}% cada año sobre el monto del año anterior (interés compuesto)"
        alts = [f"Crece {i}% cada año sobre el capital inicial (interés simple)", f"Crece {i * 2}% cada año sobre el monto del año anterior (interés compuesto)", f"Crece {m_(vals[1] - vals[0])} cada año, de forma constante (interés simple)", f"Crece {i}% en total durante los tres años (interés simple)"]
    else:
        ans = f"Crece {i}% cada año sobre el capital inicial (interés simple)"
        alts = [f"Crece {i}% cada año sobre el monto del año anterior (interés compuesto)", f"Crece {i * 2}% cada año sobre el capital inicial (interés simple)", f"Crece {m_(vals[3] - vals[0])} cada año, de forma constante (interés simple)", f"Crece {i}% en total durante los tres años (interés compuesto)"]
    return make(stem, fig, ans, alts, Q_REP, "Si el aumento en pesos es constante es interés simple; si el aumento crece, es compuesto.")


def t_change_table(r, l):
    a = r.choice([80, 120, 150, 200, 250, 400, 500])
    p = r.choice([10, 15, 20, 25, 30, 40, 60])
    kind = r.choice(["up", "down"])
    b = F(a * (100 + p if kind == "up" else 100 - p), 100)
    if b.denominator != 1:
        raise Reject
    fig = viz.table_fig(["Precio anterior", "Precio nuevo"], [[m_(a * 100), m_(int(b) * 100)]])
    stem = "La tabla muestra el precio anterior y el nuevo precio de un producto. ¿Qué porcentaje varió el precio respecto del anterior?"
    ans = f"{'Aumento' if kind == 'up' else 'Disminución'} de {p}%"
    other = "Disminución" if kind == "up" else "Aumento"
    q = pc(F(abs(int(b) - a) * 100, int(b)))
    alts = [f"{other} de {p}%", f"{'Aumento' if kind == 'up' else 'Disminución'} de {q}", f"{other} de {q}", f"{'Aumento' if kind == 'up' else 'Disminución'} de {abs(int(b) - a)}%", f"{'Aumento' if kind == 'up' else 'Disminución'} de {p + 10}%"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"Variación = ({int(b)} − {a})/{a} = {p}%.")


# ---------------------------------------------------------------- Argumentar
def t_successive(r, l):
    p = r.choice([10, 20, 30, 40, 50])
    kind = r.choice(["ud", "du"])
    loss = F(p * p, 100)
    fig = card([f"Un precio sube {p}%", f"y luego baja {p}%"] if kind == "ud" else [f"Un precio baja {p}%", f"y luego sube {p}%"], 130, 21)
    stem = f"Un precio {'sube' if kind == 'ud' else 'baja'} {p}% y luego, sobre el nuevo precio, {'baja' if kind == 'ud' else 'sube'} {p}%. ¿Qué ocurre con el precio final respecto del original?"
    ans = f"Queda {pc(loss)} menor que el original"
    alts = ["Queda igual al original", f"Queda {pc(loss)} mayor que el original", f"Queda {p}% menor que el original", f"Queda {p * 2}% menor que el original"]
    return make(stem, fig, ans, alts, Q_ARG, f"Factor total = (1 + {p / 100:.2f})(1 − {p / 100:.2f}) = 1 − {p / 100:.2f}² : el precio baja {pc(loss)}.".replace(".", ","))


def t_single_discount(r, l):
    a, b = r.choice([(20, 30), (10, 20), (20, 20), (30, 40), (10, 50), (25, 20), (50, 20)])
    single = F(100 - (100 - a) * (100 - b) / 100)
    fig = card([f"Descuento 1: {a}%", f"Descuento 2: {b}% (sobre lo rebajado)"], 130, 21)
    stem = f"Un local aplica sucesivamente un descuento de {a}% y otro de {b}% sobre el precio ya rebajado. ¿A qué descuento único equivalen ambos?"
    ans = pc(single)
    alts = [pc(a + b), pc(abs(a - b)), pc(F(a + b, 2)), pc(a * b), pc(single + 5)]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_ARG, f"Factor = {a and (100 - a)}/100·{100 - b}/100 = {fs(F((100 - a) * (100 - b), 10000))}; descuento único = {ans}.")


def _err(r):
    k = r.randrange(4)
    a, b = r.choice([(20, 30), (10, 20), (25, 20), (30, 30)])
    if k == 0:
        return [f"Descuentos sucesivos de {a}% y {b}%", f"Equivalen a un descuento de {a + b}%"], "Sumó los porcentajes: el segundo descuento se aplica sobre el precio ya rebajado, no sobre el original", \
            ["Restó los porcentajes porque el segundo descuento se aplica sobre el precio rebajado", "Multiplicó los porcentajes sin convertirlos previamente a fracciones o decimales", "Tomó el mayor de los dos porcentajes y descartó el otro descuento", "Promedió los dos porcentajes sin considerar el orden en que se aplican"]
    if k == 1:
        return ["Precio con IVA: $119.000", "Precio neto = 119.000 − 19% de 119.000"], "Restó el 19% del total: el IVA es el 19% del precio neto, por lo que el neto es total : 1,19", \
            ["Dividió el total por 1,9 en lugar de dividirlo por 1,19 para obtener el neto", "Restó 19 pesos al total en lugar de restarle el 19% de su valor", "Multiplicó el total por 1,19 en vez de dividirlo por ese factor", "Calculó el 19% del neto pero lo sumó dos veces al precio del producto"]
    if k == 2:
        return ["Capital $100.000 al 10% anual por 2 años", "Interés compuesto = 100.000 + 2 · 10.000 = $120.000"], "Usó interés simple: en el compuesto el segundo año el 10% se calcula sobre el monto del primer año", \
            ["Aplicó el 10% solo el primer año y no consideró el segundo año completo", "Multiplicó el capital por 1,1 solo una vez en lugar de aplicarlo dos veces", "Sumó el 10% del capital tres veces en vez de dos veces seguidas", "Calculó el interés compuesto pero lo restó del capital en vez de sumarlo"]
    return ["Un artículo de $80.000 sube 25%", "Para volver al precio inicial debe bajar 25%"], "Bajar el mismo porcentaje no revierte un aumento: la baja se calcula sobre un precio mayor, por lo que debe ser 20%", \
        ["Para revertir un aumento de 25% basta con bajar el precio en $25.000", "Debe bajar 30% porque el precio se calcula sobre el original más el aumento", "Debe bajar 15% porque el aumento fue calculado solo sobre la mitad del precio", "No es posible volver al precio inicial mediante un descuento porcentual"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 60 + 44 * (len(lines) + 1), 18)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["Dos descuentos sucesivos de 20% equivalen a un descuento único de 36%", "Un aumento de 25% se revierte con una baja de 20%", "El interés compuesto supera al interés simple a partir del segundo período",
        "Un aumento de 100% duplica una cantidad", "Los porcentajes sucesivos se aplican cada uno sobre el valor que resultó del anterior", "Si un precio baja 50%, para volver al original debe subir 100%"]
FALSE = ["Dos descuentos sucesivos de 20% equivalen a un descuento único de 40%", "Un aumento de 20% se revierte con una baja de 20%", "El interés simple supera al compuesto cuando pasan varios años",
         "Un aumento de 50% duplica una cantidad", "Los porcentajes sucesivos siempre se aplican sobre el valor original", "Si un precio baja 50%, para volver al original debe subir 50%"]


def _fig(r):
    return card(["Aumentos y descuentos", "Factor: 1 + tasa (sube)  ·  1 − tasa (baja)"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre aumentos y descuentos es verdadera?", "Sobre porcentajes sucesivos e intereses, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se comprueba con los factores de aumento y descuento.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre aumentos y descuentos es falsa?", "Sobre porcentajes sucesivos e intereses, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el cálculo con factores.")


BY_SKILL = {
    Q_RES: [t_discount, t_reverse, t_interest],
    Q_MOD: [t_model_expr, t_iva, t_growth_table],
    Q_REP: [t_price_bars, t_growth_rate, t_change_table],
    Q_ARG: [t_successive, t_single_discount, t_error, t_true, t_false],
}
