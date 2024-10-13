from Datasets import get_data
import pandas as pd
pd.set_option('display.max_columns', 500)
df = get_data()

# ============================== #
#    Claim Count Distribution    #
# ============================== #

claim_count_distribution = df.groupby('IDpol').agg({'ClaimNb': 'sum', 'Exposure': 'sum'}).reset_index()
claim_count_distribution = claim_count_distribution[claim_count_distribution.ClaimNb < 5]
claim_count_distribution = claim_count_distribution.groupby('ClaimNb').agg({'Exposure': 'sum'}).reset_index()
claim_count_distribution['Exposure'] = round(claim_count_distribution['Exposure'], 2)
claim_count_distribution['Empirical Probability'] = claim_count_distribution['Exposure'] / claim_count_distribution[
    'Exposure'].sum()

# ==================================== #
# The (a, b, 0) class of distributions #
# ==================================== #
claim_count_distribution['lhs'] = 0
for i in range(len(claim_count_distribution.index)):
    if i == 0:
        pass
    else:
        claim_count_distribution.loc[i, 'lhs'] = (i * claim_count_distribution.loc[i, 'Empirical Probability']) / \
                                                 claim_count_distribution.loc[i - 1, 'Empirical Probability']

print(claim_count_distribution)
# ============================== #
# Summary Frequency and Severity #
# ============================== #


Exposure = round(df['Exposure'].sum(), 2)
n_claims = round(df['ClaimNb'].sum(), 2)
claim_amount = round(df['ClaimAmount'].sum(), 2)

frequency = round(n_claims / Exposure, 2)
var_frequency = round(sum((df['ClaimNb'] - (frequency * df['Exposure'])) ** 2) / sum(df['Exposure']), 2)
severity = round(claim_amount / n_claims, 2)

summary = pd.DataFrame({'Exposure': [Exposure],
                        'Number of Claims': [n_claims],
                        'Claim Amount': [claim_amount],
                        'Frequency': [frequency],
                        'Frequency Variance': [var_frequency],
                        'Severity': [severity],
                        'Risk Premium': [round(frequency * severity, 2)]})

print(summary)