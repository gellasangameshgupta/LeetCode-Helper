# Range queries: x = concatenated non-zero digits of s[l..r], answer = x * digitsum(x)
# Pattern: prefix sums (three parallel prefix arrays), answers mod 1e9+7

MOD = 10**9 + 7


def solve(s, queries):
    # One walk, three containers ("balances with a leading 0 sentinel"):
    sum_p = [0]  # running digit sum          -> gives `sum` per range
    cnt_p = [0]  # running non-zero count     -> gives k (the shift amount)
    val_p = [0]  # running concatenated value mod MOD (value*10+d, skip zeros)

    for ch in s:
        d = int(ch)
        sum_p.append(sum_p[-1] + d)
        cnt_p.append(cnt_p[-1] + (1 if d != 0 else 0))
        val_p.append((val_p[-1] * 10 + d) % MOD if d != 0 else val_p[-1])

    answers = []
    for l, r in queries:
        total = sum_p[r + 1] - sum_p[l]  # small (<= 9*10^5): no mod needed
        k = cnt_p[r + 1] - cnt_p[l]      # non-zero digits the range contributed
        # Old prefix got shifted left k times by the range's digits,
        # so scale it back up before subtracting (sums never needed this):
        x = (val_p[r + 1] - val_p[l] * pow(10, k, MOD)) % MOD
        answers.append((x * total) % MOD)
    return answers


if __name__ == "__main__":
    assert solve("10203004", [[0, 7], [1, 3], [4, 6]]) == [12340, 4, 9]
    assert solve("1000", [[0, 3], [1, 1]]) == [1, 0]  # all-zero range: no special case
    assert solve("9876543210", [[0, 9]]) == [444444137]  # modulo actually matters
    print("All tests passed.")
