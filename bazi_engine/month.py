from datetime import datetime, timezone

from .solar_calendar import get_solar_term_moment


MONTH_START_TERMS = (
	"小寒",
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
)


MONTH_BRANCHES = (
	"丑",
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
)


def get_month_branch(birth_moment_utc: datetime) -> str:
	"""Determine the BaZi month branch from solar-term boundaries."""
	if birth_moment_utc.tzinfo is None:
		raise ValueError("birth_moment_utc must be timezone-aware")

	birth_moment_utc = birth_moment_utc.astimezone(timezone.utc)
	year = birth_moment_utc.year

	# The previous year's 大雪 starts 子月 and remains valid until 小寒.
	boundaries: list[tuple[datetime, str]] = [
		(get_solar_term_moment("大雪", year - 1).moment_utc, "子")
	]

	for term_name, branch in zip(MONTH_START_TERMS, MONTH_BRANCHES):
		term_moment = get_solar_term_moment(term_name, year).moment_utc
		boundaries.append((term_moment, branch))

	valid_boundaries = [
		boundary for boundary in boundaries if boundary[0] <= birth_moment_utc
	]
	if not valid_boundaries:
		raise ValueError("Unable to determine BaZi month branch.")

	return max(valid_boundaries, key=lambda boundary: boundary[0])[1]
