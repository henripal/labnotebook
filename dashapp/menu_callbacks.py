from dash.dependencies import Input, Output
import xpbase
from layout import app
from tables import experiments, steps



@app.callback(
    Output('dropdown', 'options'),
    [Input('run-input', 'value')]
)
def update_dropdown_values(run_number):
    histogram_data = xpbase.session.query(steps.model_params).filter(
        steps.run_id == run_number).order_by(steps.step_id.desc()).first()
    return [{'label': label, 'value': label} for label in histogram_data[0]['statedict'].keys()]
    
    

@app.callback(
    Output('runinfo', 'children'),
    [Input('run-input', 'value')]
)
def update_info(run_number):
    if run_number:
        xp = xpbase.session.query(experiments).filter(
            experiments.run_id == run_number).one()

        return xp.__str__()
    return ''

@app.callback(
    Output('compareinfo', 'children'),
    [Input('compare-input', 'value')]
)
def update_compareinfo(run_number):
    if run_number:
        xp = xpbase.session.query(experiments).filter(
            experiments.run_id == run_number).one()

        return xp.__str__()
    return ''

    

