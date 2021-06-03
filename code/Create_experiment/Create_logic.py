import math
import os
from shutil import copyfile
from pathlib import Path
import xlrd
import xlwt
import cv2
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog

from Create_exp import Ui_Create_Dialog
from Visual_log import Visual_logic

header1 = ['实验名称', '图像地址', '描述', '目视定位', '目视点对', '标记尺寸', '预处理文件所在位置']
header2 = ['编号', '创建时间', '预处理编码',
           '算法', '识别树木数量', '正确识别数量', '误判单木数目', '漏判单木数目', '准确率', '误判率', '漏判率', '匹配率', '点对']
path = ""
directory = ''


class Logic_create(QDialog, Ui_Create_Dialog):

    def __init__(self, parent=None):
        super(Logic_create, self).__init__(parent)
        self.setupUi(self)
        self.Button_open_img.clicked.connect(self.get_img)  # 选择图片绑定事件
        self.Button_open_file.clicked.connect(self.get_file)

    def get_file(self):
        global directory
        directory = QFileDialog.getExistingDirectory(None, "选取实验区文件夹", "D:/Tree")  # 起始路径
        self.file_url.setText(directory)

    def get_img(self):
        global path
        path, _ = QFileDialog.getOpenFileName(None, '选择图像', r"")  # 打开资源管理器，path为原图片绝对路径
        print(path)
        # img = QImage()  # 根据类创建对象img
        # img.load(path)  # 加载图片  这有什么用么？我之前写这个干啥 貌似是真的没啥用
        self.img_url.setText(path)

    def accept(self):  # 1’
        global path
        print("ss")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet1 = workbook.add_sheet('detail')
        worksheet2 = workbook.add_sheet('record')
        for i in range(len(header1)):
            worksheet1.write(0, i, header1[i])
        for i in range(len(header2)):
            worksheet2.write(0, i, header2[i])
        # images = cv2.imread(path)  # 打开原图
        pr_path = path  # 记录一下源地址
        img_name = ""
        img_name_all = ''
        for i in range(len(path)):
            if path[len(path) - 1 - i] == '/':
                path = path[len(path) - 1 - i:]
                img_name = path[1:]
                img_name_all = img_name
                break
        for i in range(len(img_name)):
            if img_name[len(img_name) - 1 - i] == '.':
                img_name = img_name[0:len(img_name) - 1 - i]
                break
        print(img_name)
        # wenjianjia
        # wjj = directory.split('/')
        # wj = wjj[-1]#wj是地区
        # print(wj)
        # wenjianjia
        my_file = Path(directory + '/' + img_name)
        if not my_file.exists():
            os.makedirs(my_file)

        # print(path)
        # print(my_file)
        path = str(my_file) + '\\' + img_name_all
        # print(path)
        copyfile(pr_path, path)  # 原图片备份,使用备份图片作为存储地址//1.4日修改

        # cv2.imwrite(path, images)
        worksheet1.write(1, 0, img_name)
        worksheet1.write(1, 1, path)
        worksheet1.write(1, 2, self.textEdit.toPlainText())
        print(self.textEdit.toPlainText())
        worksheet1.write(1, 3, 0)
        worksheet1.write(1, 5, str(2))
        worksheet1.write(1, 6, str(my_file))
        workbook.save(str(my_file) + '/' + img_name + '.xls')
        self.close()

    def get_path(self):
        return path
