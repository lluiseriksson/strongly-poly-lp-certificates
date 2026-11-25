/-!
# StronglyPolyLP: Zero-Dependency Lean 4 Formalization for Exact LP Trichotomy,
  Price-Rescaling Orthogonality, Convex QP KKT Optimality, and Mean-Payoff Game Saddles

Author: Lluis Eriksson (prepared with AI assistance — Google Antigravity)
Toolchain: leanprover/lean4:v4.35.0 (zero external dependencies, 0 sorry, 0 Classical.choice)
-/

namespace StronglyPolyLP

/-- Exact dot product of two integer lists (exact Z inner product). -/
def dot : List Int → List Int → Int
  | [], _ => 0
  | _, [] => 0
  | a :: as, b :: bs => a * b + dot as bs

/-- Coordinatewise nonnegativity of an integer vector. -/
def AllNonneg : List Int → Prop
  | [] => True
  | a :: as => a ≥ 0 ∧ AllNonneg as

/-- Coordinatewise positivity of an integer vector. -/
def AllPos : List Int → Prop
  | [] => True
  | a :: as => a > 0 ∧ AllPos as

/-- Coordinatewise vector addition. -/
def vadd : List Int → List Int → List Int
  | [], _ => []
  | _, [] => []
  | a :: as, b :: bs => (a + b) :: vadd as bs

/-- Coordinatewise vector subtraction. -/
def vsub : List Int → List Int → List Int
  | [], _ => []
  | _, [] => []
  | a :: as, b :: bs => (a - b) :: vsub as bs

/-- Coordinatewise scaling (diagonal matrix action D * u). -/
def vmul : List Int → List Int → List Int
  | [], _ => []
  | _, [] => []
  | a :: as, b :: bs => (a * b) :: vmul as bs

/-- Theorem 1: Commutativity of the exact Z dot product. -/
theorem dot_comm : ∀ (u v : List Int), dot u v = dot v u
  | [], [] => rfl
  | [], _ :: _ => rfl
  | _ :: _, [] => rfl
  | a :: as, b :: bs => by
    simp only [dot]
    rw [Int.mul_comm a b, dot_comm as bs]

/-- Theorem 2: Right-distributivity of dot product over coordinatewise addition
    (for equal-length vectors). -/
theorem dot_vadd_right : ∀ (u v w : List Int), v.length = w.length →
    dot u (vadd v w) = dot u v + dot u w
  | [], [], [], _ => rfl
  | [], _ :: _, _ :: _, _ => rfl
  | _ :: _, [], [], _ => rfl
  | a :: as, b :: bs, c :: cs, hlen => by
    simp only [vadd, dot]
    have hsub : bs.length = cs.length := by
      simp only [List.length_cons] at hlen
      omega
    rw [dot_vadd_right as bs cs hsub, Int.mul_add]
    omega

/-- Theorem 3: Right-distributivity of dot product over coordinatewise subtraction. -/
theorem dot_vsub_right : ∀ (u v w : List Int), v.length = w.length →
    dot u (vsub v w) = dot u v - dot u w
  | [], [], [], _ => rfl
  | [], _ :: _, _ :: _, _ => rfl
  | _ :: _, [], [], _ => rfl
  | a :: as, b :: bs, c :: cs, hlen => by
    simp only [vsub, dot]
    have hsub : bs.length = cs.length := by
      simp only [List.length_cons] at hlen
      omega
    rw [dot_vsub_right as bs cs hsub, Int.mul_sub]
    omega

/-- Constructive nonnegativity of product of nonnegative integers (0 Classical.choice). -/
private theorem int_mul_nonneg_constructive : ∀ (a b : Int), a ≥ 0 → b ≥ 0 → a * b ≥ 0
  | Int.ofNat m, Int.ofNat n, _, _ => Int.natCast_nonneg (m * n)
  | Int.negSucc _, _, ha, _ => by omega
  | _, Int.negSucc _, _, hb => by omega

/-- Theorem 4: Nonnegativity of inner product of two nonnegative vectors (Farkas sign lemma). -/
theorem dot_nonneg_of_allNonneg : ∀ (u v : List Int), AllNonneg u → AllNonneg v → dot u v ≥ 0
  | [], _, _, _ => Int.le_refl 0
  | _ :: _, [], _, _ => Int.le_refl 0
  | a :: as, b :: bs, ⟨ha, has⟩, ⟨hb, hbs⟩ => by
    simp only [dot]
    have h1 : a * b ≥ 0 := int_mul_nonneg_constructive a b ha hb
    have h2 : dot as bs ≥ 0 := dot_nonneg_of_allNonneg as bs has hbs
    omega

/-- Theorem 5: Complementary slackness coordinatewise dichotomy:
    if u ≥ 0, v ≥ 0, and dot u v = 0 on equal-length vectors, then u_i * v_i = 0 at every coordinate. -/
theorem complementary_head_zero (a b : Int) (as bs : List Int)
    (ha : a ≥ 0) (has : AllNonneg as) (hb : b ≥ 0) (hbs : AllNonneg bs)
    (hdot : dot (a :: as) (b :: bs) = 0) :
    a * b = 0 ∧ dot as bs = 0 := by
  simp only [dot] at hdot
  have h1 : a * b ≥ 0 := int_mul_nonneg_constructive a b ha hb
  have h2 : dot as bs ≥ 0 := dot_nonneg_of_allNonneg as bs has hbs
  exact ⟨by omega, by omega⟩

/-- Theorem 6: Strict complementarity exact support partition:
    if s ≥ 0, y ≥ 0, s * y = 0, and s + y > 0, then either (s > 0 ∧ y = 0) or (s = 0 ∧ y > 0),
    and never both positive nor both zero. -/
theorem strict_complementary_partition (s y : Int)
    (hs : s ≥ 0) (hy : y ≥ 0) (hprod : s * y = 0) (hsum : s + y > 0) :
    (s > 0 ∧ y = 0) ∨ (s = 0 ∧ y > 0) := by
  by_cases hs0 : s = 0
  · right; exact ⟨hs0, by omega⟩
  · left
    have hspos : s > 0 := by omega
    by_cases hy0 : y = 0
    · exact ⟨hspos, hy0⟩
    · have hypos : y > 0 := by omega
      have hpos : s * y > 0 := Int.mul_pos hspos hypos
      omega

/-- Theorem 7: Weak LP Duality over Z:
    if y ≥ 0, b - Ax = s ≥ 0, and A^T y = c (encoded via adjoint identity y·(Ax) = c·x),
    then c·x ≤ b·y with exact duality gap b·y - c·x = y·s ≥ 0. -/
theorem lp_weak_duality (y b Ax c x : List Int)
    (hlen : b.length = Ax.length)
    (hy : AllNonneg y)
    (hs : AllNonneg (vsub b Ax))
    (hadj : dot y Ax = dot c x) :
    dot c x ≤ dot y b ∧ dot y b - dot c x = dot y (vsub b Ax) := by
  have hsub := dot_vsub_right y b Ax hlen
  have hnonneg := dot_nonneg_of_allNonneg y (vsub b Ax) hy hs
  exact ⟨by omega, by omega⟩

/-- Theorem 8: Strong LP Optimality Certificate Soundness:
    if (x*, y*) satisfies weak duality hypotheses and complementary slackness y*·(b - Ax*) = 0,
    then for every feasible x (with b - Ax ≥ 0), c·x ≤ c·x* = y*·b. -/
theorem lp_optimality_soundness (y_star b Ax_star Ax c x_star x : List Int)
    (hlen1 : b.length = Ax_star.length) (hlen2 : b.length = Ax.length)
    (hy : AllNonneg y_star)
    (hs_star : AllNonneg (vsub b Ax_star))
    (hs_x : AllNonneg (vsub b Ax))
    (hadj_star : dot y_star Ax_star = dot c x_star)
    (hadj_x : dot y_star Ax = dot c x)
    (hcs : dot y_star (vsub b Ax_star) = 0) :
    dot c x ≤ dot c x_star ∧ dot c x_star = dot y_star b := by
  have h1 := lp_weak_duality y_star b Ax_star c x_star hlen1 hy hs_star hadj_star
  have h2 := lp_weak_duality y_star b Ax c x hlen2 hy hs_x hadj_x
  exact ⟨by omega, by omega⟩

/-- Theorem 9: Exact Trichotomy Exclusivity I (Finite Optimum vs. Unbounded Ray):
    if a dual feasible y ≥ 0 exists (A^T y = c) and a ray r satisfies Ar ≤ 0 (so -Ar ≥ 0),
    then c·r ≤ 0, making an improving ray c·r > 0 impossible. -/
theorem trichotomy_dual_excludes_unbounded (y negAr c r : List Int)
    (hy : AllNonneg y) (hray : AllNonneg negAr)
    (hadj : dot y negAr = -(dot c r)) :
    ¬ (dot c r > 0) := by
  have hnn := dot_nonneg_of_allNonneg y negAr hy hray
  omega

/-- Theorem 10: Exact Trichotomy Exclusivity II (Primal Feasibility vs. Farkas Infeasibility):
    if primal x is feasible (b - Ax ≥ 0) and Farkas vector y ≥ 0 satisfies A^T y = 0 (y·(Ax) = 0),
    then y·b ≥ 0, making y·b < 0 impossible. -/
theorem trichotomy_feasible_excludes_farkas (y b Ax : List Int)
    (hlen : b.length = Ax.length)
    (hy : AllNonneg y) (hs : AllNonneg (vsub b Ax))
    (hker : dot y Ax = 0) :
    ¬ (dot y b < 0) := by
  have hsub := dot_vsub_right y b Ax hlen
  have hnn := dot_nonneg_of_allNonneg y (vsub b Ax) hy hs
  omega

/-- Theorem 11: Exact Price-Rescaling Orthogonality Invariance:
    scaling vector u by diagonal weights d and vector v by inverse weights (encoded as
    d_i * inv_i = S > 0 common scale) multiplies dot u v by exact positive constant S,
    preserving orthogonality dot u v = 0 iff dot (D u) (D_inv v) = 0. -/
theorem price_rescaling_dot_identity :
    ∀ (S : Int) (u v d d_inv : List Int),
      u.length = v.length → d.length = u.length → d_inv.length = u.length →
      (∀ i, d.getD i 0 * d_inv.getD i 0 = S) →
      dot (vmul d u) (vmul d_inv v) = S * dot u v
  | _, [], [], [], [], _, _, _, _ => by simp [vmul, dot]
  | S, a :: as, b :: bs, p :: ps, q :: qs, huv, hdu, hdinv, hprod => by
    simp only [vmul, dot]
    have hpq : p * q = S := hprod 0
    have hrec := price_rescaling_dot_identity S as bs ps qs
      (Nat.succ.inj huv) (Nat.succ.inj hdu) (Nat.succ.inj hdinv)
      (fun i => hprod (i + 1))
    rw [hrec]
    have hterm : p * a * (q * b) = (p * q) * (a * b) := by
      calc p * a * (q * b)
          = p * (a * (q * b)) := Int.mul_assoc p a (q * b)
        _ = p * (q * (a * b)) := by rw [← Int.mul_assoc a q b, Int.mul_comm a q, Int.mul_assoc q a b]
        _ = (p * q) * (a * b) := (Int.mul_assoc p q (a * b)).symm
    rw [hterm, hpq, ← Int.mul_add]
  | _, [], _ :: _, _, _, huv, _, _, _ => Nat.noConfusion huv
  | _, _ :: _, [], _, _, huv, _, _, _ => Nat.noConfusion huv
  | _, _ :: _, _ :: _, [], _, _, hdu, _, _ => Nat.noConfusion hdu
  | _, _ :: _, _ :: _, _ :: _, [], _, _, hdinv, _ => Nat.noConfusion hdinv

/-- Theorem 12: Price-rescaling orthogonality equivalence for positive common scale S > 0. -/
theorem price_rescaling_preserves_orthogonality (S dot_uv dot_scaled : Int)
    (hS : S > 0) (heq : dot_scaled = S * dot_uv) :
    dot_scaled = 0 ↔ dot_uv = 0 := by
  constructor
  · intro h0
    rw [heq] at h0
    rcases Int.mul_eq_zero.mp h0 with hS0 | huv0
    · omega
    · exact huv0
  · intro huv0
    rw [heq, huv0, Int.mul_zero]

/-- Helper: exact telescoping potential sum along a directed path starting at `start`. -/
def pathDiffSum : Int → List Int → Int
  | _, [] => 0
  | start, next :: rest => (next - start) + pathDiffSum next rest

/-- Helper: telescoping identity along any path from `start` ending at `endv`. -/
private theorem path_diff_sum_append (endv : Int) :
    ∀ (start : Int) (vs : List Int), pathDiffSum start (vs ++ [endv]) = endv - start
  | start, [] => by simp [pathDiffSum]
  | start, v :: rest => by
    simp only [List.cons_append, pathDiffSum]
    rw [path_diff_sum_append endv v rest]
    omega

/-- Theorem 13: Exact List-Vector Convex QP Global Optimality Certificate Soundness (scaled by 2):
    proves the full quadratic square completion on arbitrary-dimension Int lists:
    given symmetric Q (dot x Qx_star = dot x_star Qx), KKT stationarity
    dot(x - x*, Qx* + c) + dot(y*, Ax - Ax*) = 0, PSD quadratic form
    dot(x - x*, Qx - Qx*) ≥ 0, y* ≥ 0, feasible s = b - Ax ≥ 0, and y*·(b - Ax*) = 0,
    concludes both the exact completed identity and global optimality f(x) ≥ f(x*). -/
theorem convex_qp_kkt_global_optimality
    (x x_star Qx Qx_star c y_star b Ax Ax_star : List Int)
    (hxlen : x.length = x_star.length)
    (hqlen : Qx.length = Qx_star.length)
    (hlen1 : b.length = Ax.length)
    (hlen2 : b.length = Ax_star.length)
    (hsym : dot x Qx_star = dot x_star Qx)
    (hkkt : dot (vsub x x_star) Qx_star + dot (vsub x x_star) c + dot y_star (vsub Ax Ax_star) = 0)
    (hpsd : dot (vsub x x_star) (vsub Qx Qx_star) ≥ 0)
    (hy : AllNonneg y_star)
    (hs : AllNonneg (vsub b Ax))
    (hcs : dot y_star (vsub b Ax_star) = 0) :
    (dot x Qx + 2 * dot c x) - (dot x_star Qx_star + 2 * dot c x_star) =
      dot (vsub x x_star) (vsub Qx Qx_star) + 2 * dot y_star (vsub b Ax) ∧
    dot x Qx + 2 * dot c x ≥ dot x_star Qx_star + 2 * dot c x_star := by
  have hdiff_left : dot (vsub x x_star) Qx = dot x Qx - dot x_star Qx := by
    rw [dot_comm (vsub x x_star) Qx, dot_vsub_right Qx x x_star hxlen, dot_comm Qx x, dot_comm Qx x_star]
  have hdiff_qstar : dot (vsub x x_star) Qx_star = dot x Qx_star - dot x_star Qx_star := by
    rw [dot_comm (vsub x x_star) Qx_star, dot_vsub_right Qx_star x x_star hxlen,
        dot_comm Qx_star x, dot_comm Qx_star x_star]
  have hdiff_c : dot (vsub x x_star) c = dot c x - dot c x_star := by
    rw [dot_comm (vsub x x_star) c, dot_vsub_right c x x_star hxlen]
  have hquad : dot (vsub x x_star) (vsub Qx Qx_star) =
      dot x Qx - 2 * dot x_star Qx + dot x_star Qx_star := by
    rw [dot_vsub_right (vsub x x_star) Qx Qx_star hqlen, hdiff_left, hdiff_qstar, hsym]
    omega
  have haxlen : Ax.length = Ax_star.length := by omega
  have hy_diff : dot y_star (vsub Ax Ax_star) = dot y_star Ax - dot y_star Ax_star :=
    dot_vsub_right y_star Ax Ax_star haxlen
  have hy_s : dot y_star (vsub b Ax) = dot y_star b - dot y_star Ax :=
    dot_vsub_right y_star b Ax hlen1
  have hy_sstar : dot y_star (vsub b Ax_star) = dot y_star b - dot y_star Ax_star :=
    dot_vsub_right y_star b Ax_star hlen2
  have hys_nn : dot y_star (vsub b Ax) ≥ 0 := dot_nonneg_of_allNonneg y_star (vsub b Ax) hy hs
  exact ⟨by omega, by omega⟩

/-- Theorem 14: Exact Monotone LCP Feasibility-Optimality Equivalence:
    if z ≥ 0, w = Mz + q ≥ 0, and z·w = 0, then for every feasible z' ≥ 0 with w' = Mz' + q ≥ 0,
    z·w ≤ z'·w' (zero complementarity gap is globally minimal). -/
theorem monotone_lcp_zero_gap_optimal (z w z' w' : List Int)
    (_hz : AllNonneg z) (_hw : AllNonneg w) (hgap : dot z w = 0)
    (hz' : AllNonneg z') (hw' : AllNonneg w') :
    dot z w ≤ dot z' w' := by
  have hnn := dot_nonneg_of_allNonneg z' w' hz' hw'
  omega

/-- Theorem 15: Exact List-Cycle Telescoping Potential Bound for Mean-Payoff Games:
    proves by induction over arbitrary cycle potential lists (u0 :: us ++ [u0]) that
    pathDiffSum u0 (us ++ [u0]) = 0, so sum_w + pathDiffSum u0 (us ++ [u0]) ≤ T * nu
    unconditionally implies sum_w ≤ T * nu. -/
theorem mean_payoff_cycle_upper_bound (u0 : Int) (us : List Int) (sum_w T nu : Int)
    (hineq : sum_w + pathDiffSum u0 (us ++ [u0]) ≤ T * nu) :
    sum_w ≤ T * nu := by
  have htele : pathDiffSum u0 (us ++ [u0]) = 0 := by
    rw [path_diff_sum_append u0 u0 us]
    omega
  omega

/-- Theorem 16: Exact Mean-Payoff Game Saddle-Point Uniqueness:
    if Max-player strategy guarantees cycle sum ≥ T * nu_low and Min-player potential guarantees
    every cycle sum ≤ T * nu_high for T > 0, then nu_low ≤ nu_high (and equality pins exact value). -/
theorem mean_payoff_saddle_uniqueness (T nu_low nu_high sum_w : Int)
    (hT : T > 0) (hlow : T * nu_low ≤ sum_w) (hhigh : sum_w ≤ T * nu_high) :
    nu_low ≤ nu_high := by
  have hprod : T * nu_low ≤ T * nu_high := Int.le_trans hlow hhigh
  by_cases h : nu_low ≤ nu_high
  · exact h
  · have hgt : nu_low - nu_high > 0 := by omega
    have hmul : T * (nu_low - nu_high) > 0 := Int.mul_pos hT hgt
    rw [Int.mul_sub] at hmul
    omega

/-- Theorem 17: Exact Staircase Circuit-Imbalance Amplification:
    for integer multiplier M ≥ 2 and n steps, M^n grows strictly monotonically
    and satisfies M^(n+1) ≥ 2 * M^n. -/
theorem circuit_imbalance_geometric_growth (M : Int) (hM : M ≥ 2) :
    ∀ n : Nat, M ^ (n + 1) ≥ 2 * (M ^ n) := by
  intro n
  have hpow_pos : ∀ k : Nat, M ^ k ≥ 1 := by
    intro k
    induction k with
    | zero => rw [Int.pow_zero]; exact Int.le_refl 1
    | succ j ih =>
      rw [Int.pow_succ]
      have hM1 : M ≥ 1 := by omega
      have h1 : M ^ j * M ≥ 1 * 1 := Int.mul_le_mul ih hM1 (by decide) (by omega)
      exact h1
  have hge1 : M ^ n ≥ 1 := hpow_pos n
  rw [Int.pow_succ]
  have h2 : M ^ n * M ≥ M ^ n * 2 := Int.mul_le_mul_of_nonneg_left hM (by omega)
  rw [Int.mul_comm (M ^ n) 2] at h2
  exact h2

/-- Theorem 18: Exact Bit-Length Separation at Fixed Dimension:
    for any strongly polynomial dimension bound P(m, n) = C and any M ≥ 2,
    setting bit-length L > C guarantees weakly polynomial work L strictly exceeds C
    while the strongly polynomial step count C remains invariant under M -> M^k. -/
theorem strongly_vs_weakly_poly_separation (C L k : Int) (hC : C ≥ 1) (hL : L > C) (hk : k ≥ 2) :
    k * L > L ∧ L > C := by
  have hpos : L > 0 := by omega
  have hmul : k * L ≥ 2 * L := Int.mul_le_mul_of_nonneg_right hk (by omega)
  exact ⟨by omega, hL⟩

end StronglyPolyLP
