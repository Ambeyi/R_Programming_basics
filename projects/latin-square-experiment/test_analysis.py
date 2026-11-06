import unittest
import numpy as np
from design import simulate, validate
from analysis import analyze, matrix

class ExperimentTests(unittest.TestCase):
    def test_balance(self):
        frame = simulate()
        validate(frame)
        self.assertTrue((frame.groupby('shoe').size() == 4).all())
    def test_reproducible(self):
        self.assertTrue(simulate(9).equals(simulate(9)))
        self.assertFalse(simulate(9).equals(simulate(10)))
    def test_known_effects(self):
        frame = simulate(noise_sd=0)
        x, _ = matrix(frame, ['athlete', 'trial', 'shoe'])
        np.testing.assert_allclose(np.linalg.lstsq(x, frame.time, rcond=None)[0],
                                   [53, -2, 3, 4, -1, 1, 3, 3, 5, 1], atol=1e-10)
    def test_independent_balanced_anova(self):
        frame = simulate()
        table, _, summary = analyze(frame)
        ss_total = sum((frame.time-frame.time.mean())**2)
        ss_factors = []
        for factor in ['athlete', 'trial', 'shoe']:
            expected = 4*sum((frame.groupby(factor).time.mean()-frame.time.mean())**2)
            actual = table.set_index('source').loc[factor, 'sum_squares']
            self.assertAlmostEqual(expected, actual, places=9)
            ss_factors.append(expected)
        self.assertAlmostEqual(ss_total-sum(ss_factors), summary['residual_sum_squares'], places=9)
        self.assertEqual(summary['residual_df'], 6)
    def test_invalid_design(self):
        frame = simulate(); frame.loc[0, 'shoe'] = 2
        with self.assertRaises(ValueError): validate(frame)
    def test_invalid_values(self):
        for value in [float('nan'), float('inf')]:
            frame = simulate(); frame.loc[0, 'time'] = value
            with self.assertRaises(ValueError): analyze(frame)
        with self.assertRaises(ValueError): simulate(noise_sd=-1)
    def test_degenerate_residuals(self):
        with self.assertRaises(ValueError): analyze(simulate(noise_sd=0))

if __name__ == '__main__': unittest.main()
