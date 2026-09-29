"""Clase 41 (M1) · Repaso Geometría I: integración 2D y 3D (ángulos, Pitágoras, perímetros, áreas y volúmenes)."""
from helpers import Q_RES, Q_MOD, Q_REP, Q_ARG
import clase31 as c31, clase32 as c32, clase33 as c33, clase34 as c34, clase35 as c35

BY_SKILL = {
    Q_RES: [c31.t_angle_calc, c31.t_triangle, c31.t_parallel, c32.t_pyth, c32.t_diag, c32.t_height_iso, c33.t_perim, c33.t_missing_side, c33.t_circle,
            c34.t_area, c34.t_decomp, c34.t_ring, c35.t_prism, c35.t_cylinder, c35.t_find_dim],
    Q_MOD: [c31.t_clock, c31.t_ladder, c31.t_roof, c32.t_walk, c32.t_shortcut, c33.t_lshape, c33.t_track, c33.t_cost, c34.t_paint, c34.t_tiles, c34.t_path,
            c35.t_capacity, c35.t_equiv, c35.t_carton, c35.t_fill],
    Q_REP: [c31.t_relation, c31.t_sum_relation, c31.t_tri_read, c32.t_is_right, c32.t_grid, c33.t_polyomino, c33.t_alg_perimeter, c33.t_compare,
            c34.t_grid, c34.t_expr_area, c34.t_split_expr, c35.t_surface_expr, c35.t_cyl_expr, c35.t_units_table],
    Q_ARG: [c31.t_error, c31.t_exists, c32.t_which_triple, c32.t_error, c33.t_error, c33.t_same_perim, c34.t_error, c34.t_double, c35.t_error, c35.t_scale,
            c31.t_true, c32.t_true, c33.t_true, c34.t_true, c35.t_true, c31.t_false, c32.t_false, c33.t_false, c34.t_false, c35.t_false],
}
