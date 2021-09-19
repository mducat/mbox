from PyQt5 import Qt
from PyQt5.QtWidgets import QApplication, QAction, qApp, QStyle, QTabWidget, QWidget, QGridLayout, QMenuBar, QDialog

from ui.widgets.dialogs import CreditsModal


class MboxWindow(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle('MBox')
        self.setFixedSize(1200, 800)

        layout = QGridLayout()
        self.setLayout(layout)

        exit_act = QAction(self.style().standardIcon(QStyle.SP_DialogCancelButton), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)

        credits_act = QAction('&About', self)
        credits_act.setStatusTip('About MBox')
        credits_act.triggered.connect(self.credit_popup)

        main_bar = QMenuBar()

        file_menu = main_bar.addMenu('&File')
        file_menu.addAction(exit_act)

        edit_menu = main_bar.addMenu('&Edit')
        view_menu = main_bar.addMenu('&View')
        tools_menu = main_bar.addMenu('&Tools')
        help_menu = main_bar.addMenu('&Help')

        help_menu.addAction(credits_act)

        layout.addWidget(main_bar)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Composer")
        self.tabs.addTab(self.tab2, "String chord finder")

        layout.addWidget(self.tabs)

    @staticmethod
    def credit_popup():
        modal = CreditsModal()
        modal.exec_()

    @classmethod
    def run(cls):
        app = QApplication.instance()

        if not app:
            app = QApplication([])

        this = cls()
        this.show()

        app.exec_()

        return this
