"""Clase 9 (M1) · Raíces enésimas: conceptos para M1 y estimación de raíces inexactas."""
import math
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from mathfmt import E, fmt, rs
from figs import numline
import viz

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def rt(n, idx=2):
    return f"√{n}" if idx == 2 else f"∛{n}" if idx == 3 else f"{str(idx).translate(SUP)}√{n}"


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        s = a if isinstance(a, str) else fs(F(a))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


SQ = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225]
CB = [8, 27, 64, 125, 216, 343, 512, 729, 1000]


# ---------------------------------------------------------------- Resolver problemas
def t_root_eval(r, l):
    if l == 0:
        idx = r.choice([2, 2, 3])
        base = r.randint(2, 15) if idx == 2 else r.randint(2, 9)
        n = base ** idx
        neg = idx == 3 and r.random() < 0.4
        v = -base if neg else base
        disp = rt(f"({-n})" if neg else n, idx)
        alts = [n // idx if not neg else -(n // idx), base + 1, base - 1 if base > 2 else base + 2, n, base * idx, -base if not neg else base]
        ex = f"{disp} = {v}, porque {v}{str(idx).translate(SUP)} = {v ** idx if not neg else -n}."
        ans = str(v)
        return make("¿Cuál es el valor de la raíz de la figura?", card(["Calcula:", disp], 130, 26), ans.replace("-", "−"), pick4(ans.replace("-", "−"), uq(ans.replace("-", "−"), [str(a).replace("-", "−") for a in alts if a != v])), Q_RES, ex)
    if l == 1:
        f = r.choice([2, 3, 5, 6, 7])
        k = r.choice([2, 3, 4, 5, 6])
        n = k * k * f
        ans = fmt(E((k, f)))
        alts = [fmt(E((k * k, f))), fmt(E((f, k * k if k * k != f else 1))) if f != 1 else None, fmt(E((k, 1 + f))), fmt(E((f, k))), fmt(E((k + f, 1))) if False else str(k * f)]
        disp = rt(n)
        return make("¿Cuál es la forma más simple de la raíz de la figura?", card(["Simplifica:", disp], 130, 26), ans, pick4(ans, uq(ans, alts)), Q_RES, f"{n} = {k * k}·{f}, luego {disp} = {k}√{f}.")
    f0 = r.choice([2, 3, 5, 6, 7])
    p, q = r.sample(range(1, 8), 2)
    a, b = f0 * p * p, f0 * q * q
    if a == b:
        raise Reject
    op = r.choice(["+", "−"])
    sa = math.isqrt(a // max(1, next(x for x in range(1, a + 1) if a % x == 0 and x * x <= a and all(True for _ in [0]) and False)) if False else 1)
    from mathfmt import sqfree
    ka, fa = sqfree(a)
    kb, fb = sqfree(b)
    if fa != fb:
        raise Reject
    tot = ka + kb if op == "+" else ka - kb
    if tot == 0:
        raise Reject
    ans = fmt(E((tot, fa)))
    alts = [fmt(E((1, a + b if op == "+" else abs(a - b)))), fmt(E((ka + kb if op == "−" else ka - kb, fa))) if (ka - kb) != 0 else None, fmt(E((tot, a + b))) if op == "+" else None, str(sum(1 for _ in range(1))), fmt(E((abs(tot), 1 + fa)))]
    alts = [x for x in alts if x and x != "0"]
    disp = f"√{a} {op} √{b}"
    return make("¿Cuál es el resultado de la operación de la figura?", card(["Calcula:", disp], 130, 24), ans, pick4(ans, uq(ans, alts + [fmt(E((tot + 1, fa))), fmt(E((tot, fa + 1)))])), Q_RES, f"√{a} = {ka}√{fa} y √{b} = {kb}√{fb}; se suman/restan los radicales semejantes: {ans}.")


def t_root_mul(r, l):
    kind = r.choice(["mul", "div"] if l else ["mul"])
    f0 = r.choice([2, 3, 5, 6, 7, 10, 11])
    p, q = r.randint(1, 6), r.randint(1, 6)
    a, b = f0 * p * p, f0 * q * q
    if kind == "div":
        a, b = f0 * p * p, f0 * p * p * q * q
    if kind == "mul":
        v = math.isqrt(a * b)
        if v * v != a * b:
            raise Reject
        disp = f"√{a} · √{b}"
        alts = [a + b, a * b, math.isqrt(a) + math.isqrt(b), v + 1, v * 2, F(a * b, 2)]
        ex = f"√{a}·√{b} = √{a * b} = {v}."
    else:
        q = F(b, a)
        s = math.isqrt(b // a) if b % a == 0 else 0
        if b % a or s * s != b // a:
            raise Reject
        v = s
        disp = f"√{b} : √{a}"
        alts = [b // a, b - a, F(b, a) * 2, v + 1, v * v + 1, v * 2]
        ex = f"√{b} : √{a} = √{b // a} = {v}."
    ans = str(v)
    return make("¿Cuál es el valor de la expresión de la figura?", card(["Calcula:", disp], 130, 24), ans, pick4(ans, uq(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_square_side(r, l):
    kind = r.choice(["area", "vol", "diag"] if l else ["area", "vol"])
    if kind == "area":
        s = r.randint(3, 20)
        A = s * s
        body = R(210, 30, 120, 120, FILL) + tag(270, 90, f"{A} m²", 20)
        stem = f"Un terreno cuadrado tiene un área de {A} m². ¿Cuánto mide cada lado?"
        ans = f"{s} m"
        alts = [f"{A // 2} m", f"{s * 2} m", f"{A - s} m", f"{s + 4} m", f"{s - 1} m"]
        ex = f"Lado = √{A} = {s} m."
    elif kind == "vol":
        s = r.randint(2, 10)
        Vv = s ** 3
        body = R(210, 50, 110, 110, FILL) + P([(210, 50), (240, 25), (350, 25), (320, 50)], FILL2) + P([(320, 50), (350, 25), (350, 135), (320, 160)], FILL3) + tag(265, 105, f"{Vv} cm³", 18)
        stem = f"Un cubo tiene un volumen de {Vv} cm³. ¿Cuánto mide cada arista?"
        ans = f"{s} cm"
        alts = [f"{Vv // 3} cm", f"{math.isqrt(Vv)} cm", f"{s * 3} cm", f"{s + 2} cm", f"{s - 1} cm"]
        ex = f"Arista = ∛{Vv} = {s} cm."
    else:
        s = r.randint(2, 12)
        body = R(210, 30, 120, 120, FILL) + L(210, 30, 330, 150, ACC, 4) + tag(270, 165, f"lado {s} m", 17) + tag(300, 80, "d", 17)
        stem = f"Un cuadrado tiene lados de {s} m. ¿Cuánto mide su diagonal?"
        ans = f"{s}√2 m"
        alts = [f"{2 * s} m", f"{s * s}√2 m", f"{s}√3 m", f"√{s} m", f"{2 * s}√2 m"]
        ex = f"Por Pitágoras: d = √({s}² + {s}²) = {s}√2."
    fig = wrap(560, 190, body, "Figura con la medida dada")
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_formula_root(r, l):
    kind = r.choice(["fall", "period", "speed"])
    if kind == "fall":
        h = r.choice([5, 20, 45, 80, 125, 180, 245])
        t = math.isqrt(h // 5)
        if t * t * 5 != h:
            raise Reject
        fig = card(["Tiempo de caída: t = √(h / 5)", "t en segundos, h en metros"], 130, 20)
        stem = f"El tiempo de caída de un objeto se modela con t = √(h/5), con h la altura en metros y t en segundos. ¿Cuántos segundos tarda en caer desde {h} m?"
        ans = f"{t} s"
        alts = [f"{h // 5} s", f"{t * 2} s", f"{h // 10} s", f"{t + 2} s", f"{h - 5} s"]
        ex = f"t = √({h}/5) = √{h // 5} = {t} s."
    elif kind == "period":
        Lg = r.choice([1, 4, 9, 16, 25, 36, 49])
        fig = card(["Período de un péndulo: T = 2√L", "L en metros, T en segundos"], 130, 20)
        stem = f"El período de un péndulo se aproxima con T = 2√L, con L su longitud en metros y T en segundos. ¿Cuál es el período de un péndulo de {Lg} m?"
        T = 2 * math.isqrt(Lg)
        ans = f"{T} s"
        alts = [f"{2 * Lg} s", f"{math.isqrt(Lg)} s", f"{T + 2} s", f"{Lg // 2 if Lg % 2 == 0 else Lg + 2} s", f"{T * 2} s"]
        ex = f"T = 2·√{Lg} = {T} s."
    else:
        v = r.choice([4, 6, 8, 10, 12, 15])
        d = v * v
        fig = card(["Velocidad de escape simplificada:", "v = √(2 · d)  (d en unidades convenidas)"], 130, 19)
        dd = d // 2
        stem = f"Una velocidad se modela con v = √(2d). Si d = {dd}, ¿cuál es el valor de v?"
        ans = f"{v}"
        alts = [f"{dd * 2}", f"{dd}", f"{v + 2}", f"{v * 2}", f"{dd // 2}"]
        ex = f"v = √(2·{dd}) = √{d} = {v}."
        if d % 2:
            raise Reject
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_tile(r, l):
    A = r.choice([36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 324, 400])
    s = math.isqrt(A)
    price = r.choice([300, 500, 800, 1200])
    kind = r.choice(["fence", "cost"])
    fig = card([f"Plaza cuadrada de {A} m²", "Se rodea con una reja" if kind == "fence" else "Se ponen baldosas de 1 m² a un precio dado"], 130, 20)
    if kind == "fence":
        stem = f"Una plaza cuadrada tiene {A} m² de superficie. ¿Cuántos metros de reja se necesitan para rodearla completamente?"
        ans = f"{4 * s} m"
        alts = [f"{s} m", f"{2 * s} m", f"{A} m", f"{4 * A} m", f"{s * s * 2} m"]
        ex = f"Lado = √{A} = {s} m; perímetro = 4·{s} = {4 * s} m."
    else:
        ans = f"${A * price:,}".replace(",", ".")
        stem = f"Un piso cuadrado de {A} m² se cubre con baldosas. Si el m² cuesta ${price:,}, ¿cuánto cuesta cubrirlo?".replace(",", ".")
        alts = [f"${s * price:,}".replace(",", "."), f"${4 * s * price:,}".replace(",", "."), f"${A * price + price:,}".replace(",", "."), f"${A + price:,}".replace(",", "."), f"${2 * A * price:,}".replace(",", ".")]
        ex = "El costo es el área por el precio del m²."
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_est_between(r, l):
    idx = 2 if l < 2 else r.choice([2, 3])
    n = r.choice([x for x in range(3, 90) if math.isqrt(x) ** 2 != x]) if idx == 2 else r.choice([x for x in range(9, 120) if round(x ** (1 / 3)) ** 3 != x])
    v = n ** (1 / idx)
    lo = math.floor(v)
    fig = numline(0, 10 if idx == 2 else 6, {"A": v}, step=1)
    ns = [n]
    for _ in range(50):
        m = r.randint(2, 99 if idx == 2 else 200)
        if abs(m ** (1 / idx) - v) > 0.9 and all(abs(m ** (1 / idx) - q ** (1 / idx)) > 0.9 for q in ns):
            ns.append(m)
        if len(ns) == 5:
            break
    if len(ns) < 5:
        raise Reject
    ans = rt(n, idx)
    al = [rt(m, idx) for m in ns[1:]]
    stem = f"En la recta numérica, el punto A representa a una {'raíz cuadrada' if idx == 2 else 'raíz cúbica'}. ¿Cuál de las siguientes raíces podría estar representada por A?"
    return make(stem, fig, ans, al, Q_REP, f"{ans} ≈ {v:.2f}, valor que se ubica cerca del punto A.".replace(".", ","))


def t_between_ints(r, l):
    idx = 2 if l < 2 else r.choice([2, 3])
    if idx == 2:
        n = r.choice([x for x in range(3, 200) if math.isqrt(x) ** 2 != x])
        lo = math.isqrt(n)
        rows = [[str(k * k) for k in range(max(1, lo - 2), lo + 3)]]
        heads = [f"{k}²" for k in range(max(1, lo - 2), lo + 3)]
    else:
        n = r.choice([x for x in range(9, 400) if round(x ** (1 / 3)) ** 3 != x])
        lo = int(n ** (1 / 3))
        heads = [f"{k}³" for k in range(max(1, lo - 2), lo + 3)]
        rows = [[str(k ** 3) for k in range(max(1, lo - 2), lo + 3)]]
    fig = viz.table_fig(heads, rows)
    ans = f"Entre {lo} y {lo + 1}"
    alts = [f"Entre {lo - 1} y {lo}", f"Entre {lo + 1} y {lo + 2}", f"Entre {lo // 2} y {lo // 2 + 1}", f"Entre {lo * 2} y {lo * 2 + 1}", f"Entre {n // idx} y {n // idx + 1}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(f"Usando la tabla, ¿entre cuáles números enteros consecutivos se encuentra {rt(n, idx)}?", fig, ans, al[:4], Q_REP, f"{lo ** idx} < {n} < {(lo + 1) ** idx}, luego {rt(n, idx)} está entre {lo} y {lo + 1}.")


def t_approx_tenth(r, l):
    n = r.choice([x for x in range(3, 120) if math.isqrt(x) ** 2 != x])
    v = math.sqrt(n)
    lo = round(v * 10) / 10
    xs = [round(lo - 0.1, 1), lo, round(lo + 0.1, 1)]
    if abs(v - lo) > 0.06:
        raise Reject
    rows = [[f"{x * x:.2f}".replace(".", ",") for x in xs]]
    heads = [f"{x}²".replace(".", ",") for x in xs]
    fig = viz.table_fig(heads, rows)
    stem = f"Usando la tabla, ¿cuál es el valor aproximado de √{n} con una cifra decimal?"
    ans = f"{lo}".replace(".", ",")
    alts = [f"{x}".replace(".", ",") for x in (round(lo - 0.1, 1), round(lo + 0.1, 1), round(lo + 0.2, 1), round(lo - 0.2, 1), round(n / 2, 1), round(lo * 2, 1))]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make(stem, fig, ans, al[:4], Q_REP, f"√{n} ≈ {ans}, el valor cuyo cuadrado más se acerca a {n}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b = r.choice([(9, 16), (4, 9), (16, 9), (25, 144), (36, 64)])
    if k == 0:
        return [f"√({a} + {b}) = √{a} + √{b} = {math.isqrt(a)} + {math.isqrt(b)}"], "Separó la raíz de una suma: √(a + b) no es igual a √a + √b", \
            ["Sumó los radicandos y luego sacó raíz a cada sumando por separado", "Multiplicó las raíces en lugar de sumarlas antes de calcular el resultado", "Elevó cada raíz al cuadrado antes de sumar los resultados obtenidos", "Restó los radicandos y aplicó la raíz al resultado en la operación final"]
    if k == 1:
        return [f"√(x²) = x  (con x = −5 resulta −5)"], "La raíz cuadrada entrega el valor no negativo: √(x²) = |x|, por lo que con x = −5 resulta 5", \
            ["La raíz cuadrada de un número negativo no existe en los números reales", "Elevar al cuadrado y sacar raíz son operaciones que siempre se anulan por completo", "El resultado de la raíz debe ser el opuesto de la base elevada al cuadrado", "Debió sacarse primero la raíz y después elevar el número al cuadrado"]
    if k == 2:
        return ["∛(−8) no existe porque el radicando es negativo"], "La raíz cúbica sí existe para negativos: ∛(−8) = −2, porque (−2)³ = −8", \
            ["La raíz cúbica de −8 es 2, pues el signo se pierde al elevar al cubo", "La raíz cúbica de −8 es −4, porque se divide el radicando por el índice", "La raíz cúbica de un negativo solo existe cuando el radicando es −1", "La raíz cúbica de −8 se define como el opuesto de la raíz cuadrada de 8"]
    if k == 3:
        return ["√16 = ±4"], "La expresión √16 representa solo la raíz positiva, 4; las soluciones de x² = 16 son ±4", \
            ["La raíz cuadrada de 16 es 8, porque se divide el radicando por el índice", "La raíz cuadrada de 16 es −4, pues la raíz principal siempre es negativa", "La raíz de 16 no es exacta, por lo que solo puede aproximarse con decimales", "La raíz cuadrada de 16 es 256, porque se eleva el radicando al cuadrado"]
    return ["√12 = 6"], "Dividió el radicando por 2 en lugar de descomponerlo: √12 = √(4·3) = 2√3", \
        ["Sacó raíz solo al 4 y dejó el 3 fuera de la raíz sin simplificar el resultado", "Multiplicó el radicando por 2 antes de sacar la raíz cuadrada del número", "Dividió el radicando por 3 y luego sacó la raíz cuadrada del resultado obtenido", "Sumó los factores 4 y 3 y sacó la raíz cuadrada de esa suma como resultado"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 120, 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


TRUE = ["√(a·b) = √a · √b para a y b no negativos", "La raíz cúbica de un número negativo existe en los números reales", "√2 es un número irracional", "Si a > 1, entonces √a es menor que a",
        "√(x²) = |x| para todo número real x", "La raíz cuadrada de un número no negativo es siempre no negativa"]
FALSE = ["√(a + b) = √a + √b para a y b positivos", "La raíz cuadrada de un número negativo es un número real negativo", "√16 = ±4", "Si 0 < a < 1, entonces √a es menor que a",
         "Toda raíz cuadrada de un entero positivo es un número racional", "∛(−27) no existe en los números reales"]


def _fig(r):
    return card(["Raíces", "√a · √b = √(ab)   ·   ∛(−8) = −2"], 130, 20)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre raíces es verdadera?", "Sobre raíces cuadradas y cúbicas, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de las raíces.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre raíces es falsa?", "Sobre raíces cuadradas y cúbicas, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las raíces.")


BY_SKILL = {
    Q_RES: [t_root_eval, t_root_mul],
    Q_MOD: [t_square_side, t_formula_root, t_tile],
    Q_REP: [t_est_between, t_between_ints, t_approx_tenth],
    Q_ARG: [t_error, t_true, t_false],
}
