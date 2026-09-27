from datetime import datetime

from .jiazi import JIAZI_CYCLE


# 2000-01-07 is a 甲子 day.
# This is our fixed reference point for the 60-day cycle.
REFERENCE_YEAR = 2000
REFERENCE_MONTH = 1
REFERENCE_DAY = 7
REFERENCE_JIAZI_INDEX = 0


def julian_day_number(year: int, month: int, day: int) -> int:
    """Calculate the Julian Day Number for a Gregorian calendar date.

    The integer JDN changes at civil midnight.
    """
    if month <= 2:
        year -= 1
        month += 12

    century = year // 100
    correction = 2 - century + century // 4

    return (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + correction
        - 1524
    )


def days_between(
    start_year: int,
    start_month: int,
    start_day: int,
    end_year: int,
    end_month: int,
    end_day: int,
) -> int:
    """Return the number of calendar days between two Gregorian dates."""
    start_jdn = julian_day_number(start_year, start_month, start_day)
    end_jdn = julian_day_number(end_year, end_month, end_day)
    return end_jdn - start_jdn


def get_day_pillar_name(birth_moment: datetime) -> str:
    """Calculate the BaZi Day Pillar (日柱) using the civil calendar date.

    The 23:00 Zi-hour boundary and true-solar-time correction will be
    configurable in a later layer.
    """
    if birth_moment.tzinfo is None:
        raise ValueError("birth_moment must be timezone-aware")

    offset = days_between(
        REFERENCE_YEAR,
        REFERENCE_MONTH,
        REFERENCE_DAY,
        birth_moment.year,
        birth_moment.month,
        birth_moment.day,
    )
    cycle_index = (REFERENCE_JIAZI_INDEX + offset) % 60
    return JIAZI_CYCLE[cycle_index].name