"""Stratified partitions without replacement, preserving source-row identity."""
import numpy as np
import pandas as pd

def partition(labels,seed=43):
    y=np.asarray(labels)
    if y.ndim!=1 or not np.isin(y,[0,1]).all() or len(y)==0:
        raise ValueError('Provide complete binary labels')
    if type(seed) is not int:raise ValueError('Seed must be an integer')
    rng=np.random.default_rng(seed);parts={k:[] for k in ['train','validation','test']}
    for label in [0,1]:
        indices=np.flatnonzero(y==label)
        if len(indices)<10:raise ValueError('At least ten rows per class are required')
        indices=rng.permutation(indices);n=len(indices);a=int(.7*n);b=a+int(.15*n)
        for name,chunk in zip(parts,[indices[:a],indices[a:b],indices[b:]]):parts[name].extend(chunk.tolist())
    return {name:np.array(sorted(indices),dtype=int) for name,indices in parts.items()}

def audit(frame,seed=43):
    if 'class' not in frame:raise ValueError('Missing class column')
    labels=pd.to_numeric(frame['class'],errors='raise').to_numpy()
    parts=partition(labels,seed)
    rows=[]
    for name,idx in parts.items():
        positives=int(labels[idx].sum())
        rows.append(dict(partition=name,rows=len(idx),class_0=len(idx)-positives,class_1=positives,positive_rate=positives/len(idx)))
    overlap=[]
    names=list(parts)
    # Row overlap and feature-identical records answer different questions.
    features=frame.drop(columns='class')
    hashes=pd.util.hash_pandas_object(features,index=False).to_numpy() if len(features.columns) else None
    for i,left in enumerate(names):
        for right in names[i+1:]:
            common=set(parts[left])&set(parts[right])
            shared_hashes=len(set(hashes[parts[left]])&set(hashes[parts[right]])) if hashes is not None else None
            overlap.append(dict(left=left,right=right,shared_row_positions=len(common),shared_feature_hashes=shared_hashes))
    missing=frame.isna().sum().rename_axis('column').reset_index(name='missing_rows')
    summary=dict(source_rows=len(frame),class_1=int(labels.sum()),class_0=int(len(labels)-labels.sum()),
        seed=seed,assigned_rows=sum(map(len,parts.values())),unique_assigned_rows=len(set(np.concatenate(list(parts.values())))),
        duplicate_feature_rows=int(features.duplicated().sum()) if len(features.columns) else None)
    return pd.DataFrame(rows),pd.DataFrame(overlap),missing,summary
