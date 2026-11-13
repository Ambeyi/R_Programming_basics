import unittest
import numpy as np
from model import fit,predict
from evaluation import leave_one_out

class RegressionTests(unittest.TestCase):
    def test_known_line(self):
        m=fit([0,1,2,3,4],[1,3,5,7,9])
        self.assertEqual(m['slope'],2);self.assertEqual(m['intercept'],1)
        self.assertEqual(predict(m,7)['predicted_score'],15)
    def test_interval_widths(self):
        m=fit([1,2,3,4,5],[2,5,5,9,8]);p=predict(m,3)
        self.assertLess(p['prediction95_low'],p['mean_ci95_low'])
        self.assertGreater(p['prediction95_high'],p['mean_ci95_high'])
    def test_independent_lstsq(self):
        x=np.arange(8.);y=np.array([2,5,4,8,11,10,13,16])
        b=np.linalg.lstsq(np.column_stack([np.ones(8),x]),y,rcond=None)[0]
        m=fit(x,y)
        np.testing.assert_allclose([m['intercept'],m['slope']],b)
    def test_perfect_validation(self):
        self.assertAlmostEqual(leave_one_out(range(6),[2,5,8,11,14,17])['rmse'],0)
    def test_extrapolation(self):
        m=fit([1,2,3,4],[2,3,5,6])
        self.assertTrue(predict(m,7)['extrapolation']);self.assertFalse(predict(m,1)['extrapolation'])
    def test_invalid(self):
        for x,y in [([1]*4,[1,2,3,4]),([1,2],[2,3]),([1,2,3,float('nan')],[2,3,4,5])]:
            with self.assertRaises(ValueError):fit(x,y)
    def test_constant_outcome(self):
        m=fit([1,2,3,4],[5,5,5,5])
        self.assertIsNone(m['r_squared']);self.assertEqual(m['slope'],0)

if __name__=='__main__':unittest.main()
