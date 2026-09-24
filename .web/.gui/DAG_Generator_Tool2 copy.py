# pyinstaller -F -w .\Python学习\exe文件qt\main.py

import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QFormLayout, QMessageBox, QLineEdit,
                             QDesktopWidget, QHBoxLayout, QFileDialog, QVBoxLayout)
import pandas as pd
import networkx as nx
import xlwt
# import graphviz as gz
import pygraphviz as pgv
import os
import DAG


class GUI:
    def __init__(self):
        self.app = QApplication(sys.argv)  # 1.1 获取命令行参数
        # ######### 操作区 ########
        """     create layout      """
        # ### 标题
        self.formLayout = QVBoxLayout()
        # self.formLayout = QHBoxLayout()
        # 1. EXCEL_DAG(HUAWEI)  ->      EXCEL_DAG(SELF)
        self.HUAWEI_TO_SELF_AREA = QFormLayout()
        self.H_TO_S_unit = QWidget()
        self.H_TO_S_unit.setLayout(self.HUAWEI_TO_SELF_AREA)
        # self.Input_Data_HUAWEI    Excel(HUAWEI)_输入            (1) 输入函数
        # self.Output_Data_SELF     Excel(SELF)_输出              (2) 输出函数
        # self.Data_Trans_HTOS      Excel_(HUAWEI)到(SELF)转换    (3) 按钮1 HUAWEI-TO-SELF
        # self.Data_Trans_HTOF      Excel_(HUAWEI)到(Feature)转换 (4) 按钮2 HUAWEI-TO-Feature
        # 1.0 label
        self.HUAWEI_TO_SELF_AREA.addRow(QLabel("(1) DAG Critical Features Abstract"))

        # 1.1 确定输入地址
        self.Excel_HUAWEI_Input_Path = QLineEdit()                            # 输入地址 Param(1.1.1)
        self.Button_Input_HUAWEI = QPushButton('input file (HUAWEI_Excel)')   # 按钮 Param(1.1.2)
        self.Button_Input_HUAWEI.clicked.connect(self.Input_Data_HUAWEI)      # 按钮关联函数
        hlayout = QHBoxLayout()                                               # 水平方向
        hlayout.addWidget(self.Excel_HUAWEI_Input_Path)
        hlayout.addWidget(self.Button_Input_HUAWEI)
        self.HUAWEI_TO_SELF_AREA.addRow("输入Excel(HUAWEI)文件路径:", hlayout)

        # 1.2 确定输出地址
        self.Excel_SELF_Output_Path = QLineEdit()                            # 输出地址 Param(1.2.1)
        self.Button_Output_SELF = QPushButton('output file(SELF_Excel)')    # 按钮 Param(1.2.2)
        self.Button_Output_SELF.clicked.connect(self.Output_Data_SELF)      # 按钮关联函数
        hlayout = QHBoxLayout()                                             # 水平方向
        hlayout.addWidget(self.Excel_SELF_Output_Path)
        hlayout.addWidget(self.Button_Output_SELF)
        self.HUAWEI_TO_SELF_AREA.addRow("输出Excel(SELF)文件夹路径:", hlayout)

        # 1.3 创建执行按钮
        self.Button_SELF = QPushButton('HUAWEI_Transition_SELF_EXCEL_DATA')
        self.Button_SELF.clicked.connect(self.Data_Trans_HTOS)               # 关联函数
        self.HUAWEI_TO_SELF_AREA.addRow(self.Button_SELF)

        # 2. EXCEL_DAG(SELF)    ->      EXCEL_DAG(Feature)
        # self.Input_Data_Self
        # self.Output_Data_Feature
        # self.Data_Trans_STOF
        self.SELF_TO_FEATURE_AREA = QFormLayout()
        self.S_TO_F_unit = QWidget()
        self.S_TO_F_unit.setLayout(self.SELF_TO_FEATURE_AREA)
        # 2.0. label
        self.SELF_TO_FEATURE_AREA.addRow( QLabel("(2) DAG Critical Features Abstract") )
        """
        # 2.1. 创建 self DAG excel 文件：
        self.Excel_SELF_Input_Path = QLineEdit()
        self.Button_Input_SELF = QPushButton('input file (SELF_Excel)')
        self.Button_Input_SELF.clicked.connect(self.Input_Data_Self)                # 关联函数
        hlayout = QHBoxLayout()                                                     # 水平方向
        hlayout.addWidget(self.Excel_SELF_Input_Path)
        hlayout.addWidget(self.Button_Input_SELF)
        self.SELF_TO_FEATURE_AREA.addRow("输入Excel(SELF)文件路径:", hlayout)

        # 2.2 确定输出地址
        self.Excel_Featur_Output_Path = QLineEdit()                                 # 输出地址
        self.Button_Input_Feature = QPushButton('output file(Features_Excel)')      # 按钮
        self.Button_Input_Feature.clicked.connect(self.Output_Data_Feature)         # 按钮关联函数
        hlayout = QHBoxLayout()                                                     # 水平方向
        hlayout.addWidget(self.Excel_Featur_Output_Path)
        hlayout.addWidget(self.Button_Input_Feature)
        self.SELF_TO_FEATURE_AREA.addRow("输出Excel(Feature)文件夹路径:", hlayout)

        # 2.3 创建执行按钮
        self.Button_Feature = QPushButton('Obtain DAGs Critical Features Data')
        self.Button_Feature.clicked.connect(self.Data_Trans_STOF)  # 关联函数
        self.SELF_TO_FEATURE_AREA.addRow(self.Button_Feature)
        """

        # 3. EXCEL_DAG(Feature) ->      DAG_Generator
        self.FEATURE_TO_DAG_Generator_AREA = QVBoxLayout()
        self.F_TO_DG_unit = QWidget()
        self.F_TO_DG_unit.setLayout(self.FEATURE_TO_DAG_Generator_AREA)
        self.FEATURE_TO_DAG_Generator_AREA.addWidget( QLabel("(3) DAG Critical Features list") )

        self.DAG_Feature_AREA = QHBoxLayout()
        self.DF_unit = QWidget()
        self.DF_unit.setLayout(self.DAG_Feature_AREA)
        # 3.1 基本参数
        # "Width", "Connection_Rate", 'Jump_Level'
        self.Sub_Area_Param = QFormLayout()
        self.Sub_Area_unit = QWidget()
        self.Sub_Area_unit.setLayout(self.Sub_Area_Param)
        self.Number_Of_Nodes = QLineEdit()
        self.Sub_Area_Param.addRow("(1.1)DAG的结点数量:", self.Number_Of_Nodes)
        self.Number_Of_Edges = QLineEdit()
        self.Sub_Area_Param.addRow("(1.2)DAG的边数量:", self.Number_Of_Edges)
        self.Number_Of_Levels = QLineEdit()
        self.Sub_Area_Param.addRow("(1.3)DAG的层数量:", self.Number_Of_Levels)
        self.Number_Of_Width = QLineEdit()
        self.Sub_Area_Param.addRow("(1.4)DAG的宽度:", self.Number_Of_Width)
        self.Connection_Rate = QLineEdit()
        self.Sub_Area_Param.addRow("(1.5)DAG的稠密度:", self.Connection_Rate)
        self.Jump_Level = QLineEdit()
        self.Sub_Area_Param.addRow("(1.6)DAG的跳层:", self.Jump_Level)

        self.DAG_Feature_AREA.addWidget( self.Sub_Area_unit )

        # 3.2 shape + Degree 参数
        # "Max_Shape", "Min_Shape", "Ave_Shape", "Std_Shape",
        self.Sub_Area_Param = QFormLayout()
        self.Sub_Area_unit = QWidget()
        self.Sub_Area_unit.setLayout(self.Sub_Area_Param)
        self.Param_Max_Shape = QLineEdit()
        self.Sub_Area_Param.addRow("(2.1)Max_Shape:", self.Param_Max_Shape)
        self.Param_Min_Shape = QLineEdit()
        self.Sub_Area_Param.addRow("(2.2)Min_Shape:", self.Param_Min_Shape)

        self.Param_Max_In_Degree = QLineEdit()
        self.Sub_Area_Param.addRow("(2.3)Max_In_Degree:", self.Param_Max_In_Degree)
        self.Param_Max_Out_Degree = QLineEdit()
        self.Sub_Area_Param.addRow("(2.4)Max_Out_Degree:", self.Param_Max_Out_Degree)
        self.DAG_Feature_AREA.addWidget( self.Sub_Area_unit )

        # 3.3 WCET 参数
        #  "DAG_volume", "Max_WCET", "Min_WCET", "Ave_WCET", "Std_WCET",
        self.Sub_Area_Param = QFormLayout()
        self.Sub_Area_unit = QWidget()
        self.Sub_Area_unit.setLayout(self.Sub_Area_Param)
        # self.Param_DAG_volume = QLineEdit()
        # self.Sub_Area_Param.addRow("(7.1)DAG_volume:", self.Param_DAG_volume)
        self.Param_Max_WCET = QLineEdit()
        self.Sub_Area_Param.addRow("(3.1)Max_WCET:", self.Param_Max_WCET)
        self.Param_Min_WCET = QLineEdit()
        self.Sub_Area_Param.addRow("(3.2)Min_WCET:", self.Param_Min_WCET)
        self.Param_Ave_WCET = QLineEdit()
        self.Sub_Area_Param.addRow("(3.3)Ave_WCET:", self.Param_Ave_WCET)
        self.Param_Std_WCET = QLineEdit()
        self.Sub_Area_Param.addRow("(3.4)Std_WCET:", self.Param_Std_WCET)
        self.DAG_Feature_AREA.addWidget( self.Sub_Area_unit )

        self.FEATURE_TO_DAG_Generator_AREA.addWidget(self.DF_unit)

        self.Sub_Area_Input_Param = QFormLayout()
        self.Sub_Area_Input = QWidget()
        self.Sub_Area_Input.setLayout(self.Sub_Area_Input_Param)
        self.Number_Of_DAGs = QLineEdit()
        self.Sub_Area_Input_Param.addRow("The Number of DAGs:", self.Number_Of_DAGs)
        self.FEATURE_TO_DAG_Generator_AREA.addWidget( self.Sub_Area_Input )

        self.Button_DAG_Generator = QPushButton('DAG_Generator')
        self.Button_DAG_Generator.clicked.connect(self.DAG_Generator)               # 关联函数
        self.FEATURE_TO_DAG_Generator_AREA.addWidget(self.Button_DAG_Generator)
        """
        # 3. EXCEL_DAG(Feature) ->      DAG_Generator
        self.FEATURE_TO_DAG_Generator_AREA = QHBoxLayout()
        self.F_TO_DG_unit = QWidget()
        self.F_TO_DG_unit.setLayout(self.FEATURE_TO_DAG_Generator_AREA)
        """
        # 0. TOTAL
        self.formLayout.addWidget(self.H_TO_S_unit)
        # self.formLayout.addWidget(self.S_TO_F_unit)
        self.formLayout.addWidget(self.F_TO_DG_unit)
        # makespan_unit.setLayout(makespan_area)
        # create window
        self.window = QWidget()
        self.window.resize(600, 130)                                    # 2.1 设置窗口的尺寸 # 宽，高
        center_pointer = QDesktopWidget().availableGeometry().center()  # 3.1 获取屏幕中央坐标,调整窗口在屏幕中央显示
        self.window.move(center_pointer.x(), center_pointer.y())        # 3.2 移动到中央(窗口左上角坐标)
        # print (window. frameGeometry())                               # 3.3 获取窗口坐标
        self.window.setWindowTitle('DAG Critical Features Abstract')
        self.window.setLayout(self.formLayout)
        self.window.show()
        self.app.exec_()

    #   (1) Area HUAWEI TO SELF DATA EXCEL
    def Input_Data_HUAWEI(self):    # Excel(HUAWEI)_输入
        download_path = QFileDialog.getOpenFileName(None)
        self.Excel_HUAWEI_Input_Path.setText(download_path[0])

    def Output_Data_SELF(self):     # Excel(SELF)_输出
        download_path = QFileDialog.getExistingDirectory(None)
        self.Excel_SELF_Output_Path.setText(download_path)

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


    def DAG_Generator(self):
        G = DAG.DAG_Generator()  # step0. 初始化DAG
        Dags_Num = int(self.Number_Of_DAGs.text())
        # ############ MINE ############## #
        Node_Num = int(self.Number_Of_Nodes.text())
        Edge_Num = int(self.Number_Of_Edges.text())
        Critic_Path = int(self.Number_Of_Levels.text())
        Width = int(self.Number_Of_Width.text())
        Connection_Rate = float(self.Connection_Rate.text())

        Max_Shape = int(self.Param_Max_Shape.text())
        Min_Shape = int(self.Param_Min_Shape.text())
        Max_in_degree = int(self.Param_Max_In_Degree.text())
        Max_out_degree = int(self.Param_Max_Out_Degree.text())
        Jump_level = int(self.Jump_Level.text())
        # Jump_Level = int(self.Jump_Level.text())

        # ret_dag_list = G.Main_Workbench('MINE', [Node_Num, Critic_Path, Jump_level, Max_Shape, Min_Shape, Max_in_degree, Max_out_degree], Dags_Num)
        ret_dag_list = G.Main_Workbench("MINE", [Node_Num, Critic_Path, Jump_level, Max_Shape, Min_Shape, Max_in_degree, Max_out_degree, Connection_Rate, Width], Dags_Num)

        analysis_data = []
        for DAG_id, DAG_x in enumerate(ret_dag_list):
            analysis_data.append(DAG_x.graph)
        X = pd.DataFrame(analysis_data)
        X.to_csv( self.Excel_SELF_Output_Path.text() + '/DAG_Generator.csv')
        QMessageBox.question(self.window, "Success", "DAG生成完成！", QMessageBox.Yes)

    def Input_Data_Self(self):
        pass
 
    def Output_Data_Feature(self):
        pass
 
    def Data_Trans_STOF(self):
        pass
    
    def Input_Data_Self_Inject(self):           # 输入 SELF自行DAG格式的 EXCEL
        download_path = QFileDialog.getOpenFileName(None)
        self.edit_self_input_path.setText(download_path[0])
        print( download_path )



    # todo 利用excel表格数据生成DAG
    def Data_transition(self):
        print("Hello World")
        output_path = self.edit_parallism_output_path.text()
        input_path = self.edit_parallism_input_path.text()

        if (output_path == '') or (not os.path.exists(input_path)) or (".xls" not in input_path) or (".xlsx" not in input_path):
            QMessageBox.critical(self.window,  '错误',  "输入文件不存在", QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False

        if (output_path == '') or (not os.path.exists(input_path)) or (input_path == output_path):
            QMessageBox.critical(self.window, '错误', "输出文件格式不正确", QMessageBox.Cancel | QMessageBox.Close, QMessageBox.Cancel)
            return False

        DAG_list = []
        # todo 1.录入DAG数据
        with pd.ExcelFile(input_path) as data:
            all_sheet_names = data.sheet_names  # 获取所有sheet名字；
            for DAG_ID in all_sheet_names:
                temp_DAG = nx.DiGraph()
                temp_DAG.graph['DAG_ID'] = DAG_ID
                df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
                # title_list = df.dtypes
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
        # todo 2 生成DAG图
        for DAG_x in DAG_list:
            gvd = pgv.AGraph(directed=True, rankdir="LR")
            for node_x in DAG_x.nodes(data=True):
                temp_label = ''
                temp_label += str(node_x[0]) + '\n'
                temp_label += 'Node_ID:' + str(node_x[1]['Node_ID']) + '\n'
                temp_label += 'WCET:' + str(node_x[1]['WCET']) + '\n'
                temp_label += 'Prio:' + str(node_x[1]['Prio']) + '\n'
                gvd.add_node(node_x[0], label=temp_label)
                # dot.node('%s' % node_x[0], temp_label)
            for edge_x in DAG_x.edges(data=True):
                gvd.add_edge(edge_x[0], edge_x[1])

            gvd.layout(prog='dot')          # 要有，否则会出现log文件
            gvd.draw(path=output_path + '/' + DAG_x.graph['DAG_ID'] + '.png', format='png')

            if not os.path.exists(output_path):
                os.makedirs(output_path)

        # todo 3.抽象DAG特性
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
            self.dag_param_critical_update(DAG_x, x)
            for i, feature_i in enumerate(Features_Tytle):
                worksheet.write(i, x + 1, DAG_x.graph[feature_i])
        workbook.save(output_path + '/DAG_Features.xls')
        QMessageBox.question(self.window, "Success", "DAG特性抽象完成！", QMessageBox.Yes)
        return True

    #####################################
    #   Section_5: DAG的关键参数分析
    #####################################
    def dag_param_critical_update(self, DAG_obj, i):        # (1)DAG_obj:DAG对象;     (2)i:DAG_ID
        """, worksheet"""
        # #### 0.DAG检测及基本参数 #### #
        assert format(nx.is_directed_acyclic_graph(DAG_obj))
        DAG_obj.graph['DAG_ID'] = str(i)
        DAG_obj.graph['Number_Of_Nodes'] = DAG_obj.number_of_nodes()
        DAG_obj.graph['Number_Of_Edges'] = DAG_obj.number_of_edges()
        # section1. 获取DAG的结构相关参数
        # #### 1.关键路径 #### #
        # node_list = nx.dag_longest_path(self.G, weight='weight')  # 关键路径
        # print('关键路径：{0}'.format(node_list))
        # #### 2.最短路径 #### #
        # shortest_path = list(nx.all_shortest_paths(self.G, 0, self.G.number_of_nodes() - 1, weight='weight'))
        # print('DAG的最短路径{0}条：'.format(len(shortest_path)))
        # [print(path) for path in shortest_path]

        # #### 3.获取拓扑分层 shape #### #
        # 3.1 正向shape
        rank_list = [sorted(generation) for generation in nx.topological_generations(DAG_obj)]
        for l, rank_l in enumerate(rank_list):
            for rank_x in rank_l:
                DAG_obj.nodes[rank_x]['rank'] = l
        rank_num_list = [len(x) for x in rank_list]

        DAG_obj.graph['Number_Of_Level'] = len(rank_num_list)

        DAG_obj.graph['Shape_List'] = rank_num_list
        DAG_obj.graph['Max_Shape'] = max(rank_num_list)
        DAG_obj.graph['Min_Shape'] = min(rank_num_list)
        DAG_obj.graph['Ave_Shape'] = np.mean(rank_num_list)
        DAG_obj.graph['Std_Shape'] = np.std(rank_num_list)

        # 3.2 反向shape
        re_rank_list = [sorted(generation) for generation in nx.topological_generations(nx.DiGraph.reverse(DAG_obj))]
        re_rank_list.reverse()
        re_rank_num_list = [len(x) for x in re_rank_list]
        DAG_obj.graph['Re_Shape_List'] = re_rank_num_list
        DAG_obj.graph['Max_Re_Shape'] = max(re_rank_num_list)
        DAG_obj.graph['Min_Re_Shape'] = min(re_rank_num_list)
        DAG_obj.graph['Ave_Re_Shape'] = np.mean(re_rank_num_list)  # ave-shape；
        DAG_obj.graph['Std_Re_Shape'] = np.std(re_rank_num_list)   # std-shape；

        # #### 5.antichains #### #  # "Width"
        anti_chains_list = list(nx.antichains(DAG_obj, topo_order=None))
        anti_chains_num_list = [len(x) for x in anti_chains_list]
        DAG_obj.graph['Width'] = max(anti_chains_num_list)

        # #### 6.degree #### #
        degree_list = [nx.degree(DAG_obj, self_node[0]) for self_node in DAG_obj.nodes(data=True)]
        DAG_obj.graph['Max_Degree'] = max(degree_list)  # max-degree；
        DAG_obj.graph['Min_Degree'] = min(degree_list)  # max-degree；
        DAG_obj.graph['Ave_Degree'] = np.mean(degree_list)  # ave-degree；
        DAG_obj.graph['Std_Degree'] = np.std(degree_list)  # std-degree；

        degree_in_list = [DAG_obj.in_degree(self_node[0]) for self_node in DAG_obj.nodes(data=True)]
        DAG_obj.graph['Max_In_Degree'] = max(degree_in_list)  # max-degree；
        DAG_obj.graph['Min_In_Degree'] = min(degree_in_list)  # max-degree；
        DAG_obj.graph['Ave_In_Degree'] = np.mean(degree_in_list)  # ave-degree；
        DAG_obj.graph['Std_In_Degree'] = np.std(degree_in_list)  # std-degree；

        degree_out_list = [DAG_obj.out_degree(self_node[0]) for self_node in DAG_obj.nodes(data=True)]
        DAG_obj.graph['Max_Out_Degree'] = max(degree_out_list)        # max-degree；
        DAG_obj.graph['Min_Out_Degree'] = min(degree_out_list)        # max-degree；
        DAG_obj.graph['Ave_Out_Degree'] = np.mean(degree_out_list)    # ave-degree；
        DAG_obj.graph['Std_Out_Degree'] = np.std(degree_out_list)     # std-degree；

        # #### 7.DAG的稠密度 Density  #### #
        Dag_density = (2 * DAG_obj.number_of_edges()) / (DAG_obj.number_of_nodes() * (DAG_obj.number_of_nodes()-1))
        DAG_obj.graph['Connection_Rate'] = Dag_density

        # #### 8.DAG最差执行时间list  #### #
        WCET_list = [x[1]['WCET'] for x in DAG_obj.nodes.data(data=True)]
        DAG_obj.graph['DAG_volume'] = int(np.sum(WCET_list))
        DAG_obj.graph['Max_WCET'] = float(max(WCET_list))
        DAG_obj.graph['Min_WCET'] = float(min(WCET_list))
        DAG_obj.graph['Ave_WCET'] = float(np.mean(WCET_list))
        DAG_obj.graph['Std_WCET'] = float(np.std(WCET_list))

        # #### 9.最大跳层  #### #
        Edges_Jump_List = [DAG_obj.nodes[x[1]]['rank'] - DAG_obj.nodes[x[0]]['rank'] for x in DAG_obj.edges.data()]
        DAG_obj.graph['Jump_Level'] = max(Edges_Jump_List)


if __name__ == '__main__':
    # # 创建应用
    # window_application = QApplication(sys.argv)
    # # 设置登录窗口
    # login_ui = LoginDialog()
    # # 校验是否验证通过
    # if login_ui.exec_() == QDialog.Accepted:
    G = GUI()
