"""Load group/value CSV input with strict row validation."""
import csv
import math

def read_samples(path):
    groups={'A':[],'B':[]}
    with open(path,newline='') as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames != ['group','value']:
            raise ValueError('CSV columns must be group,value in that order')
        for line,row in enumerate(reader,2):
            if row.get('group') not in groups or None in row:
                raise ValueError(f'Invalid group or column count on line {line}')
            try: value=float(row['value'])
            except (ValueError,TypeError): raise ValueError(f'Invalid value on line {line}')
            if not math.isfinite(value): raise ValueError(f'Nonfinite value on line {line}')
            groups[row['group']].append(value)
    return groups['A'],groups['B']
