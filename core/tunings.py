
import copy

from core import Chord, Note


def copy_prop(cls):

    class Copiable(cls):

        def __getattribute__(self, item):
            data = cls.__getattribute__(self, item)
            return copy.deepcopy(data)

    return Copiable


@copy_prop
class Tunings:

    guitar_tuning = Chord(
        Note('E2'),
        Note('A2'),
        Note('D3'),
        Note('G3'),
        Note('B3'),
        Note('E4'),
    )
