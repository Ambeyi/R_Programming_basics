"""Evaluate unscaled Euclidean nearest neighbours on supplied folds."""
import argparse,csv,math
from collections import Counter
from pathlib import Path

def load(path):
    with open(path,newline="",encoding="utf-8-sig") as f:
        reader=csv.DictReader(f)
        if not {"x","y","myclass","fold"}.issubset(reader.fieldnames or []):raise ValueError("Missing required columns")
        rows=[]
        for r in reader:
            x,y=float(r["x"]),float(r["y"])
            label,fold=r["myclass"].strip(),r["fold"].strip()
            if not all(map(math.isfinite,[x,y])) or not label or not fold:raise ValueError("Invalid row")
            rows.append((x,y,label,fold))
    return rows

def predict(train,point,k):
    if not isinstance(k,int) or not 1<=k<=len(train):raise ValueError("Invalid neighbour count")
    # Stable input order breaks equal-distance ties; lexical class order breaks vote ties.
    nearest=sorted(enumerate(train),key=lambda pair:((pair[1][0]-point[0])**2+(pair[1][1]-point[1])**2,pair[0]))[:k]
    votes=Counter(r[2] for _,r in nearest)
    return min(votes,key=lambda label:(-votes[label],label))

def evaluate(rows,ks=(1,3,5)):
    if not rows or len({r[3] for r in rows})<2:raise ValueError("At least two folds required")
    if not ks or len(set(ks))!=len(ks):raise ValueError("Neighbour counts must be nonempty and unique")
    results=[];confusion=Counter()
    for fold in sorted({r[3] for r in rows}):
        train=[r for r in rows if r[3]!=fold];test=[r for r in rows if r[3]==fold]
        for k in ks:
            predictions=[predict(train,r,k) for r in test]
            correct=sum(p==r[2] for p,r in zip(predictions,test))
            results.append({"fold":fold,"k":k,"train_n":len(train),"test_n":len(test),"correct":correct,"accuracy":correct/len(test)})
            confusion.update((k,r[2],prediction) for r,prediction in zip(test,predictions))
    counts=[{"k":k,"actual":a,"predicted":b,"count":n} for (k,a,b),n in sorted(confusion.items())]
    return results,counts

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("input")
    parser.add_argument("--output",default="output");parser.add_argument("--k",type=int,nargs="+",default=[1,3,5])
    args=parser.parse_args();results,counts=evaluate(load(args.input),args.k)
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    for name,rows in [("folds",results),("confusion",counts)]:
        with (out/(name+".csv")).open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(f"Completed {len(results)} fold/model evaluations")
if __name__=="__main__":main()
