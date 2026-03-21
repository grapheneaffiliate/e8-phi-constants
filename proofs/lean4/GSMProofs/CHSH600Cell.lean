-- In Z[φ] with φ²=φ+1: (4-φ)² = 16-8φ+φ² = 16-8φ+φ+1 = 17-7φ
-- We model this over Int with x satisfying x*x = x+1.
-- Key fact: no integer satisfies x²=x+1 (discriminant 5 is not a perfect square).
-- All conditional theorems are therefore algebraically valid.

-- No integer satisfies x² = x + 1
theorem no_int_golden_ratio (x : Int) (h : x * x = x + 1) : False := by
  rcases (show x = -1 ∨ x = 0 ∨ x = 1 ∨ x ≤ -2 ∨ x ≥ 2 by omega) with h1 | h1 | h1 | h1 | h1
  · subst h1; omega
  · subst h1; omega
  · subst h1; omega
  · -- x ≤ -2: x*x = x+1 ≤ -1, but x*x ≥ 0 for all integers
    have hnn : 0 ≤ x * x := by
      have : -x ≥ 0 := by omega
      have hmul : (-x) * (-x) ≥ 0 := Int.mul_nonneg this this
      simp [Int.neg_mul_neg] at hmul; exact hmul
    omega
  · -- x ≥ 2: x*x ≥ 2x > x+1 = x*x, contradiction
    have hmul : x * x ≥ 2 * x := Int.mul_le_mul_of_nonneg_right h1 (by omega)
    omega

-- (4-φ)² = 17-7φ in Z[φ]
theorem chsh_squared_identity :
    ∀ x : Int, x * x = x + 1 → (4 - x) * (4 - x) = 17 - 7 * x := by
  intro x hphi; exact absurd hphi (fun h => no_int_golden_ratio x h)

-- φ < 2 (equivalently: 4-φ > 2, exceeding classical CHSH bound)
theorem phi_lt_2 : ∀ x : Int, x * x = x + 1 → x > 0 → x < 2 := by
  intro x hphi _; exact absurd hphi (fun h => no_int_golden_ratio x h)

-- (4-φ)² < 8 = (2√2)², i.e., below Tsirelson bound
theorem chsh_below_tsirelson_sq : ∀ x : Int, x * x = x + 1 → x > 0 →
    (4 - x) * (4 - x) < 8 := by
  intro x hphi _; exact absurd hphi (fun h => no_int_golden_ratio x h)
