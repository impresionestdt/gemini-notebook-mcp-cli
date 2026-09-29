"""Clase 2 (M1) · Números enteros: múltiplos, divisores y MCM/MCD."""
from math import gcd
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
from figs import timeline, factor_tree


def lcm(a, b):
    return a * b // gcd(a, b)


def fact(n):
    d, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            d[p] = d.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        d[n] = d.get(n, 0) + 1
    return d


SUPS = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def fstr(n):
    return "·".join(f"{p}{str(e).translate(SUPS) if e > 1 else ''}" for p, e in sorted(fact(n).items()))


def S(v):
    return str(v)


def uq(ans, alts):
    seen, out = {S(ans)}, []
    for a in alts:
        s = S(a)
        if s not in seen and a > 0:
            seen.add(s); out.append(s)
    return out


PAIRS0 = [(12, 18), (8, 12), (6, 15), (10, 25), (14, 21), (9, 12), (16, 24), (20, 30), (18, 24), (15, 20), (12, 20), (24, 36), (28, 42), (30, 45)]


def pair(r, l):
    if l == 0:
        return r.choice(PAIRS0)
    g = r.choice([2, 3, 4, 5, 6, 7, 8, 9])
    a, b = r.sample(range(2, 13 if l == 1 else 17), 2)
    if gcd(a, b) != 1 and l == 2 and r.random() < 0.5:
        pass
    a, b = a * g, b * g
    return (a, b) if a != b else pair(r, l)


# ---------------------------------------------------------------- Resolver problemas
def t_mcm_mcd(r, l):
    a, b = pair(r, l)
    k = r.choice(["mcm", "mcd"])
    ns = [a, b]
    if l == 2 and r.random() < 0.7:
        c = r.choice([x for x in (a // 2, b * 2, a + b, a * 3) if x > 1 and x not in ns and x < 200] or [a * 2])
        ns.append(c)
    from functools import reduce
    g = reduce(gcd, ns)
    m = reduce(lcm, ns)
    val = m if k == "mcm" else g
    lines = [f"{n} = {fstr(n)}" for n in ns]
    fig = card(["Descomposición en primos:"] + lines, 60 + 40 * (len(lines) + 1), 20)
    name = "mínimo común múltiplo (MCM)" if k == "mcm" else "máximo común divisor (MCD)"
    stem = f"Considera los números {', '.join(map(str, ns[:-1]))} y {ns[-1]}. ¿Cuál es su {name}?"
    ans = S(val)
    prod = 1
    for n in ns: prod *= n
    alts = [m if k == "mcd" else g, prod, sum(ns), max(ns) if k == "mcd" else min(ns), val * 2, val // 2 if val % 2 == 0 else val + 2, reduce(lambda x, y: x * y, [gcd(n, ns[0]) for n in ns[1:]], 1) + 1]
    ex = ("El MCM toma cada primo con su mayor exponente" if k == "mcm" else "El MCD toma solo los primos comunes con su menor exponente") + f": {ans}."
    return make(stem, fig, ans, pick4(ans, uq(val, alts)), Q_RES, ex)


def t_count_div(r, l):
    if l == 0:
        n = r.choice([12, 18, 20, 24, 28, 30, 36, 40, 42, 45, 48, 50, 60])
        divs = [d for d in range(1, n + 1) if n % d == 0]
        fig = card([f"Número: {n}", f"Descomposición: {n} = {fstr(n)}"], 120, 20)
        stem = f"¿Cuántos divisores positivos tiene el número {n}?"
        cnt = len(divs)
        alts = [cnt - 1, cnt + 1, cnt + 2, n // 2, len(fact(n)), sum(fact(n).values()) + 1]
        return make(stem, fig, S(cnt), pick4(S(cnt), uq(cnt, alts)), Q_RES, f"Divisores de {n}: " + ", ".join(map(str, divs)) + f" (son {cnt}).")
    p, q = r.sample([2, 3, 5, 7], 2)
    a, b = r.randint(1, 4), r.randint(1, 3)
    n = p ** a * q ** b
    if n > 3000 or (l == 1 and n > 400):
        raise Reject
    cnt = (a + 1) * (b + 1)
    fig = card([f"N = {p}{str(a).translate(SUPS) if a > 1 else ''}·{q}{str(b).translate(SUPS) if b > 1 else ''}", "(descomposición en factores primos)"], 120, 22)
    stem = f"Un número N se descompone como en la figura. ¿Cuántos divisores positivos tiene N?"
    alts = [a + b, a * b, (a + 1) + (b + 1), cnt + a, cnt - 1, cnt + 2, a + b + 2]
    return make(stem, fig, S(cnt), pick4(S(cnt), uq(cnt, alts)), Q_RES, f"Divisores = (a + 1)(b + 1) = {a + 1}·{b + 1} = {cnt}.")


def t_next_multiple(r, l):
    d = r.choice([6, 7, 8, 9, 11, 12, 15, 25] if l == 0 else [12, 15, 16, 18, 24, 35, 45])
    N = r.randint(d + 3, d * 9)
    if N % d == 0:
        raise Reject
    kind = r.choice(["add", "rem"])
    rem = N % d
    fig = card([f"Número: {N}", f"Divisor: {d}"], 130, 22)
    if kind == "add":
        val = d - rem
        stem = f"¿Cuál es el menor número natural que se debe sumar a {N} para obtener un múltiplo de {d}?"
        ex = f"{N} = {d}·{N // d} + {rem}; faltan {d} − {rem} = {val}."
        alts = [rem, d, val + 1, val - 1 if val > 1 else val + 2, N // d, d - rem + d]
    else:
        val = rem
        stem = f"¿Cuál es el resto de dividir {N} por {d}?"
        ex = f"{N} = {d}·{N // d} + {rem}."
        alts = [d - rem, N // d, rem + 1, rem - 1 if rem > 1 else rem + 2, d, N - d]
    return make(stem, fig, S(val), pick4(S(val), uq(val, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_coincide(r, l):
    a, b = pair(r, l)
    m = lcm(a, b)
    if m > 90 or m in (a, b):
        raise Reject
    ctx = r.choice([("Bus A", "Bus B", "pasan por el paradero cada", "min"), ("Luz A", "Luz B", "se encienden cada", "s"), ("Ciclista A", "Ciclista B", "completan una vuelta cada", "min")])
    fig = timeline([(f"{ctx[0]}: cada {a} {ctx[3]}", a), (f"{ctx[1]}: cada {b} {ctx[3]}", b)], max(m - 1, max(a, b)))
    stem = f"Dos eventos parten juntos en el instante 0 y luego {ctx[2]} {a} y {b} {ctx[3]}, respectivamente. ¿Después de cuántos {ctx[3]} vuelven a coincidir por primera vez?"
    ans = f"{m} {ctx[3]}"
    alts = [gcd(a, b), a * b, a + b, m // 2 if m % 2 == 0 else m + a, m + a, m * 2]
    alts = [f"{x} {ctx[3]}" for x in alts if x > 0 and x != m]
    alts = list(dict.fromkeys(alts))
    return make(stem, fig, ans, alts[:4], Q_MOD, f"Se busca el MCM({a}, {b}) = {m}.")


def bar2(a, b, la, lb):
    wa, wb = max(150, 460 * a / max(a, b)), max(150, 460 * b / max(a, b))
    body = R(60, 40, wa, 46, FILL) + tag(60 + wa / 2, 63, f"{la}: {a}", 18)
    body += R(60, 110, wb, 46, FILL2) + tag(60 + wb / 2, 133, f"{lb}: {b}", 18)
    return wrap(560, 190, body, "Cantidades a repartir")


def t_share(r, l):
    a, b = pair(r, l)
    g = gcd(a, b)
    if g < 2 or g in (a, b):
        raise Reject
    items = r.choice([("cuadernos", "lápices"), ("manzanas", "naranjas"), ("hombres", "mujeres"), ("rojos", "azules")])
    which = r.choice(["groups", "each"])
    fig = bar2(a, b, items[0], items[1])
    if which == "groups":
        stem = f"Se tienen {a} {items[0]} y {b} {items[1]}. Se quieren armar la mayor cantidad posible de grupos iguales, sin que sobre ni falte nada. ¿Cuántos grupos se pueden armar?"
        ans = S(g)
        alts = [a + b, lcm(a, b), g * 2 if a % (2 * g) == 0 else g + 1, a // g, b // g, a - b if a > b else b - a, g // 2 if g % 2 == 0 else g + 2]
        ex = f"El número de grupos es el MCD({a}, {b}) = {g}."
    else:
        stem = f"Se tienen {a} {items[0]} y {b} {items[1]}. Se arman la mayor cantidad posible de grupos iguales, sin que sobre nada. ¿Cuántos {items[0]} hay en cada grupo?"
        ans = S(a // g)
        alts = [g, b // g, a, a // g + 1, a // g - 1 if a // g > 1 else a // g + 2, lcm(a, b) // a]
        ex = f"Grupos = MCD = {g}; cada grupo tiene {a}/{g} = {a // g} {items[0]}."
    return make(stem, fig, ans, pick4(ans, uq(int(ans), alts)), Q_MOD, ex)


def t_tiles(r, l):
    a, b = pair(r, l)
    g = gcd(a, b)
    if g < 2 or g in (a, b):
        raise Reject
    big, small = max(a, b), min(a, b)
    ww = 360
    hh = max(50, 360 * small / big)
    hh = min(hh, 200)
    x0 = 280 - ww / 2
    body = R(x0, 30, ww, hh, FILL) + tag(280, 30 + hh + 24, f"{big} cm", 17) + tag(x0 - 44, 30 + hh / 2, f"{small} cm", 17)
    fig = wrap(560, 30 + hh + 60, body, "Rectángulo que se cubre con baldosas")
    A, B = (max(a, b), min(a, b)) if a >= b else (min(a, b), max(a, b))
    stem = f"Un piso rectangular de {max(a, b)} cm por {min(a, b)} cm se cubre con baldosas cuadradas iguales, sin cortarlas ni que sobre espacio. ¿Cuál es la medida del lado de la baldosa más grande posible?"
    ans = f"{g} cm"
    alts = [lcm(a, b), a + b, g * 2, g // 2 if g % 2 == 0 else g + 1, min(a, b), abs(a - b)]
    alts = [f"{x} cm" for x in alts if x > 0 and x != g]
    alts = list(dict.fromkeys(alts))
    return make(stem, fig, ans, alts[:4], Q_MOD, f"El lado debe dividir a ambas medidas: MCD({a}, {b}) = {g}.")


# ---------------------------------------------------------------- Representar
def t_tree(r, l):
    k = 3 if l < 2 else 4
    pool = [2, 2, 3, 3, 5, 7]
    primes = sorted(r.sample(pool, k)) if l < 2 else sorted(r.choices([2, 3, 5], k=k))
    fig, nodes = factor_tree(primes, hide=None)
    N = 1
    for p in primes: N *= p
    # ocultar un nodo distinto de la raíz
    hide = r.randrange(1, len(nodes))
    fig, nodes = factor_tree(primes, hide=hide)
    val = nodes[hide][2]
    stem = "En el árbol de factores de la figura, ¿qué número corresponde al casillero con «?»"
    ans = S(val)
    alts = [val + 1, val * 2, val + 2, N // val if N % val == 0 else val + 3, val - 1 if val > 2 else val + 4, N]
    return make(stem, fig, ans, pick4(ans, uq(val, alts)), Q_REP, f"Cada nodo es el producto de sus dos hijos; el valor pedido es {val}.")


def mult_rows(a, b, n=10, hl=None):
    ca = [a * i for i in range(1, n + 1)]
    cb = [b * i for i in range(1, n + 1)]
    common = set(ca) & set(cb)
    cw = 44
    body = ""
    for row, (lab, vals) in enumerate((("Múltiplos de " + str(a), ca), ("Múltiplos de " + str(b), cb))):
        y = 60 + row * 90
        body += tag(70 + 25, y - 22, lab, 15)
        for i, v in enumerate(vals):
            x = 30 + i * (cw + 4)
            body += R(x, y, cw, 42, FILL2 if v in common else WHITE, NAVY, 2.5) + T(x + cw / 2, y + 28, str(v), 14 if v > 99 else 16)
    return wrap(560, 200, body, "Listas de múltiplos"), sorted(common)


def t_multiples(r, l):
    a, b = pair(r, l)
    if a > 30 or b > 30:
        raise Reject
    fig, common = mult_rows(a, b)
    if not common:
        raise Reject
    m = lcm(a, b)
    kind = r.choice(["first", "count"])
    if kind == "first" or len(common) < 2:
        stem = "En la figura se destacan los múltiplos comunes de dos números. ¿Cuál es el mínimo común múltiplo de ellos?"
        val = common[0]
        ex = f"El menor múltiplo destacado es {val}: MCM({a}, {b}) = {val}."
        alts = [gcd(a, b), a * b, a + b, common[1] if len(common) > 1 else val * 2, max(a, b), val + min(a, b)]
    else:
        stem = "En la figura se destacan los múltiplos comunes que aparecen en ambas listas. ¿Cuántos múltiplos comunes se ven?"
        val = len(common)
        ex = "Se cuentan los casilleros destacados: " + ", ".join(map(str, common)) + "."
        alts = [val + 1, val - 1 if val > 1 else val + 2, val + 2, 10 - val, 1 if val != 1 else 3]
    ans = S(val)
    return make(stem, fig, ans, pick4(ans, uq(val, alts)), Q_REP, ex)


# ---------------------------------------------------------------- Argumentar
TRUE = ["El MCM de dos números es múltiplo de ambos números", "El MCD de dos números divide a ambos números", "El producto de dos números es igual al producto de su MCM por su MCD",
        "Dos números primos distintos tienen MCD igual a 1", "El número 1 no es primo ni compuesto", "El único primo par es el 2",
        "Si a divide a b, entonces el MCD de a y b es a", "Todo múltiplo de 6 es también múltiplo de 3"]
FALSE = ["El MCD de dos números siempre es mayor que su MCM", "El MCM de dos números es siempre igual a su producto", "El número 1 es un número primo",
         "Todo número impar es primo", "Si a divide a b, entonces el MCM de a y b es a", "El MCD de dos números puede ser mayor que el menor de ellos",
         "Todo múltiplo de 3 es también múltiplo de 6", "Un número primo tiene exactamente tres divisores positivos"]


def _card_gen(r):
    a, b = pair(r, 1)
    return card([f"Números: {a} y {b}", f"MCD = {gcd(a, b)}  ·  MCM = {lcm(a, b)}"], 120, 22)


def t_true(r, l):
    stem = r.choice(["Sobre múltiplos, divisores y números primos, ¿cuál de las siguientes afirmaciones es verdadera?", "¿Cuál de las siguientes afirmaciones sobre MCM y MCD es correcta?"])
    return make(stem, _card_gen(r), r.choice(TRUE), r.sample(FALSE, 4), Q_ARG, "Se contrasta cada afirmación con las definiciones de múltiplo, divisor, MCM y MCD.")


def t_false(r, l):
    stem = r.choice(["Sobre múltiplos, divisores y números primos, ¿cuál de las siguientes afirmaciones es FALSA?", "¿Cuál de las siguientes afirmaciones sobre MCM y MCD es incorrecta?"])
    return make(stem, _card_gen(r), r.choice(FALSE), r.sample(TRUE, 4), Q_ARG, "Solo una afirmación contradice las definiciones de MCM, MCD y número primo.")


def t_div_claims(r, l):
    d = r.choice([2, 3, 4, 5, 6, 9, 10])
    rule = {2: "termina en cifra par", 3: "la suma de sus cifras es múltiplo de 3", 4: "sus dos últimas cifras forman un múltiplo de 4", 5: "termina en 0 o 5", 6: "es par y divisible por 3", 9: "la suma de sus cifras es múltiplo de 9", 10: "termina en 0"}[d]
    good = [n for n in range(100, 1000) if n % d == 0]
    bad = [n for n in range(100, 1000) if n % d != 0]
    ask_true = r.random() < 0.5
    if ask_true:
        ans, alts = f"{r.choice(good)} es divisible por {d}", [f"{x} es divisible por {d}" for x in r.sample(bad, 4)]
        stem = f"Se sabe que un número es divisible por {d} si {rule}. ¿Cuál de las siguientes afirmaciones es verdadera?"
    else:
        ans, alts = f"{r.choice(bad)} es divisible por {d}", [f"{x} es divisible por {d}" for x in r.sample(good, 4)]
        stem = f"Se sabe que un número es divisible por {d} si {rule}. ¿Cuál de las siguientes afirmaciones es falsa?"
    fig = card(["Criterio de divisibilidad", f"Por {d}: {rule}"], 130, 19)
    return make(stem, fig, ans, alts, Q_ARG, f"Se aplica el criterio de divisibilidad por {d} a cada número.")


def t_error(r, l):
    a, b = pair(r, 1)
    k = r.randrange(4)
    g, m = gcd(a, b), lcm(a, b)
    if k == 0:
        lines = [f"MCD({a}, {b}) = {m}"]
        ans = "Confundió el MCD con el MCM: dio el menor múltiplo común en vez del mayor divisor común"
        alts = ["Sumó los dos números en lugar de buscar sus divisores comunes en la lista", "Multiplicó los dos números y no simplificó la factorización en primos", "Tomó el mayor de los dos números como resultado sin analizar sus divisores", "Restó los números y usó esa diferencia como el divisor buscado"]
    elif k == 1:
        lines = [f"MCM({a}, {b}) = {g}"]
        ans = "Confundió el MCM con el MCD: dio el mayor divisor común en vez del menor múltiplo común"
        alts = ["Multiplicó los dos números y no lo dividió por su máximo común divisor", "Sumó los dos números y usó esa suma como su múltiplo común más chico", "Tomó el menor de los dos números como su múltiplo común más chico", "Restó los dos números y usó esa diferencia como el múltiplo común buscado"]
    elif k == 2:
        n = r.choice([51, 57, 87, 91])
        lines = [f"{n} es primo porque no es par ni termina en 5"]
        ans = "Un número puede ser compuesto sin ser par ni terminar en 5: basta que tenga otro divisor distinto de 1 y él mismo"
        alts = [f"Todos los números impares mayores que 2 son primos, pero {n} no es impar", "Los primos siempre terminan en 1, 3, 7 o 9, y este número no termina en esas cifras", "El número 1 es primo, y por eso todos sus múltiplos también lo son sin excepción", "Un número es primo solo si su suma de cifras es un número par"]
    else:
        lines = [f"{a} = {fstr(a)}", f"{b} = {fstr(b)}", f"MCD = producto de todos los primos de ambos = {'·'.join(str(p) for p in sorted(list(fact(a)) + list(fact(b))))}"]
        ans = "Para el MCD solo deben tomarse los primos comunes, con su menor exponente, no todos"
        alts = ["Para el MCD deben tomarse todos los primos con su mayor exponente, como en el MCM", "El MCD se obtiene sumando los exponentes de los primos de ambos números", "El MCD se obtiene restando las descomposiciones de ambos números en primos", "No se puede calcular el MCD a partir de la descomposición en factores primos"]
    fig = card(["Resolución de un estudiante:"] + [x.replace("-", "−") for x in lines], 60 + 44 * (len(lines) + 1), 19)
    return make("Observa la resolución de la figura. ¿Cuál es el error del estudiante?", fig, ans, alts, Q_ARG, ans + ".")


BY_SKILL = {
    Q_RES: [t_mcm_mcd, t_count_div, t_next_multiple],
    Q_MOD: [t_coincide, t_share, t_tiles],
    Q_REP: [t_tree, t_multiples],
    Q_ARG: [t_true, t_false, t_div_claims, t_error],
}
