"""Reproduce an illustrative two-asset diversification exercise (standard library only)."""
from pathlib import Path
import csv
import math

MU_A, MU_B = 0.12, 0.10
SD_A, SD_B = 0.30, 0.20
CORRELATIONS = (0.0417, 1.0)
OUT = Path(__file__).resolve().parent / 'results'


def portfolio(weight, rho):
    if not 0 <= weight <= 1 or not -1 <= rho <= 1:
        raise ValueError('Long-only weight and correlation outside their bounds')
    variance = (weight * SD_A) ** 2 + ((1-weight) * SD_B) ** 2
    variance += 2 * weight * (1-weight) * rho * SD_A * SD_B
    return weight * MU_A + (1-weight) * MU_B, math.sqrt(max(0, variance))


def minimum_weight(rho):
    denominator = SD_A**2 + SD_B**2 - 2*rho*SD_A*SD_B
    if denominator == 0:
        return 0.0
    return min(1.0, max(0.0, (SD_B**2-rho*SD_A*SD_B)/denominator))


def main():
    OUT.mkdir(exist_ok=True)
    rows = []
    for rho in CORRELATIONS:
        for i in range(11):
            w = i/10
            mean, sd = portfolio(w, rho)
            rows.append([rho, w, 1-w, mean, sd])
    with (OUT/'portfolio_grid.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['correlation','weight_A','weight_B','expected_return','standard_deviation'])
        writer.writerows(rows)
    lines = ['Illustrative inputs; no market observations.', 'Validation:']
    assert portfolio(0, 0.0417) == (MU_B, SD_B)
    assert portfolio(1, 0.0417) == (MU_A, SD_A)
    for i in range(101):
        w = i/100
        assert math.isclose(portfolio(w, 1)[1], w*SD_A+(1-w)*SD_B)
    for rho in CORRELATIONS:
        w = minimum_weight(rho)
        mean, sd = portfolio(w, rho)
        assert all(sd <= portfolio(i/10000, rho)[1]+1e-12 for i in range(10001))
        lines.append(f'rho={rho}: continuous long-only minimum weight_A={w:.8f}; expected_return={mean:.8f}; SD={sd:.8f}')
    assert minimum_weight(1) == 0
    lines.append('PASS: endpoints, perfect-correlation identity, boundary solution, and dense-grid minimum checks.')
    (OUT/'validation.txt').write_text('\n'.join(lines)+'\n')
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="800" height="480" viewBox="0 0 800 480">', '<rect width="800" height="480" fill="white"/>', '<g font-family="Arial" fill="#17243b">', '<text x="70" y="35" font-size="23">Diversification under two correlation assumptions</text>', '<text x="70" y="60" font-size="14">Illustrative inputs · long-only weights · not observed market performance</text>']
    for tick in range(5):
        y = 390 - tick/4*290
        svg += [f'<line x1="80" y1="{y}" x2="750" y2="{y}" stroke="#e0e5ed"/>', f'<text x="25" y="{y+5}">{15+tick*5}%</text>']
    for i in range(6):
        x=80+i/5*670
        svg.append(f'<text x="{x-10}" y="420">{i*20}%</text>')
    for rho, color in zip(CORRELATIONS, ('#126caa','#c65b20')):
        points=' '.join(f'{80+i/100*670:.2f},{390-(portfolio(i/100,rho)[1]-.15)/.20*290:.2f}' for i in range(101))
        svg.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="3"/>')
    svg += ['<text x="90" y="90" fill="#126caa">ρ = 0.0417</text>', '<text x="240" y="90" fill="#c65b20">ρ = 1.0</text>', '<text x="285" y="460">Weight allocated to Asset A</text>', '<text x="80" y="78" font-size="12">Portfolio standard deviation</text>', '</g></svg>']
    (OUT/'diversification.svg').write_text('\n'.join(svg))
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
