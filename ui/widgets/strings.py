from PyQt5 import QtGui
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPainter, QPen, QColor, QPainterPath
from PyQt5.QtWidgets import QWidget, QGridLayout

from core import Chord, Tunings, StringChord, Scale


class StringCanvas(QPainter):

    def __init__(self, parent=None):
        QPainter.__init__(self)

        self.begin(parent)
        self.drawLine(5, 5, 100, 100)
        self.end()


class StringTab(QWidget):

    def __init__(self, tuning: Chord = Tunings.guitar_tuning, tabs_len=15):
        QWidget.__init__(self)

        layout = QGridLayout()
        self.setLayout(layout)

        self.tuning = tuning
        self.tabs_len = tabs_len

        self.grid_offset_x = 20 + 40
        self.grid_offset_y = 70
        self.grid_height = 200
        self.grid_width = 1000 - 40 * 2

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

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        main_grid = QRectF(grid_offset_x, grid_offset_y,
                           grid_offset_x + grid_width, grid_offset_y + grid_height)
        qp.drawRect(main_grid)

        step_y = (grid_height + grid_offset_y) / (len(self.tuning) - 1)
        step_x = (grid_width + grid_offset_x) / self.tabs_len
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

        positions = [-1, 3, 2, 3, 4, -1]

        st = StringChord(positions)
        self.paintChord(st, qp)

        """test = Scale.minor('Fb')
        self.paintScale(test, qp)"""

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
            self.paintNote(n, i, qp)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_height = self.grid_height
        grid_width = self.grid_width

        step_y = (grid_height + grid_offset_y) / (len(self.tuning) - 1)

        font = qp.font()
        font.setPointSizeF(font.pointSize() * (self.grid_width / 500))
        qp.setFont(font)

        box_pos = [grid_offset_x, grid_offset_y - step_y - 10,
                   grid_offset_x + grid_width, grid_offset_y]
        box = QRectF(*box_pos)

        # TODO DRAW INTER

        qp.drawText(box, Qt.AlignCenter, chord.name)

    def paintNote(self, x, y, qp: QPainter):
        if y >= len(self.tuning) or x > self.tabs_len:
            raise ValueError(f'{x} {y}: Invalid coordinates !')

        note = self.tuning[y].clone()
        note.move(x)

        grid_offset_x = self.grid_offset_x
        grid_offset_y = self.grid_offset_y
        grid_height = self.grid_height
        grid_width = self.grid_width

        step_x = (grid_width + grid_offset_x) / self.tabs_len
        step_y = (grid_height + grid_offset_y) / (len(self.tuning) - 1)

        size = step_x / 2

        center = QPointF(grid_offset_x + (x - 0.5) * step_x, grid_offset_y + (len(self.tuning) - 1 - y) * step_y)

        box = QRectF(0, 0, size, size)
        box.moveCenter(center)

        path = QPainterPath()
        path.addRoundedRect(box, 5, 5)

        qp.fillPath(path, QColor(0xB3, 0xE5, 0xFC))
        qp.drawRoundedRect(box, 5, 5)

        qp.drawText(box, Qt.AlignCenter, note.name)
