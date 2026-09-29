"""Clase 16 · Semejanza avanzada: relación de áreas y volúmenes (k, k², k³)."""
import itertools
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import Plot, card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from clase10 import nice
import geo


def dec(x):
    x = F(x)
    s = f"{float(x):.4f}".rstrip("0").rstrip(".").replace(".", ",")
    return s


def num(x):
    x = F(x)
    return fs(x) if x.denominator == 1 else dec(x)


def ratio(a, b):
    g = F(a, b)
    return f"{g.numerator}:{g.denominator}"


def pair(r, l):
    """Razón de semejanza k = m/n (menor:mayor = n:m)."""
    if l == 0:
        return r.choice([(1, 2), (1, 3), (1, 4), (1, 5)])
    if l == 1:
        return r.choice([(2, 3), (2, 5), (3, 4), (3, 5), (1, 2), (1, 3), (4, 5)])
    return r.choice([(2, 3), (3, 5), (3, 4), (2, 5), (4, 7), (5, 6), (3, 7)])


# ---------------------------------------------------------------- Resolver
def t_area(r, l):
    n, m = pair(r, l)                      # menor : mayor = n : m
    s0 = r.randint(2, 6)
    s_small, s_big = n * s0, m * s0
    k2 = F(m * m, n * n)
    if l < 2:
        A1 = r.choice([2, 3, 4, 5, 6, 8, 9, 10, 12]) * n * n
        A2 = A1 * k2
        ask = "big"
        stem = f"Dos triángulos son semejantes. Dos lados homólogos miden {s_small} cm y {s_big} cm. Si el área del triángulo menor es {A1} cm², ¿cuál es el área del mayor?"
        ans = A2
        cands = [A1 * F(m, n), A1 * k2 * F(m, n), A1 + (s_big - s_small), A1 * F(n * n, m * m), A1 * (F(m, n) ** 3), A1 * F(n, m), A1 + s_big ** 2 - s_small ** 2, A1 * 2]
        fig = geo.sim_tris(F(m, n), dict(base=f"{s_small} cm"), dict(base=f"{s_big} cm"), f"A = {A1} cm²", "A = ?")
        ex = f"Razón de semejanza {n}:{m}; razón de áreas {n * n}:{m * m}. Área mayor = {A1}·{m * m}/{n * n} = {num(A2)} cm²."
    else:
        A2 = r.choice([2, 3, 4, 5, 6, 8]) * m * m
        A1 = A2 * F(n * n, m * m)
        stem = f"Dos triángulos semejantes tienen áreas de {num(A1)} cm² y {A2} cm². Si un lado del menor mide {s_small} cm, ¿cuánto mide el lado homólogo del mayor?"
        ans = s_big
        k = F(m, n)
        cands = [s_small * k * k, s_small + (A2 - A1), F(A2, A1) * s_small if F(A2, A1).denominator == 1 else s_big + 1, s_small * (k ** 3), s_big + s0, s_big - s0 if s_big > s0 else s_big + 2, s_small * 2]
        fig = geo.sim_tris(F(m, n), dict(base=f"{s_small} cm"), dict(base="x"), f"A = {num(A1)} cm²", f"A = {A2} cm²")
        ex = f"Razón de áreas {n * n}:{m * m} ⟹ razón de lados {n}:{m}: x = {s_small}·{m}/{n} = {s_big} cm."
    cs = [num(c_) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    return make(stem, fig, num(ans), pick4(num(ans), cs), Q_RES, ex)


def t_volume(r, l):
    n, m = pair(r, l)
    if l == 0:
        V1 = r.choice([1, 2, 3, 4, 5, 6, 8, 10])
        V2 = V1 * F(m, n) ** 3
        stem = f"Dos cubos son semejantes y sus aristas miden {n} cm y {m} cm. Si el volumen del cubo menor es {V1 * n ** 3} cm³, ¿cuál es el volumen del mayor?"
        V1 = V1 * n ** 3; V2 = V1 * F(m, n) ** 3
        ans = V2
        cands = [V1 * F(m, n), V1 * F(m, n) ** 2, V1 * F(n, m) ** 3, V1 * (m - n), V1 + m ** 3 - n ** 3 if False else V1 * 3, V1 * F(m, n) ** 4 if False else V1 * 2]
        fig = geo.two_cubes(F(m, n), f"{n} cm", f"{m} cm", (f"V = {V1} cm³", "V = ?"))
        ex = f"Razón de volúmenes {n ** 3}:{m ** 3}: V = {V1}·{m ** 3}/{n ** 3} = {num(V2)} cm³."
    elif l == 1:
        V1 = r.choice([1, 2, 3, 5]) * n ** 3
        V2 = V1 * F(m, n) ** 3
        kind = r.choice(["cubos", "prismas", "cilindros", "conos"])
        stem = f"Dos {kind} semejantes tienen alturas de {n * 2} cm y {m * 2} cm. Si el volumen del menor es {V1} cm³, ¿cuánto vale el volumen del mayor?"
        ans = V2
        cands = [V1 * F(m, n), V1 * F(m, n) ** 2, V1 * F(n, m) ** 3, V1 * (m - n), V1 * 3, V1 + (m ** 3 - n ** 3)]
        fig = geo.two_cubes(F(m, n), f"{n * 2} cm", f"{m * 2} cm", (f"V = {V1}", "V = ?"))
        ex = f"Razón de volúmenes = ({n}/{m})³: V = {V1}·{m}³/{n}³ = {num(V2)} cm³."
    else:
        V1 = r.choice([1, 2, 3, 4]) * n ** 3
        k = F(m, n)
        A1, A2 = 4 * n * n, 4 * m * m
        stem = f"Dos cuerpos semejantes tienen superficies de {A1} cm² y {A2} cm². Si el volumen del menor es {V1} cm³, ¿cuál es el volumen del mayor?"
        ans = V1 * k ** 3
        cands = [V1 * k ** 2, V1 * k, V1 * F(A2, A1) ** 3 if False else V1 * k ** 4, V1 * (A2 - A1) // 4 if (V1 * (A2 - A1)) % 4 == 0 else V1 * 5, V1 * F(n, m) ** 3, V1 + A2 - A1]
        fig = geo.two_cubes(k, f"S = {A1} cm²", f"S = {A2} cm²", (f"V = {V1} cm³", "V = ?"))
        ex = f"Razón de áreas {n * n}:{m * m} ⟹ razón lineal {n}:{m} ⟹ razón de volúmenes {n ** 3}:{m ** 3}: V = {num(ans)} cm³."
    cs = [num(c_) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    return make(stem, fig, num(ans), pick4(num(ans), cs), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_scale_ctx(r, l):
    if l == 0:
        sc, cm2 = r.choice([50000, 100000, 200000, 500000]), r.randint(2, 15)
        km2 = F(cm2) * F(sc, 100000) ** 2
        stem = f"En un mapa a escala 1:{sc:,} un lago ocupa {cm2} cm². ¿Cuál es su superficie real, en km²?".replace(",", ".")
        ans = km2
        cands = [F(cm2) * F(sc, 100000), F(cm2) * F(sc, 100000) ** 3, F(cm2) * sc // 100000 if False else cm2 * F(sc, 1000), F(cm2, 4) if sc != 200000 else cm2 * 2, km2 * 10, F(cm2) * F(100000, sc) ** 2, cm2 * sc // 1000]
        fig = card([f"Escala 1:{sc:,}".replace(",", "."), f"Área en el mapa: {cm2} cm²", "Área real (km²) = ?"], 210, 21)
        ex = f"1 cm del mapa = {F(sc, 100000)} km; áreas: ({F(sc, 100000)})² por cada cm²: {num(km2)} km²."
    elif l == 1:
        sc, V = r.choice([5, 10, 20, 25, 50, 100]), r.choice([2, 3, 5, 8, 12, 15])
        real = V * sc ** 3
        stem = f"Una maqueta a escala 1:{sc} de un estanque tiene una capacidad de {V} litros. ¿Cuál es la capacidad del estanque real, en litros?"
        ans = real
        cands = [V * sc, V * sc ** 2, V * sc ** 4 if False else V * 3 * sc ** 2, V * F(sc) ** 3 * 10, V + sc ** 3, V * sc ** 3 // 10, V * (sc + 1) ** 3 if False else V * sc ** 3 + 1000]
        fig = card([f"Escala 1:{sc}", f"Volumen de la maqueta: {V} L", "Volumen real = ?"], 210, 21)
        fig_ = fig
        ex = f"Razón lineal 1:{sc} ⟹ razón de volúmenes 1:{sc ** 3}: {V}·{sc ** 3} = {real} L."
    else:
        k, A = r.choice([2, 3, 4, 5]), r.choice([3, 6, 12, 15, 24, 30])
        cover = r.choice([12, 24, 36, 48, 60])
        m2 = A * k * k
        if m2 % cover: raise Reject
        n_ = m2 // cover
        stem = f"Un tarro de pintura alcanza para {cover} m². Un mural de {A} m² se amplía con razón de semejanza {k}:1. ¿Cuántos tarros se necesitan para pintar el mural ampliado?"
        ans = n_
        cands = [A * k // cover if (A * k) % cover == 0 else n_ + 1, A * k ** 3 // cover if (A * k ** 3) % cover == 0 else n_ + 2, n_ * k, n_ + 1, n_ - 1 if n_ > 1 else n_ + 3, F(A * k * k, cover) + 1, k * k]
        fig = card([f"Mural original: {A} m²", f"Razón de semejanza: {k}:1", f"Un tarro rinde {cover} m²"], 210, 21)
        ex = f"Área ampliada = {A}·{k}² = {m2} m²; tarros = {m2}/{cover} = {n_}."
    cs = [num(c_) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    cs = [c_.replace(",", "") if False else c_ for c_ in cs]
    fmtv = lambda v: (f"{int(v):,}".replace(",", ".") if F(v).denominator == 1 else num(v))
    return make(stem, fig, fmtv(ans), pick4(fmtv(ans), [fmtv(F(c_.replace(",", "."))) if False else c_ for c_ in [fmtv(c0) for c0 in cands if F(c0) != F(ans) and F(c0) > 0]]), Q_MOD, ex)


def t_pizza(r, l):
    if l == 0:
        n, m = r.choice([(2, 3), (1, 2), (3, 4), (2, 5), (1, 3), (4, 5)])
        P = r.choice([300, 400, 500, 600, 800, 1000]) * n * n
        d1, d2 = n * 10, m * 10
        price = F(P) * F(m, n) ** 2
        stem = f"El precio de una pizza es proporcional a su área. Una pizza de {d1} cm de diámetro cuesta ${P:,}. ¿Cuánto debería costar una de {d2} cm de diámetro?".replace(",", ".")
        ans = price
        cands = [F(P) * F(m, n), F(P) * F(m, n) ** 3, F(P) + (d2 - d1) * 100, F(P) * F(n, m) ** 2, F(P) * 2, F(P) * F(m * m - n * n, 1) / 2 if False else F(P) + 3000]
        fig = geo.two_discs(n, m, f"⌀ {d1} cm", f"⌀ {d2} cm", f"${P:,}".replace(",", "."), "$ ?")
        ex = f"Precio ∝ área ∝ (diámetro)²: {P}·({m}/{n})² = {int(price)}."
    elif l == 1:
        n, m = r.choice([(2, 3), (3, 4), (2, 5), (3, 5)])
        sr = r.choice([2, 3, 4, 5, 6, 8])
        r1, r2 = n * sr, m * sr
        stem = f"Dos círculos tienen radios de {r1} cm y {r2} cm. ¿Cuántas veces cabe, aproximadamente, el área del menor en el área del mayor? (usa razón exacta)"
        stem = f"Dos círculos tienen radios de {r1} cm y {r2} cm. ¿Cuál es la razón entre el área del menor y el área del mayor?"
        ans_s = ratio(n * n, m * m)
        cands = [ratio(n, m), ratio(n ** 3, m ** 3), ratio(m * m, n * n), ratio(n * n * 3, m * m * 3 + 1), f"{n * n}:{m * m + 1}", ratio(m, n)]
        fig = geo.two_discs(n, m, f"r = {r1} cm", f"r = {r2} cm", "", "")
        ex = f"Razón de áreas = (razón de radios)² = ({n}/{m})² = {n * n}/{m * m}."
        return make(stem, fig, ans_s, pick4(ans_s, cands), Q_MOD, ex)
    else:
        p = r.choice([10, 20, 25, 30, 40, 50, -10, -20, -30])
        f = (1 + F(p, 100)) ** 2
        chg = (f - 1) * 100
        stem = f"El radio de un círculo {'aumenta' if p > 0 else 'disminuye'} un {abs(p)}%. ¿Qué ocurre con su área?"
        lab = lambda v: f"{'Aumenta' if v > 0 else 'Disminuye'} {abs(float(v)):g}%".replace(".", ",")
        ans_s = lab(chg)
        cands = [lab(F(p)), lab(F(2 * p)), lab(chg + (5 if chg > 0 else -5)), lab(-chg), lab(F(p) * 3), lab(F(p) ** 2 / 10)]
        fig = geo.two_discs(10, 10 * (1 + p / 100), "r", f"r {'+' if p > 0 else '−'} {abs(p)}%", "", "")
        ex = f"Factor de área = {(100 + p) / 100:g}² = {float(f):g}: {ans_s.lower()}.".replace(".", ",", 0)
        return make(stem, fig, ans_s, pick4(ans_s, cands), Q_MOD, ex)
    cs = [(f"${int(c_):,}".replace(",", ".") if F(c_).denominator == 1 else None) for c_ in cands]
    cs = [c_ for c_ in cs if c_]
    ansf = f"${int(ans):,}".replace(",", ".")
    return make(stem, fig, ansf, pick4(ansf, cs), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_ratio_fig(r, l):
    n, m = pair(r, 1 if l == 0 else l)
    s0 = r.randint(1, 3) if l < 2 else r.randint(2, 4)
    a, b = n * s0, m * s0
    if l == 0:
        kind = "áreas"
        ans = ratio(n * n, m * m)
        fig = geo.sim_tris(F(m, n), dict(base=f"{a} cm"), dict(base=f"{b} cm"), "", "", ("Figura 1", "Figura 2"))
    elif l == 1:
        kind = r.choice(["áreas", "volúmenes"])
        ans = ratio(n * n, m * m) if kind == "áreas" else ratio(n ** 3, m ** 3)
        fig = geo.two_cubes(F(m, n), f"{a} cm", f"{b} cm", ("Cubo 1", "Cubo 2")) if True else ""
    else:
        kind = r.choice(["áreas", "volúmenes"])
        ans = ratio(n * n, m * m) if kind == "áreas" else ratio(n ** 3, m ** 3)
        fig = geo.two_cubes(F(m, n), f"{a} cm", f"{b} cm", ("Cuerpo 1", "Cuerpo 2"))
    cands = [ratio(n, m), ratio(n ** 3, m ** 3) if kind == "áreas" else ratio(n * n, m * m), ratio(m, n), f"{n * n}:{m}", f"{n}:{m * m}", ratio(m * m, n * n) if kind == "áreas" else ratio(m ** 3, n ** 3), f"{a}:{b}" if F(a, b) != F(n, m) or a == n else ratio(n + 1, m)]
    cands = [c_ for c_ in cands if c_ != ans and F(c_.split(":")[0]) / F(c_.split(":")[1]) != F(ans.split(":")[0]) / F(ans.split(":")[1])]
    stem = f"Las figuras son semejantes y las medidas indicadas son de lados homólogos. ¿Cuál es la razón entre las {kind} de la figura 1 y la figura 2?"
    return make(stem, fig, ans, pick4(ans, cands), Q_REP, f"Razón lineal {n}:{m}; razón de {kind} = {ans}.")


ORD = ["longitud", "área", "volumen"]


def t_curves(r, l):
    order = list(range(3)); r.shuffle(order)          # curva A,B,C -> magnitud (0=k,1=k²,2=k³)
    f = [lambda k: k, lambda k: k * k, lambda k: k ** 3]
    cols = [ACC, NAVY, "#475569"]
    ymax = 9
    pl = Plot(560, 285, 0, 3, 0, ymax)
    pl.axes(1, 1)
    for i, idx in enumerate(order):
        pl.curve(f[idx], 0, 3, cols[i], 4)
    pos = {0: 2.7, 1: 2.9, 2: 2.05}
    for i, idx in enumerate(order):
        k_ = {0: 2.55, 1: 2.7, 2: 2.05}[idx]
        pl.parts.append(tag(pl.X(k_), pl.Y(f[idx](k_)) - 20, "ABC"[i], 16))
    perm = lambda p: "; ".join(f"{'ABC'[i]}: {ORD[p[i]]}" for i in range(3))
    ans = perm(order)
    others = [perm(p) for p in itertools.permutations(range(3)) if list(p) != order]
    r.shuffle(others)
    stem = "El gráfico muestra cómo cambian, al multiplicar por k las dimensiones de un cuerpo, su longitud, su área y su volumen (en relación con los valores originales). ¿Qué magnitud representa cada curva?"
    return make(stem, pl.svg("Longitud, área y volumen según la razón k"), ans, others[:4], Q_REP, "Longitud ∝ k, área ∝ k² y volumen ∝ k³: la curva más empinada es el volumen.")


# ---------------------------------------------------------------- Argumentar
TRUE_A = ["Si la razón de semejanza de dos figuras es k, la razón entre sus áreas es k²", "Si la razón de semejanza de dos cuerpos es k, la razón entre sus volúmenes es k³",
          "Todos los círculos son semejantes entre sí", "La razón entre los perímetros de dos figuras semejantes es igual a la razón de semejanza", "Todos los triángulos equiláteros son semejantes entre sí"]
FALSE_A = ["Si se duplican las dimensiones de un cuerpo, su volumen también se duplica", "Dos rectángulos con lados proporcionales a los de otro son siempre semejantes entre sí sin importar el orden",
           "Si la razón de semejanza es k, la razón entre las áreas es 2k", "Todos los rectángulos son semejantes entre sí", "Si triplicamos los lados de un cuadrado, su área se triplica",
           "Dos triángulos isósceles cualesquiera son semejantes entre sí", "Si la razón de semejanza es 2, la razón entre los volúmenes es 6"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_A), r.sample(FALSE_A[:1] + FALSE_A[2:], 4)
        stem = "Sobre figuras y cuerpos semejantes, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_A[:1] + FALSE_A[2:]), r.sample(TRUE_A, 4)
        stem = "Sobre figuras y cuerpos semejantes, ¿cuál de las siguientes afirmaciones es FALSA?"
    n, m = pair(r, 1)
    fig = geo.sim_tris(F(m, n), dict(base="a"), dict(base="k·a"), "", "", ("Figura 1", "Figura 2"))
    return make(stem, fig, good, bad, Q_ARG, "Se aplica: longitudes ∝ k, áreas ∝ k², volúmenes ∝ k³; no todos los rectángulos ni triángulos isósceles son semejantes.")


def t_percent(r, l):
    n = 2 if l == 0 else r.choice([2, 3])
    p = r.choice([10, 20, 25, 50, 100]) if l < 2 else r.choice([10, 20, 30, 40, -10, -20, -25, -50])
    f = (1 + F(p, 100)) ** n
    chg = (f - 1) * 100
    what = "el área" if n == 2 else "el volumen"
    shape = "un cuadrado" if n == 2 else "un cubo"
    lab = lambda v: f"{what.capitalize()} {'aumenta' if v > 0 else 'disminuye'} {abs(float(v)):g}%".replace(".", ",")
    stem = f"Las dimensiones de {shape} {'aumentan' if p > 0 else 'disminuyen'} un {abs(p)}%. ¿Cuál de las siguientes afirmaciones es correcta?"
    ans = lab(chg)
    cands = [lab(F(p)), lab(F(n * p)), lab(chg + 10), lab(-chg), lab(F(p * (n + 1))), f"{what.capitalize()} {'aumenta' if p > 0 else 'disminuye'} {abs(p) * abs(p) / 100:g}%".replace(".", ",")]
    fig = geo.two_cubes(1 + p / 100 if p > 0 else 1, "lado", f"lado {'+' if p > 0 else '−'} {abs(p)}%") if n == 3 else geo.two_squares(1 + p / 100 if p > 0 else 1, "lado", f"lado {'+' if p > 0 else '−'} {abs(p)}%")
    return make(stem, fig, ans, pick4(ans, cands), Q_ARG, f"Factor = {(100 + p) / 100:g}^{n} = {float(f):g}: {ans.lower()}.".replace(".", ",", 0))


ERR = ["Aplicó la razón de semejanza a las áreas sin elevarla al cuadrado", "Usó el cuadrado de la razón para calcular volúmenes en lugar del cubo",
       "Invirtió la razón de semejanza al pasar de la figura menor a la mayor", "Sumó la razón de semejanza en lugar de multiplicar", "Comparó lados que no son homólogos"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    n, m = pair(r, 1)
    s0 = r.randint(1, 3)
    if k == 0:
        A = r.randint(2, 9) * n * n
        lines = [f"Lados homólogos: {n * s0} y {m * s0}; área menor = {A}", f"Razón de semejanza = {n}:{m}", f"Área mayor = {A}·{m}/{n} = {F(A * m, n)}"]
    elif k == 1:
        V = r.randint(2, 9) * n ** 3
        lines = [f"Aristas homólogas: {n * s0} y {m * s0}; volumen menor = {V}", f"Razón de semejanza = {n}:{m}", f"Volumen mayor = {V}·({m}/{n})² = {F(V * m * m, n * n)}"]
    elif k == 2:
        A = r.randint(2, 9) * m * m
        lines = [f"Lados homólogos: {n * s0} y {m * s0}; área mayor = {A}", f"Razón de semejanza (menor a mayor) = {m}:{n}", f"Área menor = {A}·({m}/{n})² = {F(A * m * m, n * n)}"]
    elif k == 3:
        A = r.randint(2, 9) * n * n
        lines = [f"Razón de semejanza {n}:{m}; área menor = {A}", f"Área mayor = {A} + ({m}/{n})²", f"Área mayor = {A + F(m * m, n * n)}"]
    else:
        A = r.randint(2, 9) * n * n
        lines = [f"Triángulos semejantes: lados de {n * s0} cm y {m * s0} cm (no homólogos)", f"Razón de semejanza = {n}:{m}; área menor = {A}", f"Área mayor = {A}·{m * m}/{n * n} = {F(A * m * m, n * n)}"]
    lines = [x.replace("-", "−").replace("/", "/") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 240, 17), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_compute(r, l):
    n, m = pair(r, l if l else 0)
    if l == 0:
        A1 = r.choice([2, 3, 5, 7, 10]) * n * n
        ask = r.choice(["A", "V"])
        if ask == "A":
            ans = A1 * F(m, n) ** 2
            stem = f"Dos figuras semejantes tienen razón de semejanza {n}:{m}. Si el área de la menor es {A1} cm², ¿cuál es el área de la mayor?"
            cands = [A1 * F(m, n), A1 * F(m, n) ** 3, A1 * F(n, m) ** 2, A1 + m - n, A1 * (m - n), A1 * 2]
            fig = geo.sim_tris(F(m, n), dict(base=f"{n}"), dict(base=f"{m}"), f"A = {A1}", "A = ?")
        else:
            V1 = r.choice([2, 3, 5]) * n ** 3
            ans = V1 * F(m, n) ** 3
            stem = f"Dos cuerpos semejantes tienen razón de semejanza {n}:{m}. Si el volumen del menor es {V1} cm³, ¿cuál es el volumen del mayor?"
            cands = [V1 * F(m, n), V1 * F(m, n) ** 2, V1 * F(n, m) ** 3, V1 + m ** 3 - n ** 3, V1 * (m - n), V1 * 2]
            fig = geo.two_cubes(F(m, n), f"{n}", f"{m}", (f"V = {V1}", "V = ?"))
        ex = "Se eleva la razón de semejanza al cuadrado (áreas) o al cubo (volúmenes)."
    elif l == 1:
        A1 = r.choice([1, 2, 3]) * n * n
        A2 = A1 * F(m, n) ** 2
        stem = f"Dos figuras semejantes tienen áreas de {num(A1)} cm² y {num(A2)} cm². ¿Cuál es la razón de semejanza (menor a mayor)?"
        ans_s = f"{n}:{m}"
        cands = [f"{n * n}:{m * m}", f"{m}:{n}", f"{n}:{m * m}", f"{n * n}:{m}", f"{n + 1}:{m}"]
        fig = geo.sim_tris(F(m, n), dict(base="a"), dict(base="?"), f"A = {num(A1)}", f"A = {num(A2)}")
        return make(stem, fig, ans_s, pick4(ans_s, cands), Q_PRO, f"Razón de áreas {n * n}:{m * m} ⟹ razón lineal {n}:{m}.")
    else:
        V1 = r.choice([1, 2, 3, 4]) * n ** 3
        V2 = V1 * F(m, n) ** 3
        A1 = r.choice([3, 5, 7, 8]) * n * n
        ans = A1 * F(m, n) ** 2
        stem = f"Dos cuerpos semejantes tienen volúmenes de {V1} cm³ y {num(V2)} cm³. Si la superficie del menor es {A1} cm², ¿cuál es la superficie del mayor?"
        cands = [A1 * F(m, n) ** 3, A1 * F(m, n), A1 * F(V2, V1), A1 * F(n, m) ** 2, A1 * (F(V2, V1) ** F(1, 3) if False else F(m, n)) + 1, A1 + (m - n)]
        fig = geo.two_cubes(F(m, n), f"V = {V1}", f"V = {num(V2)}", (f"S = {A1}", "S = ?"))
        ex = f"Razón de volúmenes {n ** 3}:{m ** 3} ⟹ razón lineal {n}:{m} ⟹ razón de áreas {n * n}:{m * m}: S = {num(ans)} cm²."
    cs = [num(c_) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    return make(stem, fig, num(ans), pick4(num(ans), cs), Q_PRO, ex)


def t_perim_area(r, l):
    n, m = pair(r, 1 if l == 0 else l)
    s0 = r.randint(2, 4)
    P1 = r.choice([6, 9, 12, 15, 18, 24]) * n
    if l == 0:
        P2 = F(P1 * m, n)
        stem = f"Dos triángulos semejantes tienen razón de semejanza {n}:{m}. Si el perímetro del menor es {P1} cm, ¿cuál es el perímetro del mayor?"
        ans = P2
        cands = [P1 * F(m, n) ** 2, P1 + m - n, P1 * F(n, m), P1 * (m - n), P1 * F(m, n) ** 3, P1 + s0]
        ex = f"Los perímetros están en la razón de semejanza: {P1}·{m}/{n} = {num(P2)}."
    else:
        A1 = r.choice([2, 3, 4, 5]) * n * n
        A2 = A1 * F(m, n) ** 2
        dif = A2 - A1
        stem = f"Dos polígonos semejantes tienen razón de semejanza {n}:{m}. Si el área del menor es {A1} cm², ¿cuántos cm² más grande es el área del mayor?"
        ans = dif
        cands = [A1 * F(m, n) - A1, A1 * (m - n), A1 * F(m, n) ** 2, A1 * F(m, n) ** 3 - A1, A2 + A1, A1 * F(m - n, n) ** 2 + 1]
        ex = f"Área mayor = {num(A2)}; diferencia = {num(A2)} − {A1} = {num(dif)}."
    fig = geo.sim_tris(F(m, n), dict(base=f"{n}"), dict(base=f"{m}"), "", "")
    cs = [num(c_) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    return make(stem, fig, num(ans), pick4(num(ans), cs), Q_PRO, ex)


BY_SKILL = {
    Q_RES: [t_area, t_volume],
    Q_MOD: [t_scale_ctx, t_pizza],
    Q_REP: [t_ratio_fig, t_curves],
    Q_ARG: [t_props, t_percent, t_error],
    Q_PRO: [t_compute, t_perim_area],
}
