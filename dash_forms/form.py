import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .container import Container
from .exceptions import FormValidationError, ValidationError


class Form(Container):
    caught_exception = FormValidationError

    def __init__(self, *args, btn_text, **kwargs):
        super().__init__(*args, **kwargs)
        self.btn = dhtml.Button(btn_text, id=self.id_builder('btn'))

    def btn_dependency(self, cls=dInput):
        return cls(self.btn.id, 'n_clicks')

    def render_header(self):
        children = []
        if self.title is not None:
            children.append(dhtml.H3(self.title) if type(self.title) is str else self.title)
        if self.collapsable:
            children.append(dhtml.Button(self.HIDE_HTML, id=self.id_builder('collapse'), className='collapse'))
        return children

    def render(self):
        return dhtml.Fieldset([
            dhtml.Legend(self.render_header(), id=self.id_builder('header'), className='header'),
            dhtml.Div([
                *[child.render() for child in self.children],
                dhtml.Div(
                    dhtml.Div(className='errors', id=self.id_builder('errors')),
                    id=self.id_builder('errors_wrapper'),
                    className='form_errors_row'
                ),
                dhtml.Div(
                    self.btn,
                    className='btn_wrapper' + (' hide' if not self.btn.children else '')
                ),
            ], id=self.id_builder('content'), className='body')
        ], id=self.id_builder(), className='form' + (' with_header' if self.title or self.collapsable else ''))

    def bind_callbacks(self, app):
        super().bind_callbacks(app)

        @app.callback(
            dOutput(self.btn.id, 'style'),
            self.dependencies(),
        )
        def display_btn(*args):
            display = 'inline-block'
            try:
                self.validate(args)
            except ValidationError:
                display = 'none'
            return {'display': display}
