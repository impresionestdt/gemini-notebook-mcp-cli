"""Clase 21 · Repaso Geometría M2: síntesis proporcional (Thales, Euclides, semejanza, homotecia, trigonometría y vectores)."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from mathfmt import E, fmt
import geo
import clase15, clase16, clase17, clase18, clase19, clase20

TRIP = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (7, 24, 25), (12, 16, 20), (15, 20, 25), (10, 24, 26)]


# ---------------------------------------------------------------- Resolver
def t_thales_pyth(r, l):
    a, b, c = r.choice(TRIP)
    if r.random() < 0.5: a, b = b, a            # a = BC (opuesto), b = AC (adyacente)
    den = r.choice([2, 3, 4, 5])
    num = r.randint(1, den - 1)
    if (b * num) % den or (a * num) % den or (c * num) % den: raise Reject
    t = F(num, den)
    AE, EC = b * t, b * (1 - t)
    DE = a * t
    AD, DB = c * t, c * (1 - t)
    labs = dict(AE=fs(AE), EC="?" if l == 1 else fs(EC), BC=fs(a), DE="x" if l == 0 else "")
    if l == 0:
        stem = f"En el triángulo ABC, rectángulo en C, se tiene BC = {a} y AC = {b}. El punto E está sobre AC con AE = {fs(AE)}, y DE es paralelo a BC (D sobre AB). ¿Cuánto mide DE?"
        ans = DE
        cands = [a - DE, a * (1 - t), DE + 1, AE, EC, a * t + AE, F(AE * b, a)]
        labs = dict(AE=fs(AE), EC=fs(EC), BC=fs(a), DE="x")
        ex = f"Por Thales DE/BC = AE/AC ⟹ DE = {a}·{fs(AE)}/{b} = {fs(DE)}."
    elif l == 1:
        stem = f"En el triángulo ABC, rectángulo en C, se tiene BC = {a} y AC = {b}. El punto E está sobre AC con AE = {fs(AE)}, y DE es paralelo a BC (D sobre AB). ¿Cuál es el perímetro del trapecio DECB?"
        per = DE + EC + a + DB
        ans = per
        cands = [DE + EC + a, a + b + c, per - DB + AD, DE + a + EC + AD, per + 1, (DE + a) * EC / 2, per - EC]
        labs = dict(AE=fs(AE), EC=fs(EC), BC=fs(a), DE=fs(DE))
        ex = f"DE = {fs(DE)}, EC = {fs(EC)}, BC = {a}, DB = {fs(DB)} (por Thales y Pitágoras): perímetro = {fs(per)}."
    else:
        stem = f"En el triángulo ABC, rectángulo en C, se tiene BC = {a} y AC = {b}. El punto E está sobre AC con AE = {fs(AE)}, y DE es paralelo a BC (D sobre AB). ¿Cuál es el área del trapecio DECB?"
        area = (DE + a) * EC / 2
        ans = area
        cands = [a * b / 2, DE * AE / 2, (DE + a) * b / 2, area + 1, a * b * t * t / 2, a * b * (1 - t * t) / 2 + 1, DE * EC]
        labs = dict(AE=fs(AE), EC=fs(EC), BC=fs(a), DE=fs(DE))
        ex = f"Área = (DE + BC)/2 · EC = ({fs(DE)} + {a})/2 · {fs(EC)} = {fs(area)}."
    fig = geo.right_par(b, a, float(t), labs)
    cs = [fs(F(c_)) for c_ in cands if F(c_) != F(ans) and F(c_) > 0]
    return make(stem, fig, fs(F(ans)), pick4(fs(F(ans)), cs), Q_RES, ex)


def t_euclid_trig(r, l):
    m, n = r.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (8, 15), (15, 8)])
    a0 = r.choice([1, 1, 2]) if (m, n) in [(3, 4), (4, 3)] else 1
    p, q = a0 * m * m, a0 * n * n
    c = p + q
    k = {3: 5, 4: 5, 5: 13, 12: 13, 6: 10, 8: 10, 15: 17}[m]
    k = {(3, 4): 5, (4, 3): 5, (5, 12): 13, (12, 5): 13, (6, 8): 10, (8, 6): 10, (8, 15): 17, (15, 8): 17}[(m, n)]
    AC, BC = a0 * m * k, a0 * n * k                    # AC² = p·c ; BC² = q·c
    h = a0 * m * n
    what = r.choice(["sen", "cos", "tan"]) if l < 2 else "area"
    if l < 2:
        which = what
        val = {"sen": F(BC, c), "cos": F(AC, c), "tan": F(BC, AC)}[which]
        stem = f"En el triángulo ABC, rectángulo en C, la altura CD determina AD = {p} y DB = {q}. Si α = ∠A, ¿cuánto vale {which} α?"
        ans = fs(val)
        pool = [F(BC, c), F(AC, c), F(BC, AC), F(AC, BC), F(c, BC), F(h, BC), F(h, AC), F(p, c), F(q, c)]
        cs = [fs(w) for w in pool if w != val]
        ex = f"Catetos: AC = √({p}·{c}) = {AC}, BC = √({q}·{c}) = {BC}; {which} α = {ans}."
    else:
        stem = f"En el triángulo ABC, rectángulo en C, la altura CD determina AD = {p} y DB = {q}. ¿Cuál es el área del triángulo ABC?"
        area = F(c * h, 2)
        ans = fs(area)
        cs = [fs(F(AC * BC, 4)), fs(F(p * q, 2)), fs(F(c * c, 2)), fs(F(AC + BC + c, 1)), fs(F(h * h, 2)), fs(area + 1), fs(F(c * BC, 2))]
        cs = [x for x in cs if x != ans]
        ex = f"h = √({p}·{q}) = {h}; área = {c}·{h}/2 = {ans}."
    fig = geo.right_tri(p, q, dict(p=str(p), q=str(q), h="", a="", b=""))
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


# ---------------------------------------------------------------- Modelar
def t_tower_cable(r, l):
    hs, ss = r.choice([(2, 3), (3, 4), (4, 3), (6, 4), (2, 1), (5, 2)])
    trip = r.choice([(6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 6, 10)])
    m, H0, cab = trip
    # Torre de altura H0 (múltiplo) con sombra proporcional
    k = F(H0, hs)
    s2 = ss * k
    if s2.denominator != 1 or H0 == hs: raise Reject
    s2 = int(s2)
    if l == 0:
        stem = f"Una vara de {hs} m proyecta una sombra de {ss} m. En ese momento, la sombra de una torre mide {s2} m. ¿Cuánto mide la torre?"
        ans = H0
        cands = [H0 + hs, s2, H0 - 1, H0 + 2, hs * s2, s2 - ss + hs]
        ex = f"Torre = {hs}·{s2}/{ss} = {H0} m."
    elif l == 1:
        stem = f"Una vara de {hs} m proyecta una sombra de {ss} m. En ese momento, la sombra de una torre mide {s2} m. Un cable une la punta de la torre con un punto del suelo situado a {m} m de su base (por el lado opuesto a la sombra). ¿Cuánto mide el cable?"
        ans = cab
        cands = [H0 + m, H0, m, cab + 1, cab - 1, H0 * m]
        ex = f"Torre = {H0} m; cable = √({H0}² + {m}²) = {cab} m."
    else:
        stem = f"Una vara de {hs} m proyecta una sombra de {ss} m. En ese momento, la sombra de una torre mide {s2} m. Un cable une la punta de la torre con un punto del suelo situado a {m} m de su base. Si θ es el ángulo que forma el cable con el suelo, ¿cuánto vale sen θ?"
        val = F(H0, cab)
        ans = fs(val)
        cands = [F(m, cab), F(H0, m), F(m, H0), F(cab, H0), F(hs, ss), F(H0, cab + 1)]
        cs = [fs(w) for w in cands if w != val]
        ex = f"Torre = {H0} m; cable = {cab} m; sen θ = {H0}/{cab} = {ans}."
    sc = 120 / max(H0, hs)
    body = L(20, 230, 540, 230, INK, 3)
    body += P([(60, 230), (60 + ss * sc, 230), (60, 230 - hs * sc)], FILL) + tag(60 + ss * sc / 2, 254, f"{ss} m", 14) + tag(38, 230 - hs * sc / 2, f"{hs} m", 14)
    tx = 260
    body += P([(tx, 230), (tx + s2 * sc * 0.7, 230), (tx, 230 - H0 * sc)], FILL2) + tag(tx + s2 * sc * 0.35, 254, f"{s2} m", 14) + tag(tx - 30, 230 - H0 * sc / 2, "x" if l == 0 else "?", 14)
    if l >= 1:
        px = tx - m * sc * 0.8
        body += L(px, 230, tx, 230 - H0 * sc, ACC, 4) + C(px, 230, 5, INK, INK, 1) + tag(px - 6, 205, f"{m} m", 14)
    fig = wrap(560, 275, body, "Dos objetos y sus sombras")
    cs = [fs(F(c_)) for c_ in cands if F(c_) != F(ans)] if l < 2 else cs
    a_s = fs(F(ans)) if l < 2 else ans
    return make(stem, fig, a_s, pick4(a_s, cs), Q_MOD, ex)


# ---------------------------------------------------------------- Representar
TOOLS = ["Teorema de Thales", "Teorema de Euclides", "Razones trigonométricas", "Razón de áreas de figuras semejantes", "Homotecia"]


def t_tool(r, l):
    k = r.choice([0, 1, 2]) if l == 0 else r.choice([0, 1, 2, 3]) if l == 1 else r.choice([0, 1, 2, 3, 4])
    if k == 0:
        nm = r.choice(clase15.NAMESETS)
        p, q, t, u = clase15.thales_data(r, 1)
        fig = geo.thales_tri(nm, str(p * t), str(q * t), str(p * u), "x", p / (p + q))
        stem = f"En la figura, {nm[3]}{nm[4]} ∥ {nm[1]}{nm[2]}. Se quiere calcular x. ¿Qué herramienta permite hacerlo de forma más directa?"
    elif k == 1:
        m_, n_ = r.choice([(1, 4), (4, 9), (9, 16), (1, 9), (4, 25)])
        fig = geo.right_tri(m_, n_, dict(p=str(m_), q=str(n_), h="x"))
        stem = "En el triángulo rectángulo de la figura, la altura sobre la hipotenusa la divide en dos segmentos. Se quiere calcular la altura x. ¿Qué herramienta permite hacerlo de forma más directa?"
    elif k == 2:
        ang = r.choice([30, 60, 45])
        fig = geo.trig_tri(1, 1 if ang == 45 else (0.58 if ang == 30 else 1.73), dict(hyp=f"{r.choice([10, 12, 20])} m", opp="x", adj=""), ang=f"{ang}°")
        stem = "En el triángulo rectángulo de la figura se conocen un ángulo agudo y la hipotenusa. Se quiere calcular el cateto x. ¿Qué herramienta permite hacerlo de forma más directa?"
    elif k == 3:
        a_, b_ = r.choice([(2, 3), (3, 4), (2, 5)])
        A1 = a_ * a_ * r.randint(2, 6)
        fig = geo.sim_tris(F(b_, a_), dict(base=f"{a_ * 2} cm"), dict(base=f"{b_ * 2} cm"), f"A = {A1} cm²", "A = x")
        stem = "Las figuras de la imagen son semejantes. Se conoce el área de la menor y los lados homólogos, y se quiere calcular el área x de la mayor. ¿Qué herramienta permite hacerlo de forma más directa?"
    else:
        O, kk, pts_, img = clase17.tri_case(r, 1)
        fig = clase17.fig_tri(O, pts_, img).svg("Triángulo, imagen y centro")
        stem = "En la figura, el triángulo A'B'C' es la imagen del triángulo ABC a partir de un punto O. Se quiere determinar la razón de la transformación. ¿Qué herramienta permite hacerlo de forma más directa?"
    ans = TOOLS[k]
    return make(stem, fig, ans, [t_ for i, t_ in enumerate(TOOLS) if i != k], Q_REP, "Cada herramienta se reconoce por la configuración: paralelas, altura sobre la hipotenusa, ángulo con lados, áreas de figuras semejantes o puntos alineados con un centro.")


BY_SKILL = {
    Q_RES: [t_thales_pyth, t_euclid_trig, clase15.t_thales, clase16.t_area, clase17.t_image_point, clase18.t_side],
    Q_MOD: [t_tower_cable, clase15.t_shadow, clase16.t_scale_ctx, clase19.t_box_ctx, clase19.t_ramp_ctx],
    Q_REP: [t_tool, clase15.t_valid_relation, clase17.t_classify, clase19.t_box_triangle, clase20.t_box_vec],
    Q_ARG: [clase15.t_parallel_check, clase16.t_props, clase19.t_compare, clase17.t_compose, clase20.t_parallel, clase18.t_proof],
    Q_PRO: [clase15.t_euclid, clase16.t_compute, clase17.t_lengths, clase18.t_special, clase19.t_solid, clase20.t_module],
}
