from sklearn.model_selection import train_test_split
from Datasets import get_data
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 12})

df = get_data()

# frequency train test
train, test = train_test_split(df, test_size=0.3, random_state=1990)
train = df.loc[train.index].copy()
test = df.loc[test.index].copy()

# severity train test
train_severity = train.loc[train['ClaimNb'] > 0].copy()
train_severity['Severity'] = train_severity['ClaimAmount'] / train_severity['ClaimNb']
test_severity = test.loc[test['ClaimNb'] > 0].copy()
test_severity['Severity'] = test_severity['ClaimAmount'] / test_severity['ClaimNb']

mu = df.ClaimNb.mean()
var = np.mean([abs(x - mu) ** 2 for x in df.ClaimNb])
print(f'mu =  {mu:.4f}\nvar = {var:.4f}')

# # examples of formula notation in smf
# print(' + '.join(train.columns))
# expr = "Claims ~ Age+C(Sex)+C(Geog, Treatment(reference=3))+EV+VehAge+NCD"

# including PYrs as parameter commented out in glm()
expr = "ClaimNb ~ VehPower + VehAge + DrivAge + BonusMalus"  # + np.log(PYrs)

FreqPoisson = smf.glm(formula=expr,
                      data=train,
                      offset=np.log(train['Exposure']),
                      family=sm.families.Poisson(link=sm.families.links.log())).fit()

print(FreqPoisson.summary())

fig, axs = plt.subplots(1, 1)

bins = np.arange(0, 10, 1)
n = 1000
print(
    f'Lambda intercept: {np.exp(FreqPoisson.params[0]):.2f}\nLambda intercept + male: {np.exp(FreqPoisson.params[0] + FreqPoisson.params[1]):.2f}')

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

# including PYrs as parameter commented out in glm()
expr = "Severity ~ VehPower + VehAge + DrivAge + BonusMalus"

### Estimate severity using GLM-gamma with default inverse-power link
SevGamma = smf.glm(formula=expr,
                   data=train_severity,
                   family=sm.families.Gamma(link=sm.families.links.log())).fit()

# dispersion aka rate
dispersion = SevGamma.scale
print(f'Dispersion: {dispersion:.4f}')

# shape is 1/dispersion
shape = 1/dispersion
print(f'Shape: {shape:.4f}')

# intercept
constant,intercept = SevGamma.params[0],np.exp(SevGamma.params[0])
print(f'Intercept: {intercept:.2f}')

# predicted mean G(Yi) is exp(Bo + Bi*Xi..)
# tuple(name,Yi,scale)
geogs = [(i,
          np.exp(constant+c),
          np.exp(constant+c)*dispersion)
         for i,c in zip(SevGamma.params.index,SevGamma.params) if 'Geog' in i]

# plot
fig,axs = plt.subplots(1,4,sharex=True,sharey=True,figsize=(13,3))

for ax,x in zip(axs.flatten(),geogs):
    sns.kdeplot(np.random.gamma(shape=shape,scale=x[2],size=10000),shade=True,ax=ax,)
    ax.set_title(x[0])
plt.show()