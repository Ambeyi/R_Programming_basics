"""Transparent listwise scale reliability and explicit reverse scoring."""
import math
from statistics import mean, variance


def alpha(matrix):
    """Raw Cronbach alpha, or None for insufficient/constant total scores."""
    if len(matrix) < 2 or len(matrix[0]) < 2:
        return None
    k = len(matrix[0])
    total_var = variance([sum(row) for row in matrix])
    if total_var == 0:
        return None
    return k / (k - 1) * (1 - sum(variance(col) for col in zip(*matrix)) / total_var)


def correlation(x, y):
    if len(x) < 2:
        return None
    dx = [v - mean(x) for v in x]
    dy = [v - mean(y) for v in y]
    denominator = math.sqrt(sum(v*v for v in dx) * sum(v*v for v in dy))
    return sum(a*b for a,b in zip(dx,dy)) / denominator if denominator else None


def analyse(rows, spec):
    """Validate one scale; return summary and item diagnostics on complete cases.

    Missing values are None or blank strings. Invalid nonmissing values fail.
    All listed items share the same inclusive numeric bounds.
    """
    items = spec['items']
    if len(items) < 2 or len(set(items)) != len(items):
        raise ValueError('At least two distinct items are required')
    reverse = set(spec.get('reverse', []))
    if not reverse.issubset(items):
        raise ValueError('Reverse items must belong to the scale')
    lo, hi = float(spec['minimum']), float(spec['maximum'])
    if not math.isfinite(lo) or not math.isfinite(hi) or lo >= hi:
        raise ValueError('Bounds must be finite and increasing')
    matrix = []
    for number, row in enumerate(rows, 1):
        values = []
        for item in items:
            if item not in row:
                raise ValueError(f'Missing column: {item}')
            raw = row[item]
            if raw is None or str(raw).strip() == '':
                values.append(None)
                continue
            try:
                value = float(raw)
            except (ValueError, TypeError) as exc:
                raise ValueError(f'Invalid number at row {number}, item {item}') from exc
            if not math.isfinite(value) or not lo <= value <= hi:
                raise ValueError(f'Out-of-range value at row {number}, item {item}')
            values.append(lo + hi - value if item in reverse else value)
        if None not in values:
            matrix.append(values)
    n = len(matrix)
    summary = dict(scale=spec['name'], input_rows=len(rows), complete_rows=n,
                   excluded_rows=len(rows)-n, items=len(items), alpha=alpha(matrix),
                   mean_score=mean([mean(r) for r in matrix]) if n else None)
    diagnostics = []
    for j, item in enumerate(items):
        column = [r[j] for r in matrix]
        rest = [[v for i,v in enumerate(r) if i != j] for r in matrix]
        diagnostics.append(dict(scale=spec['name'], item=item, reversed=item in reverse,
            mean=mean(column) if n else None,
            sd=math.sqrt(variance(column)) if n > 1 else None,
            corrected_item_total=correlation(column, [sum(r) for r in rest]),
            alpha_if_deleted=alpha(rest)))
    return summary, diagnostics
