import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .exceptions import ValidationError
from .fields import Field


class Container:
    caught_exception = None
    HIDE_HTML = dhtml.I(className='fa fa-angle-down')
    SHOW_HTML = dhtml.I(className='fa fa-angle-right')

    def __init__(self, id_builder, children, default=None, collapsable=False, title=None, validation_dependencies='children'):
        self.id_builder = id_builder
        self.children = children
        self.default = default
        self.collapsable = collapsable
        self.title = title

        self.validation_dependencies = []
        if validation_dependencies == 'children':
            self.validation_dependencies = self.dependencies()
        elif validation_dependencies is not None:
            self.validation_dependencies = validation_dependencies
    
    @property
    def default(self):
        return self.default_

    @default.setter
    def default(self, values=None):
        self.default_ = values
        if self.default_ is None:
            return
        for child in self.children:
            try:
                child.default = self.default[child.id_builder.last()]
            except KeyError:
                pass

    def dependencies(self, cls=dInput):
        return [dep for child in self.children for dep in child.dependencies(cls=cls)]

    def validate(self, data):
        cleaned = {}
        i = 0
        for child in self.children:
            n_deps = len(child.dependencies())
            cleaned[child.id_builder.last()] = child.validate(data[i:i+n_deps])
            i += n_deps
        return cleaned

    def serialize(self, cleaned_data):
        serialized = {}
        for child in self.children:
            child_name = child.id_builder.last()
            serialized[child_name] = child.serialize(cleaned_data[child_name])
        return serialized

    def get_collapse_html(self, cur_html):
        return self.SHOW_HTML if cur_html['props']['className'] == self.HIDE_HTML.className else self.HIDE_HTML

    def bind_callbacks(self, app):
        for child in self.children:
            child.bind_callbacks(app)
        
        if self.validation_dependencies:
            @app.callback(
                dOutput(self.id_builder('errors_wrapper'), 'style'),
                self.validation_dependencies,
                self.dependencies(cls=dState),
            )
            def display_errors(*args):
                display = 'none'
                try:
                    self.validate(args[len(self.validation_dependencies):])
                except self.caught_exception as e:
                    display = 'block'
                except ValidationError:
                    pass
                return {'display': display}
            
            @app.callback(
                dOutput(self.id_builder('errors'), 'children'),
                self.validation_dependencies,
                self.dependencies(cls=dState),
            )
            def print_errors(*args):
                try:
                    self.validate(args[len(self.validation_dependencies):])
                except self.caught_exception as e:
                    return str(e)
                except ValidationError:
                    pass

        if self.collapsable:
            @app.callback(
                dOutput(self.id_builder('content'), 'className'),
                [dInput(self.id_builder('collapse'), 'n_clicks')],
                [dState(self.id_builder('content'), 'className')]
            )
            def form_class_name(n_clicks, class_name):
                if n_clicks is None or class_name is None:
                    return 'body'
                return 'body' if class_name != 'body' else 'body collapsed'
            
            @app.callback(
                dOutput(self.id_builder('collapse'), 'children'),
                [dInput(self.id_builder('collapse'), 'n_clicks')],
                [dState(self.id_builder('collapse'), 'children')]
            )
            def display_collapse_btn(n_clicks, html):
                if n_clicks is None:
                    return html
                return self.get_collapse_html(html)
