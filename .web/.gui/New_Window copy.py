# pyinstaller -F -w .\Python学习\exe文件qt\main.py

import sys
from PyQt5.QtWidgets import ( QApplication, QWidget, QLabel, QPushButton, QSlider,
                              QFormLayout, QMessageBox, QComboBox, QLineEdit, QCheckBox,
                              QDesktopWidget, QHBoxLayout, QFileDialog, QDialog)
from PyQt5.QtWidgets import QVBoxLayout


class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)  # 1.1 获取命令行参数
        # ######### 操作区 ########
        """     create layout      """
        # 全局布局（1个）：
        self.Main_Form_Layout = QVBoxLayout()  # 垂直方向
        # # 局部布局（3个）
        # 输入方式1 excel文件方式
        self.excel_area = QFormLayout()
        self.excel_unit = QWidget()
        self.excel_unit.setLayout(self.excel_area)
        # 输入方式2 手动输入方式
        self.param_area = QFormLayout()
        self.param_unit = QWidget()
        self.param_unit.setLayout(self.param_area)
        # 输出
        self.output_area = QFormLayout()
        self.output_unit = QWidget()
        self.output_unit.setLayout(self.output_area)
        # # 局部布局加入全局布局（3个）
        self.Main_Form_Layout.addWidget(self.excel_unit)
        self.Main_Form_Layout.addWidget(self.param_unit)
        self.Main_Form_Layout.addWidget(self.output_unit)

        # 输入方式1
        self.excel_area.addRow(QLabel("Excel_File_Input"))
        self.excel_area.addRow("Path to the entered Excel file:", QLineEdit())
        self.excel_area.addRow("number of generated DAGs:", QLineEdit())
        self.excel_area.addRow(QPushButton('Generate DAGs by Excel'))

        # 输入方式2
        self.param_area.addRow(QLabel("Parameters_Input"))
        # (1) 基本参数：
        Temp_hlayout_1 = QHBoxLayout()
        Temp_hlayout_1.addWidget(QLabel("Nodes_Num:"))
        Temp_hlayout_1.addWidget(QLineEdit())
        Temp_hlayout_1.addWidget(QLabel("Critical_Path:"))
        Temp_hlayout_1.addWidget(QLineEdit())
        Temp_hlayout_1.addWidget(QLabel("number of generated DAGs:"))
        Temp_hlayout_1.addWidget(QLineEdit())
        self.param_area.addRow(Temp_hlayout_1)
        # (2) shape 参数
        Temp_hlayout_2 = QHBoxLayout()
        Temp_hlayout_2.addWidget(QLabel("Min_Shape:"))
        Temp_hlayout_2.addWidget(QLineEdit())
        Temp_hlayout_2.addWidget(QLabel("Max_Shape:"))
        Temp_hlayout_2.addWidget(QLineEdit())
        self.param_area.addRow(Temp_hlayout_2)
        # (3) degree 参数
        Temp_hlayout_3 = QHBoxLayout()
        Temp_hlayout_3.addWidget(QLabel("Max_in_degree:"))
        Temp_hlayout_3.addWidget(QLineEdit())
        Temp_hlayout_3.addWidget(QLabel("Max_out_degree:"))
        Temp_hlayout_3.addWidget(QLineEdit())
        self.param_area.addRow(Temp_hlayout_3)
        # (4) shape 参数
        Temp_hlayout_4 = QHBoxLayout()
        Temp_hlayout_4.addWidget(QLabel("Min_Shape:"))
        Temp_hlayout_4.addWidget(QLineEdit())
        Temp_hlayout_4.addWidget(QLabel("Max_Shape:"))
        Temp_hlayout_4.addWidget(QLineEdit())
        self.param_area.addRow(Temp_hlayout_4)

        # (5) 其他 参数
        Temp_hlayout_5 = QHBoxLayout()
        Temp_hlayout_5.addWidget(QLabel("Jump_level:"))
        Temp_hlayout_5.addWidget(QLineEdit())
        Temp_hlayout_5.addWidget(QLabel("Connection_ratio:"))
        Temp_hlayout_5.addWidget(QLineEdit())
        Temp_hlayout_5.addWidget(QLabel("Width:"))
        Temp_hlayout_5.addWidget(QLineEdit())
        self.param_area.addRow(Temp_hlayout_5)
        self.param_area.addRow(QPushButton('Generate DAGs by parameters'))

        # 输出方式
        self.output_area.addRow(QLabel("Output Data"))
        self.output_area.addRow("Folder path to output data:", QLineEdit())

        # create window
        self.window = QWidget()
        self.window.resize(600, 130)                                    # 2.1 设置窗口的尺寸 # 宽，高
        center_pointer = QDesktopWidget().availableGeometry().center()  # 3.1 获取屏幕中央坐标,调整窗口在屏幕中央显示
        self.window.move(center_pointer.x(), center_pointer.y())        # 3.2 移动到中央(窗口左上角坐标)
        # print (window. frameGeometry())                               # 3.3 获取窗口坐标
        self.window.setWindowTitle('DAG Generator')
        self.window.setLayout(self.Main_Form_Layout)
        self.window.show()
        self.app.exec_()


if __name__ == '__main__':
    G = GUI()
