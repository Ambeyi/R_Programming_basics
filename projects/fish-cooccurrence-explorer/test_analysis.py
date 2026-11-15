import unittest
import pandas as pd
from analysis import analyze

def demo():return pd.DataFrame({'Location':[1,2,3,4],'A':[1,1,0,0],'B':[0,1,1,0],'C':[0,0,0,1]})

class FishTests(unittest.TestCase):
    def test_known_distance(self):
        _,_,pairs,s=analyze(demo())
        self.assertAlmostEqual(pairs.iloc[0].jaccard_distance,2/3)
        self.assertEqual(s['disjoint_pairs'],2)
    def test_empty_species(self):
        d=demo();d['D']=0;d['E']=0
        _,_,pairs,s=analyze(d)
        self.assertEqual(s['absent_species'],2)
        self.assertEqual((pairs.status=='both_absent').sum(),1)
        self.assertTrue(pd.isna(pairs.iloc[-1].jaccard_distance))
    def test_conservation(self):
        p,r,_,s=analyze(demo())
        self.assertEqual(r.sites.sum(),s['sites'])
        self.assertEqual((r.species_per_site*r.sites).sum(),p.sites_present.sum())
    def test_identical_species(self):
        d=demo();d.B=d.A
        self.assertEqual(analyze(d)[2].iloc[0].jaccard_distance,0)
    def test_invalid(self):
        for value in [2,-1,.5,float('nan')]:
            d=demo().astype(float);d.loc[0,'A']=value
            with self.assertRaises(ValueError):analyze(d)
        d=demo();d.Location=1
        with self.assertRaises(ValueError):analyze(d)
    def test_row_order(self):
        pd.testing.assert_frame_equal(analyze(demo())[2],analyze(demo().iloc[::-1])[2])
    def test_set_based_reference(self):
        d=demo();pairs=analyze(d)[2]
        for row in pairs.itertuples():
            a=set(d.index[d[row.species_a]==1]);b=set(d.index[d[row.species_b]==1])
            self.assertAlmostEqual(row.jaccard_distance,1-len(a&b)/len(a|b))

if __name__=='__main__':unittest.main()
