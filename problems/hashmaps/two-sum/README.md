# Two Sum (LeetCode 1)

## What the Problem Is Asking

Given a list of numbers and a target, find the **two positions** whose values
add up to the target. Exactly one such pair exists; the same position cannot
be used twice.

The answer is the *indices*, not the values — for `[2,7,11,15]`, target 9,
the answer is `[0,1]` (positions of 2 and 7), not `[2,7]`. This detail ends
up driving the whole design.

Business analogy: a $9 payment landed in the bank and a list of invoice
amounts — which two *invoice records* together explain the payment? You must
point at the records, not just name the amounts.

## My Initial Thinking

My first plan: sort descending, throw away anything bigger than the target,
then iterate and sum pairs, then look up indices by value. Every part of it
failed:

- **The filter breaks on negatives.** `[10, -4, 2]`, target 6: my filter
  discards 10, but the answer is 10 + (-4). Values can be negative — always
  re-read constraints before "optimizing".
- **Sorting destroys the answer.** Sorting helped in my previous problem
  (Remove Covered Intervals) because the answer there didn't depend on
  original positions. Here the answer IS the original positions. Same tool,
  opposite fit — the problem decides whether sorting is allowed.
- **Index-lookup-by-value breaks on duplicates.** `[3,3]`, target 6: looking
  up "the index of 3" returns 0 both times → `[0,0]`, using one element
  twice.

## The Key Insight

Standing on any number `x`, I already know its partner's exact value:
`target - x` (the **complement**). No searching required to know *what* I
need — only *where* it is.

So the problem reframes to: "for each number, has its complement already
walked past, and at what index?" Answering that instantly needs a lookup
table built as I walk: a **hash map** (Python `dict`), value → index. One
glance, O(1), regardless of size.

The receptionist analogy: visitors arrive one at a time; keep a logbook.
Each visitor does exactly two things, in this order: **look** for who they
need, then **sign themselves in**.

## Pattern Used

**Hash map for instant lookup.** The clue: a search *inside* a loop.
Whenever the inner operation is "does X exist in my data?", repeated
scanning is O(n²) — and a hash map collapses each scan to O(1). The
reframing step (subtraction gives the exact key to look up) is what makes
the hash map applicable.

## Approach

1. Walk the list once with an empty logbook (dict: value → index).
2. At each number, compute `complement = target - num`.
3. Look in the logbook — the book contains only *earlier* visitors.
   - Found → done: return the partner's index (from the book) and mine.
   - Not found → sign myself in (`logbook[num] = i`) and keep walking.

Why the pair is always found: every pair has a first and a second member.
When the second one arrives, the first is already in the book. Pairs are
always found by their *later* member — which is why looking only backward
is enough.

Why `[0,0]` is impossible **by construction**: I look *before* I sign in,
so my own entry is never in the book at look-time. Any match is guaranteed
to be at an earlier index. Correctness from the ordering of steps, not from
an added check.

## Pseudocode

```
logbook = {}                          # value -> index

for each index i in nums:
    complement = target - nums[i]
    if complement in logbook:
        return [logbook[complement], i]
    logbook[nums[i]] = i              # only reached when not found
```

## Implementation

- [solution.py](solution.py) — includes the negative-number and duplicate
  test cases that killed my first two approaches.

## Dry Run

`[2,7,11,15]`, target 9:

| Standing on | Need (9 - num) | In logbook?    | Action              | Logbook after |
| ----------- | -------------- | -------------- | ------------------- | ------------- |
| 2 (i=0)     | 7              | {} → no        | sign in             | {2: 0}        |
| 7 (i=1)     | 2              | {2:0} → YES, 0 | return [0, 1]. Done |               |

The duplicate case `[3,3]`, target 6: at i=1 the book holds {3: 0} — a
duplicate of my *value* is allowed in the book (different key owner), and
the match is index 0, not myself, because I haven't signed in yet.

## Complexity

- Time: O(n) — one pass; the dict lookup and insert are each O(1).
- Space: O(n) — the logbook can grow to hold every element.

Brute force is O(n²) time but O(1) space. The one-pass version **buys speed
with memory** — nothing is free; the logbook is the price. For n = 10,000:
~100 million pair-checks vs 10,000 lookups.

## What I Learned

- The complement reframing: I don't search for "a number that works" — one
  subtraction tells me the exact key to look up.
- A hash map is a logbook of the past. Look first, sign in second — the
  ordering itself is what makes self-matching impossible.
- Sorting is not a universal opener. It solved my previous problem and
  would have destroyed this one, because here the output is the original
  indices.
- `return` exits immediately; code after it in the same block is dead and
  will never run once.
- `None`/null from a Python function almost always means "no return
  statement was ever reached" — that turns "it's broken" into "which path
  skips the return?", a far easier question.
- The real lesson isn't a shortcut: it's *stop re-searching the past and
  start remembering it* — a deliberate resource trade (memory for speed).

## Common Mistakes (I made most of these)

1. **Filtering values greater than target** — breaks the moment negatives
   are allowed. Constraints first, clever ideas second.
2. **Sorting when the answer needs original positions** — the previous
   problem's winning move was this problem's losing move.
3. **Looking ahead instead of backward** — during my first trace I "found"
   the complement by scanning the array in front of me. That's the O(n²)
   scan wearing a disguise. The logbook only ever contains the past.
4. **Recording the complement instead of myself** — I signed in the number
   I was *waiting for* (with an index peeked from the future). The visitor
   who signs the book is the one who just arrived.
5. **Swapping the branches** — my pseudocode did "found → sign in,
   not found → answer". Found → answer; not found → sign in.
6. **The dead sign-in line (my actual submitted bug).** I indented
   `logbook[num] = i` inside the `if`, *after* the `return`. Doubly dead:
   wrong branch AND unreachable. The logbook stayed `{}` forever, no lookup
   ever succeeded, the loop fell off the end, and LeetCode showed null for
   every test. In Python, indentation is logic, not formatting — moving a
   line sideways changes what the program does.

## Architect Lens

**Repeated searching is a sign the system needs an index.** This problem is
that sentence in miniature:

- **Database indexes** — `WHERE email = ?` on an unindexed table is a full
  table scan (the brute-force instinct, row by row). An index is the
  logbook: value → row location. In Salesforce terms: slow SOQL on a big
  object → first question is "is the filter field indexed / an External
  ID?"
- **Caching** — Redis, Memcached, Platform Cache are logbooks:
  key → previously computed answer. `if complement in logbook` is a cache
  hit check.
- **Deduplication / identity resolution** — matching incoming records
  against millions of existing ones (duplicate rules, upsert by external
  ID) hashes the matching key and looks up; nobody compares all pairs. The
  `[3,3]` case mirrors a real identity problem: same value, different
  records, kept distinct by ID.

The trade-off is the architect's daily bread: O(n²) → O(n) bought with O(n)
memory. Indexes cost storage and slow down writes; caches go stale. The
logbook is never free — the recurring design question is "what am I
spending to make reads fast, and when does that stop being worth it?"

## Questions I Can Now Answer

1. Standing on a number, how do I know the exact value of the partner I
   need, without searching?
2. Why does looking only *backward* (at earlier elements) still find every
   pair?
3. Why can this method never use the same element twice — what provides
   that guarantee, and why is it "by construction"?
4. `[3,3]`, target 6: walk the two steps and explain why the answer is
   [0,1] and not [0,0].
5. What does a null/None result from a Python function usually indicate,
   and what question does that turn the debugging into?
6. What did the O(n) solution *pay* for its speed, and name two real
   systems that make the same trade.
