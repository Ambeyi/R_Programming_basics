import unittest,tempfile
from pathlib import Path
from forecast import load_series,predict,evaluate
class ForecastTests(unittest.TestCase):
    def test_linear(self):
        p=predict([2,4,6,8]);self.assertEqual(p["drift"],10);self.assertEqual(p["linear_trend"],10)
    def test_flat(self):self.assertTrue(all(v==3 for v in predict([3,3,3]).values()))
    def test_no_future_leakage(self):
        a=[(2000+i,float(i)) for i in range(7)];b=a.copy();b[-1]=(2006,999)
        self.assertEqual(evaluate(a)[0][:6],evaluate(b)[0][:6])
        self.assertEqual([r["prediction"] for r in evaluate(a)[0]],[r["prediction"] for r in evaluate(b)[0]])
    def test_known_errors(self):
        _,m=evaluate([(2000+i,float(i)) for i in range(6)])
        last=next(r for r in m if r["model"]=="last_value")
        self.assertEqual(last["mae"],1);self.assertEqual(last["rmse"],1);self.assertEqual(last["mean_error"],-1)
    def test_window(self):
        for n in [1,4]:
            with self.assertRaises(ValueError):evaluate([(2000+i,i) for i in range(4)],n)
    def test_gaps_duplicates(self):
        for text in ["2000,1\n2002,2\n","2000,1\n2000,2\n"]:
            with tempfile.TemporaryDirectory() as t:
                p=Path(t)/"a.csv";p.write_text("Year,Birth Number\n"+text)
                with self.assertRaises(ValueError):load_series(p)
    def test_comma_and_sort(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/"a.csv";p.write_text('Year,Birth Number\n2001,"1,200"\n2000,1000\n')
            self.assertEqual(load_series(p),[(2000,1000),(2001,1200)])
    def test_nonfinite(self):
        with self.assertRaises(ValueError):predict([1,float("nan")])
if __name__=="__main__":unittest.main()
