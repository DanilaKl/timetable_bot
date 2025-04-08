from queue import PriorityQueue


def find_timetable_intersections(timetables: list[list[tuple]]) -> list[tuple]:
    if not timetables:
        raise ValueError("timetables must have at least one timetable")

    people_iters = [iter(timetable) for timetable in timetables]
    event_queue: PriorityQueue = PriorityQueue()

    # Initialize queue
    for i in range(len(timetables)):
        start, stop = next(people_iters[i])
        event_queue.put((start, i, True))
        event_queue.put((stop, i, False))

    result = []

    intersect_start = 0
    person_counter = 0
    while not event_queue.empty():
        num, ind, is_start = event_queue.get()
        if is_start:
            intersect_start = max(num, intersect_start)
            person_counter += 1  # the intervals of one person cannot overlap
        else:
            try:
                start, stop = next(people_iters[ind])
                event_queue.put((start, ind, True))
                event_queue.put((stop, ind, False))
            except StopIteration:
                pass

            if intersect_start < num and person_counter == len(timetables):
                result.append((intersect_start, num))
            person_counter -= 1

    return result


def _merge_intervals(intervals1: list[tuple], intervals2: list[tuple]) -> list[tuple]:
    """merge two sorted lists of intervals"""
    if not intervals1:
        return intervals2

    if not intervals2:
        return intervals1

    ind1 = 0
    ind2 = 0
    merged = []
    while ind1 < len(intervals1) and ind2 < len(intervals2):
        if (intervals1[ind1][0] < intervals2[ind2][0]
                or intervals1[ind1][1] < intervals2[ind2][1]):
            merged.append(intervals1[ind1])
            ind1 += 1
        else:
            merged.append(intervals2[ind2])
            ind2 += 1

    while ind1 < len(intervals1):
        merged.append(intervals1[ind1])
        ind1 += 1

    while ind2 < len(intervals2):
        merged.append(intervals2[ind2])
        ind2 += 1

    return merged


def _compress_intervals(intervals: list[tuple]) -> list[tuple]:
    """merges intersecting intervals, removes unnecessary ones"""
    if not intervals:
        return []

    compressed = []
    cur_interval_start, cur_interval_end = intervals[0]

    for interval in intervals:
        if cur_interval_end < interval[0]:
            compressed.append((cur_interval_start, cur_interval_end))
            cur_interval_start, cur_interval_end = interval
        else:
            cur_interval_end = max(cur_interval_end, interval[1])
    compressed.append((cur_interval_start, cur_interval_end))

    return compressed


def _interval_split(interval: tuple, sub_interval: tuple) -> tuple[tuple | None, tuple | None]:
    left_part = None
    right_part = None

    if interval[0] < sub_interval[0]:
        left_part = (interval[0], min(interval[1], sub_interval[0]))

    if interval[1] > sub_interval[1]:
        right_part = (max(interval[0], sub_interval[1]), interval[1])

    return left_part, right_part


def construct_timetable(timetable: list[tuple],
                        add_intervals: list[tuple],
                        rem_intervals: list[tuple]):
    add_intervals.sort()
    rem_intervals.sort()

    add_intervals = _merge_intervals(timetable, add_intervals)
    add_intervals = _compress_intervals(add_intervals)

    if not add_intervals:
        return []

    if not rem_intervals:
        return add_intervals

    new_timetable = []
    add_ind = 0
    rem_ind = 0
    cur_interval = add_intervals[0]
    while add_ind < len(add_intervals) and rem_ind < len(rem_intervals):
        left_part, right_part = _interval_split(cur_interval, rem_intervals[rem_ind])

        if left_part:
            new_timetable.append(left_part)

        if right_part:
            cur_interval = right_part
            rem_ind += 1
        else:
            add_ind += 1
            if add_ind < len(add_intervals):
                cur_interval = add_intervals[add_ind]

    if add_ind < len(add_intervals):
        new_timetable.append(cur_interval)
        new_timetable += add_intervals[add_ind + 1:]

    return new_timetable
