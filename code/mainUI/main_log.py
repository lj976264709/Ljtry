from PyQt5.QtGui import QImage, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QItemDelegate, QPushButton, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets

import xlwt
import xlrd  # 导入模块
from xlutils.copy import copy  # 导入copy模块
from Add_logic import Logic_add
from Check_log import Check_logic
from Create_exp import Ui_Create_Dialog
from Create_logic import Logic_create
from Visual_log import Visual_logic
from config_log import logic_config
from mainUI import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

filepath = ""
img = ""
row_list = []


class Logic_mian(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Logic_mian, self).__init__(parent)
        self.setupUi(self)
        self.Create_experiment.triggered.connect(self.jump_to_create)  # 给’创建实验按键‘绑定函数1‘
        self.Open_experiment.triggered.connect(self.jump_to_open)  # 给’打开实验‘绑定函数1‘
        self.expBT.clicked.connect(self.jump_to_add)  #
        self.mushiBT.clicked.connect(self.jump_to_mushi)  #
        self.RN.clicked.connect(self.get_table)
        self.Config.triggered.connect(self.jump_to_config)
        self.get_menu()  # 获得实验按钮

    def get_menu(self):
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(0)
        tp = st.row(0)
        for i in range(1, len(tp)):
            if len(tp[i].value) > 0:
                self.menu_2.addAction(QAction(tp[i].value, self))
        # 单击任何Qmenu对象，都会发射信号，绑定槽函数
        self.menu_2.triggered[QAction].connect(self.menu_trigger)

    def menu_trigger(self, wa):
        if wa.text() == '目视定位':
            self.jump_to_mushi()

    def jump_to_config(self):
        log = logic_config()
        log.show()
        log.exec_()

    def jump_to_mushi(self):
        if len(img) != 0:
            print(img)
            log = Visual_logic()
            log.setFileURL(filepath)
            log.getImgURL(img)  # 其实应该是set url
            log.show()
            log.exec_()

    def jump_to_add(self):
        log = Logic_add()
        log.set_url(img, filepath)  # 把图片和文件地址传过去
        log.show()
        log.exec_()

    def jump_to_create(self):  # 1’
        log = Logic_create()
        log.show()
        log.exec_()
        print(log.get_path())

    def jump_to_open(self):
        global filepath, img
        path, _ = QFileDialog.getOpenFileName(None, '选择文件', "D:/Tree/exp", "xls Files(*.xls)")  # 打开资源管理器，path绝对路径
        filepath = path
        if path == '':
            return
        # print(filepath)
        workbook = xlrd.open_workbook(path)
        sheet1 = workbook.sheet_by_index(0)
        sheet2 = workbook.sheet_by_index(1)
        img = sheet1.row(1)[1].value
        print(img)
        self.lineEdit.setText(sheet1.row(1)[0].value)
        self.textEdit.setText(sheet1.row(1)[2].value)
        ms = sheet1.row(1)[3].value

        if ms == '0':
            self.isMushi.setText("目视未完成")
        else:
            self.isMushi.setText("目视已完成")
        self.get_table()

    def get_table(self):
        self.model = QStandardItemModel(12, 12)
        titles = ['创建时间', '预处理', '单木定位算法', '识别树木数量', '正确识别数量', '错判单木数目', '漏判单木数目', '准确率', '漏判率', '误判率', '匹配率',
                  ' ']
        self.model.setHorizontalHeaderLabels(titles)
        # self.model.setItem(1,0,QStandardItem("hh"))

        xf = xlrd.open_workbook(filepath)
        st = xf.sheet_by_index(1)
        rows = st.nrows
        print("filepath")
        global row_list
        row_list = []
        r_rows = 0
        for i in range(1, rows):
            if st.cell_value(i, 0) != '*':
                for j in range(1, 12):
                    if j > 7:
                        tp = float(st.cell_value(i, j)) * 100
                        self.model.setItem(r_rows, j - 1, QStandardItem(str(round(tp, 3))))
                    else:
                        self.model.setItem(r_rows, j - 1, QStandardItem(st.cell_value(i, j)))
                row_list.append(i)
                r_rows = r_rows + 1

        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setColumnWidth(1,200)
        for i in range(0, r_rows):
            self.tableView.setIndexWidget(self.model.index(i, 11), self.buttonForRow())

    def buttonForRow(self):  # 按钮！！！！！费老劲了
        widget = QtWidgets.QWidget()
        # 查看
        self.updateBtn = QtWidgets.QPushButton('查看')
        self.updateBtn.setStyleSheet(''' text-align : center;
                                          background-color : LIMEGREEN;
                                          height : 30px;
                                          border-style: outset;
                                          font : 13px  ''')
        self.updateBtn.clicked.connect(self.UpButton)
        # 删除
        self.deleteBtn = QtWidgets.QPushButton('删除')
        self.deleteBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')
        self.deleteBtn.clicked.connect(self.DeleteButton)

        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.updateBtn)
        hLayout.addWidget(self.deleteBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def UpButton(self):
        button = self.sender()
        row = self.tableView.indexAt(button.parent().pos()).row()  # 确定位置的时候这里是关键
        xf = xlrd.open_workbook(filepath)
        st = xf.sheet_by_index(1)
        rt_ = st.cell_value(row_list[row], 13)
        wr_ = st.cell_value(row_list[row], 14)
        la_ = st.cell_value(row_list[row], 15)
        log = Check_logic()
        log.inti_infor(rt_, wr_, la_, img)  # 传值
        log.show()
        log.exec_()

    def DeleteButton(self):
        button = self.sender()
        row = self.tableView.indexAt(button.parent().pos()).row()  # 确定位置的时候这里是关键

        rb = xlrd.open_workbook(filepath)
        wb = copy(rb)
        wsheet = wb.get_sheet(1)
        print(row_list[row])
        wsheet.write(row_list[row], 0, '*')
        wb.save(filepath)
        print(row)
        self.get_table()
        # button = self.sender()
        # if button:
        #     # 确定位置的时候这里是关键
        #     row = self.tableView.indexAt(button.parent().pos()).row()
        #     # self.tableWidget.removeRow(row)
        #     print(row)
