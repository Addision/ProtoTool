import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mod_ui import *


class ModGui(QDialog):
    def __init__(self, parent=None):
        super(ModGui, self).__init__(parent)
        self.ui = Ui_DialogMod()
        self.ui.setupUi(self)
        self.setWindowOpacity(0.96)
        self.setStyleSheet('background-color: rgb(230, 230, 230);')
        # 禁用窗口最大化 拉伸
        self.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # button
        self.ui.BtnModOk.clicked.connect(self.accept)
        self.ui.BtnModCancel.clicked.connect(self.reject)
        self.mod_name = ""
        self.mod_comment = ""
        self.btn_ok = False
    
    def getInfo(self):
        self.mod_name = self.ui.LetModName.text().strip()
        self.mod_comment = self.ui.LetModCmt.text().strip()
        return self.mod_name, self.mod_comment

    @staticmethod        
    def getModInfo():
        mod_gui = ModGui()
        result = mod_gui.exec_()
        if result == QDialog.Accepted:
            mod_name, mod_comment = mod_gui.getInfo()
            return True, mod_name, mod_comment
        else:
            return False,'',''     
