import math
from shutil import copyfile

import xlrd
import xlwt
import cv2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog

from Create_exp import Ui_Create_Dialog
from Visual_log import Visual_logic

header1 = ['实验名称', '图像地址', '描述', '目视定位', '目视点对']
header2 = ['编号', '创建时间', '预处理1', '预处理2', '预处理3', '预处理4',
           '算法', '识别树木数量', '正确识别数量', '错判单木数目', '漏判单木数目', '识别精度', '点对']
path = ""


class Logic_create(QDialog, Ui_Create_Dialog):

    def __init__(self, parent=None):
        super(Logic_create, self).__init__(parent)
        self.setupUi(self)
        self.Button_open_img.clicked.connect(self.get_img)  # 选择图片绑定事件

    def get_img(self):
        global path
        path, _ = QFileDialog.getOpenFileName(None, '选择图像', r"")  # 打开资源管理器，path为原图片绝对路径
        print(path)
        img = QImage()  # 根据类创建对象img
        img.load(path)  # 加载图片
        self.img_url.setText(path)

    def accept(self):  # 1’
        global path
        # log =Visual_logic()
        # log.getImgURL(path)
        # log.show()
        # log.exec_()
        print("ss")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet1 = workbook.add_sheet('detail')
        worksheet2 = workbook.add_sheet('record')
        for i in range(len(header1)):
            worksheet1.write(0, i, header1[i])
        for i in range(len(header2)):
            worksheet2.write(0, i, header2[i])
        # images = cv2.imread(path)  # 打开原图
        pr_path=path #记录一下源地址
        img_name = ""
        for i in range(len(path)):
            if path[len(path) - 1 - i] == '/':
                path = path[len(path) - 1 - i:]
                img_name = path[1:]
                break
        for i in range(len(img_name)):
            if img_name[i]=='.':
                img_name=img_name[0:i]
                break
        print(img_name)

        copyfile(pr_path, 'D:/Tree/img' + path)# 原图片备份,使用备份图片作为存储地址//1.4日修改
        path = "D:/Tree/img" + path

        # cv2.imwrite(path, images)
        worksheet1.write(1, 0, img_name)
        worksheet1.write(1, 1, path)
        worksheet1.write(1, 2, self.textEdit.toPlainText())
        print(self.textEdit.toPlainText())
        worksheet1.write(1, 3, 0)
        workbook.save('D:/Tree/exp/'+img_name+'.xls')
        self.close()
    def get_path(self):
        return path
