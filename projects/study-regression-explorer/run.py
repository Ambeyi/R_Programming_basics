"""Analyze a CSV containing hours_studied and exam_score."""
import argparse
import json
from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr
from model import fit,predict
from evaluation import leave_one_out

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path('examples/synthetic.csv'))
    p.add_argument('--output',type=Path,default=Path('results/demo'))
    p.add_argument('--hours',type=float,nargs='+',default=[2,7,15,28])
    args=p.parse_args()
    d=pd.read_csv(args.input)
    x=d.hours_studied.to_numpy(dtype=float);y=d.exam_score.to_numpy(dtype=float)
    m=fit(x,y)
    if min(x)<0:raise ValueError('Study hours cannot be negative')
    m['pearson_r']=float(pearsonr(x,y).statistic) if len(set(y))>1 else None
    predictions=[predict(m,h) for h in args.hours]
    validation=leave_one_out(x,y)
    args.output.mkdir(parents=True,exist_ok=True)
    for name,result in [('model',m),('validation',validation)]:
        (args.output/(name+'.json')).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    pd.DataFrame(predictions).to_csv(args.output/'predictions.csv',index=False)
    print(json.dumps(dict(model=m,validation=validation),indent=2))

if __name__=='__main__':main()
