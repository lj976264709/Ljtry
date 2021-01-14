import math
import time

import cv2
import xlrd  # 导入模块
from xlutils.copy import copy  # 导入copy模块
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QRadioButton, QButtonGroup, QCheckBox, QInputDialog
import matlab.engine
import CV
from Add_exp import Ui_add_exp_dialog

pretreat = {0: '无', 10: '植被提取', 23: '均值滤波3*3', 25: '均值滤波5*5', 27: '均值滤波7*7',
            33: '中值滤波3*3', 35: '中值滤波5*5', 37: '中值滤波7*7',
            43: '高斯滤波3*3', 45: '高斯滤波5*5', 47: '高斯滤波7*7'}
vis = []
names = []
algorithm = {0: '请选择', 1: 'CV算法'}

path = ""
img = ""
right_list = []
wrong_list = []
last_list = []
bianma_ = '预处理算法编码： '
b_code=''
yuchuli = []
roww=0

class Logic_add(QDialog, Ui_add_exp_dialog):

    def __init__(self, parent=None):
        super(Logic_add, self).__init__(parent)
        self.setupUi(self)
        self.Button_renew.clicked.connect(self.init_pretratment)  # 绑定预处理重置按
        self.init_algorithm()  # 初始化处理算法
        self.init_pretratment()


    def init_pretratment(self):
        yuchuli.clear()
        self.bianma.setText(bianma_)
        positions = [(i, j) for i in range(10) for j in range(4)]
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(0)
        tp = st.row(1)
        global names
        names = []
        for i in range(1, len(tp)):
            names.append(tp[i].value)
        font = QFont()
        font.setBold(True)  # 加粗
        font.setPointSize(16)
        for position, name in zip(positions, names):
            tp = QCheckBox(name)
            tp.stateChanged.connect(self.check_op)
            tp.setFont(font)
            self.gridLayout_list.addWidget(tp, *position)

    def check_op(self):
        global yuchuli
        tp = self.sender()
        if tp.checkState() == Qt.Checked:
            tx = tp.text()
            print('9' + tx)
            if tx[-1] == '.':
                text, ok = QInputDialog.getText(self, tx+'算法参数', "请输入预处理参数，多个以空格隔开：")
                if ok:
                    canshu = text.split()
                    txx = tx[:-1]
                    for i in canshu:
                        txx = txx + '_' + i
                    yuchuli.append(txx)
                else:
                    tp.setCheckState(Qt.Unchecked)
                    return
            else:
                yuchuli.append(tx)
        else:
            print(yuchuli)
            tx = tp.text()
            if tx[-1] == '.':
                tx = tx[:-1]

            for i in range(len(yuchuli)):
                if yuchuli[i].startswith(tx):
                    yuchuli.pop(i)
        global b_code
        b_code = ''
        for i in yuchuli:
            b_code = b_code + i + '+'
        b_code = b_code[:-1]
        self.bianma.setText(bianma_ + b_code)

    def init_algorithm(self):
        self.algorithm_select.clear()
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(0)
        tp = st.row(2)
        algorithm.clear()
        algorithm[0] = '无'
        for i in range(1, len(tp)):
            if len(tp[i].value) > 0:
                algorithm[i] = tp[i].value
        for k, v in algorithm.items():
            self.algorithm_select.addItem(v, k)
        self.para1.hide()
        self.para2.hide()
        self.para_type1.hide()
        self.para_type2.hide()

    @pyqtSlot(int)
    def on_algorithm_select_activated(self, index):
        tp = self.algorithm_select.itemText(index)
        if tp[-1] == '.':
            tp = tp[:-1]

        if tp == 'CV算法':
            self.para_type1.setText('迭代次数:')
            self.para_type2.setText('膨胀收缩系数:')
            self.para_type1.show()
            self.para_type2.show()
            self.para1.show()
            self.para2.show()

    def accept(self):  # 1’
        tp = self.do_pretreatment()
        print(img)
        a = self.para1.text()
        b = self.para2.text()
        print(a, b)

        # if self.algorithm_select.currentText() == 'CV算法':
        #     ans=CV.cv.get_cv(img, int(a), float(b))
        ans = CV.cv.get_cv('D:/shaoxing0.6m_gauss.tif', 5, 0.1)
        print('yes')
        self.ans_compare(ans)  # 目视和计算结果的对比
        print('yes')
        self.write_ans(ans)  # 把结果写入文件
        print('yes')
        self.close()

    def distance(self, pa, pb):
        return math.sqrt((pa[0] - pb[0]) * (pa[0] - pb[0]) + (pa[1] - pb[1]) * (pa[1] - pb[1]))

    def ans_compare(self, ans):
        xf = xlrd.open_workbook(path)
        ms = xf.sheet_by_index(0).cell_value(1, 4)
        if len(ms)==0:
            ms='[]'
        ms_list = eval(ms)
        ans_list = eval(str(ans))
        global right_list, wrong_list, last_list
        right_list.clear()
        wrong_list.clear()
        last_list.clear()
        vis_ans = [0] * len(ans_list)
        vis_ms = [0] * len(ms_list)
        for i in range(len(ms_list)):
            for j in range(len(ans_list)):
                if vis_ans[j] == 1:
                    continue
                if self.distance(ms_list[i], ans_list[j]) < 7.0:  # 这个距离到底多少合适???还需要商量
                    vis_ms[i] = 1
                    vis_ans[j] = 1
                    break

        for i in range(len(ms_list)):
            if vis_ms[i] == 1:
                right_list.append(ms_list[i])
            else:
                last_list.append(ms_list[i])
        for i in range(len(ans_list)):
            if vis_ans[i] == 0:
                wrong_list.append(ans_list[i])

    def write_ans(self, ans):
        print(ans)
        rb = xlrd.open_workbook(path)
        row = rb.sheet_by_index(1).nrows
        wb = copy(rb)
        wsheet = wb.get_sheet(1)
        wsheet.write(row, 0, str(row))
        wsheet.write(row, 1, str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        wsheet.write(row, 2, b_code)
        wsheet.write(row, 3, self.algorithm_select.currentText() + '_' + self.para1.text() + '_' + self.para2.text())
        wsheet.write(row, 4, str(len(right_list) + len(wrong_list)))
        wsheet.write(row, 5, str(len(right_list)))
        wsheet.write(row, 6, str(len(wrong_list)))
        wsheet.write(row, 7, str(len(last_list)))

        wsheet.write(row, 8, str(len(right_list) / (len(right_list) + len(wrong_list))))
        wsheet.write(row, 9, str(len(wrong_list) / (len(right_list) + len(wrong_list))))
        wsheet.write(row, 10, str(len(last_list)/len(ans)))
        wsheet.write(row, 11, str(len(right_list) / (len(right_list) + len(wrong_list)+len(last_list))))

        wsheet.write(row, 12, str(ans))
        wsheet.write(row, 13, str(right_list))
        wsheet.write(row, 14, str(wrong_list))
        wsheet.write(row, 15, str(last_list))
        wb.save(path)
        global roww
        roww=row

    def set_url(self, img_, f_url):
        global img, path
        img = img_
        path = f_url

    def get_path(self):
        return path

    def do_pretreatment(self):
        xf=xlrd.open_workbook(path)
        st=xf.sheet_by_index(0)
        pre_url=st.cell_value(1,5)+'\\'+st.cell_value(1,0)+'_'+(str(roww+1))+'_pre.tif'
        images = cv2.imread(img)
        cv2.imwrite(pre_url, images)
