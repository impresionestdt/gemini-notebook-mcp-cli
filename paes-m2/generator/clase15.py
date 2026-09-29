"""Clase 15 · Geometría proporcional: Teorema de Thales y Teorema de Euclides."""
import random
from fractions import Fraction as F
from math import gcd, isqrt
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from mathfmt import E, fmt
import geo

NAMESETS = [("A", "B", "C", "D", "E"), ("P", "Q", "R", "S", "T"), ("O", "M", "N", "X", "Y"), ("K", "L", "M", "U", "V")]
EUN = [("A", "B", "C", "D"), ("P", "Q", "R", "S"), ("M", "N", "O", "H")]


def cmp_(vals, ans):
    return [c for c in vals if c != ans]


# ---------------------------------------------------------------- Thales
def thales_data(r, l):
    p, q = r.choice([(1, 2), (2, 3), (3, 4), (2, 5), (3, 5), (1, 3), (3, 2), (5, 3), (4, 3), (1, 4)])
    t, u = r.randint(1, 4), r.randint(1, 4)
    if t == u and l == 0: u = t % 4 + 1
    return p, q, t, u


def t_thales(r, l):
    """Resolver: hallar un segmento con DE ∥ BC."""
    nm = r.choice(NAMESETS)
    a, b, c, d, e = nm
    p, q, t, u = thales_data(r, l)
    AD, DB, AE, EC = p * t, q * t, p * u, q * u
    tt = AD / (AD + DB)
    if l == 0:
        unk = "EC"
        lab = dict(lAD=str(AD), lDB=str(DB), lAE=str(AE), lEC="x")
        ans = EC
        cands = [DB * EC // 1 if False else AE * DB // AD if (AE * DB) % AD == 0 else AE + 1, AD * EC // 1 if False else (AD * AE) // DB if (AD * AE) % DB == 0 else AE - 1, AE + (DB - AD), AE * DB - AD, DB + AE, AE + DB - AD + 1, EC + 1, EC - 1, AD + DB]
        stem = f"En el triángulo {a}{b}{c}, el segmento {d}{e} es paralelo a {b}{c}. Si {a}{d} = {AD}, {d}{b} = {DB} y {a}{e} = {AE}, ¿cuánto mide {e}{c}?"
        ex = f"{a}{d}/{d}{b} = {a}{e}/{e}{c} ⟹ {AD}/{DB} = {AE}/x ⟹ x = {EC}."
    elif l == 1:
        unk = r.choice(["AD", "DB", "AE", "EC"])
        vals = dict(AD=AD, DB=DB, AE=AE, EC=EC)
        lab = dict(lAD=str(AD), lDB=str(DB), lAE=str(AE), lEC=str(EC))
        lab[{"AD": "lAD", "DB": "lDB", "AE": "lAE", "EC": "lEC"}[unk]] = "x"
        ans = vals[unk]
        others = [v for k_, v in vals.items() if k_ != unk]
        cands = [ans + 1, ans - 1 if ans > 1 else ans + 3, others[0], others[1], others[2], sum(others) - ans, ans * 2, sum(others)]
        givens = ", ".join(f"{a if k_[0] == 'A' else d if k_[0] == 'D' else e}{{}}" for k_ in [])
        segn = {"AD": f"{a}{d}", "DB": f"{d}{b}", "AE": f"{a}{e}", "EC": f"{e}{c}"}
        given = ", ".join(f"{segn[k_]} = {vals[k_]}" for k_ in vals if k_ != unk)
        stem = f"En el triángulo {a}{b}{c}, {d}{e} ∥ {b}{c}. Si {given}, ¿cuánto mide {segn[unk]}?"
        ex = f"Por Thales {segn['AD']}/{segn['DB']} = {segn['AE']}/{segn['EC']}: se despeja {segn[unk]} = {ans}."
    else:
        if q <= p:
            p, q = q, p
        d0 = (q - p) * t
        x = p * t
        AD, DB, AE, EC = x, x + d0, p * u, q * u
        lab = dict(lAD="x", lDB=f"x + {d0}", lAE=str(AE), lEC=str(EC))
        ans = x
        cands = [q * t, d0, AE, EC, x + d0, x + 1, x - 1 if x > 1 else x + 2, AE + EC]
        stem = f"En el triángulo {a}{b}{c}, {d}{e} ∥ {b}{c}, con {a}{d} = x, {d}{b} = x + {d0}, {a}{e} = {AE} y {e}{c} = {EC}. ¿Cuál es el valor de x?"
        ex = f"x/(x + {d0}) = {AE}/{EC} ⟹ {EC}x = {AE}x + {AE * d0} ⟹ x = {x}."
    fig = geo.thales_tri(nm, lab["lAD"], lab["lDB"], lab["lAE"], lab["lEC"], tt)
    cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_RES, ex)


def t_parallels(r, l):
    p, q, t, u = thales_data(r, l)
    a, b, c, d = p * t, q * t, p * u, q * u
    if l < 2:
        which = "d" if l == 0 else r.choice(["a", "b", "c", "d"])
        vals = dict(a=a, b=b, c=c, d=d)
        lab = {k_: (str(v), v) for k_, v in vals.items()}
        lab[which] = ("x", vals[which])
        ans = vals[which]
        others = [v for k_, v in vals.items() if k_ != which]
        cands = [ans + 1, max(1, ans - 1), others[0], others[1], others[2], sum(others) - ans, ans * 2]
        stem = "Tres rectas paralelas son cortadas por dos transversales, determinando los segmentos que se muestran (en cm). ¿Cuál es el valor de x?"
        ex = "Por Thales, los segmentos son proporcionales: " + f"{lab['a'][0]}/{lab['b'][0]} = {lab['c'][0]}/{lab['d'][0]}."
    else:
        lab = dict(a=(str(a), a), b=(str(b), b), c=(str(c), c), d=("x", d))
        stem = f"Tres rectas paralelas son cortadas por dos transversales (medidas en cm). ¿Cuánto mide la transversal derecha completa (entre la primera y la tercera paralela)?"
        ans = c + d
        cands = [a + b, c, d, ans + 1, a + b + c, ans - 1, c * 2]
        ex = f"x = {c}·{b}/{a} = {d}; total = {c} + {d} = {c + d}."
        lab["d"] = ("x", d)
    fig = geo.par_fig(lab["a"], lab["b"], lab["c"], lab["d"])
    cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_RES, ex)


def t_shadow(r, l):
    if l == 0:
        h1, s1 = r.choice([(2, 3), (3, 2), (2, 1), (4, 5), (5, 4), (3, 4), (6, 4), (1, 2)])
        k = r.choice([2, 3, 4, 5, 6])
        s2 = s1 * k
        H = h1 * k
        stem = f"Un poste de {h1} m proyecta una sombra de {s1} m. En ese mismo instante, un árbol proyecta una sombra de {s2} m. ¿Cuánto mide el árbol?"
        ans = H
        cands = [H + h1, s2 - s1 + h1, H - 1, H + 2, s2, h1 * s2, s2 + h1]
        left = (h1, s1, "poste"); right = (H, s2, "árbol")
        ex = f"{h1}/{s1} = h/{s2} ⟹ h = {H} m."
    elif l == 1:
        h1, s1 = r.choice([(2, 3), (3, 4), (5, 4), (4, 3), (3, 2), (5, 2)])
        k = r.choice([3, 4, 5, 6, 8])
        s2, H = s1 * k, h1 * k
        obj = r.choice(["edificio", "torre", "mástil", "poste de luz"])
        stem = f"Una vara de {h1} m proyecta una sombra de {s1} m. En ese momento, la sombra de un {obj} mide {s2} m. ¿Cuál es la altura del {obj}, en metros?"
        ans = H
        cands = [H + h1, s2 - s1 + h1, H - 2, H + 3, s2 + h1, h1 * s2, F(s2 * s1, h1)]
        left = (h1, s1, "vara"); right = (H, s2, obj)
        ex = f"h/{s2} = {h1}/{s1} ⟹ h = {H} m."
    else:
        h1, s1 = r.choice([(2, 3), (3, 4), (5, 4), (4, 3)])
        k1, k2 = sorted(r.sample(range(2, 9), 2))
        H1, H2 = h1 * k1, h1 * k2
        s2, s3 = s1 * k1, s1 * k2
        stem = f"Una vara de {h1} m proyecta una sombra de {s1} m. En ese momento, un árbol proyecta {s2} m de sombra y un edificio {s3} m. ¿Cuántos metros más alto es el edificio que el árbol?"
        ans = H2 - H1
        cands = [s3 - s2, H2, H1, H2 + H1, ans + 1, ans - 1 if ans > 1 else ans + 2, (s3 - s2) * h1]
        left = (H1, s2, "árbol"); right = (H2, s3, "edificio")
        ex = f"Alturas: {H1} m y {H2} m; diferencia {ans} m."
    def tri(x, hh, ss, lab):
        return P([(x, 210), (x + ss, 210), (x, 210 - hh)], FILL) + tag(x + ss / 2, 235, lab[1], 16) + tag(x - 34, 210 - hh / 2, lab[0], 16) + tag(x + 6, 210 - hh - 22, lab[2], 16)
    sc = 150 / max(left[0], right[0])
    ss = 150 / max(left[0], right[0]) * 1.4
    l_lab = (f"{left[0]}" if l != 2 or True else "?", f"{left[1]}", left[2])
    r_lab = ("x" if l < 2 else "?", f"{right[1]}", right[2])
    if l == 2:
        l_lab = (f"?", f"{left[1]}", left[2]); r_lab = ("?", f"{right[1]}", right[2])
    body = (tri(90, left[0] * sc, left[1] * sc * 0.9 * (1 if left[1] else 1), l_lab) if False else "")
    ls, rs = left[1] * sc, right[1] * sc
    body = (P([(90, 210), (90 + ls, 210), (90, 210 - left[0] * sc)], FILL) + tag(90 + ls / 2, 236, f"{left[1]} m", 16) + tag(56, 210 - left[0] * sc / 2, (f"{left[0]} m" if l < 2 else "?"), 16)
            + P([(300, 210), (300 + rs, 210), (300, 210 - right[0] * sc)], FILL2) + tag(300 + rs / 2, 236, f"{right[1]} m", 16) + tag(266, 210 - right[0] * sc / 2, ("x" if l < 2 else "?"), 16)
            + L(20, 210, 540, 210, INK, 3) + tag(90, 22, "vara" if l < 2 and left[2] not in ("poste",) else left[2], 15) + tag(330, 22, right[2], 15))
    if l == 0:
        body = body.replace("?", f"{left[0]} m") if False else body
    if l < 2:
        body = body.replace(f">{'?'}<", ">x<")
    ans_s = str(ans)
    cs = [fs(c_) if isinstance(c_, F) else str(c_) for c_ in cands if c_ != ans and (not isinstance(c_, F) or c_.denominator == 1)]
    return make(stem, wrap(560, 260, body, "Dos triángulos formados por objetos y sombras"), ans_s, pick4(ans_s, cs), Q_MOD, ex)


# ---------------------------------------------------------------- Euclides
def euc_pq(r, l):
    """Devuelve (p, q, h, a, b, c) con h entero (p·q cuadrado)."""
    a0 = r.choice([1, 1, 2, 3])
    m, n = r.sample(range(1, 6), 2)
    p, q = a0 * m * m, a0 * n * n
    return p, q, a0 * m * n


def t_euclid_ctx(r, l):
    p, q, h = euc_pq(r, l)
    c = p + q
    ctx = r.choice(["Un terreno tiene forma de triángulo rectángulo y un camino recto sale del ángulo recto perpendicular a la hipotenusa, dividiéndola en", "En un triángulo rectángulo, la altura trazada desde el ángulo recto divide a la hipotenusa en dos segmentos de", "Una rampa triangular tiene un ángulo recto; la altura sobre su lado mayor lo divide en"])
    if l == 0:
        stem = f"{ctx} {p} m y {q} m. ¿Cuánto mide el camino (la altura)?"
        ans = h
        cands = [(p + q) // 2 if (p + q) % 2 == 0 else p + 1, p + q, p * q, isqrt(p * q) + 1, abs(q - p), h + 2, h - 1 if h > 1 else h + 3]
        labs = dict(p=f"{p}", q=f"{q}", h="x")
        ex = f"h² = {p}·{q} = {p * q} ⟹ h = {h} m."
    elif l == 1:
        stem = f"{ctx} {p} m y x m. Si la altura mide {h} m, ¿cuánto mide x?"
        ans = q
        cands = [h * h // p + 1, h - p if h > p else h + p, h * p, h * h, p + h, q + 2, q - 1 if q > 1 else q + 3]
        labs = dict(p=f"{p}", q="x", h=f"{h}")
        ex = f"{h}² = {p}·x ⟹ x = {q}."
    else:
        stem = f"{ctx} {p} m y {q} m. ¿Cuánto mide el cateto que está junto al segmento de {p} m (el cateto menor si {p} < {q})?"
        a2 = p * c
        ans_e = E((1, a2))
        ans = fmt(ans_e)
        cands = [fmt(E((1, q * c))), fmt(E((1, p * q))), str(p + h), str(c), fmt(E((1, p * p + h * h))) if False else str(h + 1), str(2 * h), fmt(E((1, a2 + 1)))]
        cands = [c_ for c_ in cands if c_ != ans]
        labs = dict(p=f"{p}", q=f"{q}", a="x")
        ex = f"AC² = {p}·{c} = {a2} ⟹ AC = {ans} m."
        fig = geo.right_tri(p, q, labs)
        return make(stem, fig, ans, pick4(ans, cands), Q_MOD, ex)
    fig = geo.right_tri(p, q, labs)
    cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_MOD, ex)


def t_euclid(r, l):
    """Aplicar: cálculos con los teoremas de Euclides."""
    nm = r.choice(EUN)
    na, nb, nc, nd = nm
    if l == 0:
        p, q, h = euc_pq(r, l)
        stem = f"En el triángulo {na}{nb}{nc}, rectángulo en {nc}, la altura {nc}{nd} sobre la hipotenusa {na}{nb} determina {na}{nd} = {p} y {nd}{nb} = {q}. ¿Cuánto mide {nc}{nd}?"
        ans = h
        cands = [(p + q) // 2 if (p + q) % 2 == 0 else p + 2, p + q, p * q, h + 1, h - 1 if h > 1 else h + 3, abs(q - p), h * 2]
        labs = dict(p=str(p), q=str(q), h="x")
        ex = f"CD² = AD·DB = {p}·{q} ⟹ CD = {h}."
    elif l == 1:
        a0 = r.choice([1, 2, 3, 4])
        m, n = r.sample(range(1, 5), 2)
        p, q = a0 * m * m, a0 * n * n
        c = p + q
        stem = f"En el triángulo {na}{nb}{nc}, rectángulo en {nc}, la altura {nc}{nd} divide la hipotenusa {na}{nb} de modo que {na}{nd} = {p} y {na}{nb} = {c}. ¿Cuánto mide {nd}{nb}?"
        ans = q
        cands = [c + p, c * p, c - p + 1, p, c, q + 2, max(1, q - 1)]
        labs = dict(p=str(p), q="x", c=str(c))
        ex = f"{nd}{nb} = {na}{nb} − {na}{nd} = {c} − {p} = {q}."
        fig = geo.right_tri(p, q, labs, nm)
        cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
        return make(stem, fig, str(ans), pick4(str(ans), cs), Q_PRO, ex)
    else:
        a0 = r.choice([1, 2, 3, 5]); m, n = r.sample(range(1, 6), 2)
        p, q = a0 * m * m, a0 * n * n
        c = p + q
        rad = r.random() < 0.5
        if rad:
            a2 = p * c
            ans = fmt(E((1, a2)))
            stem = f"En el triángulo {na}{nb}{nc}, rectángulo en {nc}, la altura {nc}{nd} determina {na}{nd} = {p} y {nd}{nb} = {q}. ¿Cuánto mide el cateto {na}{nc}?"
            cands = [fmt(E((1, q * c))), fmt(E((1, p * q))), str(p + q), fmt(E((1, p * p + p * q + 1))), fmt(E((1, c))), str(2 * p)]
            ex = f"{na}{nc}² = {na}{nd}·{na}{nb} = {p}·{c} = {a2}."
        else:
            b2 = q * c
            ans = fmt(E((1, b2)))
            stem = f"En el triángulo {na}{nb}{nc}, rectángulo en {nc}, la altura {nc}{nd} determina {na}{nd} = {p} y {nd}{nb} = {q}. ¿Cuánto mide el cateto {nb}{nc}?"
            cands = [fmt(E((1, p * c))), fmt(E((1, p * q))), str(p + q), fmt(E((1, q * q + p * q + 1))), fmt(E((1, c))), str(2 * q)]
            ex = f"{nb}{nc}² = {nd}{nb}·{na}{nb} = {q}·{c} = {b2}."
        labs = dict(p=str(p), q=str(q), a="x" if rad else "", b="" if rad else "x")
        cands = [c_ for c_ in cands if c_ != ans]
        fig = geo.right_tri(p, q, labs, nm)
        return make(stem, fig, ans, pick4(ans, cands), Q_PRO, ex)
    fig = geo.right_tri(p, q, labs, nm)
    cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_PRO, ex)


def t_thales_de(r, l):
    """Aplicar: DE ∥ BC, hallar DE o BC con razones."""
    nm = r.choice(NAMESETS)
    a, b, c, d, e = nm
    p, q = r.choice([(1, 2), (2, 3), (3, 4), (2, 5), (1, 3), (3, 5), (2, 1), (3, 2)])
    t = r.randint(1, 4)
    AD, DB = p * t, q * t
    AB = AD + DB
    k = r.randint(1, 5)
    BC = AB * k if l == 0 else (AB * r.randint(1, 4) if l == 1 else AB * r.randint(2, 6))
    DE = F(AD * BC, AB)
    if DE.denominator != 1: raise Reject
    DE = int(DE)
    if l < 2:
        stem = f"En el triángulo {a}{b}{c}, {d}{e} ∥ {b}{c}, con {a}{d} = {AD}, {d}{b} = {DB} y {b}{c} = {BC}. ¿Cuánto mide {d}{e}?"
        ans = DE
        cands = [DE * AB // DB if (DE * AB) % DB == 0 else DE + 1, AD * BC // DB if (AD * BC) % DB == 0 else DE + 2, BC - DE, BC * DB // AD if (BC * DB) % AD == 0 else DE + 3, DE + 1, DE - 1 if DE > 1 else DE + 4, BC]
        lab = dict(lAD=str(AD), lDB=str(DB), lBC=str(BC), lDE="x")
        ex = f"DE/BC = AD/AB = {AD}/{AB} ⟹ DE = {DE}."
    else:
        stem = f"En el triángulo {a}{b}{c}, {d}{e} ∥ {b}{c}, con {a}{d} = {AD}, {d}{b} = {DB} y {d}{e} = {DE}. ¿Cuánto mide {b}{c}?"
        ans = BC
        cands = [DE * DB // AD if (DE * DB) % AD == 0 else BC + 1, DE * AD // AB if (DE * AD) % AB == 0 else BC + 2, DE + DB, BC - DE, BC + 1, BC - 1 if BC > 1 else BC + 3, AB]
        lab = dict(lAD=str(AD), lDB=str(DB), lBC="x", lDE=str(DE))
        ex = f"DE/BC = AD/AB ⟹ BC = {DE}·{AB}/{AD} = {BC}."
    fig = geo.thales_tri(nm, lab["lAD"], lab["lDB"], "", "", AD / AB, lBC=lab["lBC"], lDE=lab["lDE"])
    cs = [str(c_) for c_ in cands if c_ != ans and c_ > 0]
    return make(stem, fig, str(ans), pick4(str(ans), cs), Q_PRO, ex)


# ---------------------------------------------------------------- Representar
def t_valid_relation(r, l):
    if l < 2:
        nm = r.choice(NAMESETS)
        a, b, c, d, e = nm
        if l == 0:
            T = [f"{a}{d}/{d}{b} = {a}{e}/{e}{c}", f"{a}{d}/{a}{b} = {a}{e}/{a}{c}", f"{d}{b}/{a}{b} = {e}{c}/{a}{c}", f"{a}{d}/{a}{b} = {d}{e}/{b}{c}", f"{a}{d}/{a}{e} = {d}{b}/{e}{c}", f"{a}{b}/{a}{d} = {a}{c}/{a}{e}"]
            Fl = [f"{a}{d}/{d}{b} = {d}{e}/{b}{c}", f"{a}{d}/{a}{b} = {e}{c}/{a}{c}", f"{a}{d}/{d}{b} = {e}{c}/{a}{e}", f"{d}{b}/{a}{b} = {a}{e}/{a}{c}", f"{a}{d}/{a}{e} = {a}{b}/{e}{c}", f"{d}{e}/{b}{c} = {d}{b}/{a}{b}"]
            fig = geo.thales_tri(nm, "", "", "", "", 0.45)
            stem = f"En la figura, {d}{e} es paralelo a {b}{c}. ¿Cuál de las siguientes relaciones es correcta?"
        else:
            T = [f"{a}{d}/{a}{b} = {a}{e}/{a}{c}", f"{a}{d}/{d}{b} = {a}{e}/{e}{c}", f"{d}{b}/{a}{d} = {e}{c}/{a}{e}", f"{a}{b}/{d}{b} = {a}{c}/{e}{c}"]
            Fl = [f"{a}{d}/{d}{b} = {e}{c}/{a}{e}", f"{a}{d}/{a}{b} = {e}{c}/{a}{c}", f"{d}{b}/{a}{b} = {a}{e}/{a}{c}", f"{a}{d}/{a}{e} = {a}{b}/{e}{c}", f"{a}{b}/{a}{d} = {e}{c}/{a}{e}"]
            fig = geo.thales_tri(nm, "", "", "", "", 0.4)
            stem = f"En la figura, {d}{e} ∥ {b}{c}. ¿Cuál de las siguientes proporciones es verdadera?"
        good, bad = r.choice(T), r.sample(Fl, 4)
    else:
        nm = r.choice(EUN)
        a, b, c, d = nm
        T = [f"{c}{d}² = {a}{d}·{d}{b}", f"{a}{c}² = {a}{d}·{a}{b}", f"{b}{c}² = {d}{b}·{a}{b}", f"{a}{c}·{b}{c} = {a}{b}·{c}{d}"]
        Fl = [f"{c}{d}² = {a}{d}·{a}{b}", f"{a}{c}² = {a}{d}·{d}{b}", f"{b}{c}² = {a}{d}·{a}{b}", f"{a}{c}·{b}{c} = {a}{d}·{d}{b}", f"{c}{d} = {a}{d} + {d}{b}", f"{a}{c}² = {c}{d}·{a}{b}"]
        good, bad = r.choice(T), r.sample(Fl, 4)
        fig = geo.right_tri(4, 9, {}, nm)
        stem = f"En el triángulo {a}{b}{c}, rectángulo en {c}, la altura {c}{d} cae sobre la hipotenusa {a}{b}. ¿Cuál de las siguientes relaciones es correcta?"
    return make(stem, fig, good, bad, Q_REP, "Se identifican segmentos correspondientes: paralelas ⟹ razones iguales (Thales); altura y catetos son medias proporcionales (Euclides).")


def t_equation(r, l):
    """Representar: plantea la ecuación correcta para x."""
    if l == 0:
        nm = r.choice(NAMESETS)
        a, b, c, d, e = nm
        p, q, t, u = thales_data(r, 0)
        AD, DB, AE, EC = p * t, q * t, p * u, q * u
        fig = geo.thales_tri(nm, str(AD), str(DB), str(AE), "x", AD / (AD + DB))
        ans = f"{AD}/{DB} = {AE}/x"
        cands = [f"{AD}/{DB} = x/{AE}", f"{AD}/{AE} = x/{DB}", f"{AD}/{AD + DB} = {AE}/x", f"{DB}/{AD} = {AE}/x", f"{AD}/{DB} = ({AE} + x)/x", f"{AD}/{DB} = x/({AE} + x)"]
        stem = f"En la figura, {d}{e} ∥ {b}{c} y las medidas están en cm. ¿Cuál de las siguientes ecuaciones permite calcular x?"
    elif l == 1:
        p, q, t, u = thales_data(r, 1)
        a, b, c, d = p * t, q * t, p * u, q * u
        fig = geo.par_fig((str(a), a), (str(b), b), (str(c), c), ("x", d))
        ans = f"{a}/{b} = {c}/x"
        cands = [f"{a}/{b} = x/{c}", f"{a}/{c} = x/{b}", f"{a}/({a} + {b}) = {c}/x", f"{b}/{a} = {c}/x", f"{a}/{b} = ({c} + x)/x", f"{a} + {b} = {c} + x"]
        stem = "Tres paralelas son cortadas por dos transversales (medidas en cm). ¿Cuál de las siguientes ecuaciones permite calcular x?"
    else:
        nm = r.choice(EUN)
        p, q, h = euc_pq(r, 2)
        which = r.choice(["h", "a", "b"])
        if which == "h":
            fig = geo.right_tri(p, q, dict(p=str(p), q=str(q), h="x"), nm)
            ans = f"x² = {p}·{q}"
            cands = [f"x = {p}·{q}", f"x² = {p} + {q}", f"x = {p} + {q}", f"x² = {p}·({p} + {q})", f"{p}/x = {q}/{p + q}", f"x² = {q}·({p} + {q})"]
        elif which == "a":
            fig = geo.right_tri(p, q, dict(p=str(p), q=str(q), a="x"), nm)
            ans = f"x² = {p}·({p} + {q})"
            cands = [f"x² = {p}·{q}", f"x² = {q}·({p} + {q})", f"x = {p}·({p} + {q})", f"x² = {p} + ({p} + {q})", f"x² = {p}² + {q}²", f"x² = ({p} + {q})²"]
        else:
            fig = geo.right_tri(p, q, dict(p=str(p), q=str(q), b="x"), nm)
            ans = f"x² = {q}·({p} + {q})"
            cands = [f"x² = {p}·{q}", f"x² = {p}·({p} + {q})", f"x = {q}·({p} + {q})", f"x² = {q} + ({p} + {q})", f"x² = {p}² + {q}²", f"x² = ({p} + {q})²"]
        stem = f"En la figura, el triángulo es rectángulo y la altura sobre la hipotenusa la divide en dos segmentos (medidas en cm). ¿Qué ecuación permite calcular x?"
    return make(stem, fig, ans, pick4(ans, cands), Q_REP, "Se plantea la proporción correspondiente o el teorema de Euclides que involucra el segmento pedido.")


# ---------------------------------------------------------------- Argumentar
def t_parallel_check(r, l):
    nm = r.choice(NAMESETS)
    a, b, c, d, e = nm
    p, q, t, u = thales_data(r, l)
    AD, DB, AE, EC = p * t, q * t, p * u, q * u
    par = r.random() < 0.5
    if not par:
        EC = EC + r.choice([1, 2, -1]) if EC > 2 else EC + 2
        if F(AD, DB) == F(AE, EC): raise Reject
    ratio = lambda x, y: str(F(x, y)) if F(x, y).denominator != 1 else str(F(x, y).numerator)
    rl, rr = F(AD, DB), F(AE, EC)
    fmtf = lambda v: f"{v.numerator}/{v.denominator}" if v.denominator != 1 else str(v.numerator)
    if par:
        ans = f"Sí, porque {a}{d}/{d}{b} = {a}{e}/{e}{c} (ambas razones valen {fmtf(rl)})"
    else:
        ans = f"No, porque {a}{d}/{d}{b} ≠ {a}{e}/{e}{c} ({fmtf(rl)} ≠ {fmtf(rr)})"
    cands = [
        f"Sí, porque {a}{d} + {d}{b} = {a}{e} + {e}{c}" if AD + DB == AE + EC else f"Sí, porque {a}{d} + {d}{b} = {a}{b} (los puntos están alineados)",
        f"No, porque {a}{d} ≠ {a}{e}" if AD != AE else f"No, porque {d}{b} ≠ {e}{c}",
        f"Sí, porque {a}{d}/{d}{b} = {e}{c}/{a}{e}" if F(AD, DB) == F(EC, AE) else f"Sí, porque {a}{d}/{d}{b} = {a}{e}/{e}{c} (ambas razones valen {fmtf(rl)})" if not par else f"No, porque {a}{d}/{d}{b} ≠ {a}{e}/{e}{c} ({fmtf(rl)} ≠ {fmtf(rr)})",
        f"No, porque los segmentos {d}{b} y {e}{c} no son iguales" if DB != EC else f"No, porque {a}{d} y {d}{b} no son iguales",
        f"Sí, porque {d}{e} es más corto que {b}{c}",
        f"No, porque {a}{d}/{a}{b} ≠ {e}{c}/{a}{c}" if not par else f"Sí, porque {a}{b} y {a}{c} son lados del triángulo",
    ]
    cands = [c_ for c_ in dict.fromkeys(cands) if c_ != ans]
    ok = ans.startswith("Sí")
    cands = [c_ for c_ in cands if not (c_.startswith("Sí, porque " + f"{a}{d}/{d}{b} = {a}{e}/{e}{c}") and not par) and not (c_.startswith("No, porque " + f"{a}{d}/{d}{b} ≠ {a}{e}/{e}{c}") and par)]
    fig = geo.thales_tri(nm, str(AD), str(DB), str(AE), str(EC), AD / (AD + DB))
    return make(f"En el triángulo {a}{b}{c}, los puntos {d} y {e} están sobre {a}{b} y {a}{c}, con {a}{d} = {AD}, {d}{b} = {DB}, {a}{e} = {AE} y {e}{c} = {EC}. ¿Es {d}{e} paralelo a {b}{c}?",
                fig, ans, pick4(ans, cands), Q_ARG, "Por el recíproco de Thales, DE ∥ BC si y solo si AD/DB = AE/EC.")


TRUE_T = ["Si dos rectas paralelas cortan a dos transversales, determinan en ellas segmentos proporcionales", "En un triángulo rectángulo, la altura sobre la hipotenusa es media proporcional entre los segmentos que determina en ella",
          "Cada cateto es media proporcional entre la hipotenusa y su proyección sobre ella", "Si una recta divide dos lados de un triángulo en segmentos proporcionales, entonces es paralela al tercer lado",
          "Si DE ∥ BC en el triángulo ABC, entonces AD/AB = DE/BC"]
FALSE_T = ["En un triángulo rectángulo, la altura sobre la hipotenusa es igual a la suma de los segmentos que determina", "El teorema de Thales solo se cumple en triángulos isósceles",
           "Si AD/DB = AE/EC, entonces DE es perpendicular a BC", "En un triángulo rectángulo, el cuadrado de la hipotenusa es igual al producto de los catetos",
           "La altura sobre la hipotenusa es la media aritmética de los segmentos que determina", "Los segmentos que determinan tres paralelas en dos transversales son siempre iguales",
           "Si DE ∥ BC en el triángulo ABC, entonces AD/DB = DE/BC"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_T), r.sample(FALSE_T, 4)
        stem = "Sobre proporcionalidad en triángulos, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_T), r.sample(TRUE_T, 4)
        stem = "Sobre proporcionalidad en triángulos, ¿cuál de las siguientes afirmaciones es FALSA?"
    nm = r.choice(NAMESETS)
    fig = geo.thales_tri(nm, "", "", "", "", 0.5)
    return make(stem, fig, good, bad, Q_ARG, "Se contrasta cada afirmación con los teoremas de Thales y de Euclides.")


ERR = ["Invirtió una de las razones al plantear la proporción", "Comparó una parte con el total en un lado y con la otra parte en el otro",
       "Cometió un error de cálculo al despejar x", "Calculó una media aritmética en lugar de una media proporcional", "Olvidó extraer la raíz cuadrada al final"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([0, 1, 2])
    p, q, t, u = thales_data(r, 1)
    AD, DB, AE, EC = p * t, q * t, p * u, q * u
    if k == 0:
        lines = [f"DE ∥ BC, AD = {AD}, DB = {DB}, AE = {AE}", f"AD/DB = x/AE ⟹ x = {AD}·{AE}/{DB}", f"x = {F(AD * AE, DB)}".replace("/", " / ") if F(AD * AE, DB).denominator != 1 else f"x = {AD * AE // DB}"]
    elif k == 1:
        lines = [f"DE ∥ BC, AD = {AD}, DB = {DB}, AE = {AE}", f"AD/DB = AE/AC (con AC = x)", f"x = {DB}·{AE}/{AD}"]
    elif k == 2:
        lines = [f"DE ∥ BC, AD = {AD}, DB = {DB}, AE = {AE}", f"AD/DB = AE/x ⟹ x = {DB}·{AE}/{AD}", f"x = {EC + r.choice([-1, 1, 2])}"]
    elif k == 3:
        pp, qq, hh = euc_pq(r, 1)
        lines = [f"Triángulo rectángulo, AD = {pp}, DB = {qq}", f"h = ({pp} + {qq})/2", f"h = {F(pp + qq, 2)}"]
    else:
        pp, qq, hh = euc_pq(r, 1)
        lines = [f"Triángulo rectángulo, AD = {pp}, DB = {qq}", f"h² = {pp}·{qq} = {pp * qq}", f"h = {pp * qq}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 230, 19), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


BY_SKILL = {
    Q_RES: [t_thales, t_parallels],
    Q_MOD: [t_shadow, t_euclid_ctx],
    Q_REP: [t_valid_relation, t_equation],
    Q_ARG: [t_parallel_check, t_props, t_error],
    Q_PRO: [t_thales_de, t_euclid],
}
