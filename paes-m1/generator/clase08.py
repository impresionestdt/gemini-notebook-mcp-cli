"""Clase 8 (M1) · Potencias de base racional y exponente entero."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
import viz

SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def sup(n):
    return str(n).translate(SUP)


def bs(b):
    b = F(b)
    if b.denominator != 1:
        return f"({b.numerator}/{b.denominator})" if b > 0 else f"(−{abs(b.numerator)}/{b.denominator})"
    return f"({fs(b)})" if b < 0 else str(b)


def pw(b, n):
    return f"{bs(b)}{sup(n)}"


def val(b, n):
    b = F(b)
    return b ** n


def uq(ans, alts, fmt=None):
    fmt = fmt or (lambda v: fs(F(v)))
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        try:
            s = fmt(a)
        except (ZeroDivisionError, ValueError):
            continue
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def sf(fn):
    try:
        return fn()
    except (ZeroDivisionError, ValueError, OverflowError):
        return None


# ---------------------------------------------------------------- Resolver problemas
def t_pow_eval(r, l):
    if l == 0:
        b = r.choice([2, 3, 5, 10, -2, -3, F(1, 2), F(1, 3)])
        n = r.choice([-3, -2, -1, 0, 2, 3, 4] if abs(F(b)) >= 2 or F(b) < 0 else [-3, -2, -1, 2, 3])
        v = val(b, n)
        alts = [val(b, -n) if b != 0 else None, F(b) * n, -abs(v) if v > 0 else abs(v), F(b) ** abs(n) if n < 0 else F(b) * abs(n), 1 / (F(b) * n) if n and b else None, v * 2]
        expr = pw(b, n)
        ex = f"{expr} = {fs(v)} (exponente negativo: se invierte la base)."
    elif l == 1:
        a, c = r.choice([(2, 3), (3, 2), (2, 5), (3, 4), (4, 3), (5, 2)])
        n = r.choice([-1, -2, -3, 2, 3])
        b = F(a, c)
        v = val(b, n)
        expr = pw(b, n)
        alts = [val(F(a, c), -n), F(a * n, c), F(a ** abs(n), c), F(a, c ** abs(n)), F(c, a) * n if a else None, val(F(c, a), n) * -1]
        ex = f"{expr} = {fs(v)}."
    else:
        a, b2 = r.choice([(2, 3), (2, 2), (3, 2), (4, 2), (5, 1)])
        n1, n2 = r.choice([(-1, -2), (-2, -1), (-1, 0), (-2, -3)])
        v = F(a) ** n1 + F(b2 + 1) ** n2
        expr = f"{a}{sup(n1)} + {b2 + 1}{sup(n2)}"
        alts = [F(a) ** (n1 + n2), F(a + b2 + 1) ** (n1 + n2), F(1, a + b2 + 1) if a + b2 + 1 else None, F(1, a * abs(n1) + (b2 + 1) * abs(n2)), -(F(a) ** abs(n1)) - (F(b2 + 1) ** abs(n2))]
        ex = f"{expr} = {fs(F(a) ** n1)} + {fs(F(b2 + 1) ** n2)} = {fs(v)}."
    if abs(v) > 5000 or abs(v) < F(1, 5000):
        raise Reject
    ans = fs(v)
    fig = card(["Calcula:", expr], 130, 26)
    return make("¿Cuál es el valor de la expresión de la figura?", fig, ans, pick4(ans, uq(ans, alts)), Q_RES, ex)


def t_pow_props(r, l):
    b = r.choice([2, 3, 5, 7, 10, F(1, 2), F(2, 3)])
    kind = r.choice(["mul", "div", "pow", "mix"] if l else ["mul", "div", "pow"])
    m, n, p = r.randint(-4, 6), r.randint(-4, 6), r.randint(-3, 5)
    if kind == "mul":
        e = m + n
        expr = f"{pw(b, m)} · {pw(b, n)}"
        alts = [m * n, m - n, e + 1, e - 1, -e]
    elif kind == "div":
        e = m - n
        expr = f"{pw(b, m)} : {pw(b, n)}"
        alts = [m + n, m * n, n - m, e + 1, e - 1]
    elif kind == "pow":
        e = m * n
        expr = f"({pw(b, m)}){sup(n)}"
        alts = [m + n, m ** 2 + n if False else m - n, -e, e + m, e + 1]
    else:
        e = m + n - p
        expr = f"{pw(b, m)} · {pw(b, n)} : {pw(b, p)}"
        alts = [m + n + p, (m + n) * p, m * n - p, e + 1, -e]
    if e == 0 or abs(e) > 12 or len({m, n}) == 1 and kind != "mul":
        raise Reject
    ans = pw(b, e)
    al = [pw(b, a) for a in alts]
    al = [x for x in dict.fromkeys(al) if x != ans]
    fig = card(["Simplifica y escribe como una sola potencia:", expr], 130, 21)
    return make("¿Cuál es el resultado de simplificar la expresión de la figura?", fig, ans, al[:4], Q_RES, f"Se aplican las propiedades de potencias de igual base: el exponente resultante es {e}.")


def t_sci(r, l):
    kind = r.choice(["to", "from", "mul"] if l else ["to", "from"])
    if kind == "to":
        mant = r.choice([1.2, 2.5, 3.4, 4.5, 6.02, 7.8, 9.1, 1.6, 3.75])
        e = r.choice([-6, -5, -4, -3, 3, 4, 5, 6, 7, 8])
        x = F(str(mant)) * F(10) ** e
        from num import dstr
        xs = dstr(x) if e < 0 else f"{int(x):,}".replace(",", ".")
        ms = str(mant).replace(".", ",")
        ans = f"{ms} · 10{sup(e)}"
        alts = [f"{ms} · 10{sup(-e)}", f"{ms} · 10{sup(e + 1)}", f"{ms} · 10{sup(e - 1)}", f"{str(mant * 10).replace('.', ',').rstrip('0').rstrip(',')} · 10{sup(e - 1)}", f"0,{str(mant).replace('.', '')} · 10{sup(e)}"]
        al = [x for x in dict.fromkeys(alts) if x != ans]
        fig = card(["Número:", xs], 120, 26)
        return make("¿Cuál es la notación científica del número de la figura?", fig, ans, al[:4], Q_RES, f"Se corre la coma hasta dejar una cifra entera distinta de cero: {ans}.")
    if kind == "from":
        mant = r.choice([2, 3, 4, 5, 6, 7, 8, 1.5, 2.5, 3.2, 4.8])
        e = r.choice([-5, -4, -3, -2, 3, 4, 5, 6])
        from num import dstr
        x = F(str(mant)) * F(10) ** e
        xs = dstr(x) if e < 0 else f"{int(x):,}".replace(",", ".")
        ms = str(mant).replace(".", ",")
        ans = xs
        alts = []
        for d in (-2, -1, 1, 2):
            y = F(str(mant)) * F(10) ** (e + d)
            alts.append(dstr(y) if e + d < 0 else f"{int(y):,}".replace(",", "."))
        fig = card(["Notación científica:", f"{ms} · 10{sup(e)}"], 130, 24)
        al = [x_ for x_ in dict.fromkeys(alts) if x_ != ans]
        return make("¿Cuál es el valor del número de la figura escrito en forma decimal?", fig, ans, al[:4], Q_RES, f"El exponente {e} indica correr la coma {abs(e)} lugares {'a la derecha' if e > 0 else 'a la izquierda'}.")
    a, b = r.choice([(2, 3), (3, 2), (4, 2), (5, 4), (6, 5), (1.5, 4)])
    e1, e2 = r.choice([(3, 4), (5, -2), (-3, 6), (4, 4), (7, -3), (-2, -3)])
    prod = F(str(a)) * F(str(b))
    ee = e1 + e2
    if prod >= 10:
        prod /= 10
        ee += 1
    sm = lambda p_: (f"{float(p_):.3f}".rstrip("0").rstrip(".")).replace(".", ",")
    ans = f"{sm(prod)} · 10{sup(ee)}"
    alts = [f"{sm(prod)} · 10{sup(e1 * e2)}", f"{sm(F(str(a)) + F(str(b)))} · 10{sup(ee)}", f"{sm(prod)} · 10{sup(ee + 1)}", f"{sm(prod)} · 10{sup(ee - 1)}", f"{sm(prod)} · 10{sup(abs(e1) + abs(e2))}"]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    fig = card(["Calcula:", f"({str(a).replace('.', ',')} · 10{sup(e1)}) · ({str(b).replace('.', ',')} · 10{sup(e2)})"], 130, 22)
    return make("¿Cuál es el resultado de la multiplicación, en notación científica?", fig, ans, al[:4], Q_RES, "Se multiplican las mantisas y se suman los exponentes de 10 (ajustando si la mantisa llega a 10 o más).")


# ---------------------------------------------------------------- Modelar
def t_growth(r, l):
    N0 = r.choice([1, 2, 3, 5, 10, 100, 500])
    base = r.choice([2, 3] if l < 2 else [2, F(1, 2), 3])
    t = r.choice([2, 3, 4, 5, 6] if l < 2 else [3, 4, 5])
    per = r.choice(["hora", "día", "minuto"])
    if base == F(1, 2):
        stem = f"Una sustancia de {N0 * 2 ** t} gramos reduce su masa a la mitad cada {per}. ¿Cuántos gramos quedan después de {t} {per}s?"
        v = F(N0 * 2 ** t) * F(1, 2) ** t
        alts = [N0 * 2 ** t - t, N0 * 2 ** t * t / 2, N0 * 2 ** t / 2, N0 * 2 ** t - N0, N0 * 2 ** (t + 1)]
        fig = card([f"Masa inicial: {N0 * 2 ** t} g", f"Se reduce a la mitad cada {per}"], 130, 20)
        ex = f"Masa = {N0 * 2 ** t}·(1/2)^{t} = {fs(v)} g."
        unit = " g"
    else:
        name = {2: "duplica", 3: "triplica"}[base]
        stem = f"Un cultivo de {N0} bacterias se {name} cada {per}. ¿Cuántas bacterias habrá después de {t} {per}s?"
        v = F(N0 * base ** t)
        alts = [N0 * base * t, N0 + base * t, N0 * t ** base, N0 * base ** (t + 1), N0 * base ** (t - 1)]
        fig = viz.table_fig(["Tiempo", "0", "1", "2", "…"], [["Bacterias", str(N0), str(N0 * base), str(N0 * base * base), "?"]]) if t > 2 else card([f"Población inicial: {N0}", f"Se {name} cada {per}"], 130, 20)
        ex = f"Población = {N0}·{base}^{t} = {fs(v)}."
        unit = ""
    ans = fs(v) + unit
    al = uq(ans, alts, lambda a: fs(F(a)) + unit)
    return make(stem, fig, ans, al[:4], Q_MOD, ex)


def t_light(r, l):
    d, v_ = r.choice([(1.5e8, 3e5), (3e8, 3e5), (9e6, 3e5), (6e5, 3e5), (3.6e9, 3e5), (4.5e7, 3e5)]) if False else (None, None)
    dm, ee = r.choice([(1.5, 8), (3, 8), (6, 6), (9, 6), (3.6, 9), (4.5, 7), (1.2, 8), (7.5, 7)])
    vm, ve = 3, 5
    t = F(str(dm)) / vm * F(10) ** (ee - ve)
    if t.denominator != 1 or t > 100000:
        raise Reject
    dstr_ = str(dm).replace(".", ",")
    fig = card([f"Distancia: {dstr_} · 10{sup(ee)} km", f"Rapidez de la luz: 3 · 10{sup(ve)} km/s"], 130, 20)
    stem = "Una señal viaja a la rapidez de la luz. ¿Cuántos segundos demora en recorrer la distancia indicada?"
    ans = f"{int(t):,}".replace(",", ".") + " s"
    alts = [t * 10, t / 10 if (t / 10).denominator == 1 else t + 10, t * 100, F(3 * vm, 1) * 100, t + 100]
    al = [f"{int(a):,}".replace(",", ".") + " s" for a in alts if F(a).denominator == 1 and a > 0 and a != t]
    return make(stem, fig, ans, list(dict.fromkeys(al))[:4], Q_MOD, f"Tiempo = distancia : rapidez = {int(t)} s.")


def t_area_vol(r, l):
    b = r.choice([2, 3, 5])
    k = r.choice([2, 3, 4])
    kind = r.choice(["area", "vol"])
    side = f"{b}{sup(k)} cm"
    if kind == "area":
        stem = f"Un cuadrado tiene lados de {side}. ¿Qué expresión representa su área?"
        ans = f"{b}{sup(2 * k)} cm²"
        alts = [f"{b}{sup(k + 2)} cm²", f"{b}{sup(k * k)} cm²", f"{b * 2}{sup(k)} cm²", f"{b}{sup(k)} cm²"]
        alts = [x for x in alts if x != ans]
        ex = f"Área = ({b}{sup(k)})² = {b}{sup(2 * k)}."
    else:
        stem = f"Un cubo tiene aristas de {side}. ¿Qué expresión representa su volumen?"
        ans = f"{b}{sup(3 * k)} cm³"
        alts = [f"{b}{sup(k + 3)} cm³", f"{b}{sup(k ** 3)} cm³", f"{b * 3}{sup(k)} cm³", f"{b}{sup(2 * k)} cm³"]
        alts = [x for x in alts if x != ans]
        ex = f"Volumen = ({b}{sup(k)})³ = {b}{sup(3 * k)}."
    body = R(200, 30, 120, 120, FILL) + tag(260, 165, side, 17)
    fig = wrap(560, 200, body, "Figura con la medida del lado")
    if len(set(alts)) < 4:
        raise Reject
    return make(stem, fig, ans, alts[:4], Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_repeated(r, l):
    b = r.choice([2, 3, 5, 7, F(1, 2), F(2, 3), -2, -3])
    n = r.choice([3, 4, 5])
    neg = l > 0 and r.random() < 0.6
    facs = " · ".join([bs(b)] * n)
    if neg:
        disp = f"1 : ({facs})" if False else f"1 / ({facs})"
        e = -n
        ans_b, ans_e = b, e
    else:
        disp = facs
        ans_b, ans_e = b, n
    fig = card(["Expresión:", disp], 130, 22)
    ans = pw(ans_b, ans_e)
    alts = [pw(ans_b, -ans_e), f"{bs(ans_b)} · {abs(ans_e)}".replace("· ", "· "), pw(-F(ans_b) if F(ans_b) != 0 else 1, ans_e), pw(ans_b, ans_e + 1), pw(ans_b, ans_e - 1) if ans_e - 1 != 0 else pw(ans_b, 2)]
    al = [x for x in dict.fromkeys(alts) if x != ans]
    return make("¿Cuál de las siguientes potencias representa la expresión de la figura?", fig, ans, al[:4], Q_REP, "Un producto de n factores iguales es la potencia con exponente n; en el denominador el exponente es negativo.")


def t_pow_table(r, l):
    b = r.choice([2, 3, 5, 10])
    ns = [-3, -2, -1, 0, 1, 2, 3][:7 if l else 6]
    hide = r.choice([i for i, n_ in enumerate(ns) if n_ != 0])
    row = [fs(F(b) ** n_) if i != hide else "?" for i, n_ in enumerate(ns)]
    fig = viz.table_fig([f"{b}ⁿ"] + [str(n_).replace("-", "−") for n_ in ns], [["Valor"] + row])
    v = F(b) ** ns[hide]
    stem = f"La tabla muestra potencias de {b} con distintos exponentes n. ¿Qué valor corresponde a «?»"
    ans = fs(v)
    alts = [F(b) ** abs(ns[hide]), F(1, b * abs(ns[hide])) if ns[hide] < 0 else F(b * ns[hide]), -v, F(b) ** ns[hide] * b, F(b) ** ns[hide] / b]
    return make(stem, fig, ans, pick4(ans, uq(ans, alts)), Q_REP, f"{b}^{ns[hide]} = {ans}.")


def t_sci_place(r, l):
    from num import dstr
    mant = r.choice([1.5, 2.4, 3.6, 4.5, 5.2, 6.8, 7.3, 8.1, 9.6])
    e = r.choice([-5, -4, -3, -2, 3, 4, 5, 6])
    x = F(str(mant)) * F(10) ** e
    xs = dstr(x) if e < 0 else f"{int(x):,}".replace(",", ".")
    ms = str(mant).replace(".", ",")
    fig = card([f"Número: {xs}", f"La coma se corre {abs(e)} lugares hasta {ms}"], 130, 20)
    ans = f"{ms} · 10{sup(e)}"
    alts = [f"{ms} · 10{sup(-e)}", f"{ms} · 10{sup(e + 1)}", f"{ms} · 10{sup(e - 1)}", f"{ms} · 10{sup(abs(e) + 1)}", f"{ms} · {abs(e)}{sup(10)}"]
    al = [x_ for x_ in dict.fromkeys(alts) if x_ != ans]
    return make("A partir de la figura, ¿cómo se escribe el número en notación científica?", fig, ans, al[:4], Q_REP, "Correr la coma a la izquierda da exponente positivo; correrla a la derecha da exponente negativo.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(6)
    a, b, c = r.sample(range(2, 6), 3)
    if k == 0:
        return [f"{a}³ + {a}⁴ = {a}⁷"], "Sumó los exponentes: esa propiedad vale para el producto de potencias, no para la suma", \
            ["Multiplicó las bases y sumó los exponentes de ambas potencias", "Sumó las bases y conservó el exponente más grande de los dos", "Restó los exponentes porque las bases de ambas potencias son iguales", "Elevó la suma de las bases al producto de los exponentes"]
    if k == 1:
        return [f"({a} + {b})² = {a}² + {b}²"], "Distribuyó el exponente sobre la suma: (a + b)² incluye además el doble producto 2ab", \
            ["Multiplicó la suma de las bases por el exponente sin elevarla al cuadrado", "Elevó al cuadrado solo la primera base y dejó la segunda sin elevar", "Restó los cuadrados en lugar de sumarlos al desarrollar el binomio", "Sumó las bases y luego duplicó el resultado en lugar de elevarlo"]
    if k == 2:
        return [f"{a}³ · {b}³ = {a * b}⁶"], "Sumó los exponentes con bases distintas: con igual exponente se multiplican las bases y se conserva el exponente", \
            ["Multiplicó las bases y también multiplicó los exponentes entre sí", "Sumó las bases y conservó el exponente común de las dos potencias", "Elevó la primera base al exponente de la segunda potencia solamente", "Dividió las bases y sumó los exponentes de las potencias dadas"]
    if k == 3:
        return [f"({a}²)³ = {a}⁵"], "Sumó los exponentes: en una potencia de potencia los exponentes se multiplican, resultando 6", \
            ["Multiplicó la base por los dos exponentes de la potencia de potencia", "Elevó la base al cuadrado y luego le sumó el exponente exterior", "Restó los exponentes porque una potencia está dentro de la otra", "Sumó los exponentes y multiplicó por la base al terminar el cálculo"]
    if k == 4:
        return [f"{a}⁻² = −{a * a}"], "Interpretó el exponente negativo como signo negativo: significa inverso, 1/a², que es positivo", \
            [f"Calculó {a}⁻² como {a}·(−2) = −{2 * a} al multiplicar la base por el exponente", "Invirtió la base pero olvidó elevarla al cuadrado al final del proceso", "Elevó al cuadrado el inverso y luego lo multiplicó por menos uno", "Restó el exponente a la base en lugar de invertir la potencia entera"]
    return [f"{a}⁰ = 0"], "Confundió el exponente cero con multiplicar por cero: toda base distinta de cero elevada a 0 vale 1", \
        ["Interpretó el exponente cero como que la potencia no existe en los reales", "Restó el exponente a la base y obtuvo la base como resultado final", "Dividió la base por sí misma y luego la multiplicó por el exponente", "Consideró que la potencia vale la base cuando el exponente es cero"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + lines, 120, 22)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equal(r, l):
    b = r.choice([2, 3, 5, 10])
    n = r.choice([2, 3, 4])
    good = [f"1/{b ** n}", f"({fs(F(1, b))}){sup(n)}", f"1/{b}{sup(n)}", f"{b}{sup(-n)}".replace("−", "⁻") if False else f"{b}{sup(-n)}", fs(F(1, b ** n))]
    good = [g for g in dict.fromkeys(good)]
    bad = r.choice([f"−{b ** n}", f"{b}{sup(n)}", f"−1/{b ** n}", f"1/{b * n}", f"{fs(F(-n, b))}"])
    fig = card([f"Potencia base: {b}{sup(-n)}"], 110, 26)
    stem = f"La expresión {b}{sup(-n)} se compara con otras. ¿Cuál de las siguientes NO es equivalente a {b}{sup(-n)}?"
    al = [x for x in good if x != bad][:4]
    if len(al) < 4 or bad in good:
        raise Reject
    return make(stem, fig, bad, al, Q_ARG, f"{b}{sup(-n)} = 1/{b}{sup(n)} = {fs(F(1, b ** n))}.")


TRUE = ["Toda base distinta de cero elevada a 0 es igual a 1", "a⁻ⁿ es el inverso multiplicativo de aⁿ, con a distinto de cero", "Al multiplicar potencias de igual base se suman los exponentes",
        "Una potencia de exponente par y base negativa es positiva", "(a·b)ⁿ es igual a aⁿ·bⁿ", "En una potencia de potencia, los exponentes se multiplican"]
FALSE = ["Al sumar potencias de igual base se suman los exponentes", "(a + b)² es siempre igual a a² + b²", "Una potencia de base negativa y exponente impar es positiva",
         "a⁻ⁿ es siempre un número negativo si a es positivo", "Toda base elevada a 0 es igual a 0", "En una potencia de potencia, los exponentes se suman"]


def _fig(r):
    return card(["Propiedades de las potencias", "aᵐ · aⁿ = aᵐ⁺ⁿ  ·  (aᵐ)ⁿ = aᵐⁿ"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre potencias es verdadera?", "Sobre las propiedades de las potencias, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de las potencias.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre potencias es falsa?", "Sobre las propiedades de las potencias, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las potencias.")


BY_SKILL = {
    Q_RES: [t_pow_eval, t_pow_props, t_sci],
    Q_MOD: [t_growth, t_light, t_area_vol],
    Q_REP: [t_repeated, t_pow_table, t_sci_place],
    Q_ARG: [t_error, t_not_equal, t_true, t_false],
}
