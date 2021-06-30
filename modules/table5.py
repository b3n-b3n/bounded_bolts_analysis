import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = {
    'ID number': ['1', '2', '3', '4'],
    'd [mm]': [9.525, 9.525, 9.525, 9.525],
    'Fx [N]': [-8.022, -6.171, -3.086, -6.171],
    'Fy [N]': [33.03, 25.408, 12.704, 25.408],
    'F [N]': [33.99, 26.15, 13.07, 26.15],
    'τ [MPa]': [254.28, 195.63, 97.78, 195.63],
    'RF [-]': [0.39, 1.03, 0.01, 1.03],
    'σ1 [MPa]': [3.57, 2.75, 0.53, 2.75],
    'RF1 [-]': [0.28, 0.36, 1.89, 0.36],
    'σ2 [MPa]': [3.57, 2.75, 0.01, 2.75],
    'RF2 [-]': [0.28, 0.36, 100.0, 0.36]
}


column_names = ['<b>' + name + '</b>' for name in list(list(data.keys()))]
val = list(data[col] for col in list(data.keys()))


fig = make_subplots(rows=2, cols=1)
fig.append_trace(go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ]), row=1, col=1)
fig.append_trace(go.Figure(data=[go.Table(header=dict(values=['A Scores', 'B Scores']),
                 cells=dict(values=[[100, 90, 80, 90], [95, 85, 75, 95]]))
                     ]), row=2, col=1)
fig.show()

