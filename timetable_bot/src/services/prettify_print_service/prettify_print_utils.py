from message_config import (MONDAY, TUESDAY, WEDNESDAY, THURSTDAY, FRIDAY, SATURDAY, SUNDAY)


DAY_MINUTES = 1440
WEEK_DAYS = [MONDAY, TUESDAY, WEDNESDAY, THURSTDAY, FRIDAY, SATURDAY, SUNDAY]

INTERVAL_TEMPLATE = '{week_day}: {start_mins:0>2}:{start_secs:0>2}-{end_mins:0>2}:{end_secs:0>2}'
INTERVAL_SHORT_TEMPLATE = '{start_mins:0>2}:{start_secs:0>2}-{end_mins:0>2}:{end_secs:0>2}'


def index_to_week_day(index: int) -> str:
    return WEEK_DAYS[index]


def minutes_to_week_day_time(minutes: int) -> tuple[int, int, int]:
    week_day = minutes // DAY_MINUTES
    remain_minutes = minutes - week_day * DAY_MINUTES

    return week_day, remain_minutes // 60, remain_minutes % 60


def timetable_strs_generator(timetable: list[tuple[int, int]]):
    week_ind = 0
    for start, end in timetable:
        if start > week_ind * DAY_MINUTES:
            yield f'\n{index_to_week_day(week_ind)}:\n'
            while start > week_ind * DAY_MINUTES:
                week_ind += 1

        _, start_mins, start_secs = minutes_to_week_day_time(start)
        _, end_mins, end_secs = minutes_to_week_day_time(end)
        interval_str = INTERVAL_SHORT_TEMPLATE.format(start_mins=start_mins,
                                                      start_secs=start_secs,
                                                      end_mins=end_mins,
                                                      end_secs=end_secs)
        yield f'({interval_str})'
