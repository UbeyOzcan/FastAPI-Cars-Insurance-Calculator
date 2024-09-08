from sklearn.model_selection import train_test_split
from Datasets import get_data
import statsmodels.api as sm
import statsmodels.formula.api as smf
import joblib

df = get_data()
df = df[(df.ClaimNb > 0) & (df.ClaimNb < 5)]
df['Severity'] = df.ClaimAmount / df.ClaimNb
# frequency train test
train, test = train_test_split(df, test_size=0.3, random_state=1990)
train = df.loc[train.index].copy()
test = df.loc[test.index].copy()

expr = "ClaimAmount ~ VehPower + VehAge + DrivAge + BonusMalus  + VehGas + Area "

SevGamma = smf.glm(formula=expr,
                   data=train,
                   offset=train.ClaimNb,
                   family=sm.families.Gamma(link=sm.families.links.log())).fit()

joblib.dump(SevGamma, 'Severity.joblib')
