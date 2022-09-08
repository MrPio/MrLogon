import os
import pickle
import shutil
import time
import webbrowser
from types import NoneType

import pyautogui
import requests
import userpaths
from favicon import favicon
from pynput.keyboard import Controller

from MrCrypto import MrCrypto

path = userpaths.get_local_appdata() + '\MrLogon'


class Login():
    def __init__(self, title, url, username, password):
        self.title = title
        self.url = url
        self.username = username
        self.password = password
        self.beforeActions = []
        self.betweenActions = []
        self.afterActions = []
        self.hasIcon=False
        self.downloadFavicon()

    def downloadFavicon(self):
        try:
            icons = favicon.get(MrCrypto().decrypt(self.url))

            icon= icons[0]

            response = requests.get(icon.url, stream=True)
            with open(userpaths.get_local_appdata() + '\MrLogon' + '\\' + self.title + '.ico', 'wb') as image:
                for chunk in response.iter_content(1024):
                    image.write(chunk)
            self.hasIcon=True
        except Exception as e:
            print (e)

    def addBeforeActions(self, actions: list):
        self.beforeActions = actions

    def addBetweenActions(self, actions: list):
        self.betweenActions = actions

    def addAfterActions(self, actions: list):
        self.afterActions = actions

    def save(self):
        with open(userpaths.get_local_appdata() + '\MrLogon' + '\\' + self.title + '.login', 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def rename(self, newTitle):
        path=userpaths.get_local_appdata() + '\MrLogon'
        os.remove(path + '\\' + self.title + '.login')
        if self.hasIcon:
            shutil.copyfile(path+ '\\' + self.title + '.ico', path+ '\\' + newTitle + '.ico')
            os.remove(path + '\\' + self.title + '.ico')


        self.title = newTitle
        self.save()

    def duplicate(self):
        if self.hasIcon:
            path=userpaths.get_local_appdata() + '\MrLogon'
            shutil.copyfile(path+ '\\' + self.title + '.ico', path+ '\\' + self.title + '1.ico')

        self.title += '1'
        self.save()
        self.title = self.title[:-1]

    def wait_for_element_appear(self, element_path: str, wait=8.0, confidence=0.7, grayscale=False):
        start = time.time()
        while True:
            element = pyautogui.locateOnScreen(element_path, grayscale=grayscale, confidence=confidence)
            if time.time() - start > wait:
                print(f"I've waited too much! [{element_path}]")
                return None
            pyautogui.sleep(0.5)
            if type(element) is not NoneType:
                break
        return element

    def click_center(self, element):
        pyautogui.click(x=element.left + int(element.width / 2),
                        y=element.top + int(element.height / 2))

    def perform(self):
        try:
            keyboard = Controller()
            mc = MrCrypto()
            webbrowser.open(mc.decrypt(self.url), new=2)
            pyautogui.sleep(0.6)

            self.execute(0)

            keyboard.type(mc.decrypt(self.username))
            if len(self.betweenActions) == 0:
                pyautogui.press("tab")
            else:
                self.execute(1)
            keyboard.type(mc.decrypt(self.password))
            pyautogui.press("enter")

            self.execute(2)
        except:
            pass

    def execute(self, index):
        list = [self.beforeActions, self.betweenActions, self.afterActions][index]
        downLast = []
        for action in list:
            prefix, suffix = str(action).split(':')
            if prefix == 'down':
                downLast.append(suffix)
                pyautogui.keyDown(suffix)
            elif prefix == 'up':
                if suffix in downLast:
                    pyautogui.keyUp(suffix)
                    downLast.remove(suffix)
                else:
                    pyautogui.press(suffix)

            elif prefix == 'wait_on':
                self.wait_for_element_appear(path + '\\' + suffix, wait=8, confidence=0.94)
            elif prefix == 'click_on':
                el = self.wait_for_element_appear(path + '\\' + suffix, wait=8, confidence=0.94)
                self.click_center(el)
