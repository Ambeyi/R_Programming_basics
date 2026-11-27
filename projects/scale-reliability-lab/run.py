"""Run configured scales against a CSV and write aggregate results."""
import argparse
import csv
import json
from pathlib import Path
from reliability import analyse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('scales', type=Path)
    parser.add_argument('--output', type=Path, default=Path('results'))
    args = parser.parse_args()
    with args.input.open(encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError('CSV requires unique column headers')
        rows = list(reader)
        headers = set(reader.fieldnames)
    specs = json.loads(args.scales.read_text(encoding='utf-8'))
    if not specs or len({s['name'] for s in specs}) != len(specs):
        raise ValueError('Provide at least one scale with unique names')
    summaries, diagnostics = [], []
    for spec in specs:
        if not set(spec['items']).issubset(headers):
            raise ValueError('Configured items are missing from CSV headers')
        summary, detail = analyse(rows, spec)
        summaries.append(summary)
        diagnostics.extend(detail)
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, records in [('scales.csv', summaries), ('items.csv', diagnostics)]:
        with (args.output / filename).open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)
    print(f'Analysed {len(specs)} scales across {len(rows)} input rows')


if __name__ == '__main__':
    main()
