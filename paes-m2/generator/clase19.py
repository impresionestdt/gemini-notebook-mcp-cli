"""Clase 19 · Trigonometría: problemas 2D y 3D (elevación, depresión y diagonales de cuerpos)."""
import itertools
from fractions import Fraction as F
from math import isqrt
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from mathfmt import E, fmt
from clase18 import Q, tv
import geo

BOXES = [(1, 2, 2, 3), (2, 3, 6, 7), (2, 10, 11, 15), (4, 4, 7, 9), (6, 6, 7, 11), (3, 4, 12, 13), (2, 6, 9, 11), (1, 4, 8, 9), (4, 12, 9, 15), (8, 9, 12, 17), (5, 6, 30, 31) if False else (4, 5, 20, 21), (6, 10, 15, 19)]
ANG = {30: "30°", 45: "45°", 60: "60°"}


def dec(x):
    return fs(F(x)) if F(x).denominator == 1 else f"{float(x):.4f}".rstrip("0").rstrip(".").replace(".", ",")


OBJS = ["torre", "edificio", "árbol", "mástil", "poste", "chimenea", "antena"]
HIGH = ["acantilado", "faro", "edificio", "torre de vigilancia"]
BOAT = ["bote", "barco", "lancha", "velero"]


def eyes(r):
    return r.choice([F(3, 2), F(2), F(1), F(5, 4)])


# ---------------------------------------------------------------- Resolver
def t_elev(r, l):
    ang = r.choice([30, 45, 60])
    if l == 0:
        d = r.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120])
        if ang == 30: d = d if d % 3 == 0 else d * 3
        ob = r.choice(OBJS)
        v = tv("tan", ang) * d
        stem = f"Desde un punto del suelo, situado a {d} m de la base de un(a) {ob}, el ángulo de elevación de su punta es {ang}°. ¿Cuál es la altura del(de la) {ob}?".replace("un(a) ", "un " if ob not in ("torre", "antena", "chimenea") else "una ").replace("del(de la) ", "del " if ob not in ("torre", "antena", "chimenea") else "de la ")
        ans = v.text()
        cs = [(tv("sen", ang) * d).text(), (tv("cos", ang) * d).text(), (Q(d, 0, 3 if ang != 45 else 2) / tv("tan", ang)).text() if ang != 45 else Q(d * 2, 0, 2).text(), Q(d, 0, 3 if ang != 45 else 2).text(), Q(0, d, 3 if ang != 45 else 2).text(), (v * 2).text()]
        fig = geo.elev_fig("elev", f"{d} m", "?", f"{ang}°")
        ex = f"Altura = {d}·tan {ang}° = {ans} m."
    elif l == 1:
        d = r.choice([30, 60, 90, 12, 24, 36, 18, 42, 48, 72, 120])
        e = eyes(r)
        ang = r.choice([30, 60]) if True else ang
        v = tv("tan", ang) * d + e
        stem = f"Un observador cuyos ojos están a {dec(e)} m del suelo se ubica a {d} m de un edificio y ve su punta bajo un ángulo de elevación de {ang}°. ¿Cuál es la altura del edificio?"
        ans = v.text()
        cs = [(tv("tan", ang) * d).text(), (tv("tan", ang) * d - e).text(), (tv("sen", ang) * d + e).text(), (tv("cos", ang) * d + e).text(), (tv("tan", ang) * (d + 1) + e).text(), Q(d + e, 0, 3).text()]
        fig = geo.elev_fig("elev", f"{d} m", "?", f"{ang}°", eye=f"{dec(e)} m")
        ex = f"Altura = {d}·tan {ang}° + {dec(e)} = {ans} m."
    else:
        d = r.choice([10, 20, 30, 40, 50, 60, 80, 100])
        # ángulos 45° (más lejos) y 60°... elegimos (30, 45) y (45, 60)
        pair = r.choice([(30, 45), (45, 60), (30, 60)])
        a1, a2 = pair
        t1, t2 = tv("tan", a1), tv("tan", a2)
        # distancias: h/t1 - h/t2 = d → h = d/(1/t1 - 1/t2)
        h = Q(d, 0, 3 if 45 not in pair or pair != (45, 60) else 3) if False else None
        inv1, inv2 = (Q(1, 0, 3 if a1 != 45 or a2 != 45 else 2) / tv("tan", a1)) if a1 != 45 else Q(1, 0, 3), None
        dd = 3
        def T3(a):
            return tv("tan", a) if a != 45 else Q(1, 0, 3)
        t1, t2 = T3(a1), T3(a2)
        h = Q(d, 0, 3) / (Q(1, 0, 3) / t1 - Q(1, 0, 3) / t2)
        stem = f"Desde dos puntos alineados con la base de una torre, separados por {d} m, se observa su punta bajo ángulos de elevación de {a1}° y {a2}°. ¿Cuál es la altura de la torre? (ignora la altura de los ojos)"
        ans = h.text()
        alts = [Q(d, 0, 3) * (Q(1, 0, 3) / (t1 - t2)) if False else h * 2, Q(F(d, 2), 0, 3), h + Q(1, 0, 3), Q(d, 0, 3) / t1, Q(d, 0, 3) * t2, (t2 - t1) * d]
        alts += [Q(d, 0, 3) * t1]
        cs = [a_.text() for a_ in alts if a_.key() != h.key()]
        fig = geo.elev_fig("elev", "", "?", f"{a1}°", ang2=f"{a2}°", dist2=f"{d} m")
        ex = f"h/tan {a1}° − h/tan {a2}° = {d} ⟹ h = {ans} m."
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


def t_dep(r, l):
    if l == 0:
        ang = r.choice([30, 45, 60])
        H = r.choice([30, 60, 90, 12, 18, 24, 36, 45, 120, 150, 48, 72])
        hi, bo = r.choice(HIGH), r.choice(BOAT)
        d = Q(H, 0, 3 if ang != 45 else 2) / (tv("tan", ang) if ang != 45 else Q(1, 0, 3)) if ang != 45 else Q(H, 0, 3)
        d = Q(H, 0, 3) / (tv("tan", ang) if ang != 45 else Q(1, 0, 3))
        stem = f"Desde lo alto de un(a) {hi} de {H} m de altura, el ángulo de depresión de un(a) {bo} es {ang}°. ¿A qué distancia horizontal de la base está?".replace("un(a) " + hi, ("una " if hi == "torre de vigilancia" else "un ") + hi).replace("un(a) " + bo, ("una " if bo == "lancha" else "un ") + bo)
        ans = d.text()
        tan = tv("tan", ang) if ang != 45 else Q(1, 0, 3)
        cs = [(Q(H, 0, 3) * tan).text(), (Q(H, 0, 3) * tv("sen", ang)).text() if ang != 45 else Q(0, F(H, 2), 2).text(), (Q(H, 0, 3) * tv("cos", ang)).text() if ang != 45 else Q(0, H, 2).text(), Q(H, 0, 3).text() if ang != 45 else Q(H * 2, 0, 3).text(), (d * 2).text(), (Q(H, 0, 3) / tv("sen", ang)).text() if ang != 45 else Q(0, H, 2).text()]
        fig = geo.elev_fig("dep", "?", f"{H} m", f"{ang}°")
        ex = f"tan {ang}° = {H}/d ⟹ d = {ans} m."
    elif l == 1:
        H = r.choice([30, 60, 90, 120, 18, 24, 36, 48, 72, 150])
        a1, a2 = r.choice([(45, 30), (60, 45), (60, 30)])
        T3 = lambda a: tv("tan", a) if a != 45 else Q(1, 0, 3)
        d1 = Q(H, 0, 3) / T3(a1)      # más cerca
        d2 = Q(H, 0, 3) / T3(a2)
        dist = d2 - d1
        stem = f"Desde lo alto de un faro de {H} m se observan dos botes alineados con su base, con ángulos de depresión de {a1}° y {a2}°. ¿Qué distancia hay entre los botes?"
        ans = dist.text()
        cs = [(d2 + d1).text(), d2.text(), d1.text(), (dist * 2).text(), (Q(H, 0, 3) * (T3(a1) - T3(a2))).text(), (T3(a1) - T3(a2)).text()]
        cs = [c for c in cs if c != ans]
        fig = geo.elev_fig("dep", "?", f"{H} m", f"{a1}°")
        ex = f"d₁ = {d1.text()} y d₂ = {d2.text()}; distancia = {ans} m."
    else:
        H = r.choice([30, 60, 90, 120, 150, 45, 24, 18, 36, 48])
        # base del otro edificio a 45°, punta a 30°
        d = H
        drop = Q(H, 0, 3) * tv("tan", 30)
        other = Q(H, 0, 3) - drop
        stem = f"Desde la azotea de un edificio de {H} m se ve la base de otro edificio con un ángulo de depresión de 45° y su punta con uno de 30°. ¿Cuál es la altura del otro edificio?"
        ans = other.text()
        cs = [drop.text(), (Q(H, 0, 3) + drop).text(), Q(H, 0, 3).text(), (Q(H, 0, 3) * tv("cos", 30)).text(), (Q(H, 0, 3) - Q(H, 0, 3) * tv("sen", 30)).text(), Q(0, H, 3).text()]
        cs = [c for c in cs if c != ans]
        fig = geo.elev_fig("dep", f"{H} m" if False else "?", f"{H} m", "45°")
        ex = f"Distancia = {H}; caída de la punta = {H}·tan 30° = {drop.text()}; altura = {H} − {drop.text()} = {ans} m."
    cs = [c for c in cs if c != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_box_ctx(r, l):
    a, b, c, d = r.choice(BOXES)
    perm = r.sample([a, b, c], 3)
    a, b, c = perm
    if l == 0:
        face = r.choice([(a, b), (a, c), (b, c)])
        diag = (face[0] ** 2 + face[1] ** 2) ** 0.5
        val = E((1, face[0] ** 2 + face[1] ** 2))
        stem = f"Una caja tiene dimensiones {a} cm × {b} cm × {c} cm. ¿Cuál es la longitud de la diagonal de la cara de dimensiones {face[0]} cm × {face[1]} cm?"
        ans = fmt(val)
        cs = [fmt(E((1, a * a + b * b + c * c))), str(face[0] + face[1]), fmt(E((1, abs(face[0] ** 2 - face[1] ** 2)))) if face[0] != face[1] else str(face[0] * 2), fmt(E((1, face[0] * face[1]))), fmt(E((1, (face[0] + face[1]) ** 2))), str(a + b + c)]
        fig = geo.box3d(a, b, c, dict(a=str(a), b=str(b), c=str(c)), diags=[("A", "C")] if face == (a, b) else [], letters=True)
        ex = f"d = √({face[0]}² + {face[1]}²) = {ans} cm."
    elif l == 1:
        stem = f"Una varilla debe guardarse dentro de una caja de {a} cm × {b} cm × {c} cm. ¿Cuál es la longitud máxima que puede tener la varilla?"
        ans = str(d)
        cs = [fmt(E((1, a * a + b * b))), fmt(E((1, a * a + c * c))), str(a + b + c), fmt(E((1, a * a + b * b + c * c + 1))), str(d + 1), str(d - 1), fmt(E((1, b * b + c * c)))]
        fig = geo.box3d(a, b, c, dict(a=str(a), b=str(b), c=str(c)), diags=[("A", "G")], letters=True)
        ex = f"d = √({a}² + {b}² + {c}²) = √{a * a + b * b + c * c} = {d} cm."
    else:
        base_d = (a * a + b * b)
        stem = f"Una caja tiene base de {a} m × {b} m y altura {c} m. Una cuerda va desde una esquina inferior hasta la esquina superior opuesta (diagonal espacial). ¿Cuánto vale sen θ, donde θ es el ángulo que forma la cuerda con el piso?"
        ans = fs(F(c, d))
        cs = [fs(F(d, c)), fmt(E((F(1, d), base_d))), fs(F(c * c, d * d)), fmt(E((F(1, c), base_d))), fs(F(c, a + b)), fs(F(a, d))]
        cs = [x for x in cs if x != ans]
        fig = geo.box3d(a, b, c, dict(a=f"{a} m", b=f"{b} m", c=f"{c} m"), diags=[("A", "G"), ("A", "C")], dashed=[("A", "C")])
        ex = f"Diagonal espacial = {d} m; sen θ = altura/diagonal = {c}/{d}."
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def t_ramp_ctx(r, l):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
    k = r.choice([2, 3, 4])
    thing = r.choice(["un cometa", "un globo", "un dron"])
    if l == 0:
        # ángulo de elevación cuya tan = a/b
        stem = f"Un observador ve {thing} bajo un ángulo de elevación θ con tan θ = {a}/{b}. Si el objeto está {a * k} m más alto que los ojos del observador, ¿a qué distancia horizontal se encuentra?"
        ans = fs(b * k)
        cs = [fs(a * k), fs(c * k), fs(F(a * k * a, b)), fs(b * k + a * k), fs(F(b * k * b, a)), fs(F(a * k * c, b))]
        labs = dict(opp=f"{a * k} m", adj="?")
        ex = f"tan θ = {a * k}/d ⟹ d = {a * k}·{b}/{a} = {b * k} m."
    elif l == 1:
        stem = f"Una persona observa {thing} bajo un ángulo de elevación θ con sen θ = {a}/{c}. Si la línea de visión mide {c * k} m, ¿a qué altura sobre el nivel de sus ojos está el objeto?"
        ans = fs(a * k)
        cs = [fs(b * k), fs(c * k), fs(a * k + b * k), fs(F(a * k * c, b)), fs(F(c * k * b, a)), fs(a * k + 1)]
        labs = dict(opp="?", hyp=f"{c * k} m")
        ex = f"Altura = {c * k}·{a}/{c} = {a * k} m."
    else:
        e = eyes(r)
        stem = f"Los ojos de un observador están a {dec(e)} m del suelo. Ve {thing} con un ángulo de elevación θ, tan θ = {a}/{b}, a {b * k} m de distancia horizontal. ¿A qué altura sobre el suelo está el objeto?"
        val = a * k + e
        ans = dec(val)
        cs = [dec(a * k), dec(a * k - e), dec(c * k + e), dec(F(a * k * a, b) + e), dec(val + 1), dec(b * k + e)]
        labs = dict(opp="?", adj=f"{b * k} m")
        ex = f"Altura sobre los ojos = {b * k}·{a}/{b} = {a * k}; total = {a * k} + {dec(e)} = {dec(val)} m."
    cs = [c_ for c_ in cs if c_ != ans]
    fig = geo.elev_fig("elev", labs.get("adj", ""), labs.get("opp", ""), "θ")
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
def t_equation(r, l):
    ang = r.choice([30, 45, 60])
    d = r.choice([20, 30, 40, 50, 60])
    kind = "elev" if l == 0 else r.choice(["elev", "dep"])
    if kind == "elev":
        stem = f"En la figura, el ángulo de elevación de la punta de la torre es {ang}° y la distancia horizontal al observador es {d} m. ¿Cuál de las siguientes ecuaciones permite calcular la altura x de la torre?"
        fig = geo.elev_fig("elev", f"{d} m", "x", f"{ang}°")
        ans = f"tan {ang}° = x/{d}"
        cs = [f"tan {ang}° = {d}/x", f"sen {ang}° = x/{d}", f"cos {ang}° = x/{d}", f"tan {90 - ang}° = x/{d}", f"sen {ang}° = {d}/x", f"tan {ang}° = x·{d}", f"cos {ang}° = {d}/x"]
    else:
        stem = f"En la figura, el ángulo de depresión desde lo alto del acantilado hasta el bote es {ang}° y el acantilado mide {d} m. ¿Cuál de las siguientes ecuaciones permite calcular la distancia horizontal x del bote a la base del acantilado?"
        fig = geo.elev_fig("dep", "x", f"{d} m", f"{ang}°")
        ans = f"tan {ang}° = {d}/x"
        cs = [f"tan {ang}° = x/{d}", f"sen {ang}° = {d}/x", f"cos {ang}° = x/{d}", f"tan {90 - ang}° = {d}/x", f"sen {ang}° = x/{d}", f"tan {ang}° = x·{d}", f"cos {ang}° = {d}/x"]
    if l == 2:
        e = r.choice([2, 3, 4])
        if kind == "elev":
            stem = f"Los ojos del observador están a {e} m del suelo, el ángulo de elevación de la punta de la torre es {ang}° y la distancia horizontal es {d} m. ¿Cuál ecuación da la altura x de la torre?"
            fig = geo.elev_fig("elev", f"{d} m", "x", f"{ang}°", eye=f"{e} m")
            ans = f"x = {d}·tan {ang}° + {e}"
            cs = [f"x = {d}·tan {ang}°", f"x = {d}·tan {ang}° − {e}", f"x = {d}·sen {ang}° + {e}", f"x = {d}/tan {ang}° + {e}", f"x = ({d} + {e})·tan {ang}°", f"x = {d}·cos {ang}° + {e}"]
    cs = list(dict.fromkeys(cs))
    return make(stem, fig, ans, pick4(ans, cs), Q_REP, "Se identifica el triángulo rectángulo y las razones que relacionan el ángulo con los lados conocidos.")


TRI = {"AG": ("A", "C", "G"), "BH": ("B", "D", "H"), "CE": ("C", "A", "E"), "DF": ("D", "B", "F")}


def t_box_triangle(r, l):
    a, b, c, d = r.choice(BOXES)
    diag = r.choice(list(TRI))
    tri = "".join(TRI[diag])
    stem_target = r.choice(["la base ABCD", "el piso ABCD"])
    good = f"Triángulo {tri}"
    v = "ABCDEFGH"
    others = []
    tri_set = set(TRI[diag])
    for t in itertools.combinations(v, 3):
        if set(t) != tri_set:
            others.append("".join(t))
    # distractores plausibles: incluyen la diagonal o parte de ella
    p, q = diag
    plaus = []
    for x in v:
        for y in v:
            pass
    plaus = [f"Triángulo {p}{x}{q}" for x in v if x not in (p, q) and set((p, x, q)) != tri_set][:12]
    plaus = [t for t in plaus]
    r.shuffle(plaus)
    cs = plaus
    fig = geo.box3d(a, b, c, dict(a=str(a), b=str(b), c=str(c)), diags=[(diag[0], diag[1])])
    stem = f"En la caja rectangular ABCDEFGH de la figura (ABCD es la base y EFGH la tapa), se traza la diagonal {diag}. ¿En cuál de los siguientes triángulos rectángulos se puede calcular el ángulo que forma la diagonal {diag} con {stem_target}?"
    return make(stem, fig, good, pick4(good, cs), Q_REP, f"El ángulo entre la diagonal y la base está en el triángulo formado por la diagonal, la diagonal de la base y la arista vertical: {tri}.")


# ---------------------------------------------------------------- Argumentar
TRUE_E = ["El ángulo de depresión desde A hasta B es igual al ángulo de elevación desde B hasta A", "El ángulo de elevación se mide desde la horizontal hacia arriba de la línea de visión",
          "En una caja de dimensiones a, b y c, la diagonal espacial mide √(a² + b² + c²)", "La diagonal de una cara de dimensiones a y b mide √(a² + b²)",
          "Si un observador se acerca a una torre, el ángulo de elevación de su punta aumenta"]
FALSE_E = ["El ángulo de depresión se mide desde la vertical hacia abajo", "La diagonal de un cubo de arista a mide a√2", "Si un observador se aleja de una torre, el ángulo de elevación de su punta aumenta",
           "En una caja de dimensiones a, b y c, la diagonal espacial mide a + b + c", "El ángulo de elevación y el de depresión entre dos puntos suman 90°",
           "La diagonal espacial de una caja es siempre menor que la diagonal de cualquiera de sus caras"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_E), r.sample(FALSE_E, 4)
        stem = "Sobre problemas de trigonometría en el plano y en el espacio, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_E), r.sample(TRUE_E, 4)
        stem = "Sobre problemas de trigonometría en el plano y en el espacio, ¿cuál de las siguientes afirmaciones es FALSA?"
    a, b, c, d = r.choice(BOXES)
    fig = geo.elev_fig("elev", "", "", "θ") if l == 0 else geo.box3d(a, b, c, {}, diags=[("A", "G")])
    return make(stem, fig, good, bad, Q_ARG, "Se razona con las definiciones de ángulo de elevación y de depresión y con el teorema de Pitágoras en el espacio.")


COMP = ["Está más cerca el observador que ve con el ángulo mayor", "Está más cerca el observador que ve con el ángulo menor", "Ambos están a la misma distancia de la torre",
        "Depende de la altura de los ojos de cada observador", "No se puede saber sin conocer la altura de la torre"]


def t_compare(r, l):
    a1, a2 = sorted(r.sample([30, 45, 60], 2))
    if l == 0:
        stem = f"Dos observadores, con los ojos a la misma altura, miran la punta de una misma torre con ángulos de elevación de {a1}° y {a2}°. ¿Cuál afirmación es correcta?"
        ans = COMP[0]
        others = COMP[1:]
        fig = geo.elev_fig("elev", "", "", f"{a1}°", ang2=f"{a2}°", dist2="")
        return make(stem, fig, ans, others, Q_ARG, "Como tan θ = h/d, a mayor ángulo (misma altura) menor distancia.")
    T3 = lambda a: tv("tan", a) if a != 45 else Q(1, 0, 3)
    ratio = T3(a2) / T3(a1)      # d1/d2 = tan a2 / tan a1
    stem = f"Dos observadores miran la punta de una misma torre con ángulos de elevación de {a1}° y {a2}° (ojos a igual altura). ¿Cuántas veces mayor es la distancia del primer observador que la del segundo?"
    ans = ratio.text()
    cs = [(Q(1, 0, 3) / ratio).text(), (ratio * ratio).text(), Q(F(a2, a1), 0, 3).text(), (T3(a2) - T3(a1)).text(), (tv("sen", a2) / tv("sen", a1)).text() if a1 != 45 and a2 != 45 else Q(2, 0, 3).text(), (T3(a1) * T3(a2)).text()]
    cs = [c for c in dict.fromkeys(cs) if c != ans]
    fig = geo.elev_fig("elev", "", "h", f"{a1}°", ang2=f"{a2}°", dist2="")
    return make(stem, fig, ans, pick4(ans, cs), Q_ARG, f"d = h/tan θ ⟹ d₁/d₂ = tan {a2}°/tan {a1}° = {ans}.")


ERR = ["Usó el ángulo de depresión como si se midiera desde la vertical", "Confundió la altura con la distancia horizontal al plantear la razón",
       "Olvidó sumar la altura de los ojos del observador", "Calculó la diagonal de una cara en lugar de la diagonal espacial", "Usó seno en lugar de tangente"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([1, 2, 3])
    H = r.choice([30, 60, 90])
    d = r.choice([20, 30, 60])
    if k == 0:
        lines = [f"Acantilado de {H} m; ángulo de depresión 30°", f"tan 60° = {H}/x", f"x = {H}/√3"]
    elif k == 1:
        lines = [f"Torre de altura x; distancia {d} m; elevación 30°", f"tan 30° = {d}/x", f"x = {d}·√3"]
    elif k == 2:
        lines = [f"Ojos a 1,5 m; distancia {d} m; elevación 45°", f"altura = {d}·tan 45° = {d} m", f"La torre mide {d} m"]
    elif k == 3:
        a, b, c, dd = r.choice(BOXES)
        lines = [f"Caja de {a} × {b} × {c}", f"diagonal espacial = √({a}² + {b}²)", f"diagonal espacial = √{a * a + b * b}"]
    else:
        lines = [f"Torre de altura x; distancia {d} m; elevación 30°", f"sen 30° = x/{d}", f"x = {d}/2 = {fs(F(d, 2))}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 220, 18), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el planteamiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_height(r, l):
    if l == 0:
        a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
        k = r.choice([2, 3, 4, 5, 6, 7, 8, 10])
        stem = f"Desde un punto a {b * k} m de la base de un poste, el ángulo de elevación de su punta cumple tan θ = {a}/{b}. ¿Cuál es la altura del poste?"
        ans = fs(a * k)
        cs = [fs(b * k), fs(c * k), fs(a * k + b * k), fs(F(b * k * b, a)), fs(a * k + 1), fs(F(b * k * c, a))]
        fig = geo.elev_fig("elev", f"{b * k} m", "?", "θ")
    elif l == 1:
        ang = r.choice([30, 60])
        h = r.choice([12, 18, 24, 30, 6, 36])
        d = Q(h, 0, 3) / tv("tan", ang)
        stem = f"El ángulo de elevación de la punta de una torre de {h} m es {ang}°. ¿A qué distancia horizontal de su base está el observador? (ignora la altura de los ojos)"
        ans = d.text()
        cs = [(Q(h, 0, 3) * tv("tan", ang)).text(), (Q(h, 0, 3) * tv("sen", ang)).text(), (Q(h, 0, 3) * tv("cos", ang)).text(), Q(h, 0, 3).text(), (d * 2).text(), (Q(h, 0, 3) / tv("sen", ang)).text()]
        fig = geo.elev_fig("elev", "?", f"{h} m", f"{ang}°")
    else:
        a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
        k = r.choice([2, 3, 4])
        e = eyes(r)
        stem = f"Un observador con los ojos a {fs(e) if e.denominator == 1 else dec(e)} m del suelo ve la punta de una torre con un ángulo de elevación θ, sen θ = {a}/{c}. Si la línea de visión mide {c * k} m, ¿cuál es la altura de la torre?"
        val = a * k + e
        ans = dec(val)
        cs = [dec(a * k), dec(c * k + e), dec(b * k + e), dec(a * k - e), dec(val + 1), dec(F(a * k * a, c) + e)]
        fig = geo.elev_fig("elev", "", "?", "θ", eye=f"{dec(e)} m")
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, "Se plantea la razón trigonométrica correspondiente y se resuelve (sumando la altura de los ojos cuando corresponde).")


def t_solid(r, l):
    a, b, c, d = r.choice(BOXES)
    a, b, c = r.sample([a, b, c], 3)
    if l == 0:
        a = r.randint(2, 15)
        stem = f"Un cubo tiene arista {a} cm. ¿Cuánto mide su diagonal espacial?"
        ans = fmt(E((a, 3)))
        cs = [fmt(E((a, 2))), str(3 * a), fmt(E((a * a, 1))) if False else str(a * a), fmt(E((a, 6))), fmt(E((1, 3 * a))), str(2 * a)]
        fig = geo.box3d(1, 1, 1, dict(a=f"{a} cm", b=f"{a} cm", c=f"{a} cm"), diags=[("A", "G")])
        ex = f"d = a√3 = {ans} cm."
    elif l == 1:
        stem = f"En una caja de {a} m × {b} m × {c} m, ¿cuánto mide la diagonal espacial?"
        ans = str(d)
        cs = [fmt(E((1, a * a + b * b))), fmt(E((1, a * a + c * c))), str(a + b + c), str(d + 1), str(d - 1), fmt(E((1, a * b + c * c)))]
        fig = geo.box3d(a, b, c, dict(a=f"{a} m", b=f"{b} m", c=f"{c} m"), diags=[("A", "G")])
        ex = f"d = √({a}² + {b}² + {c}²) = {d}."
    else:
        stem = f"En una caja de base {a} m × {b} m y altura {c} m, la diagonal espacial forma un ángulo θ con la base. ¿Cuánto vale tan θ?"
        base = E((1, a * a + b * b))
        ans = fmt(E((F(c, a * a + b * b), a * a + b * b)))
        cs = [fs(F(c, d)), fmt(E((F(1, c), a * a + b * b))), fs(F(d, c)), fmt(E((F(a, a * a + b * b), a * a + b * b))), fs(F(c, a + b)), fmt(E((F(c, 1), a * a + b * b)))]
        fig = geo.box3d(a, b, c, dict(a=f"{a} m", b=f"{b} m", c=f"{c} m"), diags=[("A", "G"), ("A", "C")], dashed=[("A", "C")])
        ex = f"Diagonal de la base = √({a * a + b * b}); tan θ = {c}/√({a * a + b * b}) = {ans}."
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, ex)


BY_SKILL = {
    Q_RES: [t_elev, t_dep],
    Q_MOD: [t_box_ctx, t_ramp_ctx],
    Q_REP: [t_equation, t_box_triangle],
    Q_ARG: [t_props, t_compare, t_error],
    Q_PRO: [t_height, t_solid],
}
