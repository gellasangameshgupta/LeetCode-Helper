# LeetCode 1288 - Remove Covered Intervals
# Pattern: sort-then-sweep


def removeCoveredIntervals(intervals):
    # Sort by start ascending; on equal starts, longer interval first.
    # The longer one must walk first so it can "cover" its same-start siblings.
    intervals.sort(key=lambda x: (x[0], -x[1]))

    count = 0
    max_end = 0  # farthest right edge among survivors so far (the "record")

    for start, end in intervals:
        # Sorting already guarantees every earlier interval starts <= start.
        # So the only remaining question is: does the newcomer beat the record?
        if end > max_end:
            count += 1
            max_end = end
        # else: covered — skip, touch nothing. A covered interval leaves no trace.

    return count


if __name__ == "__main__":
    assert removeCoveredIntervals([[1, 4], [3, 6], [2, 8]]) == 2
    assert removeCoveredIntervals([[1, 4], [2, 3]]) == 1
    assert removeCoveredIntervals([[1, 4], [1, 6], [3, 5]]) == 1  # same-start tie case
    assert removeCoveredIntervals([[2, 9], [3, 4], [5, 10]]) == 2  # overlap != coverage
    assert removeCoveredIntervals([[0, 5]]) == 1
    print("All tests passed.")
