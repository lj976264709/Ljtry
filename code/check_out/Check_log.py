from shutil import copyfile

from PyQt5.QtWidgets import QDialog
import xlrd

import image_mark
from Check_result import Ui_Dialog_Check
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

right_list = []
wrong_list = []
last_list = []
img_url = ''


class Check_logic(QDialog, Ui_Dialog_Check):
    def __init__(self, parent=None):
        super(Check_logic, self).__init__(parent)

    def inti_infor(self, a, b, c, url, filepath):
        self.setupUi(self)
        rb = xlrd.open_workbook(filepath)
        st = rb.sheet_by_index(0)
        result_url = st.cell_value(1, 6) + '\\' + st.cell_value(1, 0) + '_Compared.jpg'
        copyfile('D:/66.jpg', result_url)

        self.description.setText(" ○ 为正确标记，╳ 为错误标记，■ 为漏判：")
        global right_list, wrong_list, last_list, img_url
        right_list = eval(a)
        wrong_list = eval(b)
        last_list = eval(c)
        img_url = url
        image_mark.Image_mark.mark_function_2(right_list, wrong_list, last_list, img_url)
        print(img_url)
        tp = QPixmap('D:/66.jpg')
        if tp.height() * 651 / tp.width() > 1021:
            self.img__.setPixmap(tp.scaled(self.img__.width(), tp.height() * self.img__.width() / tp.width()))
        else:
            self.img__.setPixmap(tp.scaled(tp.width() * self.img__.height() / tp.height(), self.img__.height()))
