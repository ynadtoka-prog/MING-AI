from datetime import datetime, timezone

from .solar_calendar import get_solar_term_moment


MONTH_BRANCHES = (
    "寅",
    "卯",
    "辰",
    "巳",
    "午",
    "未",
    "申",
    "酉",
    "戌",
    "亥",
    "子",
    "丑",
)


MONTH_START_TERMS = (
    "立春",
    "惊蛰",
    "清明",
    "立夏",
    "芒种",
    "小暑",
    "立秋",
    "白露",
    "寒露",
    "立冬",
    "大雪",
    "小寒",
)


def get_month_branch(birth_moment_utc: datetime) -> str:
    """Determine the BaZi month branch from solar-term boundaries."""
    if birth_moment_utc.tzinfo is None:
        raise ValueError("birth_moment_utc must be timezone-aware")

    birth_moment_utc = birth_moment_utc.astimezone(timezone.utc)
    year = birth_moment_utc.year

    for index, term_name in enumerate(MONTH_START_TERMS):
        term_moment = get_solar_term_moment(term_name, year).moment_utc
        if birth_moment_utc < term_moment:
            return MONTH_BRANCHES[(index - 1) % 12]

    return MONTH_BRANCHES[-1]