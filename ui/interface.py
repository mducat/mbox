from PyQt5.QtWidgets import QApplication, QAction, qApp, QStyle, QTabWidget, QWidget, QMainWindow

from ui.widgets import ChordTab, StringTab, Composer, PianoTab

class MboxWindow(QMainWindow):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('MBox')
        self.setFixedSize(1200, 800)

        self.status = self.statusBar()
        self.status.showMessage("Ready", 3000)

        exit_act = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        self.addAction(exit_act)

        self.tabs = QTabWidget()
        self.composer = Composer(self)
        self.tonal_map = ChordTab()
        self.string_tab = StringTab()
        self.piano_tab = PianoTab()

        self.tabs.addTab(self.composer, "Composer")
        self.tabs.addTab(self.tonal_map, "Tonal mapping")
        self.tabs.addTab(self.string_tab, "String chord finder")
        self.tabs.addTab(self.piano_tab, "Piano chord finder")

        self.setCentralWidget(self.tabs)
        self.setContentsMargins(5, 5, 5, 5)

    @classmethod
    def run(cls):
        app = QApplication.instance()

        if not app:
            app = QApplication([])

        this = cls()
        this.show()

        app.exec_()

        return this
