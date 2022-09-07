import pickle
import userpaths
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QLineEdit, QWidget, QFormLayout, QLabel

from main import InputKeySequence


class AddAction:
    path = userpaths.get_local_appdata() + '\MrLogon'
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    dialog=None

    def onBefore(self):
        self.show(0)
    def onBetween(self):
        self.show(1)

    def onAfter(self):
        self.show(2)

    def show(self,index):
        self.ui = InputKeySequence(self.login,index)
        self.ui.setupUi()
        self.ui.show()
        # self.inputDialog.show()

    def __init__(self, login):
        super().__init__()
        self.login=login

    def setupUi(self, dialog):
        self.dialog=dialog
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(20)
        style="background-color: rgb(76, 186, 232);"

        self.before = QtWidgets.QPushButton()
        self.before.setStyleSheet(style)
        self.before.setText('Before login')
        self.before.setFont(font)
        self.before.clicked.connect(self.onBefore)

        self.between = QtWidgets.QPushButton()
        self.between.setText('Between user and pswd')
        self.between.setStyleSheet(style)
        self.between.setFont(font)
        self.before.clicked.connect(self.onBetween)

        self.after = QtWidgets.QPushButton()
        self.after.setText('After login')
        self.after.setStyleSheet(style)
        self.after.setFont(font)
        self.before.clicked.connect(self.onAfter)


        flo = QFormLayout()
        flo.addRow('', self.before)
        flo.addRow('', self.between)
        flo.addRow('', self.after)


        dialog.setLayout(flo)
        dialog.setWindowTitle("New Login")

