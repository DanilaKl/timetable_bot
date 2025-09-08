from .prettify_print_utils import (index_to_week_day,
                                   timetable_strs_generator, minutes_to_week_day_time,
                                   INTERVAL_TEMPLATE, INTERVAL_SHORT_TEMPLATE)


def prettify_week_day(index: int) -> str:
    return index_to_week_day(index)


def prettify_interval(interval: tuple[int, int]) -> str:
    start_week_ind, start_mins, start_secs = minutes_to_week_day_time(interval[0])
    _, end_mins, end_secs = minutes_to_week_day_time(interval[1])

    return INTERVAL_TEMPLATE.format(week_day=index_to_week_day(start_week_ind),
                                    start_mins=start_mins,
                                    start_secs=start_secs,
                                    end_mins=end_mins,
                                    end_secs=end_secs)


def prettify_interval_short(interval: tuple[int, int]) -> str:
    _, start_mins, start_secs = minutes_to_week_day_time(interval[0])
    _, end_mins, end_secs = minutes_to_week_day_time(interval[1])

    return INTERVAL_SHORT_TEMPLATE.format(start_mins=start_mins,
                                          start_secs=start_secs,
                                          end_mins=end_mins,
                                          end_secs=end_secs)


def prettify_timetable(timetable: list[tuple[int, int]]) -> str:
    if not timetable:
        return ''

    return ' '.join(timetable_strs_generator(timetable))


__all__ = [
    "prettify_week_day",
    "prettify_interval",
    "prettify_interval_short",
    "prettify_timetable",
]
