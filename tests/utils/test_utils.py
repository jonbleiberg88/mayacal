import pytest

from mayacal import LongCount, Mayadate
from mayacal.utils.utils import (
    GregorianDate,
    JulianDate,
    julian_day_to_gregorian,
    julian_day_to_julian,
    _convert_julian_day,
)


class TestGregorianDate:
    @pytest.mark.parametrize(
        "gregorian_date, expected_julian_day",
        [
            (GregorianDate(10, 1, 2022), 2459589.5),
            (GregorianDate(11, 1, 2022), 2459590.5),
            (GregorianDate(22, 3, 683), 1970600.5),
            (GregorianDate(10, 8, 234), 1806747.5),
            (GregorianDate(18, 1, 2022), 2459597.5),
            (GregorianDate(19, 1, 2022), 2459598.5),
        ],
    )
    def test_to_julian_day(self, gregorian_date, expected_julian_day):
        julian_day = gregorian_date.to_julian_day()

        assert (
            julian_day == expected_julian_day
        ), "Incorrect conversion to from GregorianDate to Julian day!"

    @pytest.mark.parametrize(
        "gregorian_date, expected_long_count",
        [
            (GregorianDate(10, 1, 2022), LongCount(13, 0, 9, 3, 7)),
            (GregorianDate(11, 1, 2022), LongCount(13, 0, 9, 3, 8)),
            (GregorianDate(22, 3, 683), LongCount(9, 12, 10, 15, 18)),
            (GregorianDate(10, 8, 234), LongCount(8, 9, 15, 13, 5)),
            (GregorianDate(18, 1, 2022), LongCount(13, 0, 9, 3, 15)),
            (GregorianDate(19, 1, 2022), LongCount(13, 0, 9, 3, 16)),
        ],
    )
    def test_to_mayadate(self, gregorian_date, expected_long_count):

        result = gregorian_date.to_mayadate()

        assert isinstance(result, Mayadate)
        assert result.long_count == expected_long_count

    @pytest.mark.parametrize(
        "gregorian_date, expected_julian_date",
        [
            (GregorianDate(17, 7, 1578), JulianDate(7, 7, 1578)),
            (GregorianDate(24, 10, 232), JulianDate(24, 10, 232)),
            (GregorianDate(19, 1, 2022), JulianDate(6, 1, 2022)),
        ],
    )
    def test_to_julian(self, gregorian_date, expected_julian_date):
        result = gregorian_date.to_julian()
        assert result == expected_julian_date


class TestJulianDate:
    @pytest.mark.parametrize(
        "julian_date, expected_julian_day",
        [
            (JulianDate(19, 3, 427), 1877096.5),
            (JulianDate(20, 3, 427), 1877097.5),
            (JulianDate(3, 6, 1658), 2326795.5),
            (JulianDate(10, 2, 1812), 2382930.5),
            (JulianDate(22, 3, 53), 1740496.5),
            (JulianDate(31, 8, 182), 1787775.5),
            (JulianDate(22, 1, 2022), 2459614.5),
        ],
    )
    def test_to_julian_day(self, julian_date, expected_julian_day):
        julian_day = julian_date.to_julian_day()

        assert (
            julian_day == expected_julian_day
        ), "Incorrect conversion to from JulianDate to Julian day!"

    @pytest.mark.parametrize(
        "julian_date, expected_long_count",
        [
            (JulianDate(9, 1, 2022), LongCount(13, 0, 9, 3, 19)),
            (JulianDate(10, 1, 2022), LongCount(13, 0, 9, 4, 0)),
            (JulianDate(8, 9, 218), LongCount(8, 8, 19, 10, 10)),
            (JulianDate(31, 7, 54), LongCount(8, 0, 13, 1, 10)),
            (JulianDate(7, 11, 1693), LongCount(12, 3, 16, 4, 14)),
            (JulianDate(8, 11, 1693), LongCount(12, 3, 16, 4, 15)),
        ],
    )
    def test_to_mayadate(self, julian_date, expected_long_count):

        result = julian_date.to_mayadate()

        assert isinstance(result, Mayadate)
        assert result.long_count == expected_long_count

    @pytest.mark.parametrize(
        "julian_date, expected_gregorian_date",
        [
            (JulianDate(8, 5, 234), GregorianDate(8, 5, 234)),
            (JulianDate(21, 3, 692), GregorianDate(24, 3, 692)),
            (JulianDate(9, 1, 2022), GregorianDate(22, 1, 2022)),
        ],
    )
    def test_to_gregorian(self, julian_date, expected_gregorian_date):
        result = julian_date.to_gregorian()
        assert result == expected_gregorian_date


@pytest.mark.parametrize(
    "julian_day, gregorian_date",
    [
        (2459589.5, GregorianDate(10, 1, 2022)),
        (1970601, GregorianDate(22, 3, 683)),
        (1806748, GregorianDate(10, 8, 234)),
    ],
)
def test_julian_day_to_gregorian(julian_day, gregorian_date):
    result = julian_day_to_gregorian(julian_day)

    assert isinstance(result, GregorianDate), "Result should be a GregorianDate object!"

    assert (
        result == gregorian_date
    ), "Incorrect conversion from Julian day number to JulianDate"


@pytest.mark.parametrize(
    "julian_day, julian_date",
    [
        (2459590, JulianDate(28, 12, 2021)),
        (1821972, JulianDate(15, 4, 276)),
        (2179346, JulianDate(22, 9, 1254)),
    ],
)
def test_julian_day_to_julian(julian_day, julian_date):
    result = julian_day_to_julian(julian_day)

    assert isinstance(result, JulianDate), "Result should be a JuliianDate object!"

    assert (
        result == julian_date
    ), "Incorrect conversion from Julian day number to JulianDate"


@pytest.mark.parametrize(
    "mode, julian_day, expected_day, expected_month, expected_year",
    [("julian", 2459590, 28, 12, 2021), ("gregorian", 2459590, 10, 1, 2022)],
)
def test_convert_julian_day(
    mode, julian_day, expected_day, expected_month, expected_year
):
    day, month, year = _convert_julian_day(julian_day, mode=mode)

    assert day == expected_day

    assert month == expected_month

    assert year == expected_year
