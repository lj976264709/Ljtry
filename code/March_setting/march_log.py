from shutil import copyfile

from PyQt5.QtWidgets import QDialog
import xlrd

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os

from imageCut import Form
from march import Ui_MarchSetting

list_1 = []
list_2 = []


class march_log(QDialog, Ui_MarchSetting):
    def __init__(self, parent=None):
        super(march_log, self).__init__(parent)
        self.setupUi(self)
        self.init()

    def init(self):
        global list_1
        for tp in os.walk('D:\Tree\Template'):
            list_1=tp[1]
            break
        # print(list_1)
        slm1 = QStringListModel()
        slm1.setStringList(list_1)
        self.listView_set.setModel(slm1)
        self.listView_set.clicked.connect(self.list_Clicked)
        self.addBT1.clicked.connect(self.addMarchSet)
        self.deleteBT1.clicked.connect(self.deleteSet)
        self.addBT2.clicked.connect(self.addMarch)

    def addMarch(self):
        log=Form()
        log.show()
        log.exec_()

    def deleteSet(self):
        index = self.listView_set.selectedIndexes()[0].row()
        path = 'D:\Tree\Template\\'+list_1[index]
        if os.path.exists(path):
            os.removedirs(path)
        self.init()

    def addMarchSet(self):
        text, ok = QInputDialog.getText(self, "模板集合添加", "请输入新集合名称")
        if ok:
            print(text)
        else:
            return
        path='D:\Tree\Template\\'+text
        if os.path.exists(path):
            return
        os.makedirs(path)
        self.init()

    def list_Clicked(self):
        global list_2
        index = self.listView_set.selectedIndexes()[0].row()
        print(index)
        for tp in os.walk('D:\Tree\Template\\'+list_1[index]):
            list_2=tp[2]
            break
        slm = QStringListModel()
        slm.setStringList(list_2)
        self.listView.setModel(slm)