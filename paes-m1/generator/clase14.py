"""Clase 14 (M1) · Operatoria algebraica y reducción de términos semejantes."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
import viz

ORDER = ["x²", "x", "y", ""]


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def pstr(p):
    """Polinomio {término: coef} como texto ordenado."""
    out = ""
    for k in ORDER:
        c = p.get(k, 0)
        if not c:
            continue
        a = abs(c)
        body = (str(a) if (a != 1 or not k) else "") + k
        out += (("−" if c < 0 else "") + body) if not out else ((" − " if c < 0 else " + ") + body)
    return out or "0"


def padd(p, q, m=1):
    out = dict(p)
    for k, v in q.items():
        out[k] = out.get(k, 0) + m * v
    return {k: v for k, v in out.items() if v}


def pscale(p, m):
    return {k: v * m for k, v in p.items() if v * m}


def rand_poly(r, keys, lo=-6, hi=8):
    p = {}
    for k in keys:
        c = r.randint(lo, hi)
        if c:
            p[k] = c
    if not p:
        p[keys[0]] = r.choice([1, 2, 3])
    return p


def shown(p, first_paren=False):
    return pstr(p)


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = a if isinstance(a, str) else pstr(a)
        if s not in seen and s != "0":
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver problemas
def t_reduce(r, l):
    if l == 0:
        keys = ["x", "y"]
        terms = [(rr(r, -8, 9), r.choice(keys)) for _ in range(4)]
        disp = ""
        tot = {}
        for c, k in terms:
            a = abs(c)
            body = (str(a) if a != 1 else "") + k
            disp += (("−" if c < 0 else "") + body) if not disp else ((" − " if c < 0 else " + ") + body)
            tot[k] = tot.get(k, 0) + c
        tot = {k: v for k, v in tot.items() if v}
        wrong = [{k: abs(v) for k, v in tot.items()}, {"x²": sum(c for c, k in terms if k == "x"), **({"y": sum(c for c, k in terms if k == "y")})}, dict(tot, y=tot.get("y", 0) + 1), {"x": sum(c for c, k in terms)}]
    else:
        keys = ["x²", "x", ""] if l == 1 else ["x", "y", ""]
        A, B = rand_poly(r, keys), rand_poly(r, keys)
        m = r.choice([2, 3, -1, -2])
        C = rand_poly(r, keys, -4, 5)
        tot = padd(padd(A, B, -1), C, m) if l == 2 else padd(A, B, -1)
        disp = f"({pstr(A)}) − ({pstr(B)})" + (f" + {m}({pstr(C)})" if m > 0 and l == 2 else (f" − {abs(m)}({pstr(C)})" if l == 2 else ""))
        Bw = dict(B)
        first = next(iter(B))
        wrong1 = dict(A)
        for k, v in B.items():
            wrong1[k] = wrong1.get(k, 0) + (-v if k == first else v)
        wrong = [padd(padd(A, B, 1), C, m) if l == 2 else padd(A, B, 1), {k: v for k, v in wrong1.items() if v}, dict(tot, **{ORDER[0] if l == 1 else "": tot.get("", 0) + 2}), {k: -v for k, v in tot.items()}]
        if l == 2:
            wrong[1] = padd(padd({k: v for k, v in wrong1.items() if v}, C, 1), {}, 1)
    if not tot or len(disp) > 60:
        raise Reject
    ans = pstr(tot)
    fig = card(["Reduce la expresión:", disp], 130, 21)
    al = uq(ans, wrong + [padd(tot, {"": 1}), padd(tot, {"x": 2}) if "x" in tot or True else tot])
    return make("¿Cuál es la forma reducida de la expresión de la figura?", fig, ans, al[:4], Q_RES, "Se eliminan paréntesis cuidando los signos (menos delante cambia todos los signos) y se suman los términos semejantes.")


def t_monomial(r, l):
    a, b = rr(r, -6, 7), rr(r, -5, 6)
    m, n = r.randint(1, 4), r.randint(1, 4)
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def mono(c, e):
        cs = "" if abs(c) == 1 else str(abs(c))
        es = "" if e == 1 else str(e).translate(sup)
        return ("−" if c < 0 else "") + cs + "x" + es
    kind = r.choice(["mul", "div", "pow"] if l else ["mul", "div"])
    if kind == "mul":
        c, e = a * b, m + n
        disp = f"({mono(a, m)}) · ({mono(b, n)})"
        wrong = [(a + b, m + n), (a * b, m * n), (a * b, e + 1), (-c, e), (a * b, abs(m - n) or 1)]
    elif kind == "div":
        c0 = a * b
        disp = f"({mono(c0, m + n)}) : ({mono(b, n)})"
        c, e = a, m
        wrong = [(a, m + n), (c0 // 1 - b, m), (a, m * n), (-a, m), (a, m + 1)]
    else:
        c, e = a ** 2 if abs(a) < 5 else abs(a), 2 * m
        disp = f"({mono(a, m)})²"
        c = a * a
        wrong = [(2 * a, 2 * m), (a * a, m), (a, 2 * m), (-a * a, 2 * m), (a * a, m + 2)]
    if e == 0 or abs(c) > 400:
        raise Reject
    ans = mono(c, e)
    al = list(dict.fromkeys(mono(cc, ee) for cc, ee in wrong if cc and ee > 0))
    al = [x for x in al if x != ans]
    fig = card(["Calcula:", disp], 130, 22)
    return make("¿Cuál es el resultado de la operación entre monomios de la figura?", fig, ans, al[:4], Q_RES, "Se operan los coeficientes por separado y los exponentes según la propiedad de potencias.")


# ---------------------------------------------------------------- Modelar
def t_perimeter(r, l):
    a, b, c = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
    p1, p2, p3 = r.randint(-3, 6), r.randint(-3, 6), r.randint(-3, 6)
    s1, s2, s3 = {"x": a, "": p1}, {"x": b, "": p2}, {"x": c, "": p3}
    tot = padd(padd(s1, s2), s3)
    body = P([(120, 160), (440, 160), (250, 30)], FILL) + tag(280, 178, pstr(s1), 16) + tag(370, 90, pstr(s2), 16) + tag(170, 90, pstr(s3), 16)
    fig = wrap(560, 200, body, "Triángulo con lados expresados algebraicamente")
    ans = pstr(tot)
    wrong = [padd(padd(s1, s2), s3, 0) if False else {"x": a + b + c, "": abs(p1) + abs(p2) + abs(p3)}, {"x": a * b * c, "": p1 + p2 + p3}, padd(tot, {"": 2}), padd(tot, {"x": 1}), {"x": a + b + c}]
    stem = "Los lados de un triángulo miden las expresiones de la figura. ¿Cuál es su perímetro?"
    al = uq(ans, wrong)
    if not tot:
        raise Reject
    return make(stem, fig, ans, al[:4], Q_MOD, "Perímetro = suma de los tres lados; se reducen los términos semejantes.")


def t_savings(r, l):
    a, b = rr(r, 1, 5), rr(r, -6, 8)
    c, d = rr(r, 1, 5), rr(r, -6, 8)
    A, B = {"x": a, "": b}, {"x": c, "": d}
    who = r.choice([("Ana", "Luis"), ("Marta", "Pedro"), ("Sofía", "Diego")])
    kind = r.choice(["sum", "diff"])
    tot = padd(A, B) if kind == "sum" else padd(A, B, -1)
    stem = f"{who[0]} tiene {pstr(A)} pesos y {who[1]} tiene {pstr(B)} pesos, con x un valor en pesos. ¿Qué expresión representa {'lo que tienen entre los dos' if kind == 'sum' else f'cuánto más tiene {who[0]} que {who[1]}'}?"
    ans = pstr(tot)
    wrong = [padd(A, B, -1 if kind == "sum" else 1), padd(A, {"x": -c, "": d}, 1) if kind != "sum" else {"x": a + c}, padd(tot, {"": 2}), {"x": tot.get("x", 0), "": tot.get("", 0) * -1}, {"x": a * c, "": b * d}]
    fig = card([f"{who[0]}: {pstr(A)}", f"{who[1]}: {pstr(B)}"], 130, 21)
    al = uq(ans, wrong)
    if not tot:
        raise Reject
    return make(stem, fig, ans, al[:4], Q_MOD, "Se suman o restan las expresiones término a término (si se resta, cambia el signo de todo el segundo paréntesis).")


def t_pack(r, l):
    p, q = r.randint(2, 6), r.randint(2, 6)
    a, b = r.randint(2, 5), r.randint(1, 4)
    fig = card([f"Caja de tipo A: {p}x lápices", f"Caja de tipo B: {q} lápices", f"Se compran {a} cajas A y {b} cajas B"], 170, 19)
    stem = f"Una caja de tipo A tiene {p}x lápices y una de tipo B tiene {q}. Se compran {a} cajas de tipo A y {b} cajas de tipo B. ¿Qué expresión representa el total de lápices?"
    ans = f"{a * p}x + {b * q}"
    wrong = [f"{p * a + q * b}x", f"{p}x + {q} + {a + b}", f"{a + p}x + {b + q}", f"{a * p}x·{b * q}", f"{p * a}x + {q + b}"]
    al = [w for w in dict.fromkeys(wrong) if w != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"Total = {a}·({p}x) + {b}·{q} = {a * p}x + {b * q}.")


# ---------------------------------------------------------------- Representar
def tiles_fig(cnt, w=560):
    """cnt: {'x²': n, 'x': n, '': n} (n con signo). Baldosas: x² (cuadrado), x (barra), 1 (unidad); negativas en otro color."""
    body = ""
    x = 30
    y0 = 30
    spec = (("x²", (54, 54), 62, 62, 3), ("x", (54, 22), 62, 30, 3), ("", (24, 24), 30, 30, 3))
    for k, size, dx, dy, per in spec:
        n = cnt.get(k, 0)
        if not n:
            continue
        for i in range(abs(n)):
            fill = FILL3 if n > 0 else FILL2
            lab = ("−" if n < 0 else "") + (k or "1")
            px, py = x + (i % per) * dx, y0 + (i // per) * dy
            body += R(px, py, size[0], size[1], fill, NAVY, 2.5) + T(px + size[0] / 2, py + size[1] / 2 + 6, lab, 16 if k != "" else 13)
        x += per * dx + 30
    return wrap(w, 190, body, "Baldosas algebraicas: cuadrados x², barras x y unidades")


def t_tiles(r, l):
    cnt = {"x²": rr(r, -2, 3), "x": rr(r, -3, 4), "": rr(r, -4, 5)}
    if l == 0:
        cnt.pop("x²")
    fig = tiles_fig(cnt)
    ans = pstr(cnt)
    wrong = [{k: abs(v) for k, v in cnt.items()}, {k: -v for k, v in cnt.items()}, dict(cnt, **{"": cnt.get("", 0) + 1}), {"x²": cnt.get("x", 0), "x": cnt.get("x²", 0), "": cnt.get("", 0)} if l else {"x": cnt.get("", 0), "": cnt.get("x", 0)}, {"x": sum(cnt.values())}]
    al = uq(ans, wrong)
    stem = "Las baldosas de la figura representan una expresión algebraica: las azules son positivas y las naranjas negativas. ¿Cuál es la expresión?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se cuenta cada tipo de baldosa con su signo: cuadrados x², barras x y unidades.")


def t_tiles_sum(r, l):
    A = {"x": rr(r, -3, 3), "": rr(r, -3, 4)}
    B = {"x": rr(r, -3, 3), "": rr(r, -3, 4)}
    body = tag(140, 20, "Grupo 1", 15) + tag(420, 20, "Grupo 2", 15)
    for gx, cnt in ((30, A), (300, B)):
        x = gx
        for k, size in (("x", (66, 26)), ("", (26, 26))):
            n = cnt.get(k, 0)
            for i in range(abs(n)):
                fill = FILL3 if n > 0 else FILL2
                lab = ("−" if n < 0 else "") + (k or "1")
                if k == "x":
                    px, py = x, 50 + i * 34
                else:
                    px, py = x + 90 + (i % 4) * 34, 50 + (i // 4) * 34
                body += R(px, py, size[0], size[1], fill, NAVY, 2.5) + T(px + size[0] / 2, py + size[1] / 2 + 6, lab, 15)
    fig = wrap(560, 190, body, "Dos grupos de baldosas")
    tot = padd(A, B)
    if not tot:
        raise Reject
    ans = pstr(tot)
    wrong = [padd(A, B, -1), {"x": abs(A.get("x", 0)) + abs(B.get("x", 0)), "": abs(A.get("", 0)) + abs(B.get("", 0))}, padd(tot, {"": 1}), {"x": A.get("x", 0) + A.get("", 0) + B.get("x", 0) + B.get("", 0)}, padd(tot, {"x": 1})]
    al = uq(ans, wrong)
    stem = "Los dos grupos de baldosas representan expresiones (azules positivas, naranjas negativas). ¿Cuál es la suma de ambas expresiones?"
    return make(stem, fig, ans, al[:4], Q_REP, "Se suman los coeficientes de x y las unidades de los dos grupos.")


def t_equiv_forms(r, l):
    a, b = rr(r, 2, 5), rr(r, 1, 6)
    c, d = rr(r, 1, 4), rr(r, -5, 5)
    A = {"x": a, "": b}
    expr = f"{a}(x + {b}) + {c}x" if False else f"({pstr(A)}) + ({pstr({'x': c, '': d})})"
    tot = padd(A, {"x": c, "": d})
    fig = card(["Expresión:", expr], 130, 22)
    ans = pstr(tot)
    wrong = [padd(A, {"x": c, "": d}, -1), padd(tot, {"": 1}), padd(tot, {"x": -1}), {"x": a * c, "": b * d} if d else {"x": a * c}, {"x": a + c}]
    al = uq(ans, wrong)
    return make("¿Cuál de las siguientes expresiones es equivalente a la expresión de la figura?", fig, ans, al[:4], Q_REP, "Al quitar los paréntesis precedidos por + no cambian los signos; luego se reducen los términos semejantes.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(5)
    a, b, c = r.sample(range(2, 8), 3)
    if k == 0:
        return [f"{a}x − ({b}x − {c}) = {a}x − {b}x − {c}"], f"No cambió el signo de {c}: al restar un paréntesis cambian los signos de todos sus términos", \
            ["Cambió el signo solo del segundo término del paréntesis y no del primero", "Sumó el paréntesis en lugar de restarlo, sin cambiar ningún signo", "Multiplicó cada término del paréntesis por el coeficiente de la variable", "Restó los coeficientes de x pero olvidó escribir el término numérico"]
    if k == 1:
        return [f"x² · x³ = x⁶"], "Multiplicó los exponentes: en un producto de potencias de igual base los exponentes se suman", \
            ["Sumó los exponentes pero además multiplicó la base por sí misma", "Restó los exponentes porque ambas potencias tienen la misma base", "Elevó la base al mayor de los dos exponentes sin operar", "Multiplicó la base por la suma de los dos exponentes al terminar"]
    if k == 2:
        return [f"{a}x² + {b}x² = {a + b}x⁴"], "Duplicó el exponente al sumar: en la suma de términos semejantes solo se suman los coeficientes", \
            ["Multiplicó los coeficientes en lugar de sumarlos y conservó el exponente", "Sumó los coeficientes y multiplicó por dos el exponente de la variable", "Sumó los exponentes y dejó los coeficientes sin operar entre ellos", "Restó los coeficientes y elevó la variable al cuadrado nuevamente"]
    if k == 3:
        return [f"{a}x + {b}y = {a + b}xy"], "Reunió términos que no son semejantes: x e y son partes literales distintas", \
            ["Sumó los coeficientes y conservó solo la primera variable del resultado", "Multiplicó los coeficientes y escribió ambas variables una junto a otra", "Restó los coeficientes de las dos variables y las escribió en el resultado", "Sumó los coeficientes y elevó al cuadrado la variable resultante final"]
    return [f"−{a}x · (−{b}x) = −{a * b}x²"], "Multiplicó dos negativos y obtuvo negativo: el producto de dos negativos es positivo", \
        ["Sumó los coeficientes en lugar de multiplicarlos entre sí en el producto", "Restó los exponentes en lugar de sumarlos al multiplicar las potencias", "Multiplicó los coeficientes pero perdió una de las variables al final", "Aplicó la regla de los signos de la suma a un producto de monomios"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 120, 21)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equiv(r, l):
    a, b, c, d = rr(r, 2, 6), rr(r, 1, 7), rr(r, 1, 5), rr(r, 1, 6)
    cxs = "x" if c == 1 else f"{c}x"
    base = f"({pstr({'x': a, '': b})}) − ({pstr({'x': c, '': -d})})"
    tot = {"x": a - c, "": b + d}
    good = pstr(tot)
    eq = [good, f"{a}x − {cxs} + {b} + {d}", f"{b + d}" + (pstr({'x': a - c}).join([" + " if a - c > 0 else " − ", ""]).replace("−−", "−") if False else (" + " + pstr({"x": a - c}) if a - c > 0 else " − " + pstr({"x": c - a}))), f"{a}x + {b} − {cxs} + {d}"]
    bad = r.choice([pstr({"x": a - c, "": b - d}), pstr({"x": a + c, "": b + d}), pstr({"x": a - c, "": -(b + d)}), pstr({"x": a - c, "": b + d + 1})])
    if a == c or bad in eq:
        raise Reject
    eq = list(dict.fromkeys(eq))
    if len(eq) < 4:
        raise Reject
    fig = card(["Expresión:", base], 130, 22)
    return make("¿Cuál de las siguientes expresiones NO es equivalente a la expresión de la figura?", fig, bad, eq[:4], Q_ARG, f"Al reducir: {good}.")


TRUE = ["Al restar un paréntesis, cambian los signos de todos los términos que contiene", "Solo se pueden sumar términos que tienen la misma parte literal", "x² · x³ es igual a x⁵",
        "Reducir una expresión no cambia su valor numérico para ningún valor de las variables", "3x − (2x − 1) es igual a x + 1", "(−2x)·(−3x) es igual a 6x²"]
FALSE = ["Al restar un paréntesis, solo cambia el signo del primer término", "3x y 3y son términos semejantes porque tienen el mismo coeficiente", "x² · x³ es igual a x⁶",
         "Reducir una expresión puede cambiar su valor numérico según el caso", "3x − (2x − 1) es igual a x − 1", "(−2x)·(−3x) es igual a −6x²"]


def _fig(r):
    return card(["Operatoria algebraica", "Se reducen términos con igual parte literal"], 130, 19)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre operatoria algebraica es verdadera?", "Sobre reducción de términos semejantes, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las reglas de signos y de exponentes.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre operatoria algebraica es falsa?", "Sobre reducción de términos semejantes, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las reglas de operatoria algebraica.")


BY_SKILL = {
    Q_RES: [t_reduce, t_monomial],
    Q_MOD: [t_perimeter, t_savings, t_pack],
    Q_REP: [t_tiles, t_tiles_sum, t_equiv_forms],
    Q_ARG: [t_error, t_not_equiv, t_true, t_false],
}
