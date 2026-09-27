from datetime import datetime

from .month import get_month_branch
from .year import get_year_pillar_name
from .stems import STEMS
from .branches import BRANCH_BY_NAME


# Starting Heavenly Stem for 寅 month according to the Year Stem.
# 五虎遁月
YIN_MONTH_START_STEM = {
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


def get_month_pillar(
	birth_moment_utc: datetime,
) -> str:
	"""Calculate the complete BaZi month pillar."""
	year_pillar = get_year_pillar_name(birth_moment_utc)
	year_stem = year_pillar[0]

	month_branch = get_month_branch(birth_moment_utc)
	start_stem = YIN_MONTH_START_STEM[year_stem]

	month_branch_order = (
		"寅", "卯", "辰", "巳", "午", "未",
		"申", "酉", "戌", "亥", "子", "丑",
	)
	month_index = month_branch_order.index(
		BRANCH_BY_NAME[month_branch].name
	)

	start_stem_index = next(
		i for i, stem in enumerate(STEMS)
		if stem.name == start_stem
	)
	month_stem = STEMS[(start_stem_index + month_index) % 10].name

	return f"{month_stem}{month_branch}"
