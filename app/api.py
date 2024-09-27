from enum import Enum
from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI


class Area(str, Enum):
    D = "D"
    B = "B"
    E = "E"
    C = "C"
    F = "F"
    A = "A"


class Gas(str, Enum):
    Regular = "Regular"
    Diesel = "Diesel"


app = FastAPI()



@app.get("/")
async def root(power: int,
               VehAge: int,
               DrivAge: int,
               BonusMalus: int,
               VehGas: Gas,
               Area: Area):
    root = Path(__file__).parent.parent
    frequency = joblib.load(f'{root}/Pricing_Model_Dev/Frequency.joblib')
    severity = joblib.load(f'{root}/Pricing_Model_Dev/Severity.joblib')

    single_profile = {'VehPower': [power],
                      'VehAge': [VehAge],
                      'DrivAge': [DrivAge],
                      'BonusMalus': [BonusMalus],
                      'VehGas': [VehGas.name],
                      'Area': [Area.name]}
    single_profile = pd.DataFrame.from_dict(single_profile)
    single_profile['Predicted Frequency'] = frequency.predict(single_profile)
    single_profile['Predicted Severity'] = severity.predict(single_profile)
    single_profile['Predicted Frequency'] = round(single_profile['Predicted Frequency'], 4)
    single_profile['Predicted Severity'] = round(single_profile['Predicted Severity'], 2)
    single_profile['Risk Premium'] = round(single_profile['Predicted Frequency'] * single_profile['Predicted Severity'],
                                           2)
    single_profile = single_profile.to_dict('list')

    return single_profile



