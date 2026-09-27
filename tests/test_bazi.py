from bazi_engine.jiazi import JIAZI_CYCLE


def test_jiazi_cycle_has_60_pillars():
	assert len(JIAZI_CYCLE) == 60


def test_jiazi_cycle_starts_with_jia_zi():
	assert JIAZI_CYCLE[0].name == "甲子"


def test_jiazi_cycle_ends_with_gui_hai():
	assert JIAZI_CYCLE[59].name == "癸亥"


def test_jiazi_cycle_has_unique_names():
	names = [pillar.name for pillar in JIAZI_CYCLE]

	assert len(names) == len(set(names))
