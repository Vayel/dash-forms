import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input as dInput, State as dState, Output as dOutput

from .field import Field


class UploadField(Field):
    def __init__(self, *args, clearable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.clearable = clearable

    def dependencies(self, cls=dInput):
        return [cls(self.id_builder('value'), 'contents'),]

    def render_input(self):
        # TODO: clearable
        return dcc.Upload(
            id=self.id_builder('value'),
            className='upload',
        )

    def bind_callbacks(self, app):
        super().bind_callbacks(app)

        @app.callback(
            dOutput(self.id_builder('value'), 'children'),
            [dInput(self.id_builder('value'), 'filename')]
        )
        def contents(fname):
            if fname is None:
                return dhtml.I(className='fa fa-upload')
            return fname

        # TODO: clearable
