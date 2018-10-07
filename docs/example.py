import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from dash_forms import Form, fields, ComponentId, ValidationError


class SumForm(Form):
    def __init__(self, comp_id=None):
        if comp_id is None:
            comp_id = ComponentId('my_form')

        children = [
            fields.IntField(comp_id.add('val1'), label='a', default=1,),
            fields.IntField(comp_id.add('val2'), label='b', default=1,),
        ]

        super().__init__(comp_id, children, btn_text='Go!')

    def validate(self, data):
        cleaned_data = super().validate(data)
        cleaned_data['res'] = cleaned_data['val1'] + cleaned_data['val2']
        return cleaned_data


app = dash.Dash(__name__)
form = SumForm()
app.layout = html.Div([
    form.render(),
    html.Div(id='output'),
])
form.bind_callbacks(app)

@app.callback(
    Output('output', 'children'),
    [form.btn_dependency()],
    form.dependencies(cls=State)
)
def update(n_clicks, *args):
    if n_clicks is None:
        return

    try:
        cleaned_data = form.validate(args)
    except ValidationError as e:
        return 'Error: {0}'.format(e)
    else:
        return '{0} + {1} = {2}'.format(cleaned_data['val1'], cleaned_data['val2'],
                                        cleaned_data['res'])

if __name__ == '__main__':
    app.run_server(debug=True)
