"""Clase 20 · Vectores en el plano cartesiano (R² y R³): operatoria, módulo, traslaciones y ponderación por un escalar."""
from fractions import Fraction as F
from math import isqrt
from svgkit import *
from common import Reject
from clase02 import card, pick4, make, fs, Q_RES, Q_MOD, Q_REP, Q_ARG, Q_PRO
from mathfmt import E, fmt
from clase17 import plane
import geo


def V(t):
    return "(" + ", ".join(fs(x) for x in t) + ")"


def add(u, v): return tuple(a + b for a, b in zip(u, v))
def sub(u, v): return tuple(a - b for a, b in zip(u, v))
def sc(k, u): return tuple(k * a for a in u)
def norm2(u): return sum(a * a for a in u)


def modtxt(u):
    n2 = norm2(u)
    return fmt(E((1, int(n2)))) if F(n2).denominator == 1 else fs(F(n2))


def arrow(pl, A, B, color=ACC, w=4, lab=None, dx=0, dy=-16):
    import math
    x1, y1, x2, y2 = pl.X(float(A[0])), pl.Y(float(A[1])), pl.X(float(B[0])), pl.Y(float(B[1]))
    ang = math.atan2(y2 - y1, x2 - x1)
    hl = 14
    p1 = (x2 - hl * math.cos(ang - 0.4), y2 - hl * math.sin(ang - 0.4))
    p2 = (x2 - hl * math.cos(ang + 0.4), y2 - hl * math.sin(ang + 0.4))
    pl.parts.append(L(x1, y1, x2 - 8 * math.cos(ang), y2 - 8 * math.sin(ang), color, w) + P([(x2, y2), p1, p2], color, color, 1))
    if lab:
        pl.parts.append(tag((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, lab, 16))


def rnd_vec(r, n=2, lo=-5, hi=5, nz=True):
    while True:
        v = tuple(r.randint(lo, hi) for _ in range(n))
        if not nz or any(v): return v


def combos(al, be, u, v):
    """Resultados erróneos típicos de α·u + β·v."""
    out = [sub(sc(al, u), sc(be, v)), add(sc(be, u), sc(al, v)), add(sc(al, u), v), add(u, sc(be, v)), (al * u[0] + be * v[0], u[1] + v[1]) if len(u) == 2 else sc(al + be, u),
           (al * u[0] + be * v[1], al * u[1] + be * v[0]) if len(u) == 2 else sc(al, u), sc(al + be, add(u, v)), add(sc(-al, u), sc(be, v))]
    return out


# ---------------------------------------------------------------- Resolver
def t_combo(r, l):
    u, v = rnd_vec(r), rnd_vec(r)
    if u == v: raise Reject
    if l == 0:
        op = r.choice(["+", "−"])
        ans_v = add(u, v) if op == "+" else sub(u, v)
        expr = f"u {op} v"
        al, be = 1, 1 if op == "+" else -1
    elif l == 1:
        al, be = r.choice([2, 3, -1, -2, 4, 3]), r.choice([1, 2, -1, -3, -2, 3])
        ans_v = add(sc(al, u), sc(be, v))
        expr = f"{'' if al == 1 else '−' if al == -1 else al}u {'+' if be > 0 else '−'} {'' if abs(be) == 1 else abs(be)}v"
    else:
        al, be = r.choice([2, 3, F(1, 2), F(3, 2), -2, -3]), r.choice([2, 3, F(1, 2), -1, -2, F(-1, 2)])
        u = tuple(x * 2 for x in u) if any(isinstance(k, F) for k in (al, be)) else u
        v = tuple(x * 2 for x in v) if any(isinstance(k, F) for k in (al, be)) else v
        ans_v = add(sc(F(al), u), sc(F(be), v))
        expr = f"{fs(al)}u {'+' if be > 0 else '−'} {fs(abs(be))}v"
        al, be = F(al), F(be)
    ans = V(ans_v)
    cs = [V(tuple(F(x) for x in c)) for c in combos(al, be, u, v)]
    cs = [c for c in dict.fromkeys(cs) if c != ans]
    pl = plane([(0, 0), u, v] + ([ans_v] if False else []))
    arrow(pl, (0, 0), u, ACC, 4, "u", -14, -14)
    arrow(pl, (0, 0), v, NAVY, 4, "v", 14, -14)
    stem = f"Sean u = {V(u)} y v = {V(v)}. ¿Cuál es el vector {expr}?"
    return make(stem, pl.svg("Vectores u y v"), ans, pick4(ans, cs), Q_RES, f"Se opera componente a componente: {expr} = {ans}.")


def t_from_points(r, l):
    n = 2 if l < 2 else 3
    A = rnd_vec(r, n, -6, 6, False)
    B = rnd_vec(r, n, -6, 6, False)
    if A == B: raise Reject
    AB = sub(B, A)
    if l == 0:
        stem = f"Sean A{V(A)} y B{V(B)}. ¿Cuáles son las componentes del vector AB?"
        ans = V(AB)
        cs = [V(sub(A, B)), V(add(A, B)), V(tuple(abs(x) for x in AB)), V((AB[1], AB[0])), V(sc(F(1, 2), add(A, B))) if all(F(x, 2).denominator == 1 for x in add(A, B)) else V(sc(2, AB)), V((B[0], A[1]))]
        ex = "AB = B − A."
    elif l == 1:
        kind = r.choice(["B", "M"])
        if kind == "B":
            stem = f"El vector AB = {V(AB)} y A{V(A)}. ¿Cuáles son las coordenadas de B?"
            ans = V(B)
            cs = [V(sub(A, AB)), V(AB), V(A), V(sc(2, AB)), V((B[0], -B[1])), V(add(B, (1, 1)))]
            ex = "B = A + AB."
        else:
            if any((a + b) % 2 for a, b in zip(A, B)): raise Reject
            M = tuple(F(a + b, 2) for a, b in zip(A, B))
            stem = f"Sean A{V(A)} y B{V(B)}. ¿Cuáles son las coordenadas del punto medio M del segmento AB?"
            ans = V(M)
            cs = [V(AB), V(add(A, B)), V(sc(F(1, 2), AB)), V(sub(A, B)), V((M[0], -M[1])), V((M[0] + 1, M[1]))]
            ex = "M = (A + B)/2."
    else:
        stem = f"Sean A{V(A)} y B{V(B)} puntos de R³. ¿Cuáles son las componentes del vector AB?"
        ans = V(AB)
        cs = [V(sub(A, B)), V(add(A, B)), V((AB[0], AB[1], -AB[2])), V((AB[2], AB[1], AB[0])), V(tuple(abs(x) for x in AB)), V((AB[0], AB[1], 0))]
        ex = "AB = B − A, componente a componente."
    if n == 2:
        pl = plane([A, B])
        arrow(pl, A, B, ACC, 4)
        from clase17 import label
        label(pl, A, "A", 16, -16); label(pl, B, "B", 16, -16)
        fig = pl.svg("Puntos A y B") if kind_ok(l) else pl.svg("Puntos A y B")
    else:
        fig = card([f"A{V(A)}", f"B{V(B)}", "AB = B − A"], 210, 22)
    cs = [c for c in dict.fromkeys(cs) if c != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_RES, ex)


def kind_ok(l):
    return True


# ---------------------------------------------------------------- Modelar
def t_path(r, l):
    if l == 0:
        d1, d2 = rnd_vec(r), rnd_vec(r)
        P0 = (r.randint(-3, 3), r.randint(-3, 3))
        who = r.choice(["Un dron", "Un barco", "Un robot"])
        P1 = add(P0, d1); P2 = add(P1, d2)
        stem = f"{who} parte del punto {V(P0)} y realiza dos desplazamientos consecutivos: primero {V(d1)} y luego {V(d2)}. ¿En qué punto termina?"
        ans = V(P2)
        cs = [V(add(d1, d2)), V(sub(P0, add(d1, d2))), V(sub(add(P0, d1), d2)), V(add(P0, sc(2, add(d1, d2)))), V(add(P0, d1)), V(add(add(P0, d2), (1, 0)))]
        pl = plane([P0, P1, P2])
        arrow(pl, P0, P1, ACC, 4); arrow(pl, P1, P2, NAVY, 4)
        from clase17 import label
        label(pl, P0, "inicio", 30, -16, False)
        fig = pl.svg("Trayectoria de dos desplazamientos")
        ex = f"Posición final = {V(P0)} + {V(d1)} + {V(d2)} = {ans}."
    elif l == 1:
        a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17)])
        k = r.choice([1, 1, 2])
        flip = r.random() < 0.5
        vb = (a * k, 0) if False else (a * k, b * k)
        cur = (r.choice([-3, -2, 2, 3]) * 1, r.choice([-2, 0, 2]))
        res = add(vb, cur)
        n2 = norm2(res)
        if isqrt(n2) ** 2 != n2: raise Reject
        stem = f"Un bote navega con velocidad {V(vb)} km/h respecto del agua y la corriente tiene velocidad {V(cur)} km/h. ¿Cuál es la rapidez (módulo) de la velocidad resultante?"
        ans = f"{isqrt(n2)} km/h"
        cs = [f"{isqrt(norm2(vb))} km/h" if isqrt(norm2(vb)) ** 2 == norm2(vb) else f"{isqrt(n2) + 1} km/h", f"{abs(vb[0] + cur[0]) + abs(vb[1] + cur[1])} km/h", f"{isqrt(n2) - 1} km/h", f"{isqrt(norm2(vb)) + isqrt(norm2(cur)) if isqrt(norm2(cur)) ** 2 == norm2(cur) else isqrt(n2) + 2} km/h", f"{n2} km/h", f"{isqrt(n2) + 3} km/h"]
        pl = plane([(0, 0), vb, cur, res])
        arrow(pl, (0, 0), vb, ACC, 4, "bote", 0, -16); arrow(pl, (0, 0), cur, NAVY, 4, "corriente", 0, 16)
        fig = pl.svg("Velocidad del bote y de la corriente")
        ex = f"Resultante = {V(vb)} + {V(cur)} = {V(res)}; módulo = √{n2} = {isqrt(n2)} km/h."
    else:
        base = r.choice([(1, 2, 2), (2, 3, 6), (2, 10, 11), (4, 4, 7), (6, 6, 7), (3, 4, 12)])
        # dos desplazamientos en R³ cuya suma tiene módulo entero
        d1 = (base[0], 0, 0)
        d2 = (0, base[1], base[2])
        who = r.choice(["Un dron", "Un globo"])
        P0 = (0, 0, 0)
        tot = add(d1, d2)
        n2 = norm2(tot)
        s = isqrt(n2)
        stem = f"{who} realiza dos desplazamientos consecutivos en el espacio: {V(d1)} m y luego {V(d2)} m. ¿A qué distancia del punto de partida queda?"
        ans = f"{s} m"
        cs = [f"{abs(d1[0]) + d2[1] + d2[2]} m", f"{isqrt(norm2(d2)) + d1[0] if isqrt(norm2(d2)) ** 2 == norm2(d2) else s + 1} m", f"{s + 1} m", f"{s - 1} m", f"{n2} m", f"{s + 2} m"]
        a, b, c = base
        fig = geo.box3d(a, b, c, dict(a=f"{a} m", b=f"{b} m", c=f"{c} m"), diags=[("A", "G")], letters=False)
        ex = f"Desplazamiento total = {V(tot)}; distancia = √({a}² + {b}² + {c}²) = {s} m."
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def t_translate(r, l):
    tri = r.choice([[(0, 0), (4, 0), (0, 3)], [(1, 1), (5, 1), (3, 4)], [(0, 0), (3, 1), (1, 4)], [(-2, 0), (2, 0), (0, 3)]])
    t = rnd_vec(r, 2, -5, 5)
    idx = r.randrange(3)
    names = "ABC"
    img = [add(p, t) for p in tri]
    if l == 0:
        stem = f"Se traslada el triángulo ABC, con A{V(tri[0])}, B{V(tri[1])} y C{V(tri[2])}, según el vector {V(t)}. ¿Cuáles son las coordenadas de {names[idx]}'?"
        ans = V(img[idx])
        cs = [V(sub(tri[idx], t)), V(sc(2, t)), V(add(tri[idx], (t[1], t[0]))), V(sc(2, add(tri[idx], t))) if False else V(add(tri[idx], sc(-1, t))), V(t), V((tri[idx][0] + t[0], tri[idx][1]))]
        ex = f"{names[idx]}' = {names[idx]} + t = {ans}."
    elif l == 1:
        j = (idx + 1) % 3
        stem = f"Un triángulo ABC con A{V(tri[0])}, B{V(tri[1])} y C{V(tri[2])} se traslada. Si {names[idx]}' = {V(img[idx])}, ¿cuáles son las coordenadas de {names[j]}'?"
        ans = V(img[j])
        tt = sub(img[idx], tri[idx])
        cs = [V(sub(tri[j], tt)), V(tt), V(add(img[idx], tri[j])), V(sub(img[idx], tri[j])), V(add(tri[j], (tt[1], tt[0]))), V(sc(2, tt))]
        ex = f"t = {names[idx]}' − {names[idx]} = {V(tt)}; {names[j]}' = {names[j]} + t = {ans}."
    else:
        t2 = rnd_vec(r, 2, -4, 4)
        stem = f"El punto A{V(tri[0])} se traslada según t₁ = {V(t)} y luego según t₂ = {V(t2)}. ¿Cuáles son las coordenadas finales? "
        stem = stem.strip()
        ans = V(add(add(tri[0], t), t2))
        cs = [V(add(tri[0], t)), V(sub(add(tri[0], t), t2)), V(add(tri[0], sc(2, add(t, t2)))), V(add(t, t2)), V(sub(sub(tri[0], t), t2)), V(add(tri[0], sub(t, t2)))]
        ex = f"A'' = A + t₁ + t₂ = {ans}."
    pl = plane(tri + img)
    geo_poly(pl, tri, FILL); geo_poly(pl, img, FILL2)
    arrow(pl, tri[idx], img[idx], ACC, 3)
    fig = pl.svg("Triángulo y su traslación")
    cs = [c for c in dict.fromkeys(cs) if c != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_MOD, ex)


def geo_poly(pl, pts, fill):
    pl.parts.append(P([(pl.X(float(x)), pl.Y(float(y))) for x, y in pts], fill, NAVY, 3))


# ---------------------------------------------------------------- Representar
def t_read_vec(r, l):
    if l == 0:
        A = (0, 0); B = rnd_vec(r, 2, -6, 6)
        pl = plane([A, B])
        arrow(pl, A, B, ACC, 5)
        ans = V(B)
        stem = "En la figura se muestra un vector con origen en el origen del plano. ¿Cuáles son sus componentes?"
    elif l == 1:
        A = rnd_vec(r, 2, -4, 4, False); d = rnd_vec(r); B = add(A, d)
        pl = plane([A, B])
        arrow(pl, A, B, ACC, 5, None)
        from clase17 import label
        label(pl, A, "A", 16, -16); label(pl, B, "B", 16, -16)
        ans = V(d)
        stem = "En la figura se muestra el vector AB. ¿Cuáles son sus componentes?"
    else:
        u, v = rnd_vec(r, 2, -3, 3), rnd_vec(r, 2, -3, 3)
        al, be = r.choice([(1, 1), (2, 1), (1, -1), (2, -1), (1, 2)])
        res = add(sc(al, u), sc(be, v))
        pl = plane([(0, 0), u, v, res])
        arrow(pl, (0, 0), u, ACC, 4, "u", -14, -14); arrow(pl, (0, 0), v, NAVY, 4, "v", 14, -14)
        expr = f"{'' if al == 1 else al}u {'+' if be > 0 else '−'} {'' if abs(be) == 1 else abs(be)}v"
        stem = f"En la figura se muestran los vectores u y v con origen en el origen. ¿Cuáles son las componentes del vector {expr}?"
        ans = V(res)
        B = res; d = res; A = (0, 0)
        cs = [V(c) for c in combos(al, be, u, v)]
        cs = [c for c in dict.fromkeys(cs) if c != ans]
        return make(stem, pl.svg("Vectores u y v"), ans, pick4(ans, cs), Q_REP, f"u = {V(u)}, v = {V(v)}: {expr} = {ans}.")
    d_ = sub(B, A)
    cs = [V((d_[1], d_[0])), V((-d_[0], d_[1])), V((d_[0], -d_[1])), V(B), V((-d_[0], -d_[1])), V((d_[0] + 1, d_[1]))]
    cs = [c for c in dict.fromkeys(cs) if c != ans]
    return make(stem, pl.svg("Vector en el plano cartesiano"), ans, pick4(ans, cs), Q_REP, "Se leen el desplazamiento horizontal y el vertical desde el origen del vector hasta su extremo.")


def vert(a, b, c):
    return dict(A=(0, 0, 0), B=(a, 0, 0), C=(a, b, 0), D=(0, b, 0), E=(0, 0, c), F=(a, 0, c), G=(a, b, c), H=(0, b, c))


def t_box_vec(r, l):
    a, b, c, d = r.choice([(1, 2, 2, 3), (2, 3, 6, 7), (2, 10, 11, 15), (4, 4, 7, 9), (3, 4, 12, 13), (6, 6, 7, 11), (2, 6, 9, 11)])
    vs = vert(a, b, c)
    keys = list("ABCDEFGH")
    if l == 0:
        p, q = "A", "G"
    else:
        p, q = r.sample(keys, 2)
    P_, Q_ = vs[p], vs[q]
    w = sub(Q_, P_)
    fig = geo.box3d(a, b, c, dict(a=str(a), b=str(b), c=str(c)), diags=[(p, q)] if (p, q) in [("A", "G"), ("A", "C"), ("B", "H"), ("C", "E"), ("D", "F"), ("A", "F")] or True else [])
    if l < 2:
        stem = (f"En la caja de la figura, con A = (0, 0, 0), B en el eje x, D en el eje y y E en el eje z, ¿cuáles son las componentes del vector {p}{q}?")
        ans = V(w)
        cs = [V(sub(P_, Q_)), V(tuple(abs(x) for x in w)), V((w[1], w[0], w[2])), V((w[2], w[1], w[0])), V(Q_), V((w[0], w[1], -w[2]))]
        cs = [x for x in dict.fromkeys(cs) if x != ans]
        return make(stem, fig, ans, pick4(ans, cs), Q_REP, f"{q} − {p} = {V(Q_)} − {V(P_)} = {ans}.")
    n2 = norm2(w)
    stem = f"En la caja de la figura, con A = (0, 0, 0), B en el eje x, D en el eje y y E en el eje z, ¿cuánto mide el vector {p}{q}?"
    ans = modtxt(w)
    cs = [str(a + b + c), modtxt((a, b, 0)), modtxt((a, 0, c)), modtxt((0, b, c)), str(d + 1), fmt(E((1, n2 + 1)))]
    cs = [x for x in dict.fromkeys(cs) if x != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_REP, f"|{p}{q}| = √({n2}) = {ans}.")


# ---------------------------------------------------------------- Argumentar
TRUE_V = ["La suma de vectores es conmutativa: u + v = v + u", "El módulo de k·v es |k|·|v|", "Si k < 0, el vector k·v tiene sentido opuesto al de v", "Dos vectores no nulos son paralelos si uno es múltiplo escalar del otro",
          "u + v = 0 si y solo si v = −u", "El vector AB y el vector BA tienen igual módulo y sentidos opuestos"]
FALSE_V = ["El módulo de u + v es siempre |u| + |v|", "El vector k·v siempre tiene el mismo sentido que v", "Un vector queda determinado solo por su módulo", "Dos vectores con igual módulo son siempre iguales",
           "|u − v| = |u| − |v| para todos los vectores u y v", "Si k > 1, el vector k·v es más corto que v", "El vector AB es igual al vector BA"]


def t_props(r, l):
    if l < 2:
        good, bad = r.choice(TRUE_V), r.sample(FALSE_V, 4)
        stem = "Sobre vectores en el plano y en el espacio, ¿cuál de las siguientes afirmaciones es verdadera?"
    else:
        good, bad = r.choice(FALSE_V), r.sample(TRUE_V, 4)
        stem = "Sobre vectores en el plano y en el espacio, ¿cuál de las siguientes afirmaciones es FALSA?"
    u, v = rnd_vec(r, 2, -3, 3), rnd_vec(r, 2, -3, 3)
    pl = plane([(0, 0), u, v, add(u, v)])
    arrow(pl, (0, 0), u, ACC, 4, "u", -14, -14); arrow(pl, (0, 0), v, NAVY, 4, "v", 14, -14)
    return make(stem, pl.svg("Vectores u y v"), good, bad, Q_ARG, "Se razona con la definición de suma de vectores, el producto por un escalar y el módulo.")


def t_parallel(r, l):
    if l == 0:
        a, b = r.choice([(2, 3), (1, 2), (3, 4), (2, 5), (4, 1), (3, 2)])
        m = r.choice([2, 3, -1, -2, 4, 5])
        stem = f"¿Para qué valor de k los vectores u = ({a}, {b}) y v = ({a * m}, k) son paralelos?"
        ans = str(b * m)
        cs = [str(b * m + 1), str(-b * m), str(b + m), str(a * m), str(b), str(F(b, m) if b % m else b * m + 2)]
        cs = [fs(F(c_)) if not isinstance(c_, str) else c_ for c_ in cs]
        u, v = (a, b), (a * m, b * m)
        pl = plane([(0, 0), u, v])
        arrow(pl, (0, 0), u, ACC, 4, "u", -14, -14); arrow(pl, (0, 0), v, NAVY, 4, "v", 14, -14)
        fig = pl.svg("Vectores paralelos")
        ex = f"v = {m}·u ⟹ k = {m}·{b} = {b * m}."
    elif l == 1:
        a, b, c = rnd_vec(r, 3, 1, 4)
        m = r.choice([2, 3, -1, -2])
        stem = f"¿Para qué valores de p y q los vectores u = {V((a, b, c))} y v = ({a * m}, p, q) son paralelos?"
        ans = f"p = {b * m} y q = {c * m}"
        cs = [f"p = {b} y q = {c}", f"p = {c * m} y q = {b * m}", f"p = {-b * m} y q = {c * m}", f"p = {b * m} y q = {-c * m}", f"p = {b + m} y q = {c + m}", f"p = {b * m + 1} y q = {c * m}"]
        fig = card([f"u = {V((a, b, c))}", f"v = ({a * m}, p, q)", "v = m·u"], 210, 22)
        ex = f"v = {m}·u ⟹ p = {b * m}, q = {c * m}."
    else:
        A = rnd_vec(r, 2, -4, 4, False)
        d = rnd_vec(r, 2, 1, 3)
        m = r.choice([2, 3, -1, -2])
        B = add(A, d)
        Cc = (A[0] + m * d[0], "k")
        k = A[1] + m * d[1]
        stem = f"Los puntos A{V(A)}, B{V(B)} y C({A[0] + m * d[0]}, k) son colineales. ¿Cuál es el valor de k?"
        ans = str(k)
        cs = [str(k + 1), str(k - 1), str(-k), str(A[1] + d[1] * (m + 1)), str(B[1] + m * d[1]), str(A[1] + m)]
        pl = plane([A, B, (A[0] + m * d[0], k)])
        arrow(pl, A, B, ACC, 4)
        from clase17 import label
        label(pl, A, "A", 16, -16); label(pl, B, "B", 16, -16); label(pl, (A[0] + m * d[0], k), "C", 16, -16)
        fig = pl.svg("Puntos colineales")
        ex = f"AC = {m}·AB ⟹ k = {A[1]} + {m}·{d[1]} = {k}."
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_ARG, ex)


ERR = ["Sumó los módulos de los vectores en lugar de sumar sus componentes", "Aplicó el escalar solo a una de las componentes", "Restó en el orden equivocado (A − B en lugar de B − A)",
       "Ignoró el signo negativo del escalar", "Calculó el módulo sumando las componentes sin elevarlas al cuadrado"]


def t_error(r, l):
    k = r.choice([0, 1, 2, 3, 4]) if l else r.choice([1, 2, 3])
    u, v = rnd_vec(r, 2, 1, 4), rnd_vec(r, 2, 1, 4)
    if k == 0:
        lines = [f"u = {V(u)}, v = {V(v)}", f"|u| = √{norm2(u)}, |v| = √{norm2(v)}", f"|u + v| = √{norm2(u)} + √{norm2(v)}"]
    elif k == 1:
        s = r.choice([2, 3])
        lines = [f"u = {V(u)}", f"{s}u = {s}·{V(u)}", f"{s}u = {V((s * u[0], u[1]))}"]
    elif k == 2:
        A, B = u, v
        lines = [f"A{V(A)}, B{V(B)}", "AB = A − B", f"AB = {V(sub(A, B))}"]
    elif k == 3:
        s = r.choice([2, 3])
        lines = [f"u = {V(u)}", f"−{s}u = −{s}·{V(u)}", f"−{s}u = {V(sc(s, u))}"]
    else:
        lines = [f"u = {V(u)}", f"|u| = {u[0]} + {u[1]}", f"|u| = {u[0] + u[1]}"]
    lines = [x.replace("-", "−") for x in lines]
    return make("Observa la resolución de un estudiante. ¿Qué error cometió?", card(["Resolución de un estudiante:"] + lines, 220, 19), ERR[k], [x for i, x in enumerate(ERR) if i != k], Q_ARG,
                "Se compara cada paso con el procedimiento correcto: " + ERR[k].lower() + ".")


# ---------------------------------------------------------------- Aplicar procedimientos
def t_module(r, l):
    if l == 0:
        a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (7, 24, 25), (9, 12, 15), (12, 16, 20), (20, 21, 29), (9, 40, 41), (10, 24, 26), (15, 20, 25)])
        if r.random() < 0.5: a, b = b, a
        u = (r.choice([-1, 1]) * a, r.choice([-1, 1]) * b)
        ans = str(c)
        cs = [str(a + b), fmt(E((1, a * a + b * b + 1))), str(abs(a - b)), str(c + 1), fmt(E((1, a * b))), str(a * b)]
        stem = f"¿Cuánto mide el módulo del vector u = {V(u)}?"
        fig = card([f"u = {V(u)}", "|u| = √(x² + y²)"], 190, 22)
    elif l == 1:
        a, b, c, d = r.choice([(1, 2, 2, 3), (2, 3, 6, 7), (2, 10, 11, 15), (4, 4, 7, 9), (3, 4, 12, 13)])
        u = (r.choice([-1, 1]) * a, r.choice([-1, 1]) * b, r.choice([-1, 1]) * c)
        ans = str(d)
        cs = [str(a + b + c), fmt(E((1, a * a + b * b))), str(d + 1), str(d - 1), fmt(E((1, a * a + b * b + c * c + 1))), fmt(E((1, a * b + c * c)))]
        stem = f"¿Cuánto mide el módulo del vector u = {V(u)} de R³?"
        fig = card([f"u = {V(u)}", "|u| = √(x² + y² + z²)"], 190, 22)
    else:
        for _ in range(100):
            u, v = rnd_vec(r, 2, -5, 5), rnd_vec(r, 2, -5, 5)
            al, be = r.choice([2, 3, -1, -2]), r.choice([1, 2, -1, 3])
            w = add(sc(al, u), sc(be, v))
            n2 = norm2(w)
            if isqrt(n2) ** 2 == n2 and n2 > 0: break
        else:
            raise Reject
        ans = str(isqrt(n2))
        cs = [str(abs(al) * isqrt(norm2(u)) + abs(be) * isqrt(norm2(v))) if isqrt(norm2(u)) ** 2 == norm2(u) and isqrt(norm2(v)) ** 2 == norm2(v) else str(isqrt(n2) + 1), fmt(E((1, norm2(u) + norm2(v)))), str(isqrt(n2) + 1), str(isqrt(n2) - 1) if isqrt(n2) > 1 else str(isqrt(n2) + 2), str(n2), str(abs(w[0]) + abs(w[1]))]
        stem = f"Sean u = {V(u)} y v = {V(v)}. ¿Cuánto mide el módulo del vector {al}u {'+' if be > 0 else '−'} {abs(be)}v?".replace("1u", "u").replace("1v", "v")
        fig = card([f"u = {V(u)}", f"v = {V(v)}", "Primero calcula el vector y luego su módulo"], 210, 21)
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, f"Se calcula el vector (si corresponde) y luego |w| = √(suma de los cuadrados de sus componentes) = {ans}.")


def t_scale_unit(r, l):
    a, b, c = r.choice([(3, 4, 5), (5, 12, 13), (6, 8, 10), (8, 15, 17), (9, 12, 15), (7, 24, 25), (12, 16, 20)])
    if r.random() < 0.5: a, b = b, a
    if l == 0:
        u = (r.choice([-1, 1]) * a, r.choice([-1, 1]) * b)
        a, b = u
        stem = f"¿Cuál es el vector unitario que tiene la misma dirección y sentido que u = {V(u)}?"
        ans = V((F(a, c), F(b, c)))
        cs = [V((F(a, 1), F(b, 1))), V((F(-a, c), F(-b, c))), V((F(b, c), F(a, c))), V((F(a, abs(a) + abs(b)), F(b, abs(a) + abs(b)))), V((F(c, a), F(c, b))), V((F(1, a), F(1, b)))]
        fig = card([f"u = {V(u)}", "unitario = u/|u|"], 190, 22)
    elif l == 1:
        m = r.choice([2, 3, 4, 5])
        sgn = r.choice([1, -1])
        u = (a, b)
        target = c * m
        w = (sgn * a * m, sgn * b * m)
        stem = f"¿Cuál es el vector de módulo {target} que tiene {'el mismo sentido' if sgn > 0 else 'sentido opuesto'} que u = {V(u)}?"
        ans = V(w)
        cs = [V((-w[0], -w[1])), V((a * target, b * target)), V((sgn * a * m, sgn * b)), V((sgn * F(a, m), sgn * F(b, m))), V((sgn * a * (m + 1), sgn * b * (m + 1))), V((sgn * b * m, sgn * a * m))]
        fig = card([f"u = {V(u)}", f"|u| = {c}", f"módulo pedido = {target}"], 210, 22)
    else:
        A = rnd_vec(r, 2, -5, 5, False); d = tuple(3 * x for x in rnd_vec(r, 2, -3, 3))
        B = add(A, d)
        t = r.choice([F(1, 3), F(2, 3), F(1, 3)])
        Pp = add(A, sc(t, d))
        stem = f"Sean A{V(A)} y B{V(B)}. ¿Cuáles son las coordenadas del punto P del segmento AB tal que AP = {fs(t)}·AB?"
        ans = V(Pp)
        cs = [V(add(A, sc(1 - t, d))), V(add(B, sc(t, d))), V(sc(t, B)), V(sc(F(1, 2), add(A, B))), V(add(A, sc(t, A))), V(sc(t, d))]
        pl = plane([A, B])
        arrow(pl, A, B, ACC, 4)
        from clase17 import label
        label(pl, A, "A", 16, -16); label(pl, B, "B", 16, -16)
        fig = pl.svg("Segmento AB")
    cs = [c_ for c_ in dict.fromkeys(cs) if c_ != ans]
    return make(stem, fig, ans, pick4(ans, cs), Q_PRO, "Se aplica la ponderación por escalar: k·u tiene módulo |k|·|u| y sentido según el signo de k.")


BY_SKILL = {
    Q_RES: [t_combo, t_from_points],
    Q_MOD: [t_path, t_translate],
    Q_REP: [t_read_vec, t_box_vec],
    Q_ARG: [t_props, t_parallel, t_error],
    Q_PRO: [t_module, t_scale_unit],
}
