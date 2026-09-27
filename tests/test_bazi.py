from datetime import datetime, timedelta, timezone

import pytest

from bazi_engine.chart import BaziChart
from bazi_engine.day import get_day_pillar_name
from bazi_engine.hour import get_hour_pillar
from bazi_engine.jiazi import JIAZI_CYCLE
from bazi_engine.location import BirthLocation
from bazi_engine.month import get_month_branch
from bazi_engine.month_pillar import get_month_pillar
from bazi_engine.solar_calendar import get_solar_term_moment
from bazi_engine.solar_time import (
    longitude_time_offset,
    mean_solar_time,
)
from bazi_engine.year import (
    get_bazi_year,
    get_year_pillar_name,
)


# ============================================================
# JIAZI CYCLE
# ============================================================


def test_jiazi_cycle_has_60_items():
    assert len(JIAZI_CYCLE) == 60


def test_jiazi_cycle_starts_with_jia_zi():
    assert JIAZI_CYCLE[0].name == "甲子"


def test_jiazi_cycle_ends_with_gui_hai():
    assert JIAZI_CYCLE[-1].name == "癸亥"


def test_jiazi_cycle_names_are_unique():
    names = [jiazi.name for jiazi in JIAZI_CYCLE]

    assert len(names) == len(set(names))


# ============================================================
# BAZI YEAR
# ============================================================


def test_bazi_year_before_lichun():
    moment = datetime(
        2026,
        2,
        3,
        19,
        0,
        tzinfo=timezone.utc,
    )

    assert get_bazi_year(moment) == 2025
    assert get_year_pillar_name(moment) == "乙巳"


def test_bazi_year_after_lichun():
    moment = datetime(
        2026,
        2,
        3,
        21,
        0,
        tzinfo=timezone.utc,
    )

    assert get_bazi_year(moment) == 2026
    assert get_year_pillar_name(moment) == "丙午"


# ============================================================
# SOLAR TERMS / MONTH BRANCH
# ============================================================


def test_month_branch_before_xiaohan():
    xiaohan = get_solar_term_moment(
        "小寒",
        2026,
    ).moment_utc

    before = xiaohan - timedelta(seconds=1)

    assert get_month_branch(before) == "子"


def test_month_branch_after_xiaohan():
    xiaohan = get_solar_term_moment(
        "小寒",
        2026,
    ).moment_utc

    after = xiaohan + timedelta(seconds=1)

    assert get_month_branch(after) == "丑"


def test_all_month_boundaries():
    expected = [
        ("小寒", "丑"),
        ("立春", "寅"),
        ("惊蛰", "卯"),
        ("清明", "辰"),
        ("立夏", "巳"),
        ("芒种", "午"),
        ("小暑", "未"),
        ("立秋", "申"),
        ("白露", "酉"),
        ("寒露", "戌"),
        ("立冬", "亥"),
        ("大雪", "子"),
    ]

    for term_name, expected_branch in expected:
        term = get_solar_term_moment(
            term_name,
            2026,
        ).moment_utc

        before = term - timedelta(seconds=1)
        after = term + timedelta(seconds=1)

        previous_branch = get_month_branch(before)
        current_branch = get_month_branch(after)

        assert current_branch == expected_branch
        assert previous_branch != current_branch


# ============================================================
# MONTH PILLARS
# ============================================================


def test_month_pillars_2026():
    expected = [
        ("2026-02-10T12:00:00+00:00", "庚寅"),
        ("2026-03-10T12:00:00+00:00", "辛卯"),
        ("2026-04-10T12:00:00+00:00", "壬辰"),
        ("2026-05-10T12:00:00+00:00", "癸巳"),
        ("2026-06-10T12:00:00+00:00", "甲午"),
        ("2026-07-10T12:00:00+00:00", "乙未"),
        ("2026-08-10T12:00:00+00:00", "丙申"),
        ("2026-09-10T12:00:00+00:00", "丁酉"),
        ("2026-10-10T12:00:00+00:00", "戊戌"),
        ("2026-11-10T12:00:00+00:00", "己亥"),
        ("2026-12-10T12:00:00+00:00", "庚子"),
        ("2027-01-10T12:00:00+00:00", "辛丑"),
    ]

    for date_string, expected_pillar in expected:
        moment = datetime.fromisoformat(date_string)

        assert get_month_pillar(moment) == expected_pillar


# ============================================================
# DAY PILLAR
# ============================================================


def test_day_pillar_reference():
    assert (
        get_day_pillar_name(
            datetime(
                2000,
                1,
                7,
                tzinfo=timezone.utc,
            )
        )
        == "甲子"
    )

    assert (
        get_day_pillar_name(
            datetime(
                2000,
                1,
                8,
                tzinfo=timezone.utc,
            )
        )
        == "乙丑"
    )

    assert (
        get_day_pillar_name(
            datetime(
                2000,
                1,
                9,
                tzinfo=timezone.utc,
            )
        )
        == "丙寅"
    )


def test_day_pillar_2026_reference():
    moment = datetime(
        2026,
        2,
        10,
        tzinfo=timezone.utc,
    )

    assert get_day_pillar_name(moment) == "乙卯"


def test_day_pillar_60_day_cycle():
    start = datetime(
        2000,
        1,
        7,
        tzinfo=timezone.utc,
    )

    for index in range(60):
        moment = start + timedelta(days=index)

        assert (
            get_day_pillar_name(moment)
            == JIAZI_CYCLE[index].name
        )


# ============================================================
# HOUR PILLAR
# ============================================================


def test_hour_pillars_for_jia_zi_day():
    day_pillar = "甲子"

    expected = {
        0: "丙子",
        1: "丁丑",
        3: "戊寅",
        5: "己卯",
        7: "庚辰",
        9: "辛巳",
        11: "壬午",
        13: "癸未",
        15: "甲申",
        17: "乙酉",
        19: "丙戌",
        21: "丁亥",
        23: "丙子",
    }

    for hour, expected_pillar in expected.items():
        moment = datetime(
            2026,
            2,
            10,
            hour,
            0,
            tzinfo=timezone.utc,
        )

        assert (
            get_hour_pillar(
                moment,
                day_pillar,
            )
            == expected_pillar
        )


def test_hour_stem_for_all_day_stems():
    expected = {
        "甲": "丙子",
        "乙": "戊子",
        "丙": "庚子",
        "丁": "壬子",
        "戊": "甲子",
        "己": "丙子",
        "庚": "戊子",
        "辛": "庚子",
        "壬": "壬子",
        "癸": "甲子",
    }

    moment = datetime(
        2026,
        2,
        10,
        0,
        0,
        tzinfo=timezone.utc,
    )

    for day_stem, expected_pillar in expected.items():
        day_pillar = f"{day_stem}子"

        assert (
            get_hour_pillar(
                moment,
                day_pillar,
            )
            == expected_pillar
        )


# ============================================================
# FULL BAZI CHART
# ============================================================


def test_full_bazi_chart():
    birth_moment = datetime(
        2026,
        2,
        10,
        12,
        0,
        tzinfo=timezone.utc,
    )

    chart = BaziChart.calculate(
        birth_moment
    )

    assert chart.year_pillar == "丙午"
    assert chart.month_pillar == "庚寅"
    assert chart.day_pillar == "乙卯"
    assert chart.hour_pillar == "甲午"

    assert chart.pillars == (
        "丙午",
        "庚寅",
        "乙卯",
        "甲午",
    )

    assert chart.day_stem == "乙"
    assert chart.day_branch == "卯"


# ============================================================
# BIRTH LOCATION
# ============================================================


def test_birth_location_izmir():
    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    assert location.city == "Izmir"
    assert location.latitude == 38.4237
    assert location.longitude == 27.1428
    assert location.timezone_name == "Europe/Istanbul"

    assert str(location.timezone) == "Europe/Istanbul"


def test_birth_location_rejects_invalid_latitude():
    with pytest.raises(ValueError):
        BirthLocation(
            city="Izmir",
            latitude=100.0,
            longitude=27.1428,
            timezone_name="Europe/Istanbul",
        )


def test_birth_location_rejects_invalid_longitude():
    with pytest.raises(ValueError):
        BirthLocation(
            city="Izmir",
            latitude=38.4237,
            longitude=200.0,
            timezone_name="Europe/Istanbul",
        )


def test_birth_location_rejects_empty_city():
    with pytest.raises(ValueError):
        BirthLocation(
            city="",
            latitude=38.4237,
            longitude=27.1428,
            timezone_name="Europe/Istanbul",
        )


def test_birth_location_rejects_invalid_timezone():
    with pytest.raises(Exception):
        BirthLocation(
            city="Izmir",
            latitude=38.4237,
            longitude=27.1428,
            timezone_name="Invalid/Timezone",
        )


# ============================================================
# MEAN SOLAR TIME
# ============================================================


def test_izmir_longitude_time_offset():
    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    local_moment = datetime(
        2026,
        9,
        27,
        12,
        0,
        tzinfo=location.timezone,
    )

    offset = longitude_time_offset(
        local_moment,
        location,
    )

    # Europe/Istanbul = UTC+3 in 2026.
    #
    # Timezone standard meridian:
    #
    # UTC+3 × 15° = 45°E
    #
    # Izmir:
    #
    # 27.1428°E
    #
    # Difference:
    #
    # 27.1428 - 45 = -17.8572°
    #
    # One degree = 4 minutes.
    #
    # Expected:
    #
    # -17.8572 × 4 = -71.4288 minutes.

    expected_seconds = -17.8572 * 4 * 60

    assert abs(
        offset.total_seconds() - expected_seconds
    ) < 0.01


def test_mean_solar_time_for_izmir():
    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    local_moment = datetime(
        2026,
        9,
        27,
        12,
        0,
        tzinfo=location.timezone,
    )

    solar_moment = mean_solar_time(
        local_moment,
        location,
    )

    # 12:00:00 local time
    # becomes approximately:
    #
    # 10:48:34.272 mean solar time.

    assert solar_moment.hour == 10
    assert solar_moment.minute == 48

    assert (
        abs(
            solar_moment.second
            + solar_moment.microsecond / 1_000_000
            - 34.272
        )
        < 0.001
    )


def test_mean_solar_time_requires_timezone_aware_datetime():
    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    naive_moment = datetime(
        2026,
        9,
        27,
        12,
        0,
    )

    with pytest.raises(ValueError):
        mean_solar_time(
            naive_moment,
            location,
        )


# ============================================================
# STANDARD MERIDIAN
# ============================================================


def test_izmir_standard_meridian_in_2026():
    from bazi_engine.solar_time import standard_meridian

    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    moment = datetime(
        2026,
        9,
        27,
        12,
        0,
        tzinfo=location.timezone,
    )

    assert standard_meridian(
        moment,
        location,
    ) == 45.0


def test_istanbul_timezone_offset_in_2026():
    from bazi_engine.solar_time import timezone_offset_at

    location = BirthLocation(
        city="Izmir",
        latitude=38.4237,
        longitude=27.1428,
        timezone_name="Europe/Istanbul",
    )

    moment = datetime(
        2026,
        9,
        27,
        12,
        0,
        tzinfo=location.timezone,
    )

    offset = timezone_offset_at(
        moment,
        location,
    )

    assert offset == timedelta(hours=3)
