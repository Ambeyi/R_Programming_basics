import unittest
import pandas as pd
from analyze import analyze,C
class Tests(unittest.TestCase):
 def setUp(self): self.d=pd.DataFrame([[1,'Standard',4,3],[1,'Standard',4,3],[2,'Standard',2,3]],columns=C)
 def test_order_denominator(self):
  s,d,m=analyze(self.d);self.assertEqual(m['unique_orders'],2);self.assertEqual(s.iloc[0].over_schedule_rate,.5);self.assertEqual(d.sum(),2)
 def test_conflict(self):
  self.d.iloc[1,2]=5
  with self.assertRaises(ValueError): analyze(self.d)
 def test_missing(self):
  self.d.iloc[0,2]=None
  with self.assertRaises(ValueError): analyze(self.d)
 def test_negative(self):
  self.d.iloc[0,2]=-1
  with self.assertRaises(ValueError): analyze(self.d)
if __name__=='__main__': unittest.main()
