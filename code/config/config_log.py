import xlrd  # 导入模块
from xlutils.copy import copy  # 导入copy模块
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage, QFont, QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QDialog, QInputDialog, QTreeWidgetItem, QMessageBox

from Config import Ui_Config_Dialog

list_1 = {}
list_2 = []
list_3 = []
list1tp = []
id2string = {}

class logic_config(QDialog, Ui_Config_Dialog):
    def __init__(self, parent=None):
        super(logic_config, self).__init__(parent)
        self.setupUi(self)
        self.init()
        self.pB_delete1.clicked.connect(self.delete1)
        self.pB_delete2.clicked.connect(self.delete2)
        self.pB_delete3.clicked.connect(self.delete3)
        self.pB_add1.clicked.connect(self.add1)
        self.pB_add2.clicked.connect(self.add2)
        self.pB_add3.clicked.connect(self.add3)

    def init(self):
        xf = xlrd.open_workbook('D:/Tree/config.xls')
        st = xf.sheet_by_index(0)
        global list_1, list_2, list_3
        list_1.clear()
        list_2.clear()
        list_3.clear()
        # for i in range(1, len(st.row(0))):
        #     if len(st.row(0)[i].value) > 0:
        #         list_1.append(st.row(0)[i].value)
        global list1tp , id2string
        list1tp.clear()
        id2string.clear()
        for i in range(1, st.nrows):
            for j in range(len(st.row(i))):
                if len(st.row(i)[j].value) > 0:
                    list1tp.append(st.row(i)[j].value)
        list1tp.sort()

        list_1['root'] = []
        for tp in list1tp:
            id_string = tp.split('-')
            id2string[id_string[0]] = id_string[1]
            if len(id_string[0]) == 1:
                list_1['root'].append(id_string[1])
                list_1[id_string[1]] = []
            else:
                fa = id_string[0][:-2]
                list_1[id2string[fa]].append(id_string[1])
                list_1[id_string[1]] = []
        # print(list_1)

        #####
        st = xf.sheet_by_index(1)
        for i in range(1, st.nrows):
            if len(st.row(i)[2].value) > 0:
                list_2.append(st.row(i)[2].value)

        st = xf.sheet_by_index(2)
        for i in range(1, st.nrows):
            if len(st.row(i)[2].value) > 0:
                list_3.append(st.row(i)[2].value)
        # slm1 = QStringListModel()
        # slm1.setStringList(list_1)
        slm2 = QStringListModel()
        slm2.setStringList(list_2)
        slm3 = QStringListModel()
        slm3.setStringList(list_3)
        font = QFont()
        font.setBold(True)  # 加粗
        font.setPointSize(16)
        #
        self.treeView.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        self.get_menu(rootNode, 'root')
        self.treeView.setModel(treeModel)
        self.treeView.expandAll()
        #
        self.listView_2.setFont(font)
        self.listView_2.setModel(slm2)
        self.listView_3.setFont(font)
        self.listView_3.setModel(slm3)

    def get_menu(self, root, str):
        fsize = 14
        bold = False
        if str == 'root':
            bold = True
            fsize = 16
        for ss in list_1[str]:
            mu = StandardItem(ss, fsize, bold)
            self.get_menu(mu, ss)
            root.appendRow(mu)
        # print(list_1)

    def delet_menu(self, root, str):
        global list_1, list1tp
        print(list_1)
        for ss in list_1[root]:
            if ss == str:
                list_1[root].remove(str)
            else:
                self.delet_menu(ss, str)
        for ss in list1tp:
            if ss.endswith(str):
                list1tp.remove(ss)
                break

    def write_menu(self):
        rb = xlrd.open_workbook('D:/Tree/config.xls')
        wb = copy(rb)
        wsheet = wb.get_sheet(0)
        pos = [0] * 10
        for ss in list1tp:
            wsheet.write(int(ss[0]), pos[int(ss[0])], ss)
            pos[int(ss[0])] = pos[int(ss[0])] + 1
        for i in range(10):
            if pos[i] != 0:
                wsheet.write(i, pos[i], '')
        wb.save('D:/Tree/config.xls')

    def delete1(self):
        text = self.treeView.selectedIndexes()[0].data()
        print(text)
        self.delet_menu('root', text)
        self.treeView.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        self.get_menu(rootNode, 'root')
        self.treeView.setModel(treeModel)
        self.treeView.expandAll()
        self.write_menu()

        # slm1 = QStringListModel()
        # slm1.setStringList(list_1)
        # self.listView.setModel(slm1)
        # self.file_delete(0, index + 1)

    def delete2(self):
        index = self.listView_2.selectedIndexes()[0].row()
        print(self.listView_2.selectedIndexes()[0].row())
        global list_2
        list_2.pop(index)
        slm2 = QStringListModel()
        slm2.setStringList(list_2)
        self.listView_2.setModel(slm2)
        self.file_delete(1, index + 1)

    def delete3(self):
        index = self.listView_3.selectedIndexes()[0].row()
        print(self.listView_3.selectedIndexes()[0].row())
        global list_3
        list_3.pop(index)
        slm3 = QStringListModel()
        slm3.setStringList(list_3)
        self.listView_3.setModel(slm3)
        self.file_delete(2, index + 1)

    def add1(self):
        text, ok = QInputDialog.getText(self, "菜单添加", "请输入：父目录节点-添加菜单名称")
        if ok:
            print(text)
        else:
            return
        global list_1, list1tp
        ss = text.split('-')
        try:
            list_1[ss[0]].append(ss[1])
            list_1[ss[1]] = []
        except:
            reply = QMessageBox.warning(self, '警告', '父节点不存在',
                                        QMessageBox.Yes)
        print(id2string)
        for key, value in id2string.items():
            if value==ss[0]:
                fakey=key
                break
        mxid=1
        for key in id2string.keys():
            if key!=fakey and key.startswith(fakey):
                mxid=max(mxid,int(key[len(fakey)+1]))
        print(fakey+'.'+str(mxid+1)+'-'+ss[1])
        list1tp.append(fakey+'.'+str(mxid+1)+'-'+ss[1])
        self.treeView.setHeaderHidden(True)
        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        self.get_menu(rootNode, 'root')
        self.treeView.setModel(treeModel)
        self.treeView.expandAll()
        self.write_menu()


    def add2(self):
        text, ok = QInputDialog.getText(self, "算法输入", "请输入算法名称")
        if ok:
            # item, okk = QInputDialog.getItem(self, "该算法是否需要参数", "该算法是否需要参数", ['否', '是'], 0, False)
            num_cs, okk = QInputDialog.getText(self, "算法输入", text + "所需参数个数")
            if not okk:
                return
        else:
            return
        global list_2
        list_2.append(text)
        slm2 = QStringListModel()
        slm2.setStringList(list_2)
        self.listView_2.setModel(slm2)
        self.file_write(1, len(list_2), text, num_cs)

    def add3(self):
        text, ok = QInputDialog.getText(self, "算法输入", "请输入算法名称")
        if ok:
            # item, okk = QInputDialog.getItem(self, "该算法是否需要参数", "该算法是否需要参数", ['否', '是'], 0, False)
            num_cs, okk = QInputDialog.getText(self, "算法输入", text + "所需参数个数")
            if not okk:
                return
        else:
            return
        global list_3
        list_3.append(text)
        slm3 = QStringListModel()
        slm3.setStringList(list_3)
        self.listView_3.setModel(slm3)
        self.file_write(2, len(list_3), text, num_cs)

    def file_write(self, x, y, text, num_cs):
        if x == 0:
            rb = xlrd.open_workbook('D:/Tree/config.xls')
            wb = copy(rb)
            wsheet = wb.get_sheet(0)
            wsheet.write(x, y, text)
            wb.save('D:/Tree/config.xls')
            return

        rb = xlrd.open_workbook('D:/Tree/config.xls')
        wb = copy(rb)
        wsheet = wb.get_sheet(x)
        wsheet.write(y, 0, y)
        wsheet.write(y, 2, text)
        wsheet.write(y, 3, int(num_cs))
        wb.save('D:/Tree/config.xls')

    def file_delete(self, x, y):
        if x == 0:
            print(x, y)
            rb = xlrd.open_workbook('D:/Tree/config.xls')
            tp = rb.sheet_by_index(0).row(x)
            wb = copy(rb)
            wsheet = wb.get_sheet(0)
            print("ss")
            for i in range(y, len(tp) - 1):
                wsheet.write(x, i, tp[i + 1].value)
            wsheet.write(x, len(tp) - 1, '')
            # wsheet.delete(x, len(tp) - 1)
            wb.save('D:/Tree/config.xls')
            return
        rb = xlrd.open_workbook('D:/Tree/config.xls')
        tp = rb.sheet_by_index(x)
        wb = copy(rb)
        wsheet = wb.get_sheet(x)
        print("ss")
        for i in range(y, tp.nrows - 1):
            for j in range(len(tp.row(i + 1))):
                wsheet.write(i, j, tp.cell_value(i + 1, j))
        for j in range(len(tp.row(tp.nrows - 1))):
            wsheet.write(tp.nrows - 1, j, '')
        wb.save('D:/Tree/config.xls')


class StandardItem(QStandardItem):
    def __init__(self, txt='', font_size=12, set_bold=False, color=QColor(0, 0, 0)):
        super().__init__()
        fnt = QFont('Open Sans', font_size)
        fnt.setBold(set_bold)
        self.setEditable(False)
        self.setForeground(color)
        self.setFont(fnt)
        self.setText(txt)
