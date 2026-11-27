import unittest
from reliability import alpha, analyse

SPEC = dict(name='demo', items=['a','b','c'], reverse=['c'], minimum=1, maximum=5)
ROWS = [dict(a=1,b=1,c=5),dict(a=2,b=2,c=4),dict(a=3,b=3,c=3)]

class ReliabilityTests(unittest.TestCase):
    def test_perfect_scale(self):
        summary, items = analyse(ROWS,SPEC)
        self.assertAlmostEqual(summary['alpha'],1)
        self.assertEqual(summary['mean_score'],2)
        self.assertTrue(all(abs(i['corrected_item_total']-1)<1e-12 for i in items))
    def test_listwise_missing(self):
        summary,_ = analyse(ROWS+[dict(a=1,b='',c=5)],SPEC)
        self.assertEqual((summary['complete_rows'],summary['excluded_rows']),(3,1))
    def test_constant(self):
        self.assertIsNone(alpha([[1,1],[1,1]]))
    def test_negative_alpha(self):
        self.assertLess(alpha([[1,4],[2,3],[3,1]]),0)
    def test_insufficient_cases(self):
        for rows in ([],ROWS[:1]):
            self.assertIsNone(analyse(rows,SPEC)[0]['alpha'])
    def test_invalid_values_even_in_incomplete_rows(self):
        for bad in ('nan','inf','word',0,6):
            with self.assertRaises(ValueError):
                analyse([dict(a='',b=bad,c=2)],SPEC)
    def test_invalid_configuration(self):
        for patch in (dict(items=['a','a']),dict(reverse=['z']),dict(minimum=5),dict(maximum=float('inf'))):
            with self.assertRaises(ValueError): analyse(ROWS,SPEC|patch)
    def test_two_item_deletion(self):
        _,items=analyse(ROWS,SPEC|dict(items=['a','b'],reverse=[]))
        self.assertTrue(all(i['alpha_if_deleted'] is None for i in items))
    def test_missing_column(self):
        with self.assertRaises(ValueError): analyse([dict(a=2,b=2)],SPEC)

if __name__ == '__main__': unittest.main()
