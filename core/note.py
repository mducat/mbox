import copy


class Note:

    def __init__(self, name: str):
        self.name = name.strip()
        self.octave = 4

        i = 0
        while self.name[-i - 1:].isdigit():
            i += 1

        if self.name[-i:].isdigit():
            self.octave = int(self.name[-i:])
            self.name = self.name[:-i].strip()

        self.all_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

        # FORMAT NAME

        self.o_nam = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.l_nam = ['La', 'Si', 'Do', 'Ré', 'Mi', 'Fa', 'Sol']

        for i, x in enumerate(self.l_nam):
            if self.name.upper().startswith(x.upper()):
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
            raise ValueError(f'{name}: Invalid note name !')

    @property
    def midi(self):
        return self.position + 12

    @property
    def position(self):
        return self.all_names.index(self.name) + self.octave * 12

    def interval(self, other):
        return interval(self, other) % 12

    def distance(self, other):
        return interval(self, other)

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
