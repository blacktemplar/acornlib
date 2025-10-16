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
- [x] Prove Pascal's identity: `(n+1 choose k) = (n choose k-1) + (n choose k)` - **DONE** (src/nat/nat_combo.ac:196)

## Helper Theorems Needed

### 1. Binomial coefficient edge cases (src/nat/nat_combo.ac)
- [x] `choose_out_of_bounds`: `n.choose(k) = 0` when `k > n` - **DONE** (nat_combo.ac:196)
  - Makes summation cleaner at boundaries
  - Verified automatically from definition

### 2. Summation properties (src/list.ac or new file)
Check if these already exist, otherwise prove:
- [ ] `partial_add`: Distributivity over addition
  - `partial(f, n) + partial(g, n) = partial(function(k) { f(k) + g(k) }, n)`
- [ ] `partial_mul_const_left`: Factoring out constants
  - `c * partial(f, n) = partial(function(k) { c * f(k) }, n)`
- [ ] `partial_sum_split` or summation reindexing
  - Useful for shifting indices when distributing `(a+b) * sum(...)`

### 3. Exponentiation properties (src/nat/nat_base.ac)
May already exist, verify:
- [x] `exp_add`: `a^(b+c) = a^b * a^c` - **EXISTS** (nat_base.ac:1373)
- [ ] `exp_zero_any`: `0^n = 0` for `n > 0` - may need slight variant
- [ ] Any distributive properties needed

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
