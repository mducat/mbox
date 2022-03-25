from PyQt5 import QtGui
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtWidgets import QWidget, QGridLayout

from ui.widgets.composer.controller import LilyController


class LilyDisplay(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.status = self.parent().status

        layout = QGridLayout()
        self.setLayout(layout)

        self.builder = LilyController()
        self.image = None

        self.update()

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def update(self):
        img = self.builder.build()
        h, w, _ = img.shape

        self.image = QImage(img.data, w, h, 3 * w, QImage.Format_RGB888)
        self.repaint()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)

        qp.setRenderHint(qp.HighQualityAntialiasing)

        pen = QPen()
        pen.setColor(Qt.black)
        pen.setWidth(3)
        qp.setPen(pen)

        a = QPointF(5, 5)
        qp.drawImage(a, self.image)

        qp.end()
