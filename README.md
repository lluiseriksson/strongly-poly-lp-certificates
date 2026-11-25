# Exact-Q Primal-Dual Trichotomy, Staircase Circuit-Imbalance Amplification, Convex QP KKT, and Mean-Payoff Game Saddle Certificates for Strongly Polynomial Linear Programming

**Author:** Lluis Eriksson (prepared with AI assistance — Google Antigravity)  
**License:** MIT (`LICENSE`, code); CC-BY-4.0 (manuscript)  
**Lean 4 Toolchain:** `leanprover/lean4:v4.35.0` (zero external dependencies, 18/18 theorems, 0 `sorry`, 0 `Classical.choice`, 0 warnings)  
**Certificate Schema:** `LP-TRICHOTOMY-CERT-1.0` (pure Python stdlib exact integers & `fractions.Fraction`, zero floating-point trust)

## Overview

Complementing OpenAI's November 24, 2026 deterministic strongly polynomial linear programming breakthrough (resolving Smale's 9th problem, plus strongly polynomial convex QP and deterministic mean-payoff games), this repository formalizes and machine-checks exact-$\mathbb{Z}/\mathbb{Q}$ primal-dual trichotomy exclusivity, price-rescaling orthogonality invariance, staircase circuit-imbalance amplification ($\kappa = M^{n-1}$), exact-$\mathbb{Q}$ pivoted $LDL^\top$ PSD + KKT convex QP optimality, and rational potential/strategy saddle certificates for deterministic mean-payoff games.

## Quick Verification

```bash
python scripts/verify_all.py
```
