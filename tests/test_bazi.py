from datetime import timedelta

from bazi_engine.jiazi import JIAZI_CYCLE
from bazi_engine.month import get_month_branch
from bazi_engine.solar_calendar import get_solar_term_moment
from bazi_engine.year import get_bazi_year


def test_jiazi_cycle_has_60_pillars():
	assert len(JIAZI_CYCLE) == 60


def test_jiazi_cycle_starts_with_jia_zi():
	assert JIAZI_CYCLE[0].name == "甲子"


def test_jiazi_cycle_ends_with_gui_hai():
	assert JIAZI_CYCLE[59].name == "癸亥"


def test_jiazi_cycle_has_unique_names():
	names = [pillar.name for pillar in JIAZI_CYCLE]

	assert len(names) == len(set(names))


def test_bazi_year_changes_at_lichun():
	lichun = get_solar_term_moment(
		"立春",
		2026,
	).moment_utc

	before_lichun = lichun - timedelta(seconds=1)
	after_lichun = lichun + timedelta(seconds=1)

	assert get_bazi_year(before_lichun) == 2025
	assert get_bazi_year(after_lichun) == 2026


def test_month_branch_changes_at_xiaohan():
	xiaohan = get_solar_term_moment(
		"小寒",
		2026,
	).moment_utc

	before_xiaohan = xiaohan - timedelta(seconds=1)
	after_xiaohan = xiaohan + timedelta(seconds=1)

	assert get_month_branch(before_xiaohan) == "子"
	assert get_month_branch(after_xiaohan) == "丑"


MONTH_BOUNDARIES = (
	("小寒", "子", "丑"),
	("立春", "丑", "寅"),
	("惊蛰", "寅", "卯"),
	("清明", "卯", "辰"),
	("立夏", "辰", "巳"),
	("芒种", "巳", "午"),
	("小暑", "午", "未"),
	("立秋", "未", "申"),
	("白露", "申", "酉"),
	("寒露", "酉", "戌"),
	("立冬", "戌", "亥"),
	("大雪", "亥", "子"),
)


def test_all_month_boundaries():
	for term_name, before_branch, after_branch in MONTH_BOUNDARIES:
		term = get_solar_term_moment(
			term_name,
			2026,
		).moment_utc

		before_term = term - timedelta(seconds=1)
		after_term = term + timedelta(seconds=1)

		assert get_month_branch(before_term) == before_branch
		assert get_month_branch(after_term) == after_branch
