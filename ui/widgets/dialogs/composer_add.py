import math

from PyQt5 import QtCore
from PyQt5.QtGui import QIntValidator, QStatusTipEvent
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QFormLayout, QLabel, QMessageBox, QStatusBar

from core import Note, Chord


class ComposerAddChord(QDialog):

    def __init__(self, parent, max_idx):
        QDialog.__init__(self, parent)

        self.max_idx = max_idx

        self.confirmed = False
        self.data = None
        self.setWindowTitle("Add Chord")

        layout = QFormLayout()
        self.setLayout(layout)

        self.text_box = QLineEdit()
        self.index_box = QLineEdit()
        self.length_box = QLineEdit()
        self.accept_button = QPushButton('Add chord')

        n_label = QLabel('notes')
        i_label = QLabel('index')
        l_label = QLabel('note length')

        text_tip = 'A list of notes, separated by commas. Notes can be followed by octave, e.g. "e5, c 3" or "si 3, la4" ...'
        index_tip = 'The index where the chord or note is inserted in the score'
        length_tip = 'The length of the note, must be a power of 2. e.g. 1, 2, 4, ... up to 16'

        self.text_box.setStatusTip(text_tip)
        n_label.setStatusTip(text_tip)

        self.index_box.setStatusTip(index_tip)
        i_label.setStatusTip(index_tip)

        self.length_box.setStatusTip(length_tip)
        l_label.setStatusTip(length_tip)

        self.index_box.setText(str(self.max_idx))
        self.index_box.setValidator(QIntValidator())

        self.length_box.setText('4')
        self.length_box.setValidator(QIntValidator())

        self.accept_button.clicked.connect(self.compute)

        layout.addRow(n_label, self.text_box)
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
        chord_content = self.text_box.text()
        idx_content = int(self.index_box.text())
        len_content = int(self.length_box.text())

        chord_notes = []

        for parsable in chord_content.split(','):
            if len(parsable.strip()) == 0:
                continue
            try:
                n = Note(parsable.strip().upper())
                chord_notes.append(n)
            except Exception as e:
                QMessageBox.warning(self, "Warning", str(e))
                return

        try:
            chord_value = Chord(chord_notes)
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
            return

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
        self.data = (chord_value, idx_content, len_content)

        self.done(0)

    @classmethod
    def run(cls, parent, max_idx):
        this = cls(parent, max_idx)
        this.exec_()
        if this.confirmed:
            return this.data
        return None
