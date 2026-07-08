# My Python Toolbox — the ten pieces

Almost every problem I've solved uses only these. When stuck on "how do I
write this?", find the row that matches what I want to do.

| I want to... | Python | Example |
| --- | --- | --- |
| remember one thing | `name = value` | `max_end = 0` |
| remember many things in order | list | `prefix = [0]` |
| add to the end of a list | `.append(x)` | `prefix.append(5)` |
| read item at a position | `arr[i]` | `prefix[3]` |
| read the LAST item | `arr[-1]` | `prefix[-1]` |
| remember lookups (logbook) | dict | `logbook = {}` |
| write into the logbook | `d[key] = value` | `logbook[num] = i` |
| ask "is it in the logbook?" | `key in d` | `if complement in logbook:` |
| visit items one by one | `for ch in s:` | walks characters/values |
| visit with position AND value | `for i, v in enumerate(s):` | Two Sum walk |
| decide | `if cond:` / `else:` | `if ch != '0':` |
| convert text -> number | `int(text)` | `int("40")` is 40 — READS, never sums |
| convert number -> text | `str(n)` | `str(1234)` is `"1234"` |
| how long is it | `len(s)` | `len("abc")` is 3 |
| take a piece of a string/list | `s[l:r+1]` | positions l..r |
| package steps for reuse | `def name(args): ... return x` | |
| see what happened (debugging) | `print(x)` | |
| power with modulo, fast | `pow(a, k, MOD)` | `pow(10, k, 10**9+7)` |
| remainder | `a % m` | always non-negative in Python |

## How to find a function I don't know

Don't browse catalogs. Ask the question in this shape:

**"python — I have X, I want Y"**

e.g. "python — I have a list, I want the largest item" → `max(arr)`.
Nobody memorizes the library; everyone asks that question shape. Then test
the answer on a tiny example before trusting it (`int("40")` → ?).

## The translation rule (plan -> code)

- Every **noun** my plan must remember → a **variable**
- Every **"for each..."** → a **loop**
- Every **decision** → an **if**
- A step I'll reuse → a **def**

Before any loop, ask: **what containers do I need on my desk, and what is
each one's single job?** One variable, one job, one sentence.

## Indentation is logic (cost me two bugs)

Every `:` opens a block; everything the block owns steps right one level.
- Line at loop level → runs EVERY pass.
- Line at function level (after the loop) → runs ONCE, after.
- Line after a `return` in the same block → runs NEVER (dead code).

## Tracing rules (cost me three bugs)

- When tracing, I am the computer. Execute the TEXT, not my intent.
- Pretend a colleague wrote it and I'm hunting THEIR bug.
- Sanity-check answers against bounds (a range sum can't exceed the total).
- A wrong program can pass a weak test — test each moving part.
