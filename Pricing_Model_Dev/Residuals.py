from sklearn.model_selection import train_test_split
import joblib
import pandas as pd
from Datasets import get_data

df = get_data()

# frequency train test
train, test = train_test_split(df, test_size=0.3, random_state=1990)

frequency = joblib.load('Frequency.joblib')
severity = joblib.load('Severity.joblib')
