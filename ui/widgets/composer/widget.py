from PyQt5.QtWidgets import QWidget, QGridLayout, QMenuBar, QAction, QFileDialog

from core import create_midi
from ui.widgets.composer.display import LilyDisplay
from ui.widgets.dialogs import CreditsModal


class Composer(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.status = self.parent().status

        layout = QGridLayout()
        self.setLayout(layout)

        main_bar = QMenuBar()
        main_bar.setContentsMargins(0, 0, 0, 0)
        file_menu = main_bar.addMenu('&File')

        edit_menu = main_bar.addMenu('&Edit')
        view_menu = main_bar.addMenu('&View')
        tools_menu = main_bar.addMenu('&Tools')
        help_menu = main_bar.addMenu('&Help')

        credits_act = QAction('&About', self)
        credits_act.setStatusTip('About MBox')
        credits_act.triggered.connect(self.credit_popup)

        export_midi_act = QAction('&Export Midi File', self)
        export_midi_act.setStatusTip('Export to .mid')
        export_midi_act.triggered.connect(self.export_midi)

        file_menu.addAction(export_midi_act)

        help_menu.addAction(credits_act)

        layout.setMenuBar(main_bar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.disp = LilyDisplay(self)
        layout.addWidget(self.disp)

    @staticmethod
    def credit_popup():
        modal = CreditsModal()
        modal.exec_()

    def export_midi(self):
        file_options = QFileDialog.getSaveFileName(self, 'Export Midi file', '', 'Midi files (*.mid)')
        file_path = file_options[0]

        self.disp.builder.export_midi(file_path)

