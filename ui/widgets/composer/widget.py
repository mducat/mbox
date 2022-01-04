from PyQt5.QtWidgets import QWidget, QGridLayout, QMenuBar, QAction

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

        help_menu.addAction(credits_act)

        layout.setMenuBar(main_bar)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        disp = LilyDisplay(self)
        layout.addWidget(disp)

    @staticmethod
    def credit_popup():
        modal = CreditsModal()
        modal.exec_()
