import unittest
from activity import summarize

def row(date="9/1/2017 6:00",category=" Sports "):
    return {"Date":date,"Category":category,"ip":"SECRET","url":"PRIVATE"}
class ActivityTests(unittest.TestCase):
    def test_normalization(self):
        r,d,h,c=summarize([row(),row(category="sports")]);self.assertEqual(c,[{"category":"sports","events":2}]);self.assertEqual(h[6]["events"],2)
    def test_invalid_date(self):
        r,_,_,_=summarize([row("bad"),row()]);self.assertEqual(r["invalid_dates"],1)
    def test_missing_category(self):
        r,_,_,c=summarize([row(category="")]);self.assertEqual(r["missing_category_among_accepted"],1);self.assertEqual(c[0]["category"],"(missing)")
    def test_no_identifiers(self):
        output=str(summarize([row()]));self.assertNotIn("SECRET",output);self.assertNotIn("PRIVATE",output)
    def test_all_invalid(self):
        r,d,h,c=summarize([row("bad")]);self.assertIsNone(r["first_timestamp"]);self.assertEqual(d,[]);self.assertEqual(sum(x["events"] for x in h),0)
    def test_order(self):
        a=[row(),row("9/2/2017 7:00")];self.assertEqual(summarize(a),summarize(a[::-1]))
    def test_schema(self):
        for a in [[],[{}]]:
            with self.assertRaises(ValueError):summarize(a)
if __name__=="__main__":unittest.main()
