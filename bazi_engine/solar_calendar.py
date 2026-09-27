from dataclasses import dataclass
from datetime import datetime, timezone

from .solar_terms import SOLAR_TERMS, find_solar_term, solar_term_longitude


@dataclass(frozen=True)
class SolarTermMoment:
    name: str
    moment_utc: datetime
    longitude: float


def get_solar_term_moment(name: str, year: int) -> SolarTermMoment:
    """Calculate the UTC moment of a solar term for a given year."""
    term = next((item for item in SOLAR_TERMS if item.name == name), None)
    if term is None:
        raise ValueError(f"Unknown solar term: {name}")

    longitude = solar_term_longitude(name)

    # 小寒 and 大寒 (315° and 300°) occur in January of the requested year;
    # 立春 (315° under the conventional 0°=春分 system) remains in February.
    months = {
        "小寒": (year, 1), "大寒": (year, 1),
        "立春": (year, 2), "雨水": (year, 2), "惊蛰": (year, 3),
        "春分": (year, 3), "清明": (year, 4), "谷雨": (year, 4),
        "立夏": (year, 5), "小满": (year, 5), "芒种": (year, 6),
        "夏至": (year, 6), "小暑": (year, 7), "大暑": (year, 7),
        "立秋": (year, 8), "处暑": (year, 8), "白露": (year, 9),
        "秋分": (year, 9), "寒露": (year, 10), "霜降": (year, 10),
        "立冬": (year, 11), "小雪": (year, 11), "大雪": (year, 12),
        "冬至": (year, 12),
    }
    term_year, month = months[name]
    start = datetime(term_year, month, 1, tzinfo=timezone.utc)
    if month == 12:
        end = datetime(term_year + 1, 1, 1, tzinfo=timezone.utc)
    else:
        end = datetime(term_year, month + 1, 1, tzinfo=timezone.utc)

    moment = find_solar_term(start=start, end=end, target_longitude=longitude)
    return SolarTermMoment(name=name, moment_utc=moment, longitude=longitude)