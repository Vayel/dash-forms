import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as dhtml

from ..exceptions import FieldValidationError


def _save_args(f):
    def wrapper(self, *args, **kwargs):
        f(self, *args, **kwargs)
        self._init_args = args
        self._init_kwargs = kwargs
    return wrapper


class _FieldMetaclass(type):

    def __new__(meta, name, bases, attrs):
        if '__init__' in attrs:
            attrs['__init__'] = _save_args(attrs['__init__'])
        return super().__new__(meta, name, bases, attrs)


class Field(metaclass=_FieldMetaclass):

    def __init__(self, label=None, *, default=None, required=True, auto_validate=True):
        self.label = label
        self.required = required
        self._default = default
        self.chained_id = None
        self.auto_validate = auto_validate

    @property
    def component_id(self):
        return str(self.chained_id)

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, val):
        # To be overwritten by subclasses that want to make checks
        self._default = val

    def validate(self, data):
        if self.required and (None in data or '' in data):
            raise FieldValidationError('This field is required.')
        return data if len(data) > 1 else data[0]

    def dependencies(self, cls=Input):
        return [cls(self.chained_id('value'), 'value'),]

    def render_input(self):
        return dcc.Input(type='text', value=str(self.default), id=self.chained_id('value'))

    def render(self):
        if self.label is not None:
            input_row = dhtml.Div([
                dhtml.Div(self.label, className='field_label'),
                dhtml.Div(self.render_input(), className='field_input'),
            ], id=self.chained_id('row'), className='field_row')
        else:
            input_row = dhtml.Div(
                dhtml.Div(self.render_input(), className='field_input one_col'),
                id=self.chained_id('row'),
                className='field_row',
            )

        return dhtml.Div([
            input_row,
            dhtml.Div(
                dhtml.Div(className='errors', id=self.chained_id('errors')),
                id=self.chained_id('errors_wrapper'),
                className='field_errors_row',
            ),
        ])

    def serialize(self, cleaned_data):
        return cleaned_data

    def bind_callbacks(self, app):
        if not self.auto_validate:
            return

        validation_dependencies = self.dependencies()
            
        @app.callback(
            Output(self.chained_id('errors_wrapper'), 'style'),
            validation_dependencies,
        )
        def display_errors(*args):
            display = 'none'
            try:
                self.validate(args)
            except FieldValidationError as e:
                display = 'block'
            return {'display': display}
        
        @app.callback(
            Output(self.chained_id('errors'), 'children'),
            validation_dependencies,
        )
        def print_errors(*args):
            try:
                self.validate(args)
            except FieldValidationError as e:
                return str(e)
