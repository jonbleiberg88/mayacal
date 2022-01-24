from calendar import day_name
import pytest

from mayacal import Tzolkin


class TestTzolkin:
    def test_constructor_without_number(self):
        tzolkin = Tzolkin(2, "Ik")

        assert tzolkin.day_name == "Ik"
        assert tzolkin.day_number == 2
        assert tzolkin.tzolkin_num == 1

    def test_constructor_with_just_number(self):
        tzolkin = Tzolkin(tzolkin_num=24)

        assert tzolkin.tzolkin_num == 24
        assert tzolkin.day_name == "Chikchan"
        assert tzolkin.day_number == 12

    def test_constructor_with_invalid_day_name(self):
        day_number, day_name = 12, "Monday"
        with pytest.raises(ValueError) as exception:
            Tzolkin(day_number, day_name)
            assert str(exception) == f"Invalid tzolkin day name {day_name}"

    def test_constructor_with_invalid_day_number(self):
        day_number, day_name = 44, "Imix"
        with pytest.raises(ValueError) as exception:
            Tzolkin(day_number, day_name)
            assert (
                str(exception)
                == "Invalid tzolkin day number - must be integer between 1 and 13"
            )

    def test_constructor_with_valid_combination(self):
        day_number, day_name, tzolkin_number = 12, "Chikchan", 24
        tzolkin = Tzolkin(day_number, day_name, tzolkin_number)

        assert tzolkin.tzolkin_num == tzolkin_number
        assert tzolkin.day_name == day_name
        assert tzolkin.day_number == day_number

    def test_constructor_with_invalid_combination(self):
        day_number, day_name, tzolkin_number = 12, "Chikchan", 43

        with pytest.raises(ValueError) as exception:
            Tzolkin(day_number, day_name, tzolkin_number)

            assert (
                str(exception)
                == f"Provided Tzolkin number {tzolkin_number} does not match provided day name and number {day_number} {day_name}"
            )

    @pytest.mark.parametrize(
        "tzolkin_num,expected_day,expected_day_number",
        [
            (24, "Chikchan", 12),
            (259, "Ajaw", 13),
            (0, "Imix", 1),
            (125, "Kimi", 9),
            (214, "Men", 7),
        ],
    )
    def test_reset_by_tzolkin_num(self, tzolkin_num, expected_day, expected_day_number):
        tzolkin = Tzolkin(1, "Imix")

        tzolkin.reset_by_tzolkin_num(tzolkin_num)

        assert tzolkin.day_name == expected_day
        assert tzolkin.day_number == expected_day_number

    @pytest.mark.parametrize(
        "days_to_add,initial_day_number,initial_day,expected_day_number,expected_day",
        [
            (24, 1, "Imix", 12, "Chikchan"),
            (100, 3, "Ok", 12, "Ok"),
            (12, 2, "Lamat", 1, "Ajaw"),
        ],
    )
    def test_add_days(
        self,
        days_to_add,
        initial_day_number,
        initial_day,
        expected_day_number,
        expected_day,
    ):
        initial_tzolkin = Tzolkin(initial_day_number, initial_day)

        result = initial_tzolkin.add_days(days_to_add)

        assert isinstance(result, Tzolkin)
        assert initial_tzolkin.day_number == initial_day_number
        assert initial_tzolkin.day_name == initial_day

        assert result.day_number == expected_day_number
        assert result.day_name == expected_day

        # Test in place addition
        return_value = initial_tzolkin.add_days(days_to_add, in_place=True)

        assert return_value is initial_tzolkin
        assert initial_tzolkin.day_number == expected_day_number
        assert initial_tzolkin.day_name == expected_day

    @pytest.mark.parametrize(
        "day_number,day_name,expected",
        [
            (2, "Imix", False),
            (None, "Imix", True),
            (2, None, True),
            (None, None, True),
        ],
    )
    def test_has_missing(self, day_number, day_name, expected):
        tzolkin = Tzolkin(day_number, day_name)

        assert tzolkin.has_missing() == expected

    @pytest.mark.parametrize(
        "tzolkin1,tzolkin2,expected",
        [
            (Tzolkin(2, "Imix"), Tzolkin(2, "Imix"), True),
            (Tzolkin(2, "Imix"), Tzolkin(2, None), True),
            (Tzolkin(2, "Imix"), Tzolkin(None, "Imix"), True),
            (Tzolkin(2, "Imix"), Tzolkin(None, None), True),
            (Tzolkin(2, None), Tzolkin(None, None), True),
            (Tzolkin(2, None), Tzolkin(None, "Chikchan"), True),
            (Tzolkin(2, "Imix"), Tzolkin(None, "Chikchan"), False),
            (Tzolkin(2, "Imix"), Tzolkin(5, "Chikchan"), False),
        ],
    )
    def test_match(self, tzolkin1, tzolkin2, expected):
        assert tzolkin1.match(tzolkin2) == expected
        assert tzolkin2.match(tzolkin1) == expected

    @pytest.mark.parametrize(
        "tzolkin,expected_dict",
        [
            (Tzolkin(2, "Imix"), {"day_number": 2, "day_name": "Imix"}),
            (Tzolkin(None, "Imix"), {"day_number": None, "day_name": "Imix"}),
            (Tzolkin(10, None), {"day_number": 10, "day_name": None}),
            (Tzolkin(3, "Manik"), {"day_number": 3, "day_name": "Manik"}),
            (Tzolkin(None, None), {"day_number": None, "day_name": None}),
        ],
    )
    def test_to_dict(self, tzolkin, expected_dict):

        tzolkin_dict = tzolkin.to_dict()
        assert isinstance(tzolkin_dict, dict)
        assert tzolkin_dict == expected_dict

    @pytest.mark.parametrize(
        "tzolkin1,tzolkin2,expected",
        [
            (Tzolkin(2, "Imix"), Tzolkin(2, "Imix"), True),
            (Tzolkin(2, "Imix"), Tzolkin(2, None), False),
            (Tzolkin(2, "Imix"), Tzolkin(None, "Imix"), False),
            (Tzolkin(2, "Imix"), Tzolkin(None, None), False),
            (Tzolkin(2, None), Tzolkin(None, None), False),
            (Tzolkin(2, None), Tzolkin(None, "Chikchan"), False),
            (Tzolkin(2, "Imix"), Tzolkin(None, "Chikchan"), False),
            (Tzolkin(2, "Imix"), Tzolkin(5, "Chikchan"), False),
            (Tzolkin(2, None), Tzolkin(2, None), True),
            (Tzolkin(None, None), Tzolkin(None, None), True),
            (Tzolkin(None, "Manik"), Tzolkin(None, "Manik"), True),
        ],
    )
    def test_eq(self, tzolkin1, tzolkin2, expected):

        test_result = tzolkin1 == tzolkin2
        assert test_result == expected

        test_result_2 = tzolkin2 == tzolkin1
        assert test_result_2 == expected

    @pytest.mark.parametrize(
        "tzolkin1,tzolkin2,expected",
        [
            (Tzolkin(2, "Imix"), Tzolkin(2, "Imix"), 0),
            (Tzolkin(3, "Ik"), Tzolkin(11, "Kan"), 18),
            (Tzolkin(10, "Chuwen"), Tzolkin(7, "Kawak"), 172),
        ],
    )
    def test_sub(self, tzolkin1, tzolkin2, expected):

        test_result = tzolkin1 - tzolkin2
        assert test_result == expected
