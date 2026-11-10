"""Analyze a startup CSV or the named sheet in an Excel workbook."""
import argparse
import json
from pathlib import Path
import pandas as pd
from analysis import analyze

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=Path('examples/synthetic.csv'))
    parser.add_argument('--output',type=Path,default=Path('results/demo'))
    args=parser.parse_args()
    frame=(pd.read_excel(args.input,sheet_name='DPBS 1190 Assessment Dataset')
           if args.input.suffix.lower()=='.xlsx' else pd.read_csv(args.input))
    city,cohort,corr,summary=analyze(frame)
    args.output.mkdir(parents=True,exist_ok=True)
    for name,table in [('city_summary',city),('cohort_summary',cohort),('profit_correlations',corr)]:
        table.to_csv(args.output/(name+'.csv'),index=False)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
