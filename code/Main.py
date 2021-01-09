import sys
import mainUI
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
import matlab.engine
from Create_logic import Logic_create
from main_log import Logic_mian

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = mainUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    Log = Logic_mian()
    Log.show()
    sys.exit(app.exec_())