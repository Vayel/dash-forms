import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from ..exceptions import FieldValidationError


class Field:
    def __init__(self, id_builder, label=None, default=None, required=True,
                 validation_dependencies='self'):
        self.id_builder = id_builder
        self.label = label
        self.required = required
        self.default = default
        self.validation_dependencies = []
        if validation_dependencies == 'self':
            self.validation_dependencies = self.dependencies()
        elif validation_dependencies is not None:
            self.validation_dependencies = validation_dependencies

    @property
    def default(self):
        return self.default_

    @default.setter
    def default(self, val):
        self.default_ = val

    def validate(self, data):
        if self.required and (None in data or '' in data):
            raise FieldValidationError('This field is required.')
        return data if len(data) > 1 else data[0]

    def dependencies(self, cls=dInput):
        return [cls(self.id_builder('value'), 'value'),]

    def render_input(self):
        return dcc.Input(type='text', value=str(self.default), id=self.id_builder('value'))

    def render(self):
        if self.label is not None:
            input_row = dhtml.Div([
                dhtml.Div(self.label, className='field_label'),
                dhtml.Div(self.render_input(), className='field_input'),
            ], id=self.id_builder('row'), className='field_row')
        else:
            input_row = dhtml.Div(
                dhtml.Div(self.render_input(), className='field_input one_col'),
                id=self.id_builder('row'),
                className='field_row',
            )

        return dhtml.Div([
            input_row,
            dhtml.Div(
                dhtml.Div(className='errors', id=self.id_builder('errors')),
                id=self.id_builder('errors_wrapper'),
                className='field_errors_row',
            ),
        ])

    def serialize(self, cleaned_data):
        return cleaned_data

    def bind_callbacks(self, app):
        if self.validation_dependencies:
            @app.callback(
                dOutput(self.id_builder('errors_wrapper'), 'style'),
                self.validation_dependencies,
            )
            def display_errors(*args):
                display = 'none'
                try:
                    self.validate(args)
                except FieldValidationError as e:
                    display = 'block'
                return {'display': display}
            
            @app.callback(
                dOutput(self.id_builder('errors'), 'children'),
                self.validation_dependencies,
            )
            def print_errors(*args):
                try:
                    self.validate(args)
                except FieldValidationError as e:
                    return str(e)
