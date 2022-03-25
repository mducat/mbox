import glob
import os
import pickle
import tempfile
import threading
import time
from enum import Enum

from mido import MidiFile

import cv2
import numpy as np

from core import create_midi, Chord, Note
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame


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

        self.notes = [
        ]

    def build(self):
        content = f"""
\\new Staff {{
    \\clef {self.clef.name}
    \\time {self.time.numerator}/{self.time.denominator}
"""
        for ch, ch_len in self.notes:
            content += "    <"

            for note in ch.notes:
                content += f"{note.name.replace('b', 'es').lower().replace('#', 'is')}"
                for _ in range(note.octave - 3):
                    content += '\''
                content += ' '

            content += f">{ch_len}\n"

        content += "}"

        return content


class LilyController:

    def __init__(self):
        self.staffs = [Staff()]

        pygame.mixer.init()

        parse_index = lambda v: int(v[:v.index('.')])

        self.all_sounds = glob.glob('piano_c4/*.wav')
        self.all_sounds = {parse_index(os.path.basename(v)): pygame.mixer.Sound(v) for v in self.all_sounds}

    def export_midi(self, file_path):
        chords = self.staffs[0].notes
        out = create_midi(chords)

        out.save(file_path)

    def import_midi(self, file_path):
        file = MidiFile(file_path, clip=True)
        # TODO: read clef, time, notes (+duration??)
        for track in file.tracks:
            print(track)

    def save_controller(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.staffs, f)

    def restore_controller(self, file_path):
        with open(file_path, 'rb') as f:
            self.staffs = pickle.load(f)

    def play(self):
        notes = self.staffs[0].notes
        self.play_notes(notes)

    def play_notes(self, notes):
        x = threading.Thread(target=self.play_blocking, args=(notes,))
        x.start()

    def play_blocking(self, notes):
        base_len = 0.5  # this is the duration of a black note
        base_note = Note('C')

        for ch, c_len in notes:

            for note in ch:
                try:
                    self.all_sounds[base_note.distance(note)].play(fade_ms=50)
                except Exception as e:
                    print(e)

            time.sleep((4 * base_len) / c_len)

            for note in ch:
                try:
                    self.all_sounds[base_note.distance(note)].stop()
                except Exception as e:
                    print(e)

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

        cmd = f'lilypond --png -s -dbackend=eps -dresolution=170 -o {file.name} {file.name}'
        os.system(cmd)
        res_file = file.name + '.png'

        if not os.path.exists(res_file):
            res = np.zeros((1, 1, 1))
        else:
            res = cv2.imread(res_file)

        file.close()

        file_dir = os.path.dirname(file.name)
        all_del = glob.glob(os.path.join(file_dir, 'mbox-*'))
        for f in all_del:
            os.remove(f)

        return res
