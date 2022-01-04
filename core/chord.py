from midiutil import MIDIFile

from core import Note, interval


class Chord:

    def __init__(self, *notes):
        if len(notes) == 1 and isinstance(notes[0], list):
            notes = notes[0]

        if not notes:
            raise ValueError('Cannot create empty chord.')

        if any(v for v in notes if not isinstance(v, (Note, str))):
            raise ValueError(f'Invalid object in chord.')

        self.name = None

        notes = [v if isinstance(v, Note) else Note(v) for v in notes]

        self.notes = list(set(notes))

        self.notes.sort(key=lambda x: x.position)
        self.root_note = self.notes[0]

        self.find_name()

    def __len__(self):
        return len(self.notes)

    def __getitem__(self, item):
        return self.notes[item]

    def find_name(self):
        print(self.notes)
        inter = self.get_intervals()
        names = ['P1', 'm2', 'M2', 'm3', 'M3', 'P4', 'd5', 'P5', 'm6', 'M6', 'm7', 'M7']

        res = {names[abs(v) % len(names)] for v in inter}
        print(res)

        self.name = self.root_note.name

        patterns = [
            [{'M3', 'M7', 'M2', 'M6'}, 'maj13'],
            [{'m3', 'm7', 'M6'}, 'm13'],
            [{'M3', 'm7', 'M6'}, '13'],
            [{'m3', 'm7', 'P4'}, 'm11'],
            [{'M3', 'm7', 'P4'}, '11'],
            [{'M3', 'M7', 'M2'}, 'maj9'],
            [{'m3', 'm7', 'M2'}, 'm9'],
            [{'m3', 'd5', 'M6'}, 'dim7'],
            [{'m3', 'm7', 'M3'}, '7#9'],
            [{'m7', 'M2'}, '9 '],
            [{'m3', 'm7'}, 'm7'],
            [{'m3', 'm6'}, 'm6'],
            [{'M3', 'm7'}, '7 '],
            [{'M3', 'M7'}, 'maj7'],
            [{'m3', 'd5'}, 'dim'],
            [{'m3'}, 'm'],
            [{'M3'}, ''],
            [{'P5'}, ''],
            [{'M6'}, '6'],
            [{'d5'}, 'b5'],
            [{'m6'}, 'aug'],
            [{'M2'}, 'add9'],
            [{'P4'}, 'sus4'],
            [{'M2'}, 'sus2'],
            [{'m2'}, 'b9'],
        ]

        for pat in patterns:
            if not pat[0].issubset(res):
                continue

            for v in pat[0]:
                res.remove(v)

            self.name += pat[1]

        if 'P1' in res:
            res.remove('P1')

        self.name += ' '.join(res)

    def transpose(self, amount):
        self.notes = [v.move(amount) for v in self.notes]

    def get_intervals(self):
        inter = []
        for i in self.notes[1:]:
            inter.append(interval(self.root_note, i))
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
            n = n.move(12 * ((base + i * 2) // s_len))
            notes.append(n)

        return cls(*notes)

    @classmethod
    def from_name(cls, name: str):
        # @TODO
        return cls(Note('C'))

    def __str__(self):
        return 'Chord ' + self.name

    def __repr__(self):
        return f'<{self.__str__()}>'

    def __hash__(self):
        return hash(sum(hash(v) for v in self.notes))


def create_midi(chords: [Chord]):
    file = MIDIFile(1)

    file.addTrackName(0, 1, 'Main track')

    for i, chord in enumerate(chords):
        for note in chord.notes:
            file.addNote(0, 0, note.midi, i, 1, 100)

    return file
