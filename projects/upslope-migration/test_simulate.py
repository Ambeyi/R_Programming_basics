import unittest
from simulate import shift,simulate
class Tests(unittest.TestCase):
 def test_shift(self):
  grid=[[1,0],[0,1]];self.assertEqual(shift(grid),[[0,1],[0,0]]);self.assertEqual(grid,[[1,0],[0,1]])
 def test_no_migration(self):
  h=simulate(probability=0);self.assertEqual(h[0]['occupied'],h[-1]['occupied'])
 def test_boundary_loss(self):
  h=simulate(rows=3,cols=4,years=3,probability=1);self.assertEqual(h[-1]['occupied'],0)
  self.assertEqual(sum(r['lost_cells'] for r in h),h[0]['occupied'])
 def test_reproducible(self): self.assertEqual(simulate(),simulate())
 def test_invalid(self):
  with self.assertRaises(ValueError): simulate(probability=2)
  with self.assertRaises(ValueError): shift([[1],[0,1]])
if __name__=='__main__': unittest.main()
