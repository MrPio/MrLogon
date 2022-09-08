import base64
import os
import threading
import time
import typing

import pyperclip
import userpaths
import win32api
from PIL import ImageGrab
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QLineEdit, QWidget, QFormLayout
from PyQt6.QtGui import QIntValidator, QDoubleValidator, QFont
from PyQt6.QtCore import Qt
import sys


class InputKeySequence(QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.QEvent)
    keys=[]
    def onCancel(self):
        self.close()

    def onClear(self):
        self.unlisten()
        InputKeySequence.keys=[]
        self.keys.clear()

    def onConfirm(self):
        if self.index==0:
            self.login.addBeforeActions(InputKeySequence.keys)
        elif self.index==1:
            self.login.addBetweenActions(InputKeySequence.keys)
        elif self.index==2:
            self.login.addAfterActions(InputKeySequence.keys)

        self.login.save()
        self.close()
        pass

    def onListen(self):
        if not self.listening:
            self.listen.setStyleSheet(self.styleListening)
            self.listen.setText('Listening for keys...')
        else:
            self.listen.setStyleSheet(self.styleNotListening)
            self.listen.setText('Not listening')

        self.listening=not self.listening



    def __init__(self, login,index,parent=None):
        super().__init__(parent)
        self.login=login
        self.index=index
        self.listening=False

    def onWaitOn(self):
        InputKeySequence.waitForScreenshot=True
        filename=self.grabScreenshot()
        if filename!=None:
            InputKeySequence.keys.append('wait_on:' + filename)
            self.keys.setText(str(InputKeySequence.keys))

    def onClickOn(self):
        InputKeySequence.waitForScreenshot = True
        filename=self.grabScreenshot()
        if filename!=None:
            InputKeySequence.keys.append('click_on:' + filename)
            self.keys.setText(str(InputKeySequence.keys))

    def showToast(self):
        from win10toast import ToastNotifier
        ToastNotifier().show_toast("Screenshot",'Waiting 2 seconds...',duration=2)

    def unlisten(self):
        self.listening = False
        self.listen.setStyleSheet(self.styleNotListening)
        self.listen.setText('Not listening')
    def grabScreenshot(self):
        self.unlisten()

        threading.Thread(target=self.showToast).start()
        time.sleep(2)
        hwcode = win32api.MapVirtualKey(0x2A, 0)
        win32api.keybd_event(0x2A, hwcode)
        recent_value = ImageGrab.grabclipboard()
        while True:
            image = ImageGrab.grabclipboard()
            if recent_value == image:
                time.sleep(0.5)
                continue
            if image != None:
                path = userpaths.get_local_appdata() + '\MrLogon'
                count=0
                while str(count)+'.png' in next(os.walk(path), (None, None, []))[2]:
                    count+=1
                filename=str(count)+'.png'

                image.convert('RGB').save(path+'\\'+filename, "PNG")
                InputKeySequence.waitForScreenshot = False

                return filename
            time.sleep(0.25)

    def setupUi(self):
        InputKeySequence.waitForScreenshot = False
        self.setStyleSheet("background-color: rgba(84, 202, 255,100);")
        self.setFixedSize(620,350)
        self.setWindowFlags(QtCore.Qt.WindowType.Window.FramelessWindowHint)
        font = QtGui.QFont()
        font.setFamily("Corbel")
        font.setPointSize(20)
        style="background-color: rgb(76, 186, 232);"
        style2 = "background-color: rgb(234, 234, 118);"
        self.styleListening = "background-color: rgb(76, 186, 232);"
        self.styleNotListening = "background-color: rgb(122, 54, 90);"

        self.clear = QtWidgets.QPushButton()
        self.clear.setStyleSheet(style)
        self.clear.setText('Clear')
        self.clear.setFont(font)
        self.clear.clicked.connect(self.onClear)

        self.cancel = QtWidgets.QPushButton()
        self.cancel.setStyleSheet(style)
        self.cancel.setText('Cancel')
        self.cancel.setFont(font)
        self.cancel.clicked.connect(self.onCancel)

        self.confirm = QtWidgets.QPushButton()
        self.confirm.setStyleSheet(style)
        self.confirm.setText('Save')
        self.confirm.setFont(font)
        self.confirm.clicked.connect(self.onConfirm)

        self.wait_on = QtWidgets.QPushButton()
        self.wait_on.setStyleSheet(style2)
        self.wait_on.setText('Wait for')
        self.wait_on.setFont(font)
        self.wait_on.clicked.connect(self.onWaitOn)

        self.click_on = QtWidgets.QPushButton()
        self.click_on.setStyleSheet(style2)
        self.click_on.setText('Click on')
        self.click_on.setFont(font)
        self.click_on.clicked.connect(self.onClickOn)

        self.horizontalLayout=QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(self.wait_on)
        self.horizontalLayout.addWidget(self.click_on)

        old_actions=[]
        if self.index == 0:
            old_actions = self.login.beforeActions
        elif self.index==1:
            old_actions=self.login.betweenActions
        elif self.index==2:
            old_actions=self.login.afterActions
        InputKeySequence.keys=old_actions

        self.scrollView=QtWidgets.QScrollArea()
        self.keys=QtWidgets.QLabel(str(old_actions))
        self.keys.setFont(font)
        self.keys.setWordWrap(True)
        self.scrollView.setWidgetResizable(True)
        self.scrollView.setWidget(self.keys)

        self.listen = QtWidgets.QPushButton()
        self.listen.setStyleSheet(self.styleNotListening)
        self.listen.setText('Not listening')
        self.listen.setFont(font)
        self.listen.clicked.connect(self.onListen)


        flo = QFormLayout()
        flo.setAlignment(Qt.AlignmentFlag.AlignLeading)
        flo.addRow('', self.confirm)
        flo.addRow('',self.horizontalLayout)
        flo.addRow('', self.clear)
        flo.addRow('', self.cancel)
        flo.addRow('',self.scrollView)
        flo.addRow('',self.listen)
        self.setLayout(flo)


    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self.listening:
            return
        string= self.keySelector(a0)
        if string==None:
            string=a0.text()
        InputKeySequence.keys.append('down:'+string)
        self.keys.setText(str(InputKeySequence.keys))

    def keyReleaseEvent(self, a0: QtGui.QKeyEvent) -> None:
        if not self.listening:
            return
        string= self.keySelector(a0)
        if string==None:
            string=a0.text()
        InputKeySequence.keys.append('up:'+string)
        self.keys.setText(str(InputKeySequence.keys))

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
        elif key.key()==Qt.Key.Key_Space:
            return 'space'
        return None

    def textchanged(self, text):
        print("Changed: " + text)

    def enterPress(self):
        print("Enter pressed")


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = InputKeySequence(None,None)
#     win.show()
#     sys.exit(app.exec())
