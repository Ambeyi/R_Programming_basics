"""Render the committed scenario CSV as an accessible, dependency-free SVG."""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    with (ROOT / 'results/correlation_sensitivity.csv').open(encoding='utf-8') as f:
        rows = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(f)]
    if len(rows) != 201 or any(not math.isfinite(v) for r in rows for v in r.values()):
        raise ValueError('Expected 201 finite scenario rows')
    if any(abs(r['correlation'] - (i-100)/100) > 1e-10 for i, r in enumerate(rows)):
        raise ValueError('Expected correlations from -1 to 1 in increments of 0.01')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="900" height="660" viewBox="0 0 900 660" role="img" aria-labelledby="title desc">',
           '<title id="title">How correlation changes optimal allocation and risk</title>',
           '<desc id="desc">Two charts from 201 hypothetical scenarios. Asset A allocation falls from 40 percent to zero; minimum volatility rises from zero to 20 percent. The allocation reaches zero at correlation two thirds.</desc>',
           '<rect width="900" height="660" fill="#f8fafc"/>',
           '<g font-family="Arial, sans-serif" fill="#17243b">',
           '<text x="80" y="35" font-size="23">How correlation changes allocation and risk</text>',
           '<text x="80" y="59" font-size="14">201 hypothetical scenarios · long-only minimum-variance portfolios</text>']
    for top, field, maximum, heading, color in [(110, 'weight_A', .4, 'Optimal allocation to Asset A', '#1769aa'), (375, 'standard_deviation', .2, 'Minimum portfolio standard deviation', '#a23d28')]:
        svg.append(f'<text x="80" y="{top-17}" font-size="17">{heading}</text>')
        for j in range(5):
            y = top + 175 - j/4*175
            svg.extend([f'<line x1="80" y1="{y}" x2="830" y2="{y}" stroke="#dbe2ea"/>', f'<text x="30" y="{y+5}" font-size="13">{maximum*j/4:.0%}</text>'])
        for rho in [-1, -.5, 0, .5, 1]:
            x = 80 + (rho+1)/2*750
            svg.append(f'<text x="{x}" y="{top+198}" text-anchor="middle" font-size="13">{rho:g}</text>')
        points = ' '.join(f"{80+(r['correlation']+1)/2*750:.3f},{top+175-r[field]/maximum*175:.3f}" for r in rows)
        svg.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
        svg.append(f'<line x1="705" y1="{top}" x2="705" y2="{top+175}" stroke="#475569" stroke-dasharray="5 5"/>')
        svg.append(f'<text x="710" y="{top+15}" font-size="12">ρ = 2/3</text>')
        svg.append(f'<text x="455" y="{top+222}" text-anchor="middle" font-size="14">Correlation</text>')
    svg += ['<text x="80" y="635" font-size="13">Fixed assumed returns and volatilities; no observed market data or performance claims.</text>', '</g></svg>']
    target = ROOT / 'results/correlation_sensitivity.svg'
    target.write_text('\n'.join(svg), encoding='utf-8')
    print(f'Rendered {len(rows)} points per panel: {target}')


if __name__ == '__main__':
    main()
