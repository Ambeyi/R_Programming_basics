"""Order-level shipping duration summaries."""
import argparse,json
from pathlib import Path
import pandas as pd
C=['Order Id','Shipping Mode','Days for shipping (real)','Days for shipment (scheduled)']
def analyze(d):
 if not set(C)<=set(d): raise ValueError('Required columns: '+', '.join(C))
 d=d[C].copy()
 if d.empty or d.isna().any().any(): raise ValueError('Complete nonempty input required')
 for c in C[2:]:
  d[c]=pd.to_numeric(d[c],errors='raise')
  if not d[c].between(0,3650).all(): raise ValueError('Invalid shipping duration')
 if (d.groupby(C[0])[C[1:]].nunique()>1).any().any(): raise ValueError('Conflicting shipping values within order')
 orders=d.drop_duplicates(C[0]).copy();orders['delay']=orders[C[2]]-orders[C[3]];orders['over_schedule']=orders.delay>0
 summary=orders.groupby(C[1]).agg(orders=(C[0],'size'),over_schedule=('over_schedule','sum'),mean_actual=(C[2],'mean'),mean_scheduled=(C[3],'mean'),mean_delay=('delay','mean'))
 summary['over_schedule_rate']=summary.over_schedule/summary.orders
 distribution=orders.delay.value_counts().sort_index().rename_axis('delay_days').rename('orders')
 metrics=dict(input_rows=len(d),unique_orders=len(orders),repeated_order_rows=len(d)-len(orders),over_schedule_orders=int(orders.over_schedule.sum()))
 return summary,distribution,metrics
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--output',default='results');a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 s,d,m=analyze(pd.read_csv(a.input));s.to_csv(out/'shipping_modes.csv');d.to_csv(out/'delay_distribution.csv');(out/'summary.json').write_text(json.dumps(m,indent=2));print(m)
