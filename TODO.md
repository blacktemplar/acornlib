# TODO: Binomial Theorem

## Current Task
Complete the binomial theorem proof (src/nat/nat_combo.ac:261-273)

**Status:**
- Proof is commented out but structure is documented
- Base case logic verified successfully (when uncommented)
- All helper theorems are in place:
  * `partial_add` - combines two partial sums (src/list.ac:1252)
  * `partial_scalar_mul` - distributes scalar multiplication (src/list.ac:1484-1511)
  * `partial_shift_suc` - shifts indices by 1 (src/list.ac:1513-1586)
  * `partial_split_last` - splits off last term (src/list.ac:1588-1600)
  * Pascal's identity (src/nat/nat_combo.ac:202-252)

**What remains for inductive step:**
After using `partial_scalar_mul`, we get two sums that need to be combined:
1. First sum has terms `(m choose k) * a^(k+1) * b^(m-k)` for k=0..m
2. Second sum has terms `(m choose k) * a^k * b^(m+1-k)` for k=0..m
3. Need to reindex first sum using `partial_shift_suc` to align indices
4. Apply Pascal's identity pointwise: `(m choose k-1) + (m choose k) = (m+1 choose k)`
5. Handle boundary terms (k=0 and k=m+1) using `choose_zero`, `choose_n`, `choose_out_of_bounds`

**Additional helper lemmas - COMPLETED:**
1. [x] `partial_pointwise_eq` - Function extensionality for partial sums - **DONE** (src/list.ac:1602-1658)
   - If `f(k) = g(k)` for all `k < n`, then `partial(f, n) = partial(g, n)`
   - This lets us prove sums equal by proving their terms equal pointwise

2. [x] `partial_drop_first` - Extract the first term from a partial sum - **DONE** (src/list.ac:1660-1675)
   - `n > 0 implies partial(f, n) = f(0) + partial(compose(f, Nat.suc), n - 1)`
   - Rearrangement of `partial_shift_suc` that's more convenient for some proofs

3. [x] `partial_split_first_last` - Split into first, middle, and last terms - **DONE** (src/list.ac:1677-1721)
   - `n >= 2 implies partial(f, n) = f(0) + partial(compose(f, Nat.suc), n - 2) + f(n - 1)`
   - Useful for isolating boundary terms

4. [x] `binomial_term_recurrence` - Recursive relation for binomial terms - **DONE** (src/nat/nat_combo.ac:295-346)
   - `0 < k and k <= m implies binomial_term(a, b, m.suc, k) = a * binomial_term(a, b, m, k - 1) + b * binomial_term(a, b, m, k)`
   - This expresses how each binomial term for m+1 decomposes into scaled terms from level m
   - Key relation needed for the middle terms in the inductive step

5. [x] `binomial_term_zero` - Boundary case at k=0 - **DONE** (src/nat/nat_combo.ac:261-276)
   - `binomial_term(a, b, m.suc, 0) = b * binomial_term(a, b, m, 0)`
   - Handles the k=0 boundary term in the binomial expansion

6. [x] `binomial_term_top` - Boundary case at k=m+1 - **DONE** (src/nat/nat_combo.ac:278-293)
   - `binomial_term(a, b, m.suc, m.suc) = a * binomial_term(a, b, m, m)`
   - Handles the k=m+1 boundary term in the binomial expansion

**Next step:** Complete the binomial theorem proof (src/nat/nat_combo.ac:348-385, currently commented out).

The proof structure is clear:
- Base case (n=0) is straightforward and verifies
- Inductive step needs to show: `(a+b) * partial(binomial_term(a,b,m), m.suc) = partial(binomial_term(a,b,m.suc), m.suc.suc)`
- This requires:
  1. Distributing `(a+b)` over the sum using `partial_scalar_mul` and `partial_add`
  2. Reindexing one sum using `partial_shift_suc` to align the terms
  3. Applying the three recurrence lemmas (zero, recurrence, top) to combine terms
  4. Likely needs additional helper lemmas for sum manipulation

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
