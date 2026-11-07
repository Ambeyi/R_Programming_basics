import unittest
import xml.etree.ElementTree as ET
from simulation import simulate
from analysis import summarize
from chart import render

class AgeTests(unittest.TestCase):
    def test_reproducibility(self):
        self.assertEqual(simulate(seed=9),simulate(seed=9))
        self.assertNotEqual(simulate(seed=9),simulate(seed=10))
    def test_inclusive_bounds(self):
        self.assertEqual(simulate(5,20,20),[20]*5)
        self.assertEqual(set(simulate(10000,13,80)),set(range(13,81)))
    def test_hand_calculated_summary(self):
        freq,bands,s=summarize([13,13,22,23,80])
        self.assertEqual([b['count'] for b in bands],[3,1,0,0,0,0,1])
        self.assertEqual(s['mean'],30.2);self.assertEqual(s['median'],22)
        self.assertEqual(freq[0]['count'],2)
    def test_conservation_and_expectations(self):
        freq,bands,s=summarize(simulate())
        self.assertEqual(sum(r['count'] for r in freq),8000)
        self.assertEqual(sum(r['count'] for r in bands),8000)
        self.assertAlmostEqual(sum(r['expected_count'] for r in bands),8000)
        self.assertAlmostEqual(bands[-1]['expected_count']/bands[0]['expected_count'],0.8)
    def test_invalid_parameters(self):
        for args in [(0,13,80),(5,80,13),(5,-1,80),(5,13,121),(1.5,13,80)]:
            with self.assertRaises(ValueError):simulate(*args)
        for ages in [[],[13.5],[81],[True]]:
            with self.assertRaises(ValueError):summarize(ages)
        with self.assertRaises(ValueError):summarize([13],width=0)
    def test_chart_is_valid_xml(self):
        _,bands,_=summarize([13,22,80])
        root=ET.fromstring(render(bands))
        self.assertTrue(root.tag.endswith('svg'))
        self.assertIn('Synthetic',render(bands))

if __name__=='__main__':unittest.main()
