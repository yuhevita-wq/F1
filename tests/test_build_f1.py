"""Offline tests: no network, no race-data assumptions."""
import unittest
from scripts.build_f1 import eligible, load_manifest


class FilterTests(unittest.TestCase):
    def setUp(self):
        self.a = {"id": "A-test", "class": "A",
                  "start_date": "2025-01-01", "end_date": "2025-02-28"}
        self.s = {"id": "S-test", "class": "S",
                  "start_date": "2025-01-01", "end_date": "2025-03-31"}
        self.race = {
            "race_id": "x20250101", "race_date": "2025-01-01",
            "meeting_grade": "F1", "race_type": "Ａ級予選",
            "class_scope": "A1/A2"
        }

    def test_a_f1_is_kept(self):
        self.assertTrue(eligible(self.race, self.a))

    def test_a_f2_is_dropped(self):
        self.assertFalse(eligible({**self.race, "meeting_grade": "F2"}, self.a))

    def test_fullwidth_grade_is_normalized(self):
        self.assertTrue(eligible({**self.race, "meeting_grade": "Ｆ１"}, self.a))

    def test_s_f1_is_kept(self):
        s_race = {**self.race, "race_type": "Ｓ級準決勝"}
        self.assertTrue(eligible(s_race, self.s))

    def test_s_non_f1_is_rejected(self):
        with self.assertRaises(ValueError):
            eligible({**self.race, "race_type": "Ｓ級一般",
                      "meeting_grade": "F2"}, self.s)

    def test_a3_is_rejected(self):
        with self.assertRaises(ValueError):
            eligible({**self.race, "class_scope": "A3"}, self.a)

    def test_outside_period_is_rejected(self):
        with self.assertRaises(ValueError):
            eligible({**self.race, "race_date": "2024-12-31"}, self.a)

    def test_manifest_is_fixed_and_disjoint(self):
        m = load_manifest()
        self.assertEqual(len(m["sources"]), 17)
        self.assertEqual(
            {(s["year"], s["class"]) for s in m["sources"]},
            {(2025, "A"), (2025, "S"), (2026, "A"), (2026, "S")})
        self.assertEqual(len(m["source_ref"]), 40)


if __name__ == "__main__":
    unittest.main()
