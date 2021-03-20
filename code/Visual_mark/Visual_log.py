import sys

import os
import sys
import time
from shutil import copyfile

import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint
from PIL import Image
import xlrd                           #导入模块
from xlutils.copy import copy        #导入copy模块
import image_mark
from Visual_mark import Ui_Visual
import ast
img_url = 'D:/23.tif'
img_hight = 1000  # 图片窗口大小
img_width = 400  # 图片窗口大小
k = 1  # 放缩比例
image_h = 0  # 图片真实大小
image_w = 0  # 图片真实大小
rate = 1  # 放大缩小比例
count_num = 0
node_list = []
filepath = ""

class Visual_logic(QDialog, Ui_Visual):
    def __init__(self, parent=None):
        super(Visual_logic, self).__init__(parent)
        # self.setupUi(self)
        # self.img_widget = ImageWithMouseControl(self)  # 设定图片放大缩小类
        # self.img_widget.setObjectName("img_widget")
        # self.img_Pretreat()  # 图片预处理
        # self.resize(img_hight + 120, img_width + 150)  # 重新设置窗口大小
        # self.img_widget.setGeometry(60, 100, img_hight, img_width)  # 图片大小
        # self.Revoke.clicked.connect(self.revoke)  # 撤回上一个标记
        # self.Revoke.setShortcut('Ctrl+Z')  # 绑定快捷键
        # global node_list, count_num  # 初始化
        # node_list.clear()
        # count_num = 0



    def getImgURL(self, url): #入口
        global img_url
        img_url = url
        # 初始化界面
        self.setupUi(self)
        self.count.setText('0')
        self.img_widget = ImageWithMouseControl(self)  # 设定图片放大缩小类
        self.img_widget.setObjectName("img_widget")
        self.img_Pretreat()  # 图片预处理
        self.resize(img_hight + 120, img_width + 150)  # 重新设置窗口大小
        self.img_widget.setGeometry(60, 100, img_hight, img_width)  # 图片大小
        self.Revoke.clicked.connect(self.revoke)  # 撤回上一个标记
        self.Revoke.setShortcut('Ctrl+Z')  # 绑定快捷键
        self.save.clicked.connect(self.save_node) # 保存现在标记的点位
        self.finish.clicked.connect(self.finish_mark)
        self.node_inti() # 初始化点位
        # 初始化界面

    def node_inti(self):

        global node_list, count_num  # 初始化
        node_list.clear()  # node_list还得读入一下文件
        count_num = 0
        xf=xlrd.open_workbook(filepath)
        st=xf.sheet_by_index(0)
        print("sss")
        tp=st.cell_value(1,4)
        print("ss"+tp)
        if len(tp)>0:
            node_list=eval(tp)
        print("sss")
        count_num=len(node_list)
        self.count.setText(str(count_num))
        image_mark.Image_mark.mark_function(node_list, img_url)  # 文件写入
        self.img_widget.get_pre_img()


    def finish_mark(self):

        rb = xlrd.open_workbook(filepath)
        st=rb.sheet_by_index(0)
        result_url = st.cell_value(1, 6) + '\\' + st.cell_value(1, 0) + '_mushi.jpg'
        wb = copy(rb)
        wsheet = wb.get_sheet(0)
        wsheet.write(1, 3, count_num)
        ss = str(node_list)
        wsheet.write(1, 4, ss)
        wb.save(filepath)

        copyfile('D:/23.jpg', result_url)
        self.close()

    def setFileURL(self,fileurl):
        global filepath
        filepath = fileurl

    def save_node(self):
        self.count.setText(str(count_num))# 更新计数。。
        rb= xlrd.open_workbook(filepath)
        wb=copy(rb)
        wsheet=wb.get_sheet(0)
        ss=str(node_list)
        wsheet.write(1,4,ss)
        wb.save(filepath)

    def revoke(self):
        ImageWithMouseControl.revoke_node(self.img_widget)
        self.renew_count()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            self.renew_count()

    def renew_count(self):
        self.count.setText(str(count_num))  # 更新计数。。

    def img_Pretreat(self):  # 图片预处理函数
        im = Image.open(img_url)
        global image_h, image_w, k, img_width, type_y, type_x
        image_h = im.size[0]
        image_w = im.size[1]
        print(image_h, image_w)
        k = 1000 / image_h
        img_hight = image_h * k
        img_width = image_w * k
        # type_y = img_hight / 200
        # type_x = img_width / 200


class ImageWithMouseControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.img = QPixmap(img_url)
        self.scaled_img = self.img.scaled(self.size())
        self.point = QPoint(0, 0)

    def paintEvent(self, e):
        '''
        绘图
        :param e:
        :return:
        '''
        painter = QPainter()
        painter.begin(self)
        self.draw_img(painter)
        painter.end()

    def draw_img(self, painter):
        painter.drawPixmap(self.point, self.scaled_img)

    def mouseMoveEvent(self, e):  # 重写移动事件
        if self.left_click:
            self._endPos = e.pos() - self._startPos
            self.point = self.point + self._endPos
            self._startPos = e.pos()
            self.repaint()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.left_click = True
            self._startPos = e.pos()

    def mouseReleaseEvent(self, e):
        global count_num
        if e.button() == Qt.LeftButton:
            self.left_click = False
        elif e.button() == Qt.RightButton:  # 右键标记
            self.mark_node(e.x(), e.y())
            self.img = QPixmap('D:/23.jpg')
            self.scaled_img = self.img.scaled(img_hight * rate, img_width * rate)
            self.repaint()
            count_num = count_num + 1

    def get_pre_img(self):
        self.img = QPixmap('D:/23.jpg')
        self.scaled_img = self.img.scaled(img_hight * rate, img_width * rate)
        self.repaint()

    def revoke_node(self):
        global node_list, count_num
        if len(node_list) != 0:
            node_list.pop()
        image_mark.Image_mark.mark_function(node_list, img_url)
        self.img = QPixmap('D:/23.jpg')
        self.scaled_img = self.img.scaled(img_hight * rate, img_width * rate)
        self.repaint()
        count_num = count_num - 1

    def wheelEvent(self, e):
        global rate
        if e.angleDelta().y() > 0:
            # 放大图片
            rate = rate + 0.05
            self.scaled_img = self.img.scaled(img_hight * rate, img_width * rate)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() / 0.99)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() / 0.99)
            self.point = QPoint(new_w, new_h)
            self.repaint()
        elif e.angleDelta().y() < 0:
            # 缩小图片
            rate = rate - 0.05
            self.scaled_img = self.img.scaled(img_hight * rate, img_width * rate)
            new_w = e.x() - (self.scaled_img.width() * (e.x() - self.point.x())) / (self.scaled_img.width() * 0.99)
            new_h = e.y() - (self.scaled_img.height() * (e.y() - self.point.y())) / (self.scaled_img.height() * 0.99)
            self.point = QPoint(new_w, new_h)
            self.repaint()

    def resizeEvent(self, e):
        if self.parent is not None:
            self.scaled_img = self.img.scaled(self.size())
            self.point = QPoint(0, 0)
            self.update()


    def mark_node(self, x, y):  # 标点
        global node_list
        tx = (x - self.point.x()) / (rate * k)
        ty = (y - self.point.y()) / (rate * k)
        # print(tx,ty)
        node_list.append((tx, ty))
        image_mark.Image_mark.mark_function(node_list, img_url)  # 文件写入
