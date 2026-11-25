"""52-attack adversarial red-team and exact certificate verification test suite for Paper 15.

Author: Lluis Eriksson
"""

from __future__ import annotations

import copy
import json
import pathlib
import pytest

from src.lp_certifier import CertificateVerificationError, verify_lp_certificate_exact

ROOT = pathlib.Path(__file__).resolve().parent.parent
CERTDIR = ROOT / "results" / "certificates"


def _load(name: str) -> dict:
    return json.loads((CERTDIR / name).read_text(encoding="utf-8"))


def test_all_16_certificates_verify_cleanly() -> None:
    files = sorted(CERTDIR.glob("*.cert.json"))
    assert len(files) == 16
    for f in files:
        res = verify_lp_certificate_exact(json.loads(f.read_text(encoding="utf-8")))
        assert res["schema"] == "LP-TRICHOTOMY-CERT-1.0"


def test_52_live_adversarial_red_team_attacks_rejected() -> None:
    c_opt = _load("lp_rational_2x4.cert.json")
    c_ray = _load("lp_unbounded_ray_3d.cert.json")
    c_far = _load("lp_farkas_infeasible_3d.cert.json")
    c_qp = _load("qp_kkt_3d_singular_psd.cert.json")
    c_mpg = _load("mpg_4v_fractional_value.cert.json")

    attacks = []

    def add(name: str, base: dict, mut) -> None:
        c = copy.deepcopy(base)
        mut(c)
        attacks.append((name, c))

    # --- Global / Type / Float / Schema Attacks (A01-A12) ---
    add("A01_float_in_b", c_opt, lambda c: c["b"].__setitem__(0, 10.0))
    add("A02_nan_float", c_opt, lambda c: c.__setitem__("extra", float("nan")))
    add("A03_inf_float", c_opt, lambda c: c.__setitem__("extra", float("inf")))
    add("A04_complex_smuggling", c_opt, lambda c: c.__setitem__("extra", 1 + 2j))
    add("A05_tuple_float_smuggling", c_opt, lambda c: c.__setitem__("extra", (0.5,)))
    add("A06_float_dict_key", c_opt, lambda c: c.__setitem__(1.5, "bad"))
    add("A07_decimal_string", c_opt, lambda c: c.__setitem__("claimed_optimum", "27.0"))
    add("A08_zero_denominator", c_opt, lambda c: c["y_star"].__setitem__(0, "12/0"))
    add("A09_bool_value", c_opt, lambda c: c["b"].__setitem__(0, True))
    add("A10_wrong_schema", c_opt, lambda c: c.__setitem__("schema", "BAD-1.0"))
    add("A11_unknown_mode", c_opt, lambda c: c.__setitem__("mode", "fake_mode"))
    attacks.append(("A12_non_dict_root", []))

    # --- Mode 1: LP Strict Complementary Opt Attacks (A13-A22) ---
    add("A13_primal_infeasible_x", c_opt, lambda c: c["x_star"].__setitem__(0, "5"))
    add("A14_dual_negative_y", c_opt, lambda c: c["y_star"].__setitem__(2, "-1"))
    add("A15_dual_stationarity_break", c_opt, lambda c: c["y_star"].__setitem__(0, "2"))
    add("A16_complementary_slackness_break", c_opt, lambda c: c["b"].__setitem__(0, "11"))
    add("A17_strict_complementarity_both_zero", c_opt, lambda c: (c["b"].__setitem__(2, "-4")))
    add("A18_forged_claimed_opt", c_opt, lambda c: c.__setitem__("claimed_optimum", "28"))
    add("A19_ragged_matrix_A", c_opt, lambda c: c["A"][0].append("1"))
    add("A20_wrong_x_dim", c_opt, lambda c: c["x_star"].append("0"))
    add("A21_wrong_y_dim", c_opt, lambda c: c["y_star"].pop())
    add("A22_empty_A", c_opt, lambda c: c.__setitem__("A", []))

    # --- Mode 2: Unbounded Ray & Farkas Infeasibility Attacks (A23-A32) ---
    add("A23_bad_submode", c_ray, lambda c: c.__setitem__("submode", "unknown"))
    add("A24_infeasible_base_x0", c_ray, lambda c: c["x_feasible"].__setitem__(0, "-1"))
    add("A25_ray_violates_Ar_le_0", c_ray, lambda c: c["ray"].__setitem__(0, "3"))
    add("A26_ray_zero_slope", c_ray, lambda c: c.__setitem__("ray", ["0", "0", "0"]))
    add("A27_ray_negative_slope", c_ray, lambda c: c.__setitem__("c", ["-1", "-1", "-1"]))
    add("A28_farkas_negative_y", c_far, lambda c: c["y_farkas"].__setitem__(0, "-1"))
    add("A29_farkas_ATy_nonzero", c_far, lambda c: c["y_farkas"].__setitem__(1, "1"))
    add("A30_farkas_by_nonnegative", c_far, lambda c: c["b"].__setitem__(0, "5"))
    add("A31_farkas_zero_vector", c_far, lambda c: c.__setitem__("y_farkas", ["0", "0", "0", "0"]))
    add("A32_farkas_caratheodory_support_exceeded", c_far, lambda c: (
        c["A"].append(["0", "0", "0"]),
        c["b"].append("-1"),
        c["y_farkas"].append("1"),
    ))

    # --- Mode 3: Convex QP Exact-Q LDL^T + KKT Attacks (A33-A42) ---
    add("A33_non_symmetric_Q", c_qp, lambda c: c["Q"][0].__setitem__(1, "3"))
    add("A34_indefinite_negative_diag_Q", c_qp, lambda c: c["Q"][2].__setitem__(2, "-4"))
    add("A35_indefinite_offdiag_Q", c_qp, lambda c: (c["Q"][0].__setitem__(1, "5"), c["Q"][1].__setitem__(0, "5")))
    add("A36_zero_diag_nonzero_offdiag_Q", c_qp, lambda c: (c["Q"][0].__setitem__(0, "0"), c["Q"][1].__setitem__(1, "0")))
    add("A37_qp_primal_infeasible", c_qp, lambda c: c["x_star"].__setitem__(0, "1"))
    add("A38_qp_dual_negative", c_qp, lambda c: c["y_star"].__setitem__(2, "-1"))
    add("A39_qp_comp_slack_fail", c_qp, lambda c: c["b"].__setitem__(0, "2"))
    add("A40_qp_kkt_stationarity_fail", c_qp, lambda c: c["c"].__setitem__(0, "-5"))
    add("A41_qp_forged_optimum", c_qp, lambda c: c.__setitem__("claimed_optimum", "-4"))
    add("A42_qp_dim_mismatch", c_qp, lambda c: c["Q"].pop())

    # --- Mode 4: Mean-Payoff Game Saddle Attacks (A43-A52) ---
    add("A43_mpg_nu_too_low_max_violates", c_mpg, lambda c: c.__setitem__("claimed_value", "2"))
    add("A44_mpg_nu_too_high_min_violates", c_mpg, lambda c: c.__setitem__("claimed_value", "3"))
    add("A45_mpg_tampered_potential", c_mpg, lambda c: c["potential"].__setitem__(0, "1"))
    add("A46_mpg_suboptimal_sigma_max", c_mpg, lambda c: c["sigma_max"].__setitem__("0", 3))
    add("A47_mpg_suboptimal_sigma_min", c_mpg, lambda c: c["sigma_min"].__setitem__("1", 0))
    add("A48_mpg_missing_sigma_max", c_mpg, lambda c: c["sigma_max"].pop("0"))
    add("A49_mpg_duplicate_edge", c_mpg, lambda c: c["edges"].append([0, 1, "3"]))
    add("A50_mpg_sink_vertex", c_mpg, lambda c: c.__setitem__("edges", [e for e in c["edges"] if e[0] != 3]))
    add("A51_mpg_invalid_owner", c_mpg, lambda c: c["owners"].__setitem__(0, "chance"))
    add("A52_mpg_bool_vertex_id", c_mpg, lambda c: c["edges"][0].__setitem__(0, True))

    assert len(attacks) == 52
    for name, bad_cert in attacks:
        with pytest.raises(CertificateVerificationError, match="."):
            verify_lp_certificate_exact(bad_cert)
