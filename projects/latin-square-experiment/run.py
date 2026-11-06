"""Run the bundled simulation or analyze a compatible CSV."""
import argparse
import json
from pathlib import Path
import pandas as pd
from design import simulate
from analysis import analyze

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--output', type=Path, default=Path('results'))
    parser.add_argument('--seed', type=int, default=123)
    parser.add_argument('--noise-sd', type=float, default=1.5)
    args = parser.parse_args()
    frame = pd.read_csv(args.input) if args.input else simulate(args.seed, args.noise_sd)
    anova, coefficients, summary = analyze(frame)
    summary['data_kind'] = 'user-supplied' if args.input else 'simulated'
    if not args.input:
        summary.update(seed=args.seed, noise_sd=args.noise_sd)
    args.output.mkdir(parents=True, exist_ok=True)
    anova.to_csv(args.output/'anova.csv', index=False)
    coefficients.to_csv(args.output/'coefficients.csv', index=False)
    (args.output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))

if __name__ == '__main__':
    main()
