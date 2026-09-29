"""Clase 1 (M1) · Números enteros: operatoria y prioridades (paréntesis y signos)."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, z, par, sgn_term, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import numline, signed_bars
import viz


def ev(s, **v):
    return eval(s, {}, v)


def strs(ans, alts):
    seen, out = {fs(ans)}, []
    for a in alts:
        s = fs(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def rr(r, lo, hi, nz=True):
    while True:
        x = r.randint(lo, hi)
        if x or not nz:
            return x


# ---------------------------------------------------------------- Resolver problemas
def t_eval(r, l):
    a, b, c, d, e = (rr(r, -9, 9) for _ in range(5))
    if l == 0:
        k = r.randrange(3)
        if k == 0:
            disp, ok, bad = f"{z(a)} + {par(b)} · {par(c)}", "a+b*c", ["(a+b)*c", "a+b+c", "a-b*c"]
        elif k == 1:
            disp, ok, bad = f"{z(a)} − {par(b)} · {par(c)}", "a-b*c", ["(a-b)*c", "a-b-c", "a+b*c"]
        else:
            disp, ok, bad = f"{z(a)} − ({z(b)} − {par(c)})", "a-(b-c)", ["a-b-c", "a+b-c", "a-b+(-c)"]
    elif l == 1:
        k = r.randrange(3)
        if k == 0:
            disp, ok, bad = f"{z(a)} − {par(b)} · ({z(c)} − {par(d)})", "a-b*(c-d)", ["(a-b)*(c-d)", "a-b*c-d", "a-b*c-b*d"]
        elif k == 1:
            disp, ok, bad = f"({z(a)} − {par(b)}) · ({z(c)} − {par(d)})", "(a-b)*(c-d)", ["a-b*c-d", "(a-b)*c-d", "a-b*(c-d)"]
        else:
            b = abs(b)
            disp, ok, bad = f"{z(a)} − (−{b})²", "a-b**2", ["a+b**2", "a-(-b**2)*(-1)*(-1)-b", "a-2*b"]
    else:
        k = r.randrange(2)
        if k == 0:
            disp, ok, bad = f"−{abs(a)} − ({z(b)} − ({z(c)} − {par(d)})) · {par(e)}", "-abs(a)-(b-(c-d))*e", ["-abs(a)-(b-c-d)*e", "-abs(a)-(b-(c-d)*e)", "-abs(a)+(b-(c-d))*e"]
        else:
            disp, ok, bad = f"{par(a)} · {par(b)} − ({z(c)} − {par(d)}) · {par(e)}", "a*b-(c-d)*e", ["a*b-(c-d)*e*(-1)", "a*(b-(c-d))*e", "a*b-c-d*e"]
    v = dict(a=a, b=b, c=c, d=d, e=e)
    val = ev(ok, **v)
    alts = [ev(x, **v) for x in bad] + [-val, val + 2, val - 2, val + 10]
    ans = z(val)
    if abs(val) > 400:
        raise Reject
    fig = card(["Calcula el valor de:", disp], 130, 24)
    return make("¿Cuál es el valor de la expresión de la figura?", fig, ans, pick4(ans, strs(val, alts)), Q_RES,
                "Se respetan paréntesis, potencias y multiplicaciones antes de sumar o restar, cuidando la regla de los signos.")


CTXT = [("Un termómetro", "°C"), ("Una cámara frigorífica", "°C"), ("Una estación meteorológica", "°C")]


def t_changes(r, l):
    ctx = r.choice(CTXT)
    start = r.randint(-12, 10)
    ch = [rr(r, -14, 14) for _ in range(3 + l)]
    v = start + sum(ch)
    if abs(v) > 40:
        raise Reject
    lines = [f"Temperatura inicial: {z(start)} {ctx[1]}"] + [f"{'Sube' if c > 0 else 'Baja'} {abs(c)} {ctx[1]}" for c in ch]
    fig = card(lines, 60 + 34 * len(lines), 19)
    ans = f"{z(v)} {ctx[1]}"
    alts = [start + sum(abs(c) for c in ch), start - sum(abs(c) for c in ch), -v, start + sum(ch[:-1]) - ch[-1], v + ch[0]]
    alts = [f"{fs(a)} {ctx[1]}" for a in alts]
    alts = [a for a in dict.fromkeys(alts) if a != ans]
    return make(f"{ctx[0]} registra los cambios de la figura. ¿Cuál es la temperatura final?", fig, ans, alts[:4], Q_RES,
                f"Se suman los cambios con su signo: {z(start)} " + " ".join(sgn_term(c) for c in ch) + f" = {z(v)}.")


PLACES = ["Un buzo", "Una sonda", "Un minero", "Un dron"]


def t_diff_extremes(r, l):
    n = 4 + l
    labs = ["A", "B", "C", "D", "E", "F"][:n]
    vals = r.sample([x for x in range(-60, 61, 5) if x != 0], n)
    if min(vals) > 0 or max(vals) < 0:
        raise Reject
    fig = signed_bars(vals, labs, "m")
    stem = "El gráfico muestra la altura, en metros respecto del nivel del mar, de los puntos indicados. ¿Cuál es la diferencia de altura entre el punto más alto y el más bajo?"
    diff = max(vals) - min(vals)
    ans = f"{diff} m"
    alts = [max(vals) + min(vals), abs(max(vals)) + abs(min(vals)) if False else max(vals) - abs(min(vals)), abs(min(vals)) - max(vals), max(vals) if diff != max(vals) else diff + 5, diff + 10, diff - 5]
    alts = [f"{fs(a)} m" for a in alts]
    alts = [a for a in dict.fromkeys(alts) if a != ans]
    return make(stem, fig, ans, alts[:4], Q_RES, f"Diferencia = {max(vals)} − ({z(min(vals))}) = {diff}.")


# ---------------------------------------------------------------- Modelar
def t_account(r, l):
    n = 3 + l
    ops = [rr(r, -60, 60) * 1000 for _ in range(n)]
    start = r.randint(10, 80) * 1000
    fin = start + sum(ops)
    body_rows = [["Saldo inicial", f"${start:,}".replace(",", ".")]] + [[("Depósito" if o > 0 else "Giro"), f"${abs(o):,}".replace(",", ".")] for o in ops]
    fig = viz.table_fig(["Movimiento", "Monto"], body_rows)
    kind = r.choice(["value", "expr"])
    if kind == "value":
        stem = "La tabla muestra los movimientos de una cuenta. ¿Cuál es el saldo final (en pesos; un saldo negativo indica sobregiro)?"
        ans = f"${z(fin // 1000)}.000".replace("$−", "−$") if False else (f"−${abs(fin):,}".replace(",", ".") if fin < 0 else f"${fin:,}".replace(",", "."))
        f = lambda x: (f"−${abs(x):,}".replace(",", ".") if x < 0 else f"${x:,}".replace(",", "."))
        alts = [f(start + sum(abs(o) for o in ops)), f(start - sum(abs(o) for o in ops)), f(-fin), f(start + sum(ops[:-1]) - ops[-1]), f(fin + 20000)]
        alts = [a for a in dict.fromkeys(alts) if a != ans]
        ex = "Saldo final = saldo inicial + depósitos − giros."
        return make(stem, fig, ans, alts[:4], Q_MOD, ex)
    k = lambda x: str(x // 1000)
    ans_e = k(start) + "".join(sgn_term(o // 1000) for o in ops)
    bad1 = k(start) + "".join(" + " + str(abs(o) // 1000) for o in ops)
    bad2 = k(start) + "".join(" − " + str(abs(o) // 1000) for o in ops)
    bad3 = k(start) + "".join(sgn_term(-o // 1000) for o in ops)
    bad4 = k(start) + "".join(sgn_term(o // 1000) for o in ops[:-1]) + sgn_term(-ops[-1] // 1000)
    stem = "Los movimientos de la tabla están en miles de pesos. ¿Qué expresión modela el saldo final (en miles de pesos)?"
    alts = [x for x in dict.fromkeys([bad1, bad2, bad3, bad4]) if x != ans_e]
    return make(stem, fig, ans_e, alts[:4], Q_MOD, "Los depósitos suman y los giros restan: cada movimiento entra con su signo.")


def t_floors(r, l):
    start = r.choice([-4, -3, -2, 0, 1, 3])
    a, b = r.randint(3, 9), r.randint(2, 8)
    c = r.randint(2, 6) if l else None
    stem_moves = f"sube {a} pisos, luego baja {b} pisos" + (f" y finalmente baja {c} pisos" if c else "")
    fin = start + a - b - (c or 0)
    fig = card([f"Un ascensor parte del piso {z(start)}", "Sube " + str(a) + " pisos", "Luego baja " + str(b) + " pisos"] + ([f"Finalmente baja {c} pisos"] if c else []), 60 + 34 * (3 + (1 if c else 0)), 19)
    ex = z(start) + f" + {a} − {b}" + (f" − {c}" if c else "")
    ans = ex.replace("+ ", "+ ").replace("−", "−")
    alts = [z(start) + f" + {a} + {b}" + (f" + {c}" if c else ""), z(start) + f" − {a} + {b}" + (f" + {c}" if c else ""), z(start) + f" − {a} − {b}" + (f" − {c}" if c else ""), z(start) + f" + {a} − {b}" + (f" + {c}" if c else ""), z(start) + f" + {b} − {a}" + (f" − {c}" if c else "")]
    alts = [x for x in dict.fromkeys(alts) if x != ans]
    return make("Considerando que los pisos subterráneos son negativos, ¿qué expresión permite calcular el piso final del ascensor?", fig, ans, alts[:4], Q_MOD,
                f"Sube suma y baja resta: {ex} = {z(fin)}.")


def t_profit(r, l):
    meses = ["Mar", "Abr", "May", "Jun", "Jul"][:3 + l]
    vals = [rr(r, -9, 12) for _ in meses]
    fig = signed_bars(vals, meses, "mill.")
    tot = sum(vals)
    stem = "El gráfico muestra la ganancia (positiva) o pérdida (negativa) mensual de un negocio, en millones de pesos. ¿Cuál es el resultado total del período?"
    fmt = lambda x: f"{fs(x)} millones"
    ans = fmt(tot)
    alts = [sum(abs(v) for v in vals), -tot, sum(v for v in vals if v > 0), sum(v for v in vals if v < 0), tot + 3, tot - 2]
    alts = [fmt(a) for a in dict.fromkeys(alts) if fmt(a) != ans]
    return make(stem, fig, ans, alts[:4], Q_MOD, f"Resultado = suma de los valores con su signo = {ans}.")


# ---------------------------------------------------------------- Representar
def t_numline_jump(r, l):
    lo, hi = -10, 10
    a = r.randint(-8, 3)
    b = r.choice([x for x in range(-7, 8) if abs(x) >= 3 and -10 <= a + x <= 10])
    c = r.choice([x for x in range(-7, 8) if abs(x) >= 3 and -10 <= a + b + x <= 10]) if l else None
    jumps = [(a, a + b, f"{'+' if b > 0 else '−'}{abs(b)}")]
    end = a + b
    if c:
        jumps.append((end, end + c, f"{'+' if c > 0 else '−'}{abs(c)}"))
        end += c
    fig = numline(lo, hi, {"P": a}, jumps=jumps)
    import itertools
    ans = z(a) + sgn_term(b) + (sgn_term(c) if c else "")
    pool = []
    for fa, fb, fc in itertools.product((1, -1), repeat=3):
        if (fa, fb, fc) == (1, 1, 1) or (not c and fc == -1):
            continue
        pool.append(z(fa * a) + sgn_term(fb * b) + (sgn_term(fc * c) if c else ""))
    pool.append(z(a) + sgn_term(2 * b) + (sgn_term(c) if c else ""))
    alts = [x for x in dict.fromkeys(pool) if x != ans]
    r.shuffle(alts)
    return make("En la recta numérica, P es el punto de partida y las flechas indican los desplazamientos. ¿Qué expresión representa el recorrido completo?", fig, ans, alts[:4], Q_REP,
                f"Cada flecha hacia la derecha suma y hacia la izquierda resta: el punto final es {z(end)}.")


def t_numline_order(r, l):
    vals = r.sample(range(-9, 10), 3)
    if min(abs(x - y) for i, x in enumerate(vals) for y in vals[i + 1:]) < 3:
        raise Reject
    lab = dict(zip("ABC", vals))
    fig = numline(-10, 10, {k: v for k, v in lab.items()})
    order = sorted(lab, key=lab.get)
    ans = " < ".join(order)
    import itertools
    alts = [" < ".join(p) for p in itertools.permutations("ABC") if " < ".join(p) != ans]
    stem = "En la recta numérica se ubican los números A, B y C. ¿Cuál de las siguientes ordenaciones de menor a mayor es correcta?"
    return make(stem, fig, ans, r.sample(alts, 4), Q_REP, f"Los números crecen hacia la derecha: {ans}.")


def t_numline_expr(r, l):
    A, B = r.sample(range(-9, 10), 2)
    if abs(A - B) < 3:
        raise Reject
    fig = numline(-10, 10, {"A": A, "B": B})
    kind = r.choice(["sum", "diff", "dist"])
    if kind == "sum":
        stem, val, ex = "En la recta numérica se ubican los números A y B. ¿Cuál es el valor de A + B?", A + B, f"{z(A)} + {par(B)}"
    elif kind == "diff":
        stem, val, ex = "En la recta numérica se ubican los números A y B. ¿Cuál es el valor de A − B?", A - B, f"{z(A)} − {par(B)}"
    else:
        stem, val, ex = "En la recta numérica se ubican los números A y B. ¿Cuántas unidades separan a A de B?", abs(A - B), f"|{z(A)} − {par(B)}|"
    ans = z(val)
    alts = [A + B, A - B, B - A, -(A + B), abs(A) + abs(B), abs(A + B), A, B, val + 1, val - 1]
    return make(stem, fig, ans, pick4(ans, strs(val, alts)), Q_REP, f"{ex} = {ans}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(6)
    a, b = r.randint(2, 9), r.randint(2, 9)
    if k == 0:
        return [f"{a} − ({b} − 3) = {a} − {b} − 3 = {a - b - 3}"], "Al quitar el paréntesis precedido por un signo menos, no cambió el signo de 3", \
            ["Sumó primero los dos primeros números y después restó el paréntesis", "Multiplicó el signo menos por el primer número del paréntesis", "Sumó los valores absolutos de todos los términos de la expresión", "Resolvió la expresión de derecha a izquierda sin cambiar signos"]
    if k == 1:
        return [f"−{a} · (−{b}) = −{a * b}"], "Multiplicó dos negativos y obtuvo un negativo: el producto debía ser positivo", \
            ["Sumó los números en lugar de multiplicarlos entre sí", "Cambió el signo de solo uno de los dos factores negativos", "Multiplicó bien los valores absolutos pero se equivocó en el cálculo", "Aplicó la regla de los signos de la suma a una multiplicación"]
    if k == 2:
        return [f"−{a}² = {a * a}"], "Interpretó −a² como (−a)²: el exponente solo afecta a la base, no al signo", \
            ["Multiplicó la base por 2 en lugar de elevarla al cuadrado", "Dividió la base por 2 en lugar de elevarla al cuadrado", "Restó el exponente a la base en lugar de elevar la base", "Elevó al cuadrado solo el signo negativo y no el número"]
    if k == 3:
        c = r.randint(2, 6)
        return [f"{a} + {b} · {c} = {(a + b) * c}"], "Sumó antes de multiplicar, sin respetar la prioridad de las operaciones", \
            ["Multiplicó los tres números entre sí en lugar de operarlos", "Restó en lugar de sumar el primer término de la expresión", f"Dividió por {c} en lugar de multiplicar por {c} al final", f"Multiplicó solo {b} por {a} y dejó {c} sin operar en la cuenta"]
    if k == 4:
        return [f"−{a} − {b} = {a - b}"], "Restó valores absolutos: −a − b tiene dos términos negativos, cuyas magnitudes se suman", \
            ["Sumó las magnitudes pero perdió el signo del resultado final", "Multiplicó los dos números en lugar de sumar sus magnitudes", "Restó el mayor al menor y dejó el signo del mayor", "Cambió el signo del primer número pero no el del segundo"]
    return [f"{a} − (−{b}) = {a - b}"], "Restó un número negativo como si fuera positivo: restar −b equivale a sumar b", \
        ["Sumó el opuesto del primer número al segundo número", "Cambió el signo del primer número en lugar del segundo", "Multiplicó ambos números en lugar de operarlos con signo", "Restó los valores absolutos y dejó el signo del segundo"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 120, 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["El producto de dos números negativos es positivo", "La suma de dos números negativos es negativa", "El opuesto de un número negativo es positivo",
        "Todo entero negativo es menor que cualquier entero positivo", "El cuadrado de cualquier entero distinto de cero es positivo", "−(a + b) equivale a −a − b para cualquier par de enteros",
        "Restar un entero es lo mismo que sumar su opuesto", "El producto de un positivo y un negativo es negativo"]
FALSE = ["La suma de dos números negativos siempre es positiva", "El cuadrado de un entero negativo es negativo", "Restar un número negativo disminuye el resultado",
         "−(a + b) equivale a −a + b para cualquier par de enteros", "Al multiplicar dos negativos se obtiene un negativo", "El opuesto de un entero positivo es positivo",
         "Un número negativo con mayor valor absoluto es mayor que otro negativo con menor valor absoluto", "La división de dos negativos es negativa"]


def _fig_sign(r):
    a, b = r.sample(range(-8, 9), 2)
    if abs(a - b) < 3:
        raise Reject
    return numline(-10, 10, {"a": a, "b": b})


def t_true(r, l):
    stem = r.choice(["¿Cuál de las siguientes afirmaciones sobre los números enteros es verdadera?", "Sobre las operaciones con enteros, ¿cuál afirmación es correcta?"])
    return make(stem, _fig_sign(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta cada afirmación con la regla de los signos y la definición de opuesto.")


def t_false_eq(r, l):
    a, b, c = r.sample(range(2, 10), 3)
    TR = [f"−({a} + {b}) = −{a} − {b}", f"−({a} − {b}) = −{a} + {b}", f"(−{a})² = {a * a}", f"−{a} · (−{b}) = {a * b}", f"{a} − (−{b}) = {a + b}", f"−{a} − {b} = −{a + b}", f"(−{a}) · {b} = −{a * b}", f"−(−{a}) = {a}"]
    FA = [f"−({a} + {b}) = −{a} + {b}", f"−{a}² = {a * a}", f"−{a} · (−{b}) = −{a * b}", f"{a} − (−{b}) = {a - b}", f"−{a} − {b} = {b - a}", f"(−{a}) + (−{b}) = {a + b}", f"−({a} − {b}) = −{a} − {b}"]
    ans = r.choice(FA)
    alts = r.sample(TR, 4)
    fig = card(["Propiedades de los signos", "−(a + b), (−a)², a − (−b)…"], 120, 20)
    return make("¿Cuál de las siguientes igualdades es FALSA?", fig, ans.replace("-", "−"), [x.replace("-", "−") for x in alts], Q_ARG, "Se comprueba cada igualdad con la regla de los signos.")


BY_SKILL = {
    Q_RES: [t_eval, t_changes, t_diff_extremes],
    Q_MOD: [t_account, t_floors, t_profit],
    Q_REP: [t_numline_jump, t_numline_order, t_numline_expr],
    Q_ARG: [t_error, t_true, t_false_eq],
}
