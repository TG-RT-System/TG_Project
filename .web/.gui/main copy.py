import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import ( QApplication, QWidget, QLabel, QPushButton, QSlider,
                              QFormLayout, QMessageBox, QComboBox, QLineEdit, QCheckBox,
                              QDesktopWidget )
# pyinstaller -F -w .\Python学习\exe文件qt\main.py

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)  # 1.1 获取命令行参数
        # ######### 操作区 ########
        """     create layout      """
        self.formLayout = QFormLayout()
        # 1. 标题
        self.label = QLabel("dag-gen-rnd: Randomised DAG Generator")
        self.formLayout.addRow(self.label)
        # 2. 建立下拉列表
        self.opt_alogrithm = QComboBox()
        self.opt_alogrithm.addItem("1")
        self.opt_alogrithm.addItem("2")
        self.opt_alogrithm.addItem("3")
        self.opt_alogrithm.addItem("4")
        self.formLayout.addRow("&Algorithm:", self.opt_alogrithm)
        # 3. 建立清单文本
        # parameter_1-DAG的并行度
        self.edit_parallism = QLineEdit()
        self.edit_parallism.setText("4")
        self.formLayout.addRow("&Maximum Parallelism <font color='blue'> >=1     </font>:", self.edit_parallism)
        # parameter_2-DAG的最小关键路径长度
        self.edit_critical_min = QLineEdit()
        self.edit_critical_min.setText("3")
        self.formLayout.addRow("Critical Path (min)  <font color='blue'> >=3     </font>:", self.edit_critical_min)
        # parameter_3-DAG的最大关键路径长度
        self.edit_critical_max = QLineEdit()
        self.edit_critical_max.setText("7")
        self.formLayout.addRow("Critical Path (max)  <font color='blue'> >=3     </font>:", self.edit_critical_max)
        # parameter_4-DAG的连通性（稠密度）
        self.edit_pc = QLineEdit()
        self.edit_pc.setText("0.5")
        self.formLayout.addRow("p(Connnection)       <font color='blue'> [0,1]   </font>:", self.edit_pc)
        # 4. 选框
        self.check_mcs_dag = QCheckBox()
        self.formLayout.addRow("&Mixed-Criticality DAG?", self.check_mcs_dag)
        self.check_mcs_dag.setChecked(False)

        self.check_conditional = QCheckBox()
        self.formLayout.addRow("&Conditional DAG?", self.check_conditional)
        self.check_conditional.setChecked(True)
        # 5. 按钮
        self.button_gen_conf = QPushButton('Generate Configuration')
        self.formLayout.addRow(self.button_gen_conf)

        self.button_gen = QPushButton('Generate DAGs')
        self.formLayout.addRow(self.button_gen)
        self.button_gen.clicked.connect(self.event_on_button_gen_clicked)

        self.draw_dag = QPushButton('draw DAGs')
        self.formLayout.addRow(self.draw_dag)
        self.draw_dag.clicked.connect(self.event_on_draw_dag_clicked)

        # 6. 画布
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.formLayout.addRow(self.canvas)

        # create window
        self.window = QWidget()
        # self.window.resize(400, 200)  # 2.1 设置窗口的尺寸 # 宽，高
        center_pointer = QDesktopWidget().availableGeometry().center()  # 3.1 获取屏幕中央坐标,调整窗口在屏幕中央显示
        self.window.move(center_pointer.x(), center_pointer.y())        # 3.2 移动到中央(窗口左上角坐标)
        # print (window. frameGeometry())                               # 3.3 获取窗口坐标
        self.window.setWindowTitle('PyQt5 Draw')
        self.window.setLayout(self.formLayout)
        self.window.show()
        self.app.exec_()

    def event_on_button_gen_clicked(self):
        print("Hello World")
        print( self.opt_alogrithm.currentText())
        print( self.edit_parallism.text() )
        print( self.edit_critical_min.text() )
        print( self.edit_critical_max.text() )
        print( self.edit_pc.text() )
        print( self.check_mcs_dag.isChecked() )
        print( self.check_conditional.isChecked() )

    def event_on_draw_dag_clicked(self):
        try:
            self.fig.clf()
            ax1 = self.fig.add_subplot(211)
            x = np.linspace(0, 100, 100)
            y = np.random.random(100)
            ax1.cla()
            ax1.plot(x, y)

            ax2 = self.fig.add_subplot(212)
            x = np.linspace(0, 100, 100)
            y = np.random.random(100)
            ax2.cla()
            ax2.plot(x, y)

            self.canvas.draw()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    G = GUI()