# Debugging Lessons: int(), Honest Tracing, and Weak Tests

Source problem: form `x` by concatenating the non-zero digits of `n`, let
`sum` be the digit sum of `x`, return `x * sum`. (Simple simulation — the
algorithm isn't the lesson; the debugging is.)

Working solution: [solution.py](solution.py)

## Lesson 1 — int() reads, it doesn't sum

I believed `int("123")` meant "sum the digits" → 6. It doesn't perform any
arithmetic. It reads the text as one number: `int("123")` is one hundred
twenty-three. `int("12")` is twelve, not 3.

This single misconception produced my main bug:

```python
total = total + int(kept)   # feeds the WHOLE glued string: 1, 12, 123, 1234
total = total + int(ch)     # correct: feeds one character: 1, 2, 3, 4
```

One variable name of difference; the wrong version returns 1370 where the
digit sum is 10.

Takeaway: never assume what a built-in does from its name. Check with a
tiny experiment (`int("40")` → ?) before building on it. Same applies to
any standard library function in any language.

## Lesson 2 — trace the text, not the intent

Twice I "traced" my buggy code and got the correct expected answer. My
pencil wrote `1 + int("12") = 3` — substituting what I *meant* (add the
digit 2) for what the code *says* (add twelve). The trace came out perfect
while the code was wrong: the worst combination, because the trace
certified the bug.

The rule: when tracing, I am the computer. The computer cannot see intent.
Execute the text exactly, especially at the lines I suspect are wrong —
that is the entire point of tracing.

Trick that forces honesty: pretend the code was written by a colleague and
I'm hunting for *their* bug. Suspicion keeps the pencil honest; ownership
makes it charitable.

## Lesson 3 — a wrong program can pass a weak test

My buggy version (both bugs present) returned the CORRECT answer for
n = 1000. Only one non-zero digit means several distinct mistakes collapse
into the right output. It failed loudly on n = 10203004.

Takeaway: "it passed a test" proves little if the test doesn't stress each
moving part. Good test inputs for this problem needed: multiple non-zero
digits (exposes the int(kept) bug), zeros in the middle, and n = 0 (the
empty-kept edge case). When writing tests, ask: which mistake would this
input catch?

## Bonus — the two-container question

Every loop walk carries state. Before writing any loop, ask: **what
containers do I need on my desk, and what is each one's single job?**

- Intervals problem: one container (max_end — the record).
- Two Sum: one container (the logbook — value → index).
- This problem: two containers with jobs that never mix:
  - `kept` — folder: non-zero digits glued as text → `"1234"`
  - `total` — calculator: sum of those digits as a number → `10`

My bugs were the containers bleeding into each other (feeding the folder
into the calculator; defining x from the calculator instead of the
folder). One variable, one job, one sentence — then the loop writes
itself.

## Recall questions

1. `int("205")` = ? What does int() never do?
2. Why did my perfect-looking trace certify a bug? What is the tracing
   rule?
3. Why did n = 1000 pass with two bugs present? What makes a test input
   strong?
4. What are the two containers in this problem and each one's single job?
