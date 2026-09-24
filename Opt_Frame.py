#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import numpy as np
import multiprocessing
import argparse
import pandas as pd

from datetime import datetime
from deap import base, creator, tools

ROOT_ADDR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

print(ROOT_ADDR)

sys.path.append(ROOT_ADDR)

creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

from DAG_Model import *
from Static_Scheduler import *
from Dynamic_Scheduler import *

def __Init_Individual(_td, _ta, _tm):
    return creator.Individual([
        # priority:     0
        Priority_Random(_td),
        # offset:       1
        [random.randint(0, _tm) for _ in range(_td.number_of_nodes())],
        # allocation:   2
        [random.choice([int(_cx[0]) for _cx in _ta['CPU'].items()]) for _ in range(_td.number_of_nodes())],
    ])

def __P_Crossover(_ind_x, _ind_y):
    _psx = [_ind_x.index(_i) for _i in range(len(_ind_x))]
    _psy = [_ind_x.index(_i) for _i in range(len(_ind_y))]

    _size = min(len(_psx), len(_psy))
    _cxp_1 = random.randint(1, _size)
    _cxp_2 = random.randint(1, _size - 1)
    if _cxp_2 >= _cxp_1:
        _cxp_2 += 1
    else:
        _cxp_1, _cxp_2 = _cxp_2, _cxp_1

    _tpsx = [_ni for _ni in _psy if _ni in _psx[_cxp_1:_cxp_2]]
    _tpsy = [_ni for _ni in _psx if _ni in _psy[_cxp_1:_cxp_2]]

    _psx[_cxp_1:_cxp_2] = _tpsx
    _psy[_cxp_1:_cxp_2] = _tpsy

    return [_psx.index(_i) for _i in range(_size)], [_psy.index(_i) for _i in range(_size)]

def __P_Mutator(_ind, _td, _pb=0.1):
    _ps = [_ind.index(_i) for _i in range(len(_ind))]
    for _pi in range(1, len(_ind)):
        if random.random() < _pb and _ps[_pi - 1] not in nx.ancestors(_td, _ps[_pi]) | nx.descendants(_td, _ps[_pi]):
            _ps[_pi - 1], _ps[_pi] = _ps[_pi], _ps[_pi - 1]
    for _pi, _ni in enumerate(_ps):
        _ind[_ni] = _pi
    return _ind,
    
def __O_Crossover(_ind_x, _ind_y):    
    return  tools.cxTwoPoint(_ind_x, _ind_y)

def __O_Mutator(_ind, _tm, _pb=0.1):
    for _i in range(len(_ind)):
        if random.random() < _pb:
            _ind[_i] = random.randint(0, _tm)
    return _ind,

def __A_Crossover(_ind_x, _ind_y):
    return  tools.cxTwoPoint(_ind_x, _ind_y)

def __A_Mutator(_ind, _ta, _pb=0.1):
    for _i in range(len(_ind)):
        if random.random() < _pb:
            _ind[_i] = random.choice([int(_cx[0]) for _cx in _ta['CPU'].items()])
    return _ind,

def __Evaluator(_ind, _td, _ta):
    # S1. rdag updata
    _rd = nx.DiGraph()
    _rd.add_nodes_from(_td.nodes(data=True))
    _rd.add_edges_from(_td.edges(data=True))

    for _ni, _px in enumerate(_ind[0]):
        _rd.nodes[_ni]['P'] = _px
    for _ni, _ox in enumerate(_ind[1]):
        _rd.nodes[_ni]['O'] = _ox
    for _ni, _ax in enumerate(_ind[2]):
        _rd.nodes[_ni]['A'] = _ax

    # S2.1 Static
    _du, _ru = Static_Bound_Solver(_rd, _ta, _st=True)
    _dl, _rl = Static_Bound_Solver(_rd, _ta, _st=False)

    # S2.2 Dynamic
    # _ms = list()
    # for _ in range(1000):
    #     _WS = WorkStation(_rd, _ta)
    #     _ms.append( pd.DataFrame(_WS.run())['ft'].max() )

    # _ru = np.mean(_ms) + 5 * np.std(_ms)
    # _rl = np.mean(_ms) - 5 * np.std(_ms)
    
    # S3 data output
    if _ru is None or _rl is None:
        return (float('Inf'), float('Inf'))
    else:
        return (_ru, _ru - _rl)

def Main(_td, _ta, _tm, _in=100, _pn=128, _cp=0.5, _mp=0.1):
    _tb = base.Toolbox()

    _tb.register("individual", __Init_Individual)    

    # (1) evaluator
    _tb.register("evaluate", __Evaluator)

    # (2) crossover operator
    _tb.register("a_cross", __A_Crossover)
    _tb.register("p_cross", __P_Crossover)
    _tb.register("o_cross", __O_Crossover)

    # (3) mutator operator
    _tb.register("a_mutate", __A_Mutator)
    _tb.register("p_mutate", __P_Mutator)
    _tb.register("o_mutate", __O_Mutator)

    # (4) selection
    _tb.register("select", tools.selTournament, tournsize=3)

    # (5) multiprocess
    _pool = multiprocessing.Pool(processes=os.cpu_count())
    _tb.register("map", _pool.map)
    _tb.register("starmap", _pool.starmap)

    # (6) population initial
    _rd = list()

    _pop = list([ _tb.individual(_td, _ta, _tm) for _ in range(_pn) ])

    for _ind, _fit in zip(_pop, _tb.starmap(_tb.evaluate, [(_i, _td, _ta) for _i in _pop])):
        _ind.fitness.values = _fit

    # (7) running
    for _g in range(_in):
        _st = time.time()

        # S1. Population selection
        _offspring = _tb.select(_pop, _pn)
        _offspring = list(_tb.map(_tb.clone, _offspring))

        # S2. Crossover
        for _c1, _c2 in zip(_offspring[::2], _offspring[1::2]):
            # 0. Priority
            if random.random() < _cp:
                _tb.p_cross(_c1[0], _c2[0])
                del _c1.fitness.values, _c2.fitness.values
            # 1. Offset
            if random.random() < _cp:
                _tb.o_cross(_c1[1], _c2[1])
                del _c1.fitness.values, _c2.fitness.values
            # 2. Allocation       
            if random.random() < _cp:
                _tb.a_cross(_c1[2], _c2[2])
                del _c1.fitness.values, _c2.fitness.values

        # S3. Mutator
        for _cx in _offspring:
            # 0. Priority
            if random.random() < _mp:
                _tb.p_mutate(_cx[0], _td)
                del _cx.fitness.values
            # 1. Offset
            if random.random() < _mp:
                _tb.o_mutate(_cx[1], _tm)
                del _cx.fitness.values
            # 2. Allocation
            if random.random() < _mp:
                _tb.a_mutate(_cx[2], _ta)
                del _cx.fitness.values

        # S4. Evaluate and Population update
        _npop= list( [_ind for _ind in _offspring if not _ind.fitness.valid] )
        
        for _ind, _fit in zip(_npop, _tb.starmap(_tb.evaluate, [(_i, _td, _ta) for _i in _npop])):
            _ind.fitness.values = _fit

        _pop[:] = _offspring

        # S*. Show
        _fits_1 = [ind.fitness.values[0] for ind in _pop]
        _fits_2 = [ind.fitness.values[1] for ind in _pop]

        _opt_ind = min(_pop, key=lambda ind: ind.fitness.values[0] + ind.fitness.values[1])
        _opt_fit = _opt_ind.fitness.values[0] + _opt_ind.fitness.values[1]

        _rd.append({'gn': _g, 'opt_fit': _opt_fit,
                    'min_1': min(_fits_1), 'max_1': max(_fits_1), 'ave_1': np.mean(_fits_1), 'std_1': np.std(_fits_1),
                    'min_2': min(_fits_2), 'max_2': max(_fits_2), 'ave_2': np.mean(_fits_2), 'std_2': np.std(_fits_2)})

        print(f"\tGeneration {_g}:\t{_opt_fit:.2f} -- {time.time() - _st:.2f} -- Current time:{datetime.now()} ")
    
    return _rd, _opt_ind

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Opt Frame')

    parser.add_argument('-d', '--dag', type=str, required=True, 
                            help='Input the DAG json file address')
    parser.add_argument('-a', '--arch', type=str, required=True, 
                            help='Input the Arch json file address')
    parser.add_argument('-i', '--iteration',  type=int, required=True, 
                            help='The number of iterations')
    parser.add_argument('-p', '--population', type=int, required=True, 
                            help='The population size')
    parser.add_argument('-do', '--dout', type=str, required=False, 
                            help='Optimize DAG file output address')
    parser.add_argument('-fo', '--fout', type=str, required=False, 
                            help='Iterative data file output address')

    args = parser.parse_args()

    # (1) DAG Data (json addr);
    # 处理相对路径：如果不是绝对路径，则相对于项目根目录
    dag_path = args.dag if os.path.isabs(args.dag) else os.path.join(ROOT_ADDR, args.dag)
    _td = Dag_Json_Input(dag_path)
    print(f"DAG文件路径: {dag_path}")

    # (2) Processor Data (json addr);
    # 处理相对路径：如果不是绝对路径，则相对于项目根目录
    arch_path = args.arch if os.path.isabs(args.arch) else os.path.join(ROOT_ADDR, args.arch)
    _ta = Arch_Json_Input(arch_path)
    print(f"架构文件路径: {arch_path}")

    # (3) Max offset
    _tm = sum([_wd for _ni in _td.nodes() for _arch, _feat in _td.nodes[_ni]['W'].items() for _fd, _wd in _feat.items()])
    print(_tm)

    print(args.iteration)
    print(args.population)
    _opt_rd, _opt_ind = Main(_td, _ta, _tm, args.iteration, args.population)

    # print(_opt_ind)

    if args.dout:
        # 处理输出文件路径：如果不是绝对路径，则相对于当前工作目录
        dout_path = args.dout if os.path.isabs(args.dout) else os.path.join(os.getcwd(), args.dout)
        dout_dir = os.path.dirname(dout_path)
        dout_filename = os.path.splitext(os.path.basename(dout_path))[0]
        
        # 确保输出目录存在
        os.makedirs(dout_dir, exist_ok=True)
        
        # 1. P
        for _ni, _pi in enumerate(_opt_ind[0]):
            _td.nodes[_ni]['P'] = _pi
        # 2. O
        for _ni, _oi in enumerate(_opt_ind[1]):
            _td.nodes[_ni]['O'] = _oi
        # 3. A
        for _ni, _ai in enumerate(_opt_ind[2]):
            _td.nodes[_ni]['A'] = _ai

        Dag_Json_Output(_td, dout_filename, dout_dir)
        print(f"优化后的DAG已保存到: {dout_path}")

    if args.fout:
        # 处理输出文件路径：如果不是绝对路径，则相对于当前工作目录
        fout_path = args.fout if os.path.isabs(args.fout) else os.path.join(os.getcwd(), args.fout)
        fout_dir = os.path.dirname(fout_path)
        
        # 确保输出目录存在
        os.makedirs(fout_dir, exist_ok=True)
        
        pd.DataFrame(_opt_rd).to_csv(fout_path, index=False)
        print(f"迭代数据已保存到: {fout_path}")
