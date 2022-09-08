import pickle

import userpaths
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLineEdit, QWidget, QFormLayout, QLabel

from MrCrypto import MrCrypto
from login import Login


class AddLogin(QWidget):
    path = userpaths.get_local_appdata() + '\MrLogon'
    dialog=None

    def __init__(self, Ui_MainWindow):
        super().__init__()
        self.Ui_MainWindow=Ui_MainWindow

    def setupUi(self, dialog):
        AddLogin.dialog=dialog
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(20)

        self.title = QLineEdit()
        self.title.setFont(font)

        self.url = QLineEdit()
        self.url.setFont(font)

        self.username = QLineEdit()
        self.username.setFont(font)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFont(font)

        flo = QFormLayout()
        label = QLabel('Login title: ')
        label.setFont(font)
        flo.addRow(label, self.title)

        label = QLabel('Login url: ')
        label.setFont(font)
        flo.addRow(label, self.url)

        label = QLabel('Username: ')
        label.setFont(font)
        flo.addRow(label, self.username)

        label = QLabel('Password: ')
        label.setFont(font)
        flo.addRow(label, self.password)

        add = QtWidgets.QPushButton('Add')
        add.setFont(font)
        add.clicked.connect(self.confirm)

        exit = QtWidgets.QPushButton('Cancel')
        exit.setFont(font)
        exit.clicked.connect(dialog.close)

        flo.addRow(add)
        flo.addRow(exit)

        dialog.setLayout(flo)
        dialog.setWindowTitle("New Login")

    def confirm(self):
        if not '' in [self.url.text(), self.password.text(), self.username.text(), self.title.text()]:

            cripto=MrCrypto()
            login=Login(
                self.title.text(),
                cripto.encrypt(self.url.text()),
                cripto.encrypt(self.username.text()),
                cripto.encrypt(self.password.text())
            ).save()

            AddLogin.dialog.close()
            self.Ui_MainWindow.reload()

        print('err compila tutti')


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = AddLogin()
#     win.setupUi(QtWidgets.QDialog())
#     win.show()
#     sys.exit(app.exec())
