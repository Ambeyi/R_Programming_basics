import unittest
from resolver import prepare,resolve

def mapping(current="North",start="2000-01-01",end="2009-12-31"):
    return {"current":current,"former":"Old","start_date":start,"end_date":end}
class ResolverTests(unittest.TestCase):
    def test_boundaries(self):
        r=prepare([mapping()])
        for d in ["2000-01-01","2009-12-31"]:self.assertEqual(resolve("Old",d,r)["canonical"],"North")
    def test_outside(self):self.assertEqual(resolve("Old","2010-01-01",prepare([mapping()]))["status"],"unmatched")
    def test_ambiguous(self):self.assertEqual(resolve("Old","2001-01-01",prepare([mapping(),mapping("South")]))["status"],"ambiguous")
    def test_duplicate_same_target(self):self.assertEqual(resolve("Old","2001-01-01",prepare([mapping(),mapping()]))["candidate_count"],1)
    def test_case_sensitive(self):self.assertEqual(resolve("old","2001-01-01",prepare([mapping()]))["status"],"unmatched")
    def test_invalid_interval(self):
        with self.assertRaises(ValueError):prepare([mapping(start="2010-01-01")])
    def test_invalid_date(self):
        with self.assertRaises(ValueError):resolve("Old","2001-02-30",[])
    def test_trim(self):self.assertEqual(resolve(" Old ","2001-01-01",prepare([mapping()]))["status"],"matched")
if __name__=="__main__":unittest.main()
