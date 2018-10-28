import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .field import Field
from .float_field import FloatField
from .int_field import IntField
from ..exceptions import FieldValidationError


class IntervalField(Field):

    def __init__(self, id_builder, *args, min=None, max=None, different=True, default=None,
                 required=None, is_int=False, **kwargs):

        if default is None:
            default = [None, None]
        if required is None:
            required = [None, None]
        self.different = different

        field_cls = FloatField if not is_int else IntField

        self.low_field = field_cls(
            id_builder.add('low'),
            'Low',
            min=min,
            required=required[0],
            default=default[0],
            validation_dependencies=None,
        )
        self.high_field = field_cls(
            id_builder.add('high'),
            'High',
            max=max,
            required=required[1],
            default=default[1],
            validation_dependencies=None,
        )

        super().__init__(id_builder, *args, default=default, required=required, **kwargs)

    @Field.default.setter
    def default(self, val):
        self.low_field.default = val[0]
        self.high_field.default = val[1]

    def dependencies(self, cls=dInput):
        return self.low_field.dependencies(cls=cls) + self.high_field.dependencies(cls=cls)

    def render_input(self):
        return dhtml.Div([
            dhtml.Label('[ '),
            self.low_field.render_input(),
            dhtml.Label(' , '),
            self.high_field.render_input(),
            dhtml.Label(' ]'),
        ], className='interval_field')

    def validate(self, data):
        low = self.low_field.validate([data[0]])
        high = self.high_field.validate([data[1]])

        if low is None or high is None:
            return low, high

        if low > high:
            raise FieldValidationError('The lower bound cannot be greater than the upper bound.')
        if self.different and low == high:
            raise FieldValidationError('The bounds cannot be equal.')

        return low, high
