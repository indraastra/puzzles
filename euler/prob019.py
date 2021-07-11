#!/usr/bin/python

month_days = [ None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]

def next_first(date, day):
    date, month, year = date
    next_date = 1
    next_month = (month % 12) + 1
    next_year = year
    if month == 12:
        next_year = next_year + 1
    day_span = (month_days[month]) % 7
    if is_leap_year(year) and month == 2:
        day_span += 1
    next_day = (day + day_span) % 7
    return (next_date, next_month, next_year), next_day

def is_leap_year(year):
    return (year % 400 == 0) or (not (year % 100 == 0) and (year % 4 == 0))

if __name__ == "__main__":
    date = (1, 1, 1900)
    day = 1
    # subtract 2 days to exclude 1900
    sundays = -2
    while date[2] <= 2000:
        if day == 0:
            sundays += 1
        date, day = next_first(date, day)
    print(sundays)
