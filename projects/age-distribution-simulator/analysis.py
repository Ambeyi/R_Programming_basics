"""Exact frequency tables and descriptive statistics for integer ages."""
from collections import Counter
import statistics

def summarize(ages, minimum=13, maximum=80, width=10):
    if any(type(v) is not int for v in (minimum, maximum, width)):
        raise ValueError('Bounds and width must be integers')
    if not 0 <= minimum <= maximum <= 120 or width < 1:
        raise ValueError('Invalid age bounds or band width')
    if not ages or any(type(a) is not int or not minimum <= a <= maximum for a in ages):
        raise ValueError('Ages must be nonempty integers within the bounds')
    n = len(ages)
    counts = Counter(ages)
    frequencies = [dict(age=a, count=counts[a], proportion=counts[a]/n)
                   for a in range(minimum, maximum+1)]
    bands = []
    for start in range(minimum, maximum+1, width):
        end = min(start+width-1, maximum)
        count = sum(counts[a] for a in range(start, end+1))
        bands.append(dict(band=f'{start}-{end}', count=count, proportion=count/n,
                          expected_count=n*(end-start+1)/(maximum-minimum+1)))
    summary = dict(sample_size=n, minimum=min(ages), maximum=max(ages),
                   mean=statistics.mean(ages), median=statistics.median(ages),
                   population_sd=statistics.pstdev(ages),
                   theoretical_mean=(minimum+maximum)/2)
    return frequencies, bands, summary
