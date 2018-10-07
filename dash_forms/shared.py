class ComponentId(list):
    joiner = '__'

    def __init__(self, ids):
        if type(ids) is str:
            ids = [ids]
        super().__init__(ids)

    def __call__(self, element_name=None):
        parts = self if element_name is None else [*self, element_name]
        # Cannot have periods in dash ids
        return self.joiner.join(parts).replace('.', '_')

    def last(self):
        return self[-1]

    def element_name(self, element_id):
        return element_id[len(self('')):]

    def add(self, *args):
        return self.__class__([*self, *args])

    def parent(self):
        return self.__class__(self[:-1])
