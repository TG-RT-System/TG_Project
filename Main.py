#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import z3.z3 as z3
import time
import json
import math
import numpy as np
import networkx as nx
import graphviz as gz
import matplotlib.pyplot as plt

""" 1. Data Input """
# 1. DAG Input (json)
def Dag_Json_Input(_file:str):
    _rd = nx.DiGraph()
    with open(_file, "r") as _f:
        _td = json.load(_f)
        _tdg = _td['G']
        _rd.add_nodes_from([(_nd['ID'], _nd) for _nd in _tdg['V']])
        _rd.add_edges_from(_tdg['E'])
        _rd.graph['ID'] = _td['ID']
    return _rd

# 2. Processor Input (json)
def Processor_Json_Input(_file:str):
    with open(_file, "r") as _f:
        _r = json.load(_f)
    return _r


""" 2. Data Output """
# 1. DAG fig Output (png)
def DAG_Fig_Output(_rd, _file:str):
    dot = gz.Digraph(format='png', )
    dot.attr(rankdir='LR')
    for _ni, _nd in _rd.nodes(data=True):
        dot.node(f'{_ni}', '\n'.join([f"{_ndk}:{_ndv}" for _ndk, _ndv in _nd.items()]), shape='polygon', style='rounded')
    for _ep, _es in _rd.edges():
        dot.edge(f'{_ep}', f'{_es}')
    dot.render(f"{_file}/{_rd.graph['ID']}")

# 2. Gantt fig Output (png)
def Gantt_Fig_Output(_rd, _dl:list, _file:str):
    for _ni, _st, _ct, _ai in _dl:
        if 0 < _ct:
            plt.barh(y=_ai, width=_ct, height=0.3, left=_st, edgecolor='black', color="white")
            plt.text(s=f'{_ni}\n{_ct}', y=_ai, x=_st + _ct / 2, fontsize=8,  ha='center', va='center',)
    # plt.savefig(f"./Odata/Gantt_{_file}.png")
    plt.savefig(f"{_file}/{_rd.graph['ID']}.png")

# 3. Schedule table Output (json) 
def Schedule_Tab_Output(_rd, _dl:list, _file:str):
    with open(f"{_file}/{_rd.graph['ID']}.json", "w", encoding="utf-8") as _f:
        json.dump({_n: {'s': _s, 'c': _c, 'a': _a} for _n, _s, _c, _a in _dl}, _f, indent=4, ensure_ascii=False)

""" 3*. Schedulability Verification """

""" 3. Optimal Solver """
def DAG_Opt_Solver(_td, _pd):
    # 1. Create Z3 Optimize Solver
    _s = z3.Optimize()
    
    # 2. Variables of the model
    # (1) start time of _ni
    _start = {_ni: z3.Int(f's{_ni}') for _ni in _td.nodes()}

    # (2) core id of _ni
    _assig = {_ni: z3.Int(f'a{_ni}') for _ni in _td.nodes()}

    # (3) completion time of DAG 
    _makspan = z3.Int('makespan')

    # 3. Constraint;
    for _ni in _td.nodes():
        # (1) start time of source node;
        if _td.in_degree(_ni) == 0:                              
            _s.add(0 <= _start[_ni])

        # (2) _ni starts after predecessors have completed        
        for _pi in nx.DiGraph.predecessors(_td, _ni):
            _s.add(_start[_pi] + _td.nodes[_pi]['W'] <= _start[_ni])
        
        # (3) core id of the running ni;        
        _s.add(0 <= _assig[_ni], _assig[_ni] < _pd)

        # (4) completion time of sink nodes and DAG 
        if _td.out_degree(_ni) == 0:
            _s.add(_makspan >= _start[_ni] + _td.nodes[_ni]['W'])

    # (5) The execution times of nodes wihtin a core do not overlap
    _ns = list(nx.topological_sort(_td))
    for _ne, _ni in enumerate(_ns):
        for _nj in set(_ns[_ne + 1:]) - nx.descendants(_td, _ni):
            _s.add(z3.Implies(_assig[_ni] == _assig[_nj], z3.Or(_start[_nj] >= _start[_ni] + _td.nodes[_ni]['W'], 
                                                                _start[_ni] >= _start[_nj] + _td.nodes[_nj]['W'])))        

    """ 4. 添加目标函数 """
    _s.minimize(_makspan)

    """ 5. 执行求解器 """
    # if str(_s.check()) == 'sat':
    if _s.check() == z3.sat:
        _ret = _s.model()
        _dl = [(_ni, _ret[_start[_ni]].as_long(), _nd['W'], _ret[_assig[_ni]].as_long()) 
               for _ni, _nd in _td.nodes(data=True)]
        return _dl, _ret[_makspan].as_long()
    else:
        print('Unsat')
        return False, None

if __name__ == "__main__":
    """ 1. Data Input """
    _rp = os.path.dirname(os.path.abspath(__file__))

    # (1) DAG Data (json addr);
    _td = Dag_Json_Input(_rp + "/Idata/DAGs/Dag_1.json")
 
    # (2) Processor Data (json addr);
    _pd = Processor_Json_Input(_rp + "/Idata/Processor/Processor.json")

    _m = len(_pd)


    """ * Schedulability Verification """ 


    """ 3. Optimal Solver """
    #   - 1）Priority;
    #   - 2）Allocation;
    #   - 3）Offset;

    _st = time.time()

    _dl, _ms = DAG_Opt_Solver(_td, _m)

    _et = time.time()

    print(f"Opt: \t ret:{_ms} \t time cost:{_et - _st:.4f}")


    """ 4. Data Output """
    if _dl:
        # (1) DAG Fig;
        DAG_Fig_Output(_td, _rp + "/Odata/DAGs")

        # (2) Gantt Fig;
        Gantt_Fig_Output(_td, _dl,  _rp + "/Odata/Gantt")

        # (3) Schedule Table;
        Schedule_Tab_Output(_td, _dl,  _rp + "/Odata/Table")
