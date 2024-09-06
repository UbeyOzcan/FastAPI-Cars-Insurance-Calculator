from Datasets import get_data
from matplotlib import pyplot as plt
import pandas as pd
from fitter import Fitter, get_common_distributions
import seaborn as sns
import plotly.express as px
df = px.data.tips()
fig = px.histogram(df, x="total_bill")
fig.show()
df = get_data()
# ============================== #
# Summary Frequency and Severity #
# ============================== #


Exposure = round(df['Exposure'].sum(), 2)
n_claims = round(df['ClaimNb'].sum(), 2)
claim_amount = round(df['ClaimAmount'].sum(), 2)

frequency = round(n_claims / Exposure, 2)
severity = round(claim_amount / n_claims, 2)

summary = pd.DataFrame({'Exposure': [Exposure],
                        'Number of Claims': [n_claims],
                        'Claim Amount': [claim_amount],
                        'Frequency': [frequency],
                        'Severity': [severity],
                        'Risk Premium': [round(frequency * severity, 2)]})
print(summary)

Claim_amount = df[df['ClaimAmount'] > 0]['ClaimAmount']
df_claim = df[(df['ClaimAmount'] > 100) & (df['ClaimAmount'] < 10000)]

sns.histplot(df_claim['ClaimAmount'])
plt.show()
exit()
f = Fitter(Claim_amount,
           distributions=['gamma',
                          'lognorm',
                          "beta",
                          "burr",
                          "norm"])
f.fit()
print(f.summary())
