"""Two-sided comparisons of two independent numeric samples."""
import numpy as np
from scipy import stats

def compare(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    if any(x.ndim != 1 or len(x)<2 or not np.isfinite(x).all() for x in (a,b)):
        raise ValueError('Each sample needs at least two finite observations')
    va, vb = a.var(ddof=1), b.var(ddof=1)
    if va == 0 or vb == 0:
        raise ValueError('Each sample must have positive variance')
    se = np.sqrt(va/len(a)+vb/len(b))
    df = (va/len(a)+vb/len(b))**2 / ((va/len(a))**2/(len(a)-1)+(vb/len(b))**2/(len(b)-1))
    difference = a.mean()-b.mean()
    margin = stats.t.ppf(.975, df)*se
    welch = stats.ttest_ind(a,b,equal_var=False)
    # Asymptotic calculation accounts for ties; continuity correction is explicit.
    rank = stats.mannwhitneyu(a,b,alternative='two-sided',method='asymptotic',use_continuity=True)
    ks = stats.ks_2samp(a,b,alternative='two-sided',method='exact')
    tests = [dict(test='Welch t', statistic=float(welch.statistic), p_value=float(welch.pvalue)),
             dict(test='Mann Whitney U',statistic=float(rank.statistic),p_value=float(rank.pvalue)),
             dict(test='Kolmogorov Smirnov',statistic=float(ks.statistic),p_value=float(ks.pvalue))]
    summary = dict(n_a=len(a),n_b=len(b),mean_difference=float(difference),
        mean_difference_ci95_low=float(difference-margin),mean_difference_ci95_high=float(difference+margin),
        welch_df=float(df),probability_superiority_a=float(rank.statistic/(len(a)*len(b))))
    groups = [dict(group=name,n=len(x),mean=float(x.mean()),median=float(np.median(x)),sd=float(x.std(ddof=1)))
              for name,x in [('A',a),('B',b)]]
    return groups, tests, summary
