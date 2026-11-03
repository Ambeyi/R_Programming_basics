# Upslope Migration Simulation

A self-contained Python grid simulation exploring how repeated upslope movement changes occupied-cell counts in a fixed observation window.

## Features

- Initializes a binary grid with a seeded 50% occupancy probability.
- Applies a whole-grid upslope shift with a configurable annual probability.
- Tracks occupancy, cover percentage, movement events and cells leaving the upper boundary.
- Exports annual results and scenario settings.
- Includes five tests for boundary behavior, reproducibility and validation.

## Run

Python 3.10 or later; no external packages required.

```bash
python simulate.py --probability 0.5 --seed 123 --output results
python -m unittest -v
```

The included results use a 200-by-200 grid over 15 years with annual migration probability 0.5. The CLI default probability is 0.1. Other grid dimensions and durations can be supplied through the `simulate` Python function.

## Model behavior

Row zero represents the upper boundary. A movement event removes that row, shifts all remaining rows upward and adds a bare row at the bottom. Occupancy remains constant without movement and can only decline during movement. Initial occupied cells equal final occupied cells plus cumulative boundary losses.

This is a toy spatial-translation model. It contains no growth, colonization, water balance or ecological calibration. Its outputs describe movement through a fixed window rather than predictions of vegetation response to climate.

## Outputs

`results/history.csv` contains the initial state and 15 annual observations. `results/settings.json` records the dimensions, duration, seed and migration probability. All data are generated synthetically.
