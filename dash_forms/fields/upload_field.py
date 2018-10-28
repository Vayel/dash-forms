import dash_core_components as dcc
import dash_html_components as dhtml
from dash.dependencies import Input, Output

from .field import Field


class UploadField(Field):

    def __init__(self, *args, clearable=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.clearable = clearable

    def dependencies(self, cls=Input):
        return [cls(self.chained_id('value'), 'contents'),]

    def render_input(self):
        # TODO: clearable
        return dcc.Upload(
            id=self.chained_id('value'),
            className='upload',
        )

    def bind_callbacks(self, app):
        super().bind_callbacks(app)

        @app.callback(
            Output(self.chained_id('value'), 'children'),
            [Input(self.chained_id('value'), 'filename')]
        )
        def contents(fname):
            if fname is None:
                return dhtml.I(className='fa fa-upload')
            return fname

        # TODO: clearable
