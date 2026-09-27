from dataclasses import dataclass
from datetime import datetime, timezone

from .day import get_day_pillar_name
from .hour import get_hour_pillar
from .month_pillar import get_month_pillar
from .year import get_year_pillar_name


@dataclass(frozen=True)
class BaziChart:
	"""Complete Four Pillars of Destiny (八字命盘)."""

	birth_moment: datetime
	year_pillar: str
	month_pillar: str
	day_pillar: str
	hour_pillar: str

	@property
	def pillars(self) -> tuple[str, str, str, str]:
		"""Return the pillars in traditional order: 年柱, 月柱, 日柱, 时柱."""
		return (
			self.year_pillar,
			self.month_pillar,
			self.day_pillar,
			self.hour_pillar,
		)

	@property
	def day_stem(self) -> str:
		"""Return the Day Stem (日干)."""
		return self.day_pillar[0]

	@property
	def day_branch(self) -> str:
		"""Return the Day Branch (日支)."""
		return self.day_pillar[1]

	@classmethod
	def calculate(cls, birth_moment: datetime) -> "BaziChart":
		"""Calculate a complete BaZi chart from a timezone-aware birth datetime."""
		if birth_moment.tzinfo is None:
			raise ValueError("birth_moment must be timezone-aware")

		birth_moment_utc = birth_moment.astimezone(timezone.utc)

		year_pillar = get_year_pillar_name(birth_moment_utc)
		month_pillar = get_month_pillar(birth_moment_utc)

		# Day and hour calculations use the local civil clock/date.
		day_pillar = get_day_pillar_name(birth_moment)
		hour_pillar = get_hour_pillar(birth_moment, day_pillar)

		return cls(
			birth_moment=birth_moment,
			year_pillar=year_pillar,
			month_pillar=month_pillar,
			day_pillar=day_pillar,
			hour_pillar=hour_pillar,
		)
