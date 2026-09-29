"""Clase 25 · Probabilidad condicional: tablas de doble entrada y espacio muestral reducido."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
import viz

CATS = [(("Mujeres", "Hombres"), ("Deporte", "Arte")), (("Primero", "Segundo"), ("Aprobó", "Reprobó")), (("Fumadores", "No fumadores"), ("Enfermos", "Sanos")),
        (("Socios", "No socios"), ("Compró", "No compró")), (("Urbanos", "Rurales"), ("Bus", "Auto")), (("Niños", "Adultos"), ("Té", "Café"))]


def pct(x):
    return f"{float(F(x) * 100):.2f}".rstrip("0").rstrip(".").replace(".", ",") + "%"


def fr(x):
    return fs(F(x))


def cnt_table(r, l, target_den=None):
    while True:
        a, b, c, d = (r.randint(3, 25) for _ in range(4))
        if a + b + c + d <= 100 and len({a, b, c, d}) >= 3:
            return [[a, b], [c, d]]


def dist(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = fr(a) if not isinstance(a, str) else a
        if s not in seen:
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver
def t_table_cond(r, l):
    (rl, cl) = r.choice(CATS)
    cells = cnt_table(r, l)
    a, b = cells[0]; c, d = cells[1]
    N = a + b + c + d
    r1, r2 = a + b, c + d
    c1, c2 = a + c, b + d
    i, j = r.randrange(2), r.randrange(2)
    given_row = r.random() < 0.5
    num = cells[i][j]
    if l == 0:
        if given_row:
            den = cells[i][0] + cells[i][1]
            stem = f"La tabla muestra los resultados de una encuesta a {N} personas. Si se elige una persona al azar y resulta ser de la categoría «{rl[i]}», ¿cuál es la probabilidad de que sea de la categoría «{cl[j]}»?"
            alts = [F(num, N), F(num, cells[0][j] + cells[1][j]), F(den, N), F(num, N - den), F(num, cells[1 - i][j]) if cells[1 - i][j] else F(1, 2), F(cells[i][1 - j], den)]
            hlden = dict(hl_den_row=i)
        else:
            den = cells[0][j] + cells[1][j]
            stem = f"La tabla muestra los resultados de una encuesta a {N} personas. Si se elige una persona al azar y resulta ser de la categoría «{cl[j]}», ¿cuál es la probabilidad de que sea de la categoría «{rl[i]}»?"
            alts = [F(num, N), F(num, cells[i][0] + cells[i][1]), F(den, N), F(num, N - den), F(num, cells[i][1 - j]) if cells[i][1 - j] else F(1, 2), F(cells[1 - i][j], den)]
            hlden = dict(hl_den_col=j)
        ans = fr(F(num, den))
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(i, j)], **hlden)
        ex = f"Espacio muestral reducido: {den} casos; favorables: {num}. Probabilidad = {num}/{den} = {ans}."
    elif l == 1:
        # dado que NO es ...
        jj = 1 - j
        den = cells[0][jj] + cells[1][jj]
        num = cells[i][jj]
        stem = f"La tabla muestra los resultados de una encuesta. Si se elige una persona al azar y NO es de la categoría «{cl[j]}», ¿cuál es la probabilidad de que sea de la categoría «{rl[i]}»?"
        ans = fr(F(num, den))
        alts = [F(cells[i][j], cells[0][j] + cells[1][j]), F(num, N), F(den, N), F(cells[i][j], N), F(num, N - den), F(num + cells[i][j], N)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(i, jj)], hl_den_col=jj)
        ex = f"Se reduce el espacio muestral a la columna «{cl[jj]}» ({den} casos): {num}/{den} = {ans}."
    else:
        # tabla con casilla oculta y total dado
        hi, hj = r.randrange(2), r.randrange(2)
        shown = [row[:] for row in cells]
        stem = f"En la tabla falta el número de la casilla marcada con «?». Si se elige al azar a una persona de la categoría «{rl[0]}», ¿cuál es la probabilidad de que sea de la categoría «{cl[0]}»?"
        num0, den0 = cells[0][0], cells[0][0] + cells[0][1]
        ans = fr(F(num0, den0))
        alts = [F(num0, N), F(cells[0][0], c1), F(den0, N), F(cells[0][1], den0), F(num0, N - den0), F(cells[1][0], r2)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(0, 0)], hl_den_row=0, hide=(1, 1) if False else None)
        ex = f"Se usa solo la fila «{rl[0]}»: {num0}/{den0} = {ans}."
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


def t_urn(r, l):
    rr, bb = r.randint(2, 9), r.randint(2, 9)
    gg = r.randint(1, 5) if l == 2 else 0
    N = rr + bb + gg
    counts = [("rojas", rr), ("azules", bb)] + ([("verdes", gg)] if gg else [])
    if l == 0:
        stem = f"Una urna tiene {rr} bolitas rojas y {bb} azules. Se extraen dos bolitas, una tras otra y sin devolución. Si la primera fue roja, ¿cuál es la probabilidad de que la segunda también sea roja?"
        ans = fr(F(rr - 1, N - 1))
        alts = [F(rr, N), F(rr, N - 1), F(rr - 1, N), F(rr * (rr - 1), N * (N - 1)), F(bb, N - 1), F(rr + 1, N + 1)]
        ex = f"Quedan {rr - 1} rojas entre {N - 1} bolitas: {rr - 1}/{N - 1}."
    elif l == 1:
        stem = f"Una urna tiene {rr} bolitas rojas y {bb} azules. Se extraen dos bolitas, una tras otra y sin devolución. ¿Cuál es la probabilidad de que ambas sean rojas?"
        ans = fr(F(rr * (rr - 1), N * (N - 1)))
        alts = [F(rr * rr, N * N), F(rr - 1, N - 1), F(rr, N), F(rr * (rr - 1), N * N), F(2 * rr, N + N - 1), F(rr, N) + F(rr - 1, N - 1)]
        ex = f"P(1.ª roja) · P(2.ª roja | 1.ª roja) = {rr}/{N} · {rr - 1}/{N - 1} = {ans}."
    else:
        stem = f"Una urna tiene {rr} bolitas rojas, {bb} azules y {gg} verdes. Se extraen dos bolitas sin devolución. Si la segunda fue azul, ¿cuál es la probabilidad de que la primera haya sido roja?"
        ans = fr(F(rr, N - 1))
        alts = [F(rr, N), F(rr, N - bb), F(rr * bb, N * (N - 1)), F(bb, N - 1), F(rr - 1, N - 1), F(rr, N - 2)]
        ex = f"P(1.ª roja y 2.ª azul) = {rr}/{N}·{bb}/{N - 1}; P(2.ª azul) = {bb}/{N}; cociente = {rr}/{N - 1}."
    fig = viz.urn_fig(counts)
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_tree_ctx(r, l):
    p1 = r.choice([20, 30, 40, 50, 60, 25, 35])
    p2 = 100 - p1
    d1, d2 = r.choice([1, 2, 3, 4, 5]), r.choice([1, 2, 3, 4, 5, 6])
    if d1 == d2: d2 = d1 + 1
    a1, a2 = F(p1 * d1, 100), F(p2 * d2, 100)      # % de la población total
    tot = a1 + a2
    first = [("Máq. A", f"{p1}%"), ("Máq. B", f"{p2}%")]
    second = [[("defectuosa", f"{d1}%"), ("buena", f"{100 - d1}%")], [("defectuosa", f"{d2}%"), ("buena", f"{100 - d2}%")]]
    fig = viz.ptree_fig(first, second)
    if l == 0:
        stem = f"En una fábrica, la máquina A produce el {p1}% de las piezas y la B el {p2}%. El {d1}% de las piezas de A y el {d2}% de las de B salen defectuosas. Se elige una pieza al azar: ¿cuál es la probabilidad de que sea de la máquina A y defectuosa?"
        ans = pct(F(p1 * d1, 10000))
        alts = [pct(F(d1, 100)), pct(F(p1, 100)), pct(F(p1 + d1, 100)), pct(F(p2 * d2, 10000)), pct(F(p1 * d1, 100 * 100) * 2), pct(F(d1 * d2, 10000))]
        ex = f"P(A ∩ defectuosa) = {p1}%·{d1}% = {ans}."
    elif l == 1:
        stem = f"En una fábrica, la máquina A produce el {p1}% de las piezas y la B el {p2}%. El {d1}% de las piezas de A y el {d2}% de las de B salen defectuosas. Se elige una pieza al azar: ¿cuál es la probabilidad de que sea defectuosa?"
        ans = pct(tot / 100)
        alts = [pct(F(d1 + d2, 200)), pct(F(d1 + d2, 100)), pct(F(p1 * d1, 10000)), pct(F(p2 * d2, 10000)), pct(F(d1 * d2, 10000)), pct(F(p1 * d1 + p2 * d2, 10000) + F(1, 100))]
        ex = f"P(D) = {p1}%·{d1}% + {p2}%·{d2}% = {ans}."
    else:
        stem = f"En una fábrica, la máquina A produce el {p1}% de las piezas y la B el {p2}%. El {d1}% de las piezas de A y el {d2}% de las de B salen defectuosas. Se elige una pieza al azar y resulta defectuosa. ¿Cuál es la probabilidad de que provenga de la máquina A?"
        num, den = p1 * d1, p1 * d1 + p2 * d2
        ans = fr(F(num, den))
        alts = [F(p1, 100), F(d1, 100), F(p2 * d2, den), F(num, 10000), F(p1, p1 + p2 * d2 // 1 if False else p1 + p2), F(num, den + 1)]
        ex = f"P(A | D) = {p1}·{d1} / ({p1}·{d1} + {p2}·{d2}) = {num}/{den} = {ans}."
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def t_survey(r, l):
    (rl, cl) = r.choice(CATS)
    tot = r.choice([20, 25, 40, 50, 80, 100])
    while True:
        a = r.randint(2, tot // 3); b = r.randint(2, tot // 3); c = r.randint(2, tot // 3)
        d = tot - a - b - c
        if d >= 2: break
    cells = [[a, b], [c, d]]
    N = tot
    if l == 0:
        den = a + b
        stem = f"En una encuesta a {N} personas se obtuvo la tabla mostrada. ¿Qué porcentaje de las personas de la categoría «{rl[0]}» pertenece a la categoría «{cl[0]}»?"
        ans = pct(F(a, den))
        alts = [pct(F(a, N)), pct(F(a, a + c)), pct(F(den, N)), pct(F(b, den)), pct(F(a, b)) if a < b else pct(F(a, den + b)), pct(F(a + d, N))]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(0, 0)], hl_den_row=0)
        ex = f"{a}/{den} = {ans}."
    elif l == 1:
        den = b + d
        stem = f"En una encuesta a {N} personas se obtuvo la tabla mostrada. Entre quienes pertenecen a la categoría «{cl[1]}», ¿qué porcentaje pertenece a la categoría «{rl[1]}»?"
        ans = pct(F(d, den))
        alts = [pct(F(d, N)), pct(F(d, c + d)), pct(F(den, N)), pct(F(b, den)), pct(F(d, b)) if d < b else pct(F(d, den + b)), pct(F(b + d, N) / 2)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(1, 1)], hl_den_col=1)
        ex = f"{d}/{den} = {ans}."
    else:
        pa, pb = r.choice([(60, 40), (50, 30), (80, 50), (70, 40), (40, 20), (60, 30)])
        pi = r.choice([x for x in (10, 12, 15, 20, 24, 25, 30) if x <= min(pa, pb)])
        stem = f"En un colegio, el {pa}% de los estudiantes practica un deporte (D), el {pb}% toca un instrumento (I) y el {pi}% hace ambas cosas. Si se elige a un estudiante que toca un instrumento, ¿cuál es la probabilidad de que también practique un deporte?"
        ans = fr(F(pi, pb))
        alts = [F(pi, pa), F(pi, 100), F(pa, 100), F(pi, pa + pb), F(pa + pb - pi, 100), F(pi, pb + 5)]
        fig = card([f"P(D) = {pa}%", f"P(I) = {pb}%", f"P(D ∩ I) = {pi}%"], 210, 22)
        ex = f"P(D | I) = P(D ∩ I)/P(I) = {pi}/{pb} = {ans}."
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_cells_to_prob(r, l):
    (rl, cl) = r.choice(CATS)
    cells = cnt_table(r, l)
    i, j = r.randrange(2), r.randrange(2)
    A = f"«{rl[i]}»"; B = f"«{cl[j]}»"
    kind = r.choice(["A|B", "B|A"]) if l else "A|B"
    if kind == "A|B":
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(i, j)], hl_den_col=j)
        good = f"P({rl[i]} | {cl[j]})"
        sec = f"P({cl[j]} | {rl[i]})"
    else:
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(i, j)], hl_den_row=i)
        good = f"P({cl[j]} | {rl[i]})"
        sec = f"P({rl[i]} | {cl[j]})"
    pool = [good, sec, f"P({rl[i]} ∩ {cl[j]})", f"P({rl[i]} ∪ {cl[j]})", f"P({rl[i]})" if kind == "A|B" else f"P({cl[j]})"]
    if l == 2:
        pool[4] = f"P({rl[i]}) · P({cl[j]})"
    cs = [p for p in pool if p != good]
    stem = "En la tabla, la casilla naranja es el numerador y la fila o columna azul es el total considerado (denominador). ¿Qué probabilidad se calcula con esas casillas?"
    return make(stem, fig, good, cs, Q_REP, "El denominador es el total de la condición (espacio muestral reducido) y el numerador, los casos de la intersección.")


def t_read_tree(r, l):
    p1 = r.choice([F(1, 2), F(1, 3), F(2, 5), F(3, 5), F(1, 4), F(3, 4), F(2, 3)])
    q1, q2 = r.choice([(F(1, 5), F(3, 10)), (F(1, 4), F(1, 2)), (F(2, 3), F(1, 3)), (F(3, 4), F(1, 5)), (F(1, 10), F(2, 5)), (F(2, 5), F(3, 5))])
    first = [("A", fr(p1)), ("B", fr(1 - p1))]
    second = [[("S", fr(q1)), ("no S", fr(1 - q1))], [("S", fr(q2)), ("no S", fr(1 - q2))]]
    if l == 0:
        hide = (0, None)
        stem = "En el árbol de probabilidades falta la probabilidad de la primera rama (marcada con «?»). ¿Cuál es su valor?"
        ans = fr(p1)
        alts = [1 - p1, q1, p1 * q1, p1 + q1, F(1, 2), 1 - q1]
        fig = viz.ptree_fig([("A", "?"), ("B", fr(1 - p1))], second)
    elif l == 1:
        stem = "Según el árbol de probabilidades, ¿cuál es la probabilidad del camino «A y luego S» (P(A ∩ S))?"
        ans = fr(p1 * q1)
        alts = [p1 + q1, q1, p1, p1 * (1 - q1), (1 - p1) * q2, p1 * q1 + (1 - p1) * q2]
        fig = viz.ptree_fig(first, second)
    else:
        stem = "Según el árbol de probabilidades, ¿cuál es la probabilidad total de S (P(S))?"
        ans = fr(p1 * q1 + (1 - p1) * q2)
        alts = [p1 * q1, (1 - p1) * q2, q1 + q2, p1 * q1 * (1 - p1) * q2, F(q1 + q2, 2), p1 * q1 + p1 * q2]
        fig = viz.ptree_fig(first, second)
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_REP, "Las probabilidades de las ramas que salen de un nodo suman 1; el camino se multiplica y los caminos favorables se suman.")


# ---------------------------------------------------------------- Argumentar
TRUE_C = ["P(A | B) = P(A ∩ B) / P(B), si P(B) > 0", "En general, P(A | B) y P(B | A) no son iguales", "Si A y B son independientes, P(A | B) = P(A)", "P(A ∩ B) = P(A | B) · P(B)",
          "Una probabilidad condicional siempre está entre 0 y 1", "Al condicionar por B, el espacio muestral se reduce a los casos de B"]
FALSE_C = ["P(A | B) = P(B | A) siempre", "P(A | B) = P(A) + P(B)", "P(A | B) = P(A ∩ B) / P(A)", "Si P(A | B) = 0, entonces A y B son el mismo suceso", "Una probabilidad condicional puede ser mayor que 1",
           "P(A ∩ B) = P(A | B) + P(B)", "Si A y B son independientes, P(A ∩ B) = P(A) + P(B)"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_C), r.sample(FALSE_C, 4)
        stem = "Sobre la probabilidad condicional, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_C), r.sample(TRUE_C, 4)
        stem = "Sobre la probabilidad condicional, ¿cuál de las siguientes afirmaciones es FALSA?"
    (rl, cl) = r.choice(CATS)
    fig = viz.two_way_fig(list(rl), list(cl), cnt_table(r, 0))
    return make(stem, fig, good, bad, Q_ARG, "Se razona con la definición P(A|B) = P(A∩B)/P(B) y con la independencia.")


def t_independent(r, l):
    (rl, cl) = r.choice(CATS)
    indep = r.random() < 0.5
    while True:
        p, q = r.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5)])
        u, v = r.choice([(1, 2), (2, 3), (1, 3), (3, 4), (2, 5)])
        k, m = r.randint(1, 4), r.randint(1, 4)
        cells = [[k * p * u, k * p * v], [m * q * u, m * q * v]]
        if not indep:
            dlt = r.choice([1, 2, -1])
            cells[0][0] += dlt
            cells[1][1] += dlt * 0
        a, b = cells[0]; c, d = cells[1]
        if min(a, b, c, d) < 1 or a + b + c + d > 120: continue
        N = a + b + c + d
        Ai = F(a + b, N); Bi = F(a + c, N); Pab = F(a, N)
        is_ind = Pab == Ai * Bi
        if is_ind == indep: break
    PAB = F(a, a + c)          # P(fila 0 | col 0)
    PA = F(a + b, N)
    if is_ind:
        ans = f"Sí, porque P({rl[0]} | {cl[0]}) = P({rl[0]}) (ambas valen {fr(PA)})"
    else:
        ans = f"No, porque P({rl[0]} | {cl[0]}) ≠ P({rl[0]}) ({fr(PAB)} ≠ {fr(PA)})"
    pool = [f"Sí, porque P({rl[0]} ∩ {cl[0]}) = P({rl[0]}) + P({cl[0]})", f"No, porque P({rl[0]}) ≠ P({cl[0]})", f"Sí, porque hay más de un caso favorable en la tabla", f"No, porque P({rl[0]} | {cl[0]}) = P({cl[0]} | {rl[0]})",
            f"Sí, porque P({rl[0]} | {cl[0]}) = P({cl[0]})" if PAB != Bi else f"Sí, porque los totales son iguales"]
    if is_ind:
        pool.append(f"No, porque P({rl[0]} | {cl[0]}) ≠ P({rl[0]}) ({fr(PAB)} ≠ {fr(PA)})")
        pool = [p for p in pool if not p.startswith(f"No, porque P({rl[0]} | {cl[0]}) ≠")]
    else:
        pool = [p for p in pool if not p.startswith(f"Sí, porque P({rl[0]} | {cl[0]}) = P({rl[0]})")]
    cs = [p for p in dict.fromkeys(pool) if p != ans]
    fig = viz.two_way_fig(list(rl), list(cl), cells)
    return make(f"Según la tabla, ¿los sucesos «{rl[0]}» y «{cl[0]}» son independientes?", fig, ans, pick4(ans, cs), Q_ARG,
                "Dos sucesos son independientes si P(A | B) = P(A): se compara la probabilidad condicional con la probabilidad total.")


ERR = ["Usó el total de la tabla en lugar del total de la condición", "Invirtió la condicional (calculó P(B | A) en vez de P(A | B))", "Sumó probabilidades en lugar de multiplicarlas",
       "No modificó el espacio muestral después de la primera extracción", "Confundió la probabilidad de la intersección con la condicional"]


def t_error(r, l):
    (rl, cl) = r.choice(CATS)
    cells = cnt_table(r, 1)
    a, b = cells[0]; c, d = cells[1]
    N = a + b + c + d
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    if k == 0:
        lines = [f"Total de personas: {N}; «{rl[0]}» y «{cl[0]}»: {a}; «{cl[0]}»: {a + c}", f"P({rl[0]} | {cl[0]}) = {a}/{N}"]
    elif k == 1:
        lines = [f"«{rl[0]}» y «{cl[0]}»: {a}; «{rl[0]}»: {a + b}; «{cl[0]}»: {a + c}", f"P({rl[0]} | {cl[0]}) = {a}/{a + b}"]
    elif k == 2:
        n1, n2 = r.randint(3, 8), r.randint(3, 8)
        lines = [f"Urna con {n1} rojas y {n2} azules; dos extracciones sin devolución", f"P(roja y luego azul) = {n1}/{n1 + n2} + {n2}/{n1 + n2 - 1}"]
    elif k == 3:
        n1, n2 = r.randint(3, 8), r.randint(3, 8)
        lines = [f"Urna con {n1} rojas y {n2} azules; primera extracción roja (sin devolución)", f"P(2.ª roja | 1.ª roja) = {n1}/{n1 + n2}"]
    else:
        lines = [f"«{rl[0]}» y «{cl[0]}»: {a}; «{cl[0]}»: {a + c}; total: {N}", f"P({rl[0]} | {cl[0]}) = P({rl[0]} ∩ {cl[0]}) = {a}/{N}"]
    import textwrap
    lines = [w for x in lines for w in textwrap.wrap(x.replace("-", "−"), 40)]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 60 + 34 * len(lines), 17), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_formula(r, l):
    if l == 0:
        pb = F(r.randint(2, 9), 10)
        pab = F(r.randint(1, int(pb * 10) - 1 if pb * 10 > 1 else 1), 10)
        if pab >= pb: raise Reject
        stem = f"Si P(A ∩ B) = {fs(pab)} y P(B) = {fs(pb)}, ¿cuánto vale P(A | B)?"
        ans = fr(pab / pb)
        alts = [pb / pab, pab * pb, pab, pab + pb, pb - pab, pab / (pb + pab)]
        fig = card([f"P(A ∩ B) = {fs(pab)}", f"P(B) = {fs(pb)}", "P(A | B) = P(A ∩ B) / P(B)"], 210, 21)
    elif l == 1:
        pa, pb, pu = F(r.randint(3, 6), 10), F(r.randint(3, 6), 10), F(r.randint(6, 9), 10)
        pab = pa + pb - pu
        if pab <= 0 or pab >= min(pa, pb): raise Reject
        stem = f"Si P(A) = {fs(pa)}, P(B) = {fs(pb)} y P(A ∪ B) = {fs(pu)}, ¿cuánto vale P(A | B)?"
        ans = fr(pab / pb)
        alts = [pab / pa, pab, pab * pb, (pa + pb) / pu, pab / pu, pa / pb]
        fig = card([f"P(A) = {fs(pa)}", f"P(B) = {fs(pb)}", f"P(A ∪ B) = {fs(pu)}", "Primero: P(A ∩ B) = P(A) + P(B) − P(A ∪ B)"], 240, 20)
    else:
        pa, pba = F(r.randint(2, 8), 10), F(r.randint(2, 8), 10)
        pb_given_not = F(r.randint(1, 5), 10)
        stem = f"Si P(A) = {fs(pa)}, P(B | A) = {fs(pba)} y P(B | no A) = {fs(pb_given_not)}, ¿cuánto vale P(B)?"
        ans = fr(pa * pba + (1 - pa) * pb_given_not)
        alts = [pba, pa * pba, (1 - pa) * pb_given_not, pba + pb_given_not, F(pba + pb_given_not, 2), pa + pba]
        fig = card([f"P(A) = {fs(pa)}", f"P(B | A) = {fs(pba)}", f"P(B | no A) = {fs(pb_given_not)}", "P(B) = P(A)·P(B|A) + P(no A)·P(B|no A)"], 240, 19)
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, f"Resultado: {ans}.")


def t_table_calc(r, l):
    (rl, cl) = r.choice(CATS)
    cells = cnt_table(r, 1)
    a, b = cells[0]; c, d = cells[1]
    N = a + b + c + d
    if l == 0:
        stem = f"Según la tabla, ¿cuánto vale P({cl[0]} | {rl[1]})?"
        ans = fr(F(c, c + d))
        alts = [F(a, a + c), F(c, N), F(c + d, N), F(c, a + c), F(d, c + d), F(a, a + b)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(1, 0)], hl_den_row=1)
    elif l == 1:
        stem = f"Según la tabla, ¿cuánto vale P({rl[0]} | no {cl[0]})? (Aquí «no {cl[0]}» es la categoría «{cl[1]}».)"
        ans = fr(F(b, b + d))
        alts = [F(b, N), F(a, a + c), F(b, a + b), F(b + d, N), F(d, b + d), F(a, b)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(0, 1)], hl_den_col=1)
    else:
        stem = f"Según la tabla, ¿cuánto vale P({rl[0]} | {cl[0]}) − P({rl[0]})?"
        val = F(a, a + c) - F(a + b, N)
        ans = fr(val)
        alts = [F(a, a + c), F(a + b, N), F(a, N) - F(a + b, N), F(a, a + c) + F(a + b, N), F(a, a + b) - F(a + c, N), abs(val) + F(1, 100)]
        fig = viz.two_way_fig(list(rl), list(cl), cells, hl_num=[(0, 0)], hl_den_col=0)
    cs = dist(ans, alts)
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, f"Resultado: {ans}.")


BY_SKILL = {
    Q_RES: [t_table_cond, t_urn],
    Q_MOD: [t_tree_ctx, t_survey],
    Q_REP: [t_cells_to_prob, t_read_tree],
    Q_ARG: [t_props, t_independent, t_error],
    Q_PRO: [t_formula, t_table_calc],
}
