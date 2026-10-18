"""Explore long-only optimal allocations over the full correlation range."""
import csv
from pathlib import Path
from analysis import minimum_weight, portfolio


def scenario_rows():
    for i in range(201):
        rho = (i - 100) / 100
        weight = minimum_weight(rho)
        mean, sd = portfolio(weight, rho)
        yield (rho, weight, 1-weight, mean, sd)


def main():
    output = Path(__file__).resolve().parent / 'results' / 'correlation_sensitivity.csv'
    output.parent.mkdir(exist_ok=True)
    with output.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.writer(stream)
        writer.writerow(['correlation', 'weight_A', 'weight_B', 'expected_return', 'standard_deviation'])
        writer.writerows(scenario_rows())
    print(f'Wrote 201 illustrative correlation scenarios to {output}')


if __name__ == '__main__':
    main()
