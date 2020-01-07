from datetime import date, timedelta


def next_workday():
    delta = timedelta(days=1)
    result = date.today() + delta
    while result.isoweekday() not in [1, 2, 3, 4, 5]:
        result += delta
    return result


def today_is_workday():
    return date.today().isoweekday() in [1, 2, 3, 4, 5]
