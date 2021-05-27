import math
import os
import time

import cv2
import xlrd  # 导入模块
import xlwt
from xlutils.copy import copy  # 导入copy模块
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QRadioButton, QButtonGroup, QCheckBox, QInputDialog
import matlab.engine
import CV
from Add_exp import Ui_add_exp_dialog

vis = []
names = []
algorithm = {}
num_cs = {}
name_cs = {}
path = ""
img = ""
img_after_pretreat = ""
right_list = []
wrong_list = []
last_list = []
bianma_ = '预处理算法编码： '
b_code = ''
yuchuli = []
roww = 0


class Logic_add(QDialog, Ui_add_exp_dialog):

    def __init__(self, parent=None):
        super(Logic_add, self).__init__(parent)
        self.setupUi(self)
        self.Button_renew.clicked.connect(self.init_pretratment)  # 绑定预处理重置按
        self.init_algorithm()  # 初始化处理算法
        self.init_pretratment()

    def init_pretratment(self):
        yuchuli.clear()
        num_cs.clear()
        self.bianma.setText(bianma_)
        positions = [(i, j) for i in range(10) for j in range(4)]
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(1)
        global names
        names = []
        for i in range(1, st.nrows):
            names.append(st.cell_value(i, 2))
            num_cs[st.cell_value(i, 2)] = int(st.cell_value(i, 3))

        font = QFont()
        font.setBold(True)  # 加粗
        font.setPointSize(16)
        for position, name in zip(positions, names):
            tp = QCheckBox(name)
            tp.stateChanged.connect(self.check_op)
            tp.setFont(font)
            self.gridLayout_list.addWidget(tp, *position)
        print('ok')

    def check_op(self):
        global yuchuli
        tp = self.sender()
        if tp.checkState() == Qt.Checked:
            tx = tp.text()
            print('9' + tx)
            # if tx[-1] == '.':
            if num_cs[tx] > 0:
                text, ok = QInputDialog.getText(self, tx + '算法参数', "请输入预处理参数，多个以空格隔开：")
                if ok:
                    canshu = text.split()
                    for i in canshu:
                        tx = tx + '_' + i
                    yuchuli.append(tx)
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
        name_cs.clear()
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(2)

        algorithm.clear()
        algorithm[0] = '无'
        for i in range(1, st.nrows):
            if len(st.cell_value(i, 2)) > 0:
                algorithm[i] = st.cell_value(i, 2)
                csmc = []
                for j in range(int(st.cell_value(i, 3))):
                    csmc.append(st.cell_value(i, 4 + j))
                name_cs[st.cell_value(i, 2)] = csmc
        print(name_cs)
        for k, v in algorithm.items():
            self.algorithm_select.addItem(v, k)
        self.para1.hide()
        self.para2.hide()
        self.para3.hide()
        self.para_type3.hide()
        self.label_5.hide()
        self.algorithm_select_2.hide()
        self.label_6.hide()
        self.algorithm_select_3.hide()
        self.para_type1.hide()
        self.para_type2.hide()

    @pyqtSlot(int)
    def on_algorithm_select_activated(self, index):
        tp = self.algorithm_select.itemText(index)
        if tp == '无':
            return
        if len(name_cs[tp]) == 1:
            self.para_type1.setText(name_cs[tp][0])
            self.para_type1.show()
            self.para1.show()
            self.para2.hide()
            self.para_type2.hide()
            self.para3.hide()
            self.para_type3.hide()
        elif len(name_cs[tp]) == 2:
            self.para_type1.setText(name_cs[tp][0])
            self.para1.show()
            self.para_type1.show()
            self.para_type2.setText(name_cs[tp][1])
            self.para2.show()
            self.para_type2.show()
            self.para3.hide()
            self.para_type3.hide()
        elif len(name_cs[tp]) == 3:
            self.para_type1.setText(name_cs[tp][0])
            self.para1.show()
            self.para_type1.show()
            self.para_type2.setText(name_cs[tp][1])
            self.para2.show()
            self.para_type2.show()
            self.para_type3.setText(name_cs[tp][2])
            self.para3.show()
            self.para_type3.show()

        if self.algorithm_select.currentText() == '模板匹配':
            self.label_5.show()
            self.label_6.show()
            self.algorithm_select_2.clear()
            for tp in os.walk('D:\Tree\Template'):
                for i in range(len(tp[1])):
                    self.algorithm_select_2.addItem(tp[1][i], i)
                break
            self.algorithm_select_2.show()

            self.algorithm_select_3.clear()
            methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                       'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
            for i in range(len(methods)):
                self.algorithm_select_3.addItem(methods[i], i)
            self.algorithm_select_3.show()

        else:
            self.label_5.hide()
            self.label_6.hide()
            self.algorithm_select_3.hide()
            self.algorithm_select_2.hide()

    def accept(self):  # 1’
        tp = self.do_pretreatment()
        print(img)
        a = self.para1.text()
        b = self.para2.text()
        c = self.para3.text()
        print(a, b)
        if self.algorithm_select.currentText() == '标记分水岭':
            ans = CV.cv.get_fenshuiling(img_after_pretreat, float(a))  # 1.0
        elif self.algorithm_select.currentText() == '梯度分水岭':
            ans = CV.cv.get_fenshuiling_g(img_after_pretreat, float(a), int(b))  # 1.0, 5
        elif self.algorithm_select.currentText() == 'CV模型':
            ans = CV.cv.get_cv(img_after_pretreat, float(a), int(b), float(c))
        elif self.algorithm_select.currentText() == '模板匹配':
            ans = CV.cv.get_march(img_after_pretreat, float(a), float(b),
                                  'D:\Tree\Template\\' + self.algorithm_select_2.currentText(),
                                  self.algorithm_select_3.currentText())
        elif self.algorithm_select.currentText() == '局部最大值':
            ans = CV.cv.get_maximum(img_after_pretreat, int(a), int(b))

        # print(ans)
        print('yes')
        self.ans_compare(ans)  # 目视和计算结果的对比
        print('yes')
        self.write_ans(ans)  # 把结果写入文件
        print('yes')
        self.close()

    def distance(self, pa, pb):
        return math.sqrt((pa[0] - pb[0]) * (pa[0] - pb[0]) + (pa[1] - pb[1]) * (pa[1] - pb[1]))

    def ans_compare(self, ans):
        default_distance = 150
        if self.algorithm_select.currentText() == '模板匹配':
            default_distance = float(self.para2.text()) * 1
        xf = xlrd.open_workbook(path)
        ms = xf.sheet_by_index(0).cell_value(1, 4)
        if len(ms) == 0:
            ms = '[]'
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
                if self.distance(ms_list[i], ans_list[j]) < math.sqrt(default_distance):  # 这个距离到底多少合适???还需要商量
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
        str_id = ''
        if self.algorithm_select.currentText() == '模板匹配':
            str_id = self.algorithm_select.currentText() + '_' + self.algorithm_select_2.currentText() + '_' + self.algorithm_select_3.currentText() + '_' + self.para1.text() + '_' + self.para2.text()
        elif len(self.para3.text()) > 0:
            str_id = self.algorithm_select.currentText() + '_' + self.para1.text() + '_' + self.para2.text() + '_' + self.para3.text()
        elif len(self.para2.text()) > 0:
            str_id = self.algorithm_select.currentText() + '_' + self.para1.text() + '_' + self.para2.text()
        else:
            str_id = self.algorithm_select.currentText() + '_' + self.para1.text()
        wsheet.write(row, 3, str(str_id))
        wsheet.write(row, 4, str(len(right_list) + len(wrong_list)))
        wsheet.write(row, 5, str(len(right_list)))
        wsheet.write(row, 6, str(len(wrong_list)))
        wsheet.write(row, 7, str(len(last_list)))

        wsheet.write(row, 8, str(len(right_list) / (len(right_list) + len(wrong_list))))
        wsheet.write(row, 9, str(len(wrong_list) / (len(right_list) + len(wrong_list))))
        wsheet.write(row, 10, str(len(last_list) / len(ans)))
        wsheet.write(row, 11, str(len(right_list) / (len(right_list) + len(wrong_list) + len(last_list))))

        wsheet.write(row, 12, str(ans))
        wsheet.write(row, 13, str(right_list))
        wsheet.write(row, 14, str(wrong_list))
        wsheet.write(row, 15, str(last_list))
        wb.save(path)
        global roww
        roww = row

        path_ = path[:-4] + '-' + str(str_id) + '@' + b_code + '.xls'
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet1 = workbook.add_sheet('目视')
        tp = right_list.copy()
        tp.extend(last_list)
        worksheet1.write(0, 0, 'X')
        worksheet1.write(0, 1, 'Y')
        for i in range(len(tp)):
            worksheet1.write(i + 1, 0, tp[i][0])
            worksheet1.write(i + 1, 1, tp[i][1])
        worksheet2 = workbook.add_sheet('机视')
        tp = right_list.copy()
        tp.extend(wrong_list)
        worksheet2.write(0, 0, 'X')
        worksheet2.write(0, 1, 'Y')
        for i in range(len(tp)):
            worksheet2.write(i + 1, 0, tp[i][0])
            worksheet2.write(i + 1, 1, tp[i][1])
        worksheet3 = workbook.add_sheet('正确')
        worksheet3.write(0, 0, 'X')
        worksheet3.write(0, 1, 'Y')
        for i in range(len(right_list)):
            worksheet3.write(i + 1, 0, right_list[i][0])
            worksheet3.write(i + 1, 1, right_list[i][1])
        worksheet4 = workbook.add_sheet('错判')
        worksheet4.write(0, 0, 'X')
        worksheet4.write(0, 1, 'Y')
        for i in range(len(wrong_list)):
            worksheet4.write(i + 1, 0, wrong_list[i][0])
            worksheet4.write(i + 1, 1, wrong_list[i][1])
        worksheet5 = workbook.add_sheet('漏判')
        worksheet5.write(0, 0, 'X')
        worksheet5.write(0, 1, 'Y')
        for i in range(len(last_list)):
            worksheet5.write(i + 1, 0, last_list[i][0])
            worksheet5.write(i + 1, 1, last_list[i][1])
        workbook.save(path_)

    def set_url(self, img_, f_url):
        global img, path
        img = img_
        path = f_url

    def get_path(self):
        return path

    def do_pretreatment(self):
        xf = xlrd.open_workbook(path)
        st = xf.sheet_by_index(0)
        roww = xf.sheet_by_index(1).nrows
        pre_url = st.cell_value(1, 6) + '\\' + st.cell_value(1, 0) + '_' + (str(roww)) + '_pre.tif'
        global img_after_pretreat
        img_after_pretreat = pre_url
        images = cv2.imread(img)
        flag = False
        for i in range(len(yuchuli)):
            tp = yuchuli[i].split('_')
            if tp[0] == '高斯滤波':
                images = cv2.GaussianBlur(images, (int(tp[1]), int(tp[1])), 0)
                # images =
                images = cv2.cvtColor(images, cv2.COLOR_RGB2GRAY)
            elif tp[0] == '中值滤波':
                images = cv2.medianBlur(images, int(tp[1]))
            elif tp[0] == '均值滤波':
                images = cv2.blur(images, (int(tp[1]), int(tp[1])))
            elif tp[0] == 'GLI植被提取':
                flag = True
        cv2.imwrite(pre_url, images)
        if self.algorithm_select.currentText() == 'CV模型':
            flag = True
        if flag:
            CV.cv.get_CLI(pre_url, pre_url)
