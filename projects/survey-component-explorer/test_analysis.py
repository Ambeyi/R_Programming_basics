import unittest
import numpy as np
import pandas as pd
from analysis import analyze,ITEMS

def sample():return pd.DataFrame(np.random.default_rng(42).integers(1,6,(80,28)),columns=ITEMS)

class ComponentTests(unittest.TestCase):
    def test_variance_accounting(self):
        _,s,_,_=analyze(sample())
        self.assertAlmostEqual(s.eigenvalue.sum(),28)
        self.assertAlmostEqual(s.explained_ratio.sum(),1)
        self.assertTrue((np.diff(s.eigenvalue)<=0).all())
    def test_independent_svd(self):
        d=sample();z=(d-d.mean())/d.std(ddof=1)
        expected=np.linalg.svd(z,compute_uv=False)**2/(len(d)-1)
        np.testing.assert_allclose(analyze(d)[1].eigenvalue,expected,atol=1e-12)
    def test_identical_items(self):
        d=pd.DataFrame(np.tile(np.arange(1,6),(28,1)).T,columns=ITEMS)
        _,s,_,summary=analyze(d)
        self.assertAlmostEqual(s.iloc[0].explained_ratio,1)
        self.assertEqual(summary['components_for_80_percent'],1)
    def test_invalid_ratings(self):
        for value in [0,6,1.5,float('nan')]:
            d=sample().astype(float);d.iloc[0,0]=value
            with self.assertRaises(ValueError):analyze(d)
    def test_constant_item(self):
        d=sample();d.Q1=3
        with self.assertRaises(ValueError):analyze(d)
    def test_row_order_invariance(self):
        d=sample();a=analyze(d);b=analyze(d.iloc[::-1])
        np.testing.assert_allclose(a[1].eigenvalue,b[1].eigenvalue,atol=1e-12)
    def test_item_summary(self):
        d=sample();items,_,_,_=analyze(d)
        self.assertAlmostEqual(items.iloc[0]['mean'],sum(d.Q1)/len(d))

if __name__=='__main__':unittest.main()
