import tempfile
import unittest
from pathlib import Path
import numpy as np
from analysis import compare
from data_io import read_samples

class ComparisonTests(unittest.TestCase):
    def test_known_welch_statistic(self):
        _,tests,s=compare([1,2,3],[4,5,6])
        self.assertAlmostEqual(tests[0]['statistic'],-3/(2/3)**.5)
        self.assertAlmostEqual(s['welch_df'],4)
        self.assertEqual(s['mean_difference'],-3)
    def test_pairwise_effect_with_ties(self):
        a,b=[1,2,2,5],[2,3,4]
        expected=sum((x>y)+.5*(x==y) for x in a for y in b)/(len(a)*len(b))
        _,_,s=compare(a,b)
        self.assertAlmostEqual(s['probability_superiority_a'],expected)
    def test_group_swap(self):
        a,b=[1,2,4,7],[3,4,6]
        _,t,s=compare(a,b);_,u,r=compare(b,a)
        self.assertAlmostEqual(s['mean_difference'],-r['mean_difference'])
        self.assertAlmostEqual(s['mean_difference_ci95_low'],-r['mean_difference_ci95_high'])
        for left,right in zip(t,u):self.assertAlmostEqual(left['p_value'],right['p_value'])
    def test_identical_samples(self):
        _,tests,s=compare([1,2,3,4],[1,2,3,4])
        self.assertEqual(s['mean_difference'],0)
        self.assertEqual(s['probability_superiority_a'],.5)
        self.assertEqual(tests[2]['statistic'],0)
    def test_invalid_samples(self):
        for a in [[],[1],[1,float('nan')],[1,float('inf')],[2,2],[[1,2],[3,4]]]:
            with self.assertRaises(ValueError):compare(a,[1,2,3])
    def test_csv_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.csv'
            p.write_text('group,value\nA,1\nB,2\n')
            self.assertEqual(read_samples(p),([1.],[2.]))
            for data in ['group,value\nC,1\n','group,value\nA,nan\n','group,value\nA,1,2\n']:
                p.write_text(data)
                with self.assertRaises(ValueError):read_samples(p)

if __name__=='__main__':unittest.main()
