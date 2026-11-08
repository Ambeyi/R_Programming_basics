"""Export descriptive and inferential comparisons for a group/value CSV."""
import argparse
import csv
import json
from pathlib import Path
from analysis import compare
from data_io import read_samples

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path('examples/synthetic.csv'))
    p.add_argument('--output',type=Path,default=Path('results'))
    args=p.parse_args()
    groups,tests,summary=compare(*read_samples(args.input))
    args.output.mkdir(parents=True,exist_ok=True)
    for name,rows in [('group_summary',groups),('tests',tests)]:
        with (args.output/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (args.output/'effects.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
