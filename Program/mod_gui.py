import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mod_ui import *

class ModGui(QWidget):
    def __init__(self, parent=None):
        super(ModGui, self).__init__()
        self.ui = Ui_FormMod()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        self.setStyleSheet('background-color: rgb(230, 230, 230);')
        # 禁用窗口最大化 拉伸
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)    