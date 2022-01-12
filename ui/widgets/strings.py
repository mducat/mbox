from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtWidgets import QWidget, QGridLayout

from core import Chord, Tunings, StringChord, Scale


class StringTab(QWidget):

    CHORD_DISPLAY = 0
    SCALE_DISPLAY = 1

    def __init__(self, tuning: Chord = Tunings.guitar_tuning, tabs_len=15):
        QWidget.__init__(self)

        layout = QGridLayout()
        self.setLayout(layout)

        self.tuning = tuning
        self.tabs_len = tabs_len

        positions = [-1, 3, 2, 3, 4, -1]
        self.chord = StringChord(positions)
        self.scale = Scale.minor('Fb')

        self.mode = self.CHORD_DISPLAY

        self.x_margin = 40

        self.grid_offset_x = 20 + self.x_margin
        self.grid_offset_y = 70
        self.grid_height = 200
        self.grid_width = 1000 - self.x_margin * 2

        self.step_y = (self.grid_height + self.grid_offset_y) / (len(self.tuning) - 1)
        self.step_x = (self.grid_width + self.grid_offset_x) / self.tabs_len

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        x_loc = a0.x() - self.grid_offset_x + self.step_x / 2
        x_loc /= self.step_x

        y_loc = self.grid_height - a0.y() + self.grid_offset_y + self.step_y
        y_loc /= self.step_y

        x_loc, y_loc = round(x_loc), round(y_loc)

        if 0 <= y_loc < len(self.tuning) and 0 <= x_loc < self.tabs_len:

            if self.chord[y_loc].position == x_loc:
                self.chord[y_loc] = -1
            else:
                self.chord[y_loc] = x_loc

            self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)

        qp.setRenderHint(qp.HighQualityAntialiasing)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_height = self.grid_height
        grid_width = self.grid_width

        step_x = self.step_x
        step_y = self.step_y

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        main_grid = QRectF(grid_offset_x, grid_offset_y,
                           grid_offset_x + grid_width, grid_offset_y + grid_height)
        qp.drawRect(main_grid)

        align = Qt.AlignCenter

        for i in range(len(self.tuning) - 1):
            a = QPointF(grid_offset_x, grid_offset_y + i * step_y)
            b = QPointF(2 * grid_offset_x + grid_width, grid_offset_y + i * step_y)

            qp.drawLine(a, b)

        for i in range(self.tabs_len):
            line_pos = [grid_offset_x + i * step_x, grid_offset_y,
                        grid_offset_x + i * step_x, 2 * grid_offset_y + grid_height]
            box = QRectF(line_pos[0], line_pos[3], step_x, step_y * 1.5)

            qp.drawLine(QPointF(line_pos[0], line_pos[1]), QPointF(line_pos[2], line_pos[3]))
            qp.drawText(box, align, str(i + 1))

        if self.mode == self.CHORD_DISPLAY:
            self.paintChord(self.chord, qp)
        elif self.mode == self.SCALE_DISPLAY:
            self.paintScale(self.scale, qp)

        qp.end()

    def paintScale(self, scale: Scale, qp: QPainter):
        for n in range(len(self.tuning)):
            note = self.tuning[n].clone()

            for i in range(self.tabs_len + 1):

                if note in scale:
                    self.paintNote(i, n, qp)

                note.move(1)

            del note

    def paintChord(self, chord: StringChord, qp: QPainter):
        for i, n in enumerate(chord.positions):
            self.paintNote(n, i, qp, highlight=(chord[i].note == chord.root_note))

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_width = self.grid_width

        step_y = self.step_y

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        box_pos = [grid_offset_x, grid_offset_y - step_y - 10,
                   grid_offset_x + grid_width, grid_offset_y]
        box = QRectF(*box_pos)

        # TODO DRAW INTER

        qp.drawText(box, Qt.AlignCenter, chord.name)

    def paintNote(self, x, y, qp: QPainter, highlight=False):
        if y >= len(self.tuning) or x > self.tabs_len:
            raise ValueError(f'{x} {y}: Invalid coordinates !')

        note = self.tuning[y].clone()
        note.move(x)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y

        step_x = self.step_x
        step_y = self.step_y

        size = step_x / 2

        center = QPointF(grid_offset_x + (x - 0.5) * step_x, grid_offset_y + (len(self.tuning) - 1 - y) * step_y)

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
