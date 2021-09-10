
from mbox import Chord, Note


def generate_positions(chord: Chord, tuning: Chord = None):
    if tuning is None:
        tuning = Chord([
            Note('E'),
            Note('A'),
            Note('D'),
            Note('G'),
            Note('B'),
            Note('E'),
        ])
