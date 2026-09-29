"""Clase 3 (M1) · Números racionales: operatoria con fracciones, orden y recta numérica."""
import itertools
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import numline, frac_bars, frac_pie, grid_shaded


def sf(fn):
    try:
        return fn()
    except (ZeroDivisionError, ValueError):
        return None


def opts(ans, alts):
    """Cadenas únicas por valor, distintas de la correcta."""
    seen, out = {fs(ans)}, []
    for a in alts:
        if a is None:
            continue
        s = fs(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def mx(x):
    x = F(x)
    if x.denominator == 1:
        return fs(x)
    w = int(abs(x) // 1)
    fr = abs(x) - w
    neg = "−" if x < 0 else ""
    return f"{neg}{w} {fr.numerator}/{fr.denominator}" if w else f"{neg}{fr.numerator}/{fr.denominator}"


def rfr(r, dens, lo=1, hi=None):
    d = r.choice(dens)
    n = r.randint(lo, hi or d + 3)
    if n % d == 0:
        n += 1
    return F(n, d)


def T3(a):
    return f"{a.numerator}/{a.denominator}"


# ---------------------------------------------------------------- Resolver problemas
def t_frac_ops(r, l):
    if l == 0:
        a, b = rfr(r, [2, 3, 4, 5, 6], 1, 8), rfr(r, [2, 3, 4, 5, 6], 1, 8)
        if a.denominator == b.denominator and r.random() < 0.5:
            pass
        sign = r.choice(["+", "−"])
        val = a + b if sign == "+" else a - b
        disp = f"{T3(a)} {sign} {T3(b)}"
        n1, d1, n2, d2 = a.numerator, a.denominator, b.numerator, b.denominator
        alts = [sf(lambda: F(n1 + n2 if sign == "+" else n1 - n2, d1 + d2 if sign == "+" else abs(d1 - d2) or 1)), sf(lambda: F(n1 + n2 if sign == "+" else n1 - n2, d1 * d2)), a * b, a + b if sign == "−" else a - b, b - a if sign == "−" else a * b + 1, val + F(1, d1 * d2)]
        ex = "Se amplifica a un común denominador y se opera solo con los numeradores."
    elif l == 1:
        op = r.choice(["·", ":", "+", "−"])
        a, b = rfr(r, [2, 3, 4, 5, 6, 8, 9], 1, 12), rfr(r, [2, 3, 4, 5, 6, 8, 9], 1, 12)
        val = {"·": a * b, ":": a / b, "+": a + b, "−": a - b}[op]
        disp = f"{T3(a)} {op} {T3(b)}"
        alts = [a * b, a / b, b / a, a + b, a - b, sf(lambda: F(a.numerator + b.numerator, a.denominator + b.denominator)), sf(lambda: F(a.numerator * b.denominator, a.denominator * b.numerator + 1))]
        ex = {"·": "Se multiplican numeradores y denominadores.", ":": "Dividir es multiplicar por el inverso de la segunda fracción.", "+": "Se suman con común denominador.", "−": "Se restan con común denominador."}[op]
    else:
        a, b, c = (rfr(r, [2, 3, 4, 5, 6, 8], 1, 9) for _ in range(3))
        form = r.choice(["a+b*c", "(a-b):c", "a:b+c", "a-b*c"])
        val = {"a+b*c": a + b * c, "(a-b):c": (a - b) / c, "a:b+c": a / b + c, "a-b*c": a - b * c}[form]
        disp = {"a+b*c": f"{T3(a)} + {T3(b)} · {T3(c)}", "(a-b):c": f"({T3(a)} − {T3(b)}) : {T3(c)}", "a:b+c": f"{T3(a)} : {T3(b)} + {T3(c)}", "a-b*c": f"{T3(a)} − {T3(b)} · {T3(c)}"}[form]
        wrong = {"a+b*c": [(a + b) * c, a + b + c, a * b * c], "(a-b):c": [a - b / c, (a - b) * c, a - b - c], "a:b+c": [a / (b + c), a * b + c, a / b * c], "a-b*c": [(a - b) * c, a - b - c, a + b * c]}[form]
        alts = wrong + [-val, val + F(1, 6)]
        ex = "Se respeta la prioridad: primero paréntesis, luego multiplicación/división y al final suma/resta."
    if abs(val) > 40:
        raise Reject
    fig = card(["Calcula:", disp], 130, 24)
    return make("¿Cuál es el resultado de la operación de la figura? (Se entrega simplificado.)", fig, fs(val), pick4(fs(val), opts(val, alts)), Q_RES, ex)


def t_frac_of(r, l):
    d1 = r.choice([3, 4, 5, 6, 8])
    n1 = r.randint(1, d1 - 1)
    f1 = F(n1, d1)
    if l == 0:
        N = d1 * r.randint(2, 12)
        val = f1 * N
        txt = f"los {T3(f1)} de {N}"
        alts = [N - val, F(N, 1) / f1, N + val, f1 + N, val + d1]
    else:
        d2 = r.choice([2, 3, 4, 5])
        n2 = r.randint(1, d2 - 1)
        f2 = F(n2, d2)
        N = d1 * d2 * r.randint(1, 6)
        val = f1 * f2 * N
        txt = f"los {T3(f1)} de los {T3(f2)} de {N}"
        alts = [(f1 + f2) * N, N * f1, N * f2, N - val, f1 * N / f2 if False else N * (1 - f1) * f2]
    if val.denominator != 1:
        raise Reject
    fig = card(["Calcula:", txt], 120, 22)
    return make("¿Cuál es el valor de lo indicado en la figura?", fig, fs(val), pick4(fs(val), opts(val, alts)), Q_RES, "«De» indica multiplicar la fracción por la cantidad.")


def t_mixed(r, l):
    a = F(r.randint(1, 4)) + F(r.randint(1, 4), r.choice([2, 3, 4, 5]))
    b = F(r.randint(1, 3)) + F(r.randint(1, 4), r.choice([2, 3, 4, 5]))
    if a.denominator == 1 or b.denominator == 1:
        raise Reject
    op = r.choice(["+", "−", "·"] if l else ["+", "−"])
    if op == "−" and a < b:
        a, b = b, a
    val = {"+": a + b, "−": a - b, "·": a * b}[op]
    disp = f"{mx(a)} {op} {mx(b)}"
    wa, fa, wb, fb = int(a), a - int(a), int(b), b - int(b)
    alts = [(wa + wb) + (fa + fb) if op == "+" else (wa - wb) + (fa - fb), wa * wb + fa * fb if op == "·" else None, F(wa) + F(wb) + F(fa.numerator + fb.numerator, fa.denominator + fb.denominator), val + 1, val - 1 if val > 1 else val + F(1, 2), a * b if op != "·" else a + b]
    alts = [x for x in alts if x is not None]
    fig = card(["Calcula:", disp], 120, 24)
    ans = mx(val)
    al = [mx(x) for x in dict.fromkeys(alts)]
    al = [x for x in dict.fromkeys(al) if x != ans]
    return make("¿Cuál es el resultado de la operación entre números mixtos? (Se entrega como número mixto o fracción simplificada.)", fig, ans, al[:4], Q_RES, "Se convierten los mixtos a fracciones impropias antes de operar.")


# ---------------------------------------------------------------- Modelar
def t_recipe(r, l):
    p, q = r.choice([(4, 6), (4, 10), (6, 9), (2, 5), (6, 15), (8, 12), (4, 14)])
    kg = F(r.randint(1, 5), r.choice([2, 3, 4]))
    ing = r.choice(["harina", "azúcar", "arroz", "queso"])
    val = kg * F(q, p)
    fig = card([f"Receta para {p} personas", f"Usa {T3(kg) if kg.denominator != 1 else kg} kg de {ing}"], 130, 21)
    stem = f"Una receta para {p} personas usa {T3(kg) if kg.denominator != 1 else kg} kg de {ing}. ¿Cuántos kg de {ing} se necesitan para {q} personas, manteniendo la proporción?"
    alts = [kg * F(p, q), kg + F(q - p), kg * q, kg + F(q - p, p), val + kg]
    return make(stem, fig, fs(val), pick4(fs(val), opts(val, alts)), Q_MOD, f"Se multiplica por la razón {q}/{p}: {fs(val)} kg.")


def t_rest(r, l):
    a, b = r.choice([(3, 4), (2, 5), (4, 5), (3, 5), (2, 3), (5, 6)]), r.choice([(1, 2), (1, 3), (1, 4), (2, 3), (1, 5)])
    f1, f2 = F(1, a[0]) if False else F(*b), F(1, a[1])
    f1, f2 = F(1, r.choice([3, 4, 5])), F(1, r.choice([2, 3, 4]))
    tot = r.choice([120, 240, 360, 600, 720, 840, 60, 180])
    rest = tot * (1 - f1) * (1 - f2)
    if rest.denominator != 1:
        raise Reject
    fig = card([f"Dinero inicial: ${tot:,}".replace(",", "."), f"Gasta {T3(f1)} del total", f"Luego gasta {T3(f2)} de lo que queda"], 170, 20)
    stem = "Una persona gasta su dinero como indica la figura. ¿Cuánto dinero le queda?"
    fmt = lambda x: "$" + f"{int(x):,}".replace(",", ".")
    alts = [tot * (1 - f1 - f2), tot * (1 - f1), tot * (f1 + f2), tot * (1 - f2), tot - tot * f1 - tot * f2 + tot // 10]
    alts = [fmt(x) for x in alts if F(x).denominator == 1 and x > 0]
    alts = [x for x in dict.fromkeys(alts) if x != fmt(rest)]
    return make(stem, fig, fmt(rest), alts[:4], Q_MOD, f"Queda {tot}·(1 − {T3(f1)})·(1 − {T3(f2)}) = {fmt(rest)}.")


def t_tank(r, l):
    a, b = r.choice([(3, 6), (2, 6), (4, 12), (3, 12), (5, 20), (6, 12), (2, 4), (4, 6)])
    if a >= b:
        raise Reject
    fig = card([f"Una llave llena un estanque en {a} horas", f"Un desagüe lo vacía en {b} horas"], 130, 19)
    stem = f"Un estanque se llena con una llave en {a} horas y se vacía con un desagüe en {b} horas. Si ambos funcionan a la vez y el estanque parte vacío, ¿en cuántas horas se llena?"
    t = F(a * b, b - a)
    alts = [F(a + b, 2), a + b, b - a, F(a * b, a + b), F(b, a)]
    ans = mx(t) + " h"
    al = [mx(x) + " h" for x in alts]
    al = [x for x in dict.fromkeys(al) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Rapidez neta = 1/{a} − 1/{b} = {fs(F(1, a) - F(1, b))} del estanque por hora; tiempo = {mx(t)} h.")


# ---------------------------------------------------------------- Representar
def t_numline_frac(r, l):
    den = r.choice([2, 3, 4, 5, 6] if l < 2 else [4, 5, 6, 8])
    lo, hi = (0, 2) if l < 2 else (-1, 1)
    k = r.randint(int(lo * den) + 1, int(hi * den) - 1)
    v = F(k, den)
    if v == 0 or v.denominator == 1:
        raise Reject
    fig = numline(lo, hi, {"A": v}, step=F(1, den))
    if l == 1:
        ans, alts = mx(v), [F(k + 1, den), F(k - 1, den), F(k, den + 1), F(den, k) if k else 1, F(k, den * 2), -v]
    else:
        ans, alts = fs(v), [F(k + 1, den), F(k - 1, den), F(k, den + 1), F(den, k) if k else 1, F(k, den * 2), -v]
    al = [mx(x) if l == 1 else fs(x) for x in alts]
    al = [x for x in dict.fromkeys(al) if x != ans]
    return make("En la recta numérica, cada tramo entre marcas consecutivas mide lo mismo. ¿Qué número representa el punto A?", fig, ans, al[:4], Q_REP, f"Cada marca avanza 1/{den}; A está en {fs(v)}.")


def t_order_bars(r, l):
    dens = r.sample([3, 4, 5, 6, 8, 10], 3)
    fr = [F(r.randint(1, d - 1), d) for d in dens]
    if len(set(fr)) < 3:
        raise Reject
    fig = frac_bars([(lab, f.numerator, f.denominator) if f.denominator == d else (lab, f.numerator, f.denominator) for lab, f, d in zip("ABC", fr, dens)])
    lab = dict(zip("ABC", fr))
    order = sorted(lab, key=lab.get)
    ans = " < ".join(order)
    alts = [" < ".join(p) for p in itertools.permutations("ABC") if " < ".join(p) != ans]
    return make("Las barras representan las fracciones A, B y C. ¿Cuál es el orden correcto de menor a mayor?", fig, ans, r.sample(alts, 4), Q_REP, f"Se compara qué parte de la barra está sombreada: {ans}.")


def t_shaded(r, l):
    den = r.choice([3, 4, 5, 6, 8, 10, 12])
    num = r.randint(1, den - 1)
    kind = r.choice(["pie", "grid"]) if den not in (5, 7) else "pie"
    if kind == "pie":
        fig = frac_pie(num, den)
    else:
        rows = {4: 1, 6: 2, 8: 2, 10: 2, 12: 3}.get(den, 1)
        if den == 3: rows = 1
        cols = den // rows
        fig = grid_shaded(rows, cols, num)
    ask = r.choice(["sh", "un", "pc"] if l else ["sh", "un"])
    if ask == "sh":
        stem, val = "¿Qué fracción de la figura está sombreada?", F(num, den)
    elif ask == "un":
        stem, val = "¿Qué fracción de la figura NO está sombreada?", F(den - num, den)
    else:
        stem, val = "¿Qué porcentaje aproximado de la figura está sombreado?", None
    if val is not None:
        ans = fs(val)
        alts = [F(num, den - num) if den != num else 1, F(den - num, den) if ask == "sh" else F(num, den), F(num, den + 1), F(den, num), F(num + 1, den), F(den - num, num)]
        return make(stem, fig, ans, pick4(ans, opts(val, alts)), Q_REP, f"Hay {num} partes sombreadas de {den} iguales.")
    pcs = F(num * 100, den)
    fmt = lambda x: (f"{float(x):.1f}".rstrip("0").rstrip(".").replace(".", ",")) + "%"
    ans = fmt(pcs)
    alts = [fmt(F(num, den) * 10), fmt(100 - pcs), fmt(F(den * 100, num)), fmt(F(num, den + 1) * 100), fmt(pcs + 5)]
    alts = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, alts[:4], Q_REP, f"{num}/{den} = {ans}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b, c, d = r.sample(range(2, 9), 4)
    if k == 0:
        return [f"{a}/{b} + {c}/{d} = {a + c}/{b + d}"], "Sumó numeradores y denominadores por separado en vez de amplificar a un común denominador", \
            ["Multiplicó los denominadores pero olvidó multiplicar los numeradores por el factor", "Sumó los numeradores y conservó el denominador de la primera fracción", "Restó las fracciones en lugar de sumarlas antes de simplificar el resultado", "Amplificó solo la segunda fracción y sumó los numeradores sin cambiarlos"]
    if k == 1:
        return [f"{a}/{b} : {c}/{d} = {a * c}/{b * d}"], "Multiplicó las fracciones sin invertir la segunda: dividir es multiplicar por el inverso", \
            ["Invirtió la primera fracción en lugar de invertir la segunda", "Restó los numeradores y los denominadores de ambas fracciones", "Sumó los numeradores y dejó el denominador de la segunda", "Simplificó en cruz antes de dividir y perdió un factor común"]
    if k == 2:
        n = a * 2
        return [f"{n}/{n + 2 * b} = {n - a}/{n + 2 * b - a}"], "Simplificó restando el mismo número arriba y abajo: solo se puede dividir por un factor común", \
            ["Sumó el mismo número al numerador y al denominador sin dividir por nada", "Dividió el numerador por un factor y el denominador por otro distinto", "Multiplicó el numerador por un número y el denominador por otro distinto", "Simplificó bien pero no expresó el resultado en su forma irreductible"]
    if k == 3:
        return [f"{a}/{b} · {c} = {a * c}/{b * c}"], "Multiplicó también el denominador por el entero: un entero multiplica solo al numerador", \
            ["Dividió el numerador por el entero en vez de multiplicarlo", "Sumó el entero al numerador y al denominador de la fracción", "Multiplicó el numerador por el entero y sumó el entero al denominador", "Convirtió el entero en fracción pero olvidó multiplicar los denominadores"]
    return [f"{a}/{b} − {c}/{d} = {a - c}/{b - d}".replace("-", "−")], "Restó numeradores y denominadores por separado en lugar de amplificar a un común denominador", \
        ["Restó los denominadores pero sumó los numeradores de ambas fracciones", "Multiplicó ambos denominadores y restó los numeradores sin amplificarlos", "Restó la segunda fracción de la primera pero cambió el orden de los términos", "Calculó bien el común denominador pero restó mal los numeradores amplificados"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 120, 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["Entre dos números racionales distintos siempre existe otro racional", "Si a y b son positivos y a < b, entonces 1/a > 1/b", "Un número racional se puede escribir como fracción de enteros con denominador distinto de cero",
        "Multiplicar numerador y denominador por un mismo número distinto de cero entrega una fracción equivalente", "Todo número entero es también un número racional", "Dividir por una fracción equivale a multiplicar por su inverso"]
FALSE = ["Si el denominador es mayor, la fracción es siempre menor", "La suma de dos fracciones es la suma de sus numeradores sobre la suma de sus denominadores", "Sumar el mismo número al numerador y al denominador entrega una fracción equivalente",
         "Existe un racional que es el menor de los mayores que 0", "Al multiplicar dos fracciones propias se obtiene una fracción mayor que ambas", "Toda fracción con numerador mayor que el denominador es menor que 1"]


def _fig_frac(r):
    dens = r.sample([3, 4, 5, 6, 8], 2)
    return frac_bars([("A", r.randint(1, dens[0] - 1), dens[0]), ("B", r.randint(1, dens[1] - 1), dens[1])])


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre números racionales es verdadera?", "Sobre las fracciones y su orden, ¿cuál afirmación es correcta?"]), _fig_frac(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta cada afirmación con las propiedades de las fracciones.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre números racionales es falsa?", "Sobre las fracciones y su orden, ¿cuál afirmación es incorrecta?"]), _fig_frac(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de los racionales.")


def t_not_equiv(r, l):
    d = r.randint(2, 9)
    n = r.choice([x for x in range(1, 12) if gcd_(x, d) == 1])
    base = F(n, d)
    mult = r.sample([2, 3, 4, 5, 6, 7], 4)
    eq = [f"{n * m}/{d * m}" for m in mult]
    m = r.choice([2, 3, 4])
    bad = r.choice([f"{n * m + 1}/{d * m}", f"{n * m}/{d * m + 1}", f"{n + m}/{d + m}", f"{n * m}/{d * m - 1}"])
    if F(*map(int, bad.split("/"))) == base:
        raise Reject
    fig = card([f"Fracción base: {n}/{d}", "Fracciones equivalentes: mismo valor"], 130, 20)
    stem = f"La fracción {n}/{d} se compara con otras. ¿Cuál de las siguientes NO es equivalente a {n}/{d}?"
    return make(stem, fig, bad, eq, Q_ARG, "Dos fracciones son equivalentes si sus productos cruzados son iguales.")


def gcd_(a, b):
    from math import gcd
    return gcd(a, b)


BY_SKILL = {
    Q_RES: [t_frac_ops, t_frac_of, t_mixed],
    Q_MOD: [t_recipe, t_rest, t_tank],
    Q_REP: [t_numline_frac, t_order_bars, t_shaded],
    Q_ARG: [t_error, t_true, t_false, t_not_equiv],
}
