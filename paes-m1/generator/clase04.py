"""Clase 4 (M1) · Números racionales: decimales, transformación, redondeo y truncamiento."""
import itertools
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import numline
from num import dstr, pstr, terminates
import viz


def show(x):
    return dstr(x) if terminates(x) else pstr(x)


def dopts(ans, alts):
    seen, out = {show(ans)}, []
    for a in alts:
        if a is None:
            continue
        try:
            s = show(F(a))
        except ValueError:
            continue
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def sfo(ans, alts):
    seen, out = {fs(ans)}, []
    for a in alts:
        if a is None:
            continue
        s = fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def rnd(x, k):
    x = F(x)
    return int(x * 10 ** k + F(1, 2)) if x >= 0 else -int(-x * 10 ** k + F(1, 2))


def trunc(x, k):
    return int(F(x) * 10 ** k)


def dk(n, k):
    """n / 10^k con k decimales."""
    return dstr(F(n, 10 ** k), k) if k else str(n)


# ---------------------------------------------------------------- Resolver problemas
def t_frac_to_dec(r, l):
    if l == 0:
        d = r.choice([2, 4, 5, 8, 10, 20, 25])
        n = r.randint(1, 3 * d)
        if n % d == 0:
            raise Reject
        x = F(n, d)
        alts = [x / 10, x * 10, F(d, n) if terminates(F(d, n)) else None, x + F(1, 10), x - F(1, 10) if x > F(1, 10) else x + F(1, 5), F(n, d + 1) if terminates(F(n, d + 1)) else x + F(1, 100)]
        stem = f"¿Cuál es la expresión decimal de la fracción {n}/{d}?"
        ans = dstr(x)
        al = dopts(x, alts)
        return make(stem, card([f"Fracción: {n}/{d}", "Divide numerador por denominador"], 130, 21), ans, al[:4], Q_RES, f"{n} : {d} = {ans}.")
    d = r.choice([3, 6, 9, 11, 12, 15] if l == 1 else [6, 12, 15, 18, 22, 30])
    n = r.randint(1, 2 * d)
    x = F(n, d)
    if x.denominator == 1 or terminates(x):
        raise Reject
    ans = pstr(x)
    tr = F(int(x * 1000), 1000)
    alts = [dstr(tr), dstr(F(rnd(x, 2), 100), 2), dstr(F(rnd(x, 3), 1000), 3), pstr(F(d, n)), dstr(F(int(x * 100), 100), 2)]
    al = [a for a in dict.fromkeys(alts) if a != ans]
    stem = f"¿Cuál es la expresión decimal de {n}/{d}? (Los puntos suspensivos indican que el patrón se repite.)"
    return make(stem, card([f"Fracción: {n}/{d}", "¿Decimal finito o periódico?"], 130, 21), ans, al[:4], Q_RES, f"{n}/{d} = {ans}: el decimal es periódico.")


def t_dec_to_frac(r, l):
    if l == 0:
        nd = r.choice([1, 2, 3])
        n = r.randint(1, 10 ** nd * 2 - 1)
        if n % 10 == 0 or n % (10 ** nd) == 0:
            raise Reject
        x = F(n, 10 ** nd)
        txt = dk(n, nd)
        alts = [F(n, 10 ** (nd + 1)), F(n, 10 ** max(nd - 1, 0)), F(n, 100) if nd != 2 else F(n, 1000), F(10 ** nd, n), F(n, 10 ** nd + 1)]
        stem = f"¿Qué fracción irreductible equivale al decimal {txt}?"
        ans = fs(x)
        return make(stem, card([f"Decimal: {txt}"], 110, 26), ans, pick4(ans, sfo(x, alts)), Q_RES, f"{txt} = {n}/{10 ** nd} = {ans}.")
    if l == 1:
        per = r.choice([1, 2])
        p = r.randint(1, 10 ** per - 2)
        if per == 2 and p % 11 == 0:
            raise Reject
        x = F(p, 10 ** per - 1)
        txt = pstr(x)
        alts = [F(p, 10 ** per), F(p, 10 ** per - 2), F(p, 10 ** (per + 1) - 10), F(10 ** per - 1, p), F(p + 1, 10 ** per - 1)]
    else:
        pre = r.randint(1, 3)
        p = r.randint(1, 8)
        x = F(pre * 10 + p - pre, 90)
        txt = pstr(x)
        alts = [F(pre * 10 + p, 99), F(pre * 10 + p, 100), F(pre * 10 + p, 90), F(pre * 10 + p - pre, 99), F(pre * 10 + p, 1000)]
    if terminates(x):
        raise Reject
    ans = fs(x)
    stem = f"¿Qué fracción irreductible equivale al decimal periódico {txt}?"
    return make(stem, card([f"Decimal: {txt}"], 110, 26), ans, pick4(ans, sfo(x, alts)), Q_RES, f"{txt} = {ans}.")


def t_dec_ops(r, l):
    op = r.choice(["+", "−", "·"] if l < 2 else ["·", ":", "+"])
    if op in ("+", "−"):
        a, b = F(r.randint(11, 99), 10), F(r.randint(105, 999), 100)
        if op == "−" and a < b:
            a, b = b, a
        val = a + b if op == "+" else a - b
        mis = a + b / 10 if op == "+" else a - b / 10
        alts = [mis, a * b, val * 10, val / 10, a + b if op == "−" else abs(a - b) + F(1, 10)]
    elif op == "·":
        a, b = F(r.randint(11, 99), 10), F(r.randint(11, 99), r.choice([10, 100]))
        val = a * b
        alts = [val * 10, val / 10, a + b, val * 100, val + F(1, 10)]
    else:
        b = F(r.choice([2, 4, 5, 25, 125, 15, 8]), r.choice([10, 100]))
        q = F(r.randint(2, 40), r.choice([1, 10]))
        a = q * b
        val = q
        alts = [val * 10, val / 10, a * b, b / a, val + 1]
    if not terminates(val) or val > 500 or not terminates(a) or not terminates(b):
        raise Reject
    disp = f"{show(a)} {op} {show(b)}"
    ans = dstr(val)
    fig = card(["Calcula:", disp], 130, 24)
    al = dopts(val, alts)
    return make("¿Cuál es el resultado de la operación de la figura?", fig, ans, al[:4], Q_RES, "Se opera con cuidado del valor posicional; en la multiplicación se cuentan los decimales de ambos factores.")


# ---------------------------------------------------------------- Modelar
def t_price(r, l):
    items = r.sample([("Manzanas", 1800), ("Queso", 9500), ("Pollo", 4200), ("Arroz", 1500), ("Tomates", 2400)], 2 if l else 1)
    qty = [F(r.randint(5, 39), 10) for _ in items]
    rows = [[n, dstr(q) + " kg", "$" + f"{p:,}".replace(",", ".") + " / kg"] for (n, p), q in zip(items, qty)]
    tot = sum(q * p for (n, p), q in zip(items, qty))
    if tot.denominator != 1:
        raise Reject
    fig = viz.table_fig(["Producto", "Cantidad", "Precio"], rows)
    fmt = lambda x: "$" + f"{int(x):,}".replace(",", ".")
    if l == 2:
        pay = (int(tot) // 5000 + 1) * 5000
        stem = f"Se compran los productos de la tabla y se paga con ${pay:,}. ¿Cuánto vuelto se recibe?".replace(",", ".")
        val = pay - tot
    else:
        stem = "Se compran los productos de la tabla. ¿Cuál es el total a pagar?"
        val = tot
    alts = [val * 10, val / 10 if (val / 10).denominator == 1 else val + 100, sum(p for n, p in items) + int(sum(qty)) * 100, val + 1000, val - 500 if val > 500 else val + 500, sum(q for q in qty) * items[0][1]]
    alts = [a for a in alts if F(a).denominator == 1 and a > 0]
    ans = fmt(val)
    al = [x for x in dict.fromkeys(fmt(a) for a in alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Total = suma de cantidad × precio por kilo = {fmt(tot)}.")


def t_fuel(r, l):
    kmL = F(r.choice([105, 125, 115, 135, 145, 85]), 10)
    L = F(r.randint(20, 60))
    kind = r.choice(["km", "lit"] if l else ["km"])
    if kind == "km":
        val = kmL * L
        stem = f"Un auto rinde {dstr(kmL)} km por litro de bencina. ¿Cuántos kilómetros puede recorrer con {L} litros?"
        alts = [val * 10, val / 10, L + kmL, L / kmL if terminates(L / kmL) else val + 10, val + kmL]
        unit = " km"
    else:
        km = kmL * r.randint(20, 40)
        val = km / kmL
        stem = f"Un auto rinde {dstr(kmL)} km por litro de bencina. ¿Cuántos litros necesita para recorrer {dstr(km)} km?"
        alts = [val * 10, val / 10, km * kmL if terminates(km * kmL) else val + 5, km - kmL, val + 1]
        unit = " L"
    ans = dstr(val) + unit
    fig = card([f"Rendimiento: {dstr(kmL)} km por litro", "Distancia = rendimiento × litros"], 130, 20)
    if not terminates(val):
        raise Reject
    al = [dstr(a) + unit for a in alts if a is not None and terminates(F(a))]
    al = [x for x in dict.fromkeys(al) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, "Se multiplica o divide según lo pedido, cuidando la posición de la coma.")


CONV = [("m", "cm", 100), ("km", "m", 1000), ("kg", "g", 1000), ("L", "mL", 1000), ("h", "min", 60)]


def t_units(r, l):
    a, b, k = r.choice(CONV if l else CONV[:4])
    x = F(r.randint(11, 99), 10)
    if k == 60:
        x = F(r.choice([25, 35, 45, 15, 55]), 10)
    val = x * k
    fig = card([f"Medida: {dstr(x)} {a}", f"1 {a} = {k} {b}"], 130, 21)
    stem = f"Una medida es {dstr(x)} {a}. ¿A cuántos {b} equivale? (1 {a} = {k} {b})"
    fmtv = lambda v: (dstr(F(v)) if terminates(F(v)) else fs(F(v))) + f" {b}"
    ans = fmtv(val)
    alts = [x * k * 10, x * k / 10, x / k, x + k, x * (k // 10) if k != 60 else x * 6]
    al = [fmtv(v) for v in alts]
    al = [t for t in dict.fromkeys(al) if t != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"{dstr(x)} · {k} = {dstr(val)}.")


# ---------------------------------------------------------------- Representar
def t_numline_dec(r, l):
    if l == 0:
        lo, step = r.choice([0, 1, 2, 3]), F(1, 10)
    elif l == 1:
        lo, step = r.choice([0, 1, 4]), F(1, 20)
    else:
        lo, step = r.choice([1, 2, 3]), F(1, 4)
    hi = lo + 1
    k = r.randint(1, int(1 / step) - 1)
    v = lo + k * step
    lab = lambda t: dstr(t) if ((t * 10).denominator == 1 or step == F(1, 4)) else ""
    fig = numline(lo, hi, {"A": v}, step=step, fmt=lab)
    ans = dstr(v)
    alts = [v + step, v - step, v * 10, v / 10, v + 2 * step]
    al = dopts(v, alts)
    return make("En la recta numérica, cada tramo entre marcas consecutivas mide lo mismo. ¿Qué número decimal representa el punto A?", fig, ans, al[:4], Q_REP, f"Cada marca avanza {dstr(step)}; A = {ans}.")


def cards3(vals):
    body = ""
    for i, (lab, v) in enumerate(zip("ABC", vals)):
        x = 30 + i * 175
        body += R(x, 30, 155, 90, FILL if i != 1 else FILL2, NAVY, 3) + tag(x + 28, 30, lab, 16) + T(x + 78, 88, v, 30)
    return wrap(560, 140, body, "Tres números decimales")


def t_order_dec(r, l):
    for _ in range(200):
        vals = [F(r.randint(1, 99), 10 ** r.choice([1, 2, 3])) for _ in range(3)]
        if len(set(vals)) == 3 and all(terminates(v) for v in vals) and max(len(dstr(v)) for v in vals) > min(len(dstr(v)) for v in vals):
            break
    else:
        raise Reject
    fig = cards3([dstr(v) for v in vals])
    lab = dict(zip("ABC", vals))
    order = sorted(lab, key=lab.get)
    ans = " < ".join(order)
    alts = [" < ".join(p) for p in itertools.permutations("ABC") if " < ".join(p) != ans]
    return make("Se muestran tres números decimales. ¿Cuál es el orden correcto de menor a mayor?", fig, ans, r.sample(alts, 4), Q_REP, f"Se comparan cifra a cifra con el mismo valor posicional: {ans}.")


PLACE = ["centenas", "decenas", "unidades", "décimas", "centésimas", "milésimas"]
VALS = {0: 100, 1: 10, 2: 1, 3: F(1, 10), 4: F(1, 100), 5: F(1, 1000)}


def t_place(r, l):
    digs = r.sample(range(1, 10), 6)
    idx = r.randint(0, 5) if l else r.randint(1, 5)
    body = ""
    cw = 80
    for i in range(6):
        x = 30 + i * cw + (18 if i >= 3 else 0)
        body += R(x, 30, cw, 40, FILL) + T(x + cw / 2, 56, PLACE[i], 13)
        body += R(x, 70, cw, 56, FILL2 if i == idx else WHITE) + T(x + cw / 2, 108, str(digs[i]), 32)
    fig = wrap(560, 150, body, "Tabla de valor posicional")
    val = digs[idx] * VALS[idx]
    num = f"{digs[0]}{digs[1]}{digs[2]},{digs[3]}{digs[4]}{digs[5]}"
    stem = f"La tabla muestra el número {num} con un dígito destacado. ¿Qué valor representa ese dígito?"
    sh = lambda v: dstr(F(v)) if terminates(F(v)) else fs(F(v))
    ans = sh(val)
    alts = [digs[idx] * VALS[j] for j in range(6) if j != idx] + [digs[idx]]
    al = [sh(a) for a in alts]
    al = [x for x in dict.fromkeys(al) if x != ans]
    r.shuffle(al)
    return make(stem, fig, ans, al[:4], Q_REP, f"El dígito {digs[idx]} está en las {PLACE[idx]}: vale {ans}.")


# ---------------------------------------------------------------- Argumentar
SIT = [
    ("Se necesitan trasladar {a} personas en buses de {b} asientos; ¿cuántos buses hay que pedir?", "Redondear hacia arriba"),
    ("Con {a} metros de cinta se cortan trozos de {b} metros; ¿cuántos trozos completos se obtienen?", "Truncar (redondear hacia abajo)"),
    ("Se guardan {a} libros en cajas de {b} libros cada una; ¿cuántas cajas se necesitan?", "Redondear hacia arriba"),
    ("Con ${a} se compran entradas de ${b} cada una; ¿cuántas entradas alcanzan?", "Truncar (redondear hacia abajo)"),
]
OPT = ["Redondear hacia arriba", "Truncar (redondear hacia abajo)", "Redondear al entero más cercano", "Usar siempre el valor exacto sin aproximar", "Redondear a la décima más cercana"]


def t_pertinence(r, l):
    txt, ans = r.choice(SIT)
    b = r.choice([12, 15, 18, 25, 40, 45, 50])
    a = b * r.randint(2, 9) + r.randint(1, b - 1)
    if "$" in txt:
        b, a = b * 100, a * 100
    q = txt.format(a=f"{a:,}".replace(",", "."), b=f"{b:,}".replace(",", "."))
    fig = card([f"Cantidad total: {a:,}".replace(",", "."), f"Cantidad por unidad: {b:,}".replace(",", "."), f"División: {dstr(F(a, b), 2)}…"], 170, 20)
    stem = q + " ¿Qué aproximación del resultado de la división es pertinente?"
    return make(stem, fig, ans, [o for o in OPT if o != ans], Q_ARG, f"El contexto exige {ans.lower()}: no se puede tener una parte de bus, caja o entrada.")


def t_approx_claims(r, l):
    x = F(r.randint(10000, 99999), 10 ** 4) + r.randint(1, 8)
    xs = dstr(x, 4)
    combos = [(op, k) for op in ("redondear", "truncar") for k in (0, 1, 2, 3)]

    def res(op, k):
        n = rnd(x, k) if op == "redondear" else trunc(x, k)
        return dk(n, k)

    def stmt(op, k, val):
        pos = ["la unidad", "las décimas", "las centésimas", "las milésimas"][k]
        return f"Al {op} {xs} a {pos} se obtiene {val}"

    def bad_val(op, k):
        other = res("truncar" if op == "redondear" else "redondear", k)
        if other != res(op, k):
            return other
        n = (rnd(x, k) if op == "redondear" else trunc(x, k)) + 1
        return dk(n, k)

    r.shuffle(combos)
    picks = combos[:5]
    if r.random() < 0.5:
        f_op, f_k = picks[0]
        ans = stmt(f_op, f_k, bad_val(f_op, f_k))
        alts = [stmt(op, k, res(op, k)) for op, k in picks[1:5]]
        stem = f"Considera el número {xs}. ¿Cuál de las siguientes afirmaciones sobre aproximaciones es FALSA?"
    else:
        t_op, t_k = picks[0]
        ans = stmt(t_op, t_k, res(t_op, t_k))
        alts = [stmt(op, k, bad_val(op, k)) for op, k in picks[1:5]]
        stem = f"Considera el número {xs}. ¿Cuál de las siguientes afirmaciones sobre aproximaciones es VERDADERA?"
    fig = card([f"Número: {xs}", "Redondear: mira la cifra siguiente", "Truncar: se cortan las cifras"], 170, 19)
    return make(stem, fig, ans, alts, Q_ARG, "Redondear mira la cifra siguiente (≥ 5 sube); truncar solo elimina cifras.")


def _err(r):
    k = r.randrange(5)
    if k == 0:
        return ["0,3 + 0,25 = 0,28"], "Sumó 3 con 25 sin igualar las posiciones: las décimas y las centésimas no se alinean", \
            ["Sumó bien las cifras pero desplazó la coma un lugar a la derecha por error", "Restó los números en lugar de sumarlos y dejó la coma en su lugar", "Multiplicó los dos números y conservó los decimales de ambos sumandos", "Redondeó cada sumando a la décima antes de sumarlos entre sí"]
    if k == 1:
        return ["0,4 · 0,2 = 0,8"], "Multiplicó los decimales como si fueran enteros y no ubicó la coma según el total de decimales", \
            ["Sumó los dos decimales en lugar de multiplicarlos entre sí", "Multiplicó 4 por 2 y dividió el resultado por 10 una sola vez", "Dividió 0,4 por 0,2 en lugar de multiplicar ambos números", "Elevó al cuadrado el primer decimal y descartó el segundo"]
    if k == 2:
        return ["0,3 < 0,25 porque 3 < 25"], "Comparó las partes decimales como enteros, sin considerar el valor posicional de las cifras", \
            ["Comparó solo las primeras cifras decimales y decidió sin mirar las demás", "Restó los números y concluyó según el signo del resultado obtenido", "Comparó la cantidad de cifras y eligió el número más largo", "Convirtió a fracción pero comparó solo los denominadores obtenidos"]
    if k == 3:
        return ["1/3 = 0,3 (valor exacto)"], "Truncó un decimal periódico y lo trató como exacto: 1/3 = 0,333… con infinitos 3", \
            ["Dividió 3 por 1 en lugar de dividir 1 por 3 para obtener el decimal", "Redondeó bien a la décima pero luego lo llamó exacto por costumbre", "Confundió el decimal con la fracción 3/10 al escribir el resultado", "Escribió el decimal correcto pero con una cifra periódica de menos"]
    return ["2,5 : 0,5 = 0,5"], "Amplificó solo el divisor a un entero sin amplificar también el dividendo", \
        ["Multiplicó el dividendo por 10 y el divisor por 100 en la misma división", "Dividió 0,5 entre 2,5 en lugar de dividir 2,5 entre 0,5", "Restó los dos números y dejó el resultado como cociente de ellos", "Dividió los números ignorando las comas y no corrigió después el resultado"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 120, 21)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["0,50 y 0,5 representan el mismo número", "Entre 0,3 y 0,4 existen infinitos números decimales", "Todo decimal finito se puede escribir como fracción de enteros",
        "Al truncar 0,999 a las décimas se obtiene 0,9", "Un decimal periódico se puede escribir como fracción de enteros", "0,25 es menor que 0,3"]
FALSE = ["1/3 es igual a 0,3 exactamente", "0,45 es mayor que 0,5 porque 45 es mayor que 5", "Redondear siempre entrega un número mayor que el original",
         "Todo decimal con infinitas cifras es un número irracional", "Al multiplicar dos decimales menores que 1 el producto es mayor que ambos", "0,05 y 0,5 representan el mismo número"]


def _fig(r):
    return card(["Decimales y fracciones", "0,5 = 1/2   ·   0,333… = 1/3"], 120, 20)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre números decimales es verdadera?", "Sobre decimales y su relación con las fracciones, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con el valor posicional y la equivalencia entre decimales y fracciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre números decimales es falsa?", "Sobre decimales y su relación con las fracciones, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice el valor posicional o la equivalencia con fracciones.")


BY_SKILL = {
    Q_RES: [t_frac_to_dec, t_dec_to_frac, t_dec_ops],
    Q_MOD: [t_price, t_fuel, t_units],
    Q_REP: [t_numline_dec, t_order_dec, t_place],
    Q_ARG: [t_pertinence, t_approx_claims, t_error, t_true, t_false],
}
