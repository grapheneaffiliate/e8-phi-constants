# GSM Formal Proofs in Lean 4

Machine-verified proofs for the Geometric Standard Model.

## Build

```bash
cd proofs/lean4
~/.elan/bin/lake build
```

## Theorems

| File | Theorem | Statement |
|------|---------|-----------|
| ParityConstraint | parity_constraint | No w-invariant scalar monomial at odd degrees |
| AnchorUniqueness | anchor_* | 137 is unique integer anchor for alpha inverse |
| MolienFactorization | m_perp_7_zero | Zero hidden-sector invariants at degree 7 |
| CHSH600Cell | chsh_squared_identity | (4-phi)^2 = 17-7*phi |
| SelectionRuleCompleteness | covers_all | 24 allowed + 10 forbidden = {1..34} |
