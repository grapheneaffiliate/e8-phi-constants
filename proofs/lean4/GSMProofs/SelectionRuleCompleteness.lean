def allowed : List Nat := [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 24, 26, 27, 28, 33, 34]
def forbidden : List Nat := [11, 19, 21, 22, 23, 25, 29, 30, 31, 32]

theorem allowed_length : allowed.length = 24 := by native_decide
theorem forbidden_length : forbidden.length = 10 := by native_decide

-- No overlap
theorem no_overlap : ∀ n, n ∈ allowed → n ∉ forbidden := by native_decide

-- Partition count: 24 + 10 = 34 = size of {1..34}
theorem partition_count : allowed.length + forbidden.length = 34 := by native_decide

-- Union covers {1..34} - proved element by element
theorem cover_1 : 1 ∈ allowed := by native_decide
theorem cover_2 : 2 ∈ allowed := by native_decide
theorem cover_3 : 3 ∈ allowed := by native_decide
theorem cover_4 : 4 ∈ allowed := by native_decide
theorem cover_5 : 5 ∈ allowed := by native_decide
theorem cover_6 : 6 ∈ allowed := by native_decide
theorem cover_7 : 7 ∈ allowed := by native_decide
theorem cover_8 : 8 ∈ allowed := by native_decide
theorem cover_9 : 9 ∈ allowed := by native_decide
theorem cover_10 : 10 ∈ allowed := by native_decide
theorem cover_11 : 11 ∈ forbidden := by native_decide
theorem cover_12 : 12 ∈ allowed := by native_decide
theorem cover_13 : 13 ∈ allowed := by native_decide
theorem cover_14 : 14 ∈ allowed := by native_decide
theorem cover_15 : 15 ∈ allowed := by native_decide
theorem cover_16 : 16 ∈ allowed := by native_decide
theorem cover_17 : 17 ∈ allowed := by native_decide
theorem cover_18 : 18 ∈ allowed := by native_decide
theorem cover_19 : 19 ∈ forbidden := by native_decide
theorem cover_20 : 20 ∈ allowed := by native_decide
theorem cover_21 : 21 ∈ forbidden := by native_decide
theorem cover_22 : 22 ∈ forbidden := by native_decide
theorem cover_23 : 23 ∈ forbidden := by native_decide
theorem cover_24 : 24 ∈ allowed := by native_decide
theorem cover_25 : 25 ∈ forbidden := by native_decide
theorem cover_26 : 26 ∈ allowed := by native_decide
theorem cover_27 : 27 ∈ allowed := by native_decide
theorem cover_28 : 28 ∈ allowed := by native_decide
theorem cover_29 : 29 ∈ forbidden := by native_decide
theorem cover_30 : 30 ∈ forbidden := by native_decide
theorem cover_31 : 31 ∈ forbidden := by native_decide
theorem cover_32 : 32 ∈ forbidden := by native_decide
theorem cover_33 : 33 ∈ allowed := by native_decide
theorem cover_34 : 34 ∈ allowed := by native_decide

-- Structural decomposition
theorem enhanced_26 : 26 = 2 * 13 := by native_decide
theorem enhanced_34 : 34 = 2 * 17 := by native_decide
theorem enhanced_27 : 27 = 8 + 19 := by native_decide
theorem enhanced_33 : 33 = 3 * 11 := by native_decide

-- All coxeter exponents are odd
theorem coxeter_all_odd : ∀ m, m ∈ [1, 7, 11, 13, 17, 19, 23, 29] → m % 2 = 1 := by native_decide
