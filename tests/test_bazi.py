from datetime import timedelta, datetime, timezone

from bazi_engine.jiazi import JIAZI_CYCLE
from bazi_engine.month import get_month_branch
from bazi_engine.month_pillar import get_month_pillar
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
	lichun = get_solar_term_moment("立春", 2026).moment_utc
	assert get_bazi_year(lichun - timedelta(seconds=1)) == 2025
	assert get_bazi_year(lichun + timedelta(seconds=1)) == 2026


def test_month_branch_changes_at_xiaohan():
	xiaohan = get_solar_term_moment("小寒", 2026).moment_utc
	assert get_month_branch(xiaohan - timedelta(seconds=1)) == "子"
	assert get_month_branch(xiaohan + timedelta(seconds=1)) == "丑"


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
		term = get_solar_term_moment(term_name, 2026).moment_utc
		assert get_month_branch(term - timedelta(seconds=1)) == before_branch
		assert get_month_branch(term + timedelta(seconds=1)) == after_branch


EXPECTED_MONTH_PILLARS_2026 = (
	("2026-02-10", "庚寅"),
	("2026-03-10", "辛卯"),
	("2026-04-10", "壬辰"),
	("2026-05-10", "癸巳"),
	("2026-06-10", "甲午"),
	("2026-07-10", "乙未"),
	("2026-08-10", "丙申"),
	("2026-09-10", "丁酉"),
	("2026-10-10", "戊戌"),
	("2026-11-10", "己亥"),
	("2026-12-10", "庚子"),
	("2027-01-10", "辛丑"),
)


def test_month_pillars_2026_cycle():
	for date_text, expected_pillar in EXPECTED_MONTH_PILLARS_2026:
		moment = datetime.fromisoformat(date_text).replace(hour=12, tzinfo=timezone.utc)
		assert get_month_pillar(moment) == expected_pillar
