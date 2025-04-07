from services.timetable_service import timetable_utils as ttu


def test_merge_with_empty_intervals():
    assert 1 == 1


def test_construct_only_add_intervals():
    add_intervals = [(800, 900), (100, 200), (500, 600), (300, 400)]

    result = ttu.construct_timetable([], add_intervals, [])

    assert sorted(add_intervals) == result


def test_construct_rem_intervals_before_add_intervals():
    add_intervals = [(800, 900), (1000, 1400)]
    rem_intervals = [(100, 200), (300, 400), (500, 600)]

    result = ttu.construct_timetable([], add_intervals, rem_intervals)

    assert add_intervals == result


def test_construct_rem_intervals_after_add_intervals():
    add_intervals = [(100, 200), (300, 400)]
    rem_intervals = [(500, 600), (700, 800)]

    result = ttu.construct_timetable([], add_intervals, rem_intervals)

    assert add_intervals == result


def test_construct_rem_interval_includes_all_add_intervals():
    add_intervals = [(300, 400), (500, 600)]
    rem_intervals = [(100, 800)]

    result = ttu.construct_timetable([], add_intervals, rem_intervals)

    assert len(result) == 0


def test_construct_sevral_rem_intervals_in_one_add_interval():
    add_intervals = [(50, 500), (700, 800)]
    rem_intervals = [(100, 200), (300, 400)]
    expected = [(50, 100), (200, 300), (400, 500), (700, 800)]

    result = ttu.construct_timetable([], add_intervals, rem_intervals)

    assert expected == result


def test_construct_intervals_intersections():
    add_intervals = [(100, 500), (1100, 1500), (2100, 2500), (3100, 3500)]
    rem_intervals = [(300, 500), (900, 1200), (2200, 2300), (3100, 3500)]
    expected = [(100, 300), (1200, 1500), (2100, 2200), (2300, 2500)]

    result = ttu.construct_timetable([], add_intervals, rem_intervals)

    assert expected == result


def test_intersecting_add_intervals():
    add_intervals = [(100, 300), (200, 400),
                     (600, 1000), (700, 800), (850, 900),
                     (1100, 1500)]
    expected = [(100, 400), (600, 1000), (1100, 1500)]

    result = ttu.construct_timetable([], add_intervals, [])

    assert expected == result


def test_add_intervals_to_existing_timetable():
    old_timetable = [(300, 500), (900, 1100), (1800, 2000)]
    add_intervals = [(100, 200),
                     (550, 600), (700, 800),
                     (2100, 2500), (2600, 2700)]
    expected = [(100, 200), (300, 500), (550, 600),
                (700, 800), (900, 1100), (1800, 2000),
                (2100, 2500), (2600, 2700)]

    result = ttu.construct_timetable(old_timetable, add_intervals, [])

    assert expected == result


def test_intersecting_add_intervals_with_existing_timetable():
    old_timetable = [(300, 500), (900, 1100), (1800, 2000), (3000, 4000)]
    add_intervals = [(100, 150), (200, 300),
                     (900, 950), (1000, 1050),
                     (1900, 2100)]
    expected = [(100, 150), (200, 500), (900, 1100), (1800, 2100), (3000, 4000)]

    result = ttu.construct_timetable(old_timetable, add_intervals, [])

    assert expected == result
