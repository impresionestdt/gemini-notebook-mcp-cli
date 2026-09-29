"""Clase 54 (M1) · Repaso Probabilidades: Laplace, regla de la suma y regla del producto."""
from helpers import Q_RES, Q_MOD, Q_REP, Q_ARG
import clase50 as c50, clase51 as c51, clase52 as c52

BY_SKILL = {
    Q_RES: [c50.t_urn, c50.t_dice, c50.t_numbers, c50.t_spin, c51.t_excl, c51.t_urn_or, c51.t_venn_union, c51.t_inclusion, c51.t_excl_prob,
            c52.t_indep, c52.t_repl, c52.t_norepl, c52.t_three],
    Q_MOD: [c50.t_raffle, c50.t_table_prob, c50.t_complement, c50.t_pct, c51.t_survey, c51.t_cards, c51.t_table_or, c51.t_neither,
            c52.t_shots, c52.t_defect, c52.t_weather, c52.t_cards2],
    Q_REP: [c50.t_read_urn, c50.t_impossible, c50.t_convert, c51.t_read_venn, c51.t_formula, c51.t_which_region, c52.t_read_tree, c52.t_hide_tree, c52.t_expr],
    Q_ARG: [c50.t_error, c50.t_claim, c51.t_error, c51.t_claim, c52.t_error, c52.t_indep_claim,
            c50.t_true, c51.t_true, c52.t_true, c50.t_false, c51.t_false, c52.t_false],
}
