"""Pure-stdlib exact-Q linear algebra, pivoted LDL^T PSD check, and benchmark generators.

Author: Lluis Eriksson (prepared with AI assistance — Google Antigravity)
"""

from __future__ import annotations

from fractions import Fraction
from typing import List, Tuple


def rat_to_str(q: Fraction) -> str:
    if q.denominator == 1:
        return str(q.numerator)
    return f"{q.numerator}/{q.denominator}"


def mat_vec(A: List[List[Fraction]], x: List[Fraction]) -> List[Fraction]:
    return [sum(a_ij * x_j for a_ij, x_j in zip(row, x)) for row in A]


def mat_t_vec(A: List[List[Fraction]], y: List[Fraction]) -> List[Fraction]:
    if not A:
        return []
    n = len(A[0])
    out = [Fraction(0) for _ in range(n)]
    for row, y_i in zip(A, y):
        for j, a_ij in enumerate(row):
            out[j] += a_ij * y_i
    return out


def dot(u: List[Fraction], v: List[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(u, v))


def exact_matrix_rank(A: List[List[Fraction]]) -> int:
    """Exact Gaussian elimination over Q to compute rank(A) without floats."""
    if not A or not A[0]:
        return 0
    M = [row[:] for row in A]
    m, n = len(M), len(M[0])
    r = 0
    for col in range(n):
        piv = None
        for i in range(r, m):
            if M[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][col]
        for i in range(r + 1, m):
            if M[i][col] != 0:
                fac = M[i][col] / pv
                for j in range(col, n):
                    M[i][j] -= fac * M[r][j]
        r += 1
        if r == m:
            break
    return r


def check_symmetric_psd_exact(Q: List[List[Fraction]]) -> Tuple[bool, str, List[Fraction]]:
    """Exact-Q symmetric positive semidefiniteness check via pivoted LDL^T (zero floats).

    Returns (is_psd, reason, diagonal_pivots).
    """
    n = len(Q)
    if n == 0:
        return False, "Empty matrix", []
    for i in range(n):
        if len(Q[i]) != n:
            return False, "Non-square matrix", []
        for j in range(i + 1, n):
            if Q[i][j] != Q[j][i]:
                return False, f"Matrix not symmetric at ({i},{j})", []

    M = [row[:] for row in Q]
    pivots: List[Fraction] = []
    for k in range(n):
        # Diagonal check: any negative diagonal entry proves indefiniteness immediately
        for i in range(k, n):
            if M[i][i] < 0:
                return False, f"Negative Schur diagonal at index {i}: {M[i][i]}", pivots
        # Find largest diagonal entry among k..n-1
        best = k
        for i in range(k + 1, n):
            if M[i][i] > M[best][best]:
                best = i
        if best != k:
            M[k], M[best] = M[best], M[k]
            for row in M:
                row[k], row[best] = row[best], row[k]
        piv = M[k][k]
        if piv == 0:
            # For PSD, if diagonal is 0, entire remaining row/col must be 0
            for j in range(k + 1, n):
                if M[k][j] != 0 or M[j][k] != 0:
                    return False, f"Zero diagonal with nonzero off-diagonal at ({k},{j})", pivots
            pivots.append(Fraction(0))
            continue
        pivots.append(piv)
        for i in range(k + 1, n):
            fac = M[i][k] / piv
            for j in range(k + 1, n):
                M[i][j] -= fac * M[k][j]
            M[i][k] = Fraction(0)
            M[k][i] = Fraction(0)
    return True, "PSD_CERTIFIED", pivots


def build_staircase_imbalance_lp(n: int, M: int) -> dict:
    """Build exact-Q staircase LP with exact circuit imbalance kappa = M^(n-1).

    Maximize x_n subject to:
      x_1 <= 1
      x_{j+1} - M * x_j <= 0  for j = 1..n-1
      -x_j <= 0               for j = 1..n
    Unique strictly complementary optimal vertex: x*_j = M^(j-1),
    active constraints: first n inequalities with y*_j = M^(n-j) > 0,
    strictly slack constraints: -x_j <= 0 with s*_{n+j} = M^(j-1) > 0.
    """
    A: List[List[str]] = []
    b: List[str] = []
    # Row 0: x_1 <= 1
    r0 = ["0"] * n
    r0[0] = "1"
    A.append(r0)
    b.append("1")
    # Rows 1..n-1: x_{j+1} - M*x_j <= 0
    for j in range(n - 1):
        row = ["0"] * n
        row[j] = str(-M)
        row[j + 1] = "1"
        A.append(row)
        b.append("0")
    # Rows n..2n-1: -x_j <= 0
    for j in range(n):
        row = ["0"] * n
        row[j] = "-1"
        A.append(row)
        b.append("0")

    c = ["0"] * n
    c[-1] = "1"
    x_star = [str(M ** j) for j in range(n)]
    y_star = [str(M ** (n - 1 - j)) for j in range(n)] + ["0"] * n
    return {
        "schema": "LP-TRICHOTOMY-CERT-1.0",
        "mode": "lp_strict_complementary_opt",
        "name": f"staircase_n{n}_M{M}",
        "A": A,
        "b": b,
        "c": c,
        "x_star": x_star,
        "y_star": y_star,
        "claimed_optimum": str(M ** (n - 1)),
        "claimed_imbalance_ratio": str(M ** (n - 1)),
    }
