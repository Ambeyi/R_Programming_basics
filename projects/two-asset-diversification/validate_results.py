"""Check saved sensitivity data and chart coordinates without regenerating them."""
import csv
import math
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent / 'results'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(directory=ROOT):
    with (directory / 'correlation_sensitivity.csv').open(encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    require(len(rows) == 201, 'Expected 201 scenario rows')
    values = []
    for i, row in enumerate(rows):
        r = {key: float(row[key]) for key in ['correlation', 'weight_A', 'weight_B', 'expected_return', 'standard_deviation']}
        require(all(math.isfinite(v) for v in r.values()), f'Nonfinite value in row {i}')
        rho, a, b = r['correlation'], r['weight_A'], r['weight_B']
        require(abs(rho - (i-100)/100) < 1e-10, f'Unexpected correlation in row {i}')
        require(0 <= a <= 1 and 0 <= b <= 1 and abs(a+b-1) < 1e-10, f'Invalid allocation in row {i}')
        require(abs(r['expected_return']-(.12*a+.10*b)) < 1e-10, f'Incorrect return in row {i}')
        variance = .09*a*a + .04*b*b + .12*rho*a*b
        require(r['standard_deviation'] >= 0 and abs(r['standard_deviation']**2-variance) < 1e-10, f'Incorrect risk in row {i}')
        # First-order optimality for the convex variance function on [0,1].
        gradient = 2*(.13-.12*rho)*a + .12*rho-.08
        require((a == 0 and gradient >= -1e-10) or (a == 1 and gradient <= 1e-10) or (0 < a < 1 and abs(gradient) < 1e-10), f'Nonoptimal allocation in row {i}')
        values.append(r)
    root = ET.parse(directory / 'correlation_sensitivity.svg').getroot()
    panels = root.findall('.//{http://www.w3.org/2000/svg}polyline')
    require(len(panels) == 2, 'Expected two chart panels')
    for panel, top, field, scale in zip(panels, [110,375], ['weight_A','standard_deviation'], [.4,.2]):
        points = panel.attrib['points'].split()
        require(len(points) == len(values), 'Chart point count differs from CSV')
        for point, r in zip(points, values):
            x, y = map(float, point.split(','))
            require(abs(x-(80+(r['correlation']+1)*375)) <= .00051 and abs(y-(top+175-r[field]/scale*175)) <= .00051, 'Chart coordinate differs from CSV')
    print('PASS: 201 saved scenarios, optimality conditions, and 402 chart coordinates.')


if __name__ == '__main__':
    validate()
