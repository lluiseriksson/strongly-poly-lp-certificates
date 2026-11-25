"""Pure-stdlib zero-floating-point-trust verifier (LP-TRICHOTOMY-CERT-1.0).

Supports 4 mutually exclusive exact-Q certificate modes aligned with OpenAI's
November 24, 2026 strongly polynomial LP / QP / Mean-Payoff Game theorem:
  1. lp_strict_complementary_opt     : Strict complementary primal-dual LP optimality certificate.
  2. lp_unbounded_or_farkas          : Exact unbounded improving-ray OR Farkas infeasibility certificate.
  3. convex_qp_kkt_exact             : Exact-Q pivoted LDL^T PSD + KKT global QP optimality certificate.
  4. mean_payoff_game_saddle_exact   : Exact-Q potential & positional-strategy game value certificate.

Author: Lluis Eriksson (prepared with AI assistance — Google Antigravity)
"""

from __future__ import annotations

from fractions import Fraction
import re
from typing import Any, Dict, List

from .lp_exact import (
    check_symmetric_psd_exact,
    dot,
    exact_matrix_rank,
    mat_t_vec,
    mat_vec,
    rat_to_str,
)

CERT_SCHEMA = "LP-TRICHOTOMY-CERT-1.0"
VALID_MODES = {
    "lp_strict_complementary_opt",
    "lp_unbounded_or_farkas",
    "convex_qp_kkt_exact",
    "mean_payoff_game_saddle_exact",
}
_RAT_RE = re.compile(r"\A-?[0-9]+(?:/[1-9][0-9]*)?\Z")
MAX_DIM = 64


class CertificateVerificationError(ValueError):
    """Raised whenever an exact LP/QP/game certificate fails any check."""


def _assert_no_floats(obj: Any, path: str = "root") -> None:
    if isinstance(obj, (float, complex)) or type(obj).__name__ == "Decimal":
        raise CertificateVerificationError(f"Floating-point, Decimal, or complex value forbidden at {path}: {obj!r}")
    if isinstance(obj, dict):
        for k, v in obj.items():
            _assert_no_floats(k, f"{path}.<key>")
            _assert_no_floats(v, f"{path}.{k}")
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for i, v in enumerate(obj):
            _assert_no_floats(v, f"{path}[{i}]")


def _parse_int(val: Any, name: str) -> int:
    if isinstance(val, bool) or not isinstance(val, int):
        raise CertificateVerificationError(f"{name} must be an exact int.")
    return val


def _parse_rat(val: Any, name: str) -> Fraction:
    if isinstance(val, bool):
        raise CertificateVerificationError(f"{name} cannot be bool.")
    if isinstance(val, int):
        return Fraction(val)
    if isinstance(val, str):
        if not _RAT_RE.match(val):
            raise CertificateVerificationError(f"{name} is not a canonical rational string: {val!r}")
        if "/" in val:
            a, b = val.split("/")
            return Fraction(int(a), int(b))
        return Fraction(int(val))
    raise CertificateVerificationError(f"{name} must be exact int or rational string.")


def _parse_vec(val: Any, name: str, expected_len: int | None = None) -> List[Fraction]:
    if not isinstance(val, list) or not val or len(val) > MAX_DIM:
        raise CertificateVerificationError(f"{name} must be a non-empty list of length <= {MAX_DIM}.")
    if expected_len is not None and len(val) != expected_len:
        raise CertificateVerificationError(f"{name} length {len(val)} != expected {expected_len}.")
    return [_parse_rat(v, f"{name}[{i}]") for i, v in enumerate(val)]


def _parse_mat(val: Any, name: str) -> List[List[Fraction]]:
    if not isinstance(val, list) or not val or len(val) > MAX_DIM:
        raise CertificateVerificationError(f"{name} must be a non-empty matrix with <= {MAX_DIM} rows.")
    rows = []
    ncols = None
    for i, r in enumerate(val):
        if not isinstance(r, list) or not r or len(r) > MAX_DIM:
            raise CertificateVerificationError(f"{name}[{i}] must be a non-empty row with <= {MAX_DIM} cols.")
        if ncols is None:
            ncols = len(r)
        elif len(r) != ncols:
            raise CertificateVerificationError(f"{name} has ragged row {i}.")
        rows.append([_parse_rat(v, f"{name}[{i}][{j}]") for j, v in enumerate(r)])
    return rows


def _verify_mode1_lp_opt(cert: Dict[str, Any]) -> Dict[str, Any]:
    A = _parse_mat(cert.get("A"), "A")
    m, n = len(A), len(A[0])
    b = _parse_vec(cert.get("b"), "b", m)
    c = _parse_vec(cert.get("c"), "c", n)
    x = _parse_vec(cert.get("x_star"), "x_star", n)
    y = _parse_vec(cert.get("y_star"), "y_star", m)
    claimed_opt = _parse_rat(cert.get("claimed_optimum"), "claimed_optimum")

    Ax = mat_vec(A, x)
    s = [bi - axi for bi, axi in zip(b, Ax)]
    if any(si < 0 for si in s):
        raise CertificateVerificationError("Primal infeasibility: b - A x* has negative entry.")
    if any(yi < 0 for yi in y):
        raise CertificateVerificationError("Dual infeasibility: y* has negative entry.")
    ATy = mat_t_vec(A, y)
    if ATy != c:
        raise CertificateVerificationError("Dual stationarity failed: A^T y* != c.")
    comp = dot(s, y)
    if comp != 0:
        raise CertificateVerificationError(f"Complementary slackness failed: s^T y* = {comp} != 0.")
    if any(si + yi <= 0 for si, yi in zip(s, y)):
        raise CertificateVerificationError("Strict complementarity failed: s_i + y*_i <= 0.")

    primal_obj = dot(c, x)
    dual_obj = dot(b, y)
    if primal_obj != dual_obj or primal_obj != claimed_opt:
        raise CertificateVerificationError(
            f"Strong duality mismatch: c^T x*={primal_obj}, b^T y*={dual_obj}, claimed={claimed_opt}."
        )
    active = [i for i, yi in enumerate(y) if yi > 0]
    slack = [i for i, si in enumerate(s) if si > 0]
    return {
        "schema": CERT_SCHEMA,
        "mode": "lp_strict_complementary_opt",
        "verdict": "LP_STRICT_COMPLEMENTARY_OPTIMAL",
        "m": m,
        "n": n,
        "exact_optimum": rat_to_str(primal_obj),
        "active_support_size": len(active),
        "slack_support_size": len(slack),
    }


def _verify_mode2_unbounded_or_farkas(cert: Dict[str, Any]) -> Dict[str, Any]:
    submode = cert.get("submode")
    if submode not in {"unbounded_ray", "farkas_infeasible"}:
        raise CertificateVerificationError("submode must be 'unbounded_ray' or 'farkas_infeasible'.")
    A = _parse_mat(cert.get("A"), "A")
    m, n = len(A), len(A[0])
    b = _parse_vec(cert.get("b"), "b", m)

    if submode == "unbounded_ray":
        c = _parse_vec(cert.get("c"), "c", n)
        x0 = _parse_vec(cert.get("x_feasible"), "x_feasible", n)
        r = _parse_vec(cert.get("ray"), "ray", n)
        s0 = [bi - axi for bi, axi in zip(b, mat_vec(A, x0))]
        if any(si < 0 for si in s0):
            raise CertificateVerificationError("Base point x_feasible violates A x <= b.")
        Ar = mat_vec(A, r)
        if any(ari > 0 for ari in Ar):
            raise CertificateVerificationError("Ray violates A r <= 0.")
        cr = dot(c, r)
        if cr <= 0:
            raise CertificateVerificationError(f"Ray is not strictly improving: c^T r = {cr} <= 0.")
        return {
            "schema": CERT_SCHEMA,
            "mode": "lp_unbounded_or_farkas",
            "verdict": "LP_UNBOUNDED_CERTIFIED",
            "m": m,
            "n": n,
            "ray_slope": rat_to_str(cr),
        }

    # Farkas infeasibility certificate: y >= 0, A^T y = 0, b^T y < 0, |supp(y)| <= 1 + rank(A)
    y = _parse_vec(cert.get("y_farkas"), "y_farkas", m)
    if any(yi < 0 for yi in y):
        raise CertificateVerificationError("Farkas vector y_farkas has negative entry.")
    ATy = mat_t_vec(A, y)
    if any(v != 0 for v in ATy):
        raise CertificateVerificationError("Farkas stationarity failed: A^T y != 0.")
    by = dot(b, y)
    if by >= 0:
        raise CertificateVerificationError(f"Farkas contradiction failed: b^T y = {by} >= 0.")
    supp = sum(1 for yi in y if yi > 0)
    rank_A = exact_matrix_rank(A)
    if supp > 1 + rank_A:
        raise CertificateVerificationError(
            f"Caratheodory support bound failed: |supp(y)|={supp} > 1 + rank(A)={1 + rank_A}."
        )
    return {
        "schema": CERT_SCHEMA,
        "mode": "lp_unbounded_or_farkas",
        "verdict": "LP_FARKAS_INFEASIBLE_CERTIFIED",
        "m": m,
        "n": n,
        "rank_A": rank_A,
        "support_size": supp,
        "farkas_value": rat_to_str(by),
    }


def _verify_mode3_convex_qp(cert: Dict[str, Any]) -> Dict[str, Any]:
    Q = _parse_mat(cert.get("Q"), "Q")
    n = len(Q)
    if len(Q[0]) != n:
        raise CertificateVerificationError("Q must be square.")
    is_psd, reason, pivots = check_symmetric_psd_exact(Q)
    if not is_psd:
        raise CertificateVerificationError(f"Q failed exact-Q symmetric PSD check: {reason}")
    A = _parse_mat(cert.get("A"), "A")
    m = len(A)
    if len(A[0]) != n:
        raise CertificateVerificationError("A column count must equal dimension of Q.")
    b = _parse_vec(cert.get("b"), "b", m)
    c = _parse_vec(cert.get("c"), "c", n)
    x = _parse_vec(cert.get("x_star"), "x_star", n)
    y = _parse_vec(cert.get("y_star"), "y_star", m)
    claimed_opt = _parse_rat(cert.get("claimed_optimum"), "claimed_optimum")

    # Min 1/2 x^T Q x + c^T x s.t. A x <= b
    s = [bi - axi for bi, axi in zip(b, mat_vec(A, x))]
    if any(si < 0 for si in s):
        raise CertificateVerificationError("QP primal infeasibility: b - A x* < 0.")
    if any(yi < 0 for yi in y):
        raise CertificateVerificationError("QP dual infeasibility: y* < 0.")
    if dot(s, y) != 0:
        raise CertificateVerificationError("QP complementary slackness failed: s^T y* != 0.")
    Qx = mat_vec(Q, x)
    ATy = mat_t_vec(A, y)
    grad = [Qx[j] + c[j] + ATy[j] for j in range(n)]
    if any(g != 0 for g in grad):
        raise CertificateVerificationError("QP KKT stationarity failed: Q x* + c + A^T y* != 0.")

    obj = Fraction(1, 2) * dot(x, Qx) + dot(c, x)
    if obj != claimed_opt:
        raise CertificateVerificationError(f"QP objective {obj} != claimed {claimed_opt}.")
    return {
        "schema": CERT_SCHEMA,
        "mode": "convex_qp_kkt_exact",
        "verdict": "CONVEX_QP_KKT_OPTIMAL",
        "m": m,
        "n": n,
        "exact_optimum": rat_to_str(obj),
        "positive_pivots": sum(1 for p in pivots if p > 0),
    }


def _verify_mode4_mean_payoff_game(cert: Dict[str, Any]) -> Dict[str, Any]:
    num_v = _parse_int(cert.get("num_vertices"), "num_vertices")
    if num_v < 2 or num_v > MAX_DIM:
        raise CertificateVerificationError(f"num_vertices must lie in [2, {MAX_DIM}].")
    owners = cert.get("owners")
    if not isinstance(owners, list) or len(owners) != num_v or any(o not in {"max", "min"} for o in owners):
        raise CertificateVerificationError("owners must be a list of 'max'/'min' of length num_vertices.")
    raw_edges = cert.get("edges")
    if not isinstance(raw_edges, list) or not raw_edges or len(raw_edges) > MAX_DIM * MAX_DIM:
        raise CertificateVerificationError("edges must be a non-empty list.")

    adj: List[List[tuple[int, Fraction]]] = [[] for _ in range(num_v)]
    seen_edges = set()
    for idx, e in enumerate(raw_edges):
        if not isinstance(e, list) or len(e) != 3:
            raise CertificateVerificationError(f"edges[{idx}] must be [u, v, weight].")
        u = _parse_int(e[0], f"edges[{idx}].u")
        v = _parse_int(e[1], f"edges[{idx}].v")
        w = _parse_rat(e[2], f"edges[{idx}].w")
        if not (0 <= u < num_v and 0 <= v < num_v):
            raise CertificateVerificationError(f"edges[{idx}] vertex out of range.")
        if (u, v) in seen_edges:
            raise CertificateVerificationError(f"Duplicate directed edge ({u}, {v}).")
        seen_edges.add((u, v))
        adj[u].append((v, w))

    for u in range(num_v):
        if not adj[u]:
            raise CertificateVerificationError(f"Vertex {u} has out-degree 0 (sink forbidden in mean-payoff game).")

    phi = _parse_vec(cert.get("potential"), "potential", num_v)
    nu = _parse_rat(cert.get("claimed_value"), "claimed_value")
    sigma_max = cert.get("sigma_max")
    sigma_min = cert.get("sigma_min")
    if not isinstance(sigma_max, dict) or not isinstance(sigma_min, dict):
        raise CertificateVerificationError("sigma_max and sigma_min must be dicts mapping str(u) -> target vertex.")

    for u in range(num_v):
        vals = {v: w + phi[v] - phi[u] for v, w in adj[u]}
        if owners[u] == "max":
            # Upper bound: EVERY outgoing edge from a max vertex has reduced weight <= nu
            if any(val > nu for val in vals.values()):
                raise CertificateVerificationError(f"Max vertex {u} has outgoing reduced weight > nu ({nu}).")
            # Lower bound witness: certified positional strategy sigma_max[u] achieves >= nu (hence == nu)
            if str(u) not in sigma_max:
                raise CertificateVerificationError(f"Missing sigma_max choice for max vertex {u}.")
            tgt = _parse_int(sigma_max[str(u)], f"sigma_max[{u}]")
            if tgt not in vals or vals[tgt] < nu:
                raise CertificateVerificationError(f"sigma_max[{u}] -> {tgt} fails reduced weight >= nu.")
        else:
            # Lower bound: EVERY outgoing edge from a min vertex has reduced weight >= nu
            if any(val < nu for val in vals.values()):
                raise CertificateVerificationError(f"Min vertex {u} has outgoing reduced weight < nu ({nu}).")
            # Upper bound witness: certified positional strategy sigma_min[u] achieves <= nu (hence == nu)
            if str(u) not in sigma_min:
                raise CertificateVerificationError(f"Missing sigma_min choice for min vertex {u}.")
            tgt = _parse_int(sigma_min[str(u)], f"sigma_min[{u}]")
            if tgt not in vals or vals[tgt] > nu:
                raise CertificateVerificationError(f"sigma_min[{u}] -> {tgt} fails reduced weight <= nu.")

    return {
        "schema": CERT_SCHEMA,
        "mode": "mean_payoff_game_saddle_exact",
        "verdict": "MEAN_PAYOFF_VALUE_CERTIFIED",
        "num_vertices": num_v,
        "num_edges": len(raw_edges),
        "exact_value": rat_to_str(nu),
    }


def verify_lp_certificate_exact(cert: Any) -> Dict[str, Any]:
    _assert_no_floats(cert)
    if not isinstance(cert, dict):
        raise CertificateVerificationError("Certificate root must be a dict.")
    if cert.get("schema") != CERT_SCHEMA:
        raise CertificateVerificationError(f"Invalid schema: expected {CERT_SCHEMA!r}.")
    mode = cert.get("mode")
    if mode not in VALID_MODES:
        raise CertificateVerificationError(f"Unknown mode: {mode!r}.")

    if mode == "lp_strict_complementary_opt":
        return _verify_mode1_lp_opt(cert)
    if mode == "lp_unbounded_or_farkas":
        return _verify_mode2_unbounded_or_farkas(cert)
    if mode == "convex_qp_kkt_exact":
        return _verify_mode3_convex_qp(cert)
    return _verify_mode4_mean_payoff_game(cert)
