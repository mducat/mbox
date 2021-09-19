from PyQt5.QtWidgets import QMessageBox


class CreditsModal(QMessageBox):

    def __init__(self, parent=None):
        QMessageBox.__init__(self, parent)

        self.setWindowTitle("MBox credits")
        self.setText("Music theory and composition toolbox.\nAuthor: mducat.")
        self.setStandardButtons(QMessageBox.Ok)
        self.setIcon(QMessageBox.Information)
