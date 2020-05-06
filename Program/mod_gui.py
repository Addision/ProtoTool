import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from mod_ui import *
from common import *

class ModGui(QDialog):
    def __init__(self, mod_type):
        super(ModGui, self).__init__()
        self.mod_type = mod_type
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
        self.ui.LetModName.editingFinished.connect(self.handleText)
        if self.mod_type == ModType.PUBLIC:
            self.ui.LetModName.setPlaceholderText('PublicXxxxx')
        self.btn_ok = False

    def handleText(self):
        mod_name = self.ui.LetModName.text().strip()
        if self.mod_type == ModType.PUBLIC:
            if 'Public' not in mod_name.title():
                self.ui.LetModName.setText('Public'+mod_name.title())
        else:
            self.ui.LetModName.setText(mod_name.title())
        pass

    
    def getInfo(self,):
        mod_name = self.ui.LetModName.text().strip()
        mod_comment = self.ui.LetModCmt.text().strip()
        return mod_name, mod_comment

    @staticmethod        
    def getModInfo(mod_type):
        mod_gui = ModGui(mod_type)
        result = mod_gui.exec_()
        if result == QDialog.Accepted:
            mod_name, mod_comment = mod_gui.getInfo()
            return True, mod_name, mod_comment
        else:
            return False,'',''            
