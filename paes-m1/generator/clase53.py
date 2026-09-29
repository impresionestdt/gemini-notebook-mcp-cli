"""Clase 53 (M1) · Repaso Estadística: tablas, gráficos, tendencia central, cuartiles y cajón."""
from helpers import Q_RES, Q_MOD, Q_REP, Q_ARG
import clase45 as c45, clase46 as c46, clase47 as c47, clase48 as c48, clase49 as c49

BY_SKILL = {
    Q_RES: [c45.t_count, c45.t_fr, c45.t_cum, c45.t_missing, c46.t_bar_read, c46.t_pie, c46.t_hist, c46.t_line, c47.t_mean, c47.t_median, c47.t_mode, c47.t_mean_table,
            c48.t_mark, c48.t_mean_g, c48.t_modal, c48.t_median_int, c49.t_quart, c49.t_iqr, c49.t_range_five, c49.t_pct_count],
    Q_MOD: [c45.t_survey, c45.t_total, c45.t_atleast, c45.t_compare, c46.t_more, c46.t_pie_ctx, c46.t_line_pct, c46.t_hist_pct, c47.t_new_value, c47.t_needed, c47.t_leave, c47.t_measure,
            c48.t_below, c48.t_missing, c48.t_est_total, c48.t_compare_g, c49.t_pct_rank, c49.t_wait, c49.t_fence, c49.t_compare_box],
    Q_REP: [c45.t_read, c45.t_complete, c45.t_angle, c46.t_which, c46.t_read_hbars, c46.t_pie_frac, c46.t_angle_pie, c47.t_read_chart, c47.t_table_med, c47.t_match,
            c48.t_read_hist, c48.t_mc_list, c48.t_Fi, c49.t_read_box, c49.t_box_pct, c49.t_summary],
    Q_ARG: [c45.t_error, c45.t_claim, c46.t_error, c46.t_claim, c47.t_error, c47.t_effect, c48.t_error, c48.t_claim, c49.t_error, c49.t_claim,
            c45.t_true, c46.t_true, c47.t_true, c48.t_true, c49.t_true, c45.t_false, c46.t_false, c47.t_false, c48.t_false, c49.t_false],
}
