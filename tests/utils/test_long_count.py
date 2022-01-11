import pytest

from mayacal import LongCount, DistanceNumber
from mayacal.utils.utils import GregorianDate


@pytest.fixture
def example_long_count():
    return LongCount(9, 0, 0, 0, 3)


class TestLongCount:
    def test_get_calendar_round(self, example_long_count):
        calendar_round = example_long_count.get_calendar_round()

        assert (
            str(calendar_round) == "11 Akbal 16 Keh"
        ), "Incorrect calendar round conversion!"

    @pytest.mark.parametrize(
        "long_count,gregorian_date",
        [(LongCount(13, 0, 9, 3, 7), GregorianDate(10, 1, 2022))],
    )
    def test_to_gregorian(self, long_count, gregorian_date):
        converted_date = long_count.to_gregorian()

        assert isinstance(
            converted_date, GregorianDate
        ), "Conversion to gregorian did not return a GregorianDate!"

        assert (
            converted_date == gregorian_date
        ), "Incorrect conversion to Gregorian date"


class TestDistanceNumber:
    def test_add_distance_number_to_long_count(self, example_long_count):
        distance_number = DistanceNumber(LongCount(0, 0, 13, 2, 10), sign=1)
        result = example_long_count + distance_number

        assert str(result) == "9.0.13.2.13", "Incorrect addition of distance number!"
