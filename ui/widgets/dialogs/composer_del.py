import math

from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator, QStatusTipEvent
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QLabel, QMessageBox, QStatusBar

from core import Note, Chord


class ComposerDelChord(QDialog):

    def __init__(self, parent, max_idx):
        QDialog.__init__(self, parent)

        self.max_idx = max_idx

        self.confirmed = False
        self.data = None
        self.setWindowTitle("Remove Chord")

        layout = QFormLayout()
        self.setLayout(layout)

        self.index_box = QLineEdit()
        self.accept_button = QPushButton('Remove chord')

        i_label = QLabel('index')

        index_tip = 'The index where the chord or note is removed from the score'

        self.index_box.setStatusTip(index_tip)
        i_label.setStatusTip(index_tip)

        self.index_box.setText(str(self.max_idx))
        self.index_box.setValidator(QIntValidator())

        self.accept_button.clicked.connect(self.compute)

        layout.addRow(i_label, self.index_box)

        layout.addWidget(self.accept_button)

    def event(self, a0: QtCore.QEvent) -> bool:
        if isinstance(a0, QStatusTipEvent):
            x = self
            for _ in range(4):
                x = x.parent()
            x.status.showMessage(a0.tip(), 3000)
        else:
            QDialog.event(self, a0)
        return True

    def compute(self):
        idx_content = int(self.index_box.text())

        if self.max_idx < idx_content or idx_content < 1:
            QMessageBox.warning(self, "Warning", f'Invalid index: 1 <= {idx_content} <= {self.max_idx}')
            return

        self.confirmed = True
        self.data = idx_content

        self.done(0)

    @classmethod
    def run(cls, parent, max_idx):
        this = cls(parent, max_idx)
        this.exec_()
        if this.confirmed:
            return this.data
        return None
