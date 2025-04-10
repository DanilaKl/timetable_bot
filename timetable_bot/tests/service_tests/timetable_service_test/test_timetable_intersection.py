import pytest

from services.timetable_service import timetable_utils as ttu


def test_empty_result():
    group_timetable = [
        [(0, 144)],
        [(456, 546)]
    ]
    res = ttu.find_timetable_intersections(group_timetable)

    assert len(res) == 0


def test_empty_table():
    group_timetable = []
    with pytest.raises(ValueError):
        ttu.find_timetable_intersections(group_timetable)


def generate_timetables() -> list:
    # 10_080 min in week
    # 1440 min in day
    # 420 - 1380
    case1 = ([
        [(0, 1000), (2000, 3000), (4500, 5500)],
        [(500, 1500), (2500, 3500), (4000, 5000)]
    ],  [(500, 1000), (2500, 3000), (4500, 5000)])

    case2 = ([
        [(0, 500), (600, 900),  (2000, 2500)],
        [(300, 1000),           (2200, 3000)],
        [(700, 1500),           (2100, 2300), (2400, 2700)]
    ],  [(700, 900),            (2200, 2300), (2400, 2500)])

    case3 = ([
        [(0, 1000), (1500, 2500), (3000, 4000)],
        [(900, 2000), (2400, 3500)]
    ],  [(900, 1000), (1500, 2000), (2400, 2500), (3000, 3500)])

    case4 = ([
        [(0, 500), (500, 1000), (1000, 1500)],
        [(0, 1000), (1000, 1500)]
    ],  [(0, 500), (500, 1000), (1000, 1500)])

    return [case1, case2, case3, case4]


@pytest.mark.parametrize(['timetable', 'expected'], generate_timetables())
def test_on_different_data(timetable: list[list[tuple]], expected: int) -> None:
    result = ttu.find_timetable_intersections(timetable)
    assert result == expected
