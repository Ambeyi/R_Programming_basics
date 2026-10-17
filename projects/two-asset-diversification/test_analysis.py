"""Regression checks for mathematical edge cases and rejected input."""
import math
import unittest
from analysis import portfolio, minimum_weight


class DiversificationTests(unittest.TestCase):
    def test_perfect_negative_correlation_can_cancel_risk(self):
        self.assertAlmostEqual(minimum_weight(-1), 0.4)
        self.assertAlmostEqual(portfolio(0.4, -1)[1], 0, places=7)

    def test_uncorrelated_variances_add(self):
        self.assertAlmostEqual(portfolio(0.5, 0)[1]**2, 0.0325)

    def test_perfect_positive_correlation_has_boundary_minimum(self):
        self.assertEqual(minimum_weight(1), 0)
        self.assertAlmostEqual(portfolio(0.5, 1)[1], 0.25)

    def test_minimum_beats_feasible_grid_across_correlations(self):
        for rho in [-1, -0.7, 0, 0.0417, 0.5, 0.9, 1]:
            with self.subTest(rho=rho):
                w = minimum_weight(rho)
                self.assertTrue(0 <= w <= 1)
                sd = portfolio(w, rho)[1]
                self.assertTrue(all(sd <= portfolio(i/1000, rho)[1] + 1e-8
                                    for i in range(1001)))

    def test_invalid_weights_rejected(self):
        for w in [-0.1, 1.1, math.nan, math.inf]:
            with self.assertRaises(ValueError):
                portfolio(w, 0)

    def test_invalid_correlations_rejected_by_both_functions(self):
        for rho in [-1.1, 1.1, math.nan, math.inf]:
            for function in [minimum_weight, lambda r: portfolio(0.5, r)]:
                with self.assertRaises(ValueError):
                    function(rho)


if __name__ == '__main__':
    unittest.main()
