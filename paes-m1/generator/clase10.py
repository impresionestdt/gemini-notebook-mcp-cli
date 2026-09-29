"""Clase 10 (M1) · Repaso del eje Números y resolución integrada; suficiencia de datos aplicada a números."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG
import clase01 as c1, clase02 as c2, clase03 as c3, clase04 as c4, clase05 as c5, clase06 as c6, clase07 as c7, clase08 as c8, clase09 as c9

SUF = ["(1) por sí sola", "(2) por sí sola", "Ambas juntas, (1) y (2)", "Cada una por sí sola, (1) ó (2)", "Se requiere información adicional"]


def _rank(rows):
    rs_ = [[F(x) for x in r_] for r_ in rows]
    rk = 0
    for col in (0, 1):
        piv = next((i for i in range(rk, len(rs_)) if rs_[i][col] != 0), None)
        if piv is None:
            continue
        rs_[rk], rs_[piv] = rs_[piv], rs_[rk]
        for i in range(len(rs_)):
            if i != rk and rs_[i][col] != 0:
                f = rs_[i][col] / rs_[rk][col]
                rs_[i] = [u - f * v for u, v in zip(rs_[i], rs_[rk])]
        rk += 1
    return rk


def _suff(eqs, goal):
    if not eqs:
        return False
    rows = [(a, b) for a, b, c in eqs]
    return _rank(rows) == _rank(rows + [goal])


def _opt(s1, s2, both):
    if s1 and s2:
        return SUF[3]
    if s1:
        return SUF[0]
    if s2:
        return SUF[1]
    if both:
        return SUF[2]
    return SUF[4]


def t_sufic_num(r, l):
    goal = r.choice([(1, 0), (0, 1), (1, 1), (1, -1)])
    gtxt = {(1, 0): "a", (0, 1): "b", (1, 1): "a + b", (1, -1): "a − b"}[goal]
    a0, b0 = r.randint(1, 12), r.randint(1, 12)

    def eq():
        x, y = r.randint(-3, 4), r.randint(-3, 4)
        if x == 0 and y == 0:
            raise Reject
        return (x, y, x * a0 + y * b0)

    def txt(e):
        x, y, c = e
        parts = []
        if x:
            parts.append(("−" if x < 0 else "") + ("" if abs(x) == 1 else str(abs(x))) + "a")
        if y:
            sg = ("−" if y < 0 else "+") if parts else ("−" if y < 0 else "")
            parts.append((sg + " " if parts else sg) + ("" if abs(y) == 1 else str(abs(y))) + "b")
        return " ".join(parts) + f" = {c}"
    e0 = eq() if r.random() < 0.5 else None
    e1, e2 = eq(), eq()
    base = [e0] if e0 else []
    ans = _opt(_suff(base + [e1], goal), _suff(base + [e2], goal), _suff(base + [e1, e2], goal))
    lines = [f"¿Cuál es el valor de {gtxt}?"] + ([f"Se sabe que {txt(e0)}"] if e0 else []) + [f"(1) {txt(e1)}", f"(2) {txt(e2)}"]
    lines = [x.replace("-", "−") for x in lines]
    fig = card(lines, 60 + 42 * len(lines), 19)
    stem = f"Suficiencia de datos: a y b son números enteros. ¿Se puede determinar el valor de {gtxt}? Elige la opción según las afirmaciones de la figura."
    return make(stem, fig, ans, [s for s in SUF if s != ans], Q_ARG, "Se comprueba si cada afirmación, sola o junta, determina un único valor.")


def t_sufic_pct(r, l):
    P = r.choice([20000, 40000, 50000, 80000, 100000, 120000])
    d = r.choice([10, 20, 25, 30, 40, 50])
    Fv = F(P * (100 - d), 100)
    D = P - Fv
    st = {
        "A": (f"Con un descuento de {d}%, el precio fue ${int(Fv):,}".replace(",", "."), {"A"}),
        "B": (f"El descuento fue de {d}%", {"B"}),
        "C": (f"El descuento fue de ${int(D):,}".replace(",", "."), {"C"}),
        "D": (f"El precio final fue ${int(Fv):,}".replace(",", "."), {"D"}),
        "E": ("El precio final fue menor que el original", {"E"}),
        "G": (f"El descuento fue mayor que {d - 5}%", {"G"}),
    }
    keys = r.sample(list(st), 2)

    def ok(ks):
        s = set(ks)
        return "A" in s or {"B", "C"} <= s or {"B", "D"} <= s or {"C", "D"} <= s
    k1, k2 = keys
    ans = _opt(ok([k1]), ok([k2]), ok([k1, k2]))
    fig = card(["¿Cuál era el precio original de un artículo?", f"(1) {st[k1][0]}", f"(2) {st[k2][0]}"], 200, 18)
    stem = "Suficiencia de datos: ¿se puede determinar el precio original del artículo? Elige la opción según las afirmaciones (1) y (2) de la figura."
    return make(stem, fig, ans, [s for s in SUF if s != ans], Q_ARG, "El precio original se deduce si se conoce el precio final con su descuento, o el descuento en pesos con su porcentaje.")


BY_SKILL = {
    Q_RES: [c1.t_eval, c2.t_mcm_mcd, c3.t_frac_ops, c4.t_dec_ops, c5.t_ratio_split, c6.t_pct_of, c7.t_discount, c8.t_pow_eval, c9.t_root_eval, c4.t_frac_to_dec, c3.t_mixed],
    Q_MOD: [c1.t_account, c2.t_coincide, c3.t_rest, c4.t_price, c5.t_scale, c6.t_alloy, c7.t_iva, c8.t_growth, c9.t_square_side, c2.t_share, c5.t_mixture],
    Q_REP: [c1.t_numline_expr, c2.t_multiples, c3.t_shaded, c4.t_place, c5.t_graph_prop, c6.t_pie_read, c7.t_change_table, c8.t_pow_table, c9.t_between_ints, c3.t_order_bars],
    Q_ARG: [t_sufic_num, t_sufic_pct, c1.t_error, c2.t_error, c3.t_error, c4.t_error, c5.t_error, c6.t_error, c7.t_error, c8.t_error, c9.t_error],
}
