from abc import ABCMeta

import dash_core_components as dcc
from dash.dependencies import Input, State, Output
import dash_html_components as dhtml

from .chained_id import ChainedId
from .exceptions import ValidationError
from .fields import Field


class _ContainerMeta(ABCMeta):

    def __new__(meta, name, bases, attrs):
        if name != 'Container' and Container in bases and 'caught_exception' not in attrs:
            raise AttributeError('{0}.caught_exception must be defined.'.format(name))
        attrs['instance_count'] = 0
        return super().__new__(meta, name, bases, attrs)


class Container(metaclass=_ContainerMeta):
    HIDE_HTML = dhtml.I(className='fa fa-angle-down')
    SHOW_HTML = dhtml.I(className='fa fa-angle-right')

    def __init__(self, *, default=None, collapsable=False, title=None, validation_dependencies='children'):
        self.chained_id = ChainedId('{0}-{1}'.format(self.__class__.__name__, self.__class__.instance_count))
        self.__class__.instance_count += 1

        self.children = self._build_children()
        self.default = default
        self.collapsable = collapsable
        self.title = title

        # TODO
        self.validation_dependencies = []
        if validation_dependencies == 'children':
            self.validation_dependencies = self.dependencies(Input)
        elif validation_dependencies is not None:
            self.validation_dependencies = validation_dependencies

    def _build_children(self):
        children = []
        for name, attr in self.__class__.__dict__.items():
            if not isinstance(attr, Field):
                continue
            child = attr.__class__(*attr._init_args, **attr._init_kwargs)
            child.chained_id = self.chained_id.add(name)
            children.append(child)
        return children

    @property
    def component_id(self):
        return str(self.chained_id)

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
                child.default = self.default[child.chained_id[-1]]
            except KeyError:
                pass

    def dependencies(self, cls=State):
        return [dep for child in self.children for dep in child.dependencies(cls=cls)]

    def validate(self, data):
        cleaned = {}
        i = 0
        for child in self.children:
            n_deps = len(child.dependencies())
            cleaned[child.chained_id[-1]] = child.validate(data[i:i+n_deps])
            i += n_deps
        return cleaned

    def serialize(self, cleaned_data):
        serialized = {}
        for child in self.children:
            child_name = child.chained_id[-1]
            serialized[child_name] = child.serialize(cleaned_data[child_name])
        return serialized

    def get_collapse_html(self, cur_html):
        return self.SHOW_HTML if cur_html['props']['className'] == self.HIDE_HTML.className else self.HIDE_HTML

    def bind_callbacks(self, app):
        for child in self.children:
            child.bind_callbacks(app)
        
        if self.validation_dependencies:
            @app.callback(
                Output(self.chained_id('errors_wrapper'), 'style'),
                self.validation_dependencies,
                self.dependencies(),
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
                Output(self.chained_id('errors'), 'children'),
                self.validation_dependencies,
                self.dependencies(),
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
                Output(self.chained_id('content'), 'className'),
                [Input(self.chained_id('collapse'), 'n_clicks')],
                [State(self.chained_id('content'), 'className')]
            )
            def form_class_name(n_clicks, class_name):
                if n_clicks is None or class_name is None:
                    return 'body'
                return 'body' if class_name != 'body' else 'body collapsed'
            
            @app.callback(
                Output(self.chained_id('collapse'), 'children'),
                [Input(self.chained_id('collapse'), 'n_clicks')],
                [State(self.chained_id('collapse'), 'children')]
            )
            def display_collapse_btn(n_clicks, html):
                if n_clicks is None:
                    return html
                return self.get_collapse_html(html)
