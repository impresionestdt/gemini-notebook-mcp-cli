"""Clase 24 · Permutaciones y combinatorias: orden importa / no importa."""
from collections import Counter
from math import comb, perm, factorial as fac
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
import viz


def nfmt(n):
    return f"{n:,}".replace(",", ".")


def dist(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = nfmt(a) if isinstance(a, int) else a
        if s not in seen and (not isinstance(a, int) or a > 0):
            seen.add(s); out.append(s)
    return out


GROUPS = [("estudiantes", "un comité"), ("profesores", "una comisión"), ("vecinos", "una directiva"), ("jugadores", "una delegación")]
ROLES = [("presidente, vicepresidente y secretario", 3), ("capitán y subcapitán", 2), ("primer y segundo lugar", 2), ("gerente, contador, tesorero y secretario", 4)]
WORDS = ["ANA", "OSO", "MAMA", "PAPA", "SOLO", "LOLA", "ANANA", "CASA", "TATA", "PERRO", "CARRO", "BANANA", "LLAMA", "MOMIA", "PAPAYA", "CARACAS", "ABEJA", "MISISIPI", "ESCALERA", "ABRACADABRA", "MATEMATICA", "COCODRILO", "PARALELA", "CALCULAR"]


def anagrams(w):
    c = Counter(w)
    n = fac(len(w))
    for v in c.values(): n //= fac(v)
    return n


# ---------------------------------------------------------------- Resolver
def t_choose(r, l):
    if l == 0:
        n = r.randint(5, 14)
        who, grp = r.choice(GROUPS)
        if r.random() < 0.5:
            k = r.choice([2, 3, 4])
            stem = f"De un grupo de {n} {who} se debe elegir {grp} de {k} integrantes (sin cargos distintos). ¿De cuántas maneras se puede hacer?"
            cnt = comb(n, k)
            alts = [perm(n, k), n * k, comb(n, k) * k, comb(n + 1, k), fac(n) // fac(k), comb(n, k - 1) if k > 1 else n + 1]
            fig = viz.pick_fig(min(n, 9), list(range(k)), False)
        else:
            role, k = r.choice(ROLES)
            stem = f"De un grupo de {n} {who} se debe elegir {role} (cada cargo lo ocupa una persona distinta). ¿De cuántas maneras se puede hacer?"
            cnt = perm(n, k)
            alts = [comb(n, k), n ** k, fac(n), comb(n, k) * 2, perm(n, k) // 2, perm(n, k) + n]
            fig = viz.pick_fig(min(n, 9), list(range(k)), True)
    elif l == 1:
        n, k = r.choice([(8, 3), (9, 3), (10, 4), (7, 3), (9, 4), (11, 3), (12, 4), (10, 3), (13, 3)])
        who, grp = r.choice(GROUPS)
        kind = r.choice(["incl", "excl"])
        if kind == "incl":
            stem = f"De un grupo de {n} {who} se elige {grp} de {k} integrantes. Si una persona determinada debe estar siempre en {grp.split(' ')[1] if False else 'él'}, ¿de cuántas maneras se puede elegir?".replace("debe estar siempre en él", "debe formar parte del grupo elegido")
            cnt = comb(n - 1, k - 1)
            alts = [comb(n, k), comb(n - 1, k), perm(n - 1, k - 1), comb(n, k) - comb(n - 1, k - 1), comb(n - 2, k - 2) if k > 2 else 1, comb(n, k - 1)]
        else:
            stem = f"De un grupo de {n} {who} se elige {grp} de {k} integrantes. Si dos personas determinadas NO pueden formar parte del mismo grupo elegido a la vez, ¿de cuántas maneras se puede elegir?"
            cnt = comb(n, k) - comb(n - 2, k - 2)
            alts = [comb(n, k), comb(n - 2, k - 2), comb(n - 2, k), comb(n, k) - comb(n - 2, k), comb(n, k) - 2 * comb(n - 2, k - 2), comb(n - 2, k) + 2]
        fig = card([f"n = {n}, k = {k}", "Cuenta los casos válidos: total − excluidos" if kind == "excl" else "Fija a la persona y elige al resto"], 190, 22)
    else:
        a, b = r.choice([(5, 4), (6, 4), (6, 5), (7, 5), (8, 6), (7, 4), (9, 5)])
        i, j = r.choice([(2, 2), (3, 2), (2, 3), (3, 3), (1, 2), (2, 1)])
        if i > a or j > b: raise Reject
        stem = f"Un curso tiene {a} hombres y {b} mujeres. ¿De cuántas maneras se puede formar una comisión de {i} hombres y {j} mujeres?"
        cnt = comb(a, i) * comb(b, j)
        alts = [comb(a, i) + comb(b, j), comb(a + b, i + j), perm(a, i) * perm(b, j), comb(a, i) * comb(b, j) * 2, comb(a, j) * comb(b, i) if j <= a and i <= b else cnt + 1, cnt // 2]
        fig = card([f"{a} hombres → elegir {i}", f"{b} mujeres → elegir {j}", "Total = C(a, i) · C(b, j)"], 210, 21)
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_RES, f"Se usa combinación cuando el orden no importa y permutación cuando sí importa: {ans}.")


def t_anagram(r, l):
    pool = [w for w in WORDS if (len(w) <= 5 if l == 0 else len(w) <= 8 if l == 1 else True)]
    w = r.choice(pool)
    if l < 2:
        stem = f"¿Cuántas ordenaciones distintas (con o sin sentido) se pueden formar con todas las letras de la palabra {w}?"
        cnt = anagrams(w)
        c = Counter(w)
        rep = [v for v in c.values() if v > 1]
        alts = [fac(len(w)), fac(len(w)) // (max(rep) if rep else 2), cnt * 2, cnt // 2 if cnt % 2 == 0 else cnt + 1, len(w) ** 2, cnt + len(w)]
        ex = f"{len(w)}! dividido por el factorial de cada letra repetida: {nfmt(cnt)}."
    else:
        v = [ch for ch in w if ch in "AEIOU"]
        if not v: raise Reject
        first = r.choice(sorted(set(v)))
        rest = list(w); rest.remove(first)
        cnt = anagrams("".join(rest))
        stem = f"¿Cuántas ordenaciones distintas de las letras de {w} comienzan con la letra {first}?"
        alts = [anagrams(w), fac(len(w) - 1), cnt * Counter(w)[first], cnt // 2 if cnt % 2 == 0 else cnt + 1, anagrams(w) // len(w), cnt + 1]
        ex = f"Se fija la {first} al inicio y se ordenan las {len(w) - 1} letras restantes: {nfmt(cnt)}."
    ans = nfmt(cnt)
    fig = viz.slots_fig([(ch, "×") for ch in w[:7]], ops=" ") if False else card([f"Palabra: {w}", "n! / (a! · b! · …)"], 190, 24)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_context(r, l):
    if l == 0:
        n = r.randint(6, 16)
        kind = r.choice(["hand", "match", "match2"])
        if kind == "hand":
            stem = f"En una reunión hay {n} personas y cada persona saluda de mano exactamente una vez a cada una de las otras. ¿Cuántos saludos hay en total?"
            cnt = comb(n, 2)
            alts = [n * (n - 1), n * n, fac(n), n, comb(n, 2) + n, n * (n - 1) // 4 if n % 4 == 0 else cnt + 2]
        elif kind == "match":
            stem = f"En un campeonato juegan {n} equipos, todos contra todos una sola vez. ¿Cuántos partidos se juegan?"
            cnt = comb(n, 2)
            alts = [n * (n - 1), n * n, n, comb(n, 2) * 2, fac(n), comb(n, 3)]
        else:
            stem = f"En un campeonato juegan {n} equipos, todos contra todos en dos rondas (ida y vuelta). ¿Cuántos partidos se juegan?"
            cnt = perm(n, 2)
            alts = [comb(n, 2), n * n, 2 * n, n * (n - 1) // 2 + n, fac(n), perm(n, 2) + n]
        fig = viz.pick_fig(min(n, 9), [0, 1], kind == "match2")
    elif l == 1:
        n = r.randint(6, 14)
        k = r.choice([2, 3])
        what = r.choice(["sabores de helado distintos", "libros distintos", "frutas distintas"])
        stem = f"En una tienda hay {n} {what}. ¿De cuántas maneras se pueden elegir {k} de ellos si no importa el orden de elección?"
        cnt = comb(n, k)
        alts = [perm(n, k), n * k, n ** k, fac(k), comb(n, k) * k, comb(n + 1, k)]
        fig = viz.pick_fig(min(n, 9), list(range(k)), False)
    else:
        n = r.randint(6, 16)
        kind = r.choice(["diag", "tri", "lot"])
        if kind == "diag":
            stem = f"¿Cuántas diagonales tiene un polígono convexo de {n} lados?"
            cnt = comb(n, 2) - n
            alts = [comb(n, 2), n * (n - 3), perm(n, 2) - n, comb(n, 2) + n, n - 3, comb(n, 3)]
            fig = card([f"{n} vértices", "Segmentos entre pares de vértices − lados"], 190, 22)
        elif kind == "tri":
            stem = f"Se marcan {n} puntos sobre una circunferencia, de modo que no hay tres colineales. ¿Cuántos triángulos distintos se pueden formar con ellos como vértices?"
            cnt = comb(n, 3)
            alts = [perm(n, 3), comb(n, 2), n * 3, comb(n, 3) * 2, comb(n, 3) - n, comb(n + 1, 3)]
            fig = card([f"{n} puntos en una circunferencia", "Cada terna de puntos forma un triángulo"], 190, 22)
        else:
            m, k = r.choice([(20, 3), (25, 4), (30, 3), (15, 4), (20, 4), (35, 3)])
            stem = f"En un sorteo se eligen {k} números distintos entre {m} (sin importar el orden). ¿Cuántas combinaciones posibles hay?"
            cnt = comb(m, k)
            alts = [perm(m, k), m ** k, comb(m, k) * k, comb(m, k - 1), comb(m + 1, k), fac(k)]
            fig = card([f"{k} números de entre {m}", "El orden no importa"], 190, 22)
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_MOD, f"Resultado: {ans}.")


def t_lottery(r, l):
    if l == 0:
        n, k = r.choice([(5, 2), (6, 2), (6, 3), (7, 3), (8, 2), (9, 2), (10, 2), (7, 2), (8, 3), (9, 3), (10, 3)])
        stem = f"De un total de {n} ciudades se eligen {k} para visitar en un viaje, sin importar el orden. ¿Cuántas elecciones distintas existen?"
        cnt = comb(n, k)
        alts = [perm(n, k), n ** k, fac(n), comb(n + 1, k), cnt + n, cnt * 2]
    elif l == 1:
        n, k = r.choice([(10, 3), (12, 3), (12, 4), (9, 4), (11, 4), (10, 4), (13, 3), (14, 3), (8, 4)])
        stem = f"De {n} candidatos se eligen {k} para el podio y se indica el orden de llegada (1.º, 2.º, …). ¿Cuántos podios distintos son posibles?"
        cnt = perm(n, k)
        alts = [comb(n, k), n ** k, fac(n), perm(n, k) // 2, comb(n, k) * 2, perm(n, k) + n]
    else:
        n, k, m = r.choice([(10, 4, 2), (12, 4, 2), (9, 5, 3), (11, 5, 2), (10, 5, 3), (12, 5, 3)])
        stem = f"De {n} personas se elige un grupo de {k}, y de ese grupo se designa a {m} con cargos distintos (el orden de los cargos importa). ¿De cuántas maneras se puede hacer todo el proceso?"
        cnt = comb(n, k) * perm(k, m)
        alts = [perm(n, k), comb(n, k) * comb(k, m), comb(n, k) + perm(k, m), perm(n, m), comb(n, m) * comb(n, k), cnt // 2]
    ans = nfmt(cnt)
    fig = card([f"n = {n}", f"k = {k}", "¿Importa el orden?" if l < 2 else "Primero elegir, luego ordenar"], 210, 22)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_MOD, f"Resultado: {ans}.")


# ---------------------------------------------------------------- Representar
def t_which_formula(r, l):
    n = r.randint(6, 12)
    k = r.choice([2, 3, 4])
    ordered = r.random() < 0.5
    chosen = list(range(k))
    fig = viz.pick_fig(min(n, 9), chosen, ordered)
    if l == 0:
        good = f"P({n}, {k})" if ordered else f"C({n}, {k})"
        pool = [f"P({n}, {k})", f"C({n}, {k})", f"{n}^{k}", f"{n}!", f"C({n}, {k}) / {k}!"]
        stem = f"La figura muestra una elección de {k} elementos entre {n}. ¿Qué expresión da el número de elecciones posibles del tipo mostrado?"
    elif l == 1:
        good = f"{n}!/({n - k})!" if ordered else f"{n}!/({k}!·({n - k})!)"
        pool = [f"{n}!/({n - k})!", f"{n}!/({k}!·({n - k})!)", f"{n}!/{k}!", f"{n}!·{k}!", f"({n - k})!/{n}!"]
        stem = f"La figura muestra una elección de {k} elementos entre {n}. ¿Qué expresión con factoriales da el número de elecciones posibles del tipo mostrado?"
    else:
        good = f"C({n}, {k}) · {k}!" if ordered else f"C({n}, {k})"
        pool = [f"C({n}, {k}) · {k}!", f"C({n}, {k})", f"C({n}, {k}) / {k}!", f"P({n}, {k}) · {k}!", f"{n}^{k}"]
        stem = f"La figura muestra una elección de {k} elementos entre {n}. ¿Cuál expresión da el número de elecciones posibles del tipo mostrado?"
        if ordered:
            pool = [p for p in pool]
    cs = [p for p in pool if p != good]
    r.shuffle(cs)
    return make(stem, fig, good, cs, Q_REP, "Si el orden importa se usa permutación n!/(n − k)!; si no importa, combinación n!/(k!(n − k)!).")


def t_pascal(r, l):
    rows = r.choice([6, 7, 8])
    if l == 0:
        n = r.randint(2, rows - 1); k = r.randint(1, n - 1)
        hide = (n, k)
        stem = "En el triángulo de Pascal de la figura falta un valor (marcado con «?»). ¿Cuál es ese valor?"
        cnt = comb(n, k)
        alts = [comb(n - 1, k) + comb(n - 1, k) if False else comb(n - 1, k), comb(n - 1, k - 1), cnt + 1, cnt - 1, comb(n, k) * 2, comb(n - 1, k) * comb(n - 1, k - 1)]
        fig = viz.pascal_fig(rows, hide)
    elif l == 1:
        n = r.randint(4, rows - 1); k = r.randint(2, n - 2) if n >= 4 else 1
        stem = f"En el triángulo de Pascal, la fila {n} (la primera fila es la fila 0) contiene los valores de C({n}, k). ¿Cuánto vale C({n}, {k})?"
        cnt = comb(n, k)
        alts = [comb(n, k - 1), comb(n, k + 1) if k + 1 <= n else cnt + 2, perm(n, k), 2 ** n, cnt + n, cnt - 1]
        fig = viz.pascal_fig(rows, None, [(n, k)])
    else:
        n = r.randint(4, rows - 1)
        stem = f"En el triángulo de Pascal de la figura, ¿cuál es la suma de todos los números de la fila {n} (la primera fila es la fila 0)?"
        cnt = 2 ** n
        alts = [n * n, n ** 2 + 1, comb(2 * n, n) if comb(2 * n, n) != cnt else cnt + 2, 2 ** (n + 1), 2 ** (n - 1), fac(n)]
        fig = viz.pascal_fig(rows, None, [(n, k) for k in range(n + 1)])
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_REP, "Cada número es la suma de los dos que tiene encima; la fila n contiene los C(n, k) y suma 2ⁿ.")


# ---------------------------------------------------------------- Argumentar
TRUE_P = ["C(n, k) = C(n, n − k)", "P(n, k) = C(n, k) · k!", "C(n, 0) = 1", "C(n, k) + C(n, k + 1) = C(n + 1, k + 1)", "En una permutación el orden de los elementos elegidos importa",
          "La suma de los números de la fila n del triángulo de Pascal es 2ⁿ"]
FALSE_P = ["P(n, k) = C(n, k)", "C(5, 2) = C(5, 4)", "C(n, k) siempre es mayor que P(n, k)", "n!/(n − k)! cuenta las selecciones en las que el orden no importa", "C(n, 1) = 1",
           "Con las letras de MAMA se pueden formar 4! ordenaciones distintas", "C(n, k) = n!/(n − k)!"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_P), r.sample(FALSE_P, 4)
        stem = "Sobre permutaciones y combinaciones, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_P), r.sample(TRUE_P, 4)
        stem = "Sobre permutaciones y combinaciones, ¿cuál de las siguientes afirmaciones es FALSA?"
    fig = viz.pascal_fig(r.choice([5, 6, 7]))
    return make(stem, fig, good, bad, Q_ARG, "Se razona con las definiciones y con el triángulo de Pascal.")


def t_order(r, l):
    n = r.randint(6, 14); k = r.choice([2, 3, 4])
    cases = [(f"Elegir {k} representantes de un curso de {n} estudiantes, todos con el mismo rol", False),
             (f"Elegir de un curso de {n} estudiantes a un presidente, un secretario y un tesorero" if k == 3 else f"Elegir de un curso de {n} estudiantes a {k} personas con cargos distintos", True),
             (f"Elegir {k} libros para llevar de vacaciones, entre {n} disponibles", False),
             (f"Definir el podio de {k} lugares en una carrera con {n} corredores", True)]
    desc, ordered = r.choice(cases)
    if l == 0:
        stem = f"{desc}. ¿Qué expresión da el número de formas de hacerlo?"
        good = f"P({n}, {k})" if ordered else f"C({n}, {k})"
        pool = [f"P({n}, {k})", f"C({n}, {k})", f"{n}^{k}", f"{n}!", f"C({n}, {k}) / {k}!"]
    else:
        stem = f"{desc}. ¿Cuál afirmación justifica correctamente el cálculo?"
        if ordered:
            good = f"Se usa una permutación P({n}, {k}), porque el orden (o el cargo) sí importa"
            pool = [good, f"Se usa una combinación C({n}, {k}), porque el orden (o el cargo) sí importa", f"Se usa una permutación P({n}, {k}), porque el orden no importa", f"Se usa {n}!, porque se ordenan todos los elementos", f"Se usa {n}^{k}, porque los elementos se pueden repetir"]
        else:
            good = f"Se usa una combinación C({n}, {k}), porque el orden no importa"
            pool = [good, f"Se usa una permutación P({n}, {k}), porque el orden no importa", f"Se usa una combinación C({n}, {k}), porque el orden sí importa", f"Se usa {n}!, porque se ordenan todos los elementos", f"Se usa {n}^{k}, porque los elementos se pueden repetir"]
    cs = [p for p in pool if p != good]
    fig = viz.pick_fig(min(n, 9), list(range(k)), ordered)
    return make(stem, fig, good, cs, Q_ARG, "Si el orden (o el cargo) importa, permutación; si no, combinación.")


ERR = ["Usó permutaciones aunque el orden no importa", "Usó combinaciones aunque el orden sí importa", "No dividió por el factorial de las letras repetidas", "Calculó n! en lugar de n!/(n − k)!",
       "Olvidó multiplicar por las formas de elegir el otro grupo"]


def t_error(r, l):
    n = r.randint(6, 10)
    k = r.choice([3, 4])
    kk = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    if kk == 0:
        lines = [f"Elegir un comité de {k} personas entre {n} (sin cargos)", f"Total = {n}·{n - 1}·{n - 2}" + ("·" + str(n - 3) if k == 4 else "") + f" = {nfmt(perm(n, k))}"]
    elif kk == 1:
        lines = [f"Podio de {k} lugares entre {n} corredores", f"Total = C({n}, {k}) = {nfmt(comb(n, k))}"]
    elif kk == 2:
        w = r.choice(["MAMA", "PAPA", "TATA", "OSO"])
        lines = [f"Ordenaciones de las letras de {w}", f"Total = {len(w)}! = {fac(len(w))}"]
    elif kk == 3:
        lines = [f"Elegir presidente, secretario y tesorero entre {n}", f"Total = {n}! = {nfmt(fac(n))}"]
    else:
        a, b = r.choice([(5, 4), (6, 4), (6, 5)])
        lines = [f"Comisión de 3 hombres (de {a}) y 2 mujeres (de {b})", f"Total = C({a}, 3) = {nfmt(comb(a, 3))}"]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 190, 19), ERR[kk], [x for i, x in enumerate(ERR) if i != kk], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[kk].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_eval(r, l):
    if l == 0:
        n = r.randint(5, 14); k = r.choice([2, 3, 4])
        which = r.choice(["C", "P"])
        cnt = comb(n, k) if which == "C" else perm(n, k)
        stem = f"¿Cuánto vale {which}({n}, {k})?"
        alts = [perm(n, k) if which == "C" else comb(n, k), n * k, fac(n) // fac(k), comb(n + 1, k), cnt + n, cnt * 2]
        fig = card([f"{which}({n}, {k})", "P(n, k) = n!/(n − k)!" if which == "P" else "C(n, k) = n!/(k!(n − k)!)"], 190, 24)
    elif l == 1:
        n = r.randint(6, 20)
        kind = r.choice(["c2", "c_sym"])
        if kind == "c2":
            stem = f"¿Cuánto vale C({n}, 2)?"
            cnt = comb(n, 2)
            alts = [perm(n, 2), n * 2, n * n, comb(n, 3), cnt + n, cnt - n]
            fig = card([f"C({n}, 2)", "C(n, 2) = n(n − 1)/2"], 190, 24)
        else:
            k = r.randint(2, 4)
            stem = f"Sabiendo que C({n}, {k}) = {nfmt(comb(n, k))}, ¿cuánto vale C({n}, {n - k})?"
            cnt = comb(n, n - k)
            alts = [perm(n, k), comb(n, k + 1), comb(n, k) * 2, comb(n - 1, k), comb(n, k) - 1, comb(n, n - k) + n]
            fig = card([f"C({n}, {k}) = {nfmt(comb(n, k))}", "C(n, k) = C(n, n − k)"], 190, 24)
    else:
        n = r.randint(5, 20)
        kind = r.choice(["c2", "p2"])
        if kind == "c2":
            val = comb(n, 2)
            stem = f"Si C(n, 2) = {val}, ¿cuánto vale n?"
            fig = card([f"C(n, 2) = {val}", "n(n − 1)/2 = " + str(val)], 190, 24)
        else:
            val = perm(n, 2)
            stem = f"Si P(n, 2) = {val}, ¿cuánto vale n?"
            fig = card([f"P(n, 2) = {val}", "n(n − 1) = " + str(val)], 190, 24)
        cnt = n
        alts = [n - 1, n + 1, val // 2, n + 2, n * 2, val]
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_PRO, f"Resultado: {ans}.")


def t_count_words(r, l):
    if l == 0:
        digs = r.choice(["1, 1, 2", "1, 2, 2", "3, 3, 5", "4, 4, 7", "2, 2, 6", "7, 7, 8"])
        ds = [int(x) for x in digs.split(", ")]
        stem = f"¿Cuántos números distintos de 3 cifras se pueden formar usando exactamente los dígitos {digs}?"
        cnt = anagrams("".join(map(str, ds)))
        alts = [fac(3), 3 * 3, 6, cnt + 1, cnt * 2, 9]
    elif l == 1:
        digs = r.choice(["1, 1, 2, 2", "1, 1, 1, 2", "2, 2, 3, 3", "1, 2, 2, 2", "4, 4, 5, 5", "3, 3, 3, 7", "1, 1, 2, 3", "5, 5, 6, 7"])
        ds = [int(x) for x in digs.split(", ")]
        stem = f"¿Cuántos números distintos de 4 cifras se pueden formar usando exactamente los dígitos {digs}?"
        cnt = anagrams("".join(map(str, ds)))
        alts = [fac(4), fac(4) // 2, cnt + 2, cnt * 2, 4 * 4, cnt - 1]
    else:
        w = r.choice(["BANANA", "PAPAYA", "CARACAS", "MISISIPI", "ESCALERA", "ABRACADABRA", "MATEMATICA"])
        cons = [ch for ch in w if ch not in "AEIOU"]
        v = [ch for ch in w if ch in "AEIOU"]
        # las vocales van todas juntas al comienzo, luego las consonantes
        cnt = anagrams("".join(v)) * anagrams("".join(cons))
        stem = f"¿Cuántas ordenaciones distintas de las letras de {w} tienen todas sus vocales al comienzo y todas sus consonantes al final?"
        alts = [anagrams(w), fac(len(v)) * fac(len(cons)), cnt * 2, cnt // 2 if cnt % 2 == 0 else cnt + 1, anagrams("".join(v)) + anagrams("".join(cons)), cnt + len(w)]
    ans = nfmt(cnt)
    fig = card([stem.split(". ")[0][:60], "n!/(a!·b!·…)"], 190, 20) if False else card(["Permutaciones con repetición", "n! / (a! · b! · …)"], 190, 24)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_PRO, f"Resultado: {ans}.")


BY_SKILL = {
    Q_RES: [t_choose, t_anagram],
    Q_MOD: [t_context, t_lottery],
    Q_REP: [t_which_formula, t_pascal],
    Q_ARG: [t_props, t_order, t_error],
    Q_PRO: [t_eval, t_count_words],
}
