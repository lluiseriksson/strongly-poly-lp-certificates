"""Generate 3 publication-grade 300-DPI figures for Paper 15.

Author: Lluis Eriksson
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
FIGDIR = ROOT / "paper" / "figures"

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 10.5,
    "axes.labelsize": 10,
    "legend.fontsize": 8.0,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "axes.grid": True,
    "grid.alpha": 0.28,
})


def make_fig1() -> None:
    d = json.loads((RESULTS / "exp2_circuit_imbalance_sweep.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.2), constrained_layout=True)

    colors = {10: "#1565c0", 1000: "#2e7d32", 10**6: "#ef6c00", 10**12: "#c62828"}
    labels = {10: r"$M = 10$", 1000: r"$M = 10^3$", 10**6: r"$M = 10^6$", 10**12: r"$M = 10^{12}$"}
    for M in [10, 1000, 10**6, 10**12]:
        sub = [r for r in rows if r["M"] == M]
        ns = [r["n"] for r in sub]
        lk = [r["log10_kappa"] for r in sub]
        ms = [r["verify_ms"] for r in sub]
        ax1.plot(ns, lk, "o-", color=colors[M], lw=2.0, ms=5.0, label=labels[M])
        ax2.plot(ns, ms, "s-", color=colors[M], lw=2.0, ms=5.0, label=labels[M])

    ax1.set_xlabel(r"LP dimension $n$ ($m = 2n$ constraints)")
    ax1.set_ylabel(r"Exact log circuit imbalance $\log_{10} \kappa(A_n(M))$")
    ax1.set_title(r"(a) Exact Staircase Circuit Imbalance $\kappa = M^{n-1}$")
    ax1.legend(loc="upper left", frameon=True, framealpha=0.92)

    ax2.set_xlabel(r"LP dimension $n$ ($m = 2n$ constraints)")
    ax2.set_ylabel(r"Exact-$\mathbb{Q}$ certificate verification time (ms)")
    ax2.set_title(r"(b) Zero-Float Exact-$\mathbb{Q}$ Replay Time Across $10^{180}$ Imbalance")
    ax2.legend(loc="upper left", frameon=True, framealpha=0.92)

    FIGDIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGDIR / "fig1_circuit_imbalance_scaling.png", bbox_inches="tight")
    plt.close(fig)


def make_fig2() -> None:
    d = json.loads((RESULTS / "exp3_bit_complexity_crossover.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    L = [r["log2_M"] for r in rows]
    w_ops = [r["weakly_poly_ops_n4"] for r in rows]
    c1 = [r["strongly_poly_c1"] for r in rows]
    c4 = [r["strongly_poly_c4"] for r in rows]
    c16 = [r["strongly_poly_c16"] for r in rows]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.2), constrained_layout=True)

    ax1.loglog(L, w_ops, "k-o", lw=2.2, ms=5.0, label=r"Weakly poly bit-bound $n^4 \log_2 M$ ($n=4$)")
    ax1.loglog(L, c1, "--", color="#2e7d32", lw=2.0, label=r"Strongly poly ceiling ($C_1 = 4{,}096$)")
    ax1.loglog(L, c4, "-.", color="#1565c0", lw=2.0, label=r"Strongly poly ceiling ($C_4 = 16{,}384$)")
    ax1.loglog(L, c16, ":", color="#c62828", lw=2.2, label=r"Strongly poly ceiling ($C_{16} = 65{,}536$)")
    ax1.set_xlabel(r"Coefficient bit-length $\log_2 M$ (fixed $n = 4, m = 8$)")
    ax1.set_ylabel(r"Arithmetic operation bound")
    ax1.set_title(r"(a) Strongly vs. Weakly Polynomial Bit-Length Separation")
    ax1.legend(loc="lower right", frameon=True, framealpha=0.92, fontsize=7.6)

    d4 = json.loads((RESULTS / "exp4_mpg_weight_invariance.json").read_text(encoding="utf-8"))
    mrows = d4["rows"]
    logw = [r["log10_W"] for r in mrows]
    vms = [r["verify_ms"] for r in mrows]
    ax2.plot(logw, vms, "D-", color="#6a1b9a", lw=2.1, ms=5.5, label=r"6-vertex exact-$\mathbb{Q}$ saddle verification")
    ax2.set_xlabel(r"Payoff weight magnitude $\log_{10} W$ (up to $W = 10^{24}$)")
    ax2.set_ylabel(r"Exact-$\mathbb{Q}$ certificate verification time (ms)")
    ax2.set_ylim(0, max(vms) * 1.45 + 0.05)
    ax2.set_title(r"(b) Weight-Scale Independence of Mean-Payoff Game Certificates")
    ax2.legend(loc="upper left", frameon=True, framealpha=0.92)

    fig.savefig(FIGDIR / "fig2_strongly_poly_crossover_and_mpg.png", bbox_inches="tight")
    plt.close(fig)


def make_fig3() -> None:
    d = json.loads((RESULTS / "exp1_certified_atlas.json").read_text(encoding="utf-8"))
    rows = d["rows"]
    modes = [
        ("lp_strict_complementary_opt", "Mode 1:\nLP Strict Opt", "#1565c0"),
        ("lp_unbounded_or_farkas", "Mode 2:\nRay / Farkas", "#2e7d32"),
        ("convex_qp_kkt_exact", "Mode 3:\nConvex QP KKT", "#ef6c00"),
        ("mean_payoff_game_saddle_exact", "Mode 4:\nMPG Saddle", "#6a1b9a"),
    ]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.6, 4.2), constrained_layout=True)

    names = [r["file"].replace(".cert.json", "") for r in rows]
    times = [r["time_ms"] for r in rows]
    col_map = {m[0]: m[2] for m in modes}
    cols = [col_map[r["mode"]] for r in rows]
    y_pos = np.arange(len(names))
    ax1.barh(y_pos, times, color=cols, edgecolor="black", lw=0.6)
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(names, fontsize=7.0)
    ax1.invert_yaxis()
    ax1.set_xlabel(r"Exact-$\mathbb{Q}$ verification time (ms)")
    ax1.set_title(r"(a) Exact-$\mathbb{Q}$ Verification Latency (16 Instances)")

    mode_labels = [m[1] for m in modes]
    mode_counts = [sum(1 for r in rows if r["mode"] == m[0]) for m in modes]
    mode_cols = [m[2] for m in modes]
    bars = ax2.bar(mode_labels, mode_counts, color=mode_cols, edgecolor="black", lw=0.7, width=0.52)
    for b, v in zip(bars, mode_counts):
        ax2.text(b.get_x() + b.get_width() / 2, v + 0.15, str(v), ha="center", va="bottom", fontweight="bold")
    ax2.set_ylim(0, max(mode_counts) + 1.5)
    ax2.set_ylabel(r"Certified exact-$\mathbb{Q}$ instances (100% pass)")
    ax2.tick_params(axis="x", labelsize=8.4)
    ax2.set_title(r"(b) Four-Mode Certificate Coverage")

    fig.savefig(FIGDIR / "fig3_atlas_verification_summary.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_fig1()
    make_fig2()
    make_fig3()
    print("[FIGURES] Generated 3 publication-grade 300-DPI figures in paper/figures/.")


if __name__ == "__main__":
    main()
