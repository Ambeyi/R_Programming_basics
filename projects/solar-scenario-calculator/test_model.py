import tempfile
import unittest
from pathlib import Path
from model import calculate
from scenarios import load,sensitivity

class SolarTests(unittest.TestCase):
    def test_hand_calculation(self):
        result=calculate(500,1200,.15,.9,100000)
        self.assertAlmostEqual(result['annual_energy_kwh'],81000)
        self.assertAlmostEqual(result['required_area_m2'],100000/162)
        self.assertAlmostEqual(result['annual_demand_ratio'],.81)
    def test_inverse_area(self):
        area=calculate(1,1500,.2,.8,40000)['required_area_m2']
        self.assertAlmostEqual(calculate(area,1500,.2,.8,40000)['annual_energy_kwh'],40000)
    def test_area_scaling(self):
        a=calculate(100,1200,.2,.8,50000);b=calculate(200,1200,.2,.8,50000)
        self.assertEqual(b['annual_energy_kwh'],2*a['annual_energy_kwh'])
    def test_zero_area_and_surplus(self):
        self.assertEqual(calculate(0,1200,.2,.8,50000)['annual_energy_kwh'],0)
        self.assertGreater(calculate(1000,1200,.2,.8,50000)['annual_demand_ratio'],1)
    def test_invalid_parameters(self):
        for position,bad in [(0,-1),(1,0),(2,1.1),(3,0),(4,0),(0,float('nan')),(1,float('inf')),(2,True)]:
            values=[500,1200,.15,.9,100000];values[position]=bad
            with self.assertRaises(ValueError):calculate(*values)
    def test_sensitivity_grid(self):
        base=dict(area_m2=500,irradiation_kwh_m2_year=1200,efficiency=.15,performance_factor=.9,demand_kwh_year=100000)
        rows=sensitivity(base)
        self.assertEqual(len(rows),9)
        self.assertLess(rows[0]['annual_energy_kwh'],rows[-1]['annual_energy_kwh'])
        self.assertEqual(base['efficiency'],.15)
    def test_duplicate_scenarios(self):
        header='scenario,area_m2,irradiation_kwh_m2_year,efficiency,performance_factor,demand_kwh_year\n'
        row='demo,500,1200,.15,.9,100000\n'
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'data.csv';p.write_text(header+row)
            self.assertEqual(len(load(p)),1)
            p.write_text(header+row+row)
            with self.assertRaises(ValueError):load(p)

if __name__=='__main__':unittest.main()
