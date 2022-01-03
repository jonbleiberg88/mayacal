import mayacal as mc


class TestExampleSession:
    def test_basic_conversions_and_additions(self):

        # Get associated calendar round
        lc = mc.LongCount(9, 0, 0, 0, 0)
        calendar_round = lc.get_calendar_round()
        assert (
            str(calendar_round) == "8 Ajaw 13 Keh"
        ), "Incorrect calendar round conversion!"

        # Add a distance number
        dist = mc.DistanceNumber(mc.LongCount(0, 0, 13, 2, 10), sign=1)
        new_lc = lc + dist

        assert (
            str(new_lc) == "9.0.13.2.10"
        ), "Incorrect long count returned after addition of distance number!"

        # Get associated mayadate
        mayadate = new_lc.get_mayadate()
        assert (
            str(mayadate) == "9.0.13.2.10  6 Ok 18 Sak"
        ), "Incorrect mayadate for long count!"

        # Convert to Julian calendar
        julian_date = new_lc.to_julian()
        assert (
            str(julian_date) == "Nov 19, 448 CE"
        ), "Incorrect Julian date for long count!"

        # Convert to Gregorian calendar
        gregorian_date = new_lc.to_gregorian()
        assert (
            str(gregorian_date) == "Nov 20, 448 CE"
        ), "Incorrect Gregorian date for long count!"

    def test_inferring_long_count_dates_from_calendar_round(self):
        cr = mc.CalendarRound(mc.Tzolkin(6, "Ok"), mc.Haab(18, "Sak"))

        min_lc = mc.LongCount(9, 0, 0, 0, 0)
        max_lc = mc.LongCount(10, 0, 0, 0, 0)

        long_count_possibilities = cr.get_long_count_possibilities(min_lc, max_lc)

        possibilities_string = [str(lc) for lc in long_count_possibilities]
        expected_possibilities = [
            "9.0.13.2.10",
            "9.3.5.15.10",
            "9.5.18.10.10",
            "9.8.11.5.10",
            "9.11.4.0.10",
            "9.13.16.13.10",
            "9.16.9.8.10",
            "9.19.2.3.10",
        ]

        assert (
            possibilities_string == expected_possibilities
        ), "Incorrect long count possibilities returned!"

    def test_find_distance_between_long_count_dates(self):
        lc_1 = mc.LongCount(9, 12, 13, 0, 5)
        lc_2 = mc.LongCount(8, 0, 0, 0, 0)
        diff = lc_1 - lc_2

        assert str(diff) == "1.12.13.0.5", "Incorrect long count difference!"

        assert diff.get_total_kin() == 235085, "Incorrect conversion to number of kin!"

        assert (
            diff.to_approx_years(pretty_print=True) == "643 years, 7 months, 16 days"
        ), "Incorrect conversion to year month day form!"

    def test_infer_mayadate(self):
        cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), mc.Haab(8, "Kumku"))
        lc = mc.LongCount(9, 4, None, 10, None)

        date = mc.Mayadate(lc, cr)
        inferred_dates = date.infer_mayadates()

        assert len(inferred_dates) == 1, "Incorrect number of dates inferred!"
        assert (
            str(inferred_dates[0]) == "9.4.10.10.0  4 Ajaw 8 Kumku"
        ), "Incorrect date inferred!"

    def test_infer_mayadate_with_glyph_g(self):
        cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), mc.Haab(8, "Kumku"))
        lc = mc.LongCount(9, None, None, None, None)

        date = mc.Mayadate(lc, cr, glyph_g="G3")
        inferred_dates = date.infer_mayadates()

        assert len(inferred_dates) == 1, "Incorrect number of dates inferred!"
        assert (
            str(inferred_dates[0]) == "9.1.17.15.0  4 Ajaw 8 Kumku"
        ), "Incorrect date returned!"

    def test_infer_long_count_dates_from_mayadate(self):
        cr = mc.CalendarRound(mc.Tzolkin(4, "Ajaw"), haab=None)
        lc = mc.LongCount(10, None, 8, 10, None)

        date = mc.Mayadate(lc, cr)
        inferred_long_counts = date.infer_long_count_dates()

        assert (
            len(inferred_long_counts) == 2
        ), "Incorrect number of long counts inferred!"

        inferred_long_counts_str = [str(lc) for lc in inferred_long_counts]
        assert inferred_long_counts_str == [
            "10.1.8.10.0",
            "10.14.8.10.0",
        ], "Incorrect long counts returned!"
