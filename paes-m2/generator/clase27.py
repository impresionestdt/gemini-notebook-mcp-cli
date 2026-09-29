"""Clase 27 · Propiedades de las medidas de dispersión: efecto de sumar o multiplicar constantes."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase26 import dataset, mean, var, sd_exact, ssd, lst, uniq, dots2, two_cards, dots

SD_INT = lambda r, l: dataset(r, l, "sd")


def stats(d):
    return mean(d), var(d), sd_exact(var(d)), max(d) - min(d)


def sgn(x):
    return fs(x)


def kname(k):
    return {2: "se duplica", 3: "se triplica", 4: "se cuadruplica", 5: "se multiplica por 5", 10: "se multiplica por 10"}[k]


# ---------------------------------------------------------------- Resolver problemas
def t_shift(r, l):
    d = SD_INT(r, l)
    m, v, s, R = stats(d)
    c = r.choice([3, 4, 5, 7, 10, 12, 20] if l < 2 else [-3, -5, -8, 15, 25, 50])
    what = r.choice(["varianza", "desviación estándar", "rango"])
    val = {"varianza": v, "desviación estándar": s, "rango": R}[what]
    verbo = f"se suma {c} a cada dato" if c > 0 else f"se restan {-c} a cada dato"
    fig = two_cards([f"Media: {m}", f"Varianza: {fs(v)}", f"Desv. estándar: {fs(s)}", f"Rango: {R}"], ["Cada dato cambia", f"{'+' if c > 0 else '−'} {abs(c)}", "", ""], "Datos originales", "Transformación")
    stem = f"Un conjunto de datos tiene las medidas indicadas. Si {verbo}, ¿cuál es la nueva {what}?"
    ans = fs(val)
    alts = [val + c, val + c * c, val * abs(c), val - c if val > abs(c) else val + 1, val * c * c, m + c]
    ex = f"Sumar o restar una constante desplaza los datos pero no cambia su separación: la {what} sigue siendo {ans}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_scale(r, l):
    d = SD_INT(r, l)
    m, v, s, R = stats(d)
    k = r.choice([2, 3, 4, 5] if l < 2 else [2, 3, 4, 5, 10])
    what = r.choice(["varianza", "desviación estándar", "rango"])
    val = {"varianza": v * k * k, "desviación estándar": s * k, "rango": R * k}[what]
    base = {"varianza": v, "desviación estándar": s, "rango": R}[what]
    fig = two_cards([f"Media: {m}", f"Varianza: {fs(v)}", f"Desv. estándar: {fs(s)}", f"Rango: {R}"], [f"Cada dato se", f"multiplica por {k}", "", ""], "Datos originales", "Transformación")
    stem = f"Un conjunto de datos tiene las medidas indicadas. Si cada dato se multiplica por {k}, ¿cuál es la nueva {what}?"
    ans = fs(val)
    alts = [base, base * k * k if what != "varianza" else base * k, base + k, base * k if what == "varianza" else base * k * k, base * k * k * k, F(base, k) if base % k == 0 else base + 2 * k]
    ex = f"Al multiplicar por {k}, el rango y la desviación estándar se multiplican por {k}, y la varianza por {k}² = {k * k}: resultado {ans}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


def t_affine(r, l):
    d = SD_INT(r, l)
    m, v, s, R = stats(d)
    a = r.choice([2, 3, 4, 5] if l < 2 else [-2, -3, -4, 5])
    b = r.choice([1, 3, 5, 10, 20])
    what = r.choice(["desviación estándar", "varianza"])
    val = {"desviación estándar": s * abs(a), "varianza": v * a * a}[what]
    base = {"desviación estándar": s, "varianza": v}[what]
    fig = card([f"Datos x: media {m}, σ = {fs(s)}", f"Nuevos datos: y = {a}x + {b}".replace("+ -", "− ").replace("-", "−")], 130, 20)
    stem = f"Los datos x tienen desviación estándar {fs(s)}. Se definen los datos y = {a}x + {b}. ¿Cuál es la {what} de y?".replace("+ -", "− ").replace("-", "−")
    ans = fs(val)
    alts = [base, base * a if a > 0 else base * -a, base * abs(a) + b if what == "desviación estándar" else base + b, base * a * a + b if what == "varianza" else base * abs(a) ** 2, -val, base * abs(a) * 3]
    ex = f"El sumando {b} no altera la dispersión; el factor {a} multiplica la desviación estándar por |{a}| y la varianza por {a * a}: {ans}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_raise(r, l):
    m = r.choice([400, 500, 600, 800, 1000]) * 1000
    s = r.choice([20, 50, 80, 100, 150]) * 1000
    tipo = r.choice(["fijo", "doble"] if l else ["fijo"])
    n = lambda x: f"${x:,}".replace(",", ".")
    fig = card([f"Sueldos actuales: media {n(m)}", f"Desviación estándar {n(s)}"], 120, 20)
    if tipo == "fijo":
        c = r.choice([30, 50, 80, 100]) * 1000
        stem = f"En una empresa los sueldos tienen la media y desviación estándar indicadas. Todos reciben un bono fijo de {n(c)}. ¿Cuál es la desviación estándar de los nuevos sueldos?"
        ans = n(s)
        alts = [n(s + c), n(m + c), n(s * 2), n(s + c // 2), n(c)]
        ex = "Un aumento igual para todos desplaza los sueldos sin cambiar su dispersión."
    else:
        stem = "En una empresa los sueldos tienen la media y desviación estándar indicadas. Todos los sueldos se duplican. ¿Cuál es la desviación estándar de los nuevos sueldos?"
        ans = n(2 * s)
        alts = [n(s), n(4 * s), n(s + m), n(2 * s + m), n(m * 2)]
        ex = "Duplicar los datos duplica la desviación estándar."
    return make(stem, fig, ans, alts[:4], Q_MOD, ex)


CONV = [("metros", "centímetros", 100), ("kilómetros", "metros", 1000), ("horas", "minutos", 60), ("minutos", "segundos", 60), ("kilogramos", "gramos", 1000)]


def t_units(r, l):
    a, b, k = r.choice(CONV)
    s = r.choice([2, 3, 4, 5, 6, 8, 10, 12])
    m = r.randint(10, 60)
    fig = card([f"Datos en {a}: media {m}", f"Desviación estándar {s} {a}"], 120, 20)
    what = r.choice(["desviación estándar", "varianza"] if l else ["desviación estándar"])
    ans_v = s * k if what == "desviación estándar" else s * s * k * k
    base = s if what == "desviación estándar" else s * s
    stem = f"Las mediciones están en {a}. Al expresarlas en {b} (1 {a[:-1] if a.endswith('s') else a} = {k} {b}), ¿cuál es la nueva {what} (en {b}{'²' if what == 'varianza' else ''})?"
    fmtn = lambda x: f"{x:,}".replace(",", ".")
    ans = fmtn(ans_v)
    alts = [base, base + k, base * k * k if what == "desviación estándar" else base * k, m * k, base * k * 10, base * k // 2]
    ex = f"Cambiar de unidad es multiplicar por {k}: la desviación estándar se multiplica por {k} y la varianza por {k}²."
    alts = uniq(ans, [fmtn(x) for x in alts])
    return make(stem, fig, ans, alts[:4], Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_dots_shift(r, l):
    d = dataset(r, 0, "var", n=r.choice([6, 8]))
    k = r.choice([1, 1, 2, 3]) if l else 1
    c = r.choice([4, 5, 6, 8, 10])
    if k == 1:
        B = [x + c for x in d]
        stem = "El diagrama B se obtuvo a partir de A transformando todos sus datos. ¿Qué afirmación es correcta?"
        ans = "Tienen igual rango y desviación estándar, pero distinta media"
        alts = ["Tienen igual media, pero B tiene mayor desviación estándar", "Tienen igual media y distinta desviación estándar", "B tiene mayor rango y mayor desviación estándar que A", "B tiene menor varianza que A, pues sus datos son mayores"]
        ex = f"B se obtiene sumando {c} a cada dato de A: solo cambia la posición (la media), no la dispersión."
    else:
        base = [x - min(d) + 1 for x in d]
        A = base
        B = [k * x for x in base]
        if max(B) > 30:
            raise Reject
        stem = f"El diagrama B se obtuvo multiplicando por {k} cada dato de A. ¿Qué afirmación es correcta?"
        ans = f"La desviación estándar de B es {k} veces la de A y su rango también"
        alts = [f"La desviación estándar de B es igual a la de A, pues los datos siguen la misma forma", f"La varianza de B es {k} veces la de A y su rango también", f"El rango de B es igual al de A, pero su media es {k} veces mayor", f"La desviación estándar de B es {k} veces menor que la de A"]
        ex = f"Multiplicar por {k} multiplica por {k} el rango y la desviación estándar (la varianza queda multiplicada por {k * k})."
        return make(stem, dots2(A, B), ans, alts, Q_REP, ex)
    return make(stem, dots2(d, B), ans, alts, Q_REP, ex)


def t_missing_stat(r, l):
    d = SD_INT(r, l)
    m, v, s, R = stats(d)
    k = r.choice([2, 3, 4, 5])
    c = r.choice([2, 5, 10])
    slot = r.choice(["rango", "varianza", "media"])
    trans = f"cada dato × {k}" if l < 2 else f"cada dato × {k} y luego + {c}"
    mm = m * k + (c if l == 2 else 0)
    vals = {"rango": (R, R * k), "varianza": (v, v * k * k), "media": (m, mm)}
    lines_a = [f"Media: {m}", f"Varianza: {fs(v)}", f"Rango: {R}"]
    lines_b = [f"Media: {fs(mm)}" if slot != "media" else "Media: ?", f"Varianza: {fs(v * k * k)}" if slot != "varianza" else "Varianza: ?", f"Rango: {R * k}" if slot != "rango" else "Rango: ?"]
    fig = two_cards(lines_a + [""], lines_b + [trans], "Originales", "Transformados")
    ans_v = vals[slot][1]
    stem = f"La tabla compara un conjunto de datos y su transformación ({trans}). ¿Qué valor corresponde a «{slot.capitalize()}: ?» en los datos transformados?"
    ans = fs(ans_v)
    base = vals[slot][0]
    alts = [base, base * k, base + k, base * k * k if slot != "varianza" else base * k, base * k + c + 1, base * k * k * k]
    ex = f"Media: se transforma igual que los datos; rango: × {k}; varianza: × {k}² = {k * k}."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_REP, ex)


def t_compare_transform(r, l):
    d = dataset(r, 0, "var", n=r.choice([5, 6, 8]))
    c = r.choice([3, 5, 8, 10])
    k = r.choice([2, 3])
    mode = r.choice(["sum", "mul"])
    B = [x + c for x in d] if mode == "sum" else [k * x for x in d]
    lab = f"B: cada dato de A {'+ ' + str(c) if mode == 'sum' else '× ' + str(k)}"
    which = r.choice(["mayor", "igual"]) if mode == "mul" else "igual"
    stem = "Los diagramas muestran el conjunto A y el conjunto B, obtenido a partir de A. ¿Qué se puede afirmar sobre la dispersión de B respecto de A?"
    if mode == "sum":
        ans = "Es la misma, pues B solo desplaza los datos de A"
        alts = ["Es mayor, pues los datos de B son mayores", "Es menor, pues B tiene valores más altos", f"Es {c} unidades mayor, pues cada dato subió {c}", "No se puede comparar sin conocer las medias"]
        ex = "Al sumar una constante, las distancias entre los datos no cambian."
    else:
        ans = f"Es mayor: los datos de B están más separados entre sí, {k} veces"
        alts = ["Es la misma, pues la forma del diagrama se conserva", f"Es menor, pues los datos se multiplican por {k}", "Es la misma, pues la media se multiplicó igual", f"Es {k} unidades mayor"]
        ex = f"Multiplicar por {k} separa los datos {k} veces más: el rango y la desviación estándar se multiplican por {k}."
    return make(stem, dots2(d, B, "A", "B"), ans, alts, Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
TRUE = [
    "Sumar la misma constante a todos los datos no cambia la desviación estándar",
    "Sumar la misma constante a todos los datos no cambia el rango",
    "Multiplicar todos los datos por 3 multiplica por 3 la desviación estándar",
    "Multiplicar todos los datos por 3 multiplica por 9 la varianza",
    "Al restar una constante a todos los datos, la varianza permanece igual",
    "Multiplicar por −2 todos los datos multiplica por 2 la desviación estándar",
    "La desviación estándar de los datos multiplicados por k es |k| veces la original",
    "Si se agrega un dato igual a la media, la media no cambia y la varianza disminuye",
    "Cambiar la unidad de medida de los datos modifica la desviación estándar en el mismo factor",
]
FALSE = [
    "Sumar una constante a todos los datos aumenta la varianza en esa constante",
    "Multiplicar todos los datos por 3 multiplica por 3 la varianza",
    "Sumar 10 a todos los datos aumenta 10 unidades el rango",
    "Multiplicar por −2 todos los datos hace negativa la desviación estándar",
    "Si se duplican todos los datos, la desviación estándar no cambia",
    "Sumar una constante a todos los datos aumenta la desviación estándar en esa constante",
    "Al multiplicar por 2 los datos, el rango se mantiene",
    "Al sumar una constante, la media no cambia",
    "Agregar un dato igual a la media aumenta la varianza",
    "Si se multiplican los datos por 0,5, la varianza se reduce a la mitad",
    "La varianza se multiplica por k cuando los datos se multiplican por k",
    "Sumar una constante negativa reduce la dispersión de los datos",
]


def _fig27(r):
    d = dataset(r, 0, "var", n=6)
    c = r.choice([3, 5, 8])
    return dots2(d, [x + c for x in d], "Datos", "Datos + c")


def t_true(r, l):
    ctx = r.choice(["Se transforman los datos de un estudio", "Se modifica un conjunto de datos", "Se trabaja con datos de una muestra", "Se ajustan los datos de una medición"])
    stem = f"{ctx}. ¿Cuál de las siguientes afirmaciones sobre las medidas de dispersión es verdadera?"
    return make(stem, _fig27(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se aplican las propiedades: sumar constantes no altera la dispersión; multiplicar por k multiplica la desviación estándar por |k| y la varianza por k².")


def t_false(r, l):
    ctx = r.choice(["Se transforman los datos de un estudio", "Se modifica un conjunto de datos", "Se trabaja con datos de una muestra", "Se ajustan los datos de una medición"])
    stem = f"{ctx}. ¿Cuál de las siguientes afirmaciones sobre las medidas de dispersión es FALSA?"
    return make(stem, _fig27(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las propiedades de la varianza, la desviación estándar y el rango frente a transformaciones.")


def t_error(r, l):
    d = SD_INT(r, 0)
    m, v, s, R = stats(d)
    c = r.choice([3, 4, 5, 6, 10])
    k = r.choice([2, 3, 4])
    kind = r.randrange(3)
    ERR = ["Sumó la constante a la varianza, pero sumar no altera la dispersión",
           "Multiplicó la varianza por k, pero debía multiplicarla por k al cuadrado",
           "Multiplicó la desviación estándar por k al cuadrado en lugar de por k",
           "Restó la constante al rango, pero sumar no altera el rango"]
    if kind == 0:
        line1, line2, ans = f"Se suma {c} a cada dato", f"Nueva varianza = {fs(v)} + {c} = {fs(v + c)}", ERR[0]
    elif kind == 1:
        line1, line2, ans = f"Cada dato se multiplica por {k}", f"Nueva varianza = {fs(v)} · {k} = {fs(v * k)}", ERR[1]
    else:
        line1, line2, ans = f"Cada dato se multiplica por {k}", f"Nueva desv. estándar = {fs(s)} · {k * k} = {fs(s * k * k)}", ERR[2]
    fig = card([f"Datos originales: varianza {fs(v)}, σ = {fs(s)}", line1, line2], 170, 18)
    stem = "Un estudiante calculó una medida de dispersión luego de transformar los datos. ¿Qué error cometió?"
    return make(stem, fig, ans, [e for e in ERR if e != ans] + ["Confundió la varianza con el rango de los datos"], Q_ARG,
                "La suma de constantes no cambia la dispersión; multiplicar por k multiplica σ por |k| y la varianza por k².")


def t_add_mean(r, l):
    d = SD_INT(r, 0)
    m, v, s, R = stats(d)
    fig = dots(d)
    ctx = r.choice(["una nueva medición", "un nuevo participante", "un dato adicional"])
    stem = f"A los datos del diagrama (media {m}) se agrega {ctx} igual a la media. ¿Qué ocurre con la media y la varianza?"
    ans = "La media no cambia y la varianza disminuye"
    alts = ["La media y la varianza no cambian", "La media no cambia y la varianza aumenta", "La media aumenta y la varianza no cambia", "La media y la varianza aumentan"]
    ex = "La suma de cuadrados de las desviaciones no cambia (el nuevo dato aporta 0) pero se divide por un n mayor, por lo que la varianza disminuye."
    return make(stem, fig, ans, alts, Q_ARG, ex)


# ---------------------------------------------------------------- Aplicar procedimientos
def t_calc_var_y(r, l):
    d = dataset(r, l, "var")
    m, v, s, R = stats(d)
    a = r.choice([2, 3, 4] if l < 2 else [-2, -3, 5])
    b = r.choice([1, 2, 5, 10])
    fig = dots(d)
    stem = f"Los datos del diagrama tienen varianza {fs(v)}. ¿Cuál es la varianza de los datos y = {a}x + {b}?".replace("-", "−")
    ans = fs(v * a * a)
    alts = [v, v * abs(a), v * a * a + b, v * abs(a) + b, v + b, v * a * a * a * a]
    ex = f"Var(y) = a²·Var(x) = {a * a}·{fs(v)} = {ans}; el sumando {b} no interviene."
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


def t_calc_sd_z(r, l):
    d = SD_INT(r, l)
    m, v, s, R = stats(d)
    a = r.choice([2, 3, 5, 10] if l < 2 else [-2, -3, -5, 4])
    b = r.choice([1, 4, 7, 12])
    fig = card([f"Datos: {lst(d)}", f"Nuevos datos: {a}x + {b}".replace("+ -", "− ").replace("-", "−")], 130, 19)
    stem = f"Con los datos {lst(d)} se construyen los datos y = {a}x + {b}. ¿Cuál es la desviación estándar de y?".replace("-", "−")
    ans = fs(s * abs(a))
    alts = [s, s * a * a if a > 0 else s * abs(a) * 2, s * abs(a) + b, v * a * a, s + b, v]
    ex = f"σ(x) = √{fs(v)} = {fs(s)}; σ(y) = |{a}|·σ(x) = {ans}.".replace("-", "−")
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


def t_calc_range(r, l):
    d = dataset(r, 0, "var")
    R = max(d) - min(d)
    a = r.choice([2, 3, 4, 5] if l < 2 else [-2, -3, -4])
    b = r.choice([1, 3, 6, 10])
    fig = dots(d)
    stem = f"El diagrama muestra un conjunto de datos x. ¿Cuál es el rango de los datos y = {a}x + {b}?".replace("-", "−")
    ans = fs(R * abs(a))
    alts = [R, R * abs(a) + b, R + b, R * a * a, max(d) * abs(a) + b - (min(d) * abs(a) + b) + b, R * abs(a) + 1]
    ex = f"Rango(x) = {max(d)} − {min(d)} = {R}; Rango(y) = |{a}|·{R} = {ans}.".replace("-", "−")
    return make(stem, fig, ans, pick4(ans, uniq(ans, alts)), Q_PRO, ex)


BY_SKILL = {
    Q_RES: [t_shift, t_scale, t_affine],
    Q_MOD: [t_raise, t_units],
    Q_REP: [t_dots_shift, t_missing_stat, t_compare_transform],
    Q_ARG: [t_true, t_false, t_error, t_add_mean],
    Q_PRO: [t_calc_var_y, t_calc_sd_z, t_calc_range],
}
