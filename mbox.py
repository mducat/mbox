import copy

from ui import Interface

# TODO
# - UI ?
# - gen guitar + piano map
# - know scales for a chord
# - allow diff tuning


class Note:

    def __init__(self, name: str, octave: int = 4):
        self.name = name
        self.octave = octave

        self.all_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

        # FORMAT NAME

        self.o_nam = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.l_nam = ['La', 'Si', 'Do', 'Ré', 'Mi', 'Fa', 'Sol']

        for i, x in enumerate(self.l_nam):
            if self.name.startswith(x):
                self.name = self.name[len(x):] + self.o_nam[i]

        convert = {
            'D#': 'Eb',
            'E#': 'F',
            'A#': 'Bb',
            'B#': 'C',

            'Cb': 'B',
            'Db': 'C#',
            'Fb': 'E',
            'Gb': 'F#',
            'Ab': 'G#',
        }

        if self.name == 'Cb':
            self.octave -= 1

        if self.name == 'B#':
            self.octave += 1

        if self.name in convert:
            self.name = convert[self.name]

        if self.name not in self.all_names:
            raise ValueError('Invalid name !')

    @property
    def position(self):
        return self.all_names.index(self.name) + self.octave * 12

    def move(self, n):
        i = self.all_names.index(self.name)
        i += n

        all_len = len(self.all_names)
        while i >= all_len:
            i -= all_len
            self.octave += 1

        while i < 0:
            i += all_len
            self.octave -= 1

        self.name = self.all_names[i]
        return self

    def clone(self):
        return copy.deepcopy(self)

    def to_latin_name(self):
        for i, x in enumerate(self.o_nam):
            if self.name.startswith(x):
                return self.l_nam[i] + self.name[len(x):]

        return None

    def __eq__(self, other):
        return self.name == other.name and self.octave == other.octave

    def __hash__(self):
        return hash(self.name + str(self.octave))

    def __str__(self):
        return f'{self.name} {self.octave}'

    def __repr__(self):
        return f'<Note {self.__str__()}>'


def interval(a: Note, b: Note):
    return b.position - a.position


class Chord:

    def __init__(self, notes: [Note]):
        self.notes = list(set(notes))

        self.notes.sort(key=lambda x: x.position)

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, item):
        return self.notes[item]

    def get_intervals(self):
        inter = []
        for i in self.notes[1:]:
            inter.append(interval(self.notes[0], i))
        return inter

    def analyse(self):
        inter = self.get_intervals()

        if inter == [3, 7]:
            return 'min'

        if inter == [4, 7]:
            return 'maj'

        if inter == [4, 8]:
            return 'aug'

        if inter == [3, 6]:
            return 'dim'

        return 'unknown'

    @classmethod
    def triad(cls, base: int, scale):
        s_len = len(scale)

        notes = []
        for i in range(3):
            n = scale[(base + i * 2) % s_len]
            n = n.clone().move(12 * ((base + i * 2) // s_len))
            notes.append(n)

        return cls(notes)

    def __str__(self):
        chord_name = ', '.join([v.name for v in self.notes])

        return 'Chord ' + chord_name

    def __repr__(self):
        return f'<{self.__str__()}>'

    def __hash__(self):
        return hash(sum(hash(v) for v in self.notes))


class Scale:

    def __init__(self, notes: Chord):
        self.scale = notes

    def analyse(self):
        nums = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        res = []

        for i in range(len(self.scale)):
            chord = Chord.triad(i, scale)
            an = chord.analyse()
            pr = nums[i]

            if an == 'maj':
                pr = pr.upper()
            elif an == 'aug':
                pr = pr.upper() + '+'
            elif an == 'dim':
                pr = pr + '°'

            res.append(pr)
        return res

    def __len__(self):
        return len(self.scale)

    def __getitem__(self, item):
        return self.scale[item]

    @classmethod
    def for_steps(cls, base: Note, steps: list):
        notes = []

        for i in steps:
            notes.append(base)
            base = base.clone().move(i)

        return cls(Chord(notes))

    @classmethod
    def major(cls, base: Note, mode: int = 0):
        steps = [2, 2, 1, 2, 2, 2, 1]
        steps = steps[-mode:] + steps[:-mode]
        return cls.for_steps(base, steps)

    @classmethod
    def minor(cls, base: Note, mode: int = 0):
        steps = [2, 1, 2, 2, 1, 2, 2]
        steps = steps[-mode:] + steps[:-mode]
        return cls.for_steps(base, steps)

    def __str__(self):
        return 'Scale ' + ', '.join([v.name for v in self.scale.notes])

    def __repr__(self):
        return f'<{self.__str__()}>'


if __name__ == '__main__':
    scale = Scale.minor(Note('C#'))
    print(scale)
    print(scale.analyse())
    ...
    # Interface().run()
