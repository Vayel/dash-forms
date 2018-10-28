class ChainedId(list):
    joiner = '__'

    def __init__(self, ids):
        if isinstance(ids, str):
            ids = [ids]
        super().__init__(ids)

    def __call__(self, child=None):
        parts = self if child is None else [*self, child]
        # Cannot have periods in dash ids
        return self.joiner.join(parts).replace('.', '_')

    def __str__(self):
        return self()

    def add(self, *args):
        return self.__class__([*self, *args])

    def parent(self):
        return self.__class__(self[:-1])
