"""Create a synthetic population and export aggregate results."""
import argparse
import csv
import json
from pathlib import Path
from simulation import simulate
from analysis import summarize
from chart import render

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name, default in [('size',8000),('minimum',13),('maximum',80),('seed',123),('width',10)]:
        parser.add_argument('--'+name,type=int,default=default)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    ages=simulate(args.size,args.minimum,args.maximum,args.seed)
    frequencies,bands,summary=summarize(ages,args.minimum,args.maximum,args.width)
    args.output.mkdir(parents=True,exist_ok=True)
    for name,rows in [('age_frequencies',frequencies),('age_bands',bands)]:
        with (args.output/(name+'.csv')).open('w',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    summary.update(data_kind='synthetic',seed=args.seed,lower_bound=args.minimum,
                   upper_bound=args.maximum,band_width=args.width)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (args.output/'age_distribution.svg').write_text(render(bands))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
