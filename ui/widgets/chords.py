from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPointF, QRect, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox

from core import Note, Scale, Chord


class ChordTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.w_size = (1200, 600)
        self.func_size = 40

        self.functions = [
            ['i', '', (580, 460), (1, 'min')],
            ['I', '', (580, 400), (1, 'min')],
            ['bIII', '', (540, 510), (3, 'bmaj')],
            ['vi°7', '', (610, 510), (6, 'dim7')],
            ['vi', '', (690, 510), (6, 'min')],

            ['iv', '', (220, 200), (4, 'min')],
            ['bVI', '', (210, 255), (4, 'bmaj')],
            ['IV', '', (180, 150), (4, 'maj')],
            ['ii°7', '', (270, 210), (2, 'dim7')],
            ['ii7', '', (320, 150), (2, 'min7')],

            ['bVII7', '', (850, 150), (7, 'bmaj7')],
            ['bVII', '', (895, 210), (7, 'bmaj')],
            ['V7', '', (955, 200), (5, 'maj7')],
            ['V', '', (1000, 150), (5, 'maj')],
            ['vii°7', '', (950, 260), (7, 'dim7')],
            ['vii°', '', (1010, 310), (7, 'dim')],
        ]

        self.note_box = QComboBox(self)
        self.ext_box = QComboBox(self)
        self.base = None
        self.ext = None

        for i in range(12):
            self.note_box.addItem(Note('C').move(i).name)
        self.note_box.currentIndexChanged.connect(self.rename)

        self.ext_box.addItems(['Nothing', 'Add 7th', 'Add 9th'])
        self.ext_box.currentIndexChanged.connect(self.ext_changed)

    def ext_changed(self, idx):
        to_map = {0: None, 1: '7', 2: '9'}
        self.ext = to_map[idx]

    def rename(self, idx):
        self.base = Note('C').move(idx)
        sc_maj = Scale.major(self.base)
        sc_min = Scale.minor(self.base)

        for i, item in enumerate(self.functions):
            name, disp, pos, par = item

            if 'maj' in par[1]:
                sc = sc_maj
            else:
                sc = sc_min

            r_name = sc[par[0] - 1].name

            if 'b' in name:
                r_name = sc[par[0] - 2].name
            if '°' in name:
                r_name += '°'
            if '7' in name:
                r_name += '7'

            self.functions[i][1] = r_name

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        x, y = a0.x(), a0.y()

        for item in self.functions:
            name, disp, pos, par = item

            rect = QRectF(pos[0], pos[1], self.func_size, self.func_size)

            if rect.contains(QPointF(x, y)):
                self.write(*par, name)
                return

    def write(self, *args):
        if self.base is None:
            return

        sc_maj = Scale.major(self.base)
        sc_min = Scale.minor(self.base)

        x = self
        for _ in range(3):
            x = x.parent()

        if 'maj' in args[1]:
            sc = sc_maj
        else:
            sc = sc_min

        r_pos = args[0] - 1

        if 'b' in args[2]:
            r_pos = args[0] - 2

        chord_ = Chord.triad(r_pos, sc, self.ext)

        x.composer.disp.builder.play_notes([(chord_, 4)])
        x.composer.disp.builder.staffs[0].append((chord_, 4))

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)

        font = qp.font()
        font.setPointSizeF(font.pointSize() * 2)
        qp.setFont(font)

        qp.setRenderHint(qp.HighQualityAntialiasing)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)

        self.draw_zones(qp)

        width, height = self.w_size
        ellipsis_size = 150

        pen.setWidth(2)
        qp.setPen(pen)

        dom_circle = QRectF((width - ellipsis_size) / 1.2, (height - ellipsis_size) / 2.5, ellipsis_size, ellipsis_size)
        sub_circle = QRectF((width - ellipsis_size) / 5.5, (height - ellipsis_size) / 2.5, ellipsis_size, ellipsis_size)
        home_circle = QRectF((width - ellipsis_size) / 2, (height - ellipsis_size), ellipsis_size, ellipsis_size)

        qp.drawEllipse(dom_circle)
        qp.drawEllipse(sub_circle)
        qp.drawEllipse(home_circle)

        for i, item in enumerate(self.functions):
            name, disp, pos, par = item

            if disp == '':
                disp = name
                self.functions[i][1] = disp

            rect = QRectF(pos[0], pos[1], self.func_size + (12 if len(name) >= 4 else 0), self.func_size)
            qp.drawRect(rect)

            qp.drawText(rect, Qt.AlignCenter, disp)

        qp.end()

    def draw_zones(self, qp):
        width, height = self.w_size

        a = QPointF(width / 2, height / 1.8)
        b = QPointF(width, height)

        qp.drawLine(a, b)

        a = QPointF(width / 2, height / 1.8)
        b = QPointF(0, height)

        qp.drawLine(a, b)

        a = QPointF(width / 2, height / 1.8)
        b = QPointF(width / 2, 0)

        qp.drawLine(a, b)

