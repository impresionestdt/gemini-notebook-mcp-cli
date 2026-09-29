"""Clase 18 · Trigonometría básica: seno, coseno y tangente."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from mathfmt import E, fmt
import geo

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (6, 8, 10), (9, 12, 15), (12, 16, 20), (10, 24, 26), (15, 20, 25), (12, 35, 37)]


def fr(a, b):
    g = F(a, b)
    return fs(g)


def ratios(o, a, h):
    return {"sen": F(o, h), "cos": F(a, h), "tan": F(o, a)}


def wrong_ratios(o, a, h):
    return [F(a, h), F(o, h), F(o, a), F(a, o), F(h, o), F(h, a), F(o + a, h), F(h - o, h), F(h - a, h)]


NM = {"sen": "sen α", "cos": "cos α", "tan": "tan α"}


# ---------------------------------------------------------------- valores exactos
class Q:
    """Números a + b√d con d ∈ {2, 3} (d fijo por expresión)."""
    def __init__(s, a, b=0, d=3): s.a, s.b, s.d = F(a), F(b), d
    def __add__(s, o): o = o if isinstance(o, Q) else Q(o, 0, s.d); return Q(s.a + o.a, s.b + o.b, s.d)
    def __sub__(s, o): o = o if isinstance(o, Q) else Q(o, 0, s.d); return Q(s.a - o.a, s.b - o.b, s.d)
    def __mul__(s, o): o = o if isinstance(o, Q) else Q(o, 0, s.d); return Q(s.a * o.a + s.d * s.b * o.b, s.a * o.b + s.b * o.a, s.d)
    def inv(s):
        den = s.a * s.a - s.d * s.b * s.b
        return Q(s.a / den, -s.b / den, s.d)
    def __truediv__(s, o): o = o if isinstance(o, Q) else Q(o, 0, s.d); return s * o.inv()
    def val(s): return float(s.a) + float(s.b) * s.d ** 0.5
    def text(s): return fmt(E((s.a, 1), (s.b, s.d))) if (s.a != 0 or s.b != 0) else "0"
    def key(s): return (s.a, s.b, s.d)


def tv(fn, ang):
    """Valor exacto de sen/cos/tan en 30°, 45° o 60°."""
    if ang == 45:
        h = Q(0, F(1, 2), 2)
        return {"sen": h, "cos": h, "tan": Q(1, 0, 2)}[fn]
    if ang == 30:
        return {"sen": Q(F(1, 2), 0, 3), "cos": Q(0, F(1, 2), 3), "tan": Q(0, F(1, 3), 3)}[fn]
    return {"sen": Q(0, F(1, 2), 3), "cos": Q(F(1, 2), 0, 3), "tan": Q(0, 1, 3)}[fn]


# ---------------------------------------------------------------- Resolver
def t_ratio(r, l):
    a, b, c = r.choice(TRIPLES)
    k = r.choice([1, 1, 2, 3]) if l == 0 else 1
    if r.random() < 0.5: a, b = b, a
    o, ad, h = a * k, b * k, c * k              # opuesto, adyacente, hipotenusa de α
    fn = r.choice(["sen", "cos", "tan"])
    R_ = ratios(o, ad, h)
    if l == 0:
        stem = f"En el triángulo rectángulo de la figura, el cateto opuesto a α mide {o}, el adyacente {ad} y la hipotenusa {h}. ¿Cuánto vale {NM[fn]}?"
        labs = dict(opp=str(o), adj=str(ad), hyp=str(h))
    elif l == 1:
        hide = r.choice(["o", "a"])
        if hide == "o":
            stem = f"En el triángulo rectángulo de la figura, el cateto adyacente a α mide {ad} y la hipotenusa {h}. ¿Cuánto vale {NM[fn]}?"
            labs = dict(adj=str(ad), hyp=str(h), opp="?")
        else:
            stem = f"En el triángulo rectángulo de la figura, el cateto opuesto a α mide {o} y la hipotenusa {h}. ¿Cuánto vale {NM[fn]}?"
            labs = dict(opp=str(o), hyp=str(h), adj="?")
    else:
        stem = f"En el triángulo rectángulo de la figura, el cateto opuesto a α mide {o} y el cateto adyacente {ad}. ¿Cuánto vale {NM[fn]}?"
        labs = dict(opp=str(o), adj=str(ad), hyp="?")
    ans = fs(R_[fn])
    others = [w for w in wrong_ratios(o, ad, h) if w != R_[fn]]
    cs = [fs(w) for w in others]
    fig = geo.trig_tri(ad, o, labs)
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, f"{NM[fn]} = {'cateto opuesto/hipotenusa' if fn == 'sen' else 'cateto adyacente/hipotenusa' if fn == 'cos' else 'cateto opuesto/cateto adyacente'} = {ans}.")


def t_side(r, l):
    if l == 0:
        a, b, c = r.choice(TRIPLES[:6])
        k = r.choice([2, 3, 4, 5])
        fn = r.choice(["sen", "cos"])
        h = c * k
        if fn == "sen":
            stem = f"En un triángulo rectángulo, sen α = {a}/{c} y la hipotenusa mide {h}. ¿Cuánto mide el cateto opuesto a α?"
            ans = a * k
            labs = dict(opp="x", hyp=str(h), adj=""); adj_, opp_ = b, a
            cands = [b * k, h - a, h * a, F(h * c, a), a * c, a * k + 1]
        else:
            stem = f"En un triángulo rectángulo, cos α = {b}/{c} y la hipotenusa mide {h}. ¿Cuánto mide el cateto adyacente a α?"
            ans = b * k
            labs = dict(adj="x", hyp=str(h), opp=""); adj_, opp_ = b, a
            cands = [a * k, h - b, h * b, F(h * c, b), b * c, b * k + 1]
        cs = [fs(F(c_)) for c_ in cands if F(c_) != ans]
        fig = geo.trig_tri(adj_, opp_, labs)
        return make(stem, fig, str(ans), pick4(str(ans), cs), Q_RES, f"{'Opuesto' if fn == 'sen' else 'Adyacente'} = hipotenusa·razón = {h}·{fn}: {ans}.")
    if l == 1:
        ang = r.choice([30, 45, 60])
        h = r.choice([4, 6, 8, 10, 12, 14, 16, 20])
        fn = r.choice(["sen", "cos"]) if ang != 45 else "sen"
        d = 2 if ang == 45 else 3
        v = tv(fn, ang) * h if True else None
        v = Q(v.a, v.b, v.d)
        side = "opuesto" if fn == "sen" else "adyacente"
        stem = f"En un triángulo rectángulo, un ángulo agudo mide {ang}° y la hipotenusa mide {h} cm. ¿Cuánto mide el cateto {side} a ese ángulo?"
        ans = v.text()
        alts = [tv("cos" if fn == "sen" else "sen", ang) * h, tv("tan", ang) * h, Q(h, 0, d), Q(0, h, d), tv(fn, ang) * (h // 2 or 1), Q(F(h, 2), 0, d) if False else tv(fn, ang) * (h + 2)]
        cs = [a_.text() for a_ in alts if a_.key() != v.key()]
        fig = geo.trig_tri(1, 1 if ang == 45 else (0.58 if ang == 30 else 1.73), dict(hyp=f"{h} cm", adj="" if fn == "sen" else "x", opp="x" if fn == "sen" else ""), ang=f"{ang}°")
        return make(stem, fig, ans, pick4(ans, cs), Q_RES, f"Cateto {side} = {h}·{fn} {ang}° = {ans} cm.")
    p, q = r.choice([(5, 12), (3, 4), (8, 15), (7, 24), (20, 21)])
    k = r.choice([2, 3, 4])
    adj = q * k
    opp = p * k
    hyp = F(F(p, 1) ** 2 + F(q, 1) ** 2).limit_denominator(1)
    c = {(5, 12): 13, (3, 4): 5, (8, 15): 17, (7, 24): 25, (20, 21): 29}[(p, q)]
    stem = f"En un triángulo rectángulo, tan α = {p}/{q} y el cateto adyacente a α mide {adj}. ¿Cuánto mide la hipotenusa?"
    ans = c * k
    cands = [adj + opp, opp, adj * c, F(adj * c, p), c * k + k, c + k, adj * p // 1, adj * q]
    cs = [fs(F(c_)) for c_ in cands if F(c_) != ans]
    fig = geo.trig_tri(q, p, dict(adj=str(adj), hyp="x", opp="?"))
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_RES, f"Opuesto = {opp}; hipotenusa = √({opp}² + {adj}²) = {ans}.")


# ---------------------------------------------------------------- Modelar
def t_ctx(r, l):
    a, b, c = r.choice(TRIPLES[:6])
    k = r.choice([1, 2, 3]) if l > 0 else 1
    if l == 0:
        thing = r.choice(["escalera", "rampa", "tirante"])
        h, base, L_ = a * k, b * k, c * k
        fn = r.choice(["sen", "cos", "tan"])
        stem = f"Una {thing} de {L_} m de largo llega a una altura de {h} m sobre el suelo, quedando su base a {base} m del pie de la pared. Si α es el ángulo que forma con el suelo, ¿cuánto vale {NM[fn]}?"
        ans = fs(ratios(h, base, L_)[fn])
        cs = [fs(w) for w in wrong_ratios(h, base, L_) if w != ratios(h, base, L_)[fn]]
        labs = dict(opp=f"{h} m", adj=f"{base} m", hyp=f"{L_} m")
        ex = f"{NM[fn]} = {ans}."
    elif l == 1:
        h, L_ = a * k, c * k
        stem = f"Una escalera de {L_} m forma con el suelo un ángulo α tal que sen α = {a}/{c}. ¿A qué altura llega la escalera sobre la pared?"
        ans = fs(h)
        cs = [fs(F(c_)) for c_ in [b * k, L_ - h, L_ * a, F(L_ * c, a), h + 1, h - 1 if h > 1 else h + 2]]
        cs = [c_ for c_ in cs if c_ != ans]
        labs = dict(opp="?", adj="", hyp=f"{L_} m")
        ex = f"Altura = {L_}·{a}/{c} = {h} m."
    else:
        thing = r.choice(["techo", "rampa de acceso"])
        base = b * k * 2
        stem = f"Un {thing} tiene un ángulo α con la horizontal tal que tan α = {a}/{b}. Si su proyección horizontal mide {base} m, ¿cuánto mide su longitud inclinada (hipotenusa)?"
        ans = fs(c * k * 2)
        cs = [fs(F(c_)) for c_ in [base + a * k * 2, a * k * 2, base * c, F(base * c, a), c * k * 2 + 2, c * 2]]
        cs = [c_ for c_ in cs if c_ != ans]
        labs = dict(opp="", adj=f"{base} m", hyp="?")
        ex = f"Altura = {base}·{a}/{b} = {a * k * 2}; longitud = √({a * k * 2}² + {base}²) = {c * k * 2} m."
        a, b = a, b
    fig = geo.trig_tri(b, a, labs)
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def t_sun(r, l):
    a, b, c = r.choice(TRIPLES[:6])
    k = r.choice([2, 3, 4, 5]) if l > 0 else 2
    H, S, D = a * k, b * k, c * k
    fn = r.choice(["sen", "cos", "tan"]) if l < 2 else r.choice(["sen", "cos"])
    if l < 2:
        stem = f"Un poste de {H} m proyecta una sombra de {S} m. Si θ es el ángulo de elevación del Sol, ¿cuánto vale {fn} θ?" if fn == "tan" else f"Un poste de {H} m proyecta una sombra de {S} m. Si θ es el ángulo de elevación del Sol y el rayo solar que pasa por la punta del poste llega al suelo a {D} m de su base, ¿cuánto vale {fn} θ?"
        R_ = ratios(H, S, D)
        ans = fs(R_[fn])
        cs = [fs(w) for w in wrong_ratios(H, S, D) if w != R_[fn]]
        labs = dict(opp=f"{H} m", adj=f"{S} m", hyp=f"{D} m" if fn != "tan" else "")
    else:
        stem = f"La sombra de un edificio mide {S} m y el ángulo de elevación del Sol cumple tan θ = {fr(H, S)}. ¿Cuánto mide el edificio?"
        ans = fs(H)
        cs = [fs(F(c_)) for c_ in [S + H, F(S * S, H), S * a, D, H + 1, F(S * b, a) if a else 1]]
        cs = [c_ for c_ in cs if c_ != ans]
        labs = dict(opp="?", adj=f"{S} m", hyp="")
    fig = geo.trig_tri(S, H, labs, ang="θ")
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, "Se usa la razón trigonométrica adecuada en el triángulo rectángulo formado por el objeto, su sombra y el rayo solar.")


# ---------------------------------------------------------------- Representar
RAT = {"sen": ("a", "c"), "cos": ("b", "c"), "tan": ("a", "b")}   # respecto de α en A: a opuesto, b adyacente, c hipotenusa


LSETS = [("a", "b", "c"), ("p", "q", "r"), ("x", "y", "z"), ("m", "n", "t")]
VSETS = [("A", "B", "C"), ("P", "Q", "R"), ("M", "N", "O"), ("D", "E", "F")]


def t_letter_ratio(r, l):
    la, lb, lc = r.choice(LSETS)
    va = r.choice(VSETS)
    fn = r.choice(["sen", "cos", "tan"])
    ang = "α" if l == 0 else r.choice(["α", "β"])
    sub = {"a": la, "b": lb, "c": lc}
    if ang == "α":
        num, den = RAT[fn]
    else:
        num, den = {"sen": ("b", "c"), "cos": ("a", "c"), "tan": ("b", "a")}[fn]
    allr = ["a/b", "b/a", "a/c", "c/a", "b/c", "c/b"]
    rn = lambda t: "/".join(sub[x] for x in t.split("/"))
    ans = rn(f"{num}/{den}")
    cs = [rn(x) for x in allr if x != f"{num}/{den}"]
    r.shuffle(cs)
    labs = dict(opp=la, adj=lb, hyp=lc)
    fig = geo.trig_tri(r.choice([1.2, 1.5, 1.0, 2.0]), 1, labs, show_other="β", names=va)
    stem = f"En el triángulo rectángulo de la figura (recto en {va[2]}), ¿cuál de las siguientes razones representa {fn} {ang}?"
    ex = f"Con respecto a {ang}: opuesto y adyacente se identifican en la figura; {fn} {ang} = {ans}."
    if l == 2:
        pairs = {"sen": "cos", "cos": "sen"}
        if fn == "tan":
            fn = "sen"; num, den = (RAT["sen"] if ang == "α" else ("b", "c"))
        ans = rn(f"{num}/{den}")
        cs = [rn(x) for x in allr if x != f"{num}/{den}"]
        r.shuffle(cs)
        other = "α" if ang == "β" else "β"
        f2 = pairs[fn]
        stem = f"En el triángulo rectángulo de la figura (recto en {va[2]}), {fn} {ang} es igual a {f2} {other}. ¿Cuál de las siguientes razones es el valor común de ambos?"
        ex = "Los ángulos agudos de un triángulo rectángulo son complementarios: el seno de uno es el coseno del otro."
    return make(stem, fig, ans, pick4(ans, cs), Q_REP, ex)


def t_table(r, l):
    angs = [30, 45, 60]
    fns = ["sen", "cos", "tan"]
    def cell(fn, ang): return tv(fn, ang)
    if l == 0:
        pool = [(fn, 45) for fn in fns] + [("sen", 30), ("cos", 60)]
    elif l == 1:
        pool = [(fn, a_) for fn in fns for a_ in (30, 60)]
    else:
        pool = [(fn, a_) for fn in fns for a_ in angs]
    fn, ang = r.choice(pool)
    v = cell(fn, ang)
    body = R(30, 30, 500, 40, "#E0F2FE") + R(30, 70, 500, 130, WHITE)
    cw = 500 / 4
    hdr = ["", "sen", "cos", "tan"]
    for j, t in enumerate(hdr): body += T(30 + cw * (j + 0.5), 57, t, 20)
    for i, a_ in enumerate(angs):
        body += T(30 + cw * 0.5, 100 + 40 * i, f"{a_}°", 20)
        for j, f_ in enumerate(fns):
            txt = "?" if (f_, a_) == (fn, ang) else cell(f_, a_).text()
            body += T(30 + cw * (j + 1.5), 100 + 40 * i, txt, 19)
    for j in range(5): body += L(30 + cw * j, 30, 30 + cw * j, 200, NAVY, 2)
    for i in range(5): body += L(30, 30 + (i * 42.5 if i < 5 else 0), 530, 30 + i * 42.5, NAVY, 1.5)
    fig = wrap(560, 230, body, "Tabla de razones trigonométricas de 30°, 45° y 60°")
    ans = v.text()
    allv = []
    for f_ in fns:
        for a_ in angs:
            allv.append(cell(f_, a_).text())
    cs = [x for x in dict.fromkeys(allv) if x != ans]
    return make(f"La tabla muestra las razones trigonométricas de los ángulos de 30°, 45° y 60°. ¿Qué valor corresponde a {fn} {ang}° (la casilla con «?»)?", fig, ans, pick4(ans, cs), Q_REP, f"{fn} {ang}° = {ans}.")


def t_angle_from_value(r, l):
    fns = ["sen", "cos", "tan"]
    angs = [30, 45, 60]
    fn, ang = r.choice([(f_, a_) for f_ in fns for a_ in angs if not (l == 0 and a_ != 45 and f_ == 'tan')])
    v = tv(fn, ang)
    body = R(30, 30, 500, 40, "#E0F2FE") + R(30, 70, 500, 130, WHITE)
    cw = 500 / 4
    for j, t in enumerate(["", "sen", "cos", "tan"]): body += T(30 + cw * (j + 0.5), 57, t, 20)
    for i, a_ in enumerate(angs):
        body += T(30 + cw * 0.5, 100 + 40 * i, f"{a_}°", 20)
        for j, f_ in enumerate(fns):
            body += T(30 + cw * (j + 1.5), 100 + 40 * i, tv(f_, a_).text(), 19)
    for j in range(5): body += L(30 + cw * j, 30, 30 + cw * j, 200, NAVY, 2)
    for i in range(5): body += L(30, 30 + i * 42.5, 530, 30 + i * 42.5, NAVY, 1.5)
    fig = wrap(560, 230, body, "Tabla de razones trigonométricas")
    matches = [a_ for a_ in angs if tv(fn, a_).key() == v.key()]
    if len(matches) != 1: raise Reject
    ans = f"{ang}°"
    cs = [f"{x}°" for x in (30, 45, 60, 15, 75, 90, 0) if x != ang]
    r.shuffle(cs)
    return make(f"Usando la tabla, ¿para qué ángulo agudo θ se cumple {fn} θ = {v.text()}?", fig, ans, pick4(ans, cs), Q_REP, f"En la tabla, {fn} {ang}° = {v.text()}.")


# ---------------------------------------------------------------- Argumentar
TRUE_T = ["sen²α + cos²α = 1 para todo ángulo agudo α", "tan α = sen α / cos α para todo ángulo agudo α", "Si α y β son los ángulos agudos de un triángulo rectángulo, sen α = cos β",
          "sen α y cos α, para un ángulo agudo, son siempre menores que 1", "tan 45° = 1", "sen 30° = cos 60°"]
FALSE_T = ["sen α + cos α = 1 para todo ángulo agudo α", "tan α = cos α / sen α para todo ángulo agudo α", "El coseno de un ángulo agudo puede ser mayor que 1", "sen 60° = 2·sen 30°",
           "tan α es siempre menor que 1 si α es agudo", "sen α = cos α para todo ángulo agudo α", "tan 45° = 0"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_T), r.sample(FALSE_T, 4)
        stem = "Sobre las razones trigonométricas de ángulos agudos, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_T), r.sample(TRUE_T, 4)
        stem = "Sobre las razones trigonométricas de ángulos agudos, ¿cuál de las siguientes afirmaciones es FALSA?"
    fig = geo.trig_tri(1.2, 1, dict(opp="a", adj="b", hyp="c"), show_other="β")
    return make(stem, fig, good, bad, Q_ARG, "Se justifican con el triángulo rectángulo: a² + b² = c², sen α = a/c, cos α = b/c, tan α = a/b.")


def t_proof(r, l):
    a, b, c = r.choice(TRIPLES[:6])
    if l == 0:
        stem = f"En un triángulo rectángulo de lados {a}, {b} y {c} (hipotenusa), ¿cuál de las siguientes verificaciones muestra correctamente que sen²α + cos²α = 1?"
        good = f"({a}/{c})² + ({b}/{c})² = {a * a}/{c * c} + {b * b}/{c * c} = {c * c}/{c * c} = 1"
        bad = [f"{a}/{c} + {b}/{c} = ({a} + {b})/{c} = 1", f"({a}/{b})² + ({b}/{a})² = 1", f"({a}/{c})² · ({b}/{c})² = 1", f"{a}²/{c} + {b}²/{c} = {a * a + b * b}/{c} = 1", f"({a}/{c})² + ({b}/{c})² = {a * a + b * b}/{c} = 1"]
    elif l == 1:
        stem = f"En un triángulo rectángulo de lados {a}, {b} y {c} (hipotenusa), ¿cuál de las siguientes verificaciones muestra correctamente que tan α = sen α / cos α, con α opuesto a {a}?"
        good = f"sen α / cos α = ({a}/{c}) / ({b}/{c}) = {a}/{b} = tan α"
        bad = [f"sen α / cos α = ({a}/{c}) · ({b}/{c}) = {a * b}/{c * c} = tan α", f"sen α / cos α = ({b}/{c}) / ({a}/{c}) = {b}/{a} = tan α", f"sen α / cos α = ({a}/{c}) / ({b}/{c}) = {a}/{c} = tan α", f"sen α / cos α = ({a} + {b})/{c} = tan α", f"sen α / cos α = ({a}/{c}) − ({b}/{c}) = tan α"]
    else:
        stem = f"En un triángulo rectángulo de lados {a}, {b} y {c} (hipotenusa), α es el ángulo opuesto a {a} y β = 90° − α. ¿Cuál de las siguientes verificaciones muestra correctamente que sen α = cos β?"
        good = f"sen α = {a}/{c}; el cateto adyacente a β mide {a}, luego cos β = {a}/{c}"
        bad = [f"sen α = {a}/{c}; el cateto adyacente a β mide {b}, luego cos β = {b}/{c}", f"sen α = {a}/{c}; el cateto opuesto a β mide {a}, luego cos β = {a}/{b}", f"sen α = {a}/{c} y cos β = {c}/{a}", f"sen α = {a}/{c}; el cateto adyacente a β mide {a}, luego cos β = {a}/{b}", f"sen α = {a}/{c}; como α + β = 90°, cos β = 1 − {a}/{c}"]
    fig = geo.trig_tri(b, a, dict(opp=str(a), adj=str(b), hyp=str(c)), show_other="β" if l == 2 else None)
    return make(stem, fig, good, bad[:4], Q_ARG, "Se aplican las definiciones de las razones con los lados del triángulo y se comprueba cada paso.")


ERR = ["Usó el cateto adyacente en lugar del opuesto", "Dividió por el otro cateto en lugar de dividir por la hipotenusa", "Invirtió la razón (el cociente quedó al revés)",
       "Confundió el ángulo con su complemento", "Cometió un error al calcular la hipotenusa con el teorema de Pitágoras"]


def t_error(r, l):
    a, b, c = r.choice(TRIPLES[:6])
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    if k == 0:
        lines = [f"Cateto opuesto a α = {a}, adyacente = {b}, hipotenusa = {c}", f"sen α = cateto adyacente / hipotenusa = {b}/{c}"]
    elif k == 1:
        lines = [f"Cateto opuesto a α = {a}, adyacente = {b}, hipotenusa = {c}", f"sen α = cateto opuesto / otro cateto = {a}/{b}"]
    elif k == 2:
        lines = [f"Cateto opuesto a α = {a}, adyacente = {b}", f"tan α = adyacente / opuesto = {b}/{a}"]
    elif k == 3:
        lines = ["Ángulos agudos: α = 60° y β = 30°", "sen 60° = 1/2"]
    else:
        lines = [f"Catetos {a} y {b}", f"hipotenusa = {a} + {b} = {a + b}", f"sen α = {a}/{a + b}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 220, 19), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con las definiciones: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_special(r, l):
    d = 3 if r.random() < 0.7 else 2
    angs = [30, 60] if d == 3 else [45]
    a1, a2 = r.choice(angs), r.choice(angs)
    f1, f2 = r.choice(["sen", "cos", "tan"]), r.choice(["sen", "cos", "tan"])
    x, y = tv(f1, a1), tv(f2, a2)
    if l == 0:
        op = r.choice(["+", "−"])
        v = x + y if op == "+" else x - y
        expr = f"{f1} {a1}° {op} {f2} {a2}°"
        wrong = lambda p, q: (p + q if op == "+" else p - q)
    elif l == 1:
        op = r.choice(["·", "/"])
        if op == "/" and (y.a == 0 and y.b == 0): raise Reject
        v = x * y if op == "·" else x / y
        expr = f"{f1} {a1}° {op} {f2} {a2}°".replace("/", "÷")
        wrong = lambda p, q: (p * q if op == "·" else p / q)
    else:
        v = x * x + y * y
        expr = f"sen² {a1}° + cos² {a2}°" if False else f"({f1} {a1}°)² + ({f2} {a2}°)²"
        wrong = lambda p, q: p * q + q
    if any(abs(v.val()) > 100 for _ in [0]): raise Reject
    ans = v.text()
    others = []
    for f_ in ("sen", "cos", "tan"):
        for a_ in angs:
            others.append(tv(f_, a_))
    cands = [wrong(y, x), wrong(tv("cos" if f1 == "sen" else "sen", a1), y), wrong(x, tv("cos" if f2 == "sen" else "sen", a2)), wrong(tv("tan", a1), y), wrong(x, tv("tan", a2)), x + y, x * y, x - y]
    cs = [c_.text() for c_ in cands if c_.key() != v.key()]
    fig = card([expr, "Usa los valores exactos de 30°, 45° y 60°"], 190, 22)
    return make(f"¿Cuál es el valor exacto de {expr}?", fig, ans, pick4(ans, cs), Q_PRO, f"Se reemplazan los valores exactos y se opera: {ans}.")


def t_find_x(r, l):
    if l == 0:
        a, b, c = r.choice(TRIPLES[:6])
        k = r.choice([2, 3, 4])
        stem = f"En un triángulo rectángulo los catetos miden {a * k} y {b * k}. ¿Cuánto vale sen α, si α es el ángulo opuesto al cateto de {a * k}?"
        ans = fs(F(a, c))
        cs = [fs(F(b, c)), fs(F(a, b)), fs(F(b, a)), fs(F(a + b, c)), fs(F(a * k, c * k + 1)), fs(F(c, a))]
        fig = geo.trig_tri(b * k, a * k, dict(opp=str(a * k), adj=str(b * k), hyp="?"))
        cs = [c_ for c_ in cs if c_ != ans]
        return make(stem, fig, ans, pick4(ans, cs), Q_PRO, f"Hipotenusa = {c * k}; sen α = {a * k}/{c * k} = {ans}.")
    if l == 1:
        ang = r.choice([30, 60, 45])
        s = r.choice([6, 8, 10, 12, 18])
        fn = "tan"
        adj = s if ang != 45 else s
        v = tv("tan", ang) * s
        stem = f"En un triángulo rectángulo, un ángulo agudo mide {ang}° y el cateto adyacente a ese ángulo mide {s} cm. ¿Cuánto mide el cateto opuesto?"
        ans = v.text()
        d = 2 if ang == 45 else 3
        cs = [(tv("sen", ang) * s).text(), (tv("cos", ang) * s).text(), (Q(s, 0, d) / tv("tan", ang)).text() if ang != 45 else Q(s * 2, 0, 2).text(), Q(0, s, d).text() if ang != 60 else Q(s, 0, d).text(), Q(F(s, 2), 0, d).text(), Q(s * 2, 0, d).text()]
        cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
        fig = geo.trig_tri(1, 1 if ang == 45 else (0.58 if ang == 30 else 1.73), dict(adj=f"{s} cm", opp="x", hyp=""), ang=f"{ang}°")
        return make(stem, fig, ans, pick4(ans, cs), Q_PRO, f"Opuesto = {s}·tan {ang}° = {ans} cm.")
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)])
    k = r.choice([2, 3, 4, 5])
    stem = f"En un triángulo rectángulo, cos α = {b}/{c} y la hipotenusa mide {c * k}. ¿Cuál es el perímetro del triángulo?"
    ans = (a + b + c) * k
    cands = [(b + c) * k, (a + c) * k, (a + b) * k, c * k * 2, a * k + b * k * 2, (a + b + c) * k + k]
    cs = [str(c_) for c_ in cands if c_ != ans]
    fig = geo.trig_tri(b, a, dict(hyp=str(c * k), adj="", opp=""))
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_PRO, f"Catetos: {b * k} y {a * k}; perímetro = {ans}.")


BY_SKILL = {
    Q_RES: [t_ratio, t_side],
    Q_MOD: [t_ctx, t_sun],
    Q_REP: [t_letter_ratio, t_table, t_angle_from_value],
    Q_ARG: [t_props, t_proof, t_error],
    Q_PRO: [t_special, t_find_x],
}
