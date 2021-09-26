
from core import Chord, Tunings


class StringChord(Chord):

    def __init__(self, positions: [int], tuning: Chord = Tunings.guitar_tuning):
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

    def to_tab(self):
        res = str()

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

        res += ' '.join(to_print) + '\n'

        res += '┍━'
        res += '┯━'.join('' for _ in range(len(self.tuning) - 1))
        res += '┑\n'

        for i in range(0 if base != 0 else 1, up - base + 1):
            current = [j for j, v in enumerate(self.positions) if v == i + base]
            dots = ['●' if j in current else '│' for j in range(len(self.tuning))]
            res += ' '.join(dots) + '\n'
            res += '├'
            res += '─┼'.join('' for _ in range(len(self.tuning) - 1))
            res += '─┤\n'

        res += ' '.join('│' for _ in range(len(self.tuning))) + '\n'
        res += '└─'
        res += '┴─'.join('' for _ in range(len(self.tuning) - 1))
        res += '┘\n'

        return res

    def show(self):
        print()
        print(self.name)
        print(self.to_tab())


# @todo rename: inversions generator
def generate_positions(chord: Chord, tuning: Chord = Tunings.guitar_tuning, limit: int = 15, max_dist: int = 4):

    if len(chord.notes) > len(tuning.notes):
        raise ValueError(f'Unable to play a {len(chord.notes)} notes chord on a {len(tuning.notes)} notes tuning !')

    names = {v.name for v in chord.notes}

    def recur(r_chord, r_pos, r_limit, x):

        if x >= len(r_chord.notes):

            if {v.name for v in r_chord.notes} == names:
                return {bytes(r_pos)}
            else:
                # @todo add mutes !
                return {}

        res = set()

        while r_pos[x] <= r_limit:
            rec_data = recur(r_chord, r_pos, r_limit, x + 1)
            res = res.union(rec_data)

            r_chord.notes[x].move(1)
            r_pos[x] += 1

            while r_chord.notes[x].name not in names and r_pos[x] <= r_limit:
                r_chord.notes[x].move(1)
                r_pos[x] += 1

        r_chord.notes[x].move(-r_pos[x])
        r_pos[x] = 0

        return res

    r = recur(tuning, [0 for _ in range(len(tuning.notes))], 4, 0)

    # @todo add high versions
    return [list(v) for v in r]
