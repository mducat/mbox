
from core import Chord, Note, Tunings


class StringChord(Chord):

    def __init__(self, positions: [int], tuning: [Note]):
        if len(positions) != len(tuning):
            raise ValueError('Positions size differing from tuning size!')

        self.positions = positions
        self.tuning = tuning

        notes = list()

        for i, pos in enumerate(positions):
            if pos < 0:
                continue

            n = tuning[i].clone()
            n.move(pos)

            notes.append(n)

        super(StringChord, self).__init__(*notes)

    def __str__(self):
        return 'StringChord ' + self.name

    def __hash__(self):
        notes_hash = Chord.__hash__(self)
        position_hash = sum(hash(v) for v in self.positions)
        tuning_hash = sum(hash(v) for v in self.tuning)

        return hash(notes_hash + position_hash + tuning_hash)

    def show(self):
        to_print = []
        for v in self.positions:
            if v < 0:
                to_print.append('x')
            elif v == 0:
                to_print.append('o')
            else:
                to_print.append(' ')

        base = min(v for v in self.positions if v >= 0)
        up = max(self.positions)

        print()
        print(self.name)
        print(' '.join(to_print))

        print('┍━', end='')
        print('┯━'.join('' for _ in range(len(self.tuning) - 1)), end='')
        print('┑')

        for i in range(1, up - base + 1):
            current = [j for j, v in enumerate(self.positions) if v == i + base]
            dots = ['●' if j in current else '│' for j in range(len(self.tuning))]
            print(' '.join(dots))
            print('├', end='')
            print('─┼'.join('' for _ in range(len(self.tuning) - 1)), end='')
            print('─┤')

        print(' '.join('│' for j in range(len(self.tuning))))
        print('└─', end='')
        print('┴─'.join('' for _ in range(len(self.tuning) - 1)), end='')
        print('┘')


def generate_positions(chord: Chord, tuning: Chord = None):
    if tuning is None:
        tuning = Tunings.guitar_tuning

    if len(chord.notes) > len(tuning.notes):
        raise ValueError(f'Unable to play a {len(chord.notes)} notes chord on a {len(tuning.notes)} notes tuning !')
