"""Export prevalence, richness and species-pair Jaccard summaries."""
import argparse,json
from pathlib import Path
import pandas as pd
from analysis import analyze

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=Path('examples/synthetic.csv'))
    p.add_argument('--output',type=Path,default=Path('results/demo'))
    args=p.parse_args()
    prevalence,richness,pairs,summary=analyze(pd.read_csv(args.input))
    args.output.mkdir(parents=True,exist_ok=True)
    for name,table in [('prevalence',prevalence),('richness',richness),('closest_pairs',pairs.sort_values(['jaccard_distance','species_a','species_b']).head(20))]:table.to_csv(args.output/(name+'.csv'),index=False)
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
