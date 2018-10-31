import json

import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html

from dash_forms import Form, fields, ValidationError


class SumForm(Form):
    left = fields.IntField('a', default=1,)
    right = fields.IntField('b', default=1,)

    def validate(self, data):
        cleaned_data = super().validate(data)
        cleaned_data['res'] = cleaned_data['left'] + cleaned_data['right']
        return cleaned_data


app = dash.Dash(__name__)
form = SumForm('Go')
form2 = SumForm('Go2')
app.layout = html.Div([
    form.render(),
    html.Div(id='output'),
    form2.render(),
    html.Div(id='output2'),
])
form.bind_callbacks(app)
form2.bind_callbacks(app)


@app.callback(
    Output('output', 'children'),
    [form.btn_dependency()],
    form.dependencies()
)
def update(n_clicks, *form_args):
    if n_clicks is None:
        return

    try:
        cleaned_data = form.validate(form_args)
    except ValidationError as e:
        return 'Error: {0}'.format(e)
    else:
        return '{0} + {1} = {2}'.format(cleaned_data['left'], cleaned_data['right'],
                                        cleaned_data['res'])


@app.callback(
    Output('output2', 'children'),
    [form2.btn_dependency()],
    form2.dependencies()
)
def update(n_clicks, *form_args):
    if n_clicks is None:
        return

    try:
        cleaned_data = form2.validate(form_args)
    except ValidationError as e:
        return 'Error: {0}'.format(e)
    else:
        return '{0} + {1} = {2}'.format(cleaned_data['left'], cleaned_data['right'],
                                        cleaned_data['res'])


if __name__ == '__main__':
    app.run_server(debug=True)
