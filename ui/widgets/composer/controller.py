import os
import tempfile
from enum import Enum

import cv2


class Clef(Enum):
    treble = 0
    bass = 1


class Staff:

    def __init__(self):
        self.clef = Clef.treble

    def build(self):
        content = f"""
        \\new Staff \\relative c' {{
            \\clef {self.clef.name}
            \\time 3/4
            c4 d e f g a b cis
        }}
        """

        return content


class LilyController:

    def __init__(self):
        self.staffs = [Staff(), Staff(), Staff()]

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

        res = cv2.imread(res_file)
        os.system('rm /tmp/mbox-*')

        return res
