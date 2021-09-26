
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

    # @todo check notes order

    ukulele_tuning = Chord(
        Note('G4'),
        Note('C4'),
        Note('E4'),
        Note('A4'),
    )

    bass_tuning = Chord(
        Note('G2'),
        Note('D2'),
        Note('A1'),
        Note('E1'),
    )
