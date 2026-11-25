import argparse,csv
from pathlib import Path
from discount import calculate

def main():
    parser=argparse.ArgumentParser(description="Compare present values across discount rates")
    parser.add_argument("input");parser.add_argument("--rates",type=float,nargs="+",default=[0,0.03,0.05])
    parser.add_argument("--output",default="output");args=parser.parse_args()
    if len(set(args.rates))!=len(args.rates):raise ValueError("Rates must be unique")
    with open(args.input,newline="",encoding="utf-8-sig") as f:rows=list(csv.DictReader(f))
    details=[];totals=[]
    for rate in args.rates:
        d,t=calculate(rows,rate);details.extend(d);totals.extend(t)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    for name,data in [("flows",details),("totals",totals)]:
        with (out/(name+".csv")).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
    print(f"Wrote {len(details)} discounted flows and {len(totals)} scenario/rate totals")
if __name__=="__main__":main()
