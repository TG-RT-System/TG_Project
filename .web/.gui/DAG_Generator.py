#!/usr/bin/python3
# -*- coding: utf-8 -*-

################################################################################
# DAG Generator
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
################################################################################
import re
import math
import copy
# import datetime
import numpy as np
import pandas as pd
import networkx as nx
# from itertools import combinations
# from z3.z3 import Int, Sum, If, Solver, Or, IntNumRef, Bool
from random import random, sample, uniform, randint, choice


######################
# Generation type 1 ~
# Manual_Generation
######################
def Manual_Input(File_Type, Address_List):
    dag_list = []
    for address_x in Address_List:
        if File_Type == 'XLSX':
            dag_list += __User_DAG_Inject(address_x)
        elif File_Type == 'CSV':
            dag_list += __User_DAG_Read_SCV_Input(address_x)
        elif File_Type == 'HAISI':
            dag_list += __User_DAG_Read_HAISI_Input_new(address_x)
        elif File_Type == 'FEATURE':
            dag_list += __User_DAG_Feature_Input(address_x)
        else:
            pass

    for dag_x in dag_list:
        for node_x in dag_x.nodes(data=True):
            node_x[1]['Node_Indes'] = node_x[0]
    return dag_list


def __User_DAG_Read_HAISI_Input_new(addr):
    with pd.ExcelFile(addr) as data:
        # Sheet(1) : DAG_Instance_List
        df = pd.read_excel(data, 'DAG_Instance', index_col=None, na_values=["NA"], header=3)
        df.loc[:, ['DAGType', 'DAGTypeID']] = df.loc[:, ['DAGType', 'DAGTypeID']].fillna(method='ffill')  # axis：0为垂直，1为水平
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
        df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']] = df.loc[:, ['DAGType', 'DAGTypeID', 'Random range']].fillna(method='ffill')  # axis：0为垂直，1为水平
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


def __User_DAG_Feature_Input(address):
    with pd.ExcelFile(address) as data:
        all_sheet_names = data.sheet_names
        DAG_Feature_list = []
        for DAG_ID in all_sheet_names:
            df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
            DAG_Feature_list.append(np.array(df))
    return DAG_Feature_list


def __User_DAG_Inject(address):
    # dd = pd.read_excel(address, index_col=0)
    with pd.ExcelFile(address) as data:
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


def __User_DAG_Read_SCV_Input(address_x):
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


######################
# Generation type 2 ~
# Algorithm_Generation
# adjacent_matrix
######################
# ['ERDOS_GNM','ERDOS_GNP','LAYER_BY_LAYER','FANIN_FANOUT','RANDOM_ORDERS', 'MINE']
# ['GGEN', 'MARTINEZ_2018','KWOK_1999','MOGHADDAM_2021','DAGGEN','MARKOV_CHAIN','PARALLEL_APPROACH',]
def Algorithm_input(Algorithm, Algorithm_param_dict):
    dag_list = []
    if Algorithm == 'ERDOS_GNM':
        dag_list = __gen_gnm(Algorithm_param_dict)
    elif Algorithm == 'ERDOS_GNP':
        dag_list = __gen_gnp(Algorithm_param_dict)
    elif Algorithm == 'LAYER_BY_LAYER':
        dag_list = __gen_layer_by_layer(Algorithm_param_dict)
    elif Algorithm == 'FANIN_FANOUT':
        dag_list = __gen_fan_in_fan_out(Algorithm_param_dict)
    elif Algorithm == 'RANDOM_ORDERS':
        dag_list = __gen_random_order(Algorithm_param_dict)
    elif Algorithm == 'MINE_NEW2':
        dag_list = __gen_mine_new_2(Algorithm_param_dict)
    elif Algorithm == 'MINE_NEW':
        dag_list = __gen_mine_new(Algorithm_param_dict)
    elif Algorithm == 'MINE':
        dag_list = __gen_mine(Algorithm_param_dict)
    elif Algorithm == 'FLOW':
        dag_list = __gen_mine(Algorithm_param_dict)
    else:
        pass
    return dag_list


# #### DAG generator GNM  #### #
def __gen_gnm(param_dict):
    n = param_dict['Node_Num']
    m = param_dict['Edge_Num']
    DAG_num = param_dict['DAG_Num']

    assert n * (n - 1) >= m >= n - 1
    ret_DAG_list = []
    for x in range(DAG_num):
        while True:
            temp_DAG = nx.gnm_random_graph(n, m, directed=True)
            if nx.is_directed_acyclic_graph(temp_DAG):
                for node_x in temp_DAG.nodes(data=True):
                    node_x[1]['Node_Index'] = node_x[0]
                    node_x[1]['Node_ID'] = node_x[0]
                break
        temp_DAG.graph['DAG_ID'] = x
        ret_DAG_list.append(temp_DAG)
    return ret_DAG_list


# #### DAG generator GNP  #### #
def __gen_gnp(param_dict):
    n = param_dict['Node_Num']
    p = param_dict['Edge_Pro']
    DAG_num = param_dict['DAG_Num']

    ret_DAG_list = []
    for dag_id in range(DAG_num):
        Temp_Matrix = np.zeros((n, n), dtype=bool)
        for x in range(1, n-1):
            for y in range(x+1, n-1):
                if random() < p:
                    Temp_Matrix[x][y] = True
        ret_DAG = nx.from_numpy_matrix(np.array(Temp_Matrix), create_using=nx.DiGraph)
        # self.G = nx.fast_gnp_random_graph(n=n, p=p, seed=None, directed=True)
        while True:
            for x in ret_DAG.nodes(data=True):
                if len(list(ret_DAG.predecessors(x[0]))) == 0 and x[0] != 0:
                    ret_DAG.add_edge(0, x[0])                    # 无前驱节点的连接到0
                if len(list(ret_DAG.successors(x[0]))) == 0 and x[0] != n-1:
                    ret_DAG.add_edge(x[0], n-1)                  # 无前后继点的连接到n-1
            if nx.is_directed_acyclic_graph(ret_DAG):
                for node_x in ret_DAG.nodes(data=True):
                    node_x[1]['Node_Index'] = node_x[0]
                    node_x[1]['Node_ID'] = node_x[0]
                ret_DAG_list.append(ret_DAG)                   # return ret_DAG    # break
                break
            else:
                print("GNP Failed")
    return ret_DAG_list


# #### DAG generator Layer_By_Layer 算法  #### #
def __gen_layer_by_layer(param_dict):
    return False


# #### DAG generator Fan_in_Fan_out 算法  #### #
def __gen_fan_in_fan_out(param_dict):
    return False


# #### DAG generator Random_Order 算法  #### #
def __gen_random_order(param_dict):
    return False


# #### DAG generator mine 算法  #### #
def __gen_mine(Param_Dict):
    # 这里Node_Num和Critic_Path是算首尾结点的
    assert (Param_Dict['Node_Num'] > 3)
    assert (Param_Dict['Critic_Path'] >= 3)
    assert (Param_Dict['Jump_level'] >= 1)
    assert (Param_Dict['Max_in_degree'] >= 1)
    assert (Param_Dict['Max_out_degree'] >= 1)
    assert (Param_Dict['Max_Shape'] >= Param_Dict['Min_Shape'])
    assert (Param_Dict['Min_Shape'] >= 1)
    assert (Param_Dict['Width'] >= Param_Dict['Max_Shape'])
    assert ((Param_Dict['Node_Num'] - 2) <= Param_Dict['Max_Shape'] * (Param_Dict['Critic_Path'] - 2))
    assert ((Param_Dict['Node_Num'] - 2) >= Param_Dict['Min_Shape'] * (Param_Dict['Critic_Path'] - 2))

    # 参数定义：
    n = Param_Dict['Node_Num']
    k = Param_Dict['Critic_Path']

    max_shape = Param_Dict['Max_Shape']
    min_shape = Param_Dict['Min_Shape']
    max_out_degree = Param_Dict['Max_out_degree']
    max_in_degree = Param_Dict['Max_in_degree']
    width = Param_Dict['Width']
    jl = Param_Dict['Jump_level']
    connection_ratio = Param_Dict['Conn_ratio']
    DAG_Num = Param_Dict['DAG_Num']

    node_level_list = [Int(f'node_level_{x}') for x in range(n)]
    ADJ_Matrix = [[Int(f"ADJ_{i}_{j}") for j in range(n)] for i in range(n)]  # Adjacency_Matrix
    ADJ_r_Matrix = [[Int(f"ADJr_{i}_{j}") for j in range(n)] for i in range(n)]  # Adjacency_Matrix

    # ACC_Matrix      = [[Int(f"ACC_{i}_{j}") for j in range(n)] for i in range(n)]    # Accessibility
    # TEM_Matrix_1    = [[Int(f"TEM_{i}_{j}") for j in range(n)] for i in range(n)]    # Accessibility
    s = Solver()
    # (0) 上三角基本数据约束
    s.add([Or(ADJ_Matrix[i][j] == 1, ADJ_Matrix[i][j] == 0) for i in range(n) for j in range(n) if i < j])
    # (1) 下三角 && 对角线全部为0
    s.add([ADJ_Matrix[i][j] == 0 for i in range(n) for j in range(n) if i >= j])
    # (2) Shape内元素为0
    # (2.1) 确定shape
    for n_x in range(1, n-1):
        s.add(node_level_list[n_x] < k, node_level_list[n_x] > 1)
        s.add(node_level_list[n_x] >= node_level_list[n_x - 1], node_level_list[n_x] <= node_level_list[n_x + 1])  # 层数顺序递增
    for kx in range(2, k):
        self_level_node_num = Sum([If(nl_x == kx, 1, 0) for nl_x in node_level_list])
        last_level_node_num = Sum([If(nl_x == kx - 1, 1, 0) for nl_x in node_level_list])
        next_level_node_num = Sum([If(nl_x == kx + 1, 1, 0) for nl_x in node_level_list])
        s.add(self_level_node_num <= max_shape)  # 层为kx的节点数量
        s.add(self_level_node_num >= min_shape)  # 层为kx的节点数量
        s.add(self_level_node_num <= width)  # 层中节点的数量一定小于width
        s.add(last_level_node_num * max_out_degree >= self_level_node_num)  # 前一层节点的数量乘以最大出度必须大于等于本层节点数
        s.add(next_level_node_num * max_in_degree >= self_level_node_num)  # 后一层节点的数量乘以最大入度必须大于等于本层节点数
    s.add(node_level_list[0] == 1)  # 首节点在第一层
    s.add(node_level_list[n - 1] == k)  # 尾节点在第k层
    # (2.2) shape内元素为0
    for n_x in range(n):
        s.add([ADJ_Matrix[n_x][n_y] == If(node_level_list[n_x] == node_level_list[n_y], 0, ADJ_Matrix[n_x][n_y]) for
               n_y in range(n_x + 1, n)])
    # (3) jl, indegree, outdegree
    for n_x in range(1, n):
        s.add(Sum([If(node_level_list[n_x] - node_level_list[n_y] == 1, ADJ_Matrix[n_y][n_x], 0) for n_y in
                   range(n_x)]) >= 1)
        s.add(Sum([If(node_level_list[n_x] - node_level_list[n_y] > jl, ADJ_Matrix[n_y][
            n_x], 0) for n_y in
                   range(n_x)]) == 0)  # jl 约束向前
    for n_x in range(n - 1):
        s.add(Sum([If(node_level_list[n_y] - node_level_list[n_x] > 0, ADJ_Matrix[n_x][n_y], 0) for n_y in
                   range(n_x + 1, n)]) >= 1)  # jl 约束后前
        s.add(Sum([If(node_level_list[n_y] - node_level_list[n_x] > jl, ADJ_Matrix[n_x][n_y], 0) for n_y in
                   range(n_x + 1, n)]) == 0)  # jl 约束后前
    # (4) 稠密度约束  必须小于 connection_ratio 即 m 小于 connection_ratio * n * （n-1） / 2
    s.add(Sum([ADJ_Matrix[n_x][n_y] for n_x in range(n) for n_y in range(n_x + 1, n)]) <= (
                connection_ratio * n * (n - 1) / 2))
    # (5) 度约束
    for n_x in range(n):
        sum_out_degree = [ADJ_Matrix[n_x][n_y] for n_y in range(n_x + 1, n)]
        sum_in_degree = [ADJ_Matrix[n_y][n_x] for n_y in range(n_x)]
        s.add(Sum(sum_in_degree) <= max_in_degree)  # (6) 出度约束
        s.add(Sum(sum_out_degree) <= max_in_degree)  # (7) 入度约束

    Temp_DAG_list = []
    for sDAG_NUM in range(DAG_Num):
        if str(s.check()) == 'sat':
            result = s.model()
            ret_list = [result[node_level_list[x]].as_long() for x in range(n)]
            # print(ret_list) # 邻接矩阵
            r = [[result[ADJ_Matrix[i][j]].as_long() for j in range(n)] for i in range(n)]
            # print("")
            # for rx in r:
            #     print(rx)
            # rr = [[result[ACC_Matrix[i][j]].as_long() for j in range(n)] for i in range(n)]
            # print("")
            # for rx in rr:
            #     print(rx)
            Temp_G = nx.DiGraph(np.array(r))
            Temp_G.graph['DAG_ID'] = str(sDAG_NUM)
            # 生成结果检查
            assert format(nx.is_directed_acyclic_graph(Temp_G))
            for node_x in Temp_G.nodes(data=True):
                t_edges_list = ''
                for s_node_x in list(Temp_G.successors( node_x[0] )):
                    t_edges_list += '({0},{1});'.format(node_x[0], s_node_x)
                node_x[1]['Edges_List'] = t_edges_list
                node_x[1]['Node_Index'] = node_x[0]
                node_x[1]['Node_ID'] = node_x[0]
            Temp_DAG_list.append(Temp_G)
            s.add(Or([ADJ_Matrix[i][j] != result[ADJ_Matrix[i][j]] for i in range(n) for j in range(n)]))
        else:
            print("fully output!\n")
            return Temp_DAG_list
    return Temp_DAG_list


# #### DAG generator mine 算法  #### #
def __gen_mine_new(Param_Dict):
    Temp_DAG_list = []
    n = Param_Dict['Node_Num']
    # (1) 邻接矩阵
    ADJ_Matrix = np.full(shape=(n, n), fill_value=Int('None'))
    for x in range(n):
        for y in range(n):
            ADJ_Matrix[x][y] = Int(f"ADJ_{x}_{y}")

    # (2) 可达矩阵
    Arr_Matrix = ADJ_Matrix + np.eye(n, dtype=int)
    for _ in range(n):
        Arr_Matrix = np.dot(Arr_Matrix, ADJ_Matrix + np.eye(n, dtype=int))
    Arr_Matrix_Binary = np.full(shape=(n, n), fill_value=Int('None'))

    for x in range(n):
        for y in range(n):
            Arr_Matrix_Binary[x][y] = If(Arr_Matrix[x][y] > 0, 1, 0)

    s = Solver()
    # sink 和 source 分别默认为第一个和最后一个结点；
    # (1) 基础约束1，一个source & sink结点；
    for n_y in range(1, n):
        s.add(ADJ_Matrix[:, n_y].sum() > 0)  # 除了第一例，其他列的和都大于0；
    for n_x in range(n - 1):
        s.add(ADJ_Matrix[n_x, :].sum() > 0)  # 除了最后一行，其他行的和都大于0；
    # (1) 基础约束2，DAG是连通的；
    s.add(Arr_Matrix_Binary[0, :].sum() == n)  # source结点+全部可达
    s.add(Arr_Matrix_Binary[:, n - 1].sum() == n)  # 所有结点全部可达sink；
    # (1) 基础约束3，下三角 && 对角线全部为0
    for n_x in range(n):
        for n_y in range(n):
            if n_y <= n_x:
                s.add(ADJ_Matrix[n_x][n_y] == 0)
            else:
                s.add(Or([ADJ_Matrix[n_x][n_y] == 1, ADJ_Matrix[n_x][n_y] == 0]))
    # (1) 基础约束4， 无环，可达矩阵的
    for n_xy in range(n):
        s.add(Arr_Matrix[n_xy][n_xy] == 1)  # 所有结点全部可达sink；
    # (1) 基础约束4，边只有单向的
    # for n_x in range(n):
    #     for n_y in range(n):
    #         if n_x == n_y:
    #             s.add(ADJ_Matrix[n_x][n_y] == 0)
    #         else:
    #             s.add(ADJ_Matrix[n_x][n_y] + ADJ_Matrix[n_y][n_x] <= 1)
    #             s.add(Or([ADJ_Matrix[n_x][n_y] == 1, ADJ_Matrix[n_x][n_y] == 0]))
    #             # s.add(Arr_Matrix_Binary[n_x][n_y] + Arr_Matrix_Binary[n_y][n_x] <= 1)
    sDAG_NUM = 0
    while True:
        sDAG_NUM += 1
        if str(s.check()) == 'sat':
            result = s.model()
            ret_ADJ_Matrix = np.full(shape=(n, n), fill_value=1, dtype=int)
            for i in range(n):
                for j in range(n):
                    ret_ADJ_Matrix[i][j] = int(result.eval(ADJ_Matrix[i][j]).as_long())
            ret_ARR_Matrix = np.full(shape=(n, n), fill_value=1, dtype=int)
            for i in range(n):
                for j in range(n):
                    ret_ARR_Matrix[i][j] = result.eval(Arr_Matrix[i][j]).as_long()
            ret_ARR_Matrix_Binary = np.full(shape=(n, n), fill_value=1, dtype=int)
            for i in range(n):
                for j in range(n):
                    ret_ARR_Matrix_Binary[i][j] = result.eval(Arr_Matrix_Binary[i][j]).as_long()
            #
            # print("")
            # print(f"{ret_ADJ_Matrix}")
            # print(f"{ret_ARR_Matrix}")
            # print(f"{ret_ARR_Matrix_Binary}")
            # eigenvalue, featurevector = np.linalg.eig(ret_ARR_Matrix - np.eye(n))
            # for i in range(len(eigenvalue)):
            #     eigenvalue[i] = round(eigenvalue[i], 2)
            # print("特征值：", eigenvalue)

            Temp_G = nx.DiGraph(ret_ADJ_Matrix)
            Temp_G.graph['DAG_ID'] = str(sDAG_NUM)
            # 生成结果检查
            assert format(nx.is_directed_acyclic_graph(Temp_G))
            for node_x in Temp_G.nodes(data=True):
                node_x[1]['Node_Index'] = node_x[0]
                node_x[1]['Node_ID'] = node_x[0]
            # assert shape_list == [sorted(generation) for generation in nx.topological_generations(Temp_G)]
            Temp_DAG_list.append(Temp_G)
            s.add(Or([ADJ_Matrix[i][j] != result[ADJ_Matrix[i][j]] for i in range(n) for j in range(n)]))

        else:
            print(f"work finish dag_num:{len(Temp_DAG_list)}!\n")
            break
    return Temp_DAG_list

# #### DAG generator mine 算法  #### #
def __gen_mine_new_2(Param_Dict):
    # 这里Node_Num和Critic_Path是算首尾结点的
    assert (Param_Dict['Node_Num'] > 3)
    assert (Param_Dict['Critic_Path'] >= 3)
    assert (Param_Dict['Jump_level'] >= 1)
    assert (Param_Dict['Max_in_degree'] >= 1)
    assert (Param_Dict['Max_out_degree'] >= 1)
    assert (Param_Dict['Max_Shape'] >= Param_Dict['Min_Shape'])
    assert (Param_Dict['Min_Shape'] >= 1)
    assert (Param_Dict['Width'] >= Param_Dict['Max_Shape'])
    assert ((Param_Dict['Node_Num'] - 2) <= Param_Dict['Max_Shape'] * (Param_Dict['Critic_Path'] - 2))
    assert ((Param_Dict['Node_Num'] - 2) >= Param_Dict['Min_Shape'] * (Param_Dict['Critic_Path'] - 2))

    # 参数定义：
    n = Param_Dict['Node_Num']
    k = Param_Dict['Critic_Path']
    max_shape = Param_Dict['Max_Shape']
    min_shape = Param_Dict['Min_Shape']
    max_out_degree = Param_Dict['Max_out_degree']
    max_in_degree = Param_Dict['Max_in_degree']
    width = Param_Dict['Width']
    jl = Param_Dict['Jump_level']
    connection_ratio = Param_Dict['Conn_ratio']
    DAG_Num = Param_Dict['DAG_Num']

    # width_list = np.full(shape=n, fill_value=Int('None'))
    # for x in range(n):
    #     width_list[x] = Int(f'node_level_{x}')
    node_level_list = np.full(shape=n, fill_value=Int('None'))
    for x in range(n):
        node_level_list[x] = Int(f'node_level_{x}')
    ADJ_Matrix = np.full(shape=(n, n), fill_value=Int('None'))
    for x in range(n):
        for y in range(n):
            ADJ_Matrix[x][y] = Bool(f"ADJ_{x}_{y}")
    TEM_Matrix = np.full(shape=(n, n), fill_value=Int('None'))
    for x in range(n):
        for y in range(n):
            TEM_Matrix[x][y] = Int(f"TEM_{x}_{y}")
    Arr_Matrix_2 = np.full(shape=(n, n), fill_value=Int('None'))
    for x in range(n):
        for y in range(n):
            Arr_Matrix_2[x][y] = Int(f"ARR2_{x}_{y}")

    s = Solver()
    for x in range(n):
        for y in range(n):
            if x == y:
                s.add(TEM_Matrix[x][y] == 1)
            else:
                s.add(TEM_Matrix[x][y] == If(ADJ_Matrix[x][y], 1, 0))

    Arr_Matrix = np.power(TEM_Matrix, n)

    # (2) Shape内元素为0
    # (2.1) 确定shape
    for n_x in range(1, n - 1):
        s.add(node_level_list[n_x] < k, node_level_list[n_x] > 1)
        s.add(node_level_list[n_x] >= node_level_list[n_x - 1],
              node_level_list[n_x] <= node_level_list[n_x + 1])  # 层数顺序递增
    for kx in range(2, k):
        self_level_node_num = Sum([If(nl_x == kx, 1, 0) for nl_x in node_level_list])
        last_level_node_num = Sum([If(nl_x == kx - 1, 1, 0) for nl_x in node_level_list])
        next_level_node_num = Sum([If(nl_x == kx + 1, 1, 0) for nl_x in node_level_list])
        s.add(self_level_node_num <= max_shape)  # 层为kx的节点数量
        s.add(self_level_node_num >= min_shape)  # 层为kx的节点数量
        s.add(self_level_node_num <= width)  # 层中节点的数量一定小于width
        s.add(last_level_node_num * max_out_degree >= self_level_node_num)  # 前一层节点的数量乘以最大出度必须大于等于本层节点数
        s.add(next_level_node_num * max_in_degree >= self_level_node_num)  # 后一层节点的数量乘以最大入度必须大于等于本层节点数
    s.add(node_level_list[0] == 1)  # 首节点在第一层
    s.add(node_level_list[n - 1] == k)  # 尾节点在第k层

    # (1) 下三角 && 对角线全部为0
    s.add([ADJ_Matrix[n_x][n_y] == False for n_x in range(n) for n_y in range(n_x + 1)])

    for n_x in range(n):
        # (2) shape内元素为0
        s.add([ADJ_Matrix[n_x][n_y] == If(node_level_list[n_x] == node_level_list[n_y], False, ADJ_Matrix[n_x][n_y])
               for n_y in range(n_x + 1, n)])
        # (5) 度约束
        sum_out_degree = [If(ADJ_Matrix[n_x][n_y], 1, 0) for n_y in range(n_x + 1, n)]
        sum_in_degree = [If(ADJ_Matrix[n_y][n_x], 1, 0) for n_y in range(n_x)]
        s.add(Sum(sum_in_degree) <= max_in_degree)  # (6) 出度约束
        s.add(Sum(sum_out_degree) <= max_in_degree)  # (7) 入度约束

    # (3) jl, indegree, outdegree
    for n_x in range(1, n):
        s.add(Sum([If(node_level_list[n_x] - node_level_list[n_y] == 1, ADJ_Matrix[n_y][n_x], False) for n_y in
                   range(n_x)]) >= 1)
        s.add(Sum([If(node_level_list[n_x] - node_level_list[n_y] > jl, ADJ_Matrix[n_y][n_x], False) for n_y in
                   range(n_x)]) == 0)  # jl 约束向前
    for n_x in range(n - 1):
        s.add(Or([If(node_level_list[n_y] - node_level_list[n_x] > 0, ADJ_Matrix[n_x][n_y], False) for n_y in
                  range(n_x + 1, n)]) == True)  # jl 约束后前
        s.add(Or([If(node_level_list[n_y] - node_level_list[n_x] > jl, ADJ_Matrix[n_x][n_y], False) for n_y in
                  range(n_x + 1, n)]) == False)  # jl 约束后前

    # (4) 稠密度约束  必须小于 connection_ratio 即 m 小于 connection_ratio * n * （n-1） / 2
    s.add(Sum([If(ADJ_Matrix[n_x][n_y], 1, 0) for n_x in range(n) for n_y in range(n_x + 1, n)]) <= (
                connection_ratio * n * (n - 1) / 2))
    # s.add(Sum(sum_out_degree + sum_in_degree) <= max_degree)  # (8) 度约束
    # (6) DAG的width 约束：
    # """
    width_dict = {}
    for x in range(n):
        for y in range(n):
            Arr_Matrix_2[x][y] = If(Arr_Matrix[x][y] == 0, 0, 1)
    for n_x in range(1, n - 1):
        width_dict[n_x] = [Arr_Matrix_2[n_y][n_x] for n_y in range(n_x)] + [Arr_Matrix_2[n_x][n_y] for n_y in
                                                                            range(n_x + 1, n)]
        s.add(Sum(width_dict[n_x]) <= width)
    s.add(Or([Sum(width_dict[n_x]) == width for n_x in range(1, n - 1)]) == True)
    # """
    Temp_DAG_list = []
    for sDAG_NUM in range(DAG_Num):
        if str(s.check()) == 'sat':
            result = s.model()
            ret_level = np.full(shape=n, fill_value=1)
            for i in range(n):
                ret_level[i] = result[node_level_list[i]].as_long()
            ret_ADJ_Matrix = np.full(shape=(n, n), fill_value=False)
            for i in range(n):
                for j in range(n):
                    ret_ADJ_Matrix[i][j] = result.eval(ADJ_Matrix[i][j])
            ret_ARR_Matrix = np.full(shape=(n, n), fill_value=1, dtype=IntNumRef)
            for i in range(n):
                for j in range(n):
                    ret_ARR_Matrix[i][j] = result.eval(Arr_Matrix[i][j])
            ret_ARR_Matrix2 = np.full(shape=(n, n), fill_value=1, dtype=IntNumRef)
            for i in range(n):
                for j in range(n):
                    ret_ARR_Matrix2[i][j] = result.eval(Arr_Matrix_2[i][j])
            """
            print("")
            print(f"{ret_level}")
            print(f"{ret_ADJ_Matrix}")
            print(f"{ret_ARR_Matrix}")
            print(f"{ret_ARR_Matrix2}")
            """
            Temp_G = nx.DiGraph(ret_ADJ_Matrix)
            Temp_G.graph['DAG_ID'] = str(sDAG_NUM)
            # 生成结果检查
            assert format(nx.is_directed_acyclic_graph(Temp_G))
            for node_x in Temp_G.nodes(data=True):
                t_edges_list = ''
                for s_node_x in list(Temp_G.successors(node_x[0])):
                    t_edges_list += '({0},{1});'.format(node_x[0], s_node_x)
                node_x[1]['Edges_List'] = t_edges_list
                node_x[1]['Node_Index'] = node_x[0]
                node_x[1]['Node_ID'] = node_x[0]
            Temp_DAG_list.append(Temp_G)
            s.add(Or([ADJ_Matrix[i][j] != result[ADJ_Matrix[i][j]] for i in range(n) for j in range(n)]))

        else:
            print("fully output!\n")
            return Temp_DAG_list
    return Temp_DAG_list


# #### DAG generator FLOW 算法  #### #
def __gen_flow_single(Algorithm_param_dict):
    Flow_set = Algorithm_param_dict['Flow_set']
    flow_num = Algorithm_param_dict['flow_num']
    arrival_interval = Algorithm_param_dict['arrival_interval']
    WCET_interval_max = Algorithm_param_dict['WCET_interval']
    DAG_num = Algorithm_param_dict['DAG_Num']
    ret_DAGs_list = []
    for DAG_num_id in range(DAG_num):
        temp_flow_set = [copy.deepcopy(sample(Flow_set, 1)[0]) for _ in range(flow_num)]
        temp_dag, source_node_num, sink_node_num = DPC.DAG_list_merge(temp_flow_set)
        # DFA.dag_critical_path_new(temp_dag)
        # DPC.Priority_Config('SELF', [temp_dag])
        for node_x in temp_dag.nodes(data=True):
            node_x[1]['DAG'].nodes[node_x[1]['Node_Index']]['Prio'] = node_x[1]['Prio']
        for temp_flow_x in temp_flow_set:
            max_level = max([nx[1]['rank'] for nx in temp_flow_x.nodes(data=True)])
            random_level = math.ceil(uniform(1, max_level)) - 1
            temp_flow_x.graph['Arrive_time'] = float(uniform(arrival_interval[0], arrival_interval[1]))
            for nx in temp_flow_x.nodes(data=True):
                if nx[1]['Node_ID'] == 'start' or nx[1]['Node_ID'] == 'end':
                    nx[1]['AET'] = 0
                else:
                    nx[1]['AET'] = int((1 + uniform(-WCET_interval_max, WCET_interval_max)) * nx[1]['WCET'])
            s_rank_nodes_list = [nx[0] for nx in temp_flow_x.nodes(data=True) if
                                 nx[1]['rank'] > random_level and nx[1]['Node_ID'] != 'end']
            for srn in s_rank_nodes_list:
                temp_flow_x.remove_node(srn)
            end_node_s = [nx[0] for nx in temp_flow_x.nodes(data=True) if nx[1]['Node_ID'] == 'end'][0]
            n_succnode_s = [nxx for nxx in temp_flow_x.nodes() if
                            (nxx != end_node_s) and (len(list(temp_flow_x.successors(nxx))) == 0)]
            for nss in n_succnode_s:
                temp_flow_x.add_edge(nss, end_node_s)
            branch_node_id_list = list(
                set([tfnx[1]['Node_ID'] for tfnx in temp_flow_x.nodes(data=True) if tfnx[1]['C_Node'] == True]))
            for bnode_id_x in branch_node_id_list:
                temp_bnode_list = [tbnx for tbnx in temp_flow_x.nodes(data=True) if
                                   tbnx[1]['Node_ID'] == bnode_id_x]
                for n_nodex in sample(temp_bnode_list, randint(0, len(temp_bnode_list) - 1)):
                    temp_flow_x.remove_node(n_nodex[0])
        ret_DAGs_list.append(temp_flow_set)
    return ret_DAGs_list


def Branch_Node_Detection(tDAG):
    node_set = set(tDAG.nodes())
    for node_x in tDAG.nodes():
        tDAG.nodes[node_x]['CNode'] = False
    for node_x in tDAG.nodes():
        if tDAG.nodes[node_x]['CNode'] == True:
            continue
        ans_set = set(nx.ancestors(tDAG, node_x))
        des_set = set(nx.descendants(tDAG, node_x))
        cur_set = node_set - {node_x} - ans_set - des_set

        pre_set = set(tDAG.predecessors(node_x))
        suc_set = set(tDAG.successors(node_x))
        for cur_v in cur_set:
            pre_set_y = set(tDAG.predecessors(cur_v))
            suc_set_y = set(tDAG.successors(cur_v))
            if pre_set == pre_set_y and suc_set == suc_set_y:
                tDAG.nodes[cur_v]['CNode'] = True
                node_set.remove(cur_v)
                # node_x的并行结点中，如果前驱后继相同，则赋予Ture
                pass
    pass


def Dynamic_Generalization(Dynamic_type, Algorithm_param_dict):
    ret_dynamic_dag_list = []
    if Dynamic_type == 'Haisi':
        ret_dynamic_dag_list = __dynamic_haisi(Algorithm_param_dict)
    else:
        pass
    return ret_dynamic_dag_list


def __dynamic_haisi(param_dict):
    jr_lo = param_dict['jr_lower']
    jr_up = param_dict['jr_upper']
    arrive_time = param_dict['arrive_time']
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
        # todo DAG——生成方法（2）利用excel表格数据生成DAG 每个sheet一个DAG
        # def User_DAG_Inject(self, address):
        #     with pd.ExcelFile(address) as data:
        #         all_sheet_names = data.sheet_names
        #         DAG_dict = {}
        #         for DAG_ID in all_sheet_names:
        #             temp_DAG = nx.DiGraph()
        #             temp_DAG.graph['DAG_ID'] = DAG_ID
        #             df = pd.read_excel(data, DAG_ID, index_col=None, na_values=["NA"])
        #             title_list = df.dtypes
        #             for row in df.index:
        #                 temp_DAG.add_node(df.loc[row]['Node_Index'], DAG_ID=DAG_ID, Status="Block")
        #                 for title_id, data_type in title_list.items():
        #                     row_data = df.loc[row][title_id]
        #                     if title_id == 'Edges_List':
        #                         if type(row_data) == float:
        #                             continue
        #                         row_data = row_data.split(';')
        #                         for edge_data in row_data:
        #                             edge_list = edge_data[1:-1].split(',')
        #                             temp_DAG.add_edge(int(edge_list[0]), int(edge_list[1]))
        #                     else:
        #                         temp_DAG.nodes[df.loc[row]['Node_Index']][title_id] = row_data
        #             DAG_dict[DAG_ID] = temp_DAG
        #     return DAG_dict
        #


"""

# #### DAG generator FLOW 算法  #### #
def __gen_flow_new(Algorithm_param_dict):
    Flow_set = Algorithm_param_dict['Flow_set']  # []
    flow_num = Algorithm_param_dict['flow_num']  # 1~10
    arrival_interval = Algorithm_param_dict['arrival_interval']  # [0, 20 * 2260]
    WCET_interval_max = Algorithm_param_dict['WCET_interval']  # [0, 0.1]
    DAG_num = Algorithm_param_dict['DAG_Num']
    ret_DAG_list = []
    for dag_id in range(DAG_num):
        temp_flow_set = [copy.deepcopy(sample(Flow_set, 1)[0]) for _ in range(flow_num)]  # 随机抽取（可重复）flow_num个流
        for temp_flow_x in temp_flow_set:
            max_level = max([nx[1]['rank'] for nx in temp_flow_x.nodes(data=True)])
            random_level = math.ceil(uniform(1, max_level)) - 1
            # print(f"flow:{temp_flow_x.graph['DAG_ID']},max_level:{max_level},rand_level{random_level}")
            for nx in temp_flow_x.nodes(data=True):
                # (1) 初始化起始时间_ok
                if nx[1]['Node_ID'] == 'start':
                    nx[1]['AET'] = int(uniform(arrival_interval[0], arrival_interval[1]))
                # (1) 初始化截止时间_ok
                elif nx[1]['Node_ID'] == 'end':
                    nx[1]['AET'] = 0
                # (2) 随机执行时间波动;
                else:
                    nx[1]['AET'] = int((1 + uniform(-WCET_interval_max, WCET_interval_max)) * nx[1]['WCET'])
            # (3) 层数变化_大于random的为0
            s_rank_nodes_list = [nx[0] for nx in temp_flow_x.nodes(data=True) if
                                 nx[1]['rank'] > random_level and nx[1]['Node_ID'] != 'end']
            for srn in s_rank_nodes_list:
                temp_flow_x.remove_node(srn)
            # (3) 无后继结点与end连接
            end_node_s = [nx[0] for nx in temp_flow_x.nodes(data=True) if nx[1]['Node_ID'] == 'end'][0]
            n_succnode_s = [nxx for nxx in temp_flow_x.nodes() if
                            (nxx != end_node_s) and (len(list(temp_flow_x.successors(nxx))) == 0)]
            for nss in n_succnode_s:
                temp_flow_x.add_edge(nss, end_node_s)
            # (4) 分支数量波动
            branch_node_id_list = list(
                set([tfnx[1]['Node_ID'] for tfnx in temp_flow_x.nodes(data=True) if tfnx[1]['C_Node'] == True]))
            for bnode_id_x in branch_node_id_list:
                temp_bnode_list = [tbnx for tbnx in temp_flow_x.nodes(data=True) if
                                   tbnx[1]['Node_ID'] == bnode_id_x]
                for n_nodex in sample(temp_bnode_list, randint(0, len(temp_bnode_list) - 1)):
                    temp_flow_x.remove_node(n_nodex[0])  # 随机抽0, len(temp_bnode_list)
        temp_dag, source_node_num, sink_node_num = DPC.DAG_list_merge(temp_flow_set)
        for node_x in temp_dag.nodes(data=True):
            node_x[1]['WCET_old'] = node_x[1]['WCET']
        ret_DAG_list.append(temp_dag)
    return ret_DAG_list

    # def transitive_reduction_matrix(self):
    #     matrix = np.array(nx.adjacency_matrix(self.G).todense())
    #     row, columns = matrix.shape
    #     assert (row == self.task_num)
    #     assert (columns == self.task_num)
    #     print("matrix shape is ({0},{1})".format(row, columns))
    #     i_test = np.eye(self.task_num).astype(bool)
    #     i_matrix = matrix.astype(bool)
    #     D = np.power((i_matrix | i_test), self.task_num)  # (M | I)^n
    #     D = D.astype(bool) & (~i_test)
    #     TR = matrix & (~(np.dot(i_matrix, D)))  # Tr = T ∩ （-（T . D））
    #     return nx.DiGraph(TR)
"""

# def exam_pic_show(dag_x, title):
#     dot = gz.Digraph()
#     dot.attr(rankdir='LR')
#     for node_x in dag_x.nodes(data=True):
#         temp_label = 'Node_ID:{0}\nPrio:{1}\nWCET:{2}\nIndex:{3}\n'.format(
#             str(node_x[0]), str(node_x[1]['Prio']), str(node_x[1]['WCET']), str(node_x[1]['Node_ID']))
#         temp_node_dict = node_x[1]
#         if 'critic' in temp_node_dict:
#             if node_x[1]['critic']:
#                 color_t = 'red'
#             else:
#                 color_t = 'green'
#         else:
#             color_t = 'black'
#         dot.node('%s' % node_x[0], temp_label, color=color_t)
#     for edge_x in dag_x.edges():
#         dot.edge('%s' % edge_x[0], '%s' % edge_x[1])
#     # dot.view('./test.png')
#     dot.view(f'./pic_test_7-25/{title}')

"""
import numpy as np
import itertools

# # 创建一个二维数组
# a = np.array([[1, 2, 3], [4, 5,6], [7, 8, 9]])
# # 创建一个新的一维数组
# b = np.array([10, 11, 12])
# # 在二维数组中插入一行
# c1 = np.insert(a, a.shape[0], b, axis=0)
# c2 = np.insert(a, a.shape[1], b, axis=1)
# print(c1)
# print(c2)

# 设计基本函数
def DAG_Generator(Source_Matrix, Node_Num):

    last_node_num = Source_Matrix.shape[0]
    ret_data = []
    for lnum in range(1, last_node_num + 1):        # insert_col_x = copy.deepcopy(insert_col)
        edge_list = list(itertools.combinations(list(range(last_node_num)), lnum))
        for edge_trup in edge_list:
            Source_Matrix_Cp = copy.deepcopy(Source_Matrix)
            insert_col = np.zeros((1, last_node_num))
            for edge_x in edge_trup:
                insert_col[0][edge_x] = 1
            Source_Matrix_Cp = np.insert(Source_Matrix_Cp, Source_Matrix_Cp.shape[1], insert_col, axis=1)    # 列
            Source_Matrix_Cp = np.insert(Source_Matrix_Cp, Source_Matrix_Cp.shape[0], np.zeros((1, Source_Matrix_Cp.shape[1])), axis=0)    # 行

            if Node_Num == 2:
                # 唯一的尾结点sink node；
                # ret_data.append(Source_Matrix_Cp)
                f_n1 = [n_x  for n_x in range(Source_Matrix_Cp.shape[0]) if np.sum(Source_Matrix_Cp[n_x]) == 0]  # 选择
                f_n2 = [n_x  for n_x in range(Source_Matrix_Cp.shape[0]) if np.sum(Source_Matrix_Cp[n_x]) != 0]  # 必连
                for lnum in range(len(f_n1) + 1):
                    test_1 = list(itertools.combinations(f_n1, lnum))
                    for s_node_list in list(itertools.combinations(f_n1, lnum)):
                        Source_Matrix_Cp_temp = copy.deepcopy(Source_Matrix_Cp)
                        temp_fn = copy.deepcopy(f_n2) + [s_node_x for s_node_x in s_node_list]
                        insert_col = np.zeros((1, Source_Matrix_Cp.shape[0]))
                        for edge_x in temp_fn:
                            insert_col[0][edge_x] = 1
                        Source_Matrix_Cp_temp = np.insert(Source_Matrix_Cp_temp, Source_Matrix_Cp_temp.shape[1], insert_col, axis=1)  # 列
                        Source_Matrix_Cp_temp = np.insert(Source_Matrix_Cp_temp, Source_Matrix_Cp_temp.shape[0], np.zeros((1, Source_Matrix_Cp_temp.shape[1])), axis=0)  # 行
                        ret_data.append(Source_Matrix_Cp_temp)
                #         Source_Matrix_Cp = np.c_[Source_Matrix_Cp, insert_col.T]
                #         insert_row = np.zeros((1, Source_Matrix_Cp.shape[1]))
                #         Source_Matrix_Cp = np.r_[Source_Matrix_Cp, insert_row]
                #         # 加入尾结点；没有后继的一定链接，其他的分配

            else:
                ret_data += DAG_Generator(Source_Matrix_Cp, Node_Num - 1)
    return ret_data


if __name__ == "__main__":
    for node_num in range(2, 10):
        ret_matrix_list = DAG_Generator(np.zeros((1, 1)), node_num)
        print(f'node_num:{node_num}, dag_num :{len(ret_matrix_list)}')
        # graph = nx.from_numpy_matrix(Matrix)
    pass
# for shape_num in range(node_num):
"""

if __name__ == "__main__":
    All_DAG_list = Algorithm_input('MINE',{'DAG_Num': 10, 'Node_Num': 37, 'Critic_Path': 7, 'Width': 15,
                                           'Jump_level': 1, 'Conn_ratio': 0.08859, 'Max_Shape': 15,'Min_Shape': 1,
                                           'Max_in_degree': 15, 'Max_out_degree': 5})


    pass
    """
        # ############ Manual ############## #
    # ### (1) CSV
    # All_DAG_list = Manual_Input('CSV', ['./Exam_data/csv_data/exam1/' + f_x for f_x in ['1.csv', '2.csv', '3.csv']])
    # ### (2) HAISI
    # All_DAG_list = Manual_Input('HAISI', ['./Exam_data/haisi_data/DAG1.xlsx'])

    # ############ Algorithm ############## #
    # ['ERDOS_GNM','ERDOS_GNP', 'LAYER_BY_LAYER','FANIN_FANOUT', 'RANDOM_ORDERS', 'MINE']
    # ### (1) MINE
    # dag - 1
    # All_DAG_list = Algorithm_input('MINE',
    #                                {'DAG_Num': 1, 'Node_Num': 48, 'Critic_Path': 10, 'Width': 16,
    #                                 'Jump_level': 7, 'Conn_ratio': 0.06383, 'Max_Shape': 11,
    #                                 'Min_Shape': 1, 'Max_in_degree': 11, 'Max_out_degree': 7})
    # MAX_WCET =292952
    # MIN_WCET =1500

    # dag - 2
    # All_DAG_list = Algorithm_input('MINE',
    #                                {'DAG_Num': 10, 'Node_Num': 15, 'Critic_Path': 4, 'Width': 11,
    #                                 'Jump_level': 1, 'Conn_ratio': 0.22857, 'Max_Shape': 11,
    #                                 'Min_Shape': 1, 'Max_in_degree': 11, 'Max_out_degree': 7})
    # MAX_WCET =327388
    # MIN_WCET =1500
    # dag - 3

    MAX_WCET = 264088
    MIN_WCET = 3032

    # ### (2) ERDOS_GNM
    # All_DAG_list = Algorithm_input('ERDOS_GNM', {'DAG_Num': 10, 'Node_Num': 10, 'Edge_Num': 20})
    # ### (3) ERDOS_GNP
    # All_DAG_list = Algorithm_input('ERDOS_GNP',  {'DAG_Num': 10, 'Node_Num': 10, 'Edge_Pro': 0.3})

    for dag_id, dag_obj in enumerate(All_DAG_list):
        # ############ WCET_Config ############## #
        DWC.WCET_Config(dag_obj, 'Uniform', Virtual_node=True, a=264088, b=3032)
        # ############ Critical_Param_Config ############## #
        DFA.dag_param_critical_update(dag_obj, dag_id)

    # ############ Data output ############## #
    time_str = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H=%M=%S')
    output_path = './Result_data/test/' + time_str + '/'

    DDP.Exam_Data_Output(All_DAG_list, 'PIC', output_path)     # 输出图像
    DDP.Exam_Data_Output(All_DAG_list, 'CSV', output_path)     # 输出数据
    DDP.Exam_Data_Output(All_DAG_list, 'CRI', output_path)     # 输出关键参数
    # DDP.Exam_Data_Output(All_DAG_list, 'HAISI', output_path)   # 输出关键参数
    """


    # #### Transitive reduction Function #### #
    #   param:  matrix: Adjacency Matrix
    #   return: A matrix that has been reduced in transitive
