"""Clase 23 · Técnicas de conteo: principio multiplicativo y uso de factoriales."""
from fractions import Fraction as F
from math import factorial as fac
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
import viz

CTX = [("prendas", [("camisas", "una camisa"), ("pantalones", "un pantalón"), ("zapatos", "un par de zapatos"), ("chaquetas", "una chaqueta")]),
       ("menú", [("entradas", "una entrada"), ("platos", "un plato de fondo"), ("postres", "un postre"), ("bebidas", "una bebida")]),
       ("equipo", [("bicicletas", "una bicicleta"), ("cascos", "un casco"), ("guantes", "un par de guantes"), ("bidones", "un bidón")])]


def nfmt(n):
    return f"{n:,}".replace(",", ".")


def dist(ans, alts):
    seen, out = {ans}, []
    for a in alts:
        s = nfmt(a) if isinstance(a, int) else a
        if s not in seen and (not isinstance(a, int) or a > 0):
            seen.add(s); out.append(s)
    return out


# ---------------------------------------------------------------- Resolver
def t_multiplicative(r, l):
    if l == 0:
        name, opts = r.choice(CTX)
        k = r.choice([2, 3])
        parts = r.sample(opts, k)
        ns = [r.randint(2, 6) for _ in parts]
        prod = 1
        for n in ns: prod *= n
        listing = ", ".join(f"{n} {p[0]}" for n, p in zip(ns, parts))
        stem = f"Una persona dispone de {listing}. Si debe elegir " + ", ".join(p[1] for p in parts[:-1]) + f" y {parts[-1][1]}, ¿de cuántas maneras distintas puede hacerlo?"
        ans = nfmt(prod)
        alts = [sum(ns), prod + ns[0], prod - ns[-1], prod * 2, ns[0] * ns[1] if k == 3 else prod + 1, prod + sum(ns)]
        fig = viz.slots_fig([(p[0], n) for p, n in zip(parts, ns)])
        ex = " · ".join(map(str, ns)) + f" = {prod}."
    elif l == 1:
        kind = r.choice(["digits", "plate", "code"])
        if kind == "digits":
            n, sz = r.choice([3, 4, 5]), r.choice([7, 8, 9, 10])
            lo, hi = (0, sz - 1)
            stem = f"¿Cuántos códigos de {n} dígitos distintos se pueden formar con los dígitos del {lo} al {hi} si no se puede repetir ningún dígito?"
            cnt = 1
            for i in range(n): cnt *= sz - i
            items = [(f"{i + 1}.º", sz - i) for i in range(n)]
            alts = [sz ** n, fac(sz), sz * n, cnt // sz, fac(sz) // fac(sz - n) * 2, (sz - 1) ** n, cnt + sz]
        elif kind == "plate":
            a_, b_ = r.choice([(2, 3), (3, 2), (2, 2), (3, 3), (1, 4), (4, 1)])
            al = r.choice([26, 24, 22])
            stem = f"Una patente se forma con {a_} letras (de un alfabeto de {al} letras, sin repetir) seguidas de {b_} dígitos (del 0 al 9, pueden repetirse). ¿Cuántas patentes distintas hay?"
            cnt = 1
            for i in range(a_): cnt *= al - i
            cnt *= 10 ** b_
            items = [(f"letra {i + 1}", al - i) for i in range(a_)] + [(f"dígito {i + 1}", 10) for i in range(b_)]
            alts = [al ** a_ * 10 ** b_, cnt // 10, al * a_ + 10 * b_, cnt * 2, al ** a_ * 10 * b_, cnt + al]
        else:
            n, sz = r.choice([3, 4, 5]), r.choice([6, 8, 9])
            ev = sz // 2
            stem = f"Se forman claves de {n} dígitos con los dígitos 1, 2, …, {sz}, sin repetir dígitos y de modo que la clave termine en un dígito par. ¿Cuántas claves hay?"
            cnt = ev
            for i in range(n - 1): cnt *= sz - 1 - i
            items = [(f"{i + 1}.º", sz - 1 - i) for i in range(n - 1)] + [("último", ev)]
            alts = [sz * (sz - 1) * (sz - 2), sz ** n, cnt * 2, cnt // 2, ev * sz ** (n - 1), ev + (sz - 1) * (n - 1)]
        ans = nfmt(cnt)
        fig = viz.slots_fig(items[:5])
        ex = "Se multiplican las opciones de cada etapa (sin repetición, cada etapa tiene una opción menos)."
    else:
        kind = r.choice(["first", "even", "big"])
        if kind == "first":
            n, sz = r.choice([3, 4, 5]), r.choice([7, 8, 9, 10])
            stem = f"¿Cuántos números de {n} cifras se pueden formar con los dígitos del 0 al {sz - 1}, sin repetir cifras, si el número no puede comenzar con 0?"
            cnt = sz - 1
            for i in range(n - 1): cnt *= sz - 1 - i
            items = [("1.ª (≠ 0)", sz - 1)] + [(f"{i + 2}.ª", sz - 1 - i) for i in range(n - 1)]
            alts = [sz * (sz - 1) * (sz - 2), (sz - 1) * sz ** (n - 1), sz ** n, cnt - (sz - 1), (sz - 1) ** n, cnt * sz // (sz - 1)]
            ex = "La primera cifra tiene una opción menos (no puede ser 0); luego cada cifra tiene una opción menos que la anterior."
        elif kind == "even":
            sz = r.choice([8, 9, 10])
            stem = f"¿Cuántos números pares de 3 cifras distintas se pueden formar con los dígitos del 0 al {sz - 1}?"
            evens = [d for d in range(sz) if d % 2 == 0]
            cnt = (sz - 1) * (sz - 2) + (len(evens) - 1) * (sz - 2) * (sz - 2)
            items = None
            alts = [len(evens) * (sz - 1) * (sz - 2), len(evens) * sz * sz, (len(evens) - 1) * (sz - 1) * (sz - 2), cnt + 1, cnt - (len(evens) - 1), cnt * 2]
            ex = "Se cuentan por casos: terminan en 0 o terminan en otro dígito par (y la primera cifra no puede ser 0)."
        else:
            n, sz, m = r.choice([3, 4]), r.choice([7, 8, 9]), r.choice([5, 6])
            big = "500" if n == 3 else "5.000"
            stem = f"¿Cuántos números de {n} cifras distintas, formados con los dígitos del 1 al {sz}, son mayores que {big}?"
            first = sz - 4
            cnt = first
            for i in range(n - 1): cnt *= sz - 1 - i
            items = None
            alts = [sz * (sz - 1) * (sz - 2) * (sz - 3 if n == 4 else 1), first * sz ** (n - 1), cnt * 2, cnt // first, first * (sz - 1) ** (n - 1), cnt + sz - 1]
            ex = f"La primera cifra debe ser mayor que 4 ({first} opciones); las demás disminuyen de a una."
        ans = nfmt(cnt)
        fig = viz.slots_fig(items[:5]) if items else card([stem.split(" ¿")[0][:1] or "", "Cuenta por casos / etapas"], 190, 22)
        if not items:
            fig = viz.slots_fig([("etapas", "?")], ops="×")
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_RES, ex)


NAMES = [("Ana", "Beto"), ("Carla", "Diego"), ("Elena", "Felipe"), ("Gabriela", "Hugo"), ("Inés", "Javier"), ("Karen", "Luis")]
GROUPS = ["personas en una fila", "estudiantes en una banca", "libros distintos en un estante", "autos en un estacionamiento de una hilera", "banderas distintas en un mástil", "cuadros en una pared"]


def t_arrange(r, l):
    n = r.choice([4, 5, 6, 7, 8, 9])
    what = r.choice(GROUPS)
    if l == 0:
        stem = f"¿De cuántas maneras se pueden ordenar {n} {what}?"
        cnt = fac(n)
        alts = [n * n, n * (n - 1), fac(n) // 2, fac(n) + n, fac(n - 1), n ** n]
        fig = viz.slots_fig([(f"lugar {i + 1}", n - i) for i in range(min(n, 5))])
    elif l == 1:
        k = r.choice([2, 3])
        stem = f"¿De cuántas maneras se pueden ordenar {n} {what} si {k} de ellos deben quedar siempre juntos, en cualquier orden entre sí?"
        cnt = fac(n - k + 1) * fac(k)
        alts = [fac(n), fac(n - k + 1), fac(n - k) * fac(k), fac(n) // fac(k), fac(n - 1), fac(n) - cnt]
        fig = card([f"{n} elementos en fila", f"{k} deben estar juntos", "Cuenta el grupo como 1 elemento"], 210, 21)
    else:
        a_, b_ = r.choice(NAMES)
        stem = f"¿De cuántas maneras se pueden ordenar {n} personas en una fila si {a_} y {b_} NO deben quedar juntos?"
        cnt = fac(n) - 2 * fac(n - 1)
        alts = [fac(n) - fac(n - 1), fac(n - 1) * 2, fac(n), fac(n - 2) * (n - 1) * 2, fac(n) - fac(n - 2) * 2, 2 * fac(n - 1)]
        fig = card([f"{n} personas en fila", f"{a_} y {b_} no juntos", "Total − casos con ambos juntos"], 210, 21)
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_RES, f"Resultado: {ans}.")


# ---------------------------------------------------------------- Modelar
def t_context(r, l):
    if l == 0:
        a, b, c = r.randint(2, 5), r.randint(2, 5), r.randint(2, 4)
        stem = f"Para viajar de la ciudad A a la ciudad D hay {a} rutas de A a B, {b} rutas de B a C y {c} rutas de C a D. ¿Cuántos recorridos distintos hay de A a D pasando por B y C?"
        cnt = a * b * c
        alts = [a + b + c, a * b + c, cnt + a, cnt * 2, a * b, cnt - c]
        fig = viz.slots_fig([("A → B", a), ("B → C", b), ("C → D", c)])
    elif l == 1:
        a, b, d = r.randint(2, 4), r.randint(2, 4), r.randint(1, 4)
        stem = f"Para ir de A a C se puede ir directamente por {d} caminos, o bien pasar por B usando {a} caminos de A a B y {b} caminos de B a C. ¿Cuántas rutas distintas hay de A a C?"
        cnt = a * b + d
        alts = [a * b * d, a + b + d, (a + b) * d, a * b, cnt + 1, a * b + d * 2]
        fig = viz.roads_fig(a, b, d)
    else:
        n = r.choice([5, 6, 7, 8, 9, 10, 11, 12])
        k = r.choice([2, 3, 4])
        who = r.choice(["atletas", "estudiantes", "equipos", "candidatos"])
        stem = f"En un concurso participan {n} {who} y se premian los {k} primeros lugares (sin que un mismo participante ocupe dos lugares). ¿Cuántas formas distintas hay de repartir los premios?"
        cnt = 1
        for i in range(k): cnt *= n - i
        alts = [fac(n), n ** k, n * k, fac(n) // fac(k), cnt // fac(k), cnt * 2, cnt + n]
        fig = viz.slots_fig([(f"lugar {i + 1}", n - i) for i in range(k)])
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_MOD, f"Se multiplican las etapas sucesivas y se suman los casos excluyentes: {ans}.")


def t_password(r, l):
    if l == 0:
        L_, D_ = r.choice([(2, 2), (2, 3), (3, 2), (1, 3)])
        stem = f"Una clave se forma con {L_} letra(s) (de un alfabeto de 26 letras) y {D_} dígito(s) (0 al 9), en ese orden, pudiendo repetirse. ¿Cuántas claves distintas hay?"
        cnt = 26 ** L_ * 10 ** D_
        alts = [26 * L_ + 10 * D_, 26 ** L_ + 10 ** D_, 26 * 10 * (L_ + D_), cnt // 10, cnt * 2, 36 ** (L_ + D_)]
        fig = viz.slots_fig([(f"letra {i + 1}", 26) for i in range(L_)] + [(f"dígito {i + 1}", 10) for i in range(D_)])
    elif l == 1:
        n = r.choice([3, 4, 5])
        s_ = r.choice([4, 5, 6])
        stem = f"¿Cuántas palabras (con o sin sentido) de {n} letras se pueden formar con {s_} letras distintas, si no se puede repetir ninguna letra?"
        cnt = 1
        for i in range(n): cnt *= s_ - i
        if n > s_: raise Reject
        alts = [s_ ** n, fac(s_), s_ * n, cnt * 2, cnt // 2, n ** s_]
        fig = viz.slots_fig([(f"letra {i + 1}", s_ - i) for i in range(n)])
    else:
        n = r.choice([4, 5, 6])
        first, last = r.choice([("impar", "par"), ("par", "impar"), ("par", "par"), ("impar", "impar")])
        stem = f"Una clave de {n} dígitos (0 al 9, pueden repetirse) debe comenzar con un dígito {first} y terminar con un dígito {last}. ¿Cuántas claves hay?"
        cnt = 5 * 10 ** (n - 2) * 5
        alts = [10 ** n // 4, 5 * 5 * n, 10 ** n // 2, 5 * 10 ** (n - 1), 10 ** (n - 2) * 10, 25 * 9 ** (n - 2)]
        fig = viz.slots_fig([(first, 5)] + [("libre", 10)] * (n - 2) + [(last, 5)])
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_MOD, "Se multiplica la cantidad de opciones de cada posición, respetando las restricciones.")


# ---------------------------------------------------------------- Representar
def t_read_diagram(r, l):
    if l == 0:
        a, b = r.randint(2, 5), r.randint(2, 5)
        cnt = a * b
        nm = r.choice([("A", "B", "C"), ("P", "Q", "R"), ("1", "2", "3"), ("X", "Y", "Z")])
        fig = viz.roads_fig(a, b, 0, nm)
        stem = f"En el mapa se muestran las rutas de {nm[0]} a {nm[1]} y de {nm[1]} a {nm[2]}. ¿Cuántos recorridos distintos hay de {nm[0]} a {nm[2]} pasando por {nm[1]}?"
        alts = [a + b, a * b + a, a * b - 1, a * b * 2, a * b + b, (a + b) * 2]
    elif l == 1:
        a, b, d = r.randint(2, 3), r.randint(2, 3), r.randint(1, 3)
        cnt = a * b + d
        fig = viz.roads_fig(a, b, d)
        stem = "En el mapa, las curvas azules son caminos A→B y B→C, y las curvas rojas son caminos directos de A a C. ¿Cuántas rutas distintas hay de A a C?"
        alts = [a * b * d, a + b + d, a * b, (a + b) * d, cnt + 1, a * b + d * 2]
    else:
        a, b, c = r.randint(2, 6), r.randint(2, 5), r.randint(2, 5)
        cnt = a * b * c
        fig = viz.slots_fig([("etapa 1", a), ("etapa 2", b), ("etapa 3", c)])
        stem = "El diagrama indica cuántas opciones hay en cada etapa sucesiva de un proceso. ¿Cuántos resultados distintos puede tener el proceso completo?"
        alts = [a + b + c, a * b + c, a * b, cnt + a, cnt * 2, cnt - 1]
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_REP, "Se multiplican las opciones de etapas sucesivas y se suman las rutas excluyentes.")


def t_tree(r, l):
    if l == 0:
        a, b = r.randint(2, 3), r.randint(2, 4)
        ch = [b] * a
        stem = "En el diagrama de árbol de la figura, cada rama de la primera etapa se abre en ramas de la segunda etapa. ¿Cuántos resultados distintos (extremos de ramas) tiene el árbol completo?"
    elif l == 1:
        ch = [r.randint(1, 4) for _ in range(r.randint(2, 4))]
        stem = "En el diagrama de árbol de la figura, cada nodo de la primera etapa se abre en un número distinto de ramas. ¿Cuántos resultados distintos tiene el árbol completo?"
        if len(set(ch)) < 2 or sum(ch) > 12: raise Reject
    else:
        a, b = r.randint(2, 4), r.randint(2, 3)
        m3 = r.choice([2, 3, 4])
        ch = [b] * a
        stem = f"El diagrama de árbol muestra las dos primeras etapas de un proceso de tres etapas. Si en la tercera etapa cada resultado se abre siempre en {m3} opciones más, ¿cuántos resultados distintos tendrá el proceso completo?"
    cnt = sum(ch) * (m3 if l == 2 else 1)
    alts = [len(ch) + max(ch), len(ch) * max(ch), cnt + 1, cnt - 1, cnt * 2, sum(ch) + len(ch)]
    if l == 0: alts = [a + b, a * b + a, a * b - 1, a * b * 2, a * b + b, (a + b) * 2]
    fig = viz.tree_fig(ch, "Etapa 1", "Etapa 2")
    ans = nfmt(cnt)
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_REP, f"Se cuentan los extremos de las ramas: {ans}.")


# ---------------------------------------------------------------- Argumentar
TRUE_C = ["El principio multiplicativo se aplica cuando el proceso se realiza en etapas sucesivas y cada etapa tiene un número fijo de opciones", "n! = n · (n − 1)! para todo entero n ≥ 1",
          "0! = 1", "El número de formas de ordenar n objetos distintos en fila es n!", "Si se puede elegir A de a maneras o B de b maneras (sin poder hacer ambas), hay a + b opciones",
          "5!/3! = 20"]
FALSE_C = ["Si hay 3 opciones en una etapa y 4 en la siguiente, hay 7 formas de completar ambas etapas", "0! = 0", "(2n)! = 2·n! para todo n", "n! + m! = (n + m)!", "5! = 5·4",
           "Las formas de ordenar 4 objetos distintos en fila son 4·4·4·4", "6!/3! = 2!"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_C), r.sample(FALSE_C, 4)
        stem = "Sobre técnicas de conteo, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_C), r.sample(TRUE_C, 4)
        stem = "Sobre técnicas de conteo, ¿cuál de las siguientes afirmaciones es FALSA?"
    a, b, c = r.randint(2, 4), r.randint(2, 4), r.randint(2, 3)
    fig = viz.slots_fig([("etapa 1", a), ("etapa 2", b), ("etapa 3", c)])
    return make(stem, fig, good, bad, Q_ARG, "Se razona con el principio multiplicativo, el principio aditivo y la definición de factorial.")


def t_which_plan(r, l):
    a, b = r.choice([(3, 4), (2, 5), (4, 3), (5, 2), (3, 5), (4, 6)])
    if l == 0:
        kind = r.choice(["prod", "sum"])
        if kind == "prod":
            stem = f"Una persona debe elegir una camisa entre {a} y un pantalón entre {b}. ¿Cuál expresión da el número de conjuntos distintos (camisa y pantalón)?"
            good = f"{a} · {b}"
        else:
            stem = f"Una persona debe elegir UNA sola prenda: una camisa entre {a} o un pantalón entre {b}. ¿Cuál expresión da el número de opciones?"
            good = f"{a} + {b}"
        pool = [f"{a} · {b}", f"{a} + {b}", f"{a}^{b}", f"{b}^{a}", f"{a}! · {b}!"]
    elif l == 1:
        kind = r.choice(["pow", "perm"])
        if kind == "pow":
            stem = f"Se forma un código de {b} posiciones y en cada posición se puede usar cualquiera de {a} símbolos, con repetición. ¿Cuál expresión da el número de códigos?"
            good = f"{a}^{b}"
        else:
            b = min(b, a)
            stem = f"Se ordenan {a} objetos distintos en fila. ¿Cuál expresión da el número de ordenaciones?"
            good = f"{a}!"
        pool = [f"{a}^{b}", f"{b}^{a}", f"{a}!", f"{a} · {b}", f"{a} + {b}"]
    else:
        stem = f"Hay {a} rutas directas de A a C, y también se puede ir por B con {b} rutas de A a B y 2 rutas de B a C. ¿Cuál expresión da el número de rutas de A a C?"
        good = f"{a} + {b} · 2"
        pool = [f"{a} + {b} · 2", f"{a} · {b} · 2", f"({a} + {b}) · 2", f"{a} + {b} + 2", f"{a} · ({b} + 2)"]
    cs = [p for p in pool if p != good]
    fig = viz.slots_fig([("opciones", a), ("etapa 2", b)], ops="?")
    return make(stem, fig, good, cs, Q_ARG, "Etapas sucesivas se multiplican; opciones excluyentes se suman; con repetición aparece una potencia; ordenar n objetos distintos da n!.")


ERR = ["Sumó las opciones de las etapas en lugar de multiplicarlas", "Multiplicó por una etapa que no forma parte del proceso", "No consideró que no se pueden repetir elementos",
       "Calculó n! completo aunque solo se ordenan algunos elementos", "Contó como distintas disposiciones que son la misma elección"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    a, b = r.randint(3, 6), r.randint(3, 6)
    if k == 0:
        lines = [f"{a} entradas y {b} postres; una entrada y un postre", f"Total = {a} + {b} = {a + b}"]
    elif k == 1:
        lines = [f"{a} camisas y {b} pantalones; se elige un conjunto", f"Total = {a} · {b} · 2 = {a * b * 2}"]
    elif k == 2:
        lines = ["Claves de 4 dígitos sin repetir dígitos", "Total = 10 · 10 · 10 · 10 = 10.000"]
    elif k == 3:
        n = r.choice([5, 6, 7])
        lines = [f"De {n} personas se eligen presidente, secretario y tesorero", f"Total = {n}! = {fac(n)}"]
    else:
        lines = ["Elegir 2 amigos de 4 para un viaje (el orden no importa)", "Total = 4 · 3 = 12"]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 200, 19), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_factorial(r, l):
    if l == 0:
        n = r.randint(5, 11); d = r.choice([2, 3, 4])
        k = n - d
        cnt = fac(n) // fac(k)
        stem = f"¿Cuál es el valor de {n}!/{k}!?"
        alts = [fac(d), d, fac(n) - fac(k), cnt + n, cnt // 2, n * k, fac(n) // fac(k + 1)]
        fig = card([f"{n}! / {k}!", "n! = n · (n − 1) · … · 2 · 1"], 190, 24)
        ans = nfmt(cnt)
        cs = dist(ans, alts)
    elif l == 1:
        if r.random() < 0.3:
            v = r.choice([("(n + 2)!/n!", "(n + 2)(n + 1)", ["n + 2", "(n + 2)n", "2!", "(n + 1)!", "n² + 2"]),
                          ("(n + 3)!/(n + 1)!", "(n + 3)(n + 2)", ["n + 3", "(n + 3)(n + 1)", "2!", "(n + 2)!", "n² + 3"]),
                          ("(n + 1)!/(n − 1)!", "(n + 1)n", ["n + 1", "(n + 1)(n − 1)", "2!", "n!", "n² + 1"]),
                          ("n!/(n − 3)!", "n(n − 1)(n − 2)", ["n(n − 3)", "n − 3", "3!", "(n − 1)(n − 2)", "n³"]),
                          ("(n + 2)!/(n − 1)!", "(n + 2)(n + 1)n", ["(n + 2)(n + 1)", "3!", "(n + 2)n", "(n + 1)!", "n³ + 2"])])
            stem = f"¿A cuál expresión equivale {v[0]} (con n natural suficientemente grande)?"
            ans, cs = v[1], v[2]
            fig = card([v[0], "Desarrolla el factorial mayor hasta el menor"], 190, 24)
        else:
            n = r.randint(4, 12); a_, b_ = r.choice([(1, -1), (2, 0), (3, 1), (1, 0), (2, -1)])
            hi, lo = n + a_, n + b_
            cnt = fac(hi) // fac(lo)
            stem = f"¿Cuál es el valor de {hi}!/{lo}!?"
            ans = nfmt(cnt)
            cs = dist(ans, [fac(hi - lo), hi - lo, cnt + hi, hi * lo, cnt // 2, fac(hi) - fac(lo)])
            fig = card([f"{hi}! / {lo}!", "Simplifica los factores comunes"], 190, 24)
    else:
        n = r.randint(5, 14)
        style = r.choice([0, 1])
        if style == 0:
            prod = n * (n - 1)
            stem = f"Si n!/(n − 2)! = {prod}, ¿cuánto vale n?"
            fig = card([f"n! / (n − 2)! = {prod}", "n! / (n − 2)! = n(n − 1)"], 190, 24)
        else:
            prod = n * (n - 1) * (n - 2)
            stem = f"Si n!/(n − 3)! = {prod}, ¿cuánto vale n?"
            fig = card([f"n! / (n − 3)! = {prod}", "n! / (n − 3)! = n(n − 1)(n − 2)"], 190, 24)
        ans = str(n)
        cs = [str(n - 1), str(n + 1), str(prod), str(n - 2), str(prod // 2), str(n + 2)]
        cs = [c for c in cs if c != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, "Se simplifican los factores comunes de los factoriales.")


def t_count(r, l):
    if l == 0:
        L_, D_ = r.choice([(3, 3), (2, 4), (3, 2), (4, 2), (2, 3), (3, 4)])
        al = r.choice([26, 24, 22])
        stem = f"Una patente tiene {L_} letras distintas (de {al}) seguidas de {D_} dígitos distintos (de 10). ¿Cuántas patentes hay?"
        cnt = 1
        for i in range(L_): cnt *= al - i
        for i in range(D_): cnt *= 10 - i
        alts = [al ** L_ * 10 ** D_, al ** L_ * 10 * D_, cnt // 10, cnt * 2, al * L_ + 10 * D_, cnt + al]
        npos = L_ + D_
    elif l == 1:
        n, sz = r.choice([3, 4, 5, 6]), r.choice([7, 8, 9])
        stem = f"¿Cuántos números de {n} cifras distintas se pueden formar con los dígitos del 1 al {sz}?"
        cnt = 1
        for i in range(n): cnt *= sz - i
        alts = [sz ** n, fac(sz), cnt // 2, cnt * 2, sz * n, cnt + sz]
        npos = n
    else:
        n, sz, h = r.choice([3, 4]), r.choice([7, 8, 9]), r.choice([3, 4, 5])
        big = (f"{h}00" if n == 3 else f"{h}.000")
        stem = f"¿Cuántos números de {n} cifras distintas, formados con los dígitos del 1 al {sz}, son mayores que {big}?"
        first = sz - h
        cnt = first
        for i in range(n - 1): cnt *= sz - 1 - i
        alts = [sz * (sz - 1) * (sz - 2) * (sz - 3 if n == 4 else 1), first * sz ** (n - 1), cnt * 2, cnt // first, cnt + sz, first * (sz - 1) ** (n - 1)]
        npos = n
    ans = nfmt(cnt)
    fig = viz.slots_fig([(f"pos. {i + 1}", "?") for i in range(min(5, npos))])
    return make(stem, fig, ans, pick4(ans, dist(ans, alts)), Q_PRO, f"Se multiplican las opciones de cada posición: {ans}.")


BY_SKILL = {
    Q_RES: [t_multiplicative, t_arrange],
    Q_MOD: [t_context, t_password],
    Q_REP: [t_read_diagram, t_tree],
    Q_ARG: [t_props, t_which_plan, t_error],
    Q_PRO: [t_factorial, t_count],
}
