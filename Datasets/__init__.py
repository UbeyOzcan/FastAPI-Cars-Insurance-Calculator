import pandas as pd
import os


def get_data() -> pd.DataFrame:
    path = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(path, "frenchmtpl_clean.csv"), sep=';')
    df.drop(['IDpol'], axis=1, inplace=True)
    df = df.groupby(
        ['VehPower', 'VehAge', 'DrivAge', 'BonusMalus', 'VehBrand', 'VehGas', 'Area', 'Density', 'Region']).agg(
        {'ClaimNb': 'sum', 'Exposure': 'sum', 'ClaimAmount': 'sum'}).reset_index()
    return df
