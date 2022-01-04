import os
import tempfile
from enum import Enum

from mido import MidiFile

import cv2
import numpy as np


class Clef(Enum):
    treble = 0
    bass = 1
    ut = 2
    french = 3
    violin = 4
    GG = 5
    soprano = 6
    mezzosoprano = 7
    alto = 8
    C = 9
    baritone = 10
    tenor = 11
    varC = 12
    altovarC = 13
    tenorvarC = 14
    baritonevarC = 15
    varbaritone = 16
    baritonevarF = 17
    F = 18
    subbass = 19
    percussion = 20
    varpercussion = 21


class TimeSig:

    def __init__(self, *data):
        if len(data) == 0:
            data = (4, 4)

        if isinstance(data[0], (list, tuple, set)):
            data = data[0]

        self.numerator = data[0]
        self.denominator = data[1]


class Staff:

    default_time = TimeSig()

    def __init__(self, clef=Clef.treble, time=default_time):
        self.clef = clef
        self.time = time

        self.notes = []  # TODO: define format

    def build(self):
        content = f"""
        \\new Staff \\relative c {{
            \\clef {self.clef.name}
            \\time {self.time.numerator}/{self.time.denominator}
            c4 d e f g a b cis
        }}
        """

        return content


class LilyController:

    def __init__(self):
        self.staffs = [Staff(), Staff(), Staff()]

    def export_midi(self):
        ...

    def import_midi(self):
        file = MidiFile('test.mid', clip=True)
        # TODO: read clef, time, notes (+duration??)
        for track in file.tracks:
            print(track)

    def build(self):
        content = """
        \\header {
            tagline = ""
        }
        <<
        """

        for staff in self.staffs:
            content += staff.build()

        content += ">>"

        file = tempfile.NamedTemporaryFile(prefix='mbox-', delete=False)
        file.write(bytes(content, encoding='utf-8'))
        file.flush()

        # TODO: this is hella system specific
        cmd = f"lilypond --png -s -dbackend=eps -dresolution=170 -o {file.name} {file.name}"
        os.system(cmd)
        res_file = file.name + '.png'

        if not os.path.exists(res_file):
            res = np.zeros((1, 1, 1))
        else:
            res = cv2.imread(res_file)

        os.system('rm /tmp/mbox-*')

        return res
