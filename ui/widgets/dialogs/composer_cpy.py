import math

from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator, QStatusTipEvent
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QLabel, QMessageBox, QStatusBar

from core import Note, Chord


class ComposerCpyChord(QDialog):

    def __init__(self, parent, max_idx, cpy_from):
        QDialog.__init__(self, parent)

        self.max_idx = max_idx
        self.cpy_from = cpy_from

        self.confirmed = False
        self.data = None
        self.setWindowTitle("Copy Chord")

        layout = QFormLayout()
        self.setLayout(layout)

        self.index_box = QLineEdit()
        self.length_box = QLineEdit()
        self.accept_button = QPushButton('Copy chord')

        i_label = QLabel('index')
        l_label = QLabel('note length')

        index_tip = 'The index where the chord or note is inserted in the score'
        length_tip = 'The length of the note, must be a power of 2. e.g. 1, 2, 4, ... up to 16'

        self.index_box.setStatusTip(index_tip)
        i_label.setStatusTip(index_tip)

        self.length_box.setStatusTip(length_tip)
        l_label.setStatusTip(length_tip)

        self.index_box.setText(str(self.max_idx))
        self.index_box.setValidator(QIntValidator())

        self.length_box.setText('4')
        self.length_box.setValidator(QIntValidator())

        self.accept_button.clicked.connect(self.compute)

        layout.addRow(i_label, self.index_box)
        layout.addRow(l_label, self.length_box)

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
        len_content = int(self.length_box.text())

        if self.max_idx < idx_content or idx_content < 0:
            QMessageBox.warning(self, "Warning", f'Invalid index: 0 <= {idx_content} <= {self.max_idx}')
            return

        if 16 < len_content or len_content < 0:
            QMessageBox.warning(self, "Warning", f'Invalid length: 0 <= {len_content} <= 8')
            return

        def check_power(n_len):
            return math.ceil(math.log2(n_len)) == math.floor(math.log2(n_len))

        if not check_power(len_content):
            QMessageBox.warning(self, "Warning", f'Invalid length: {len_content} is not a power of 2')
            return

        self.confirmed = True
        self.data = (self.cpy_from.chord.clone(), idx_content, len_content)

        self.done(0)

    @classmethod
    def run(cls, parent, max_idx, cpy_from):
        this = cls(parent, max_idx, cpy_from)
        this.exec_()
        if this.confirmed:
            return this.data
        return None
