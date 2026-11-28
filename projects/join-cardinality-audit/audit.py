"""Predict equality left-join cardinality without materialising the join."""
from collections import Counter


def counts(rows, keys):
    if not keys or len(set(keys)) != len(keys):
        raise ValueError('Supply distinct key columns')
    result, missing = Counter(), 0
    for row in rows:
        if any(key not in row for key in keys):
            raise ValueError('Missing key column')
        values = tuple(row[key] for key in keys)
        if any(value is None or str(value).strip() == '' for value in values):
            missing += 1
        else:
            result[values] += 1
    return result, missing


def audit(left, right, keys):
    """Keys match exactly; any blank/null component never matches.

    Inputs are lists of dictionaries. Nonblank key strings retain whitespace,
    case and leading zeros. No identifiers are included in the output.
    """
    lc, lm = counts(left, keys)
    rc, rm = counts(right, keys)
    common = lc.keys() & rc.keys()
    matched = sum(lc[k] for k in common)
    projected = lm + sum(n * max(rc.get(k, 0), 1) for k,n in lc.items())
    ldup = any(lc[k] > 1 for k in common)
    rdup = any(rc[k] > 1 for k in common)
    relationship = ('no_matches' if not common else
        'many_to_many' if ldup and rdup else
        'many_to_one' if ldup else 'one_to_many' if rdup else 'one_to_one')
    return dict(left_rows=len(left), right_rows=len(right),
        left_missing_key_rows=lm, right_missing_key_rows=rm,
        left_distinct_keys=len(lc), right_distinct_keys=len(rc),
        left_duplicate_keys=sum(n>1 for n in lc.values()),
        right_duplicate_keys=sum(n>1 for n in rc.values()),
        matching_keys=len(common), matched_left_rows=matched,
        unmatched_left_rows=len(left)-matched,
        unmatched_right_rows=rm+sum(n for k,n in rc.items() if k not in lc),
        projected_left_join_rows=projected,
        additional_rows=projected-len(left),
        expansion_factor=projected/len(left) if left else None,
        matched_key_relationship=relationship,
        many_to_many_keys=sum(lc[k]>1 and rc[k]>1 for k in common))
