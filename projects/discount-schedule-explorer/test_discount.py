import unittest
from discount import calculate

def flow(year=1,amount=110):return {"scenario":"A","year":year,"amount":amount}
class DiscountTests(unittest.TestCase):
    def test_known_value(self):self.assertAlmostEqual(calculate([flow()],.1)[1][0]["present_value"],100)
    def test_year_zero(self):self.assertEqual(calculate([flow(0)],.1)[1][0]["present_value"],110)
    def test_zero_rate(self):self.assertEqual(calculate([flow(),flow(2,-10)],0)[1][0]["present_value"],100)
    def test_fractional_year(self):self.assertAlmostEqual(calculate([flow(.5,121)],.21)[1][0]["present_value"],110)
    def test_negative_rate(self):self.assertAlmostEqual(calculate([flow(1,90)],-.1)[1][0]["present_value"],100)
    def test_invalid_rate(self):
        for rate in [-1,-2,float("nan"),float("inf")]:
            with self.assertRaises(ValueError):calculate([flow()],rate)
    def test_invalid_flow(self):
        for rows in [[],[{}],[flow(-1)],[flow(amount=float("nan"))]]:
            with self.assertRaises(ValueError):calculate(rows,0)
    def test_multiple_scenarios(self):
        b=flow();b["scenario"]="B";self.assertEqual(len(calculate([flow(),b],0)[1]),2)
if __name__=="__main__":unittest.main()
