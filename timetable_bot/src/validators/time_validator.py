import re

from datetime import time


TIME_REGEXP = (' *(?P<hour1>[0-9]{1,2}):(?P<minute1>[0-9]{1,2})'
               ' *- *'
               '(?P<hour2>[0-9]{1,2}):(?P<minute2>[0-9]{1,2}) *')


def validate_intervals(msg: str) -> tuple[time, time]:
    match = re.fullmatch(
        TIME_REGEXP,
        msg
    )
    if not match:
        raise ValueError('Проверьте данные на корректность')

    try:
        start = time(int(match.group('hour1')),
                     int(match.group('minute1')))
        end = time(int(match.group('hour2')),
                   int(match.group('minute2')))
    except ValueError:
        raise ValueError('Не получилось обработать время. Проверьте введённые данные')

    if start >= end:
        raise ValueError('Конечное время должно быть больше конечного')

    return (start, end)
