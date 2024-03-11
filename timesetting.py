import datetime


def clockify2normal(cl_date):
    dates = cl_date[0:10]
    times = cl_date[11:19]

    year, month, day = dates.split('-')
    hour, mins, sec = times.split(':')

    return datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(mins),
                             second=int(sec))


def normal2clockify(norm_date):
    return f"{norm_date.strftime('%Y-%m-%dT%H:%M:%SZ')}"


from datetime import datetime, timezone, timedelta


def utc2Teh(utc_time):
    tehran_offset = timedelta(hours=3.5)
    tehran_datetime = utc_time + tehran_offset

    return tehran_datetime


def Teh2utc(in_time):
    tehran_offset = timedelta(hours=3.5)

    tehran_datetime = in_time
    utc_datetime = tehran_datetime - tehran_offset

    return utc_datetime


def ifmonth():
    return True if datetime.datetime.now().date().day == 16 else False


import datetime


def daily_interval():
    today = datetime.datetime.now().date()
    yesterday = today - datetime.timedelta(days=1)

    end = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
    start = datetime.datetime(year=yesterday.year, month=yesterday.month, day=yesterday.day, hour=0, minute=0, second=0)

    return [start, end]


def duration_to_time(duration_str):
    duration_str = duration_str[2:]  # Remove 'PT' prefix and 'S' suffix
    hour, mins, sec = 0, 0, 0
    start = 0
    for i, char in enumerate(duration_str):
        if not char.isdigit():
            end = i
            if char == 'H':
                hour = int(duration_str[start:end])
            elif char == 'M':
                mins = int(duration_str[start:end])
            elif char == 'S':
                sec = int(duration_str[start:end])
            start = i + 1

    return datetime.time(hour, mins, sec)


def monthly_interval():
    today = datetime.datetime.now().date()
    today = today.replace(day=15)
    pre_month = today - datetime.timedelta(days=today.day + 1)
    pre_month = pre_month.replace(day=15)

    end = datetime.datetime(year=today.year, month=today.month, day=today.day, hour=0, minute=0, second=0)
    start = datetime.datetime(year=pre_month.year, month=pre_month.month, day=pre_month.day, hour=0, minute=0, second=0)

    return [start, end]


def delta2hr(timdelta):
    secs = timdelta.seconds
    mins = secs // 60
    secs %= 60
    hrs = mins // 60 + timdelta.days * 24
    mins %= 60
    return f'{hrs}:{mins:02}:{secs:02}'
