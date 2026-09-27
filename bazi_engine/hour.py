from datetime import datetime

from .stems import STEMS


HOUR_BRANCHES = (
	"子",  # 23:00–00:59
	"丑",  # 01:00–02:59
	"寅",  # 03:00–04:59
	"卯",  # 05:00–06:59
	"辰",  # 07:00–08:59
	"巳",  # 09:00–10:59
	"午",  # 11:00–12:59
	"未",  # 13:00–14:59
	"申",  # 15:00–16:59
	"酉",  # 17:00–18:59
	"戌",  # 19:00–20:59
	"亥",  # 21:00–22:59
)


# 五鼠遁
# For each pair of Day Stems, this is the Hour Stem
# that starts at 子时.
FIRST_HOUR_STEM = {
	"甲": "丙",
	"己": "丙",
	"乙": "戊",
	"庚": "戊",
	"丙": "庚",
	"辛": "庚",
	"丁": "壬",
	"壬": "壬",
	"戊": "甲",
	"癸": "甲",
}


def get_hour_branch(birth_moment: datetime) -> str:
	"""
	Determine the Earthly Branch of the birth hour.

	This version uses civil/local clock time.
	True solar time will be added later as a configurable layer.
	"""

	if birth_moment.tzinfo is None:
		raise ValueError(
			"birth_moment must be timezone-aware"
		)

	hour = birth_moment.hour

	# 子时 begins at 23:00.
	if hour == 23:
		return "子"

	branch_index = (hour + 1) // 2

	return HOUR_BRANCHES[branch_index]


def get_hour_pillar(
	birth_moment: datetime,
	day_pillar_name: str,
) -> str:
	"""
	Calculate the complete BaZi Hour Pillar (时柱).

	The hour branch is determined from local clock time.
	The hour stem is determined from the Day Stem using 五鼠遁.
	"""

	if birth_moment.tzinfo is None:
		raise ValueError(
			"birth_moment must be timezone-aware"
		)

	if len(day_pillar_name) != 2:
		raise ValueError(
			"day_pillar_name must contain exactly two Chinese characters"
		)

	day_stem = day_pillar_name[0]

	if day_stem not in FIRST_HOUR_STEM:
		raise ValueError(
			f"Unknown Day Stem: {day_stem}"
		)

	hour_branch = get_hour_branch(birth_moment)

	branch_index = HOUR_BRANCHES.index(hour_branch)

	first_stem = FIRST_HOUR_STEM[day_stem]

	first_stem_index = next(
		i
		for i, stem in enumerate(STEMS)
		if stem.name == first_stem
	)

	hour_stem_index = (
		first_stem_index + branch_index
	) % 10

	hour_stem = STEMS[hour_stem_index].name

	return f"{hour_stem}{hour_branch}"
