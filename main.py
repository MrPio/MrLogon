import typing
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt6.QtCore import Qt
import sys


class InputKeySequence(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)


    def onCancel(self):
        self.close()

    def onConfirm(self):
        pass


    def __init__(self, login,index,parent=None):
        super().__init__(parent)
        self.login=login
        self.index=index


    def setupUi(self):
        self.setStyleSheet("background-color: rgba(84, 202, 255,100);")
        self.setFixedSize(300,300)
        self.setWindowFlags(QtCore.Qt.WindowType.Window.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(20)
        style="background-color: rgb(76, 186, 232);"

        self.cancel = QtWidgets.QPushButton()
        self.cancel.setStyleSheet(style)
        self.cancel.setText('Cancel')
        self.cancel.setFont(font)
        self.cancel.clicked.connect(self.onCancel)

        self.confirm = QtWidgets.QPushButton()
        self.confirm.setStyleSheet(style)
        self.confirm.setText('Confirm')
        self.confirm.setFont(font)
        self.confirm.clicked.connect(self.onConfirm)

        self.keys=QtTextView
        # aggiungi la textbox che fa vedere il testo dei tasti metre lo modifico

        flo = QFormLayout()
        flo.setAlignment(Qt.AlignmentFlag.AlignLeading)
        flo.addRow('', self.confirm)
        flo.addRow('', self.cancel)
        flo.addRow('', self.cancel)
        self.setLayout(flo)


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        str= self.keySelector(a0)
        if str==None:
            str=a0.text()
        print(str)

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        str= self.keySelector(a0)
        if str==None:
            str=a0.text()
        print(str)

    def keySelector(self,key: QtGui.QKeyEvent):
        if key.key()==Qt.Key.Key_Control:
            return 'ctrl'
        elif key.key() == Qt.Key.Key_Shift:
            return 'shift'
        elif key.key()==Qt.Key.Key_Tab:
            return 'tab'
        elif key.key()==Qt.Key.Key_Meta:
            return 'win'
        elif key.key()==Qt.Key.Key_Alt:
            return 'alt'
        elif key.key()==Qt.Key.Key_Enter:
            return 'enter'
        elif key.key()==Qt.Key.Key_Escape:
            return 'esc'
        elif key.key()==Qt.Key.Key_Return:
            return 'return'
        return None

    def textchanged(self, text):
        print("Changed: " + text)

    def enterPress(self):
        print("Enter pressed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = InputKeySequence(None,None)
    win.show()
    sys.exit(app.exec())
