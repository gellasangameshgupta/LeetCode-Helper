# LeetCode 1 - Two Sum
# Pattern: hash map (one-pass lookup table)


def twoSum(nums, target):
    logbook = {}  # value -> index where I saw it (record of the PAST only)

    for i, num in enumerate(nums):
        complement = target - num  # the exact partner I need
        if complement in logbook:  # O(1) look — book holds only earlier visitors
            return [logbook[complement], i]
        logbook[num] = i  # sign MYSELF in, at loop level, AFTER the look
        # Look-before-sign is a correctness rule, not style:
        # my own entry is never in the book at look-time -> can't match myself.


if __name__ == "__main__":
    assert sorted(twoSum([2, 7, 11, 15], 9)) == [0, 1]
    assert sorted(twoSum([3, 2, 4], 6)) == [1, 2]
    assert sorted(twoSum([3, 3], 6)) == [0, 1]      # duplicate values, distinct indices
    assert sorted(twoSum([10, -4, 2], 6)) == [0, 1]  # negative numbers: no filtering!
    print("All tests passed.")
