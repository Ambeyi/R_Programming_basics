import argparse,csv,json
from pathlib import Path
from forecast import load_series,evaluate

def main():
    parser=argparse.ArgumentParser(description="Evaluate annual forecasting baselines")
    parser.add_argument("input");parser.add_argument("--min-train",type=int,default=4)
    parser.add_argument("--output",default="output");args=parser.parse_args()
    series=load_series(args.input);folds,metrics=evaluate(series,args.min_train)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    for name,rows in [("folds",folds),("metrics",metrics)]:
        with (out/(name+".csv")).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    summary={"observations":len(series),"first_year":series[0][0],"last_year":series[-1][0],
             "initial_training_years":args.min_train,"test_years":len(series)-args.min_train,
             "lowest_mae_model":metrics[0]["model"]}
    (out/"summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary))
if __name__=="__main__":main()
