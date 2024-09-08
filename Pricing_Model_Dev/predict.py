import joblib
import pandas as pd
from pathlib import Path

pd.set_option('display.max_columns', 500)

frequency = joblib.load('Frequency.joblib')
severity = joblib.load('Severity.joblib')

single_profile = {'VehPower': [10],
                  'VehAge': [0],
                  'DrivAge': [30],
                  'BonusMalus': [50],
                  'VehGas': ['Regular'],
                  'Area': ['F']}

single_profile = pd.DataFrame.from_dict(single_profile)
root = Path(__file__).parent.parent
print(root)
single_profile['expected_freq'] = frequency.predict(single_profile)
single_profile['expected_sev'] = severity.predict(single_profile)

single_profile['RP'] = single_profile['expected_freq'] * single_profile['expected_sev']
single_profile = single_profile.to_dict('list')
print(single_profile)
