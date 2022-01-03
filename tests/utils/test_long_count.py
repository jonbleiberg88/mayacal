import pytest

from mayacal import LongCount, DistanceNumber


@pytest.fixture
def example_long_count():
    return LongCount(9, 0, 0, 0, 3)


class TestLongCount:
    def test_get_calendar_round(self, example_long_count):
        calendar_round = example_long_count.get_calendar_round()

        assert (
            str(calendar_round) == "11 Akbal 16 Keh"
        ), "Incorrect calendar round conversion!"


class TestDistanceNumber:
    def test_add_distance_number_to_long_count(self, example_long_count):
        distance_number = DistanceNumber(LongCount(0, 0, 13, 2, 10), sign=1)
        result = example_long_count + distance_number

        assert str(result) == "9.0.13.2.13", "Incorrect addition of distance number!"
