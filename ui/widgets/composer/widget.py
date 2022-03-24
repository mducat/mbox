from PyQt5.QtWidgets import QWidget, QGridLayout, QMenuBar, QAction, QFileDialog

from core import create_midi
from ui.widgets.composer.display import LilyDisplay
from ui.widgets.dialogs import CreditsModal, ComposerAddChord, ComposerDelChord


class Composer(QWidget):

    def __init__(self, parent):
        QWidget.__init__(self, parent)

        self.status = self.parent().status

        layout = QGridLayout()
        self.setLayout(layout)

        self.main_bar = QMenuBar()
        self.main_bar.setContentsMargins(0, 0, 0, 0)

        self.setup_file_menu()

        edit_menu = self.main_bar.addMenu('&Edit')
        view_menu = self.main_bar.addMenu('&View')

        self.setup_tools_menu()

        help_menu = self.main_bar.addMenu('&Help')

        credits_act = QAction('&About', self)
        credits_act.setStatusTip('About MBox')
        credits_act.triggered.connect(self.credit_popup)

        help_menu.addAction(credits_act)

        layout.setMenuBar(self.main_bar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.disp = LilyDisplay(self)
        layout.addWidget(self.disp)

    def setup_tools_menu(self):
        tools_menu = self.main_bar.addMenu('&Tools')

        add_act = QAction('&Add Note/Chord', self)
        add_act.setShortcut('Ctrl+A')
        add_act.setStatusTip('Add a note or a chord to the composer display')
        add_act.triggered.connect(self.add_chord)

        del_act = QAction('&Remove Note/Chord', self)
        del_act.setShortcut('Ctrl+D')
        del_act.setStatusTip('Remove a note or a chord to the composer display')
        del_act.triggered.connect(self.del_chord)

        tools_menu.addAction(add_act)
        tools_menu.addAction(del_act)

    def setup_file_menu(self):
        file_menu = self.main_bar.addMenu('&File')

        save_act = QAction('&Save score', self)
        save_act.setShortcut('Ctrl+S')
        save_act.setStatusTip('Save as')
        save_act.triggered.connect(self.save_composed)

        open_act = QAction('&Open score', self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open project')
        open_act.triggered.connect(self.open_composed)

        export_midi_act = QAction('&Export Midi File', self)
        export_midi_act.setStatusTip('Export to .mid')
        export_midi_act.triggered.connect(self.export_midi)

        file_menu.addAction(save_act)
        file_menu.addAction(open_act)
        file_menu.addSeparator()
        file_menu.addAction(export_midi_act)

        return file_menu

    @staticmethod
    def credit_popup():
        modal = CreditsModal()
        modal.exec_()

    def export_midi(self):
        file_options = QFileDialog.getSaveFileName(self, 'Export Midi file', '', 'Midi files (*.mid)')
        file_path = file_options[0]

        if not file_path:
            return

        self.disp.builder.export_midi(file_path)

    def save_composed(self):
        file_options = QFileDialog.getSaveFileName(self, 'Save Score', '', 'MBox Composer file (*.mbox)')
        file_path = file_options[0]

        if not file_path:
            return

        self.disp.builder.save_controller(file_path)

    def open_composed(self):
        file_options = QFileDialog.getOpenFileName(self, 'Open Score', '', 'MBox Composer file (*.mbox)')
        file_path = file_options[0]

        if not file_path:
            return

        try:
            self.disp.builder.restore_controller(file_path)

            self.disp.update()
        except Exception as e:
            print(e)

    def add_chord(self):
        staff = self.disp.builder.staffs[0]
        data = ComposerAddChord.run(self, len(staff.notes))

        if data is None:
            return

        chord, idx, nlen = data

        staff.notes.insert(idx, (chord, nlen))
        self.disp.update()

    def del_chord(self):
        staff = self.disp.builder.staffs[0]
        data = ComposerDelChord.run(self, len(staff.notes))

        if data is None:
            return

        idx = data

        if len(staff.notes) == 0:
            return

        staff.notes.pop(idx - 1)
        self.disp.update()
