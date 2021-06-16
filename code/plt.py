from plotly import graph_objs as go
import pandas


df = pandas.DataFrame([['1', '2', '3', '4'],
                        [9.525, 9.525, 9.525, 9.525],
                        [50.08, 0.0, 0.0, 50.08],
                        [50.08, 50.08, 0.0, 0.0],
                        [2.6, 2.0, 1.0, 2.0],
                        [1.0, 2.6, 1.0, 2.6],
                        [1.0, 1.0, 2.6, 1.0],
                        [1.0, 1.0, 1.0, 1.0]],
                        columns=['name', 'diameter', 'x-pos', 'y-pos'])
print(df)

fig = go.Figure(data=[go.Table(header=dict(values=list(df.columns), fill_color='paleturquoise', align='left'),
    cells=dict(values=[df.Rank, df.State, df.Postal, df.Population],
               fill_color='lavender',
               align='left'))
])

fig.show()
