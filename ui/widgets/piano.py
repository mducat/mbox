import math

from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from PyQt5.QtWidgets import QWidget, QGridLayout

from core import Chord, Scale, Note


class PianoTab(QWidget):
    CHORD_DISPLAY = 0
    SCALE_DISPLAY = 1

    def __init__(self, notes_len=12 * 3):
        QWidget.__init__(self)

        if notes_len % 12 != 0:
            raise ValueError('cannot create piano display with notes_len % 12 != 0')

        layout = QGridLayout()
        self.setLayout(layout)

        self.notes_len = notes_len

        nb_octaves = int(notes_len / 12)

        self.base_note = Note('C' + str(4 - math.floor(nb_octaves / 2)))

        self.scale = Scale.minor('F#')
        self.chord = Chord.triad(0, self.scale)

        self.mode = self.CHORD_DISPLAY

        self.x_margin = 40

        self.grid_offset_x = 20 + self.x_margin
        self.grid_offset_y = 70
        self.grid_height = 300
        self.grid_width = 1100 - self.x_margin

        self.nb_octaves = int(self.notes_len / 12)
        self.octave_len = self.grid_width / self.nb_octaves

        self.note_size = self.octave_len / 7

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        y_loc = a0.y() - self.grid_offset_y
        y_loc /= self.grid_height * 1.2

        y_loc = round(y_loc)

        x_loc = a0.x() - self.grid_offset_x + self.note_size / 2
        if y_loc == 0:
            x_loc -= self.note_size / 2
        x_loc /= self.note_size

        x_loc = round(x_loc) - 1

        x_local = x_loc % 7
        x_oct = math.floor(x_loc / 7)

        if y_loc == 0:
            offset = x_oct * 12 + 1 + x_local * 2 - (1 if x_local > 2 else 0)
        elif y_loc == 1:
            offset = x_oct * 12 + x_local * 2 - (1 if x_local > 2 else 0)

        new_note = self.base_note.clone().move(offset)

        if new_note in self.chord:
            self.chord -= new_note
        else:
            self.chord += new_note

        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        qp.setRenderHint(qp.HighQualityAntialiasing)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_height = self.grid_height
        grid_width = self.grid_width

        nb_octaves = int(self.notes_len / 12)
        octave_len = self.grid_width / nb_octaves

        note_len = octave_len / 7

        for i in range(nb_octaves):

            for j in range(7):

                white_rect = QRectF(
                    grid_offset_x + octave_len * i + note_len * j,
                    grid_offset_y,
                    note_len,
                    grid_height,
                )

                black_j = j + 0.75 + (1 if j >= 2 else 0)

                black_rect = QRectF(
                    grid_offset_x + octave_len * i + note_len * black_j,
                    grid_offset_y,
                    note_len / 2,
                    grid_height * (4 / 7),
                )

                qp.drawRect(white_rect)
                if j not in [5, 6]:
                    qp.fillRect(black_rect, QBrush(Qt.black))

        if self.mode == self.CHORD_DISPLAY:
            self.paintChord(self.chord, qp)
        elif self.mode == self.SCALE_DISPLAY:
            self.paintScale(self.scale, qp)

        qp.end()

    def paintScale(self, scale: Scale, qp: QPainter):
        note = self.base_note.clone()

        for i in range(self.notes_len):

            if note in scale:
                self.paintNote(i, qp)

            note.move(1)

        del note

    def paintChord(self, chord: Chord, qp: QPainter):
        for n in chord.notes:
            self.paintNote(self.base_note.distance(n), qp, highlight=(n == chord.root_note))

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_width = self.grid_width

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        box_pos = [grid_offset_x, grid_offset_y - 70,
                   grid_offset_x + grid_width, grid_offset_y]
        box = QRectF(*box_pos)

        # TODO DRAW INTER

        qp.drawText(box, Qt.AlignCenter, chord.name)

    def paintNote(self, x, qp: QPainter, highlight=False):
        if x > self.notes_len or x < 0:
            raise ValueError(f'{x}: Invalid coordinates !')

        note = self.base_note.clone()
        note.move(x)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y

        nb_octaves = int(self.notes_len / 12)
        octave_len = self.grid_width / nb_octaves

        note_len = octave_len / 7

        is_black = [1, 3, 6, 8, 10]
        nb_oct = math.floor(x / 12)

        if x % 12 in is_black:

            black_x = (x % 12) / 2 + 0.5 + (0.5 if x % 12 >= 4 else 0)

            center = QPointF(
                grid_offset_x + nb_oct * octave_len + note_len * black_x,
                grid_offset_y + self.grid_height * (4 / 7) - 20)
        else:
            white_x = (x % 12) / 2 + 0.50 + (0.5 if x % 12 >= 5 else 0)

            center = QPointF(
                grid_offset_x + nb_oct * octave_len + white_x * note_len,
                grid_offset_y + self.grid_height - 25)

        size = self.note_size / 1.5

        pen = QPen()
        pen.setColor(QColor(0x33, 0x33, 0x33))
        pen.setWidth(2)
        qp.setPen(pen)

        box = QRectF(0, 0, size, size)
        box.moveCenter(center)

        path = QPainterPath()
        path.addRoundedRect(box, 5, 5)

        qp.fillPath(path, QColor(0xB3, 0xE5, 0xFC) if not highlight else QColor(0xFF, 0x7F, 0x7F))
        qp.drawRoundedRect(box, 5, 5)

        qp.drawText(box, Qt.AlignCenter, note.name)
