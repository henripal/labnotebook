import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()

colors = {'title_background': '#3F51B5',
         'menu_background': '#E8EAF6'}

app.css.append_css({"external_url": "https://codepen.io/ricetuna/pen/QQJXed.css"})


app.layout = html.Div(className='container', children=[
    html.Div(className='row', children=[
        html.Div(className='twelve columns',
                 children=html.H4('xpbase'),
                 style={'background-color': colors['title_background'], 'color': 'white'})
    ]),
    html.Div(className='row', children=[
        html.Div(className='two columns', children='Run Id:'),
        dcc.Input(className= 'one columns', id='run-input', type='number', value=32),
        html.Div(className='four columns', id='runinfo'),
        dcc.Dropdown(className='two columns', id='dropdown', options=[], value='fc1.bias'),
        html.Button(className='two columnes', children='PRESS ME', id='button')
    ]),
    html.Div(className='row', children=[
        html.Div(className='two columns', children='Compare To:'),
        dcc.Input(className='one columns', id='compare-input', type='number', value=None),
        html.Div(className='four columns', id='compareinfo')
    ]),
    html.Div(className='row', children=[
        html.Div(className='four columns', children=[
            dcc.Graph(id='accuracies', config={'displayModeBar': False}),
            dcc.Graph(id='losses', config={'displayModeBar': False}),
            dcc.Interval(id='training-loss-update', interval=2000, n_intervals=0)
        ]),
        html.Div(className='four columns', children=[
            dcc.Graph(id='histogram', config={'displayModeBar': False}),
            dcc.Graph(id='variances'),
        ])
    ]),
])
