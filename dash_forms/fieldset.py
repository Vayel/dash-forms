from functools import partial

import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .container import Container
from .exceptions import FieldsetValidationError


class Fieldset(Container):
    caught_exception = FieldsetValidationError

    def __init__(self, *args, required=None, **kwargs):
        super().__init__(*args, **kwargs)
        if required is not None:
            for field in self.children:
                field.required = required if type(required) is bool else required.get(field)

    def render_header(self):
        title = ''
        if self.title is not None:
            title = [dhtml.H3(self.title) if type(self.title) is str else self.title]
            if self.collapsable:
                title.append(dhtml.Button(self.HIDE_HTML, id=self.id_builder('collapse'), className='collapse'))
        return dhtml.Div(title, className='header')

    def render(self):
        rows = [dhtml.Div(
            dhtml.Div(className='errors', id=self.id_builder('errors')),
            id=self.id_builder('errors_wrapper'),
            className='fieldset_errors_row'
        )]

        for field in self.children:
            rows.extend(field.render())

        return dhtml.Div([
            self.render_header(),
            dhtml.Div(rows, id=self.id_builder('content'), className='body')
        ], id=self.id_builder(), className='fieldset')
