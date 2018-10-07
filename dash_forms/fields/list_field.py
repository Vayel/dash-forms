import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .field import Field


class ListField(Field):
    def __init__(self, id_builder, *args, options, **kwargs):
        self.options = options
        if 'default' not in kwargs:
            kwargs['default'] = self.options[0]['value']
        super().__init__(id_builder, *args, **kwargs)

    @Field.default.setter
    def default(self, val):
        if val not in [option['value'] for option in self.options]:
            raise ValueError("No option with value '{0}' in {1}.".format(
                val,
                self.id_builder()
            ))
        self.default_ = val

    def render_input(self):
        return dcc.Dropdown(
            options=self.options,
            value=self.default,
            id=self.id_builder('value'),
            searchable=False,
            clearable=False,
        )
