"""Clase 42 (M1) · Repaso Geometría II: geometría proporcional (plano cartesiano, isometrías, semejanza y Thales)."""
from helpers import Q_RES, Q_MOD, Q_REP, Q_ARG
import clase36 as c36, clase37 as c37, clase38 as c38, clase39 as c39, clase40 as c40

BY_SKILL = {
    Q_RES: [c36.t_quadrant, c36.t_midpoint, c36.t_dist, c36.t_vec_op, c37.t_translate, c37.t_reflect_pt, c37.t_find_img, c37.t_compose, c38.t_rot_pt, c38.t_rot_center,
            c39.t_side, c39.t_perim_area, c39.t_tri_prop, c40.t_ec, c40.t_de, c40.t_par3, c40.t_ab],
    Q_MOD: [c36.t_route, c36.t_map, c36.t_area, c36.t_disp, c37.t_perim, c37.t_mirror, c37.t_tiles, c38.t_blades, c38.t_clock, c38.t_turns,
            c39.t_shadow, c39.t_map, c39.t_photo, c40.t_river, c40.t_streets, c40.t_split],
    Q_REP: [c36.t_read_point, c36.t_vec_fig, c36.t_reflect, c37.t_which, c37.t_read_img, c37.t_rule, c38.t_which_rot, c38.t_read_rot, c38.t_sym,
            c39.t_read_sim, c39.t_expr, c39.t_table, c40.t_read_prop, c40.t_read_par, c40.t_table],
    Q_ARG: [c36.t_error, c36.t_claim, c37.t_error, c37.t_prop, c38.t_error, c38.t_prop, c39.t_error, c39.t_crit, c40.t_error, c40.t_converse,
            c36.t_true, c37.t_true, c38.t_true, c39.t_true, c40.t_true, c36.t_false, c37.t_false, c38.t_false, c39.t_false, c40.t_false],
}
