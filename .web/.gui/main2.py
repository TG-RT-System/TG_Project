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

class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)  # 1.1 获取命令行参数
        # ######### 操作区 ########
        """     create layout      """
        # 全局布局（1个）：
        # self.formLayout = QVBoxLayout()
        self.formLayout = QFormLayout()     # 网格
        # 局部布局（2个）
        self.makespan_area          = QFormLayout()  # makespan图像区域垂直（1）
        self.paramete_area          = QHBoxLayout()  # 参数区域水平（2）
        # 局中局布局（3个）
        self.input_paramete_area    = QFormLayout()  # 列表（2.1）
        self.output_paramete_area   = QFormLayout()  # 垂直（2.2）
        self.ctrl_paramete_area     = QFormLayout()  # 垂直（2.3）
        # 准备3个部件
        self.paramete_unit          = QWidget()
        self.input_unit             = QWidget()
        self.output_unit            = QWidget()
        self.ctrl_unit              = QWidget()
        self.makespan_unit          = QWidget()
        # 3个部件设置局部布局
        self.paramete_unit.setLayout(self.paramete_area)
        self.input_unit.setLayout   (self.input_paramete_area)
        self.output_unit.setLayout  (self.output_paramete_area)
        self.ctrl_unit.setLayout    (self.ctrl_paramete_area)
        self.makespan_unit.setLayout(self.makespan_area)

        self.paramete_area.addWidget(self.input_unit)
        self.paramete_area.addWidget(self.output_unit)
        self.paramete_area.addWidget(self.ctrl_unit)
        self.formLayout.addWidget(self.paramete_unit)
        self.formLayout.addWidget(self.makespan_unit)
        # 1. 标题
        # self.formLayout.addRow(QLabel("dag-gen-rnd: Randomised DAG Generator"))

        # ############ #
        # 1.输入参数区域 #
        # ############ #
        self.input_paramete_area.addWidget(QLabel("input_paramete_area"))
        # 1.1. parameter_1-设置 生成算法类型
        self.opt_alogrithm = QComboBox()
        self.opt_alogrithm.addItem("GNM")
        self.opt_alogrithm.addItem("GNP")
        self.opt_alogrithm.addItem("RNG")
        self.opt_alogrithm.addItem("LBL")
        self.opt_alogrithm.addItem("MINE")
        # 1.2. parameter_2-DAG的并行度
        self.edit_parallism = QLineEdit()
        self.edit_parallism.setText("4")
        """
        # 1.3. parameter_3-DAG的最小关键路径长度
        self.edit_critical_min = QLineEdit()
        self.edit_critical_min.setText("3")
        # 1.4. parameter_4-DAG的最大关键路径长度
        self.edit_critical_max = QLineEdit()
        self.edit_critical_max.setText("7")
        """
        self.edit_critical = QLineEdit()
        self.edit_critical.setText("3")
        # 1.5. parameter_5-DAG的连通性（稠密度）
        self.edit_pc = QLineEdit()
        self.edit_pc.setText("0.5")
        # 1.6. parameter_6-是否为混合关键性调度
        self.check_mcs_dag = QCheckBox()
        self.check_mcs_dag.setChecked(False)
        # 1.7. parameter_7-是否为条件DAG
        self.check_conditional = QCheckBox()
        self.check_conditional.setChecked(True)

        self.input_paramete_area.addRow("&Algorithm:", self.opt_alogrithm)
        self.input_paramete_area.addRow("&Maximum Parallelism<font color='blue'> >=1 </font>:",  self.edit_parallism)
        self.input_paramete_area.addRow("&Maximum Parallelism<font color='blue'> >=1 </font>:",  self.edit_critical)
        # self.input_paramete_area.addRow("Critical Path (min) <font color='blue'> >=3 </font>:",self.edit_critical_min)
        # self.input_paramete_area.addRow("Critical Path (max) <font color='blue'> >=3 </font>:",self.edit_critical_max)
        self.input_paramete_area.addRow("p(Connnection)      <font color='blue'> [0,1] </font>:", self.edit_pc)
        self.input_paramete_area.addRow("&Mixed-Criticality DAG?", self.check_mcs_dag)
        self.input_paramete_area.addRow("&Conditional DAG?", self.check_conditional)

        # ############ #
        # 2.输出参数区域 #
        # ############ #
        self.output_paramete_area.addWidget(QLabel("output_paramete_area"))

        # ############ #
        # 3.控制区域 #
        # ############ #
        self.ctrl_paramete_area.addWidget(QLabel("ctrl_paramete_area"))
        # 3.1. 按钮1
        self.button_gen_conf = QPushButton('Generate Configuration')
        # 3.2. 按钮2
        self.button_gen = QPushButton('Generate DAGs')
        self.button_gen.clicked.connect(self.event_on_button_gen_clicked)
        # 3.3. 按钮3
        self.draw_dag = QPushButton('draw DAGs')
        self.draw_dag.clicked.connect(self.event_on_draw_dag_clicked)

        self.ctrl_paramete_area.addWidget(self.button_gen_conf)
        self.ctrl_paramete_area.addWidget(self.button_gen)
        self.ctrl_paramete_area.addWidget(self.draw_dag)
        # ############# #
        # 4.makespan区域 #
        # ############# #
        self.fig    = plt.Figure()
        self.canvas = FC(self.fig)
        self.makespan_area.addWidget(self.canvas)

        # create window
        self.window = QWidget()
        # self.window.resize(400, 200)  # 2.1 设置窗口的尺寸 # 宽，高
        center_pointer = QDesktopWidget().availableGeometry().center()  # 获取屏幕中央坐标,调整窗口在屏幕中央显示
        self.window.move(center_pointer.x(), center_pointer.y())        # 移动到中央(窗口左上角坐标)
        # print (window. frameGeometry())                               # 获取窗口坐标
        self.window.setWindowTitle('PyQt5 Draw')                        # 窗口标题
        self.window.setLayout(self.formLayout)
        self.window.show()
        self.app.exec_()

    def event_on_button_gen_clicked(self):
        print(self.edit_pc.text())
        print(self.check_mcs_dag.isChecked())
        print(self.check_conditional.isChecked())
        G = DAG.DAG()               # （0）DAG初始化
        ##############################
        # step0. DAG参数配置
        # （1.1）手动生成DAG
        # G.user_defined_dag()
        # （1.2）随机生成DAG参数初始化
        # （1.2.1）DAG_结构生成
        G.DAG_ID        = "DAG_{0}".format("4_6")           # 配置DAG的ID
        G.Priority      = 1                                 # 配置DAG的优先级
        G.parallelism   = int(self.edit_parallism.text())   # 输入并行度
        G.Critical_path = int(self.edit_critical.text())    # 输入关键路径长度
        G.DAG_Generator(self.opt_alogrithm.currentText())   # "GNP"、"mine"、"GNM"
        plt.subplot(121)  # 绘制子图,创建一个1行2列的图形，并选取第1行第1列的子图作为绘图背景
        nx.draw(G.G)
        plt.subplot(122)  # 创建一个1行2列的图形，选取第1行第2列的子图作为绘图背景
        # nx.draw(G, pos=nx.circular_layout(G), node_color='r', edge_color='b')  # 绘图函数
        plt.show()  # 展示图
        """
        # G.WCET_Config("gauss", 10, 100)   # gauss # random # normal
        # G.WCET_Config("random", 10, 100)  # gauss # random # normal
        G.WCET_Config("normal", 10, 100)    # gauss # random # normal
        G.Priority_Config("random")         # DAG 优先级配置；
        G.critical_path_config()            # DAG 关键路径配置；
        G.graph_node_position_determine()   # step5. DAG节点位置确定
        """
        ##############################
        # step6*. DAG的响应时间分析测试
        ##############################
        # core_num = 3
        # NP_RTA = G.Response_Time_analysis("non-preemptive", core_num)
        # P_RTA = G.Response_Time_analysis("preemptive", core_num)
        # print("DAG在core数为{0}的平台下，可抢占模式的响应时间为：{1}、不可抢占模式的响应时间为:{2}".format(
        #     core_num, NP_RTA, P_RTA))

        # #### DAG 关键数据分析；#### #
        # G.dag_param_critical_update()  # 关键数据分析
        # #### 画图；#### #
        # plt.xlabel('crirical={}'.format(G.Critical_path))
        # plt.ylabel('param={}'.format(G.parallelism))
        # plt.show()

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
