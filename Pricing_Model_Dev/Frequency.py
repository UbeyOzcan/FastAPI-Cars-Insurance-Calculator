from sklearn.model_selection import train_test_split
from Datasets import get_data
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import joblib
df = get_data()

# frequency train test
train, test = train_test_split(df, test_size=0.3, random_state=1990)
train = df.loc[train.index].copy()
test = df.loc[test.index].copy()

expr = "ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus  + VehGas + Area "

FreqPoisson = smf.glm(formula=expr,
                      data=train,
                      offset=np.log(train['Exposure']),
                      family=sm.families.Poisson(link=sm.families.links.log())).fit()

joblib.dump(FreqPoisson, 'Frequency.joblib')

