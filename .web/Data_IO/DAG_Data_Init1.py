# !/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Real-Time Systems Group
Hunan University HNU
Created by Fang YJ on 2023/10/25.
"""
import sys
sys.path.append('/public3/home/a2s001977/fyj')


import os
import copy
import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from scipy import stats
from threading import Thread
from random import choice, random
from itertools import combinations, permutations
from multiprocessing import cpu_count, Pool, Manager, Event, Process
from multiprocessing.pool import ThreadPool
# from mpi4py.futures import MPIPoolExecutor

from Src.DAG_Data import UDAG, LDAG, CDAG
from Src.DAG_Data_IO import DAG_Data_Input as DDI
from Src.DAG_Configure import DAG_Configure as DC

from Src.DAG_Scheduler import Core
from Src.DAG_Scheduler import LC_inject_HC as LH
from Src.DAG_Scheduler import Simpy_Simulator as SS
# from Src.DAG_Scheduler import Light_Simulator as LSS
# from Src.DAG_Configure.Priority_Allocation import DAG_Priority_Config as DPC


DagNum = 10
ExamNum = 500
# Jitter = (0.0, 0.1)

DAG_Input_Addr = ["../_Data/DAG_Data_Huawei_new.xlsx"]

# Experiment 1
NP_Output_Addr = f"../_Data/__NP_Retu/"

# Experiment 2
FP_Output_Addr = f"../_Data/__FP_Retu/"

# Experiment 3
pm_x = None

# Experiment 3_1
P_MUTATION = 0.1        # 变异的概率
P_CROSSOVER = 0.9       # 交叉的概率
MAX_GENERATION = 40     # 停止条件中的最大迭代次数
POPULATION_SIZE = 64    # 种群中的个体数量(越大越平滑)
Evaluate_num = 100


# Experiment 3_2
PT_Iutput_Addr = f"../_Data/__PT_Retu/"     # 抢占表存储地址；

LP_Output_Addr = f"../_Data/__LP_Retu/"     # 测试实验数据输出地址；

core_num_dick = {"l_l": {"2_8": 16, "4_6": 18, "6_4": 18, "8_2": 16},
                 "l_w": {"2_8": 24, "4_6": 24, "6_4": 20, "8_2": 16},
                 "w_l": {"2_8": 14, "4_6": 22, "6_4": 17, "8_2": 18},
                 "w_w": {"2_8": 26, "4_6": 24, "6_4": 28, "8_2": 24}}


def Dag_Init(__Jitter):
    __DagDatas = DDI.manual_input('General', DAG_Input_Addr)
    DagConfig = DC.DAG_Configure('MINE')
    __Ret_CDags = []
    for __LDagId, __LDagX in enumerate(__DagDatas):
        __LDagX.graph['Random_range'] = (0, __Jitter/100)
        __Ret_CDags.append(DagConfig.dag_feature_configure(__LDagX))
    return __Ret_CDags


def Dag_Case_Init(__DagDick, __HlId, __HlR):
    __HIDag, __LODag = __DagDick[__HlId[0]], __DagDick[__HlId[1]]
    __DagVol = __HIDag.graph["vol"] + __LODag.graph["vol"]
    # __hi_node_num, __lo_node_num = __hi_dag.number_of_nodes() + 1, __lo_dag.number_of_nodes() + 1
    __RetDags = []
    for __DagX, __Crit, __DagR, __DagId in zip((__HIDag, __LODag), (1, 2), __HlR, __HlId):
        __DagRate = (__DagR * __DagVol) / (__DagX.graph["vol"] * sum(__HlR))
        for __node_x in __DagX.nodes(data=True):
            __node_x[1]["JobCycle"] *= __DagRate
        # __DagX.graph["vol"] = sum(nx.get_node_attributes(__dag_x, 'wcet').values())
        for __Dt in range(DagNum):
            __TDag = copy.deepcopy(__DagX)
            __TDag.cdag_inst_init(__Dt, __Crit)
            __RetDags.append(__TDag)
        # (*) DAG图展示
        # SRS.exam_pic_show(dag_data["DAG"], f"{dag_type}-id{dag_data['id']}-r{dag_data['r']}")
    return __RetDags


def PT_load(__DagDick, __HLID, __HLR, __Jitter):
    # (1) 多核多DAG场景参数配置
    pm_shape = (__DagDick[__HLID[0]].number_of_nodes() + 1, __DagDick[__HLID[1]].number_of_nodes() + 1)
    core_num = core_num_dick[f"{__HLID[0]}_{__HLID[1]}"][f"{__HLR[0]}_{__HLR[1]}"]
    ppm = np.full(shape=(pm_shape[0] * pm_shape[1]), fill_value=True)
    # (2) 加载 PM
    # """
    # E:\github\DAG_Simulator_Platform\_Data\__PT_Retu\ll\2HI-8LO
    # file_name = f"{__HLID[0]}{__HLID[1]}\{__HLR[0]}HI-{__HLR[1]}LO\{core_num}Core_{__Jitter}jit.npy"
    # ppm = np.load(PT_Iutput_Addr+file_name, allow_pickle=True).item()
    # ppm = np.load(PT_Iutput_Addr + file_name)
    # """
    return np.stack([copy.deepcopy(ppm).reshape(pm_shape), np.full(shape=pm_shape, fill_value=False)])

def basic_simulate(__Params):
    # 动态泛化
    __En = __Params["EN"]
    __Pt = __Params["PM"]
    __RetDags = __Params["RetDags"]
    __CoreNum = __Params["CoreNum"]
    __SNPType = __Params["SNPType"]
    __Print = __Params["Print"]
    __RetDict = {"vol": 0, "en": __En}
    # __RetDict = {}
    __TempRetDags = [CDAG() for _ in range(len(__RetDags))]
    for __TRdag, __RDag in zip(__TempRetDags, __RetDags):
        __TRdag.cdag_copy(__RDag)
        __TRdag.dag_dynamic_generalization()
        __RetDict["vol"] += sum(nx.get_node_attributes(__TRdag, name='wcet').values())

    __SBs = {'np': SS.FullyNonPreemptiveSimulator(),
             'fp': SS.FullyPreemptiveSimulator(),
             'lp': SS.LimitedPreemptiveSimulator()
             }

    for __SType, __NType, __PType in __SNPType:
        __SBs[__SType].data_init(__TempRetDags, __CoreNum, Priority_rank=__NType,
                                 Preempt_type=__PType, Limited_Preempt_type='PT', Preempt_table=__Pt)
        __SBs[__SType].simulate()

        __SimRet = __SBs[__SType].Core_Data_List
        # __RetDict[f"{__SType}_{__PType}"] = __SimRet
        for __CType in ["c1", "c2", "all", ]:
            __RetDict[f"{__SType}_{__PType}_{__CType}"] = Core.ret_makespan(__SimRet, __CType)
    if __Print:
        print(__RetDict)
    return __RetDict