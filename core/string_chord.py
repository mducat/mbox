
from core import Chord, Note


class StringChord(Chord):

    def __init__(self, notes: list[Note], positions: [int], tuning: [Note]):
        super(StringChord, self).__init__(*notes)

        if len(positions) != len(tuning):
            raise ValueError('Positions size differing from tuning size!')

        if len(notes) > len(tuning):
            raise ValueError(f'Unable to play a {len(notes)} notes chord on a {len(tuning)} notes tuning !')

        self.positions = positions
        self.tuning = tuning

        checked = set()

        for i, pos in enumerate(positions):
            if pos < 0:
                continue

            n = tuning[i].clone()
            n.move(pos)

            checked.add(n.name)

            del n

        expected = {v.name for v in self.notes}

        if checked != expected:
            raise ValueError('Invalid string chord !')

    def __str__(self):
        return 'String' + Chord.__str__(self)

    def __hash__(self):
        notes_hash = Chord.__hash__(self)
        position_hash = sum(hash(v) for v in self.positions)
        tuning_hash = sum(hash(v) for v in self.tuning)

        return hash(notes_hash + position_hash + tuning_hash)

    def show(self):
        ...


def generate_positions(chord: Chord, tuning: Chord = None):
    if tuning is None:
        tuning = Chord(
            Note('E2'),
            Note('A2'),
            Note('D3'),
            Note('G3'),
            Note('B3'),
            Note('E4'),
        )

    if len(chord.notes) > len(tuning.notes):
        raise ValueError(f'Unable to play a {len(chord.notes)} notes chord on a {len(tuning.notes)} notes tuning !')
