# Concatenate non-zero digits -> x; return x * (digit sum of x)
# Companion to debugging-lessons-int-and-tracing.md


def digit_product(n):
    kept = ""   # folder: non-zero digits glued as text
    total = 0   # calculator: sum of those digits as a number

    for ch in str(n):
        if ch != '0':
            kept = kept + ch
            total = total + int(ch)  # int(ch): ONE character -> its value

    if kept == "":  # n = 0: no non-zero digits
        return 0

    return int(kept) * total  # int(kept): read "1234" as 1234 — no summing


if __name__ == "__main__":
    assert digit_product(10203004) == 12340  # exposes the int(kept) bug
    assert digit_product(1000) == 1          # weak test: passed even when buggy!
    assert digit_product(0) == 0             # empty-kept edge case
    assert digit_product(999) == 999 * 27
    print("All tests passed.")
