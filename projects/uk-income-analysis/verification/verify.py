"""Independently reproduce the original R OLS estimates. Input stays private."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root = Path(__file__).resolve().parents[1]
d = pd.read_excel(sys.argv[1]).sort_values('year')
cols = ['demox_eiu', 'income_per_person', 'invest_pct_gdp', 'tax_pct_gdp']
assert len(d) == 11 and d.year.is_unique and d[cols + ['gini_index']].notna().all().all()
X = np.column_stack([np.ones(len(d)), d[cols].to_numpy()])
y = d.gini_index.to_numpy()
b, _, rank, _ = np.linalg.lstsq(X, y, rcond=None)
assert rank == X.shape[1]
e = y - X @ b
df = len(y) - rank
_, R = np.linalg.qr(X)
Ri = np.linalg.inv(R)
se = np.sqrt(np.diag(Ri @ Ri.T) * (e @ e / df))
r2 = 1 - (e @ e) / ((y - y.mean()) @ (y - y.mean()))
expected = np.array([95.6795730, -.9246736, .0005925, -.1916387, -.2014983])
np.testing.assert_allclose(b, expected, atol=5e-7, rtol=0)
out = root / 'results'; out.mkdir(exist_ok=True)
pd.DataFrame({'term':['Intercept']+cols,'estimate':b,'standard_error':se,'t':b/se,'p_value':2*t.sf(abs(b/se),df)}).to_csv(out/'ols_coefficients.csv',index=False)
d[cols+['gini_index']].describe().to_csv(out/'summary_statistics.csv')
d[cols+['gini_index']].corr().to_csv(out/'correlations.csv')
(out/'validation.txt').write_text(f'11 complete observations; years {int(d.year.min())}-{int(d.year.max())}\nOLS rank: {rank}; residual degrees of freedom: {df}\nR squared: {r2:.7f}\nAdjusted R squared: {1-(1-r2)*(len(y)-1)/df:.7f}\nAll five coefficients agree with the archived 2023 R report within 0.0000005.\nOutputs regenerated using Python NumPy/SciPy; revised R script not executed in this environment.\nClassical OLS inference is illustrative, not time-series-robust.\n')
plt.rcParams.update({'svg.fonttype':'none','font.size':10})
fig,axes=plt.subplots(1,2,figsize=(10,4),layout='constrained')
axes[0].plot(d.year,d.gini_index,marker='o',color='#176B87');axes[0].set(title='Gini index, 2006–2016',xlabel='Year',ylabel='Gini index (supplied scale)')
axes[1].scatter(d.demox_eiu,d.gini_index,color='#176B87');axes[1].set(title='Democracy and inequality',xlabel='demox_eiu (supplied scale)',ylabel='Gini index')
for a in axes:a.grid(alpha=.2)
fig.suptitle('UK exploratory analysis · 11 annual observations')
fig.savefig(out/'overview.svg');plt.close(fig)
print((out/'validation.txt').read_text())
