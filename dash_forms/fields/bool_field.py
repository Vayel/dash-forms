import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from ..exceptions import FieldValidationError
from .field import Field


class BoolField(Field):
    def render_input(self):
        return dcc.Checklist(
            options=[{'label': '', 'value': 'is_checked'}],
            values=['is_checked'] if self.default else [],
            id=self.get_id('value'),
        )

    def validate(self, data):
        data = super().validate(data)
        return data.get('is_checked', False)
