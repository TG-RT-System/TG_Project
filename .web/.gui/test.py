import sys
import DAG
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt  # 导入模块函数，目的是为了绘制子图
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QSlider, QFormLayout, QMessageBox, QComboBox,
                             QLineEdit, QCheckBox, QDesktopWidget,
                             QHBoxLayout, QVBoxLayout, QGridLayout)

# 水平布局：QHBoxLayout（所有控件都在一行水平摆放，并且无法设置控件的垂直方向上的对齐方式，只可以设置其水平方向上的对齐方式）
# 垂直布局：QVBoxLayout（所有控件都在一列垂直摆放，并且无法设置控件的水平方向上的对齐方式，只可以设置其垂直方向上的对齐方式）
# 网格布局：QGridLayout （所有控件都在N行N列摆放，可以设置控件的水平和垂直方向上的对齐方式）
# 表格布局：QFormLayout （所有控件都在N行2列摆放，可以设置控件的水平和垂直方向上的对齐方式）
app = QApplication(sys.argv)  # 1.1 获取命令行参数
# ######### 操作区 ########
"""     create layout      """
# 全局布局（1个）：
# self.formLayout = QVBoxLayout()
formLayout = QFormLayout()     # 1.网格
# 局部布局（2个）
# ################## 1 ###########################
makespan_area = QFormLayout()  # 局部布局（1.1）
makespan_unit = QWidget()
makespan_unit.setLayout(makespan_area)
formLayout.addWidget(makespan_unit)

# ################## 2 ###########################
paramete_area = QHBoxLayout()  # 局部布局（1.2）
paramete_unit = QWidget()
paramete_unit.setLayout(paramete_area)

input_paramete_area    = QFormLayout()  # 列表（1.2.1）
input_unit = QWidget()
input_unit.setLayout(input_paramete_area)
paramete_area.addWidget(input_unit)

opt_alogrithm = QComboBox()
input_paramete_area.addRow("&Algorithm:", opt_alogrithm)


output_paramete_area   = QFormLayout()  # 垂直（1.2.2）
output_unit = QWidget()
output_unit.setLayout(output_paramete_area)
paramete_area.addWidget(output_unit)

ctrl_paramete_area     = QFormLayout()  # 垂直（1.2.3）
ctrl_unit = QWidget()
ctrl_unit.setLayout(ctrl_paramete_area)
paramete_area.addWidget(ctrl_unit)

formLayout.addWidget(paramete_unit)
##############################################


window = QWidget()
window.resize(600, 130)  # 2.1 设置窗口的尺寸 # 宽，高
center_pointer = QDesktopWidget().availableGeometry().center()  # 3.1 获取屏幕中央坐标,调整窗口在屏幕中央显示
window.move(center_pointer.x(), center_pointer.y())             # 3.2 移动到中央(窗口左上角坐标)
# print (window. frameGeometry())                               # 3.3 获取窗口坐标
window.setWindowTitle('DAG Critical Features Abstract')
window.setLayout(formLayout)

window.show()
app.exec_()