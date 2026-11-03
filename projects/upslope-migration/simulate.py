"""Toy grid migration: occupied cells move upslope without growth."""
import argparse,csv,json,random
from pathlib import Path

def shift(grid):
    if not grid or not grid[0] or any(len(r)!=len(grid[0]) for r in grid):
        raise ValueError('A nonempty rectangular grid is required')
    if any(v not in (0,1) for r in grid for v in r):
        raise ValueError('Grid values must be binary')
    return [r[:] for r in grid[1:]]+[[0]*len(grid[0])]

def simulate(rows=200,cols=200,years=15,probability=.1,seed=123):
    if any(isinstance(v,bool) or not isinstance(v,int) or v<1 for v in [rows,cols,years]):
        raise ValueError('Dimensions and years must be positive integers')
    if not 0<=probability<=1: raise ValueError('Probability must be between zero and one')
    rng=random.Random(seed);grid=[[int(rng.random()<.5) for _ in range(cols)] for _ in range(rows)]
    history=[]
    def record(year,moved,lost):
        count=sum(map(sum,grid));history.append(dict(year=year,migrated=moved,lost_cells=lost,occupied=count,cover_percent=100*count/(rows*cols)))
    record(0,False,0)
    for year in range(1,years+1):
        moved=rng.random()<probability;lost=sum(grid[0]) if moved else 0
        if moved: grid=shift(grid)
        record(year,moved,lost)
    return history

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',default='results');p.add_argument('--seed',type=int,default=123);p.add_argument('--probability',type=float,default=.1);a=p.parse_args()
    h=simulate(seed=a.seed,probability=a.probability);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    with (out/'history.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=h[0]);w.writeheader();w.writerows(h)
    (out/'settings.json').write_text(json.dumps(dict(rows=200,cols=200,years=15,probability=a.probability,seed=a.seed),indent=2))
    print(h[0]);print(h[-1])
