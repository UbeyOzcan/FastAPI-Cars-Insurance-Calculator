from Datasets import get_data
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pd.set_option('display.max_columns', 500)
df = get_data()
dict_uni = {'Freqency': None, 'Severity': None}
#rfs = ['VehPower', 'VehAge', 'DrivAge', 'BonusMalus', 'VehBrand', 'VehGas', 'Area', 'Density', 'Region']
rfs = [ 'VehGas', 'Area']
for i in rfs:
    uni = df.groupby(i).agg({'ClaimNb': 'sum', 'Exposure': 'sum', 'ClaimAmount': 'sum'}).reset_index()
    print(uni)
    uni['Frequency'] = uni['ClaimNb'] / uni['Exposure']
    uni['Severity'] = uni['ClaimAmount'] / uni['ClaimNb']
    for j in ['Frequency', 'Severity']:
        weight = 'Exposure' if j == 'Frequency' else 'ClaimNb'
        trace1 = go.Bar(
            x=uni[i],
            y=uni['Exposure' if j == 'Frequency' else 'ClaimNb'],
            name='Exposure' if j == 'Frequency' else 'ClaimNb',
            marker=dict(
                color='rgb(34,163,192)'
            )
        )
        trace2 = go.Scatter(
            x=uni[i],
            y=uni[j],
            name=f'Claim {j}',
            yaxis='y2'

        )

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(trace1)
        fig.add_trace(trace2, secondary_y=True)
        fig['layout'].update(height=600, width=800, title=f'Claim {j} and {weight}', xaxis=dict(
            tickangle=-90))
        fig.update_layout(plot_bgcolor='white')
        fig.update_xaxes(title_text=i)
        fig.update_yaxes(title_text='Exposure' if j == 'Frequency' else 'ClaimNb')
        fig.update_yaxes(title_text=j, secondary_y=True)
        fig.write_image(f'plot/plot {j} for {i}.png')
