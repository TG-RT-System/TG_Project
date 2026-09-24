# pyinstaller -F -w .\Python学习\exe文件qt\main.py

import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt5.QtWidgets import ( QApplication, QWidget, QLabel, QPushButton, QSlider,
                              QFormLayout, QMessageBox, QComboBox, QLineEdit, QCheckBox,
                              QDesktopWidget, QHBoxLayout, QFileDialog, QDialog, QVBoxLayout)
import pandas as pd
import networkx as nx
import xlwt
# import graphviz as gz
import pygraphviz as pgv
import os

import Scheduler.DAG_Generator as DG
import Scheduler.DAG_Features_Analysis as DFA
import Scheduler.DAG_Data_Processing as DDP
import Scheduler.DAG_WCET_Config as DWC

class GUI:
    def __init__(self):
        self.Flow_Data_Set = None
        self.app = QApplication(sys.argv)  # 1.1 获取命令行参数
        # ######### 操作区 ########
        """     create layout      """
        # ### 标题
        # self.formLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.window = QWidget()
        self.window.setLayout(self.formLayout)

        self.formLayout.addRow(QLabel("DAG Data Input"))
        self.Excel_DAG_data_InPath  = QLineEdit()
        self.Excel_DAG_param_InPath = QLineEdit()
        self.Excel_Flow_data_InPath = QLineEdit()

        self.Button_DAG_Data_Input = QPushButton('DAG参数抽象')
        self.Button_DAG_Data_Input.clicked.connect(lambda: self.Input_Addr('DAG_data', self.Excel_DAG_data_InPath))
        self.Button_DAG_Param_Input = QPushButton('DAG参数提取')
        self.Button_DAG_Param_Input.clicked.connect(lambda: self.Input_Addr('DAG_param', self.Excel_DAG_param_InPath))
        self.Button_Flow_Param_Input = QPushButton('Flow数据提取')
        self.Button_Flow_Param_Input.clicked.connect(lambda: self.Input_Addr('Flow_data', self.Excel_Flow_data_InPath))

        # 1.1 确定DAG_Excel输入地址
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("(1) 输入_Excel_Data_Addr_文件路径:"))
        hlayout.addWidget(self.Excel_DAG_data_InPath)
        hlayout.addWidget(self.Button_DAG_Data_Input)
        self.formLayout.addRow(hlayout)

        # 1.2 确定DAG_Excel输入地址
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("(2) 输入_Excel_Param_Addr_文件路径:"))
        hlayout.addWidget(self.Excel_DAG_param_InPath)
        hlayout.addWidget(self.Button_DAG_Param_Input)
        self.formLayout.addRow(hlayout)

        # hlayout = QHBoxLayout()
        # hlayout.addWidget(QLabel("(3) 输入_Excel_Flow_Addr_文件路径:"))
        # hlayout.addWidget(self.Excel_Flow_data_InPath)
        # hlayout.addWidget(self.Button_Flow_Param_Input)
        # self.formLayout.addRow(hlayout)

        # 2 DAG特性参数；
        # self.formLayout.addRow(QLabel('DAG Critical Features list'))
        self.label = QLabel("DAG Generator Tool")

        self.Number_Of_Nodes        = QLineEdit()   # (1.):
        self.Number_Of_Edges        = QLineEdit()   # (1.):
        self.Number_Of_Levels       = QLineEdit()   # (1.):
        self.Number_Of_Width        = QLineEdit()   # (1.):
        self.Gen_DAG_NUM            = QLineEdit()
        self.Connection_Rate        = QLineEdit()   # (1.):
        self.Jump_Level             = QLineEdit()   # (1.):
        self.DAG_volume             = QLineEdit()   # (1.):
        self.DAG_Cri_Rate           = QLineEdit()   # (1.):
        self.Param_Max_Shape        = QLineEdit()
        self.Param_Min_Shape        = QLineEdit()
        self.Param_Max_In_Degree    = QLineEdit()
        self.Param_Max_Out_Degree   = QLineEdit()
        self.Param_Max_WCET         = QLineEdit()
        self.Param_Min_WCET         = QLineEdit()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("(1.1) Nodes_Num:"))
        hlayout.addWidget(self.Number_Of_Nodes)
        # hlayout.addWidget(QLabel("(1.2)DAG的边数量:"))
        # hlayout.addWidget(self.Number_Of_Edges)
        hlayout.addWidget(QLabel("(1.2) Level:"))
        hlayout.addWidget(self.Number_Of_Levels)
        hlayout.addWidget(QLabel("(1.3) Width:"))
        hlayout.addWidget(self.Number_Of_Width)
        hlayout.addWidget(QLabel("(1.4) Number_Of_DAGs:"))
        hlayout.addWidget(self.Gen_DAG_NUM)
        self.formLayout.addRow(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("(1.5) Connection_Rate:"))
        hlayout.addWidget(self.Connection_Rate)
        hlayout.addWidget(QLabel("(1.6) Jump_Level:"))
        hlayout.addWidget(self.Jump_Level)
        hlayout.addWidget(QLabel("(1.7) Max_WCET:"))
        hlayout.addWidget(self.Param_Max_WCET)
        hlayout.addWidget(QLabel("(1.8) Min_WCET:"))
        hlayout.addWidget(self.Param_Min_WCET)
        # hlayout.addWidget(QLabel("(1.7)DAG的体积:"))
        # hlayout.addWidget(self.DAG_volume)
        # hlayout.addWidget(QLabel("(1.8)DAG的关键路径比:"))
        # hlayout.addWidget(self.DAG_Cri_Rate)
        self.formLayout.addRow(hlayout)

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("(1.9) Max_Shape:"))
        hlayout.addWidget(self.Param_Max_Shape)
        hlayout.addWidget(QLabel("(1.10) Min_Shape:"))
        hlayout.addWidget(self.Param_Min_Shape)
        hlayout.addWidget(QLabel("(1.11) Max_In_Degree:"))
        hlayout.addWidget(self.Param_Max_In_Degree)
        hlayout.addWidget(QLabel("(1.12) Max_Out_Degree:"))
        hlayout.addWidget(self.Param_Max_Out_Degree)
        self.formLayout.addRow(hlayout)

        # 3 DAG生成参数；
        self.formLayout.addRow(QLabel('DAG Generation Paramter'))
        self.Arrive_time_bottom  = QLineEdit()
        self.Arrive_time_roof    = QLineEdit()
        self.Gen_Jitter          = QLineEdit()
        self.Branch_node         = QLineEdit()

        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("Arrive time:"))
        hlayout.addWidget(QLabel("["))
        hlayout.addWidget(self.Arrive_time_bottom)
        hlayout.addWidget(QLabel("—"))
        hlayout.addWidget(self.Arrive_time_roof)
        hlayout.addWidget(QLabel("]\t"))

        hlayout.addWidget(QLabel("Random range(%):"))
        hlayout.addWidget(self.Gen_Jitter)
        hlayout.addWidget(QLabel("\t"))

        self.level_change = QCheckBox('level_change')
        hlayout.addWidget(self.level_change)
        hlayout.addWidget(QLabel("\t"))

        hlayout.addWidget(QLabel("branch_nodes:"))
        hlayout.addWidget(self.Branch_node)

        self.formLayout.addRow(hlayout)

        # 4 确定输出地址
        self.formLayout.addRow(QLabel("DAG Data Output:"))
        hlayout = QHBoxLayout()
        hlayout.addWidget(QLabel("输出_Excel_DAG_Data_文件路径:"))
        self.Excel_DAG_data_OutPath = QLineEdit()
        self.Output_Button = QPushButton('打开')
        self.Output_Button.clicked.connect(self.Output_Data_SELF)  # 按钮关联函数
        hlayout.addWidget(self.Excel_DAG_data_OutPath)
        hlayout.addWidget(self.Output_Button)
        self.formLayout.addRow(hlayout)

        self.formLayout.addRow(QLabel('DAG Output Model:'))
        # self.DAG_Generator_Param = QPushButton('基于参数生成DAG(1/2)\n(附加：生成DAG数量)')
        self.DAG_Generator_Param = QPushButton('DAG Generate')
        self.DAG_Generator_Param.clicked.connect(self.DAG_Generator_Param_Based)

        # self.DAG_Generator_Flow  = QPushButton('基于流生成DAG(3)\n(附加：生成DAG数量， 生成流数量和jitter比例)')
        # self.DAG_Generator_Flow.clicked.connect(self.DAG_Generator_Flow_Based)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.DAG_Generator_Param)
        # hlayout.addWidget(self.DAG_Generator_Flow)
        self.formLayout.addRow(hlayout)

        self.window.resize(500, 130)
        # self.window.setWindowTitle('DAG Critical Features Abstract')
        self.window.setWindowTitle("DAG Generator Tool")
        self.window.show()
        self.app.exec_()

    def Input_Addr(self, path, Qedit):
        download_path = QFileDialog.getOpenFileName(None)[0]
        print(download_path)
        if download_path == '':
            return False
        else:
            Qedit.setText(download_path)
            if path == 'DAG_data':
                self.DAG_Data_Abstract()
            elif path == 'DAG_param':
                self.DAG_Param_Input()
            elif path == 'Flow_data':
                self.Flow_Data_InPut()
            else:
                return False
            return True

    # (1) type 1
    def DAG_Data_Abstract(self):
        input_path = self.Excel_DAG_data_InPath.text()
        if (not os.path.exists(input_path)) or (".csv" not in input_path):
            QMessageBox.critical(self.window, '错误', '输入文件不存在', QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        DAG_Obj = DG.Manual_Input('CSV', [input_path])[0]
        DFA.dag_param_critical_update(DAG_Obj, DAGType=1, DAG_id=1, Period=0)
        self.DAG_Critical_Features_Set(DAG_Obj)

    # (2) type 2
    def DAG_Param_Input(self):
        input_path = self.Excel_DAG_param_InPath.text()
        if (not os.path.exists(input_path)) or (".xlsx" not in input_path):
            QMessageBox.critical(self.window, '错误', '输入文件不存在', QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        self.Data_Critical_Features_Set(DG.DAG_Feature_Input(input_path)[0])

    # (3) type 3
    def Flow_Data_InPut(self):
        input_path = self.Excel_Flow_data_InPath.text()
        if (not os.path.exists(input_path)) or (".xlsx" not in input_path):
            QMessageBox.critical(self.window, '错误', '输入文件不存在', QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        self.Flow_Data_Set = DG.Manual_Input('XLSX', [input_path])
        for dag_id, dag_x in enumerate(self.Flow_Data_Set):
            DFA.dag_param_critical_update(dag_x, DAGType=dag_x.graph['DAG_ID'], DAG_id=dag_id, Period=0)
        self.Input_Flow_SetNum.setText(str(len(self.Flow_Data_Set)))

    def Data_Critical_Features_Set(self, DAG_Feature):
        rows, columns = DAG_Feature.shape
        temp_data_dict = {DAG_Feature[rows_x][0]:DAG_Feature[rows_x][1] for rows_x in range(rows)}
        self.Number_Of_Nodes.setText(str(temp_data_dict['Number_Of_Nodes']))
        self.Number_Of_Edges.setText(str(temp_data_dict['Number_Of_Edges']))
        self.Number_Of_Levels.setText(str(temp_data_dict['Number_Of_Level']))
        self.Number_Of_Width.setText(str(temp_data_dict["Width"]))
        self.Connection_Rate.setText(str(round(temp_data_dict["Connection_Rate"], 2)))
        # self.DAG_volume.setText(str(temp_data_dict["Volume"]))
        # self.DAG_Cri_Rate.setText(str(round(temp_data_dict["CriVolumeRate"], 2)))
        self.Jump_Level.setText(str(temp_data_dict["Jump_Level"]))

        self.Param_Max_Shape.setText(str(temp_data_dict["Max_Shape"]))
        self.Param_Min_Shape.setText(str(temp_data_dict["Min_Shape"]))
        self.Param_Max_In_Degree.setText(str(temp_data_dict["Max_In_Degree"]))
        self.Param_Max_Out_Degree.setText(str(temp_data_dict["Max_Out_Degree"]))
        self.Param_Max_WCET.setText(str(temp_data_dict["Max_WCET"]))
        self.Param_Min_WCET.setText(str(temp_data_dict["Min_WCET"]))

    def DAG_Critical_Features_Set(self, temp_DAG_obj):
        self.Number_Of_Nodes.setText(str(temp_DAG_obj.number_of_nodes()))
        self.Number_Of_Edges.setText(str(temp_DAG_obj.number_of_edges()))
        self.Number_Of_Levels.setText(str(temp_DAG_obj.graph['Number_Of_Level']))
        self.Number_Of_Width.setText(str(temp_DAG_obj.graph["Width"]))
        self.Connection_Rate.setText(str(round(temp_DAG_obj.graph["Connection_Rate"], 2)))
        # self.DAG_volume.setText(str(temp_DAG_obj.graph["Volume"]))
        # self.DAG_Cri_Rate.setText(str(round(temp_DAG_obj.graph["CriVolumeRate"], 2)))
        self.Jump_Level.setText(str(temp_DAG_obj.graph["Jump_Level"]))

        self.Param_Max_Shape.setText(str(temp_DAG_obj.graph["Max_Shape"]))
        self.Param_Min_Shape.setText(str(temp_DAG_obj.graph["Min_Shape"]))
        self.Param_Max_In_Degree.setText(str(temp_DAG_obj.graph["Max_In_Degree"]))
        self.Param_Max_Out_Degree.setText(str(temp_DAG_obj.graph["Max_Out_Degree"]))
        self.Param_Max_WCET.setText(str(temp_DAG_obj.graph["Max_WCET"]))
        self.Param_Min_WCET.setText(str(temp_DAG_obj.graph["Min_WCET"]))

    def Output_Data_SELF(self):
        self.Excel_DAG_data_OutPath.setText( QFileDialog.getExistingDirectory(None) )

    def DAG_Generator_Flow_Based(self):
        try:
            Dags_Num        = int(self.Gen_DAG_NUM.text())
            Flow_NUM        = int(self.Gen_Flow_NUM.text())
            Jitter_Rate     = float(self.Gen_Jitter.text())

            Param_dict = {'Flow_set': self.Flow_Data_Set, 'flow_num': Flow_NUM, 'WCET_interval': Jitter_Rate,
                          'DAG_Num': Dags_Num, 'arrival_interval': [0, 20 * 2260]}
            Total_DAG_list = DG.Algorithm_input('FLOW', Param_dict)
            for DAG_id, DAG_x in enumerate(Total_DAG_list):
                # DWC.WCET_Config(DAG_x, 'Uniform', Virtual_node=True, a=Min_WCET, b=Max_WCET)
                DFA.dag_param_critical_update(DAG_x, DAGType=DAG_id, DAG_id=DAG_id, Period=0)
                for node_x in DAG_x.nodes(data=True):
                    node_x[1]['WCET'] = int(node_x[1]['WCET'])
            new_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            DDP.Exam_Data_Output(Total_DAG_list, 'ALL', self.Excel_DAG_data_OutPath.text() + '/Flow_Data_Generator/{0}/'.format(new_time))
        except:
            QMessageBox.critical(self.window, 'Faile', '生成失败', QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        else:
            QMessageBox.question(self.window, "Success", "DAG生成完成！", QMessageBox.Yes)
            return True

    def Data_Trans_HTOS(self):      # Excel_(HUAWEI)到_(SELF)转换 包括（self and feature data）
        input_path = self.Excel_HUAWEI_Input_Path.text()
        output_path = self.Excel_SELF_Output_Path.text()
        if (output_path == '') or (not os.path.exists(input_path)) or (".xls" not in input_path) or (".xlsx" not in input_path):
            QMessageBox.critical(self.window, '错误', "文件错误", QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        if input_path == output_path:
            QMessageBox.critical(self.window, '错误', "文件错误", QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        DAG_list = []
        # todo 录入DAG数据
        with pd.ExcelFile(input_path) as data:
            all_sheet_names = data.sheet_names  # 获取所有sheet名字；
            for DAG_ID in all_sheet_names:
                temp_DAG = nx.DiGraph()
                temp_DAG.graph['DAG_ID'] = DAG_ID
                df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
                temp_node_index = 0
                self_node_dict = {}
                for row in df.index:
                    node_list_ID = df.loc[row]['JobTypeID']
                    if node_list_ID != node_list_ID:
                        continue
                    else:
                        node_list_ID = int(node_list_ID)
                    node_temp_num = int(df.loc[row]['InstanceNumber'])
                    node_precursor_list = df.loc[row]['TriggerJobTypeIDSet']
                    if node_precursor_list != node_precursor_list:
                        node_precursor_list = []
                    elif type(node_precursor_list) == str:
                        node_precursor_list = node_precursor_list.split(',')
                    else:
                        node_precursor_list = [node_precursor_list]
                    node_execution_time = df.loc[row]['ExecutionTime']
                    node_priority = int(df.loc[row]['QoS'])
                    self_node_dict[node_list_ID] = []
                    for x in range(node_temp_num):
                        temp_node_index += 1
                        node_temp_id = 'Job_' + str(node_list_ID) + '_' + str(x+1)
                        temp_DAG.add_node(temp_node_index, Node_Index=temp_node_index, Node_ID=node_temp_id, WCET=node_execution_time, Prio=node_priority)
                        self_node_dict[node_list_ID] .append(temp_node_index)
                        for node_precursor in node_precursor_list:
                            for u in self_node_dict[int(node_precursor)]:
                                temp_DAG.add_edge(u, temp_node_index)
                DAG_list.append(temp_DAG)
        # todo （1）保存DAG（self）_excel  文件
        workbook = xlwt.Workbook(encoding='utf-8')
        for obj_dag_i in (DAG_list):
            nodex = obj_dag_i.nodes[1]
            node_feature = [node_k for node_k, node_v in nodex.items()]
            worksheet = workbook.add_sheet("DAG_{0}".format(obj_dag_i.graph["DAG_ID"]))
            for j, node_j in enumerate(node_feature):
                worksheet.write(0, j, node_j)
            for j, node_j in enumerate(obj_dag_i.nodes(data=True)):
                for k, node_feature_k in enumerate(node_feature):
                    worksheet.write(j+1, k, node_j[1][node_feature_k])
        workbook.save(output_path + '/DAG_SELF.xls')
        # todo （2）保存DAG（feature）_excel  文件
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet("DAG_Critical_Features")
        Features_Tytle = ["DAG_ID", "Number_Of_Nodes",  "Number_Of_Edges",  "Number_Of_Level",
                          "Max_Shape",    "Min_Shape",    "Ave_Shape", "Std_Shape",
                          "Max_Re_Shape", "Min_Re_Shape", "Ave_Re_Shape", "Std_Re_Shape",
                          "Width", "Max_Degree", "Min_Degree", "Ave_Degree", "Std_Degree",
                          "Max_In_Degree", "Min_In_Degree", "Ave_In_Degree", "Std_In_Degree",
                          "Max_Out_Degree", "Min_Out_Degree", "Ave_Out_Degree", "Std_Out_Degree",
                          "Connection_Rate", "DAG_volume", "Max_WCET", "Min_WCET", "Ave_WCET", "Std_WCET", 'Jump_Level']
        for i, feature_i in enumerate(Features_Tytle):
            worksheet.write(i, 0, feature_i)
        for x, DAG_x in enumerate(DAG_list):
            self.dag_param_critical_update(DAG_x, x)        # 更新DAG特性；
            for i, feature_i in enumerate(Features_Tytle):
                worksheet.write(i, x + 1, DAG_x.graph[feature_i])
        workbook.save(output_path + '/DAG_Features.xls')
        # todo （3）保存DAG图png文件：
        for DAG_x in DAG_list:
            gvd = pgv.AGraph(directed=True, rankdir="LR")
            for node_x in DAG_x.nodes(data=True):
                temp_label = ''
                temp_label += str(node_x[0]) + '\n'
                temp_label += 'Node_ID:' + str(node_x[1]['Node_ID']) + '\n'
                temp_label += 'WCET:' + str(node_x[1]['WCET']) + '\n'
                temp_label += 'Prio:' + str(node_x[1]['Prio']) + '\n'
                gvd.add_node(node_x[0], label=temp_label)
            for edge_x in DAG_x.edges(data=True):
                gvd.add_edge(edge_x[0], edge_x[1])
            gvd.layout(prog='dot')  # 要有，否则会出现log文件
            gvd.draw(path=output_path + '/' + DAG_x.graph['DAG_ID'] + '.png', format='png')
        # todo （4）添加特性到参数表中：
        for DAG_x in DAG_list:
            self.Number_Of_Nodes.setText( str(DAG_x.graph["Number_Of_Nodes"]) )
            self.Number_Of_Edges.setText( str(DAG_x.graph["Number_Of_Edges"]) )
            self.Number_Of_Levels.setText( str(DAG_x.graph["Number_Of_Level"]) )
            self.Number_Of_Width.setText( str(DAG_x.graph["Width"]) )
            self.Connection_Rate.setText( str(round(DAG_x.graph["Connection_Rate"], 2)) )
            self.Jump_Level.setText( str(DAG_x.graph["Jump_Level"]) )

            self.Param_Max_Shape.setText( str(DAG_x.graph["Max_Shape"]) )
            self.Param_Min_Shape.setText( str(DAG_x.graph["Min_Shape"]) )
            self.Param_Max_In_Degree.setText( str(DAG_x.graph["Max_In_Degree"]) )
            self.Param_Max_Out_Degree.setText( str(DAG_x.graph["Max_Out_Degree"]) )

            self.Param_Max_WCET.setText( str(round(DAG_x.graph["Max_WCET"], 2)) )
            self.Param_Min_WCET.setText( str(round(DAG_x.graph["Min_WCET"], 2)) )
            self.Param_Ave_WCET.setText( str(round(DAG_x.graph["Ave_WCET"], 2)) )
            self.Param_Std_WCET.setText( str(round(DAG_x.graph["Std_WCET"], 2)) )

        # todo （0）返回正确信息：
        QMessageBox.question(self.window, "Success", "DAG特性抽象完成！", QMessageBox.Yes)
        return True

    def DAG_Generator_Param_Based(self):
        try:
            Dags_Num        = int(self.Gen_DAG_NUM.text())
            Width           = int(float(self.Number_Of_Width.text()))
            Node_Num        = int(float(self.Number_Of_Nodes.text()))
            Edge_Num        = int(float(self.Number_Of_Edges.text()))
            Critic_Path     = int(float(self.Number_Of_Levels.text()))
            Jump_level      = int(float(self.Jump_Level.text()))
            Max_Shape       = int(float(self.Param_Max_Shape.text()))
            Min_Shape       = int(float(self.Param_Min_Shape.text()))
            Max_in_degree   = int(float(self.Param_Max_In_Degree.text()))
            Max_out_degree  = int(float(self.Param_Max_Out_Degree.text()))
            Connection_Rate = float(self.Connection_Rate.text())
            Max_WCET        = float(self.Param_Max_WCET.text())
            Min_WCET        = float(self.Param_Min_WCET.text())

            ret_dag_list = DG.Algorithm_input("MINE", {'Node_Num': Node_Num,
                                                       'Edge_Num': Edge_Num,
                                                       'Critic_Path': Critic_Path,
                                                       'Jump_level': Jump_level,
                                                       'Max_Shape': Max_Shape,
                                                       'Min_Shape': Min_Shape,
                                                       'Max_in_degree': Max_in_degree,
                                                       'Max_out_degree': Max_out_degree,
                                                       'Conn_ratio': Connection_Rate,
                                                       'Width': Width,
                                                       'DAG_Num': Dags_Num})

            analysis_data = []
            for DAG_id, DAG_x in enumerate(ret_dag_list):
                DWC.WCET_Config(DAG_x, 'Uniform', Virtual_node=True, a=Min_WCET, b=Max_WCET)
                DFA.dag_param_critical_update(DAG_x, DAGType=DAG_id, DAG_id=DAG_id, Period=0)
                for node_x in DAG_x.nodes(data=True):
                    node_x[1]['WCET'] = int(node_x[1]['WCET'])
                analysis_data.append(DAG_x)
            new_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            DDP.Exam_Data_Output(analysis_data, 'ALL', self.Excel_DAG_data_OutPath.text() + '/DAG_Data_Generator/{0}/'.format(new_time))
        except:
            QMessageBox.critical(self.window, 'Faile', '生成失败', QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False
        else:
            QMessageBox.question(self.window, "Success", "DAG生成完成！", QMessageBox.Yes)
            return True


if __name__ == '__main__':
    # # 创建应用
    # window_application = QApplication(sys.argv)
    # # 设置登录窗口
    # login_ui = LoginDialog()
    # # 校验是否验证通过
    # if login_ui.exec_() == QDialog.Accepted:
    G = GUI()
