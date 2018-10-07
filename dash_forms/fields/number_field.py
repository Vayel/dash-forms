import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from ..exceptions import FieldValidationError
from .field import Field


class NumberField(Field):
    parse = float

    def __init__(self, *args, min=None, max=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.min = min
        self.max = max

    def validate(self, data):
        x = super().validate(data)
        if x is None or x == '':
            return

        try:
            x = self.parse(x)
        except ValueError:
            raise FieldValidationError('The value must be a number.')
            
        if self.min is not None and x < self.min:
            raise FieldValidationError('The value cannot be lower than {0}.'.format(self.min))
        if self.max is not None and x > self.max:
            raise FieldValidationError('The value cannot be greater than {0}.'.format(self.max))

        return x
