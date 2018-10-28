import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as dhtml

from .container import Container
from .exceptions import FormValidationError, ValidationError


class Form(Container):
    caught_exception = FormValidationError

    def __init__(self, btn_text, **kwargs):
        super().__init__(**kwargs)
        self.btn = dhtml.Button(btn_text, id=self.chained_id('__btn__'))

    def btn_dependency(self, cls=Input):
        return cls(self.btn.id, 'n_clicks')

    def render_header(self):
        children = []
        if self.title is not None:
            children.append(dhtml.H3(self.title) if type(self.title) is str else self.title)
        if self.collapsable:
            children.append(dhtml.Button(self.HIDE_HTML, id=self.chained_id('collapse'), className='collapse'))
        return children

    def render(self):
        return dhtml.Fieldset([
            dhtml.Legend(self.render_header(), id=self.chained_id('header'), className='header'),
            dhtml.Div([
                *[child.render() for child in self.children],
                dhtml.Div(
                    dhtml.Div(className='errors', id=self.chained_id('errors')),
                    id=self.chained_id('errors_wrapper'),
                    className='form_errors_row'
                ),
                dhtml.Div(
                    self.btn,
                    className='btn_wrapper' + (' hide' if not self.btn.children else '')
                ),
            ], id=self.chained_id('content'), className='body')
        ], id=self.chained_id(), className='form' + (' with_header' if self.title or self.collapsable else ''))

    def bind_callbacks(self, app):
        super().bind_callbacks(app)

        @app.callback(
            Output(self.btn.id, 'style'),
            self.dependencies(Input),
        )
        def display_btn(*args):
            display = 'inline-block'
            try:
                self.validate(args)
            except ValidationError:
                display = 'none'
            return {'display': display}
