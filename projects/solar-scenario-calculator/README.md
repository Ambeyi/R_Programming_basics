# Solar scenario calculator

Explore annual solar energy output, panel area requirements and annual demand coverage using explicit energy and area units. Runs on Python 3.10+ with no external packages.

## Features

- Evaluate multiple scenarios from a validated CSV.
- Calculate annual energy, energy yield per square metre, required panel area and annual energy balance.
- Compare nine efficiency and performance-factor combinations for the first input scenario.
- Export reproducible CSV and JSON results.
- Verify calculations with seven automated tests.

## Run

From this project directory:

```bash
python run.py
python -m unittest -v
python run.py --input examples/scenarios.csv --output results/custom
```

The input columns are `scenario`, `area_m2`, `irradiation_kwh_m2_year`, `efficiency`, `performance_factor`, and `demand_kwh_year`. Efficiency and performance factor are fractions between zero and one, excluding zero. Scenario names must be unique.

## Hypothetical results

| Scenario | Annual energy kWh | Annual demand ratio |
| --- | ---: | ---: |
| Baseline | 81,000 | 0.81 |
| Higher efficiency | 113,400 | 1.134 |
| Larger area | 121,500 | 1.215 |
| Lower performance | 67,500 | 0.675 |

The baseline uses 500 m² of active panel area, annual irradiation of 1,200 kWh/m², efficiency 0.15, performance factor 0.90 and annual demand of 100,000 kWh. Its required area for annual energy equality is approximately 617.28 m².

All example inputs are hypothetical. Annual generation exceeding annual demand does not establish hourly self-sufficiency or eliminate the need for grid supply or storage.

## Outputs

- `results/scenarios.csv`: inputs and calculations for every scenario.
- `results/sensitivity.csv`: nine combinations for the first scenario.
- `results/summary.json`: scenario counts and highest annual generation.
- `results/verification.txt`: seven passing tests.

See [METHODS.md](METHODS.md) for formulas, assumptions and model scope.
