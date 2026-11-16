import unittest
import numpy as np
import pandas as pd
from split import partition,audit

class SplitTests(unittest.TestCase):
    def test_counts(self):
        y=[0]*100+[1]*20;p=partition(y)
        self.assertEqual([len(x) for x in p.values()],[84,18,18])
        self.assertEqual([sum(np.array(y)[x]) for x in p.values()],[14,3,3])
    def test_disjoint_complete(self):
        p=partition([0]*101+[1]*21);a=list(p.values())
        self.assertEqual(len(set(np.concatenate(a))),122)
        self.assertEqual(sum(map(len,a)),122)
    def test_determinism(self):
        y=[0]*100+[1]*20
        np.testing.assert_array_equal(partition(y)['train'],partition(y)['train'])
        self.assertFalse(np.array_equal(partition(y,43)['train'],partition(y,44)['train']))
    def test_invalid_labels(self):
        for labels in [[],[0]*20,[0]*20+[1]*9,[0]*20+[1]*10+[2],[0]*20+[1]*10+[float('nan')]]:
            with self.assertRaises(ValueError):partition(labels)
    def test_duplicate_features(self):
        d=pd.DataFrame({'feature':[1]*40,'class':[0]*20+[1]*20})
        _,o,_,s=audit(d)
        self.assertTrue((o.shared_row_positions==0).all())
        self.assertTrue((o.shared_feature_hashes==1).all())
        self.assertEqual(s['duplicate_feature_rows'],39)
    def test_missing_features_retained(self):
        d=pd.DataFrame({'feature':[None]*40,'class':[0]*20+[1]*20})
        _,_,m,s=audit(d)
        self.assertEqual(m.set_index('column').loc['feature','missing_rows'],40)
        self.assertEqual(s['assigned_rows'],40)
    def test_rounding_remainder(self):
        p=partition([0]*11+[1]*11)
        self.assertEqual([len(x) for x in p.values()],[14,2,6])

if __name__=='__main__':unittest.main()
