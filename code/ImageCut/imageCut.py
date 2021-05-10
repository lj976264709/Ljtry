from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QPushButton, QSpacerItem, QSizePolicy, QFileDialog, \
    QMessageBox

try:
    from graphics import GraphicsView, GraphicsPixmapItem
except:
    from graphics import GraphicsView, GraphicsPixmapItem


class Form(QDialog):
    def __init__(self):
        super(Form, self).__init__()
        self.resize(1024, 768)

        self.picture = r' '
        self.init_ui()
        # 视图背景颜色
        self.graphicsView.setBackgroundBrush(QColor(28, 31, 34))
        self.graphicsView.save_signal.connect(self.pushButton_save.setEnabled)
        self.pushButton_cut.clicked.connect(self.pushButton_cut_clicked)
        self.pushButton_save.clicked.connect(self.pushButton_save_clicked)
        self.pushButton_open.clicked.connect(self.pushButton_open_clicked)
        # image_item = GraphicsPolygonItem()
        # image_item.setFlag(QGraphicsItem.ItemIsMovable)
        # self.scene.addItem(image_item)

    def init_ui(self):
        self.setWindowTitle("模板采取")
        self.gridLayout = QGridLayout(self)
        self.pushButton_open = QPushButton('open', self)
        self.pushButton_open.setEnabled(True)
        self.gridLayout.addWidget(self.pushButton_open, 0, 0, 1, 1)
        self.pushButton_cut = QPushButton('cut', self)
        self.pushButton_cut.setCheckable(False)
        self.pushButton_open.setMaximumSize(QSize(100, 16777215))
        self.gridLayout.addWidget(self.pushButton_cut, 1, 0, 1, 1)
        self.pushButton_save = QPushButton('save', self)
        self.pushButton_save.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton_save, 2, 0, 1, 1)
        spacerItem = QSpacerItem(20, 549, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.graphicsView = GraphicsView(self.picture, self)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.gridLayout.addWidget(self.graphicsView, 0, 1, 4, 1)

    def pushButton_cut_clicked(self):
        if self.graphicsView.image_item.is_start_cut:
            self.graphicsView.image_item.is_start_cut = False
            self.graphicsView.image_item.setCursor(Qt.ArrowCursor)  # 箭头光标
        else:
            self.graphicsView.image_item.is_start_cut = True
            self.graphicsView.image_item.setCursor(Qt.CrossCursor)  # 十字光标

    def pushButton_save_clicked(self):
        rect = QRect(self.graphicsView.image_item.start_point.toPoint(),
                     self.graphicsView.image_item.end_point.toPoint())
        new_pixmap = self.graphicsView.image_item.pixmap().copy(rect)
        default_filename='name.png'
        dirpath = QFileDialog.getSaveFileName( self,'选择保存路径', r'D:\Tree\Template\name.png','Image(*.png)')
        if dirpath[0]!='':
            new_pixmap.save(dirpath[0])
            QMessageBox.information(self, "提示框", "模板保存成功", QMessageBox.Yes)


    def pushButton_open_clicked(self):
        print("open")
        path, _ = QFileDialog.getOpenFileName(None, '选择图像', "D:\\","Image Files(*.jpg *.png *tif)")  # 打开资源管理器，path为原图片绝对路径
        self.picture=path
        print(self.picture)
        self.graphicsView.setPicture(self.picture)

