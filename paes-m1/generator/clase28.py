"""Clase 28 (M1) · Repaso del eje Álgebra y Funciones: discriminación entre modelos lineales y cuadráticos."""
from fractions import Fraction as F
from svgkit import *
from common import Reject
from helpers import card, pick4, make, fs, Plot, Q_RES, Q_MOD, Q_REP, Q_ARG
from clase25 import quad, M, rr
import viz
import clase13 as c13, clase14 as c14, clase15 as c15, clase16 as c16, clase17 as c17, clase18 as c18, clase19 as c19, clase20 as c20, clase21 as c21
import clase22 as c22, clase23 as c23, clase24 as c24, clase25 as c25, clase26 as c26, clase27 as c27


TYPES = ["Lineal", "Cuadrática"]


def t_model_type(r, l):
    kind = r.choice(["lin", "quad"])
    xs = [0, 1, 2, 3, 4, 5]
    if kind == "lin":
        a, b = rr(r, -4, 5), rr(r, -6, 8)
        ys = [a * x + b for x in xs]
        ans = "Lineal, porque la variación de y entre valores consecutivos de x es constante"
    else:
        a, b, c = rr(r, -3, 3), rr(r, -4, 4), rr(r, -5, 5)
        ys = [a * x * x + b * x + c for x in xs]
        ans = "Cuadrática, porque las variaciones de y cambian de forma constante (las segundas diferencias son iguales)"
    fig = viz.table_fig(["x"] + [str(x) for x in xs], [["y"] + [str(y).replace("-", "−") for y in ys]])
    stem = "La tabla muestra los valores de una función para x = 0, 1, 2, 3, 4, 5. ¿Qué tipo de modelo la representa mejor y por qué?"
    opts = ["Lineal, porque la variación de y entre valores consecutivos de x es constante", "Cuadrática, porque las variaciones de y cambian de forma constante (las segundas diferencias son iguales)",
            "Lineal, porque todos los valores de y son números enteros positivos y negativos", "Cuadrática, porque el valor de y para x = 0 es distinto de cero",
            "Ninguno de los dos, porque los valores de y no siguen ningún patrón"]
    al = [o for o in opts if o != ans]
    return make(stem, fig, ans, al, Q_ARG, "En un modelo lineal las primeras diferencias son constantes; en uno cuadrático lo son las segundas diferencias.")


CTX = [("El área de un cuadrado según la medida de su lado", "Cuadrática", "el área depende del cuadrado del lado"), ("El costo de comprar kilos de fruta a un precio fijo por kilo", "Lineal", "el costo aumenta lo mismo por cada kilo"),
       ("La altura de una pelota lanzada hacia arriba según el tiempo", "Cuadrática", "la trayectoria es una parábola"), ("El pago mensual de un plan con cargo fijo y precio por unidad", "Lineal", "el pago aumenta lo mismo por cada unidad"),
       ("El área de un círculo según la medida de su radio", "Cuadrática", "el área depende del cuadrado del radio"), ("La distancia recorrida a rapidez constante según el tiempo", "Lineal", "la distancia aumenta lo mismo en cada segundo"),
       ("La ganancia de una empresa cuando el precio baja al vender más unidades", "Cuadrática", "la ganancia sube hasta un máximo y luego baja"), ("La temperatura convertida de grados Celsius a Fahrenheit", "Lineal", "la relación entre ambas escalas es de primer grado")]


def t_context_type(r, l):
    c = r.choice(CTX)
    fig = card(["Situación:", c[0]], 130, 18)
    other = "Cuadrática" if c[1] == "Lineal" else "Lineal"
    ans = f"{c[1]}, porque {c[2]}"
    alts = [f"{other}, porque {c[2]}", f"{other}, porque la situación involucra dos variables", f"{c[1]}, porque siempre se cumple que a mayor valor de x mayor valor de y", "Ninguno, porque la situación no puede modelarse con una función"]
    stem = "¿Qué tipo de modelo (lineal o cuadrático) describe mejor la situación de la figura?"
    return make(stem, fig, ans, alts, Q_ARG, "Se decide según cómo cambia la cantidad dependiente: variación constante (lineal) o dependencia del cuadrado (cuadrática).")


def t_graph_type(r, l):
    kind = r.choice(["lin", "quad"])
    p = Plot(560, 300, -6, 6, -8, 8)
    p.axes(2, 2)
    if kind == "lin":
        a, b = rr(r, -2, 2), rr(r, -3, 3)
        p.curve(lambda x: a * x + b, -6, 6, ACC, 4.5)
    else:
        a, h, k = r.choice([1, -1]), r.randint(-3, 3), r.randint(-4, 4)
        p.curve(lambda x: a * (x - h) ** 2 + k, -6, 6, ACC, 4.5)
    fig = p.svg("Gráfico de una función")
    ans = "Lineal: su gráfico es una recta" if kind == "lin" else "Cuadrática: su gráfico es una parábola"
    opts = ["Lineal: su gráfico es una recta", "Cuadrática: su gráfico es una parábola", "Lineal: su gráfico tiene un vértice", "Cuadrática: su gráfico es una recta que pasa por el origen", "Ninguna: el gráfico no corresponde a una función"]
    al = [o for o in opts if o != ans]
    return make("¿Qué tipo de función representa el gráfico y por qué?", fig, ans, al, Q_REP, "La recta corresponde a una función de primer grado y la parábola a una de segundo grado.")


BY_SKILL = {
    Q_RES: [c13.t_eval_expr, c14.t_reduce, c15.t_expand, c16.t_factor, c17.t_solve, c19.t_solve, c21.t_solve, c22.t_eval, c23.t_slope, c26.t_vertex, c27.t_solve, c25.t_eval],
    Q_MOD: [c17.t_balance, c18.t_pose, c19.t_prices, c20.t_decide, c21.t_budget, c24.t_choose, c26.t_projectile, c27.t_ground, c26.t_profit_max, c15.t_garden, c14.t_perimeter],
    Q_REP: [c17.t_numline_sol, c19.t_graph, c21.t_read_interval, c22.t_table, c23.t_read_line, c25.t_equation_from_graph, c27.t_graph_roots, t_graph_type, c26.t_graph_vertex, c16.t_area_read],
    Q_ARG: [t_model_type, t_context_type, c20.t_decision_arg, c13.t_error, c14.t_error, c15.t_error, c16.t_error, c17.t_error, c19.t_error, c21.t_error, c22.t_error, c23.t_error, c24.t_error, c25.t_error, c26.t_error, c27.t_error],
}
