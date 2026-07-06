# Remove Covered Intervals (LeetCode 1288)

## What the Problem Is Asking

You get a list of ranges like `[start, end)`. Some ranges sit entirely inside
another range — those are redundant. Count how many ranges survive after
removing every range that is fully swallowed by another one.

An interval `[a, b)` is covered by `[c, d)` only when **both** conditions hold
against the **same** other interval: `c <= a` AND `b <= d`.

Business analogy: overlapping service contracts. If contract B's coverage
period sits entirely within contract A's, contract B adds nothing — cancel it.

## My Initial Thinking

I drew the intervals on a horizontal line and compared each one against every
other one by eye. That works — it is an O(n²) all-pairs check, and with
n <= 1000 it would even pass.

Two things went wrong early:

- I accidentally "covered" an interval with itself (checked `1 <= 1 and
  4 <= 6` without asking *which* interval was doing the covering). Coverage
  must come from a *different* interval, and both conditions must hold against
  that same interval.
- I assumed overlap means coverage. It does not. `[5,10]` overlaps `[2,9]`
  heavily, but it pokes out past 9, so nothing covers it. Poking out on
  either side saves an interval.

## The Key Insight

Sort by start, then walk left to right. Sorting pre-pays half the coverage
check: everyone behind me is guaranteed to start at or before me. The only
question left is "does anyone behind me end at or after me?" — and answering
that needs just **one number**: the farthest end seen so far. The champion's
reach answers for everyone.

The bigger personal insight: it's not about how you code, it's about how you
approach the problem. My instinct was pairwise comparison; sorting transformed
the problem so a single pass with two variables replaced it.

## Pattern Used

**Sort-then-sweep.** Clues: the problem compares intervals against each other
(covered / overlap / merge). Interval problems almost always get simpler after
sorting by start — sorting turns "check against everything" into "check
against a running record".

## Approach

1. Sort by start ascending. On equal starts, put the **longer interval
   first** (end descending) — the long one must walk first so its same-start
   siblings see it in the record. Without this, `[[1,4],[1,6]]` gives the
   wrong answer.
2. Walk the sorted list carrying one number, `max_end` (start it at 0).
3. For each interval, ask: does the newcomer's end beat the record?
   - Yes → it survives. Count it, update `max_end`.
   - No → it is covered. **Do nothing.** Skip means skip.
4. Return the count.

## Pseudocode

```
sort intervals by (start ascending, end descending)

count = 0
max_end = 0

for each [start, end] in intervals:
    if end > max_end:        # newcomer beats the record -> not covered
        count += 1
        max_end = end
    # else: covered, leaves no trace

return count
```

## Implementation

- [solution.py](solution.py) — includes the test cases from this session,
  including the two traps (same-start tie, overlap-vs-coverage).

## Dry Run

`[[1,4],[1,6],[3,5]]` — sorted (start asc, end desc): `[1,6], [1,4], [3,5]`

| Interval | Comparison    | Result   | count | max_end |
| -------- | ------------- | -------- | ----- | ------- |
| [1,6]    | 6 > 0 → yes   | survives | 1     | 6       |
| [1,4]    | 4 > 6 → no    | covered  | 1     | 6       |
| [3,5]    | 5 > 6 → no    | covered  | 1     | 6       |

Answer: 1. (Without the descending tie-break, [1,4] would have walked first
and wrongly survived.)

## Complexity

- Time: O(n log n) — the sort dominates; the sweep itself is one comparison
  per interval.
- Space: O(1) extra — the entire "memory" of the walk is two numbers.

My original all-pairs idea is O(n²): correct, and fine for n = 1000
(~a million checks), but it is what breaks first as input grows. Big O
describes how work *grows*, not whether it is fast today.

## What I Learned

- Sorting is a problem-transformation tool, not just an ordering step. It
  pre-answers the start condition so only the end condition needs checking.
- A Python sort key like `key=lambda x: (x[0], -x[1])` expresses "ascending
  by first value, descending by second" — negating a value flips its order.
- "Do nothing" is a legitimate branch of an algorithm. A covered interval
  leaves no trace: count unchanged, record unchanged.
- Approach beats syntax. The hard part was never the code; it was converting
  the visual intuition into precise steps.

## Common Mistakes (I made most of these)

1. **Covering an interval with itself** — coverage requires a *different*
   interval, and both conditions against the *same* one.
2. **Overlap ≠ coverage** — an interval that pokes out on either side
   survives, no matter how much it overlaps.
3. **Touching state on the skip branch** — I decremented `count` and
   overwrote `max_end` when an interval was covered. Covered intervals must
   leave everything unchanged. Count never decreases.
4. **Flipping the comparison** — I wrote `max_end > end` when I meant
   `end > max_end`. Anchor: high-jump competition — "did the *newcomer* beat
   the *record*?" Newcomer on the left, record on the right. A flipped
   comparison silently inverts every decision and is invisible unless you
   trace.
5. **Eyeballing instead of tracing** — twice I announced an answer from
   looking at the intervals and got it wrong. The dry-run discipline exists
   to catch what the eye skips: obey the algorithm's steps, don't overrule
   them.
6. **Forgetting the same-start tie-break** — plain sort-by-start breaks the
   walk's promise ("anyone who could cover me has already walked past") when
   starts are equal.

## Architect Lens

This is redundancy elimination via sort-then-sweep, and it appears all over
real systems:

- **Firewall / CIDR rule pruning** — "allow 10.0.0.0/8" makes
  "allow 10.1.0.0/16" dead weight; network tooling prunes covered rules with
  literally this algorithm.
- **Permission audits** — a broad grant (e.g., a wide Salesforce permission
  set) makes narrower grants redundant; finding them is coverage detection.
- **Contract / entitlement dedup** — is a new license period subsumed by an
  existing one?
- **The database-index lesson** — my O(n²) instinct was "compare everything
  against everything." Sorting paid an upfront O(n log n) cost so every later
  question became a single comparison. That is exactly what a database index
  does: pay an ordering cost once so lookups stop being full scans. Repeated
  pairwise searching in a design is usually a sign the system wants an
  ordering or an index.

## Questions I Can Now Answer

1. Why does sorting by start remove the need to check the start condition
   during the walk?
2. Two intervals share a start. Which must come first in the sort, and what
   goes wrong otherwise?
3. `[5,10]` overlaps `[2,9]` — why does it survive?
4. An interval is covered. What happens to `count` and `max_end`?
5. Why is `end > max_end` correct and `max_end > end` a silent
   logic-inversion bug?
