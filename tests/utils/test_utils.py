import pytest

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
            (GregorianDate(22, 3, 683), 1970600.5),
            (GregorianDate(10, 8, 234), 1806747.5),
            (GregorianDate(19, 1, 2022), 2459599),
        ],
    )
    def test_to_julian_day(self, gregorian_date, expected_julian_day):
        julian_day = gregorian_date.to_julian_day()

        assert (
            julian_day == expected_julian_day
        ), "Incorrect conversion to from GregorianDate to Julian day!"


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
