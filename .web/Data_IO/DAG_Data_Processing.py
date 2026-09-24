#!/usr/bin/python3
# -*- coding: utf-8 -*-

# from . import DAG_Features_Analysis as DFA
# from . import DAG_WCET_Config as DWC
import graphviz as gz
import networkx as nx
import pandas as pd
import datetime
import os
# import xlwt
# import numpy as np


output_type_list = ['PDF', 'PNG', 'CSV', 'DAT', 'GV', 'GPLCKLE']


def Exam_Data_Output(DAG_list, output_type, address):
    if output_type == 'PIC':  # include pdf and png
        __exam_pic_Output(DAG_list, address)
    elif output_type == 'CSV':
        __exam_xlsx_Self_Output(DAG_list, address)
    elif output_type == 'CRI':      # dag critical list
        __exam_critical_Output(DAG_list, address)
    elif output_type == 'HAISI':
        __exam_xlsx_HAISI_Output(DAG_list, address)
    elif output_type == 'ALL':  # include 'PIC' , 'CSV' , 'CRI'
        __exam_xlsx_ALL_Output(DAG_list, address)
    else:
        pass


def __exam_xlsx_ALL_Output(DAG_list, address):
    os.makedirs(address, mode=0o777, exist_ok=True)
    for dag_x in DAG_list:
        # ###################### (1)PIC ###################### #
        file_addr_name = address + str(dag_x.graph['DAG_ID'])
        dot = gz.Digraph(node_attr={'shape': 'box'}, edge_attr={'labeldistance': "10.5"}, format="png")
        dot.attr(rankdir='LR')
        for node_x in dag_x.nodes(data=True):
            temp_label = 'Node_ID:{0}\nWCET:{1}\n'.format(str(node_x[1]['Node_ID']), str(node_x[1]['WCET']))
            temp_node_dict = node_x[1]
            if 'critic' in temp_node_dict:
                if node_x[1]['critic']:
                    color_t = 'red'
                else:
                    color_t = 'green'
            else:
                color_t = 'black'
            dot.node('%s' % node_x[0], temp_label, color=color_t)
        for edge_x in dag_x.edges():
            dot.edge('%s' % edge_x[0], '%s' % edge_x[1])
        dot.render(filename=file_addr_name, format="png", view=False)  # 1.generate pdf file
        dot.render(filename=file_addr_name, format="pdf", view=False)  # 2.generate pdf file

        # ###################### (2)CSV ###################### #
        df = pd.DataFrame({node_x[0]: node_x[1] for node_x in dag_x.nodes(data=True)},
                          index=['Node_Index', 'Node_ID', 'Edges_List', 'BCET', 'ACET', 'WCET', 'AET', 'Group', 'critic', 'PT'],
                          columns=dag_x.nodes()).T
        df.to_csv(file_addr_name + '.csv')                              # 3.generate csv file
        # ###################### (3)CRI ###################### #
        df = pd.DataFrame({dag_x.graph['DAG_ID']: dag_x.graph},
                          index=["DAG_ID", "Number_Of_Nodes", "Number_Of_Edges", "Max_Shape", "Min_Shape", "Ave_Shape",
                                 "Std_Shape", "Max_Re_Shape", "Min_Re_Shape", "Ave_Re_Shape", "Std_Re_Shape",
                                 "Max_Degree", "Min_Degree", "Ave_Degree", "Std_Degree", "Max_In_Degree",
                                 "Min_In_Degree", "Ave_In_Degree", "Std_In_Degree", "Max_Out_Degree", "Max_Out_Degree",
                                 "Ave_Out_Degree", "Std_Out_Degree", "Width", "Connection_Rate", "DAG_volume"],
                          columns=[dag_x.graph['DAG_ID']])
        df.to_csv(file_addr_name + 'Critical' + '.csv')                 # 4.generate critical csv file


#########################################
# OUTPUT PDF and PNG
#########################################
def __exam_pic_Output(DAG_list, address):
    temp_address = address + 'PIC/'
    os.makedirs(temp_address, mode=0o777, exist_ok=True)
    for dag_x in DAG_list:
        dot = gz.Digraph()
        dot.attr(rankdir='LR')
        for node_x in dag_x.nodes(data=True):
            # temp_label = 'Node_ID:{0}\nrank:{1}\nWCET:{2}\nGroup:{3}\n'.format(str(node_x[1]['Node_ID']),str(node_x[1]['rank']),str(node_x[1]['WCET']),str(node_x[1]['Group']))
            # temp_label = 'Node_ID:{0}\nrank:{1}\nWCET:{2}\n'.format(str(node_x[1]['Node_ID']),str(node_x[1]['rank']),str(node_x[1]['WCET']))
            temp_label = '{0}_{1}\nWCET:{2}\nPrio:{3}\nlevel:{4}\n'.format(str(node_x[1]['JobTypeID']),
                                                                str(node_x[1]['Node_Index']),
                                                                str(int(node_x[1]['WCET'])),
                                                                str(node_x[1]['Prio']),
                                                                str(int(node_x[1]['rank'])))
            # temp_label = '{0}_{1}\nWCET:{2}\nET:{3}\n'.format(str(node_x[1]['Node_ID']),
            #                                                   str(node_x[1]['Node_Index']),
            #                                                   str(node_x[1]['WCET']),
            #                                                   str(node_x[1]['ET']))
            temp_node_dict = node_x[1]
            if 'critic' in temp_node_dict:
                if node_x[1]['critic']:
                    color_t = 'red'
                else:
                    color_t = 'green'
            else:
                color_t = 'black'
            dot.node('%s' % node_x[0], temp_label, color=color_t, shape='box')
        for edge_x in dag_x.edges():
            dot.edge('%s' % edge_x[0], '%s' % edge_x[1])
        dot.render(filename=temp_address + str(dag_x.graph['DAG_ID']), format="png", view=False)
        dot.render(filename=temp_address + str(dag_x.graph['DAG_ID']), format="pdf", view=False)


def __exam_xlsx_Self_Output(DAG_list, address):
    temp_address = address + 'CSV/'
    os.makedirs(temp_address, mode=0o777, exist_ok=True)
    # title_list = ['Node_Index', 'Node_ID', 'Succ_Nodes', 'BCET', 'ACET', 'WCET', 'Group']
    title_list = ['Node_Index', 'Node_ID', 'Edges_List', 'BCET', 'ACET', 'WCET', 'Group', 'critic']
    writer = pd.ExcelWriter(temp_address + '2022-12-28(1)-experiment.xlsx')
    for dag_x in DAG_list:
        temp_data = {}
        node_id_list = []
        for node_x in dag_x.nodes(data=True):
            temp_data[node_x[0]] = node_x[1]
            node_id_list.append(node_x[0])
        df = pd.DataFrame(temp_data, index=title_list, columns=node_id_list)
        df = df.T
        df.to_csv(temp_address + str(dag_x.graph['DAG_ID']) + '.csv')

        df.to_excel(writer, sheet_name=str(dag_x.graph['DAG_ID']), index=False, header=True)
    writer.save()


def __exam_critical_Output(DAG_list, address):
    temp_address = address + 'CRI/'
    os.makedirs(temp_address, mode=0o777, exist_ok=True)
    excel_title = ["DAG_ID", "Number_Of_Nodes", "Number_Of_Edges",
                   "Max_Shape", "Min_Shape", "Ave_Shape", "Std_Shape",
                   "Max_Re_Shape", "Min_Re_Shape", "Ave_Re_Shape", "Std_Re_Shape",
                   "Max_Degree", "Min_Degree", "Ave_Degree", "Std_Degree",
                   "Max_In_Degree", "Min_In_Degree", "Ave_In_Degree", "Std_In_Degree",
                   "Max_Out_Degree", "Max_Out_Degree", "Ave_Out_Degree", "Std_Out_Degree",
                   "Width", "Connection_Rate", "DAG_volume"]
    node_id_list = [dag_x.graph['DAG_ID'] for dag_x in DAG_list]
    temp_data = {dag_x.graph['DAG_ID']: dag_x.graph for dag_x in DAG_list}
    df = pd.DataFrame(temp_data, index=excel_title, columns=node_id_list)
    df = df.T
    df.to_csv(temp_address + 'Critical' + '.csv')
    # if isinstance(temp_data, float):
    #     temp_data = round(temp_data, 2)


def __exam_xlsx_HAISI_Output(DAG_list, address):
    temp_address = address + 'HAISI/'
    os.makedirs(temp_address, mode=0o777, exist_ok=True)
    excel_title = ['JobTypeID', 'InstanceNumber', 'TriggerJobTypeIDSet', 'ExecutionTime', 'QoS', 'CoreType']
    for dag_x in DAG_list:
        Temp_JobType_Num = dag_x.graph['JobType_Num']
        temp_dict = {job_id_x:[] for job_id_x in range(1, Temp_JobType_Num + 1)}
        for node_x in dag_x.nodes(data=True):
            temp_dict[node_x[1]['JobTypeID']].append(node_x)
        temp_df_dict = {}
        QoS_list = { job_id_x: min([node_xx[1]['Prio'] for node_xx in temp_dict[job_id_x]]) for job_id_x in range(1, Temp_JobType_Num + 1) }    # 最小优先级
        QoS_list = sorted(QoS_list.items(), key=lambda x: x[1])
        QoS_Dict = { QoS_list[job_id_x][0]: job_id_x for job_id_x in range(Temp_JobType_Num)}
        for job_id_x in range(1, Temp_JobType_Num + 1):
            TriggerJobList = [str(dag_x.nodes[temp_node_x_x]["JobTypeID"]) for temp_node_x in temp_dict[job_id_x] for temp_node_x_x in list(dag_x.successors(temp_node_x[0]))]
            ExecutionTimeList = list(set([temp_node_x[1]['WCET'] for temp_node_x in temp_dict[job_id_x] ]))
            # assert len(ExecutionTimeList) == 1
            temp_df_dict[job_id_x] = {'JobTypeID': job_id_x,
                                      'InstanceNumber': len(temp_dict[job_id_x]),
                                      'TriggerJobTypeIDSet': ','.join(list(set(TriggerJobList))),
                                      'ExecutionTime': ExecutionTimeList[0],
                                      'QoS': QoS_Dict[job_id_x],
                                      'CoreType': ''}
        df = pd.DataFrame(temp_df_dict, index=excel_title)
        df = df.T
        df.to_csv(temp_address + dag_x.graph['DAG_ID'] + '.csv', index=False)


if __name__ == "__main__":
    G = nx.DiGraph()
    G.add_node(0, Node_Index=1, JobTypeID=1, Node_ID='0', Succ_Nodes=[1], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(1, Node_Index=2, JobTypeID=2, Node_ID='1', Succ_Nodes=[2, 3, 4, 5, 6, 7, 8], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(2, Node_Index=3, JobTypeID=3, Node_ID='2', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(3, Node_Index=4, JobTypeID=4, Node_ID='3', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(4, Node_Index=5, JobTypeID=5, Node_ID='4', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(5, Node_Index=6, JobTypeID=6, Node_ID='5', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(6, Node_Index=7, JobTypeID=7, Node_ID='6', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(7, Node_Index=8, JobTypeID=8, Node_ID='7', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(8, Node_Index=9, JobTypeID=9, Node_ID='8', Succ_Nodes=[9], BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.add_node(9, Node_Index=10, JobTypeID=10, Node_ID='9', Succ_Nodes=[],  BCET=1, ACET=1, WCET=1, rank=1, Group=1, Prio=1)
    G.graph['JobType_Num'] = len(list(set([node_x[1]['JobTypeID'] for node_x in G.nodes(data=True)])))
    G.add_edges_from([(0, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
                      (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9)])

    # ############ WCET_Config ############## #
    # DWC.WCET_Config(G, 'Uniform', Virtual_node=True, a=10000, b=100)
    # ############ WCET_Config ############## #
    # DFA.dag_param_critical_update(G, 'test')

    # G.graph['Nodes_Number'] = 'test'

    # time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H=%M=%S')
    # output_path = './Result_data/test/' + time_str + '/'

    # Exam_Data_Output([G], 'PIC', output_path)       # 输出图像
    # Exam_Data_Output([G], 'CSV', output_path)       # 输出数据
    # Exam_Data_Output([G], 'CRI', output_path)       # 输出关键参数
    # Exam_Data_Output([G], 'HAISI', output_path)     # 输出关键参数
    # Exam_Data_Output([G], 'M1_S2_C2', output_path)

    # print( nx.average_degree_connectivity(G) )
    # print( nx.degree(G) )  # 计算图的密度，其值为边数m除以图中可能边数（即n(n - 1) / 2）
    # ###节点度中心系数。通过节点的度表示节点在图中的重要性，默认情况下会进行归一化，其值表达为节点度d(u) 除以n - 1（其中n - 1就是归一化使用的常量）。这里由于可能存在循环，所以该值可能大于1.
    # print( nx.degree_centrality(G) )
    # #### 节点距离中心系数。通过距离来表示节点在图中的重要性，一般是指节点到其他节点的平均路径的倒数，这里还乘以了n - 1。该值越大表示节点到其他节点的距离越近，即中心性越高。
    # print( nx.closeness_centrality(G) )
    # ### 节点介数中心系数。在无向图中，该值表示为节点作占最短路径的个数除以((n - 1)(n - 2) / 2)；在有向图中，该值表达为节点作占最短路径个数除以((n - 1)(n - 2))。
    # print( nx.betweenness_centrality(G) )
    # ### 图或网络的传递性。即图或网络中，认识同一个节点的两个节点也可能认识双方，计算公式为3 * 图中三角形的个数 / 三元组个数（该三元组个数是有公共顶点的边对数，这样就好数了）。
    # print( nx.transitivity(G) )
    # ### 图或网络中节点的聚类系数。计算公式为：节点u的两个邻居节点间的边数除以((d(u)(d(u) - 1) / 2)。
    # print( nx.clustering(G) )
    # ### 计算最小覆盖链
    # H = G.to_undirected()  # 有向图转化成无向图-方法1
    # H = nx.Graph(G)  # 有向图转化成无向图-方法2
    # F = H.to_directed()  # 无向图转化成有向图-方法1
    # F = nx.DiGraph(H)  # 无向图转化成有向图-方法2
    # print(nx.min_edge_cover(H))


