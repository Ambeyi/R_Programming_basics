import unittest
import pandas as pd
from analysis import analyze,validate

def demo():
    return pd.DataFrame([['0-4','Suva','none',1,4],['0-4','Suva','lower',9,9],
                         ['5-9','rural','upper',10,30]],
                        columns=['duration','residence','education','nMother','nChildren'])

class GroupedTests(unittest.TestCase):
    def test_weighted_ratio(self):
        tables,s=analyze(demo())
        self.assertEqual(tables['duration'].iloc[0].children_per_mother,1.3)
        self.assertEqual(s['children_per_mother'],43/20)
    def test_totals_conserved(self):
        tables,s=analyze(demo())
        for key in ['duration','residence','education','duration_residence']:
            self.assertEqual(tables[key].mothers.sum(),s['mothers'])
            self.assertEqual(tables[key].children.sum(),s['children'])
    def test_missing_combinations(self):
        tables,s=analyze(demo())
        self.assertEqual(s['missing_cells'],69)
        self.assertEqual(len(tables['missing_cells']),69)
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):validate(pd.concat([demo(),demo().iloc[:1]]))
    def test_invalid_counts(self):
        for key,value in [('nMother',0),('nChildren',-1),('nChildren',1.2),('nMother',float('inf')),('education','unknown')]:
            d=demo();d[key]=d[key].astype(object);d.loc[0,key]=value
            with self.assertRaises(ValueError):validate(d)
    def test_zero_children_allowed(self):
        d=demo();d.nChildren=0
        self.assertEqual(analyze(d)[1]['children_per_mother'],0)
    def test_input_preserved(self):
        d=demo();before=d.copy();analyze(d)
        pd.testing.assert_frame_equal(d,before)

if __name__=='__main__':unittest.main()
