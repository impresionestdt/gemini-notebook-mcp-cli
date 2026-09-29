"""Clase 30 · Corrección integral y estrategias finales: análisis de distractores (por qué una alternativa falsa «parece» correcta)."""
from fractions import Fraction as F
from math import gcd
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
import geo
import clase26


def n(x):
    return f"{int(x):,}".replace(",", ".")


def M(s):
    return s.replace("-", "−")


def uniq(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = a if isinstance(a, str) else fs(a)
        if s not in seen:
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver problemas (problemas con «trampa»)
def t_pct_trap(r, l):
    p = r.choice([10, 20, 25, 30, 40, 50] if l < 2 else [10, 15, 20, 25, 30, 40, 60])
    q = p if l == 0 else r.choice([x for x in (10, 20, 25, 30, 40, 50) if x != p])
    base = r.choice([10000, 20000, 40000, 50000, 80000, 100000, 200000])
    fin = F(base) * (100 + p) * (100 - q) / 10000
    if fin.denominator != 1 or fin == base:
        raise Reject
    fin = int(fin)
    fig = card([f"Precio inicial: ${n(base)}", f"Aumenta {p}% y luego baja {q}%"], 130, 21)
    stem = "Un artículo cambia de precio como indica la figura. ¿Cuál es su precio final?"
    ans = f"${n(fin)}"
    alts = [f"${n(base)}", f"${n(base * (100 + p - q) // 100)}", f"${n(base * (100 - p) * (100 + q) // 10000)}" if base * (100 - p) * (100 + q) % 10000 == 0 else f"${n(fin + base // 100)}",
            f"${n(base + base * p // 100)}", f"${n(base - base * q // 100)}", f"${n(2 * base - fin)}"]
    ex = f"Los porcentajes se aplican sobre bases distintas: {n(base)}·{F(100 + p, 100)}·{F(100 - q, 100)} = {n(fin)}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_scale_trap(r, l):
    k = r.choice([2, 3, 4, 5])
    a = r.randint(2, 9)
    if l == 0:
        A = a * a
        fig = geo.two_squares(k, f"área {A} cm²", "área = ?")
        stem = f"El segundo cuadrado es una ampliación del primero con razón de semejanza {k}:1 (sus lados). ¿Cuál es su área?"
        ans = f"{A * k * k} cm²"
        alts = [f"{A * k} cm²", f"{A * k ** 3} cm²", f"{A + k} cm²", f"{A * 2 * k} cm²", f"{A * k * k + A} cm²"]
        ex = f"El área se multiplica por la razón al cuadrado: {A}·{k}² = {A * k * k}."
    elif l == 1:
        V = a ** 3
        fig = geo.two_cubes(k, f"V = {V} cm³", "V = ?")
        stem = f"El segundo cubo es una ampliación del primero con razón de semejanza {k}:1 (sus aristas). ¿Cuál es su volumen?"
        ans = f"{V * k ** 3} cm³"
        alts = [f"{V * k} cm³", f"{V * k * k} cm³", f"{V + k} cm³", f"{V * 3 * k} cm³", f"{V * k ** 3 + V} cm³"]
        ex = f"El volumen se multiplica por la razón al cubo: {V}·{k}³ = {V * k ** 3}."
    else:
        A = a * a
        fig = geo.two_squares(k, f"área {A} cm²", f"área {A * k * k} cm²")
        stem = f"Dos cuadrados tienen las áreas indicadas. ¿Cuál es la razón de semejanza entre sus lados (mayor : menor)?"
        ans = f"{k} : 1"
        alts = [f"{k * k} : 1", f"{k ** 3} : 1", f"{A * k * k - A} : 1", f"{k * 2} : 1", f"1 : {k}"]
        ex = f"La razón de áreas es {k * k}; la razón de lados es su raíz cuadrada: {k}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_comb_trap(r, l):
    nn = r.randint(5, 10 if l < 2 else 12)
    k = r.randint(2, 4 if l < 2 else 5)
    if k >= nn:
        raise Reject
    from math import comb, perm
    ctx = r.choice([("personas", "un comité"), ("estudiantes", "una delegación"), ("vecinos", "una directiva")])
    fig = card([f"{nn} {ctx[0]} y se forma {ctx[1]} de {k}", "No hay cargos: el orden NO importa"], 130, 20)
    stem = f"De un grupo de {nn} {ctx[0]} se elige {ctx[1]} de {k} integrantes, sin cargos distintos. ¿De cuántas maneras se puede elegir?"
    ans = n(comb(nn, k))
    alts = [n(perm(nn, k)), n(nn ** k), n(nn * k), n(comb(nn, k) * 2), n(comb(nn, k - 1) if k > 1 else nn + 1), n(nn + k)]
    ex = f"El orden no importa: C({nn},{k}) = {ans}; la permutación {n(perm(nn, k))} cuenta cada grupo varias veces."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
MULT = [(2, "doble"), (3, "triple"), (4, "cuádruplo"), (5, "quíntuplo")]


def t_translate(r, l):
    k, nm = r.choice(MULT)
    a, b = r.randint(2, 12), r.randint(3, 40)
    kind = r.choice(["a", "b"])
    if kind == "a":
        sent = f"El {nm} de un número, disminuido en {a}, es {b}."
        ans, alts = f"{k}x − {a} = {b}", [f"{k}(x − {a}) = {b}", f"{k}x + {a} = {b}", f"x − {a} = {k * b}", f"{k}x − {a}x = {b}", f"{k} − x − {a} = {b}"]
        ex = f"«El {nm} de un número» es {k}x y luego se le resta {a}: {k}x − {a} = {b}."
    else:
        sent = f"El {nm} de un número disminuido en {a} es {b}."
        ans, alts = f"{k}(x − {a}) = {b}", [f"{k}x − {a} = {b}", f"{k}(x + {a}) = {b}", f"x − {a} = {k}{b}".replace(f"{k}{b}", str(k * b)), f"{k}x − {a}x = {b}", f"{k} − (x − {a}) = {b}"]
        ex = f"Primero se disminuye el número en {a} y luego se toma su {nm}: {k}(x − {a}) = {b}."
    fig = card(["Enunciado:", sent], 130, 20)
    stem = "¿Qué ecuación modela correctamente el enunciado de la figura?"
    return make(M(stem), fig, M(ans), [M(x) for x in uniq(ans, alts)][:4], Q_MOD, ex)


def dec(p):
    return f"{1 + p / 100:.2f}".rstrip("0").rstrip(".").replace(".", ",")


def t_growth_model(r, l):
    p = r.choice([2, 3, 4, 5, 8, 10, 12, 15, 20, 25])
    C0 = r.choice([100, 200, 500, 1000, 2000, 5000])
    comp = l > 0 or r.random() < 0.5
    ctx = "interés compuesto anual" if comp else "interés simple anual"
    fig = card([f"Capital inicial: ${n(C0)}", f"Crece {p}% cada año ({ctx})"], 130, 20)
    g = dec(p)
    if comp:
        ans = f"C(t) = {n(C0)}·{g}^t"
        alts = [f"C(t) = {n(C0)}·(1 + {p / 100:.2f}·t)".replace(".", ","), f"C(t) = {n(C0)}·{g}·t", f"C(t) = {n(C0)} + {g}^t", f"C(t) = {n(C0)}·{p / 100:.2f}^t".replace(".", ","), f"C(t) = {n(C0)}·{p}^t"]
        ex = "Con interés compuesto el capital se multiplica por el factor de crecimiento cada año: C0·(1 + p)^t."
    else:
        ans = f"C(t) = {n(C0)}·(1 + {p / 100:.2f}·t)".replace(".", ",")
        alts = [f"C(t) = {n(C0)}·{g}^t", f"C(t) = {n(C0)}·{g}·t", f"C(t) = {n(C0)} + {g}^t", f"C(t) = {n(C0)}·{p / 100:.2f}^t".replace(".", ","), f"C(t) = {n(C0)}·{p}^t"]
        ex = "Con interés simple el aumento cada año es siempre el mismo (lineal): C0·(1 + p·t)."
    stem = "¿Qué expresión modela el capital C(t) después de t años?"
    return make(stem, fig, ans, uniq(ans, alts)[:4], Q_MOD, ex)


def t_fraction_rest(r, l):
    a, b = r.choice([(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (2, 7), (5, 6)] if l < 2 else [(3, 8), (4, 7), (5, 8), (3, 7), (5, 9)])
    tot = r.choice([120, 240, 360, 480, 600, 840])
    rest = F(tot) * (1 - F(1, a)) * (1 - F(1, b))
    if rest.denominator != 1:
        raise Reject
    fig = card([f"Dinero inicial: ${n(tot)}", f"Gasta 1/{a} del total y luego 1/{b} de lo que queda"], 130, 19)
    stem = "Según la figura, ¿cuánto dinero queda al final?"
    ans = f"${n(rest)}"
    alts = [f"${n(tot * (1 - F(1, a) - F(1, b)))}" if tot * (1 - F(1, a) - F(1, b)) == int(tot * (1 - F(1, a) - F(1, b))) and tot * (1 - F(1, a) - F(1, b)) > 0 else f"${n(rest + 20)}",
            f"${n(tot * (1 - F(1, a)))}" if (tot * (1 - F(1, a))).denominator == 1 else f"${n(rest + 40)}", f"${n(tot * (F(1, a) + F(1, b)))}" if (tot * (F(1, a) + F(1, b))).denominator == 1 else f"${n(rest + 60)}",
            f"${n(tot * (1 - F(1, b)))}" if (tot * (1 - F(1, b))).denominator == 1 else f"${n(rest - 20)}", f"${n(tot - tot // a - tot // b)}"]
    ex = f"Quedan {tot}·(1−1/{a})·(1−1/{b}) = {n(rest)}: la segunda fracción se toma sobre lo que queda, no sobre el total."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]


def t_trig_read(r, l):
    a, b, c = r.choice(TRIP if l else TRIP[:3])
    k = r.choice([1, 2, 3])
    if r.random() < 0.5:
        a, b = b, a
    adj, opp, hyp = a * k, b * k, c * k
    fig = geo.trig_tri(adj, opp, {"adj": f"{adj}", "opp": f"{opp}", "hyp": f"{hyp}"})
    which = r.choice(["sen", "cos", "tan"])
    val = {"sen": F(opp, hyp), "cos": F(adj, hyp), "tan": F(opp, adj)}
    stem = f"En el triángulo rectángulo de la figura, ¿cuál es el valor de {which} α?"
    ans = fs(val[which])
    alts = [F(hyp, opp), F(hyp, adj), F(adj, opp), F(opp, hyp), F(adj, hyp), F(opp, adj)]
    alts = [x for x in alts if fs(x) != ans]
    ex = f"sen = cateto opuesto/hipotenusa, cos = adyacente/hipotenusa, tan = opuesto/adyacente. Aquí {which} α = {ans}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_REP, ex)


NAMES = [("A", "B", "C", "D", "E"), ("P", "Q", "R", "S", "T"), ("M", "N", "O", "X", "Y"), ("K", "L", "U", "V", "W")]


def t_thales_read(r, l):
    a, b, c, d, e = r.choice(NAMES)
    t = r.choice([0.35, 0.4, 0.5, 0.6])
    fig = geo.thales_tri((a, b, c, d, e), "", "", "", "", t)
    TRUE = [f"{a}{d}/{a}{b} = {a}{e}/{a}{c}", f"{a}{d}/{d}{b} = {a}{e}/{e}{c}", f"{a}{d}/{a}{b} = {d}{e}/{b}{c}", f"{d}{b}/{a}{b} = {e}{c}/{a}{c}"]
    FALSE = [f"{a}{d}/{d}{b} = {e}{c}/{a}{e}", f"{a}{d}/{a}{b} = {a}{e}/{e}{c}", f"{a}{d}/{d}{e} = {d}{b}/{b}{c}", f"{d}{e}/{b}{c} = {a}{d}/{d}{b}", f"{a}{d}/{a}{b} = {e}{c}/{a}{c}"]
    ans = r.choice(TRUE)
    alts = r.sample(FALSE, 4)
    stem = f"En la figura, {d}{e} es paralela a {b}{c}. ¿Cuál de las siguientes proporciones es verdadera?"
    return make(stem, fig, ans, alts, Q_REP, f"Por el teorema de Thales y la semejanza, solo {ans} relaciona segmentos correspondientes.")


def t_dispersion_read(r, l):
    return clase26.t_which_more_spread(r, l)


# ---------------------------------------------------------------- Argumentar (¿por qué se equivocó?)
def _err(r, l):
    k = r.randrange(9)
    a = r.randint(2, 9)
    if k == 0:
        c = a * a
        return ([f"x² = {c}", f"x = √{c} = {a}"], "Omitió la solución negativa, pues x² = c tiene dos soluciones",
                ["Debió dividir {c} por 2, no sacar raíz".format(c=c), "Sumó 2 al resultado en lugar de sacar raíz", "Cambió el signo de {c} antes de sacar raíz".format(c=c), "Elevó al cuadrado {c} en lugar de sacar raíz".format(c=c)])
    if k == 1:
        return ([f"(x + {a})² = x² + {a * a}"], "Olvidó el doble producto: (x + a)² = x² + 2ax + a²",
                ["Sumó {a} en lugar de restarlo al desarrollar".format(a=a), "Multiplicó {a} por 2 pero no lo elevó al cuadrado".format(a=a), "Elevó x al cubo en vez de al cuadrado", "Distribuyó el cuadrado solo sobre el término x"])
    if k == 2:
        m = a * r.randint(2, 6)
        return ([f"−{a}x > {m}", f"x > {m}/{a} = {m // a}"], "No invirtió el sentido de la desigualdad al dividir por un negativo",
                ["Dividió por {a} en lugar de por −{a}".format(a=a), "Restó {a} a ambos lados sin necesidad".format(a=a), "Cambió el signo del lado derecho solamente", "Multiplicó por {a} en vez de dividir".format(a=a)])
    if k == 3:
        b, c, d = r.sample(range(2, 9), 3)
        return ([f"{a}/{b} + {c}/{d} = {a + c}/{b + d}"], "Sumó numeradores y denominadores por separado en lugar de amplificar a común denominador",
                ["Multiplicó los denominadores pero no los numeradores", "Restó los numeradores en vez de sumarlos", "Sumó solo los denominadores", "Simplificó cruzado antes de sumar"])
    if k == 4:
        p = r.choice([10, 20, 25, 30, 40, 50])
        return ([f"Sube {p}% y luego baja {p}%", "Precio final = precio inicial"], "Supuso que el aumento y la baja se anulan, ignorando que las bases de cálculo son distintas",
                ["Aplicó la baja sobre el precio inicial en vez de sobre el nuevo precio", "Restó los porcentajes y aplicó cero por ciento", "Calculó la baja antes del aumento y cambió el resultado", "Sumó ambos porcentajes antes de aplicarlos"])
    if k == 5:
        b = a + r.randint(1, 4)
        return ([f"Catetos {a} y {b}", f"Hipotenusa = {a} + {b} = {a + b}"], "Sumó los catetos en lugar de aplicar Pitágoras (raíz de la suma de sus cuadrados)",
                ["Restó los cuadrados de los catetos en vez de sumarlos", "Calculó la suma de cuadrados pero no sacó la raíz", "Usó un cateto como si fuera la hipotenusa", "Multiplicó los catetos y dividió por 2"])
    if k == 6:
        nn = a + 3
        from math import perm
        return ([f"Elegir 2 de {nn} personas (sin cargos)", f"{nn}·{nn - 1} = {perm(nn, 2)}"], "Usó permutaciones aunque el orden no importa: faltó dividir por 2!",
                ["Elevó {nn} al cuadrado en vez de multiplicar consecutivos".format(nn=nn), "Sumó {nn} y {m} en lugar de multiplicar".format(nn=nn, m=nn - 1), "Dividió por {nn}! en vez de por 2!".format(nn=nn), "Olvidó el factor {m} de la segunda elección".format(m=nn - 1)])
    if k == 7:
        p1, p2 = r.choice([(1, 2), (1, 3), (2, 5), (1, 4)]), r.choice([(1, 5), (2, 3), (3, 4)])
        pa, pb = F(*p1), F(*p2)
        return ([f"A y B independientes: P(A) = {fs(pa)}, P(B) = {fs(pb)}", f"P(A ∩ B) = {fs(pa)} + {fs(pb)} = {fs(pa + pb)}"], "Sumó las probabilidades en lugar de multiplicarlas para eventos independientes",
                ["Restó las probabilidades en vez de multiplicarlas", "Dividió P(A) por P(B) como en la condicional", "Usó el complemento de cada probabilidad", "Multiplicó por 2 el resultado de la unión"])
    d = clase26.dataset(r, 0, "var", n=r.choice([4, 5, 6]))
    m = clase26.mean(d)
    return ([f"Datos: {clase26.lst(d)}  (media {m})", "Varianza = (suma de desviaciones)/n = 0"], "Promedió las desviaciones sin elevarlas al cuadrado, por lo que se anulan",
            ["Dividió por la media en vez de por n", "Usó el rango como varianza", "Elevó al cuadrado la media en lugar de las desviaciones", "Tomó solo el mayor de los datos como referencia"])


def t_error(r, l):
    lines, ans, alts = _err(r, l)
    fig = card(["Resolución de un estudiante:"] + [M(x) for x in lines], 60 + 44 * (len(lines) + 1), 20)
    stem = "Observa la resolución de la figura. ¿Cuál es el error que explica por qué el resultado parece correcto, pero no lo es?"
    return make(stem, fig, ans, alts, Q_ARG, ans + ".")


def t_trap_option(r, l):
    """¿Por qué es tentadora la alternativa trampa? (percent / potencias / fracciones)."""
    k = r.randrange(4)
    if k == 0:
        p = r.choice([10, 20, 25, 30, 40, 50]); base = r.choice([10000, 20000, 50000, 100000])
        lines = [f"Precio ${n(base)}: sube {p}% y baja {p}%", f"Un alumno marca ${n(base)}"]
        ans = "Es tentadora porque parece que el aumento y la baja iguales se compensan"
        alts = ["Es tentadora porque coincide con el precio tras un descuento único", "Es tentadora porque resulta de restar los porcentajes", "Es tentadora porque el precio final siempre es mayor", "Es tentadora porque se calcula con interés simple"]
    elif k == 1:
        b = r.randint(2, 5); e = r.randint(2, 4)
        lines = [f"¿Cuánto es ({b}²)^{e}?", f"Un alumno marca {b ** 2 + e}"]
        ans = "Es tentadora porque se suman los exponentes en lugar de multiplicarlos"
        alts = ["Es tentadora porque se restan los exponentes del cociente", "Es tentadora porque se eleva la base a la potencia mayor", "Es tentadora porque se multiplica la base por el exponente", "Es tentadora porque se ignora el paréntesis"]
        lines[1] = f"Un alumno marca {b ** (2 + e)}"
    elif k == 2:
        a, b = r.sample(range(2, 9), 2)
        lines = [f"¿Cuál es el valor de √({a * a} + {b * b})?", f"Un alumno marca {a + b}"]
        ans = "Es tentadora porque se saca la raíz a cada sumando por separado"
        alts = ["Es tentadora porque se elevan al cuadrado ambos números", "Es tentadora porque se restan las raíces", "Es tentadora porque se multiplica por 2 la raíz de la suma", "Es tentadora porque se sacó raíz cúbica de la suma"]
    else:
        a = r.randint(2, 6); b = r.randint(2, 6)
        lines = [f"¿Cuál es la pendiente de la recta por (0, {a}) y ({b}, 0)?", f"Un alumno marca {fs(F(b, a))}"]
        ans = "Es tentadora porque se invirtió el cociente: usó Δx/Δy en vez de Δy/Δx"
        alts = ["Es tentadora porque se usó la ordenada al origen como pendiente", "Es tentadora porque se sumaron las coordenadas", "Es tentadora porque se ignoró el signo del cociente", "Es tentadora porque se restó a a b"]
        if F(b, a) == F(-a, b):
            raise Reject
    fig = card([M(x) for x in lines], 120, 20)
    stem = "En la figura se muestra una alternativa incorrecta que un alumno marcó. ¿Por qué esa alternativa parece correcta?"
    return make(stem, fig, ans, alts, Q_ARG, ans + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_expand(r, l):
    a = r.randint(2, 9)
    s = r.choice(["+", "−"])
    if l == 0:
        sg = 1 if s == "+" else -1
        ex_ = f"(x {s} {a})²"
        ans = M(f"x² {'+' if sg > 0 else '-'} {2 * a}x + {a * a}")
        alts = [M(f"x² + {a * a}"), M(f"x² - {a * a}"), M(f"x² {'+' if sg > 0 else '-'} {a}x + {a * a}"), M(f"x² {'-' if sg > 0 else '+'} {2 * a}x + {a * a}"), M(f"x² {'+' if sg > 0 else '-'} {2 * a}x - {a * a}")]
    else:
        m = r.randint(2, 4)
        sg = 1 if s == "+" else -1
        ex_ = f"({m}x {s} {a})²"
        ans = M(f"{m * m}x² {'+' if sg > 0 else '-'} {2 * m * a}x + {a * a}")
        alts = [M(f"{m * m}x² + {a * a}"), M(f"{m}x² {'+' if sg > 0 else '-'} {2 * m * a}x + {a * a}"), M(f"{m * m}x² {'+' if sg > 0 else '-'} {m * a}x + {a * a}"), M(f"{m * m}x² {'-' if sg > 0 else '+'} {2 * m * a}x + {a * a}"), M(f"{m * m}x² {'+' if sg > 0 else '-'} {2 * m * a}x - {a * a}")]
    fig = card(["Desarrolla:", M(ex_)], 130, 24)
    return make("¿Cuál es el desarrollo del cuadrado de binomio de la figura?", fig, ans, uniq(ans, alts)[:4], Q_PRO, "(a ± b)² = a² ± 2ab + b²: el doble producto no puede omitirse.")


def t_ineq(r, l):
    k = r.randint(2, 6)
    v = r.randint(-6, 8)
    m = r.randint(1, 12) if l else 0
    c = m - k * v
    if l == 0:
        text = f"−{k}x > {-k * v}" if -k * v != 0 else None
    else:
        text = f"−{k}x + {m} > {c}"
    if text is None:
        raise Reject
    ans = f"x < {fs(F(v))}"
    alts = [f"x > {fs(F(v))}", f"x < {fs(F(-v))}", f"x > {fs(F(-v))}", f"x < {fs(F(v + 1))}", f"x > {fs(F(v - 1))}"]
    fig = card(["Resuelve la inecuación:", M(text)], 130, 24)
    return make(M("¿Cuál es el conjunto solución de la inecuación de la figura?"), fig, M(ans), [M(x) for x in uniq(M(ans), [M(a) for a in alts])][:4], Q_PRO,
                "Al dividir por un número negativo se invierte el sentido de la desigualdad.")


def t_log_val(r, l):
    b = r.choice([2, 3, 5, 10])
    e1, e2 = r.randint(1, 4), r.randint(1, 4)
    if l == 0:
        ex_, val = f"log_{b}({b ** e1})", e1
        alts = [b ** e1, e1 + 1, e1 - 1 if e1 > 1 else e1 + 2, b * e1, F(e1, b)]
    elif l == 1:
        ex_, val = f"log_{b}(1/{b ** e1})", -e1
        alts = [e1, F(1, e1), -e1 - 1, b ** e1, F(1, b ** e1)]
    else:
        ex_, val = f"log_{b}({b ** e1}·{b ** e2})", e1 + e2
        alts = [e1 * e2, b ** (e1 + e2), e1 + e2 + 1, (e1 + e2) * b, b ** e1 * b ** e2]
    fig = card(["Calcula el valor de:", M(ex_)], 130, 24)
    ans = fs(F(val))
    return make("¿Cuál es el valor de la expresión de la figura?", fig, ans, pick4(ans, uniq(ans, [F(x) for x in alts])), Q_PRO,
                "log_b(N) es el exponente al que hay que elevar b para obtener N.")


def t_frac_add(r, l):
    b, d = r.sample([2, 3, 4, 5, 6, 8, 9], 2)
    a, c = r.randint(1, b - 1), r.randint(1, d - 1)
    if l == 2:
        sign = r.choice([1, -1])
    else:
        sign = 1
    val = F(a, b) + sign * F(c, d)
    if val <= 0 or val.denominator == 1 or F(a, b) == F(c, d):
        raise Reject
    text = f"{a}/{b} {'+' if sign > 0 else '−'} {c}/{d}"
    ans = fs(val)
    alts = [F(a + sign * c, b + d), F(a + sign * c, b * d), F(a * c, b * d), F(a + sign * c, max(b, d)), F(a * d + sign * b * c, b + d)]
    fig = card(["Calcula:", text], 130, 24)
    alts = [x for x in alts if x > 0]
    return make("¿Cuál es el resultado de la operación de la figura?", fig, ans, pick4(ans, uniq(ans, alts)), Q_PRO,
                "Se amplifica a un común denominador: (ad ± bc)/bd, y luego se simplifica.")


BY_SKILL = {
    Q_RES: [t_pct_trap, t_scale_trap, t_comb_trap],
    Q_MOD: [t_translate, t_growth_model, t_fraction_rest],
    Q_REP: [t_trig_read, t_thales_read, t_dispersion_read],
    Q_ARG: [t_error, t_trap_option],
    Q_PRO: [t_expand, t_ineq, t_log_val, t_frac_add],
}
