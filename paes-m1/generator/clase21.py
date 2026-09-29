"""Clase 21 (M1) · Inecuaciones lineales: intervalos en la recta real y presupuestos."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase13 import co, lin
from figs import interval_line
from num import dstr
import viz

SYM = {"<": "<", ">": ">", "<=": "≤", ">=": "≥"}
FLIP = {"<": ">", ">": "<", "<=": ">=", ">=": "<="}
STRICT = {"<": "<=", ">": ">=", "<=": "<", ">=": ">"}


def rr(r, lo, hi):
    while True:
        v = r.randint(lo, hi)
        if v:
            return v


def ineq(op, v, var="x"):
    return f"{var} {SYM[op]} {fs(F(v))}"


def interval(a, b, ac, bc):
    l = "−∞" if a is None else fs(F(a))
    rgt = "∞" if b is None else fs(F(b))
    return f"{'[' if ac and a is not None else '('}{l}, {rgt}{']' if bc and b is not None else ')'}"


def uq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        if a is None:
            continue
        if a not in seen:
            seen.add(a); out.append(a)
    return out


def gen_lin(r, l):
    """Inecuación a x + b OP c con solución x OP' k; devuelve texto, op final, k y errores."""
    a = rr(r, -6, 7)
    if abs(a) == 1:
        a = a * 2
    k = rr(r, -8, 10)
    b = rr(r, -9, 9)
    op = r.choice(["<", ">", "<=", ">="])
    c = a * k + b
    text = f"{lin(a, b)} {SYM[op]} {c}".replace("-", "−")
    op_f = op if a > 0 else FLIP[op]
    return text, op_f, k, a, b, c, op


# ---------------------------------------------------------------- Resolver problemas
def t_solve(r, l):
    if l < 2:
        text, op_f, k, a, b, c, op = gen_lin(r, l)
        ans = ineq(op_f, k).replace("-", "−")
        alts = [ineq(FLIP[op_f], k), ineq(op_f, -k), ineq(op_f, F(c + b, a)) if a else None, ineq(FLIP[op_f], -k), ineq(STRICT[op_f], k)]
        if l == 0 and a < 0:
            raise Reject
        ex = "Se despeja x dividiendo por su coeficiente: si es negativo, se invierte el sentido de la desigualdad."
    else:
        a = rr(r, 2, 4)
        lo, hi = rr(r, -8, 4), rr(r, 5, 12)
        b = rr(r, -6, 6)
        # lo' < a x + b <= hi'
        k1, k2 = rr(r, -5, 3), rr(r, 4, 9)
        text = f"{a * k1 + b} < {lin(a, b)} ≤ {a * k2 + b}".replace("-", "−")
        ans = f"{fs(F(k1))} < x ≤ {k2}".replace("-", "−")
        alts = [f"{fs(F(k1))} ≤ x < {k2}", f"{k1} < x ≤ {a * k2}", f"{a * k1} < x ≤ {a * k2}", f"{k2} < x ≤ {k1}", f"{fs(F(-k1))} < x ≤ {k2}"]
        alts = [x.replace("-", "−") for x in alts]
        ex = "Se resta el término independiente a los tres miembros y luego se divide por el coeficiente positivo."
    fig = card(["Resuelve la inecuación:", text], 130, 22)
    al = uq(ans, alts)
    return make("¿Cuál es el conjunto solución de la inecuación de la figura?", fig, ans, al[:4], Q_RES, ex)


def t_integers(r, l):
    a = r.randint(2, 5)
    k = r.randint(3, 12)
    b = rr(r, -6, 6)
    op = r.choice(["<", "<="])
    c = a * k + b
    lo = r.choice([0, 1, -2])
    if op == "<":
        top = k - 1 if True else k
        cnt = top - lo + 1
        cond = "<"
    else:
        top = k
        cnt = top - lo + 1
        cond = "≤"
    if cnt < 2:
        raise Reject
    text = f"{lin(a, b)} {cond} {c}".replace("-", "−")
    fig = card(["Inecuación:", text, f"con x entero y x ≥ {lo}".replace("-", "−")], 170, 21)
    ans = str(cnt)
    alts = [cnt - 1, cnt + 1, cnt + 2, k, top]
    al = [str(x) for x in dict.fromkeys(alts) if x != cnt and x > 0]
    stem = f"¿Cuántos números enteros x, con x ≥ {lo}, cumplen la inecuación de la figura?".replace("-", "−")
    return make(stem, fig, ans, al[:4], Q_RES, f"La solución es x {cond} {k}; los enteros desde {lo} hasta {top} son {cnt}.".replace("-", "−"))


def t_smallest(r, l):
    a = r.randint(2, 6)
    k = r.randint(2, 15)
    b = rr(r, -9, 9)
    strict = r.random() < 0.6
    c = a * k + b + (r.randint(0, a - 1) if strict or True else 0)
    op = ">" if strict else ">="
    sol = F(c - b, a)
    import math
    if strict:
        n = math.floor(sol) + 1
    else:
        n = math.ceil(sol)
    fig = card([f"{lin(a, b)} {SYM[op]} {c}".replace("-", "−"), "x es un número entero"], 130, 22)
    ans = str(n)
    alts = [n - 1, n + 1, math.floor(sol), math.ceil(sol) + 1, n + 2, n - 2, n * 2]
    al = [str(x).replace("-", "−") for x in dict.fromkeys(alts) if x != n]
    return make("¿Cuál es el menor número entero que cumple la inecuación de la figura?", fig, str(n).replace("-", "−"), al[:4], Q_RES, f"x {SYM[op]} {fs(sol)}; el menor entero es {n}.".replace("-", "−"))


# ---------------------------------------------------------------- Modelar
def f_(z):
    return "$" + f"{z:,}".replace(",", ".")


def t_budget(r, l):
    B = r.choice([10000, 15000, 20000, 30000, 50000])
    a = r.choice([2000, 3000, 4000, 5000])
    b = r.choice([500, 800, 1000, 1200, 1500])
    n_max = (B - a) // b
    if n_max < 2 or (B - a) % b == 0 and False:
        raise Reject
    ctx = r.choice([("entrada", "bebida"), ("pasaje", "snack"), ("matrícula", "clase")])
    art = {"entrada": "una", "pasaje": "un", "matrícula": "una"}[ctx[0]]
    fig = card([f"Presupuesto: {f_(B)}", f"{ctx[0].capitalize()}: {f_(a)} (una vez)", f"Cada {ctx[1]}: {f_(b)}"], 170, 19)
    kind = r.choice(["max", "expr"])
    if kind == "max":
        stem = f"Con un presupuesto de {f_(B)} se compra {art} {ctx[0]} de {f_(a)} y se quieren comprar {ctx[1]}s de {f_(b)} cada una. ¿Cuál es la mayor cantidad de {ctx[1]}s que se puede comprar?"
        ans = str(n_max)
        alts = [n_max + 1, n_max - 1, B // b, (B + a) // b, n_max + 2]
        al = [str(x) for x in dict.fromkeys(alts) if x != n_max and x > 0]
        return make(stem, fig, ans, al[:4], Q_MOD, f"{a} + {b}n ≤ {B} ⟹ n ≤ {fs(F(B - a, b))}; el mayor entero es {n_max}.")
    stem = f"Con un presupuesto de {f_(B)} se compra {art} {ctx[0]} de {f_(a)} y n {ctx[1]}s de {f_(b)} cada una. ¿Qué inecuación representa la situación?"
    ans = f"{a} + {b}n ≤ {B}"
    alts = [f"{a} + {b}n ≥ {B}", f"{a + b}n ≤ {B}", f"{a}n + {b} ≤ {B}", f"{a} + {b}n < {B - a}"]
    return make(stem, fig, ans, alts, Q_MOD, "El gasto total (fijo + variable) no puede superar el presupuesto.")


def t_min_grade(r, l):
    k = r.choice([3, 4, 5])
    notes = [r.randint(35, 68) for _ in range(k)]
    need = F(r.choice([40, 45, 50]))
    tot = need * (k + 1)
    x = tot - sum(notes)
    if x < 10 or x > 70:
        raise Reject
    fmt = lambda t: dstr(F(t, 10), 1)
    fig = card(["Notas: " + "; ".join(fmt(n) for n in notes), f"Promedio de {k + 1} notas ≥ {fmt(need)}"], 140, 19)
    stem = f"Una estudiante tiene las notas {', '.join(fmt(n) for n in notes)} y rendirá una última prueba. Para aprobar necesita un promedio de las {k + 1} notas de al menos {fmt(need)}. ¿Qué nota mínima debe obtener?"
    ans = fmt(x)
    alts = [F(need) - F(sum(notes), k), tot - sum(notes) + 5, F(sum(notes), k), x - 6 if x > 16 else x + 6, need * 2 - sum(notes) // k]
    def sfmt(a):
        try:
            return fmt(a)
        except ValueError:
            return None
    al = [t for t in dict.fromkeys(sfmt(a) for a in alts + [x + 3, x - 4, x + 8]) if t and t != ans]
    return make(stem, fig, ans, al[:4], Q_MOD, f"(suma + x)/{k + 1} ≥ {fmt(need)} ⟹ x ≥ {fmt(x)}.")


def t_plan(r, l):
    a, b = r.choice([(5000, 300), (4000, 400), (6000, 200)]), None
    a, b = a
    c = a - r.randint(1, 4) * 500
    u = r.randint(3, 12)
    d = b + (a - c) // u if (a - c) % u == 0 else None
    if d is None or d <= b:
        raise Reject
    fig = card([f"Plan A: {f_(a)} + {f_(b)} por unidad", f"Plan B: {f_(c)} + {f_(d)} por unidad"], 130, 18)
    stem = f"El plan A cuesta {f_(a)} fijos más {f_(b)} por unidad y el plan B cuesta {f_(c)} fijos más {f_(d)} por unidad. ¿Para qué cantidad de unidades el plan A resulta más barato que el plan B?"
    ans = f"Más de {u} unidades"
    alts = [f"Menos de {u} unidades", f"Más de {u + 1} unidades", f"Exactamente {u} unidades", f"Más de {(a - c) // 100} unidades"]
    return make(stem, fig, ans, alts, Q_MOD, f"{a} + {b}x < {c} + {d}x ⟹ x > {u}.")


# ---------------------------------------------------------------- Representar
def t_read_interval(r, l):
    kind = r.choice(["ray_l", "ray_r", "seg"] if l else ["ray_l", "ray_r"])
    lo, hi = -6, 6
    if kind == "seg":
        a, b = r.randint(-5, 0), r.randint(1, 5)
        ac, bc = r.random() < 0.5, r.random() < 0.5
        fig = interval_line(lo, hi, a, b, ac, bc)
        ans = f"{fs(F(a))} {'≤' if ac else '<'} x {'≤' if bc else '<'} {b}".replace("-", "−")
        alts = [f"{fs(F(a))} {'<' if ac else '≤'} x {'≤' if bc else '<'} {b}", f"{fs(F(a))} {'≤' if ac else '<'} x {'<' if bc else '≤'} {b}", f"x {'≤' if ac else '<'} {fs(F(a))} o x {'≥' if bc else '>'} {b}", f"{b} {'≤' if ac else '<'} x {'≤' if bc else '<'} {fs(F(a))}", f"{fs(F(-a))} {'≤' if ac else '<'} x {'≤' if bc else '<'} {-b}"]
        alts = [x.replace("-", "−") for x in alts]
    else:
        k = r.randint(-4, 4)
        closed = r.random() < 0.5
        if kind == "ray_l":
            fig = interval_line(lo, hi, None, k, True, closed)
            ans = f"x {'≤' if closed else '<'} {fs(F(k))}".replace("-", "−")
            alts = [f"x {'≥' if closed else '>'} {fs(F(k))}", f"x {'<' if closed else '≤'} {fs(F(k))}", f"x {'≤' if closed else '<'} {fs(F(-k))}", f"x {'≥' if not closed else '>'} {fs(F(k))}", f"x {'≥' if closed else '>'} {fs(F(-k))}"]
        else:
            fig = interval_line(lo, hi, k, None, closed, True)
            ans = f"x {'≥' if closed else '>'} {fs(F(k))}".replace("-", "−")
            alts = [f"x {'≤' if closed else '<'} {fs(F(k))}", f"x {'>' if closed else '≥'} {fs(F(k))}", f"x {'≥' if closed else '>'} {fs(F(-k))}", f"x {'≤' if not closed else '<'} {fs(F(k))}", f"x {'≤' if closed else '<'} {fs(F(-k))}"]
        alts = [x.replace("-", "−") for x in alts]
    al = uq(ans, alts)
    return make("¿Qué desigualdad representa la parte sombreada de la recta numérica? (Círculo lleno: incluye el número; círculo vacío: no lo incluye.)", fig, ans, al[:4], Q_REP, "El sentido del sombreado indica > o <; el círculo lleno o vacío indica si se incluye el extremo.")


def t_interval_notation(r, l):
    k = r.randint(-4, 4)
    closed = r.random() < 0.5
    kind = r.choice(["l", "r", "s"])
    lo, hi = -6, 6
    if kind == "s":
        a, b = r.randint(-5, 0), r.randint(1, 5)
        ac, bc = r.random() < 0.5, r.random() < 0.5
        fig = interval_line(lo, hi, a, b, ac, bc)
        ans = interval(a, b, ac, bc)
        alts = [interval(a, b, not ac, bc), interval(a, b, ac, not bc), interval(a, b, not ac, not bc), interval(b, a, ac, bc), interval(-b, -a, ac, bc)]
    elif kind == "l":
        fig = interval_line(lo, hi, None, k, True, closed)
        ans = interval(None, k, True, closed)
        alts = [interval(None, k, True, not closed), interval(k, None, closed, True), interval(-k, None, closed, True), interval(None, -k, True, closed), interval(k, None, not closed, True)]
    else:
        fig = interval_line(lo, hi, k, None, closed, True)
        ans = interval(k, None, closed, True)
        alts = [interval(k, None, not closed, True), interval(None, k, True, closed), interval(None, -k, True, closed), interval(-k, None, closed, True), interval(None, k, True, not closed)]
    al = uq(ans, alts)
    return make("¿Qué intervalo representa la parte sombreada de la recta numérica? (Círculo lleno: incluido; círculo vacío: excluido.)", fig, ans, al[:4], Q_REP, "Los paréntesis excluyen el extremo y los corchetes lo incluyen; el infinito siempre va con paréntesis.")


def t_table_ineq(r, l):
    a, b = rr(r, 1, 4), rr(r, -5, 6)
    xs = [0, 1, 2, 3, 4, 5, 6]
    k = r.randint(2, 12)
    op = r.choice([">", ">=", "<", "<="])
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [[lin(a, b)] + [str(a * x + b).replace("-", "−") for x in xs]])
    ok = lambda v: {"<": v < k, "<=": v <= k, ">": v > k, ">=": v >= k}[op]
    sols = [x for x in xs if ok(a * x + b)]
    if not sols or len(sols) == len(xs):
        raise Reject
    stem = f"La tabla muestra los valores de la expresión {lin(a, b)} para distintos valores de x. Según la tabla, ¿qué valores de x cumplen {lin(a, b)} {SYM[op]} {k}?".replace("-", "−")
    ans = "x = " + ", ".join(map(str, sols))
    other = [x for x in xs if x not in sols]
    alts = ["x = " + ", ".join(map(str, other)), "x = " + ", ".join(map(str, sols[1:])) if len(sols) > 1 else "x = " + ", ".join(map(str, sols + [sols[-1] + 1])), "x = " + ", ".join(map(str, sols + ([sols[-1] + 1] if sols[-1] + 1 in xs else [sols[0] - 1]))), "x = " + ", ".join(map(str, sols[:-1])) if len(sols) > 1 else "x = " + str(a), "x = " + ", ".join(str(a * x + b) for x in sols)]
    al = uq(ans, [x.replace("-", "−") for x in alts])
    return make(stem, fig, ans.replace("-", "−"), al[:4], Q_REP, f"Se buscan en la tabla los valores de x cuyo resultado cumple la condición: {ans}.")


# ---------------------------------------------------------------- Argumentar
def _err(r):
    k = r.randrange(4)
    a, b = r.randint(2, 6), r.randint(2, 9)
    if k == 0:
        return [f"−{a}x > {a * b}", f"x > −{b}"], "No invirtió el sentido de la desigualdad al dividir por un número negativo: debió quedar x < −b", \
            ["Cambió el signo del lado derecho pero no el del coeficiente al dividir", "Dividió solo el lado izquierdo por el coeficiente negativo de la inecuación", "Invirtió la desigualdad cuando el coeficiente era positivo, sin motivo", "Multiplicó ambos lados por el coeficiente en vez de dividirlos entre él"]
    if k == 1:
        return [f"x + {b} < {a + b}", f"x ≤ {a}"], "Cambió la desigualdad estricta por una no estricta: el valor límite no forma parte de la solución", \
            ["Restó el término independiente solo de un lado de la inecuación", "Sumó el término independiente en lugar de restarlo de ambos lados", "Invirtió el sentido de la desigualdad al pasar el término numérico", "Dividió por el término independiente en lugar de restarlo del lado derecho"]
    if k == 2:
        return [f"{a}x − {b} ≥ {a}", f"{a}x ≥ {a} − {b}"], "Al pasar −b al otro lado no cambió su signo: debió sumarse, quedando ax ≥ a + b", \
            ["Dividió por el coeficiente antes de mover el término numérico de lugar", "Cambió el sentido de la desigualdad al pasar el término numérico", "Restó el coeficiente de x a ambos lados de la inecuación completa", "Multiplicó el término numérico por menos uno solo en el lado izquierdo"]
    return [f"«Necesito al menos {b} puntos»", f"Inecuación: x < {b}"], "«Al menos» significa mayor o igual: debió plantear x ≥ b, no x < b", \
        ["«Al menos» significa mayor que, sin incluir el valor: debió plantear x > b", "«Al menos» significa menor o igual: debió plantear x ≤ b para el valor dado", "«Al menos» significa exactamente igual: debió plantear una ecuación x = b", "El planteo es correcto porque necesitar puntos implica un valor menor que b"]


def t_error(r, l):
    lines, ans, alts = _err(r)
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 20)
    return make("Observa la resolución de la figura. ¿Qué error cometió el estudiante?", fig, ans, alts, Q_ARG, ans + ".")


def t_not_equiv(r, l):
    k = r.randint(2, 9)
    a = r.randint(2, 5)
    b = r.randint(1, 8)
    c = a * k + b
    base = f"{a}x + {b} < {c}"
    good = [f"{a}x < {c - b}", f"x < {k}", f"−{a}x > −{c - b}", f"{2 * a}x + {2 * b} < {2 * c}"]
    bad = r.choice([f"x > {k}", f"{a}x < {c + b}", f"−{a}x < −{c - b}", f"x < {c - b}"])
    fig = card(["Inecuación:", base], 130, 24)
    return make("¿Cuál de las siguientes inecuaciones NO es equivalente a la inecuación de la figura?", fig, bad.replace("-", "−"), [g.replace("-", "−") for g in good], Q_ARG, f"La solución de la inecuación es x < {k}.")


TRUE = ["Al multiplicar o dividir ambos lados por un número negativo, se invierte el sentido de la desigualdad", "En x ≥ 3, el número 3 es una solución de la inecuación", "En x > 3, el número 3 no es una solución de la inecuación",
        "La expresión «a lo más 5» se escribe x ≤ 5", "La expresión «al menos 5» se escribe x ≥ 5", "Sumar el mismo número a ambos lados de una desigualdad no cambia su sentido"]
FALSE = ["Al dividir ambos lados por un número negativo, el sentido de la desigualdad se mantiene", "En x > 3, el número 3 es una solución de la inecuación", "La expresión «a lo más 5» se escribe x ≥ 5",
         "La expresión «al menos 5» se escribe x < 5", "Una inecuación de primer grado siempre tiene una única solución", "Sumar un número negativo a ambos lados invierte el sentido de la desigualdad"]


def _fig(r):
    return interval_line(-6, 6, r.randint(-3, 3), None, True, True)


def t_true(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre inecuaciones es verdadera?", "Sobre desigualdades e intervalos, ¿cuál afirmación es correcta?"]), _fig(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta con las propiedades de las desigualdades.")


def t_false(r, l):
    return make(r.choice(["¿Cuál de las siguientes afirmaciones sobre inecuaciones es falsa?", "Sobre desigualdades e intervalos, ¿cuál afirmación es incorrecta?"]), _fig(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de las desigualdades.")


BY_SKILL = {
    Q_RES: [t_solve, t_integers, t_smallest],
    Q_MOD: [t_budget, t_min_grade, t_plan],
    Q_REP: [t_read_interval, t_interval_notation, t_table_ineq],
    Q_ARG: [t_error, t_not_equiv, t_true, t_false],
}
