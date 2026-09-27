from datetime import datetime, timezone

from .solar_calendar import get_solar_term_moment
from .jiazi import JIAZI_CYCLE


# 1984 was a 甲子 year after 立春.
REFERENCE_YEAR = 1984


def get_bazi_year(birth_moment_utc: datetime) -> int:
	"""Determine the BaZi year according to the 立春 boundary."""
	if birth_moment_utc.tzinfo is None:
		raise ValueError("birth_moment_utc must be timezone-aware")

	birth_moment_utc = birth_moment_utc.astimezone(timezone.utc)
	calendar_year = birth_moment_utc.year
	lichun = get_solar_term_moment("立春", calendar_year).moment_utc

	if birth_moment_utc < lichun:
		return calendar_year - 1
	return calendar_year


def get_year_pillar_name(birth_moment_utc: datetime) -> str:
	"""Return the complete BaZi year pillar, for example 甲子 or 丙午."""
	bazi_year = get_bazi_year(birth_moment_utc)
	cycle_index = (bazi_year - REFERENCE_YEAR) % 60
	return JIAZI_CYCLE[cycle_index].name
