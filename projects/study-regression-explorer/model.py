"""Simple least squares with mean and individual prediction intervals."""
import numpy as np
from scipy.stats import t

def fit(x,y):
    x,y=np.asarray(x,dtype=float),np.asarray(y,dtype=float)
    if x.ndim!=1 or y.ndim!=1 or len(x)!=len(y) or len(x)<4:
        raise ValueError('Provide paired one-dimensional samples of at least four rows')
    if not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError('Values must be finite')
    sxx=float(((x-x.mean())**2).sum())
    if sxx<=0:raise ValueError('Predictor must vary')
    slope=float(((x-x.mean())*(y-y.mean())).sum()/sxx)
    intercept=float(y.mean()-slope*x.mean())
    error=y-intercept-slope*x
    sse=float(error@error);sst=float(((y-y.mean())**2).sum())
    return dict(n=len(x),slope=slope,intercept=intercept,x_mean=float(x.mean()),sxx=sxx,
        residual_variance=sse/(len(x)-2),r_squared=1-sse/sst if sst>0 else None,
        x_min=float(x.min()),x_max=float(x.max()))

def predict(model,x):
    x=float(x)
    if not np.isfinite(x):raise ValueError('Prediction input must be finite')
    value=model['intercept']+model['slope']*x
    leverage=1/model['n']+(x-model['x_mean'])**2/model['sxx']
    critical=t.ppf(.975,model['n']-2)
    mean_margin=critical*np.sqrt(model['residual_variance']*leverage)
    individual_margin=critical*np.sqrt(model['residual_variance']*(1+leverage))
    return dict(hours_studied=x,predicted_score=value,mean_ci95_low=value-mean_margin,
        mean_ci95_high=value+mean_margin,prediction95_low=value-individual_margin,
        prediction95_high=value+individual_margin,extrapolation=not model['x_min']<=x<=model['x_max'])
