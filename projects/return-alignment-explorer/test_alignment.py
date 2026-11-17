import math
import tempfile
import unittest
from datetime import date
from pathlib import Path
from alignment import load_prices, align, summarize

class AlignmentTests(unittest.TestCase):
    def load(self, content):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"input.csv"
            path.write_text(content)
            return load_prices(path)
    def test_invalid_prices(self):
        prices, audit = self.load("Date,Close\n2020-01-01,1\n2020-01-02,0\n2020-01-03,nan\nbad,2\n")
        self.assertEqual(len(prices), 1)
        self.assertEqual(audit["rejected_rows"], 3)
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            self.load("Date,Close\n2020-01-01,1\n2020-01-01,2\n")
    def test_schema(self):
        with self.assertRaises(ValueError): self.load("x,y\n1,2\n")
    def series(self):
        return {date(2020,1,d): v for d,v in [(1,1),(2,2),(3,8),(4,16)]}
    def test_shared_intervals(self):
        left = self.series(); right = left.copy(); del right[date(2020,1,2)]
        rows = align(left,right)
        self.assertEqual(rows[0]["days"], 2)
        self.assertAlmostEqual(rows[0]["left_return"], math.log(8))
        self.assertEqual(rows[0]["left_return"], rows[0]["right_return"])
    def test_insufficient_overlap(self):
        with self.assertRaises(ValueError): align(self.series(), {})
    def test_perfect_correlation(self):
        result = summarize(align(self.series(),self.series()))
        self.assertAlmostEqual(result["pearson_correlation"],1)
    def test_constant_returns(self):
        flat = {d: 5 for d in self.series()}
        self.assertIsNone(summarize(align(flat,flat))["pearson_correlation"])
    def test_order_independent(self):
        left = self.series()
        self.assertEqual(align(left,left),align(dict(reversed(list(left.items()))),left))

if __name__ == "__main__": unittest.main()
