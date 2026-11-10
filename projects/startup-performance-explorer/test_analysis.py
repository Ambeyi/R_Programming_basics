import unittest
import pandas as pd
from analysis import analyze,validate,NUMERIC

def sample():
    d=pd.DataFrame({name:[10,20,30] for name in NUMERIC})
    d['City']=['A','A','B'];d['StartYear']=[2005,2005,2006];d['IsSuccessful']=[1,0,1]
    return d

class StartupTests(unittest.TestCase):
    def test_known_groups(self):
        city,cohort,corr,s=analyze(sample())
        a=city.set_index('City').loc['A']
        self.assertEqual(a['mean_profit'],15);self.assertEqual(a['success_rate'],.5)
        self.assertEqual(s['successes'],2);self.assertEqual(s['records'],3)
        self.assertEqual(cohort['records'].sum(),3)
        self.assertAlmostEqual(corr.iloc[0].pearson_r,1)
    def test_conservation(self):
        city,cohort,_,_=analyze(sample())
        for table in [city,cohort]:
            self.assertEqual(table.total_profit.sum(),60)
            self.assertEqual(table.total_sales.sum(),60)
            self.assertEqual(table.successes.sum(),2)
    def test_constant_correlation(self):
        d=sample();d['Equipment']=1
        _,_,corr,_=analyze(d)
        self.assertEqual(corr.iloc[0]['status'],'constant_or_insufficient')
        self.assertTrue(pd.isna(corr.iloc[0].pearson_r))
    def test_losses_supported(self):
        d=sample();d.loc[0,'Profit']=-10
        self.assertEqual(validate(d).Profit.sum(),40)
    def test_invalid_fields(self):
        for field,value in [('City',' '),('StartYear',2005.5),('IsSuccessful',2),('Sales',-1),('Profit',float('inf')),('Website',None)]:
            d=sample();d[field]=d[field].astype(object);d.loc[0,field]=value
            with self.assertRaises(ValueError):validate(d)
        with self.assertRaises(ValueError):validate(sample().drop(columns='City'))
    def test_input_unchanged(self):
        d=sample();before=d.copy(deep=True);analyze(d)
        pd.testing.assert_frame_equal(d,before)

if __name__=='__main__':unittest.main()
