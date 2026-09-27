from datetime import datetime, timedelta, timezone

from bazi_engine.chart import BaziChart
from bazi_engine.day import get_day_pillar_name
from bazi_engine.hour import get_hour_pillar
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

	before_lichun = lichun - timedelta(seconds=1)
	after_lichun = lichun + timedelta(seconds=1)

	assert get_bazi_year(before_lichun) == 2025
	assert get_bazi_year(after_lichun) == 2026


def test_month_branch_changes_at_xiaohan():
	xiaohan = get_solar_term_moment("小寒", 2026).moment_utc

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
		term = get_solar_term_moment(term_name, 2026).moment_utc

		assert get_month_branch(term - timedelta(seconds=1)) == before_branch
		assert get_month_branch(term + timedelta(seconds=1)) == after_branch


EXPECTED_MONTH_PILLARS_2026 = tuple(
	zip(
		(
			"2026-02-10", "2026-03-10", "2026-04-10", "2026-05-10",
			"2026-06-10", "2026-07-10", "2026-08-10", "2026-09-10",
			"2026-10-10", "2026-11-10", "2026-12-10", "2027-01-10",
		),
		("庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑"),
	)
)


def test_month_pillars_2026_cycle():
	for date_text, expected_pillar in EXPECTED_MONTH_PILLARS_2026:
		moment = datetime.fromisoformat(date_text).replace(hour=12, tzinfo=timezone.utc)
		assert get_month_pillar(moment) == expected_pillar


EXPECTED_DAY_PILLARS = (
	("2000-01-07", "甲子"), ("2000-01-08", "乙丑"), ("2000-01-09", "丙寅"),
	("2026-02-10", "乙卯"), ("2026-02-11", "丙辰"),
)


def test_day_pillars_reference_dates():
	for date_text, expected_pillar in EXPECTED_DAY_PILLARS:
		moment = datetime.fromisoformat(date_text).replace(hour=12, tzinfo=timezone.utc)
		assert get_day_pillar_name(moment) == expected_pillar


def test_day_pillar_advances_one_step_per_day():
	start = datetime(2000, 1, 7, 12, tzinfo=timezone.utc)
	for offset in range(60):
		assert get_day_pillar_name(start + timedelta(days=offset)) == JIAZI_CYCLE[offset].name


def test_hour_pillars_for_jia_zi_day():
	tests = ((0, "丙子"), (1, "丁丑"), (3, "戊寅"), (5, "己卯"), (7, "庚辰"), (9, "辛巳"), (11, "壬午"), (13, "癸未"), (15, "甲申"), (17, "乙酉"), (19, "丙戌"), (21, "丁亥"), (23, "丙子"))
	for hour, expected in tests:
		moment = datetime(2000, 1, 7, hour, tzinfo=timezone.utc)
		assert get_hour_pillar(moment, "甲子") == expected


def test_hour_stem_for_all_day_stems():
	expected = {"甲": "丙", "乙": "戊", "丙": "庚", "丁": "壬", "戊": "甲", "己": "丙", "庚": "戊", "辛": "庚", "壬": "壬", "癸": "甲"}
	for day_stem, hour_stem in expected.items():
		moment = datetime(2000, 1, 7, tzinfo=timezone.utc)
		assert get_hour_pillar(moment, day_stem + "子") == hour_stem + "子"


def test_full_bazi_chart_calculation():
	birth_moment = datetime(2026, 2, 10, 12, tzinfo=timezone.utc)
	chart = BaziChart.calculate(birth_moment)

	assert chart.year_pillar == "丙午"
	assert chart.month_pillar == "庚寅"
	assert chart.day_pillar == "乙卯"
	assert chart.hour_pillar == "甲午"
	assert chart.pillars == ("丙午", "庚寅", "乙卯", "甲午")
	assert chart.day_stem == "乙"
	assert chart.day_branch == "卯"
