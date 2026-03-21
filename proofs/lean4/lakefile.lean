import Lake
open Lake DSL

package GSMProofs where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib GSMProofs where
  roots := #[`GSMProofs]
