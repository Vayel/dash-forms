import dash_core_components as dcc

from .field import Field


class ListField(Field):

    def __init__(self, *args, options, **kwargs):
        self.options = options
        if 'default' not in kwargs:
            kwargs['default'] = self.options[0]['value']
        super().__init__(*args, **kwargs)

    @Field.default.setter
    def default(self, val):
        if val not in [option['value'] for option in self.options]:
            raise ValueError("No option with value '{0}' in {1}.".format(
                val,
                self.chained_id
            ))
        self._default = val

    def render_input(self):
        return dcc.Dropdown(
            options=self.options,
            value=self.default,
            id=self.chained_id('value'),
            searchable=False,
            clearable=False,
        )
