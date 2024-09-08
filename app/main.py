from fastapi import FastAPI
import pandas as pd
import joblib
from pathlib import Path

app = FastAPI()


@app.get("/")
async def premium(power: int = None,
                  vehicle_age: int = None,
                  driver_age: int = None,
                  bonus_malus: int = None,
                  vehicle_gas: str = None,
                  area: str = None):
    root = Path(__file__).parent.parent
    frequency = joblib.load(f'{root}/Pricing_Model_Dev/Frequency.joblib')
    severity = joblib.load(f'{root}/Pricing_Model_Dev/Severity.joblib')
    single_profile = {'VehPower': [power],
                      'VehAge': [vehicle_age],
                      'DrivAge': [driver_age],
                      'BonusMalus': [bonus_malus],
                      'VehGas': [vehicle_gas],
                      'Area': [area]}
    single_profile = pd.DataFrame.from_dict(single_profile)
    single_profile['Predicted Frequency'] = frequency.predict(single_profile)
    single_profile['Predicted Severity'] = severity.predict(single_profile)
    single_profile['Predicted Frequency'] = round(single_profile['Predicted Frequency'], 4)
    single_profile['Predicted Severity'] = round(single_profile['Predicted Severity'], 2)
    single_profile['Risk Premium'] = round(single_profile['Predicted Frequency'] * single_profile['Predicted Severity'],
                                           2)
    single_profile = single_profile.to_dict('list')

    return single_profile
