import unittest
import pandas as pd
from analyze import analyze
class Tests(unittest.TestCase):
 def setUp(self): self.d=pd.DataFrame({'Year':[2000]*12,'Month':range(1,13),'Value':range(1,13)})
 def test_complete_mean(self):
  a,s,m=analyze(self.d);self.assertEqual(a.iloc[0]['mean'],6.5);self.assertEqual(m['complete_years'],1)
 def test_partial(self): self.assertEqual(analyze(self.d.iloc[:11])[2]['incomplete_years'],1)
 def test_duplicate(self):
  with self.assertRaises(ValueError): analyze(pd.concat([self.d,self.d]))
 def test_invalid(self):
  for col,val in [('Month',13),('Year',2000.5),('Value',float('inf'))]:
   d=self.d.astype(float);d.loc[0,col]=val
   with self.assertRaises(ValueError): analyze(d)
if __name__=='__main__': unittest.main()
