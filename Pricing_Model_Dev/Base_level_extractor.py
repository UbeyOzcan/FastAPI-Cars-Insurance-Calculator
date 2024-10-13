from Datasets import get_data
import pandas as pd

pd.set_option('display.max_columns', 500)
df = get_data()
# rfs = ['VehPower', 'VehAge', 'DrivAge', 'BonusMalus', 'VehBrand', 'VehGas', 'Area', 'Density', 'Region']
rfs = ['VehGas', 'Area']
base_level = {'Frequency': {},
              'Severity': {}}
for i in rfs:
    uni = df.groupby(i).agg({'ClaimNb': 'sum', 'Exposure': 'sum'})
    base_freq = uni['Exposure'].idxmax()
    base_sev = uni['ClaimNb'].idxmax()
    base_level['Frequency'][i] = base_freq
    base_level['Severity'][i] = base_sev

print(base_level)
