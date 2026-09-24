#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import copy
import math
import time
import numpy as np
import pandas as pd
import networkx as nx
from itertools import combinations
from random import random, sample, uniform, randint, choice, seed

from Src.DAG_Data import UDAG, LDAG, CDAG
# from Src.DAG_Configure import DAG_Configure as DC

######################
# Manual_Generation
# OutPut LDAG--
######################
def manual_input(__FileType, __AddrList):
    __DagList = []
    for __AddrX in __AddrList:
        if __FileType == 'General':
            __DagList += __general_dag_input(__AddrX)
        elif __FileType == 'Haisi':
            __DagList += __haisi_dag_input(__AddrX)
        # elif File_Type == 'CSV':
        #     dag_list += __User_DAG_SCV_Input(addr_x)
        # elif File_Type == 'FEATURE':
        #     dag_list += __User_DAG_Feature_Input(addr_x)
        else:
            pass
    return __DagList


def __general_dag_input(address_x):
    with pd.ExcelFile(address_x) as data:
        all_sheet_names = data.sheet_names
        DAG_list = []
        for __dag_typeid, __dag_type in enumerate(all_sheet_names):
            temp_DAG = LDAG()

            temp_DAG.graph.update({'DAGType': __dag_type, 'DAGTypeID': __dag_typeid, 'DAGInst': '', 'DAGInstID': 0,
                                   'SlotLen': 0, 'DAGsubmitOffset': 0, 'Arrive_time': 0.0, 'Random_range': (0.0, 0.0),
                                   'Cycle': 1,  'Period': 0, 'Criticality': 1,   # Cycle：默认执行1次, Period：一次循环无周期
                                   })
            df = pd.read_excel(data, __dag_type, index_col=None, na_values=["NA"])
            for row in df.index:
                temp_DAG.add_node(df.loc[row]['Node_Index'], DAG=temp_DAG, Crit=1, JobInstNum=1, QoS=df.loc[row]['Prio'],
                                  JobID=df.loc[row]['Node_ID'], JobTypeID=df.loc[row]['Node_Index'],
                                  JobCycle=df.loc[row]['WCET'], PublishJob=df.loc[row]['Edges_List'])
                if type(df.loc[row]['Edges_List']) is str:
                    for s_node in df.loc[row]['Edges_List'].split(';'):
                        if s_node != '':
                            temp_DAG.add_edge(int(df.loc[row]['Node_Index']), int(s_node))
            DAG_list.append(temp_DAG)
    return DAG_list

def __haisi_dag_input(address_x):
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
                            for p_node_x in [node_x for node_x in dag_oo.nodes(data=True) if
                                             node_x[1]['JobTypeID'] == edge_p]:  # 遍历所有同ID的前驱
                                s_node_list = sample([node_x for node_x in dag_oo.nodes(data=True) if
                                                      node_x[1]['JobTypeID'] == temp_edge_s_list[0] and
                                                      len([self_nx for self_nx in list(dag_oo.predecessors(node_x[0]))
                                                           if dag_oo.nodes[self_nx]['JobTypeID'] == p_node_x[1][
                                                               'JobTypeID']]) < int(temp_edge_s_list[1])]
                                                     , k=int(temp_edge_s_list[2]))
                                for s_node_x in s_node_list:
                                    dag_oo.add_edge(p_node_x[0], s_node_x[0])
                        else:
                            for p_node_x in [node_x for node_x in dag_oo.nodes(data=True) if
                                             node_x[1]['JobTypeID'] == edge_p]:
                                for s_node_x in [node_x for node_x in dag_oo.nodes(data=True) if
                                                 node_x[1]['JobTypeID'] == temp_edge_s_list[0]]:
                                    dag_oo.add_edge(p_node_x[0], s_node_x[0])
        # Sheet(2) : DAG_Type_List
        df = pd.read_excel(data, 'DAG_Type', index_col=None, na_values=["NA"], header=1)
        # df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']] = df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']].fillna(method='ffill')  # axis：0为垂直，1为水平
        df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']] = df.loc[:, ['DAGType', 'DAGTypeID',
                                                                         'Random range']].ffill()  # axis：0为垂直，1为水平

        # print(df)
        all_dag_list = []
        for index, row in df.iterrows():
            temp_dag = copy.deepcopy(DAG_Obj_dict[row['DAGType']])
            temp_dag.graph['DAGType'] = row['DAGType']
            temp_dag.graph['DAGTypeID'] = row['DAGTypeID']
            temp_dag.graph['DAGInstID'] = row['DAGInstID']
            min_r, max_r = row['Random range'][:-1].split('~')
            # temp_dag.graph['Arrive_time'] = float(row['DAGsubmitOffset']) * float(row['SlotLen']) * random.uniform(float(min_r), float(max_r)) / 100
            temp_dag.graph['Arrive_time'] = float(row['DAGsubmitOffset']) * float(row['SlotLen']) * (
                    1 + uniform(-float(max_r), float(max_r)) / 100)
            all_dag_list.append(temp_dag)
    return all_dag_list

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

def __User_DAG_Feature_Input(address_x):
    with pd.ExcelFile(address_x) as data:
        all_sheet_names = data.sheet_names
        DAG_Feature_list = []
        for DAG_ID in all_sheet_names:
            df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
            DAG_Feature_list.append(np.array(df))
    return DAG_Feature_list

def __dag_input_xlsx(self):
    for addr_x in self.Address_List:
        with pd.ExcelFile(addr_x) as data:
            all_sheet_names = data.sheet_names
            for DAG_ID in all_sheet_names:
                temp_dag = nx.DiGraph()
                temp_dag.graph['DAG_ID'] = DAG_ID
                df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
                title_list = df.dtypes
                # xxxx = df.columns
                for row in df.index:
                    temp_dag.add_node(df.loc[row]['Node_Index'], DAG=temp_dag)
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
                                temp_dag.add_edge(int(edge_list[0]), int(edge_list[1]))
                        else:
                            temp_dag.nodes[df.loc[row]['Node_Index']][title_id] = row_data
                self.dag_list.append(temp_dag)


if __name__ == "__main__":
    # 本项目的基础地址
    Base_Addr = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # ### (1) CSV
    __ddi = manual_input('General', ["../../_Data/DAG_Data_Huawei_new.xlsx"])
    __dc = DC.DAG_Configure()
    # for dag_id, dag_obj in enumerate(All_DAG_list):
    for __dag_id, __dag_x in enumerate(__ddi):
        # (1) 基本参数配置；
        DFA.dag_data_initial(__dag_x, __dag_id, DAGType=__dag_id, Critic=1)
        # (2) 关键参数配置；
        DFA.dag_param_critical_update(__dag_x)
        # (3) 优先级配置；
        DPC.Priority_Config('MINE', __dag_x)

    for DAG_id, DAG_x in enumerate(__ddi):
        # print(f'DAG ID : {dag_x.graph["DAG_ID"]}')
        dag_data_initial(DAG_x, DAG_id, DAG_id, 0)
        # (2) DAG的拓扑结构参数计算
        dag_topology_initial(DAG_x)
        DWC.WCET_Config(DAG_x, 'Uniform', Virtual_node=True, a=10000, b=100)
        # (3) DAG的颗粒度参数计算
        dag_graine_initial(DAG_x)
        # (4) DAG的优先级计算
        # print( DAG_x.graph )
        SRS.exam_pic_show(DAG_x, f"{DAG_x.graph['DAG_ID']}")
        # SRS.exam_pic_show(DAG_x, f"{DAG_x.graph['DAG_ID']}")
        # for x_id, x_data in DAG_x.graph:
        # DFA = DAG_Features_Analysis(dag_x, dag_id, dag_type=dag_id, dag_inst_id=0, slot_len=0.0,
        #                             dag_submit_offset=0, random_range=0.3, period=1, cycle=1, critic=0)

    # ######### Critical_Param_Config ########## #
    # DFA.dag_param_critical_update(dag_obj, dag_id)

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
#         for node_x in temp_dag.nodes(__PM_Data=True):
#             node_x[1]['DAG'].nodes[node_x[1]['Node_Index']]['Prio'] = node_x[1]['Prio']
#         for temp_flow_x in temp_flow_set:
#             max_level = max([nx[1]['rank'] for nx in temp_flow_x.nodes(__PM_Data=True)])
#             random_level = math.ceil(uniform(1, max_level)) - 1
#             temp_flow_x.graph['Arrive_time'] = float(uniform(arrival_interval[0], arrival_interval[1]))
#             for nx in temp_flow_x.nodes(__PM_Data=True):
#                 if nx[1]['Node_ID'] == 'start' or nx[1]['Node_ID'] == 'end':
#                     nx[1]['AET'] = 0
#                 else:
#                     nx[1]['AET'] = int((1 + uniform(-WCET_interval_max, WCET_interval_max)) * nx[1]['WCET'])
#             s_rank_nodes_list = [nx[0] for nx in temp_flow_x.nodes(__PM_Data=True) if
#                                  nx[1]['rank'] > random_level and nx[1]['Node_ID'] != 'end']
#             for srn in s_rank_nodes_list:
#                 temp_flow_x.remove_node(srn)
#             end_node_s = [nx[0] for nx in temp_flow_x.nodes(__PM_Data=True) if nx[1]['Node_ID'] == 'end'][0]
#             n_succnode_s = [nxx for nxx in temp_flow_x.nodes() if
#                             (nxx != end_node_s) and (len(list(temp_flow_x.successors(nxx))) == 0)]
#             for nss in n_succnode_s:
#                 temp_flow_x.add_edge(nss, end_node_s)
#             branch_node_id_list = list(
#                 set([tfnx[1]['Node_ID'] for tfnx in temp_flow_x.nodes(__PM_Data=True) if tfnx[1]['C_Node'] == True]))
#             for bnode_id_x in branch_node_id_list:
#                 temp_bnode_list = [tbnx for tbnx in temp_flow_x.nodes(__PM_Data=True) if
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





