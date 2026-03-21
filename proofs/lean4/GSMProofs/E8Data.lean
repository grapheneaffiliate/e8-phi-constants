-- E8 Lie algebra structural constants
def e8_dimension : Nat := 248
def e8_rank : Nat := 8
def e8_roots : Nat := 240
def e8_coxeter_number : Nat := 30
def e8_casimir_degrees : List Nat := [2, 8, 12, 14, 18, 20, 24, 30]
def e8_coxeter_exponents : List Nat := [1, 7, 11, 13, 17, 19, 23, 29]
def h4_coxeter_exponents : List Nat := [1, 11, 19, 29]
def e8_only_coxeter : List Nat := [7, 13, 17, 23]
def so8_dimension : Nat := 28
def e6_dimension : Nat := 78
def f4_dimension : Nat := 52
def f4_roots : Nat := 48
def h4_order : Nat := 14400
def h4_vertices : Nat := 120

-- Basic verifications
theorem e8_root_decomp : e8_roots = 5 * f4_roots := by native_decide
theorem e8_projection : e8_roots = 2 * h4_vertices := by native_decide
theorem anchor_137 : 128 + e8_rank + 1 = 137 := by native_decide
theorem dim_eq_roots_plus_rank : e8_roots + e8_rank = e8_dimension := by native_decide
