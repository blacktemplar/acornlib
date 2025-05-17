This code is tricky, because it uses Acorn, a theorem proving language that you don't know.

Before writing a proof, look at at least one Acorn file to understand the syntax. For proofs by induction, look at nat.ac. For proofs involving limits, look at real_ring.ac.

You can run

```
acorn
```

to run the verifier. This should be run after every change, to make sure the proof is verifiable.

## Tips

Before proving a theorem, consider whether there is a lemma that could be factored out into a separate theorem. If there is, ask the user whether they would prefer you to prove the lemma first.

Before proving a theorem, check if the theorem statement is actually true. If the user asks you to prove a false theorem, explain why you can't.

Numeric literals must have a type specified. You can write `Nat.0` to indicate zero, the natural number. `Real.0` indicates zero, the real number. A `numerals Nat` statement will set the default, but don't add that if it isn't already there.

Variable names must be lowercase.

## Fixing Proofs

When a statement could not be verified, there are two possibilities.

Possibility 1 is that the statement is false. Rewrite the proof so that it does not use false statements.

Possibility 2 is that the statement is too big of a logical leap from the previous statement. Fix this by filling in the missing steps of reasoning, rather than rewriting the entire proof.
