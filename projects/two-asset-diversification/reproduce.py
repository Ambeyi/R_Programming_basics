"""Run checks and regenerate all Python outputs, independent of working directory."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    # Keep assertions enabled even if this runner is invoked with python -O.
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    steps = [
        ['-m', 'unittest', '-v', 'test_analysis.py'],
        ['analysis.py'],
        ['sensitivity.py'],
        ['plot_sensitivity.py'],
    ]
    for args in steps:
        print('Running: ' + ' '.join(args), flush=True)
        subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)
    expected = ['portfolio_grid.csv', 'validation.txt', 'diversification.svg',
                'correlation_sensitivity.csv', 'correlation_sensitivity.svg']
    for name in expected:
        output = ROOT / 'results' / name
        if not output.is_file() or output.stat().st_size == 0:
            raise RuntimeError(f'Missing or empty output: {output}')
    print('PASS: regression tests and all five Python outputs completed.')


if __name__ == '__main__':
    main()
