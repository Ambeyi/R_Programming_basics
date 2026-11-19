import unittest
from coverage import audit

def row(y="2020",v="2",c="X",i="A"):
    return {"Country Code":c,"Indicator Code":i,"Year":y,"Value":v}
class CoverageTests(unittest.TestCase):
    def test_gap(self):
        s,g,_,_,_=audit([row(),row("2022")])
        self.assertEqual(g,[{"country":"X","indicator":"A","year":2021}])
        self.assertAlmostEqual(s[0]["coverage_percent"],200/3)
    def test_duplicate(self):
        s,_,d,_,r=audit([row(),row(v="3")])
        self.assertEqual(s[0]["valid_years"],1);self.assertEqual(d[0]["rows"],2)
        self.assertEqual(r["duplicate_rows_beyond_first"],1)
    def test_invalid_values(self):
        for v in ["", "nan", "inf", "bad"]:
            s,_,_,_,r=audit([row(v=v)])
            self.assertEqual(r["rejected_rows"],1);self.assertIsNone(s[0]["first_year"])
    def test_invalid_year(self):
        for y in ["2020.5","0","10000",""]:
            self.assertEqual(audit([row(y=y)])[4]["rejected_rows"],1)
    def test_country_separation(self):
        self.assertEqual(audit([row(),row(c="Y")])[4]["series"],2)
    def test_empty_schema(self):
        for data in [[],[{}]]:
            with self.assertRaises(ValueError):audit(data)
    def test_missing_key(self):
        self.assertEqual(audit([row(c=" ")])[4]["rejection_reasons"],{"missing_key":1})
    def test_order(self):
        data=[row("2022"),row(),row("2021")]
        self.assertEqual(audit(data),audit(data[::-1]))
if __name__=="__main__":unittest.main()
