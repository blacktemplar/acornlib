# TODO: Binomial Theorem

## Goal
Prove the binomial theorem: `(a + b)^n = sum_{k=0}^{n} (n choose k) * a^k * b^(n-k)`

In Acorn syntax (using `partial` from `list.ac`):
```acorn
theorem binomial(a: Nat, b: Nat, n: Nat) {
    (a + b).exp(n) = partial(function(k: Nat) {
        n.choose(k) * a.exp(k) * b.exp(n - k)
    }, n.suc)
}
```

Note: We use `n.suc` because `partial(f, m)` sums from 0 to m-1, so we need n+1 terms.

## Current Status
- [x] Define binomial coefficients `n.choose(k)` - **DONE** (src/nat/nat_combo.ac)
- [x] Prove Pascal's identity: `(n+1 choose k) = (n choose k-1) + (n choose k)` - **DONE** (src/nat/nat_combo.ac:202)
- [x] Define `binomial_term` helper function - **DONE** (src/nat/nat_combo.ac:255)
- [x] Define `add_fn[T, A: AddSemigroup]` for pointwise addition - **DONE** (src/add_semigroup.ac:13)
- [x] Define `mul_fn[T, S: Semigroup]` for scalar multiplication - **DONE** (src/semigroup.ac:14)
- [x] Prove `partial_one`: `partial(f, 1) = f(0)` - **DONE** (src/list.ac:1186)
- [x] Prove `map_sum_add` helper theorem - **DONE** (src/list.ac:1202)
- [x] Prove `partial_add` theorem - **DONE** (src/list.ac:1252)
- [ ] **NEXT STEP**: Add `mul_zero_left` and `mul_zero_right` axioms to Semiring typeclass
  - These cannot be derived without additive inverses
  - Requires updating all Semiring instances: Nat (already has theorems), Rat, Real, etc.
  - See discussion in src/list.ac:1267-1290
- [ ] Prove `sum_scalar_mul` theorem (requires mul_zero axioms) - **BLOCKED**
- [ ] Prove `partial_scalar_mul` for distributing scalar multiplication through partial sums - **BLOCKED**
  - Requires sum_scalar_mul
  - Also has prover limitations with map_map application
- [ ] Prove reindexing theorems for partial sums
- [ ] Complete the binomial theorem proof (currently commented out in src/nat/nat_combo.ac:274)

## Helper Theorems Needed

### 1. Binomial coefficient edge cases (src/nat/nat_combo.ac)
- [x] `choose_out_of_bounds`: `n.choose(k) = 0` when `k > n` - **DONE** (nat_combo.ac:196)
  - Makes summation cleaner at boundaries
  - Verified automatically from definition

### 2. Summation properties
- [x] `partial_add_seq_comm`: Distributivity over addition - **EXISTS** (real_series.ac:420)
  - `partial(add_seq(a, b)) = add_seq(partial(a), partial(b))`
  - Where `add_seq(a, b)(n) = a(n) + b(n)` (pointwise addition)
- [x] `partial_mul_seq_comm`: Factoring out constants - **EXISTS** (real_series.ac:460)
  - `partial(mul_seq(c, f)) = mul_seq(c, partial(f))`
  - Where `mul_seq(c, f)(n) = c * f(n)` (scalar multiplication)
- [ ] `partial_sum_split` or summation reindexing
  - Useful for shifting indices when distributing `(a+b) * sum(...)`
  - May need index shifting theorem for the inductive step

### 3. Exponentiation properties (src/nat/nat_base.ac)
- [x] `exp_zero`: `a.exp(0) = 1` - **EXISTS** (nat_base.ac:1369)
- [x] `exp_one`: `a.exp(1) = a` - **EXISTS** (nat_base.ac:1362)
- [x] `exp_add`: `a.exp(b + c) = a.exp(b) * a.exp(c)` - **EXISTS** (nat_base.ac:1373)
- [x] `zero_exp`: `n != 0 implies 0.exp(n) = 0` - **EXISTS** (nat_base.ac:1448)
- [x] `exp_mul`: `a.exp(b * c) = a.exp(b).exp(c)` - **EXISTS** (nat_base.ac:1391)

## Proof Strategy

### Base case (n = 0)
```
(a + b)^0 = 1
= 0.choose(0) * a^0 * b^0
= 1 * 1 * 1
```

### Inductive step (n → n+1)
Assume: `(a+b)^n = sum_{k=0}^{n} (n choose k) * a^k * b^(n-k)`

Prove: `(a+b)^(n+1) = sum_{k=0}^{n+1} ((n+1) choose k) * a^k * b^(n+1-k)`

**Key steps:**
1. `(a+b)^(n+1) = (a+b) * (a+b)^n`
2. Distribute: `= a * (a+b)^n + b * (a+b)^n`
3. Apply induction hypothesis to both terms
4. `= a * sum_{k=0}^{n} ... + b * sum_{k=0}^{n} ...`
5. Distribute constants into sums
6. Reindex one of the sums (shift k → k-1 or k+1)
7. Combine using Pascal's identity: `(n+1 choose k) = (n choose k-1) + (n choose k)`
8. Handle boundary cases using `choose_out_of_bounds`

## Files to Modify
- `src/nat/nat_combo.ac` - binomial coefficient theorems and final binomial theorem
- `src/list.ac` - summation helper theorems (if not already present)
- `src/nat/nat_base.ac` - exponentiation helpers (if needed)

---

# Things to Do Next

After the binomial theorem is complete, the natural progression is to work on infinite series and the exponential function:

## 1. Cauchy Products
Define and prove properties of the Cauchy product of two infinite series.

The Cauchy product of two series `∑ aₙ` and `∑ bₙ` is:
```
∑ cₙ where cₙ = ∑_{k=0}^{n} aₖ * b_{n-k}
```

**Why it matters:** This is essential for proving `e^x * e^y = e^(x+y)` and other properties of power series.

**Prerequisites:**
- Convergence theorems for infinite series (may already exist in `src/real/real_series.ac`)
- Summation manipulation theorems
- The binomial theorem provides the finite version of this product

**Key theorems to prove:**
- [ ] Cauchy product convergence: If `∑ aₙ` and `∑ bₙ` both converge absolutely, their Cauchy product converges
- [ ] Cauchy product formula: `(∑ aₙ) * (∑ bₙ) = ∑ cₙ` where `cₙ = ∑_{k=0}^{n} aₖ * b_{n-k}`

## 2. Define e^x via Partial Sums
Define the exponential function for real numbers using the power series:
```
e^x = ∑_{n=0}^{∞} x^n / n!
```

**Implementation approach:**
- Define as a limit: `exp(x) = limit(partial(function(n) { x^n / n! }, _))`
- Prove convergence for all real x
- May need to work with Real or Rat first, then generalize

**Files involved:**
- New file `src/real/real_exp.ac` or extend `src/real/real_series.ac`
- Will need factorial for Real (lift from Nat factorial)

## 3. Prove Properties of e^x
Once e^x is defined, prove its fundamental properties:

**Essential theorems:**
- [ ] `exp_zero`: `e^0 = 1`
- [ ] `exp_add`: `e^x * e^y = e^(x+y)` (uses Cauchy product!)
- [ ] `exp_pos`: `e^x > 0` for all x
- [ ] `exp_derivative`: `d/dx(e^x) = e^x` (if we develop calculus)
- [ ] Relationship to natural logarithm (if we define ln)
- [ ] Taylor series convergence properties

**Connection to binomial theorem:**
The binomial theorem gives the finite approximation:
```
(1 + x/n)^n = ∑_{k=0}^{n} (n choose k) * (x/n)^k
```
As n → ∞, this approaches e^x, providing an alternative definition and a bridge between discrete and continuous mathematics.

## Roadmap Summary
1. ✓ Binomial coefficients and Pascal's identity
2. → Binomial theorem (current focus)
3. → Cauchy products
4. → Define e^x as a power series
5. → Prove e^x * e^y = e^(x+y) using Cauchy products
6. → Further analysis of exponential function
