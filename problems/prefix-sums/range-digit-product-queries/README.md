# Range Digit-Product Queries (prefix sums + modulo)

Honesty note up front: I solved this **heavily guided**. I can execute the
technique but could not yet rebuild it from a blank page. Status:
practising, not mastery. This README is written partly for future-me to
re-derive it.

## What the Problem Is Asking

The previous problem (concatenate non-zero digits -> x, return
x * digitsum) — but now asked about up to 100,000 *slices* of one
100,000-character string, answers mod 10^9+7.

## My Initial Thinking

Reuse the old loop per query (slice, walk, compute). That is CORRECT — and
about 200x too slow. The estimate that proved it (a skill I learned here):

- worst cost of one query: 100,000 character-visits
- number of queries: 100,000
- total: 10^10 visits; Python does ~10^7/sec → ~17 minutes. Limit: seconds.

Cost-per-unit x number-of-units / speed = time. Four lines, before writing
any code.

## The Key Insight

Queries overlap — the naive way recomputes the same partial results
thousands of times. Same smell as Two Sum ("stop re-searching the past"),
but for ranges. The cure: **pay once upfront** — precompute running
balances so any range question becomes two lookups and a subtraction.

sum of l..r = prefix[r+1] - prefix[l]   (with a leading 0 sentinel)

I reinvented the sentinel myself: "what's the balance before anything
existed? 0."

## Pattern Used

**Prefix sums** — see [patterns/prefix-sum.md](../../../patterns/prefix-sum.md).
Clues: many queries over ranges of unchanging data; the naive solution
re-walks overlapping slices.

## Approach

One walk builds three parallel prefix arrays (three containers, one job
each):

1. `sum_p` — running digit sum. Zeros deposit nothing, so "sum of non-zero
   digits" needs no special handling.
2. `cnt_p` — running count of non-zero digits (the sum twin: add 1).
3. `val_p` — running value of concatenated non-zero digits, mod 10^9+7.
   Concatenation IS arithmetic: `value = value*10 + digit` (shift left,
   fill the slot). Zeros: skip, value unchanged.

Per query [l, r]:

- `sum` = sum_p[r+1] - sum_p[l]
- `k`   = cnt_p[r+1] - cnt_p[l]
- `x`   = (val_p[r+1] - val_p[l] * 10^k) mod M
- answer = x * sum mod M

**Why x needs the multiplication when sum didn't:** sums don't move when
new deposits arrive — an old 5 stays worth 5. Digits DO move: every new
non-zero digit shifts all earlier digits left, so by position r the old
prefix has been silently multiplied by 10^k. The `* 10^k` recreates that
shift so the subtraction lines up. (Concrete: prefix "12" inside "1234" is
worth 1200, not 12; 1234 - 12*100 = 34.)

**Why all-zero ranges need no special case:** zeros never touch any
container, so the two balances are equal, k = 0 makes the scale factor 1,
and everything annihilates to 0. Correctness falling out of structure, not
special cases — like Two Sum's look-before-sign.

**Why the modulo:** the true concatenated value can have 100,000 digits.
Keeping every value reduced mod 10^9+7 keeps arithmetic machine-sized, and
modular arithmetic survives +, -, x, so reducing at every step gives the
same final remainder. `pow(10, k, MOD)` computes the scale factor already
reduced. Python's `%` always returns non-negative, which silently repairs
the subtraction going "negative" — Java/Apex would need `+ MOD` manually.

## Implementation

- [solution.py](solution.py) — all three examples as tests, plus comments
  marking each idea.

## Dry Run

s = "10203004": val_p = [0, 1, 1, 12, 12, 123, 123, 123, 1234] — the
plateaus are the zeros walking by.

Query [2,7] (substring "203004", expected x = 234):
val_p[8] = 1234, val_p[2] = 1, k = cnt of {2,3,4} = 3
x = 1234 - 1 * 10^3 = 234 ✓ (with k=2 wrongly: 1134 — I made exactly that
mistake, see below)

## Complexity

- Build: O(m) — one walk, three appends per character.
- Per query: O(1) lookups + one modular pow (O(log k)).
- Measured: worst case (100k digits, 100k full-range queries) ran in
  ~0.11 s vs ~17 min estimated naive. ~10,000x.
- Space: O(m) for three arrays — memory bought speed, again.

## What I Learned

- Capacity estimation from constraints BEFORE coding (the 4-line habit).
- Prefix sums: pay once, answer ranges forever. Sentinel 0 kills the
  l = 0 special case.
- Concatenation is arithmetic (value*10 + digit) — which is what makes a
  prefix over it possible at all.
- "Correct" and "fast enough" are different properties; the naive solution
  was correct and architecturally wrong at this scale.
- My honest gap: I can run this machine but not yet design it unaided.

## Common Mistakes (mine, from the session)

1. **Summing balance values together** (8+16+18) — a balance IS a sum;
   the mechanism is always two lookups and ONE subtraction. Sanity check
   caught it: no range can sum to more than the whole string's total.
2. **Miscounting k** (said 2, was 3) and then reporting the check as
   passing without doing the arithmetic — 1234 - 100 = 1134 ≠ 234. A check
   only protects you if you execute it.
3. Assuming plain subtraction works for val_p (gives 1222 instead of 34) —
   forgetting that earlier digits were shifted by the range's arrivals.

## Architect Lens

"Answer expensive range questions instantly by paying once upfront" is a
production pattern:

- **Data-warehouse pre-aggregation / OLAP cubes** — dashboards read daily
  rollups, not raw transactions.
- **Materialized views** — the database stores a precomputed query result.
- **Bank statements** — a running balance IS a prefix sum; the bank never
  re-adds your lifetime of transactions.

The production questions that come with the pattern: what happens when the
underlying data CHANGES (full rebuild vs incremental update)? How fresh
must answers be? Is the build cost justified if queries are rare?
Precompute-vs-recompute is a recurring architecture trade.

## Questions I Can Now Answer

1. Estimate: 10^5 queries, each walking up to 10^5 chars, in Python —
   roughly how long, and how did you get there?
2. Why does `sum of l..r = prefix[r+1] - prefix[l]`, and what is the
   leading 0 for?
3. Why does val_p need `* 10^k` before subtracting when sum_p doesn't?
4. Why do all-zero ranges need no special case?
5. Why is the modulo needed at all, and why is it legal to reduce at every
   step?
