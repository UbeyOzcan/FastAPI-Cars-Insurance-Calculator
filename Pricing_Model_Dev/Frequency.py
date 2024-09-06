from sklearn.model_selection import train_test_split
from Datasets import get_data
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib import pyplot as plt
import seaborn as sns

df = get_data()

summary = df.groupby('ClaimNb').agg({'Exposure': 'sum'})
print(summary)
# frequency train test
train, test = train_test_split(df, test_size=0.3, random_state=1990)
train = df.loc[train.index].copy()
test = df.loc[test.index].copy()

mu = df.ClaimNb.mean()
var = np.mean([abs(x - mu) ** 2 for x in df.ClaimNb])
print(f'mu =  {mu:.4f}\nvar = {var:.4f}')

# # examples of formula notation in smf
# print(' + '.join(train.columns))
# expr = "Claims ~ Age+C(Sex)+C(Geog, Treatment(reference=3))+EV+VehAge+NCD"

# including PYrs as parameter commented out in glm()
expr = "ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus + VehBrand + VehGas + Area + Density + Region"

FreqPoisson = smf.glm(formula=expr,
                      data=train,
                      offset=np.log(train['Exposure']),
                      family=sm.families.Poisson(link=sm.families.links.log())).fit()

print(FreqPoisson.summary())

fig, axs = plt.subplots(1, 1)

bins = np.arange(0, 10, 1)
n = 1000
print(
    f'Lambda intercept: {np.exp(FreqPoisson.params[0]):.4f}\nLambda intercept + male: {np.exp(FreqPoisson.params[0] + FreqPoisson.params[1]):.4f}')

print(np.exp(FreqPoisson.params[0]))
exit()
axs.hist(np.random.poisson(lam=np.exp(FreqPoisson.params[0]), size=n),
         bins=bins, rwidth=0.1,
         alpha=1, label='intercept', align='left', color='k')

axs.hist(np.random.poisson(lam=np.exp(FreqPoisson.params[0] + FreqPoisson.params[1]), size=n),
         bins=bins, rwidth=0.5,
         alpha=0.5, label='intercept + Bi', align='left')
axs.set_xticks(bins)
axs.legend()
plt.show()

# get prediction to access easy confidence intervals
gp = FreqPoisson.get_prediction(test)

test['Fpo'] = FreqPoisson.predict(transform=True, exog=test, offset=np.log(test['Exposure']))

fig, axs = plt.subplots(1, 1, figsize=(13, 3.3), sharex=False, sharey=True)
sns.histplot(test['Fpo'], ax=axs, label='Poisson')
plt.show()
