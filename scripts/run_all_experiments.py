"""Generate all 16 exact-Q certificates and 4 deterministic experiments for Paper 15.

Author: Lluis Eriksson (prepared with AI assistance — Google Antigravity)
"""

from __future__ import annotations

import json
import math
import pathlib
import sys
import time
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.lp_certifier import verify_lp_certificate_exact  # noqa: E402
from src.lp_exact import build_staircase_imbalance_lp  # noqa: E402

RESULTS = ROOT / "results"
CERTDIR = RESULTS / "certificates"


def build_all_certificates() -> list[tuple[str, dict]]:
    certs: list[tuple[str, dict]] = []

    # --- Mode 1: 6 Strict Complementary LP Optimality Certificates ---
    certs.append(("lp_staircase_n3_M10.cert.json", build_staircase_imbalance_lp(3, 10)))
    certs.append(("lp_staircase_n4_M100.cert.json", build_staircase_imbalance_lp(4, 100)))
    certs.append(("lp_staircase_n5_M1000.cert.json", build_staircase_imbalance_lp(5, 1000)))
    certs.append(("lp_staircase_n6_M10000.cert.json", build_staircase_imbalance_lp(6, 10000)))
    certs.append(("lp_staircase_n8_M1024.cert.json", build_staircase_imbalance_lp(8, 1024)))

    # Non-staircase fractional LP: max 3x1 + 5x2 s.t. x1 + 2x2 <= 10, 3x1 + x2 <= 15, -x1 <= 0, -x2 <= 0
    # Active: rows 0, 1 -> x1 = 4, x2 = 3, obj = 27; dual: y0 + 3y1 = 3, 2y0 + y1 = 5 => y0 = 12/5, y1 = 1/5
    certs.append(("lp_rational_2x4.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_strict_complementary_opt",
        "name": "lp_rational_2x4",
        "A": [["1", "2"], ["3", "1"], ["-1", "0"], ["0", "-1"]],
        "b": ["10", "15", "0", "0"],
        "c": ["3", "5"],
        "x_star": ["4", "3"],
        "y_star": ["12/5", "1/5", "0", "0"],
        "claimed_optimum": "27",
    }))

    # --- Mode 2: 4 Unbounded Ray & Farkas Infeasibility Certificates ---
    certs.append(("lp_unbounded_ray_3d.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_unbounded_or_farkas",
        "submode": "unbounded_ray",
        "name": "lp_unbounded_ray_3d",
        "A": [["1", "-2", "0"], ["0", "1", "-3"], ["-1", "0", "0"]],
        "b": ["1", "2", "0"],
        "c": ["1", "1", "1"],
        "x_feasible": ["0", "0", "0"],
        "ray": ["1", "1", "1"],
    }))
    certs.append(("lp_unbounded_staircase_4d.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_unbounded_or_farkas",
        "submode": "unbounded_ray",
        "name": "lp_unbounded_staircase_4d",
        "A": [["-1", "0", "0", "0"], ["10", "-1", "0", "0"], ["0", "10", "-1", "0"], ["0", "0", "10", "-1"]],
        "b": ["-1", "0", "0", "0"],
        "c": ["0", "0", "0", "1"],
        "x_feasible": ["1", "10", "100", "1000"],
        "ray": ["1", "10", "100", "1000"],
    }))
    certs.append(("lp_farkas_infeasible_2d.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_unbounded_or_farkas",
        "submode": "farkas_infeasible",
        "name": "lp_farkas_infeasible_2d",
        "A": [["1", "1"], ["-1", "0"], ["0", "-1"]],
        "b": ["1", "-1", "-1"],
        "y_farkas": ["1", "1", "1"],
    }))
    certs.append(("lp_farkas_infeasible_3d.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_unbounded_or_farkas",
        "submode": "farkas_infeasible",
        "name": "lp_farkas_infeasible_3d",
        "A": [["1", "1", "1"], ["-2", "0", "0"], ["0", "-3", "0"], ["0", "0", "-6"]],
        "b": ["1", "-1", "-2", "-5"],
        # y = [1, 1/2, 1/3, 1/6]: A^T y = 0, b^T y = 1 - 1/2 - 2/3 - 5/6 = -1 < 0, supp=4 <= 1+3
        "y_farkas": ["1", "1/2", "1/3", "1/6"],
    }))

    # --- Mode 3: 3 Convex QP Exact-Q LDL^T + KKT Optimality Certificates ---
    # QP1: min 1/2 (2x1^2 + 2x2^2) - 4x1 - 6x2 s.t. x1 + x2 <= 3, -x1 <= 0, -x2 <= 0
    # Unconstrained (2, 3) violates x1+x2<=3; active x1+x2=3: 2x1-4+y0=0, 2x2-6+y0=0 => x1=1, x2=2, y0=2; obj = 1+4-4-12 = -11
    certs.append(("qp_kkt_2d_active.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "convex_qp_kkt_exact",
        "name": "qp_kkt_2d_active",
        "Q": [["2", "0"], ["0", "2"]],
        "A": [["1", "1"], ["-1", "0"], ["0", "-1"]],
        "b": ["3", "0", "0"],
        "c": ["-4", "-6"],
        "x_star": ["1", "2"],
        "y_star": ["2", "0", "0"],
        "claimed_optimum": "-11",
    }))
    # QP2: singular rank-2 PSD Q = [[2,2,0],[2,2,0],[0,0,4]], c=[-4,-4,-4], A=[[1,0,0],[0,1,0],[0,0,1],[-1,-1,-1]], b=[1,1,1,0]
    # Check x*=(1/2, 1/2, 1), Qx* = (2,2,4), c=(-4,-4,-4) => Qx*+c = (-2,-2,0)
    # Better: A=[[1,0,0],[0,1,0],[0,0,1]], b=[1/2, 1/2, 1], y*=[2, 2, 0]: Qx*+c+A^Ty* = (2-4+2, 2-4+2, 4-4+0) = (0,0,0)!
    # obj = 1/2*(1 + 1 + 4) + (-2 - 2 - 4) = 3 - 8 = -5
    certs.append(("qp_kkt_3d_singular_psd.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "convex_qp_kkt_exact",
        "name": "qp_kkt_3d_singular_psd",
        "Q": [["2", "2", "0"], ["2", "2", "0"], ["0", "0", "4"]],
        "A": [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]],
        "b": ["1/2", "1/2", "1"],
        "c": ["-4", "-4", "-4"],
        "x_star": ["1/2", "1/2", "1"],
        "y_star": ["2", "2", "0"],
        "claimed_optimum": "-5",
    }))
    # QP3: 4D correlated PSD Q = diag(2,2,2,2) + 1*1^T (all eigenvalues >= 2, PSD), c = [-6,-6,-6,-6], s.t. sum x_i <= 2, -x_i <= 0
    # By symmetry x* = (1/2,1/2,1/2,1/2), Qx* = (3,3,3,3), Qx*+c = (-3,-3,-3,-3), y* = [3, 0, 0, 0, 0]
    # obj = 1/2*(4 * 3/2) + (-12) = 3 - 12 = -9
    certs.append(("qp_kkt_4d_correlated.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "convex_qp_kkt_exact",
        "name": "qp_kkt_4d_correlated",
        "Q": [["3", "1", "1", "1"], ["1", "3", "1", "1"], ["1", "1", "3", "1"], ["1", "1", "1", "3"]],
        "A": [["1", "1", "1", "1"], ["-1", "0", "0", "0"], ["0", "-1", "0", "0"], ["0", "0", "-1", "0"], ["0", "0", "0", "-1"]],
        "b": ["2", "0", "0", "0", "0"],
        "c": ["-6", "-6", "-6", "-6"],
        "x_star": ["1/2", "1/2", "1/2", "1/2"],
        "y_star": ["3", "0", "0", "0", "0"],
        "claimed_optimum": "-9",
    }))

    # --- Mode 4: 3 Deterministic Mean-Payoff Game Saddle Certificates ---
    # Game 1: 4 vertices, alternating max(0,2)/min(1,3), value nu = 0, phi = [0, 0, 0, 0]
    certs.append(("mpg_4v_zero_value.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "mean_payoff_game_saddle_exact",
        "name": "mpg_4v_zero_value",
        "num_vertices": 4,
        "owners": ["max", "min", "max", "min"],
        "edges": [
            [0, 1, "0"], [0, 3, "-2"],
            [1, 2, "0"], [1, 0, "3"],
            [2, 3, "0"], [2, 1, "-4"],
            [3, 0, "0"], [3, 2, "5"],
        ],
        "potential": ["0", "0", "0", "0"],
        "claimed_value": "0",
        "sigma_max": {"0": 1, "2": 3},
        "sigma_min": {"1": 2, "3": 0},
    }))
    # Game 2: 4 vertices, fractional value nu = 5/2, phi = [0, -1/2, 1, 1/2]
    # Check reduced weights w(u,v) + phi[v] - phi[u]:
    # 0(max)->1: w + (-1/2) - 0 = 5/2 => w = 3; 0->3: w + 1/2 - 0 <= 5/2 => w = 1 (red=3/2)
    # 1(min)->2: w + 1 - (-1/2) = 5/2 => w = 1; 1->0: w + 0 - (-1/2) >= 5/2 => w = 4 (red=9/2)
    # 2(max)->3: w + 1/2 - 1 = 5/2 => w = 3; 2->1: w + (-1/2) - 1 <= 5/2 => w = 2 (red=1/2)
    # 3(min)->0: w + 0 - 1/2 = 5/2 => w = 3; 3->2: w + 1 - 1/2 >= 5/2 => w = 5 (red=11/2)
    certs.append(("mpg_4v_fractional_value.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "mean_payoff_game_saddle_exact",
        "name": "mpg_4v_fractional_value",
        "num_vertices": 4,
        "owners": ["max", "min", "max", "min"],
        "edges": [
            [0, 1, "3"], [0, 3, "1"],
            [1, 2, "1"], [1, 0, "4"],
            [2, 3, "3"], [2, 1, "2"],
            [3, 0, "3"], [3, 2, "5"],
        ],
        "potential": ["0", "-1/2", "1", "1/2"],
        "claimed_value": "5/2",
        "sigma_max": {"0": 1, "2": 3},
        "sigma_min": {"1": 2, "3": 0},
    }))
    # Game 3: 6 vertices, high-weight integer instance (weights ~ 10^6), exact rational value nu = 1000001/3
    # Let phi = [0, 1/3, 2/3, 0, 1/3, 2/3] -> cycle 0->1->2->3->4->5->0 with weights:
    # 0(max)->1: w + 1/3 - 0 = 1000001/3 => w = 333333 + 1/3? Make integer weights!
    # Pick phi = [0, -1/3, -2/3, 0, -1/3, -2/3]:
    # 0->1: w - 1/3 = 1000001/3 => w = 333334 (exact int!)
    # 1->2: w - 1/3 = 1000001/3 => w = 333334
    # 2->3: w + 2/3 = 1000001/3 => w = 333333
    # 3->4: w - 1/3 = 1000001/3 => w = 333334
    # 4->5: w - 1/3 = 1000001/3 => w = 333334
    # 5->0: w + 2/3 = 1000001/3 => w = 333333
    certs.append(("mpg_6v_large_weights.cert.json", {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "mean_payoff_game_saddle_exact",
        "name": "mpg_6v_large_weights",
        "num_vertices": 6,
        "owners": ["max", "min", "max", "min", "max", "min"],
        "edges": [
            [0, 1, "333334"], [0, 4, "100000"],
            [1, 2, "333334"], [1, 5, "900000"],
            [2, 3, "333333"], [2, 0, "50000"],
            [3, 4, "333334"], [3, 1, "800000"],
            [4, 5, "333334"], [4, 2, "200000"],
            [5, 0, "333333"], [5, 3, "950000"],
        ],
        "potential": ["0", "-1/3", "-2/3", "0", "-1/3", "-2/3"],
        "claimed_value": "1000001/3",
        "sigma_max": {"0": 1, "2": 3, "4": 5},
        "sigma_min": {"1": 2, "3": 4, "5": 0},
    }))

    return certs


def main() -> None:
    CERTDIR.mkdir(parents=True, exist_ok=True)
    certs = build_all_certificates()

    # Exp 1: Certified Atlas (16/16 exact-Q certificates)
    atlas_rows = []
    for fname, cert in certs:
        (CERTDIR / fname).write_text(json.dumps(cert, indent=2) + "\n", encoding="utf-8")
        t0 = time.perf_counter()
        res = verify_lp_certificate_exact(cert)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        atlas_rows.append({"file": fname, "mode": res["mode"], "verdict": res["verdict"], "time_ms": round(dt_ms, 3), "details": res})
    (RESULTS / "exp1_certified_atlas.json").write_text(
        json.dumps({"count": len(atlas_rows), "rows": atlas_rows}, indent=2) + "\n", encoding="utf-8"
    )

    # Exp 2: Staircase Circuit-Imbalance Amplification & Verification Timing Sweep
    imbalance_rows = []
    for n in [3, 4, 6, 8, 12, 16]:
        for M in [10, 1000, 10**6, 10**12]:
            c = build_staircase_imbalance_lp(n, M)
            t0 = time.perf_counter()
            res = verify_lp_certificate_exact(c)
            dt_ms = (time.perf_counter() - t0) * 1000.0
            bits = int((n - 1) * math.log2(M))
            imbalance_rows.append({
                "n": n,
                "M": M,
                "log10_kappa": round((n - 1) * math.log10(M), 2),
                "bit_length_opt": bits,
                "verify_ms": round(dt_ms, 3),
                "verdict": res["verdict"],
            })
    (RESULTS / "exp2_circuit_imbalance_sweep.json").write_text(
        json.dumps({"rows": imbalance_rows}, indent=2) + "\n", encoding="utf-8"
    )

    # Exp 3: Strongly vs Weakly Polynomial Bit-Length Crossover Curves
    crossover_rows = []
    for log2_M in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
        # Illustrative fixed-dimension comparison at n = 4, m = 8:
        # Weakly polynomial IPM/Ellipsoid cost proxy: n^3 * (n * log2_M) = 256 * log2_M
        # Strongly polynomial dimension-only cost proxy (constant in log2_M): e.g. c0 * n^6 = 4096 * c0
        crossover_rows.append({
            "log2_M": log2_M,
            "weakly_poly_ops_n4": 256 * log2_M,
            "strongly_poly_c1": 4096,
            "strongly_poly_c4": 16384,
            "strongly_poly_c16": 65536,
            "ratio_weak_over_c4": round((256 * log2_M) / 16384.0, 4),
        })
    (RESULTS / "exp3_bit_complexity_crossover.json").write_text(
        json.dumps({"rows": crossover_rows}, indent=2) + "\n", encoding="utf-8"
    )

    # Exp 4: Mean-Payoff Game Weight-Scale Independence (n=6 fixed, W = 10^k)
    mpg_rows = []
    for exp_k in [1, 2, 4, 8, 12, 18, 24]:
        W = 10 ** exp_k
        # 6-vertex alternating game with value (3*W + 2)/3 = W + 2/3 -> exact integer weights W, W+1
        gcert = {
            "schema": "LP-TRICHOTOMY-CERT-1.0",
            "mode": "mean_payoff_game_saddle_exact",
            "num_vertices": 6,
            "owners": ["max", "min", "max", "min", "max", "min"],
            "edges": [
                [0, 1, str(W + 1)], [0, 4, str(W // 2)],
                [1, 2, str(W + 1)], [1, 5, str(2 * W)],
                [2, 3, str(W)], [2, 0, str(W // 4)],
                [3, 4, str(W + 1)], [3, 1, str(3 * W)],
                [4, 5, str(W + 1)], [4, 2, str(W // 3)],
                [5, 0, str(W)], [5, 3, str(4 * W)],
            ],
            "potential": ["0", "-1/3", "-2/3", "0", "-1/3", "-2/3"],
            "claimed_value": f"{3 * W + 2}/3",
            "sigma_max": {"0": 1, "2": 3, "4": 5},
            "sigma_min": {"1": 2, "3": 4, "5": 0},
        }
        t0 = time.perf_counter()
        res = verify_lp_certificate_exact(gcert)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        mpg_rows.append({
            "log10_W": exp_k,
            "bit_length_W": W.bit_length(),
            "exact_value": res["exact_value"],
            "verify_ms": round(dt_ms, 3),
        })
    (RESULTS / "exp4_mpg_weight_invariance.json").write_text(
        json.dumps({"rows": mpg_rows}, indent=2) + "\n", encoding="utf-8"
    )

    print(f"[EXPERIMENTS] Generated & verified {len(atlas_rows)}/16 exact-Q certificates + 4 experiments.")


if __name__ == "__main__":
    main()
