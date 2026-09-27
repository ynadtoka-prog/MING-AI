from dataclasses import dataclass
from datetime import datetime, timezone

import swisseph as swe


@dataclass(frozen=True)
class SolarTerm:
    name: str
    longitude: float


SOLAR_TERMS: tuple[SolarTerm, ...] = (
    SolarTerm("春分", 0.0),
    SolarTerm("清明", 15.0),
    SolarTerm("谷雨", 30.0),
    SolarTerm("立夏", 45.0),
    SolarTerm("小满", 60.0),
    SolarTerm("芒种", 75.0),
    SolarTerm("夏至", 90.0),
    SolarTerm("小暑", 105.0),
    SolarTerm("大暑", 120.0),
    SolarTerm("立秋", 135.0),
    SolarTerm("处暑", 150.0),
    SolarTerm("白露", 165.0),
    SolarTerm("秋分", 180.0),
    SolarTerm("寒露", 195.0),
    SolarTerm("霜降", 210.0),
    SolarTerm("立冬", 225.0),
    SolarTerm("小雪", 240.0),
    SolarTerm("大雪", 255.0),
    SolarTerm("冬至", 270.0),
    SolarTerm("小寒", 285.0),
    SolarTerm("大寒", 300.0),
    SolarTerm("立春", 315.0),
    SolarTerm("雨水", 330.0),
    SolarTerm("惊蛰", 345.0),
)


def sun_longitude(julian_day_ut: float) -> float:
    """Return the Sun's apparent geocentric ecliptic longitude."""
    result, _, _ = swe.calc_ut(julian_day_ut, swe.SUN)
    return result[0] % 360.0


def datetime_to_julian_day(moment: datetime) -> float:
    """Convert an aware datetime to Julian Day (UT)."""
    if moment.tzinfo is None or moment.utcoffset() is None:
        raise ValueError("moment must be timezone-aware")

    utc_moment = moment.astimezone(timezone.utc)
    decimal_hour = (
        utc_moment.hour
        + utc_moment.minute / 60.0
        + utc_moment.second / 3600.0
        + utc_moment.microsecond / 3_600_000_000.0
    )
    return swe.julday(
        utc_moment.year, utc_moment.month, utc_moment.day, decimal_hour
    )


def solar_term_longitude(name: str) -> float:
    """Return the target solar longitude for a named solar term."""
    for term in SOLAR_TERMS:
        if term.name == name:
            return term.longitude
    raise ValueError(f"Unknown solar term: {name}")


def longitude_difference(current: float, target: float) -> float:
    """Return signed angular difference in the range [-180, 180)."""
    return (current - target + 180.0) % 360.0 - 180.0


def find_solar_term(
    start: datetime,
    end: datetime,
    target_longitude: float,
) -> datetime:
    """Find the UTC moment the Sun reaches target_longitude in the interval."""
    if (
        start.tzinfo is None
        or start.utcoffset() is None
        or end.tzinfo is None
        or end.utcoffset() is None
    ):
        raise ValueError("start and end must be timezone-aware")

    start = start.astimezone(timezone.utc)
    end = end.astimezone(timezone.utc)
    if start > end:
        raise ValueError("start must not be after end")

    target_longitude %= 360.0
    start_diff = longitude_difference(
        sun_longitude(datetime_to_julian_day(start)), target_longitude
    )
    end_diff = longitude_difference(
        sun_longitude(datetime_to_julian_day(end)), target_longitude
    )

    if start_diff == 0:
        return start
    if end_diff == 0:
        return end
    if start_diff * end_diff > 0:
        raise ValueError(
            "The requested solar-term crossing was not found "
            "inside the supplied time interval."
        )

    left, right = start, end
    for _ in range(50):
        middle = left + (right - left) / 2
        middle_diff = longitude_difference(
            sun_longitude(datetime_to_julian_day(middle)), target_longitude
        )
        if abs(middle_diff) < 1e-8:
            return middle
        if start_diff * middle_diff <= 0:
            right = middle
            end_diff = middle_diff
        else:
            left = middle
            start_diff = middle_diff

    return left + (right - left) / 2