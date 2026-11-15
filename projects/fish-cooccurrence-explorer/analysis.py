"""Species-level Jaccard distances from binary site observations."""
import numpy as np
import pandas as pd

def analyze(frame):
    if 'Location' not in frame or len(frame)<1 or len(frame.columns)<3:
        raise ValueError('Require Location and at least two species columns')
    if frame.Location.isna().any() or frame.Location.duplicated().any():
        raise ValueError('Site identifiers must be present and unique')
    species=[c for c in frame.columns if c!='Location']
    x=frame[species].apply(pd.to_numeric,errors='raise').to_numpy(dtype=float)
    if not np.isfinite(x).all() or not np.isin(x,[0,1]).all():
        raise ValueError('Species entries must be complete binary observations')
    x=x.astype(np.int64);counts=x.sum(axis=0);shared=x.T@x
    pairs=[];disjoint=np.zeros(len(species),dtype=int)
    for i in range(len(species)):
        for j in range(i+1,len(species)):
            union=int(counts[i]+counts[j]-shared[i,j])
            distance=1-float(shared[i,j])/union if union else None
            if union and shared[i,j]==0:disjoint[i]+=1;disjoint[j]+=1
            pairs.append(dict(species_a=species[i],species_b=species[j],shared_sites=int(shared[i,j]),
                union_sites=union,jaccard_distance=distance,status='defined' if union else 'both_absent'))
    prevalence=pd.DataFrame(dict(species=species,sites_present=counts,prevalence=counts/len(x),disjoint_partners=disjoint))
    richness=pd.Series(x.sum(axis=1)).value_counts().sort_index().rename_axis('species_per_site').reset_index(name='sites')
    pair_table=pd.DataFrame(pairs)
    summary=dict(sites=len(x),species=len(species),species_pairs=len(pairs),
        empty_sites=int((x.sum(axis=1)==0).sum()),absent_species=int((counts==0).sum()),
        defined_pairs=int((pair_table.status=='defined').sum()),
        disjoint_pairs=int(((pair_table.union_sites>0)&(pair_table.shared_sites==0)).sum()),
        mean_site_richness=float(x.sum(axis=1).mean()))
    return prevalence,richness,pair_table,summary
