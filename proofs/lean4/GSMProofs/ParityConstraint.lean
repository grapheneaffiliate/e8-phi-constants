theorem parity_constraint (a1 a2 a3 a4 n : Nat)
    (hsum : a1 + a2 + a3 + a4 = n) (hodd : n % 2 = 1) :
    (a1 + 11 * a2 + 19 * a3 + 29 * a4) % 30 ≠ 0 := by
  omega

theorem no_invariants_11 (a1 a2 a3 a4 : Nat) (h : a1 + a2 + a3 + a4 = 11) :
    (a1 + 11 * a2 + 19 * a3 + 29 * a4) % 30 ≠ 0 :=
  parity_constraint a1 a2 a3 a4 11 h (by omega)

theorem no_invariants_19 (a1 a2 a3 a4 : Nat) (h : a1 + a2 + a3 + a4 = 19) :
    (a1 + 11 * a2 + 19 * a3 + 29 * a4) % 30 ≠ 0 :=
  parity_constraint a1 a2 a3 a4 19 h (by omega)

theorem no_invariants_29 (a1 a2 a3 a4 : Nat) (h : a1 + a2 + a3 + a4 = 29) :
    (a1 + 11 * a2 + 19 * a3 + 29 * a4) % 30 ≠ 0 :=
  parity_constraint a1 a2 a3 a4 29 h (by omega)
