from Datasets import get_data
import pandas as pd
import json

df = get_data()
rfs = ['VehPower', 'VehAge', 'DrivAge', 'BonusMalus', 'VehBrand', 'VehGas', 'Area', 'Density', 'Region']
# rfs = ['VehGas', 'Area']
base_level = {'Frequency': {},
              'Severity': {}}
for i in rfs:
    uni = df.groupby(i).agg({'ClaimNb': 'sum', 'Exposure': 'sum'})
    base_freq = uni['Exposure'].idxmax()
    base_sev = uni['ClaimNb'].idxmax()
    print(f'Base Freq {base_freq} and Base Sev {base_sev}')
    base_level['Frequency'][i] = f'{base_freq}'
    base_level['Severity'][i] = f'{base_sev}'

with open('base_level.json', 'w') as fp:
    json.dump(base_level, fp)
