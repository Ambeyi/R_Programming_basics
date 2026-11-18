import unittest
from preferences import ATTRIBUTES, analyze

def row(value=4): return dict.fromkeys(ATTRIBUTES,value)

class PreferenceTests(unittest.TestCase):
    def test_empty(self):
        with self.assertRaises(ValueError): analyze([])
    def test_schema(self):
        with self.assertRaises(ValueError): analyze([{}])
    def test_ties(self):
        summary, _, audit = analyze([row()])
        self.assertEqual(audit["complete_responses_with_tied_top"],1)
        self.assertTrue(all(r["top_choice_count"]==1 for r in summary))
    def test_missing(self):
        r = row(); r["imp_price"] = ""
        summary, _, audit = analyze([r])
        price = next(x for x in summary if x["attribute"]=="imp_price")
        self.assertIsNone(price["mean"])
        self.assertEqual(price["missing"],1)
        self.assertEqual(audit["complete_responses"],0)
    def test_invalid(self):
        for value in [0,8,2.5,"nan","inf","bad"]:
            r = row(); r["imp_price"] = value
            summary,_,_ = analyze([r])
            self.assertEqual(next(x for x in summary if x["attribute"]=="imp_price")["invalid"],1)
    def test_mean_and_distribution(self):
        summary, distribution, _ = analyze([row(1),row(7)])
        self.assertTrue(all(x["mean"]==4 and x["median"]==4 for x in summary))
        self.assertEqual(sum(x["count"] for x in distribution),14)
    def test_top_choice(self):
        r=row();r["imp_taste"]=7
        summary,_,audit=analyze([r])
        self.assertEqual(summary[0]["attribute"],"imp_taste")
        self.assertEqual(summary[0]["top_choice_percent"],100)
        self.assertEqual(audit["complete_responses_with_tied_top"],0)

if __name__ == "__main__": unittest.main()
