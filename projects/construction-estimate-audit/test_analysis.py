"""Tests use clearly synthetic data, not the source workbook."""
import unittest
import numpy as np
import pandas as pd
from analyze import analyze

class AuditTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        self.df = pd.DataFrame({
            'Material_Cost': rng.integers(10000, 50000, 30),
            'Labor_Cost': rng.integers(5000, 30000, 30),
            'Profit_Rate': rng.choice([10,15,20,25,30],30),
            'Discount_or_Markup': rng.integers(-10000,10000,30)})
        d = self.df
        d['Total_Estimate'] = (d.Material_Cost+d.Labor_Cost)*(1+d.Profit_Rate/100)+d.Discount_or_Markup
    def test_formula_and_modified_total(self):
        self.assertEqual(analyze(self.df)['formula_rows_within_one_cent'], 30)
        self.df.loc[0,'Total_Estimate'] += 100
        result = analyze(self.df)
        self.assertEqual(result['formula_rows_within_one_cent'], 29)
        self.assertAlmostEqual(result['formula_max_absolute_error'],100)
    def test_known_additive_model(self):
        d = self.df
        d['Total_Estimate'] = 7+2*d.Material_Cost+3*d.Labor_Cost+4*d.Profit_Rate+5*d.Discount_or_Markup
        np.testing.assert_allclose(list(analyze(d)['additive_ols_coefficients'].values()), [7,2,3,4,5], atol=1e-7)
    def test_invalid_input(self):
        for bad in [self.df.drop(columns='Profit_Rate'), self.df.assign(Profit_Rate=np.nan), self.df.assign(Profit_Rate=10), self.df.head(5)]:
            with self.assertRaises(ValueError): analyze(bad)

if __name__ == '__main__': unittest.main()
