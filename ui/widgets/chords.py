from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPointF, QRect, QRectF
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtWidgets import QWidget, QLabel


class ChordTab(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.w_size = (1200, 600)
        self.func_size = 40

        self.functions = [
            ('i', (580, 460), self.write),
            ('I', (580, 400), self.write),
            ('bIII', (540, 510), self.write),
            ('vi°7', (610, 510), self.write),
            ('vi', (690, 510), self.write),

            ('iv', (220, 200), self.write),
            ('bVI', (210, 255), self.write),
            ('IV', (180, 150), self.write),
            ('ii°7', (270, 210), self.write),
            ('ii7', (320, 150), self.write),

            ('bVII7', (850, 150), self.write),
            ('bVII', (895, 210), self.write),
            ('V7', (955, 200), self.write),
            ('V', (1000, 150), self.write),
            ('vii°7', (950, 260), self.write),
            ('vii°', (1010, 310), self.write),
        ]

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        x, y = a0.x(), a0.y()

        for item in self.functions:
            name, pos, func = item

            rect = QRectF(pos[0], pos[1], self.func_size, self.func_size)

            if rect.contains(QPointF(x, y)):
                func(name)
                return

    def write(self, *args):
        print(args)

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

        for item in self.functions:
            name, pos, func = item

            rect = QRectF(pos[0], pos[1], self.func_size + (12 if len(name) >= 4 else 0), self.func_size)
            qp.drawRect(rect)

            qp.drawText(rect, Qt.AlignCenter, name)

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

