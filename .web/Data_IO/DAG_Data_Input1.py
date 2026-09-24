#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import math
import copy
import numpy as np
import pandas as pd
import networkx as nx
# from itertools import combinations
from random import random, sample, uniform, randint, choice


######################
# Manual_Generation
######################
def Manual_Input(File_Type, Address_List):
    dag_list = []
    for address_x in Address_List:
        if File_Type == 'XLSX':
            dag_list += __User_DAG_Inject(address_x)
        elif File_Type == 'CSV':
            dag_list += __User_DAG_SCV_Input(address_x)
        elif File_Type == 'HAISI':
            dag_list += __User_DAG_HAISI_Input(address_x)
        elif File_Type == 'FEATURE':
            dag_list += __User_DAG_Feature_Input(address_x)
        else:
            pass

    for dag_x in dag_list:
        for node_x in dag_x.nodes(data=True):
            node_x[1]['Node_Indes'] = node_x[0]
    return dag_list


def __User_DAG_Inject(address_x):
    with pd.ExcelFile(address_x) as data:
        all_sheet_names = data.sheet_names
        DAG_list = []
        for DAG_ID in all_sheet_names:
            temp_DAG = nx.DiGraph()
            temp_DAG.graph['DAG_ID'] = DAG_ID
            df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
            title_list = df.dtypes
            # xxxx = df.columns
            for row in df.index:
                temp_DAG.add_node(df.loc[row]['Node_Index'], DAG=temp_DAG)
                for title_id, data_type in title_list.items():
                    row_data = df.loc[row][title_id]
                    if title_id == 'Edges_List':
                        if type(row_data) in [float, np.float64]:
                            continue
                        row_data = row_data.split(';')
                        for edge_data in row_data:
                            if edge_data == '':
                                continue
                            edge_list = edge_data[1:-1].split(',')
                            temp_DAG.add_edge(int(edge_list[0]), int(edge_list[1]))
                    else:
                        temp_DAG.nodes[df.loc[row]['Node_Index']][title_id] = row_data
            DAG_list.append(temp_DAG)
    return DAG_list


def __User_DAG_SCV_Input(address_x):
    temp_data = pd.read_csv(address_x, index_col=None, na_values=["NA"])
    temp_DAG = nx.DiGraph()
    title_list = temp_data.dtypes
    for row in temp_data.index:
        temp_DAG.add_node(temp_data.loc[row]['Node_Index'])
        for title_id, data_type in title_list.items():
            row_data = temp_data.loc[row][title_id]
            temp_DAG.nodes[temp_data.loc[row]['Node_Index']][title_id] = row_data
    for row in temp_data.index:
        row_data = temp_data.loc[row]['Edges_List']
        if type(row_data) == float:
            continue
        row_data = row_data.strip('[]')
        row_data = row_data.split(';')
        for edge_data in row_data:
            if edge_data == '':
                continue
            edge_list = edge_data[1:-1].split(',')
            temp_DAG.add_edge(int(edge_list[0]), int(edge_list[1]))
    return [temp_DAG]


def __User_DAG_HAISI_Input(address_x):
    with pd.ExcelFile(address_x) as data:
        # Sheet(1) : DAG_Instance_List
        df = pd.read_excel(data, 'DAG_Instance', index_col=None, na_values=["NA"], header=3)
        # df.loc[:, ['DAGType', 'DAGTypeID']] = df.loc[:, ['DAGType', 'DAGTypeID']].fillna(method='ffill')  # axis：0为垂直，1为水平
        df.loc[:, ['DAGType', 'DAGTypeID']] = df.loc[:, ['DAGType', 'DAGTypeID']].ffill()  # axis：0为垂直，1为水平

        # df.loc[:, ['DAGType', 'DAGTypeID']] = df.loc[:, ['DAGType', 'DAGTypeID']].fillna()  # axis：0为垂直，1为水平

        DAG_ID_list = list(set(df.loc[:, 'DAGType']))
        DAG_Obj_dict = {}
        for dag_id_x in DAG_ID_list:
            temp_DAG = nx.DiGraph()
            temp_DAG.graph['DAG_ID'] = dag_id_x
            DAG_Obj_dict[dag_id_x] = temp_DAG
        DAG_dict = df.T.to_dict(orient='dict')
        DAG_edges_dict = {DAG_ID_x: [] for DAG_ID_x in DAG_ID_list}
        for _, dag_data_x in DAG_dict.items():
            temp_dag = DAG_Obj_dict[dag_data_x['DAGType']]
            temp_dag.graph['DAGType'] = dag_data_x['DAGType']
            temp_dag.graph['DAG_ID'] = dag_data_x['DAGType']
            DAG_edges_dict[dag_data_x['DAGType']].append((dag_data_x['JobTypeID'], dag_data_x['PublishJob']))
            for _ in range(dag_data_x['JobInstNum']):
                NODE_ID = temp_dag.number_of_nodes()
                temp_dag.add_node(NODE_ID, JobTypeID=dag_data_x['JobTypeID'], DAG=temp_dag, Node_Index=NODE_ID,
                                  JobID=dag_data_x['JobID'], Node_ID=dag_data_x['JobID'],
                                  Qos=dag_data_x['Qos'], WCET=dag_data_x['JobCycle'],
                                  JobCycle=dag_data_x['JobCycle'], PublishJob=dag_data_x['PublishJob'])
        for dag_id, dag_edge_list in DAG_edges_dict.items():
            dag_oo = DAG_Obj_dict[dag_id]
            for (edge_p, edge_s) in dag_edge_list:
                if type(edge_s) == str:
                    temp_edge_list = edge_s.split(';')
                    for temp_edge_s_list in temp_edge_list:
                        if len(temp_edge_s_list) == 0:
                            continue
                        temp_edge_s_list = re.split('\(|\)|\:', temp_edge_s_list)
                        if len(temp_edge_s_list) > 1:
                            for p_node_x in [node_x for node_x in dag_oo.nodes(data=True) if node_x[1]['JobTypeID'] == edge_p]:  # 遍历所有同ID的前驱
                                s_node_list = sample([node_x for node_x in dag_oo.nodes(data=True) if node_x[1]['JobTypeID'] == temp_edge_s_list[0] and
                                                             len([self_nx for self_nx in list(dag_oo.predecessors(node_x[0])) if dag_oo.nodes[self_nx]['JobTypeID'] == p_node_x[1]['JobTypeID']]) < int(temp_edge_s_list[1])]
                                                            , k=int(temp_edge_s_list[2]))
                                for s_node_x in s_node_list:
                                    dag_oo.add_edge(p_node_x[0], s_node_x[0])
                        else:
                            for p_node_x in [node_x for node_x in dag_oo.nodes(data=True) if node_x[1]['JobTypeID'] == edge_p]:
                                for s_node_x in [node_x for node_x in dag_oo.nodes(data=True) if node_x[1]['JobTypeID'] == temp_edge_s_list[0]]:
                                    dag_oo.add_edge(p_node_x[0], s_node_x[0])
        # Sheet(2) : DAG_Type_List
        df = pd.read_excel(data, 'DAG_Type', index_col=None, na_values=["NA"], header=1)
        # df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']] = df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']].fillna(method='ffill')  # axis：0为垂直，1为水平
        df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']] = df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']].ffill()  # axis：0为垂直，1为水平

        # print(df)
        all_dag_list = []
        for index, row in df.iterrows():
            temp_dag = copy.deepcopy(DAG_Obj_dict[row['DAGType']])
            temp_dag.graph['DAGType'] = row['DAGType']
            temp_dag.graph['DAGTypeID'] = row['DAGTypeID']
            temp_dag.graph['DAGInstID'] = row['DAGInstID']
            min_r, max_r = row['Random range'][:-1].split('~')
            # temp_dag.graph['Arrive_time'] = float(row['DAGsubmitOffset']) * float(row['SlotLen']) * random.uniform(float(min_r), float(max_r)) / 100
            temp_dag.graph['Arrive_time'] = float(row['DAGsubmitOffset']) * float(row['SlotLen']) * (1 + uniform(-float(max_r), float(max_r)) / 100)
            all_dag_list.append(temp_dag)
    return all_dag_list


def __User_DAG_Feature_Input(address_x):
    with pd.ExcelFile(address_x) as data:
        all_sheet_names = data.sheet_names
        DAG_Feature_list = []
        for DAG_ID in all_sheet_names:
            df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
            DAG_Feature_list.append(np.array(df))
    return DAG_Feature_list


def Dynamic_Generalization(param_dict):
    # if Dynamic_type == 'Haisi':
    return __dynamic_haisi(param_dict)
    # else:
    #     pass


def __dynamic_haisi(param_dict):
    jr_lo = param_dict['jr_rank'][0]
    jr_up = param_dict['jr_rank'][1]
    arrive_time = param_dict['AT']
    ret_dag_list = copy.deepcopy(param_dict['DAGs'])

    for dag_x in ret_dag_list:
        # (1.1) 结点执行时长波动；
        for node_x in dag_x.nodes(data=True):
            node_x[1]['WCET'] = node_x[1]['WCET'] * (1 + choice([1, -1]) * uniform(jr_lo, jr_up))
        # (1.2) 到达时间抖动
        dag_x.graph['Arrive_time'] = randint(0, arrive_time)

    return ret_dag_list


def __General_Dynamic_Generalization(tDAG, jitter_interval=(0.0, 0.0), arrive_time=0, flow_num=1, minshape=1):
    dag_len = tDAG.graph['Number_Of_Level']
    jr_do, jr_up = jitter_interval
    maxshape = randint(minshape, dag_len)
    # (1.1) 流数变化
    ret_dag_list = [copy.deepcopy(tDAG) for _ in range(flow_num)]

    for ret_dag_x in ret_dag_list:
        # (1.2) 到达时间抖动
        ret_dag_x.graph['Arrive_time'] = randint(0, arrive_time)
        # (1.3) 层数变化
        rn_list = [nx[0] for nx in ret_dag_x.nodes(data=True) if nx[1]['rank'] >= maxshape]
        for rnx in rn_list:
            ret_dag_x.remove_node(rnx)
        # (1.4) 分支结点变化
        rn_list = [nx[0] for nx in ret_dag_x.nodes(data=True) if nx[1]['CNode'] and random() > 0.5]
        for rnx in rn_list:
            ret_dag_x.remove_node(rnx)
        # (1.5) 执行时间抖动
        for node_x in ret_dag_x.nodes(data=True):
            node_x[1]['WCET'] = node_x[1]['WCET'] * (1 + choice([1, -1]) * uniform(jr_do, jr_up))

    return ret_dag_list


# if __name__ == "__main__":
#     All_DAG_list = Algorithm_input('MINE',{'DAG_Num': 10, 'Node_Num': 37, 'Critic_Path': 7, 'Width': 15,
#                                            'Jump_level': 1, 'Conn_ratio': 0.08859, 'Max_Shape': 15,'Min_Shape': 1,
#                                            'Max_in_degree': 15, 'Max_out_degree': 5})
#
#
#     pass
#     """
#         # ############ Manual ############## #
#     # ### (1) CSV
#     # All_DAG_list = Manual_Input('CSV', ['./Exam_data/csv_data/exam1/' + f_x for f_x in ['1.csv', '2.csv', '3.csv']])
#     # ### (2) HAISI
#     # All_DAG_list = Manual_Input('HAISI', ['./Exam_data/haisi_data/DAG1.xlsx'])
#
#     # ############ Algorithm ############## #
#     # ['ERDOS_GNM','ERDOS_GNP', 'LAYER_BY_LAYER','FANIN_FANOUT', 'RANDOM_ORDERS', 'MINE']
#     # ### (1) MINE
#     # dag - 1
#     # All_DAG_list = Algorithm_input('MINE',
#     #                                {'DAG_Num': 1, 'Node_Num': 48, 'Critic_Path': 10, 'Width': 16,
#     #                                 'Jump_level': 7, 'Conn_ratio': 0.06383, 'Max_Shape': 11,
#     #                                 'Min_Shape': 1, 'Max_in_degree': 11, 'Max_out_degree': 7})
#     # MAX_WCET =292952
#     # MIN_WCET =1500
#
#     # dag - 2
#     # All_DAG_list = Algorithm_input('MINE',
#     #                                {'DAG_Num': 10, 'Node_Num': 15, 'Critic_Path': 4, 'Width': 11,
#     #                                 'Jump_level': 1, 'Conn_ratio': 0.22857, 'Max_Shape': 11,
#     #                                 'Min_Shape': 1, 'Max_in_degree': 11, 'Max_out_degree': 7})
#     # MAX_WCET =327388
#     # MIN_WCET =1500
#     # dag - 3
#
#     MAX_WCET = 264088
#     MIN_WCET = 3032
#
#     # ### (2) ERDOS_GNM
#     # All_DAG_list = Algorithm_input('ERDOS_GNM', {'DAG_Num': 10, 'Node_Num': 10, 'Edge_Num': 20})
#     # ### (3) ERDOS_GNP
#     # All_DAG_list = Algorithm_input('ERDOS_GNP',  {'DAG_Num': 10, 'Node_Num': 10, 'Edge_Pro': 0.3})
#
#     for dag_id, dag_obj in enumerate(All_DAG_list):
#         # ############ WCET_Config ############## #
#         DWC.WCET_Config(dag_obj, 'Uniform', Virtual_node=True, a=264088, b=3032)
#         # ############ Critical_Param_Config ############## #
#         DFA.dag_param_critical_update(dag_obj, dag_id)
#
#     # ############ Data output ############## #
#     time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H=%M=%S')
#     output_path = './Result_data/test/' + time_str + '/'
#
#     DDP.Exam_Data_Output(All_DAG_list, 'PIC', output_path)     # 输出图像
#     DDP.Exam_Data_Output(All_DAG_list, 'CSV', output_path)     # 输出数据
#     DDP.Exam_Data_Output(All_DAG_list, 'CRI', output_path)     # 输出关键参数
#     # DDP.Exam_Data_Output(All_DAG_list, 'HAISI', output_path)   # 输出关键参数
#     """
#
#
#     # #### Transitive reduction Function #### #
#     #   param:  matrix: Adjacency Matrix
#     #   return: A matrix that has been reduced in transitive

# #### DAG generator FLOW 算法  #### #
# def __gen_flow_single(Algorithm_param_dict):
#     Flow_set = Algorithm_param_dict['Flow_set']
#     flow_num = Algorithm_param_dict['flow_num']
#     arrival_interval = Algorithm_param_dict['arrival_interval']
#     WCET_interval_max = Algorithm_param_dict['WCET_interval']
#     DAG_num = Algorithm_param_dict['DAG_Num']
#     ret_DAGs_list = []
#     for DAG_num_id in range(DAG_num):
#         temp_flow_set = [copy.deepcopy(sample(Flow_set, 1)[0]) for _ in range(flow_num)]
#         temp_dag, source_node_num, sink_node_num = DPC.DAG_list_merge(temp_flow_set)
#         # DFA.dag_critical_path_new(temp_dag)
#         # DPC.Priority_Config('SELF', [temp_dag])
#         for node_x in temp_dag.nodes(PM_Data=True):
#             node_x[1]['DAG'].nodes[node_x[1]['Node_Index']]['Prio'] = node_x[1]['Prio']
#         for temp_flow_x in temp_flow_set:
#             max_level = max([nx[1]['rank'] for nx in temp_flow_x.nodes(PM_Data=True)])
#             random_level = math.ceil(uniform(1, max_level)) - 1
#             temp_flow_x.graph['Arrive_time'] = float(uniform(arrival_interval[0], arrival_interval[1]))
#             for nx in temp_flow_x.nodes(PM_Data=True):
#                 if nx[1]['Node_ID'] == 'start' or nx[1]['Node_ID'] == 'end':
#                     nx[1]['AET'] = 0
#                 else:
#                     nx[1]['AET'] = int((1 + uniform(-WCET_interval_max, WCET_interval_max)) * nx[1]['WCET'])
#             s_rank_nodes_list = [nx[0] for nx in temp_flow_x.nodes(PM_Data=True) if
#                                  nx[1]['rank'] > random_level and nx[1]['Node_ID'] != 'end']
#             for srn in s_rank_nodes_list:
#                 temp_flow_x.remove_node(srn)
#             end_node_s = [nx[0] for nx in temp_flow_x.nodes(PM_Data=True) if nx[1]['Node_ID'] == 'end'][0]
#             n_succnode_s = [nxx for nxx in temp_flow_x.nodes() if
#                             (nxx != end_node_s) and (len(list(temp_flow_x.successors(nxx))) == 0)]
#             for nss in n_succnode_s:
#                 temp_flow_x.add_edge(nss, end_node_s)
#             branch_node_id_list = list(
#                 set([tfnx[1]['Node_ID'] for tfnx in temp_flow_x.nodes(PM_Data=True) if tfnx[1]['C_Node'] == True]))
#             for bnode_id_x in branch_node_id_list:
#                 temp_bnode_list = [tbnx for tbnx in temp_flow_x.nodes(PM_Data=True) if
#                                    tbnx[1]['Node_ID'] == bnode_id_x]
#                 for n_nodex in sample(temp_bnode_list, randint(0, len(temp_bnode_list) - 1)):
#                     temp_flow_x.remove_node(n_nodex[0])
#         ret_DAGs_list.append(temp_flow_set)
#     return ret_DAGs_list
#
#
# def Branch_Node_Detection(tDAG):
#     node_set = set(tDAG.nodes())
#     for node_x in tDAG.nodes():
#         tDAG.nodes[node_x]['CNode'] = False
#     for node_x in tDAG.nodes():
#         if tDAG.nodes[node_x]['CNode'] == True:
#             continue
#         ans_set = set(nx.ancestors(tDAG, node_x))
#         des_set = set(nx.descendants(tDAG, node_x))
#         cur_set = node_set - {node_x} - ans_set - des_set
#
#         pre_set = set(tDAG.predecessors(node_x))
#         suc_set = set(tDAG.successors(node_x))
#         for cur_v in cur_set:
#             pre_set_y = set(tDAG.predecessors(cur_v))
#             suc_set_y = set(tDAG.successors(cur_v))
#             if pre_set == pre_set_y and suc_set == suc_set_y:
#                 tDAG.nodes[cur_v]['CNode'] = True
#                 node_set.remove(cur_v)
#                 # node_x的并行结点中，如果前驱后继相同，则赋予Ture
#                 pass
#     pass

