import pandas as pd
import os


def get_data() -> pd.DataFrame:
    path = os.path.dirname(__file__)
    df = pd.read_csv(os.path.join(path, "frenchmtpl_clean.csv"), sep=';')
    return df
