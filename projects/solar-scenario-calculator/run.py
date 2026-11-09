"""Evaluate annual solar scenarios and a first-scenario sensitivity grid."""
import argparse
import csv
import json
from pathlib import Path
from scenarios import load,evaluate,sensitivity

def write_csv(path,rows):
    with path.open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('examples/scenarios.csv'))
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    rows=load(args.input);results=evaluate(rows);grid=sensitivity(rows[0])
    args.output.mkdir(parents=True,exist_ok=True)
    write_csv(args.output/'scenarios.csv',results)
    write_csv(args.output/'sensitivity.csv',grid)
    summary=dict(scenarios=len(results),sensitivity_cases=len(grid),sensitivity_base=rows[0]['scenario'],
                 highest_energy_scenario=max(results,key=lambda r:r['annual_energy_kwh'])['scenario'])
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
