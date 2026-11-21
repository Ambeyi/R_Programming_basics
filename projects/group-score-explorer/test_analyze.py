import unittest
from analyze import summarize
class GroupTests(unittest.TestCase):
    def test_known_summary(self):
        s,_=summarize([{"group":"A","y":v} for v in [1,2,3]])
        self.assertEqual((s[0]["mean"],s[0]["median"],s[0]["sample_sd"]),(2,2,1))
    def test_difference_direction(self):
        _,p=summarize([{"group":"B","y":5},{"group":"A","y":2}])
        self.assertEqual(p,[{"group_a":"A","group_b":"B","mean_a_minus_b":-3}])
    def test_singleton(self):
        s,p=summarize([{"group":"A","y":1}]);self.assertIsNone(s[0]["sample_sd"]);self.assertEqual(p,[])
    def test_invalid(self):
        for value in ["nan","inf","bad",""]:
            with self.assertRaises(ValueError):summarize([{"group":"A","y":value}])
    def test_schema_and_empty(self):
        for data in [[],[{}],[{"group":" ","y":1}]]:
            with self.assertRaises(ValueError):summarize(data)
    def test_order(self):
        rows=[{"group":"B","y":2},{"group":"A","y":4},{"group":"B","y":6}]
        self.assertEqual(summarize(rows),summarize(rows[::-1]))
if __name__=="__main__":unittest.main()
