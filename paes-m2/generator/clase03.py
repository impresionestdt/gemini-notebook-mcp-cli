"""Clase 3 · Porcentajes avanzados e interés compuesto."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO


def money(n):
    n = F(n)
    if n.denominator != 1:
        raise Reject
    return "$" + f"{int(n):,}".replace(",", ".")


def pc(x, sign=False):
    x = F(x)
    s = f"{float(x):.3f}".rstrip("0").rstrip(".").replace(".", ",")
    return ("+" if sign and x > 0 else "") + s + "%"


def num(x):
    return f"{float(x):.4f}".rstrip("0").rstrip(".").replace(".", ",")


# ---------------------------------------------------------------- figuras
def chain(boxes, arrows=None, title=None):
    n = len(boxes)
    gap = 56
    bw = (520 - (n - 1) * gap) / n
    body = ""
    for i, t in enumerate(boxes):
        x = 20 + i * (bw + gap)
        last = t == "?"
        body += R(x, 85, bw, 60, FILL2 if last else FILL) + T(x + bw / 2, 122, t, 17 if len(t) < 9 else 13)
        if i:
            body += L(x - gap + 3, 115, x - 3, 115, ACC, 4) + P([(x - 3, 115), (x - 13, 108), (x - 13, 122)], ACC, ACC, 1)
            if arrows:
                body += tag(x - gap / 2, 58, arrows[i - 1], 15)
    if title:
        body += tag(280, 22, title, 16)
    return wrap(560, 175, body, "Secuencia de pasos")


def bars(items, top=None, h=170):
    """items: (valor_para_altura, etiqueta, relleno)"""
    items = [(float(v), lab, fill) for v, lab, fill in items]
    top = float(top or max(v for v, _, _ in items))
    n = len(items)
    bw = 90
    gap = (520 - n * bw) / max(1, n - 1) if n > 1 else 0
    body = L(20, 200, 540, 200, INK, 3)
    for i, (v, lab, fill) in enumerate(items):
        x = 20 + i * (bw + gap) if n > 1 else 235
        hh = 150 * v / top
        body += R(x, 200 - hh, bw, hh, fill) + tag(x + bw / 2, 200 - hh - 18, lab, 15)
    return wrap(560, 235, body, "Gráfico de barras")


def pct_bar(frac, labelL, labelR):
    body = R(30, 70, 500, 70, WHITE) + R(30, 70, 500 * float(frac), 70, FILL3)
    for i in range(11):
        body += L(30 + 50 * i, 140, 30 + 50 * i, 152, INK, 2)
        if i % 2 == 0:
            body += T(30 + 50 * i, 175, f"{10*i}%", 14)
    body += tag(max(30 + 250 * float(frac), 110), 105, labelL, 16)
    if frac < 1:
        body += tag(30 + 500 * float(frac) + 250 * (1 - float(frac)), 30, labelR, 15)
    return wrap(560, 200, body, "Barra de porcentaje")


def price_tag(top, main):
    body = (P([(150, 40), (410, 40), (470, 100), (410, 160), (150, 160)], FILL2) + C(172, 100, 8, WHITE, NAVY, 3)
            + T(322, 88, top, 18) + T(322, 130, main, 28))
    return wrap(560, 200, body, "Etiqueta de precio")


# ---------------------------------------------------------------- Resolver
def t_chain_pct(r, l):
    ch = [r.choice([10, 20, 25, 30, 40, 50])]
    signs = [1]
    if l == 0:
        ch.append(r.choice([10, 20, 25, 50])); signs.append(1)
    elif l == 1:
        ch.append(r.choice([10, 20, 25, 30, 40, 50])); signs.append(-1)
    else:
        ch += [r.choice([10, 20, 25, 30, 40, 50]), r.choice([10, 20, 25, 50])]; signs += [-1, 1]
    f = F(1)
    for c, s in zip(ch, signs):
        f *= 1 + s * F(c, 100)
    tot = (f - 1) * 100
    s_sum = sum(s * c for s, c in zip(signs, ch))
    cands = [pc(s_sum, True), pc(-tot, True), pc(f * 100, True), pc(ch[0] * ch[1] / 100 * signs[1], True) if l < 2 else pc(s_sum + 10, True),
             pc(tot + 1, True), pc(signs[-1] * ch[-1], True), pc(tot / 2, True), pc(-s_sum, True)]
    ans = pc(tot, True)
    txt = ", luego ".join(f"{'sube' if s > 0 else 'baja'} un {c}%" for s, c in zip(signs, ch))
    stem = f"El precio de un producto {txt}. ¿Cuál es la variación porcentual total respecto del precio inicial?"
    fig = chain(["Inicial"] + ["?" if i == len(ch) - 1 else "…" for i in range(len(ch))] if False else ["Precio inicial", *[f"{'+' if s > 0 else '−'}{c}%" for s, c in zip(signs, ch)], "?"] if False else
                ["Inicial"] + ["Paso %d" % (i + 1) for i in range(len(ch) - 1)] + ["Final"], [f"{'+' if s > 0 else '−'}{c}%" for s, c in zip(signs, ch)])
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, f"Factor total = {'·'.join(num(1 + s * F(c, 100)) for s, c in zip(signs, ch))} = {num(f)}; variación = {ans}.")


def t_reverse(r, l):
    if l == 0:
        d = F(r.choice([10, 20, 25, 30, 40, 50]), 100)
        O = r.choice([20000, 24000, 30000, 36000, 40000, 45000, 60000, 80000])
        P = O * (1 - d)
        if P.denominator != 1: raise Reject
        stem, top = f"Un artículo con {int(d*100)}% de descuento cuesta {money(P)}. ¿Cuál era su precio original?", f"−{int(d*100)}%"
        cands = [money(P * (1 + d)), money(P / (1 + d)) if (P / (1 + d)).denominator == 1 else money(P + 1000), money(2 * O - P), money(P + (O - P) // 2), money(O + 1000)]
        ex, fig = f"P·(1 − {num(d)}) = {money(P)} ⟹ P = {money(P)}/{num(1-d)} = {money(O)}.", price_tag(f"Con {int(d*100)}% de descuento", money(P))
    elif l == 1:
        O = r.choice([10000, 20000, 25000, 40000, 50000, 80000, 100000])
        V = O * F(119, 100)
        if V.denominator != 1: raise Reject
        stem, top = f"Un producto cuesta {money(V)} con IVA (19%) incluido. ¿Cuál es su precio neto (sin IVA)?", "IVA"
        cands = [money(V * F(81, 100)), money(V - V * F(19, 100)) if (V * F(19, 100)).denominator == 1 else money(V - 1900), money(V * F(119, 100)) if (V * F(119, 100)).denominator == 1 else money(V + 1900), money(V - 19000) if V > 19000 else money(V - 190), money(O + 1900)]
        cands = [c for c in cands if c != money(O)]
        ex, fig = f"Neto·1,19 = {money(V)} ⟹ neto = {money(O)}.", price_tag("Precio con IVA incluido", money(V))
    else:
        d = F(r.choice([10, 20, 25, 30, 40]), 100)
        O = r.choice([10000, 20000, 25000, 40000, 50000, 80000, 100000, 125000, 200000])
        Fp = O * (1 - d) * F(119, 100)
        if Fp.denominator != 1: raise Reject
        stem = f"Un artículo tiene {int(d*100)}% de descuento sobre su precio de lista y luego se le suma IVA de 19%, con lo que se paga {money(Fp)}. ¿Cuál es el precio de lista?"
        alt = Fp / (1 + F(19, 100) - d)
        cands = [money(Fp * (1 + d) / F(119, 100)) if (Fp * (1 + d) / F(119, 100)).denominator == 1 else money(O + 5000), money(Fp / (1 + d) / F(119, 100)) if (Fp / (1 + d) / F(119, 100)).denominator == 1 else money(O - 5000), money(alt) if alt.denominator == 1 else money(O + 2500), money(Fp * (1 + d)) if (Fp * (1 + d)).denominator == 1 else money(O - 2500), money(Fp - O * F(19, 100)) if (O * F(19, 100)).denominator == 1 else money(O + 7500)]
        ex, fig = f"Lista·{num(1-d)}·1,19 = {money(Fp)} ⟹ lista = {money(O)}.", price_tag(f"−{int(d*100)}% y luego +19% IVA", money(Fp))
    ans = money(O)
    return make(stem, fig, ans, pick4(ans, cands), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_compound(r, l):
    rp = F(r.choice([5, 10, 20, 25, 50]), 100)
    k = r.choice([2, 3]) if rp <= F(1, 5) else 2
    C0 = r.choice([1000, 2000, 4000, 5000, 8000, 10000, 16000, 20000, 40000, 100000])
    C = C0 * (1 + rp) ** k
    if C.denominator != 1: raise Reject
    if l == 0:
        stem = f"Se depositan {money(C0)} a una tasa de interés compuesto de {pc(rp*100)} anual. ¿Cuánto dinero habrá al cabo de {k} años?"
        bx, ar = [money(C0)] + [f"Año {i}" for i in range(1, k)] + ["?"], [f"+{pc(rp*100)}"] * k
        nom, per = rp, "años"
    else:
        m = r.choice([2, 4] if l == 1 else [4, 12])
        nom = rp * m
        if nom > F(2): raise Reject
        unit = {2: ("semestralmente", "semestre"), 4: ("trimestralmente", "trimestre"), 12: ("mensualmente", "mes")}[m]
        months = k * 12 // m
        stem = (f"Se depositan {money(C0)} a una tasa nominal anual de {pc(nom*100)} con capitalización {unit[0]}. "
                f"¿Cuánto dinero habrá al cabo de {months} meses?")
        bx, ar = [money(C0)] + [f"{unit[1].capitalize()} {i}" for i in range(1, k)] + ["?"], [f"+{pc(rp*100)}"] * k
    simple = C0 * (1 + rp * k)
    cands = [money(simple), money(C0 * (1 + nom) ** k) if (C0 * (1 + nom) ** k).denominator == 1 and nom != rp else money(C0 * (1 + rp) ** (k + 1)) if (C0 * (1 + rp) ** (k + 1)).denominator == 1 else money(C + 1000),
             money(C0 * (1 + rp) ** (k - 1)) if (C0 * (1 + rp) ** (k - 1)).denominator == 1 else money(C - 1000),
             money(C0 * (1 + rp) ** (k + 1)) if (C0 * (1 + rp) ** (k + 1)).denominator == 1 else money(C + 2000), money(C0 * (1 + rp * k) + C0 * rp) if True else "", money(C0 + C0 * rp * k * 2)]
    ans = money(C)
    return make(stem, chain(bx, ar, "Capital en cada período"), ans, pick4(ans, cands), Q_MOD,
                f"Tasa por período {pc(rp*100)}, {k} períodos: C = {money(C0)}·{num(1+rp)}^{k} = {ans}.")


def t_decay(r, l):
    if l < 2:
        grow = l == 1
        p = F(r.choice([10, 20, 50]), 100)
        k = r.choice([2, 3])
        V0 = r.choice([1000, 2000, 5000, 8000, 10000, 20000, 40000, 100000, 125000, 200000])
        if not grow:
            V = V0 * (1 - p) ** k
            if V.denominator != 1: raise Reject
            stem = f"Un vehículo de {money(V0)} pierde {pc(p*100)} de su valor cada año. ¿Cuánto vale después de {k} años?"
            cands = [money(V0 * (1 - p * k)), money(V0 * (1 - p) ** (k - 1)), money(V0 * p ** k) if (V0 * p ** k).denominator == 1 else money(V0 - 1000),
                     money(V0 * (1 - p) ** (k + 1)) if (V0 * (1 - p) ** (k + 1)).denominator == 1 else money(V0 - 2000), money(V0 - V0 * p), money(V0 * (1 + p) ** k) if (V0 * (1 + p) ** k).denominator == 1 else money(V0 + 500)]
            ans = money(V)
            vals = [(V0 * (1 - p) ** i, money(V0 * (1 - p) ** i) if (V0 * (1 - p) ** i).denominator == 1 else "…", FILL) for i in range(k)] + [(V0 * (1 - p) ** k, "?", FILL2)]
            ex = f"V = {money(V0)}·{num(1-p)}^{k} = {ans}."
        else:
            fac = (1 + p) ** k
            stem = f"Una población crece {pc(p*100)} cada año. Después de {k} años, ¿cuántas veces la población inicial hay?"
            ans = num(fac) + " veces"
            cands = [num(1 + p * k) + " veces", num((1 + p) ** (k - 1)) + " veces", num(fac + p) + " veces", num(p ** k) + " veces", num((1 + p) ** (k + 1)) + " veces", num(k * (1 + p)) + " veces"]
            vals = [((1 + p) ** i, "×1" if i == 0 else "…", FILL) for i in range(k)] + [((1 + p) ** k, "?", FILL2)]
            ex = f"Factor = {num(1+p)}^{k} = {num(fac)}."
        return make(stem, bars(vals), ans, pick4(ans, cands), Q_MOD, ex)
    # L2: elegir el modelo
    grow = r.random() < 0.5
    p = r.choice([5, 10, 12, 20, 25])
    V0 = r.choice([2000000, 5000000, 8000000, 12000000, 900000, 1500000])
    V0s = f"{V0:,}".replace(",", ".")
    q = num(F(p, 100))
    fq = num(1 + F(p, 100)) if grow else num(1 - F(p, 100))
    other = num(1 - F(p, 100)) if grow else num(1 + F(p, 100))
    ans = f"V(t) = {V0s}·({fq})^t"
    cands = [f"V(t) = {V0s}·({other})^t", f"V(t) = {V0s}·({q})^t", f"V(t) = {V0s}·(1 {'+' if grow else '−'} {q}·t)", f"V(t) = {V0s}·({fq})·t", f"V(t) = {V0s} {'+' if grow else '−'} ({q})^t"]
    stem = (f"Una inversión de ${V0s} " + (f"crece {p}% cada año." if grow else f"pierde {p}% de su valor cada año.") + " ¿Qué expresión modela su valor V(t) después de t años?")
    top = (1 + F(p, 100)) ** 4 if grow else 1
    vals = [((1 + F(p, 100) if grow else 1 - F(p, 100)) ** i, f"t = {i}", FILL) for i in range(4)]
    return make(stem, bars(vals), ans, pick4(ans, cands), Q_MOD, f"Cada año el valor se multiplica por {fq}, por lo que V(t) = V₀·({fq})^t.")


# ---------------------------------------------------------------- Representar
def t_bars_rate(r, l):
    if l == 0:
        rate, per = r.choice([10, 20, 25, 50]), 1
    elif l == 1:
        rate, per = r.choice([10, 20, 25, 50]), 2
    else:
        rate, per = r.choice([-10, -20, -25, -50, 10, 20]), r.choice([2, 3])
    C0 = r.choice([1000, 2000, 4000, 8000, 10000, 16000, 20000])
    f = 1 + F(rate, 100)
    vals = [C0 * f ** i for i in range(per + 1)]
    if any(v.denominator != 1 for v in vals): raise Reject
    items = []
    for i, v in enumerate(vals):
        show = i in (0, per) if l >= 1 else True
        items.append((float(v), money(v) if show else "?", FILL2 if not show else FILL))
    tot = (f ** per - 1) * 100
    ans = pc(abs(rate)) if rate < 0 else pc(rate)
    what = "disminución" if rate < 0 else "aumento"
    cands = [pc(abs(tot) / per), pc(abs(tot)), pc(abs(rate) + 10), pc(abs(rate) - 5 if abs(rate) > 5 else abs(rate) + 5), pc(abs(rate) / 2), pc(abs(tot) / per + 5)]
    stem = f"El gráfico muestra el valor de un capital al cabo de cada año. Si la variación porcentual anual es constante, ¿de cuánto es el {what} porcentual por año?"
    return make(stem, bars(items), ans, pick4(ans, cands), Q_REP, f"Factor anual = ({money(vals[-1])}/{money(vals[0])})^(1/{per}) = {num(f)}, es decir un {what} de {ans}.")


def beaker(x, vol, conc, fill):
    return (R(x, 60, 110, 130, WHITE) + R(x, 190 - 130 * fill, 110, 130 * fill, FILL3) + tag(x + 55, 120, f"{vol} L", 16)
            + tag(x + 55, 160, conc, 16))


def t_mixture(r, l):
    a, b = sorted(r.sample(range(5, 60, 5), 2))
    if l == 0:
        x = y = r.choice([2, 4, 5, 10])
        t = F(a + b, 2)
    else:
        x, y = r.choice([1, 2, 3, 4, 5, 6]), r.choice([1, 2, 3, 4, 5, 6])
        t = F(x * a + y * b, x + y)
    if l == 2:
        y0 = r.choice([2, 3, 4, 5, 6]); x0 = r.choice([2, 4, 6, 8])
        t = F(x0 * a + y0 * b, x0 + y0)
        if t.denominator != 1 or x0 == y0: raise Reject
        stem = f"Se mezclan {x0} litros de una solución al {a}% con una solución al {b}° para obtener una mezcla al {int(t)}%. ¿Cuántos litros de la solución al {b}% se necesitan?".replace(f"{b}°", f"{b}%")
        ans = f"{y0} litros"
        cands = [f"{x0} litros", f"{y0 + 1} litros", f"{y0 * 2} litros", f"{x0 + y0} litros", f"{max(1, y0 - 1)} litros", f"{x0 * 2} litros"]
        fig = wrap(560, 230, beaker(20, x0, f"{a}%", .5) + beaker(230, "?", f"{b}%", .5) + beaker(430, "", f"{int(t)}%", .6), "Dos soluciones que se mezclan")
        return make(stem, fig, ans, pick4(ans, cands), Q_REP, f"Concentración: ({x0}·{a} + y·{b})/({x0}+y) = {int(t)} ⟹ y = {y0}.")
    if t.denominator not in (1, 2): raise Reject
    stem = f"Se mezclan {x} litros de una solución al {a}% con {y} litros de una solución al {b}%. ¿Qué porcentaje de concentración tiene la mezcla?"
    ans = pc(t)
    cands = [pc(F(a + b, 2)), pc(a + b), pc(F(y * a + x * b, x + y)), pc(t + 5), pc(t - 5), pc(F(x * a + y * b, 100))]
    fig = wrap(560, 230, beaker(20, x, f"{a}%", .5) + beaker(230, y, f"{b}%", .5) + beaker(430, x + y, "?", .7), "Dos soluciones que se mezclan")
    return make(stem, fig, ans, pick4(ans, cands), Q_REP, f"({x}·{a} + {y}·{b})/{x + y} = {ans}.")


# ---------------------------------------------------------------- Argumentar
def _stmt(v):
    v = F(v)
    if v == 0:
        return "Queda igual que el precio inicial"
    return f"Queda {pc(abs(v))} {'mayor' if v > 0 else 'menor'} que el precio inicial"


def t_arg_chain(r, l):
    a = r.choice([10, 20, 25, 30, 40, 50])
    b = a if l == 0 else r.choice([x for x in [10, 20, 25, 30, 40, 50] if x != a])
    net = (1 + F(a, 100)) * (1 - F(b, 100)) - 1
    net *= 100
    ans = _stmt(net)
    cands = [_stmt(0), _stmt(-net if net else 1), _stmt(a - b if a != b else a), _stmt(F(a - b, 2) if a != b else F(a, 2)), _stmt(abs(net) * 10 if net else 1), _stmt(-(a - b) if a != b else -a)]
    fig = chain(["Precio inicial", "Sube", "Baja"], [f"+{a}%", f"−{b}%"], "¿Cómo queda el precio final?")
    fig = fig.replace(">Sube<", ">Tras subir<").replace(">Baja<", ">Precio final<")
    stem = f"El precio de un producto sube {a}% y luego baja {b}%. ¿Cuál de las siguientes afirmaciones es verdadera?"
    return make(stem, fig, ans, pick4(ans, cands), Q_ARG, f"(1 + {a/100})·(1 − {b/100}) = {num((1+F(a,100))*(1-F(b,100)))}; el precio final {ans[6:].lower() if False else 'cambia'} un {pc(net, True)} respecto del inicial.")


def t_simple_vs_comp(r, l):
    rate = F(r.choice([10, 20] if l else [10, 20, 50]), 100)
    n = 2 if l == 0 else 3
    C0 = r.choice([1000, 2000, 4000, 5000, 8000, 10000, 20000, 40000])
    diff = C0 * ((1 + rate) ** n - 1 - n * rate)
    if diff.denominator != 1 or diff == 0: raise Reject
    ans = f"El compuesto supera al simple en {money(diff)}"
    cands = ["Ambos generan el mismo interés", f"El compuesto supera al simple en {money(diff * 2)}",
             f"El simple supera al compuesto en {money(diff)}", f"El compuesto supera al simple en {money(C0 * rate)}" if C0 * rate != diff else f"El compuesto supera al simple en {money(diff + 500)}",
             f"El compuesto supera al simple en {money(diff / 2)}" if (diff / 2).denominator == 1 else f"El compuesto supera al simple en {money(diff + 100)}", f"El compuesto supera al simple en {money(C0 * rate * n)}"]
    rf = float(rate)
    ymax = float((1 + rate) ** 5) * 1.1
    pl2 = Plot(560, 250, 0, 5, 1, ymax, ml=20)
    pl2.parts.append(L(pl2.X(0), pl2.Y(1), pl2.X(5), pl2.Y(1), INK, 3) + L(pl2.X(0), pl2.Y(1), pl2.X(0), pl2.Y(ymax), INK, 3)
                     + T(pl2.X(5) - 4, pl2.Y(1) + 24, "años", 15, "end") + T(pl2.X(0) + 8, pl2.Y(ymax) + 14, "capital", 15, "start"))
    pl2.curve(lambda x: 1 + rf * x, 0, 5, NAVY, 4)
    pl2.curve(lambda x: (1 + rf) ** x, 0, 5, ACC, 4)
    pl2.parts.append(tag(pl2.X(4.2), pl2.Y(1 + rf * 4.2) + 28, "interés simple", 15) + tag(pl2.X(3.2), pl2.Y((1 + rf) ** 3.2) - 26, "interés compuesto", 15))
    stem = f"Se invierten {money(C0)} al {pc(rate*100)} anual durante {n} años, una vez con interés simple y otra con interés compuesto anual. ¿Cuál afirmación es verdadera?"
    return make(stem, pl2.svg("Interés simple vs compuesto"), ans, pick4(ans, cands), Q_ARG,
                f"Compuesto: {money(C0*(1+rate)**n)}; simple: {money(C0*(1+rate*n))}. Diferencia = {money(diff)}.")


def t_points(r, l):
    t = r.choice([10, 20, 25, 50]) if l < 2 else r.choice([10, 20, 25, 40, 50])
    p = r.choice([4, 5, 8, 10, 12, 16, 20, 25, 30, 40] if l else [4, 5, 8, 10, 20, 40])
    q = p * (1 + F(t, 100))
    if l == 2 and r.random() < 0.5:
        p, q = q, p
    if q.denominator != 1 or p == q: raise Reject
    p, q = int(p), int(q)
    d = q - p
    rel = F(abs(d) * 100, p)
    verb = "Aumentó" if d > 0 else "Disminuyó"
    pt = lambda n: f"{n} punto porcentual" if n == 1 else f"{n} puntos porcentuales"
    fmt_ = lambda a, b: f"{verb} {pt(a)} y {pc(b)} en términos relativos"
    ans = fmt_(abs(d), rel)
    cands = [fmt_(int(rel), abs(d)) if rel.denominator == 1 else fmt_(abs(d), rel + 5), fmt_(abs(d), abs(d)), fmt_(abs(d) * 2, rel), fmt_(abs(d), rel * 2),
             fmt_(abs(d) + 1, rel), ("Disminuyó" if d > 0 else "Aumentó") + f" {pt(abs(d))} y {pc(rel)} en términos relativos"]
    fig = bars([(p, f"Antes: {p}%", FILL), (q, f"Ahora: {q}%", FILL2)], max(p, q))
    return make(f"La tasa de desempleo de una comuna pasó de {p}% a {q}%. ¿Cuál afirmación describe correctamente el cambio?", fig, ans, pick4(ans, cands), Q_ARG,
                f"Diferencia absoluta: {abs(d)} puntos porcentuales. Cambio relativo: {abs(d)}/{p} = {pc(rel)}.")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_percent_calc(r, l):
    if l == 0:
        p = r.choice([5, 10, 15, 20, 25, 30, 35, 40, 60, 75])
        N = r.choice([80, 120, 200, 240, 360, 400, 600, 800, 1200])
        v = F(p * N, 100)
        if v.denominator != 1: raise Reject
        stem, ans = f"¿Cuánto es el {p}% de {N}?", str(int(v))
        cands = [str(int(v) + 10), str(int(N - v)), str(int(v) * 2), str(int(N * p / 10)) if (N * p / 10) % 1 == 0 else str(int(v) + 5), str(int(F(N, p) )) ]
        fig, ex = pct_bar(F(p, 100), f"{p}% de {N}", ""), f"{p}/100 · {N} = {ans}."
    elif l == 1:
        A = r.choice([15, 18, 24, 30, 36, 45, 60, 72, 90, 120])
        B = r.choice([60, 80, 90, 120, 150, 180, 200, 240, 300, 360, 400])
        if A >= B or (F(A, B) * 100).denominator > 2: raise Reject
        stem, ans = f"¿Qué porcentaje de {B} es {A}?", pc(F(A * 100, B))
        cands = [pc(F(B * 100, A)), pc(F(A * 100, B) + 10), pc(F(B - A, B) * 100), pc(F(A, B)), pc(F(A * 100, B) * 2), pc(F(B - A) * 100 / A)]
        fig, ex = pct_bar(F(A, B), f"{A} de {B}", "Total"), f"{A}/{B}·100 = {ans}."
    else:
        rp, k = r.choice([10, 20, 50]), r.choice([2, 3])
        tot = ((1 + F(rp, 100)) ** k - 1) * 100
        stem, ans = f"Un aumento de {rp}% se aplica {k} veces seguidas sobre una cantidad. ¿A qué aumento porcentual total equivale?", pc(tot)
        cands = [pc(rp * k), pc(tot + rp), pc(tot - 1), pc(rp ** k), pc((1 + F(rp, 100)) ** k * 100), pc(tot * 2)]
        fig = chain(["Cantidad", *["…"] * (k - 1), "Resultado"], [f"+{rp}%"] * k)
        ex = f"{num(1+F(rp,100))}^{k} = {num((1+F(rp,100))**k)}, es decir {ans} de aumento."
    return make(stem, fig, ans, pick4(ans, cands), Q_PRO, ex)


def t_simple_interest(r, l):
    C = r.choice([100000, 200000, 250000, 400000, 500000, 800000, 1000000])
    rate = F(r.choice([2, 3, 4, 5, 6, 8, 10, 12]), 100)
    t = r.choice([2, 3, 4, 5, 6])
    I = C * rate * t
    if I.denominator != 1: raise Reject
    if l == 0:
        stem, ans = f"Se depositan {money(C)} al {pc(rate*100)} anual de interés simple durante {t} años. ¿Cuánto interés se gana?", money(I)
        cands = [money(C * (1 + rate) ** t) if (C * (1 + rate) ** t).denominator == 1 else money(I + 5000), money(C * rate), money(I + C), money(C * rate * (t + 1)), money(C * rate * t / 2)]
    elif l == 1:
        stem, ans = f"Un capital de {money(C)} gana {money(I)} de interés simple en {t} años. ¿Cuál es la tasa de interés anual?", pc(rate * 100)
        cands = [pc(rate * 100 * t), pc(rate * 100 / t), pc(I * 100 / C), pc(rate * 100 + 2), pc(rate * 100 * 2)]
    else:
        stem, ans = f"Con interés simple de {pc(rate*100)} anual se ganan {money(I)} en {t} años. ¿Cuál fue el capital invertido?", money(C)
        cands = [money(I / rate) if (I / rate).denominator == 1 else money(C + 50000), money(I * rate * t) if (I * rate * t).denominator == 1 else money(C * 2), money(I / t), money(C - I) if C > I else money(C / 2), money(I / (rate * t * t)) if (I / (rate * t * t)).denominator == 1 else money(C + 100000)]
    fig = chain([money(C) if l != 2 else "?", *[f"Año {i}" for i in range(1, min(t, 3))], f"+ {money(I)}" if l != 0 else "?"], [f"+{pc(rate*100)}"] * min(t, 3) if False else [f"+{pc(rate*100)} de C"] * min(t, 3), "Interés simple: mismo monto cada año") if False else \
        chain(["Capital" if l != 2 else "?", "Interés/año", "Total"] if False else ["Capital C" if l != 2 else "C = ?", f"{t} años", "Interés I"], [pc(rate * 100) if l != 1 else "r = ?", "I = C·r·t"], "Interés simple: I = C · r · t")
    return make(stem, fig, ans, pick4(ans, cands), Q_PRO, f"I = C·r·t = {money(C)}·{num(rate)}·{t} = {money(I)}.")


BY_SKILL = {
    Q_RES: [t_chain_pct, t_reverse],
    Q_MOD: [t_compound, t_decay],
    Q_REP: [t_bars_rate, t_mixture],
    Q_ARG: [t_arg_chain, t_simple_vs_comp, t_points],
    Q_PRO: [t_percent_calc, t_simple_interest],
}
