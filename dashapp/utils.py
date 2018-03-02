import numpy as np
from layout import app
import plotly.graph_objs as go


def make_graph(data):
    trace = []
    for d, tracename in data:
        trace.append(go.Scatter(
            y=np.ravel(d),
            x=np.arange(len(d)),
            mode='lines',
            name = tracename
        ))

    layout=go.Layout(
        height=300,
        xaxis={
            'title': 'year',
        },
        yaxis={
            'title': 'grunt '
        },
        margin = {'l': 40, 'b': 40, 't': 10, 'r': 40},
        showlegend=False
    )

    return {'data': trace, 'layout': layout}

