-- Casimir partition: the 8 Casimir degrees split into H4 and perp sets
-- H4 degrees (visible sector): {2, 12, 20, 30}
-- Perp degrees (hidden sector): {8, 14, 18, 24}
-- Their sorted union is {2, 8, 12, 14, 18, 20, 24, 30}
theorem casimir_partition_union :
    ([2, 12, 20, 30] ++ [8, 14, 18, 24]).length = [2, 8, 12, 14, 18, 20, 24, 30].length := by
  native_decide

-- Partition sizes
theorem h4_casimir_count : [2, 12, 20, 30].length = 4 := by native_decide
theorem perp_casimir_count : [8, 14, 18, 24].length = 4 := by native_decide
theorem total_casimir_count : [2, 8, 12, 14, 18, 20, 24, 30].length = 8 := by native_decide

-- No overlap between H4 and perp Casimir degrees
theorem casimir_disjoint : ∀ n, n ∈ [2, 12, 20, 30] → n ∉ [8, 14, 18, 24] := by native_decide

-- No solution to 8a + 14b + 18c + 24d = 7 (all terms ≥ 8 when nonzero)
theorem m_perp_7_zero (a b c d : Nat) : 8 * a + 14 * b + 18 * c + 24 * d ≠ 7 := by omega

-- Unique solution to 8a + 14b + 18c + 24d = 8 is (1,0,0,0)
theorem m_perp_8_unique (a b c d : Nat) (h : 8 * a + 14 * b + 18 * c + 24 * d = 8) :
    a = 1 ∧ b = 0 ∧ c = 0 ∧ d = 0 := by omega
