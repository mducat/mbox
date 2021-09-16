from midiutil import MIDIFile

from core import Note, interval


class Chord:

    def __init__(self, *notes: [Note]):
        self.notes = list(set(notes))

        if not notes:
            raise ValueError('Cannot create empty chord.')

        if any(v for v in notes if not isinstance(v, Note)):
            raise ValueError(f'Invalid object in chord.')

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
            n = n.move(12 * ((base + i * 2) // s_len))
            notes.append(n)

        return cls(*notes)

    @classmethod
    def from_name(cls, name: str):
        # @TODO
        return cls(Note('C'))

    @property
    def name(self):
        return ', '.join([v.name for v in self.notes])

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
