# Pattern: Prefix Sum

*Started 2026-07-08 after Range Digit-Product Queries. Grows as I solve
more problems with it.*

## What it is

Precompute running balances over a sequence so that any range question
becomes two lookups and one subtraction, instead of a walk.

```
digits:            5   3   8   2
prefix:        0   5   8  16  18      <- one longer; leading 0 sentinel

sum of l..r = prefix[r+1] - prefix[l]
```

Pay once: O(n) build. Then every query is O(1). Memory buys speed — same
trade as a hash map, shaped for ranges.

## How to recognize it

- MANY queries over RANGES of data that doesn't change between queries.
- The naive solution re-walks overlapping slices (recomputing the same
  partial results).
- Constraint smell: queries x range-length multiplies to 10^9+ operations.

## Questions to ask

- Is the underlying data immutable during the queries? (If it changes,
  prefix arrays need rebuilding — different tools exist for that.)
- What operation am I accumulating? Addition subtracts cleanly. Anything
  positional (concatenation) needs a scale factor (x 10^k). Counts are
  just sums of 1s.
- Range starting at 0 — is my sentinel in place?

## Basic template

```python
prefix = [0]
for item in data:
    prefix.append(prefix[-1] + value_of(item))
# range l..r:
prefix[r+1] - prefix[l]
```

## Variations met so far

- **Count prefix**: accumulate 1 per matching item (non-zero digits).
- **Positional/value prefix with modulo**: value = (value*10 + d) % MOD;
  range extraction needs val[r+1] - val[l] * pow(10, k, MOD), where k is
  the range's contribution count. Python's % repairs negative results;
  Java/Apex need + MOD.

## Common mistakes (mine)

- Adding balance values together — a balance IS a sum; the answer is
  always ONE subtraction of TWO lookups.
- Forgetting that positional data shifts: plain subtraction on the value
  prefix is wrong without the 10^k scale.
- No sanity check: a range answer can never exceed the whole-sequence
  total.

## Problems solved with it

- [Range Digit-Product Queries](../problems/prefix-sums/range-digit-product-queries/)
  — three parallel prefixes (sum, count, modular value). Guided.

## Real-world connections

Data-warehouse pre-aggregation and OLAP cubes; materialized views; running
balances on bank statements; rolling metrics. Core trade: precompute vs
recompute — build cost, storage, and staleness vs query speed.
