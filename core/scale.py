
from typing import Union

from core import Chord, Note


class Scale:

    def __init__(self, notes: Chord):
        self.scale = notes

    def analyse(self):
        nums = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii']
        res = []

        for i in range(len(self.scale)):
            chord = Chord.triad(i, self)
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
        return self.scale[item].clone()

    def __eq__(self, other):
        return self.scale == other.scale

    def __contains__(self, item):
        return item.name in {v.name for v in self.scale}

    @classmethod
    def for_steps(cls, base: Note, steps: list):
        notes = []

        for i in steps:
            notes.append(base)
            base = base.clone().move(i)

        return cls(Chord(*notes))

    @classmethod
    def mode_steps(cls, base: Union[Note, str], mode: int, steps: list):
        if isinstance(base, str):
            base = Note(base)
        steps = steps[-mode:] + steps[:-mode]
        return cls.for_steps(base, steps)

    @classmethod
    def major(cls, base: Union[Note, str], mode: int = 0):
        steps = [2, 2, 1, 2, 2, 2, 1]
        return cls.mode_steps(base, mode, steps)

    @classmethod
    def minor(cls, base: Union[Note, str], mode: int = 0):
        steps = [2, 1, 2, 2, 1, 2, 2]
        return cls.mode_steps(base, mode, steps)

    def __str__(self):
        return 'Scale ' + ', '.join([v.name for v in self.scale.notes])

    def __repr__(self):
        return f'<{self.__str__()}>'
