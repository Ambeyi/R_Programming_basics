"""Leave-one-out evaluation refits the regression for each held-out row."""
import numpy as np
from model import fit,predict

def leave_one_out(x,y):
    x,y=np.asarray(x,dtype=float),np.asarray(y,dtype=float)
    fit(x,y)
    if len(x)<5:raise ValueError('Leave-one-out requires at least five observations')
    errors=[]
    for i in range(len(x)):
        keep=np.arange(len(x))!=i
        m=fit(x[keep],y[keep])
        errors.append(float(y[i]-predict(m,x[i])['predicted_score']))
    e=np.asarray(errors)
    return dict(method='leave_one_out',held_out_predictions=len(e),rmse=float(np.sqrt(np.mean(e**2))),mae=float(np.mean(abs(e))))
