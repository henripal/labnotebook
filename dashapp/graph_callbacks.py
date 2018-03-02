from dash.dependencies import Input, Output, State
import numpy as np
import xpbase
from layout import app
from utils import make_graph
from tables import experiments, steps


    


@app.callback(
    Output('accuracies', 'figure'),
    [Input('run-input', 'value'),
    Input('compare-input', 'value'),
    Input('training-loss-update', 'n_intervals')]
)
def update_accs(run_number, compare_input, n_intervals):
    results = []
    for rn in [run_number, compare_input]:
        if rn:
            trainacc = xpbase.session.query(steps.trainacc).filter(
                steps.run_id == rn).all()
            valacc = xpbase.session.query(steps.valacc).filter(
                steps.run_id == rn).all()
            n = len(trainacc)
            results.append((trainacc, 'train run ' + str(rn)))
            results.append((valacc, 'val run' + str(rn)))
            
    
    return make_graph(results)
        
    
@app.callback(
    Output('losses', 'figure'),
    [Input('run-input', 'value'),
    Input('compare-input', 'value'),
    Input('training-loss-update', 'n_intervals')]
)
def update_losses(run_number, compare_input, n_intervals):
    results = []
    
    for rn in [run_number, compare_input]:
        if rn:
            losses = xpbase.session.query(steps.trainloss).filter(
                steps.run_id == rn).all()
            n = len(losses)
            results.append((losses, 'losses run ' + str(rn)))
    
    return make_graph(results)
    

@app.callback(
    Output('histogram', 'figure'),
    [Input('run-input', 'value'),
    Input('compare-input', 'value'),
    Input('dropdown', 'value')]
)
def update_histogram(run_number, compare_number, layer_name):
    results = []
    
    for rn in [run_number, compare_number]:
        if rn:
            histogram_data = xpbase.session.query(steps.model_params).filter(
                steps.run_id == rn).order_by(steps.step_id.desc()).first()
            histogram, buckets = np.histogram(histogram_data[0]['statedict'][layer_name])
            results.append((histogram, 'hist run ' + str(rn)))

    
    return make_graph(results)

import plotly.plotly as py
from plotly.graph_objs import *

@app.callback(
    Output('variances', 'figure'),
    [Input('button', 'n_clicks')],
    [State('run-input', 'value'),
    State('compare-input', 'value')]
)
def make_variances(n_clicks, run_number, compare_number):
    """
    will compute the historical median and max variance for params,
    and store in hidden div
    """
    results = []
    
    for rn in [run_number, compare_number]:
        if rn:
            median_data = xpbase.session.query(
                steps.model_params['std_median']).filter(
                    steps.run_id == rn).all()
            max_data = xpbase.session.query(
                steps.model_params['std_max']).filter(
                    steps.run_id == rn).all()
            
            results.append((median_data, 'median std run ' + str(run_number)))
            results.append((max_data, 'max std run ' + str(run_number)))
        
    
    return make_graph(results)
    
    
    

