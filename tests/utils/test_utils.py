import pytest

from mayacal.utils.utils import (
    GregorianDate,
    JulianDate,
    julian_day_to_gregorian,
    julian_day_to_julian,
    _convert_julian_day,
)


class TestGregorianDate:
    def test_to_julian_day(self):
        gregorian_date = GregorianDate(10, 1, 2022)

        julian_day = gregorian_date.to_julian_day()

        assert (
            julian_day == 2459589.5
        ), "Incorrect conversion to from GregorianDate to Julian day!"


def test_julian_day_to_gregorian():
    result = julian_day_to_gregorian(2459589.5)

    assert isinstance(result, GregorianDate), "Result should be a GregorianDate object!"

    assert result == GregorianDate(
        10, 1, 2022
    ), "Incorrect conversion from Julian day number to JulianDate"


def test_julian_day_to_julian():
    result = julian_day_to_julian(2459590)

    assert isinstance(result, JulianDate), "Result should be a JuliianDate object!"

    assert result == JulianDate(
        28, 12, 2021
    ), "Incorrect conversion from Julian day number to JulianDate"


def test_convert_julian_day_in_julian_mode():
    day, month, year = _convert_julian_day(2459590, mode="julian")

    assert day == 28

    assert month == 12

    assert year == 2021


def test_convert_julian_day_in_gregorian_mode():
    day, month, year = _convert_julian_day(2459590, mode="gregorian")

    assert day == 10

    assert month == 1

    assert year == 2022
