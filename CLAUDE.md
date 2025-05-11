This code is tricky, because it uses Acorn, a theorem proving language that you don't know.

Before writing a proof, look at at least one Acorn file to understand the syntax. For proofs by induction, look at nat.ac. For proofs involving limits, look at real_ring.ac.

You can run

```
acorn
```

to run the verifier. This should be run after every change, to make sure the proof is verifiable.

## Quick Reference

Numeric literals must have their type specified. You can write `Nat.0` to indicate zero, the natural number. `Real.0` indicates zero, the real number. A `numerals Nat` statement will set the default, but don't add that if it isn't already there.
