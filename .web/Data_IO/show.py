#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import json
import graphviz as gz
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from datetime import datetime
from Tools.Parameter import *

""" 1. Data Input """
# (0) Data Input (json)
def Data_Json_Input(_file:str):
    with open(_file, "r") as _f:
    # with open(_file, "r", encoding="utf-8") as _f:
        _r = json.load(_f)
    return _r

# (1) DAG Input (json)
def Dag_Json_Input(_file:str):
    _rd = nx.DiGraph()
    with open(_file, "r") as _f:
        _td = json.load(_f)
        _rd.add_edges_from(_td['G']['E'])
        _rd.add_nodes_from([(int(_ni), _nd) for _ni, _nd in _td['G']['V'].items()])
        _rd.graph |= {'T': _td['T'], 'D': _td['D'], 'ID':_td['ID']}
    return _rd

# (2) Arch Input (json)
def Arch_Json_Input(_file:str):
    with open(_file, "r") as _f:
    # with open(_file, "r", encoding="utf-8") as _f:
        _r = json.load(_f)
    return _r

""" 2. Data Output """
# (1) Task Output (json)
def Dag_Json_Output(_td, _id, _file:str):
    _rd = {
            "ID": _id,
            "T": _td.graph["T"], 
            "D": _td.graph["D"],
            "G":{
                "V": {str(_ni): _td.nodes[_ni] for _ni in _td.nodes()},
                "E": list(_td.edges())
            }
          }
    with open(f"{_file}/{_id}.json", "w", encoding="utf-8") as _f:
        json.dump(_rd, _f, indent=4, ensure_ascii=False) 

# (2) Resource Output (json)

# (2) DAG fig Output (png)
def DAG_Fig_Output(_rd, _file:str):
    dot = gz.Digraph() # format='png', node_attr={'shape': 'box'}, edge_attr={'labeldistance': "10.5"}
    dot.attr(rankdir='LR')
    for _ni, _nd in _rd.nodes(data=True):
        dot.node(f'{_ni}', 
                 f'''{_nd["INDEX"]}''',
                #  \nW:{_nd["W"]}\nB:{_nd["B"]}''', 
                 color='black',  shape='polygon', style='rounded')  # shape='box'        
    for _ep, _es in _rd.edges():
        dot.edge(f'{_ep}', f'{_es}')
    dot.render( filename=f"{_file}/{_rd.graph['ID']}", 
                format="png",   # 1.generate png file
                # format="pdf",   # 2.generate pdf file
                view=False)

# (3) Gantt
def Gantt_Fig_Output(_rd, _dl:list, _file:str, solver_name:str=""):
    # for _ni, _st, _ct, _ai in _dl:
    #     if 0 < _ct:
    #         plt.barh(y=_ai, width=_ct, height=0.3, left=_st, edgecolor='black', color="white")
    #         plt.text(s=f'{_ni}\n{_ct}', y=_ai, x=_st + _ct / 2, fontsize=8,  ha='center', va='center',)
    # filename = f"{_rd.graph['ID']}_{solver_name}.png" if solver_name else f"{_rd.graph['ID']}.png"
    # plt.savefig(f"{_file}/{filename}")
    # plt.savefig(f"./Odata/Gantt_{_file}.png")
    # plt.savefig(f"{_file}/{_rd.graph['ID']}.png")
    # 按核心分组任务
    core_tasks = {}
    for _ni, _st, _ct, _ai in _dl:
        if _ai not in core_tasks:
            core_tasks[_ai] = []
        core_tasks[_ai].append((_ni, _st, _ct))
    # 按核心编号排序
    core_ids = sorted(core_tasks.keys())
    plt.figure(figsize=(10, 2 + 0.5 * len(core_ids)))
    for idx, core in enumerate(core_ids):
        tasks = sorted(core_tasks[core], key=lambda x: x[1])
        for _ni, _st, _ct in tasks:
            plt.barh(y=idx, width=_ct, height=0.4, left=_st, edgecolor='black', color="white")
            plt.text(x=_st + _ct/2, y=idx, s=f"{_ni}/{_ct}", va='center', ha='center', fontsize=8)
    plt.yticks(range(len(core_ids)), [f"Core {core}" for core in core_ids])
    plt.xlabel("Time")
    plt.ylabel("Core")
    plt.title(f"Gantt Chart ({solver_name.upper()})")
    plt.tight_layout()
    filename = f"{_rd.graph['ID']}_{solver_name}.png" if solver_name else f"{_rd.graph['ID']}.png"
    plt.savefig(f"{_file}/{filename}")
    plt.close()

# (4) Gantt fig Output
def Gantt_Fig_Output_P(_dl):
    _title = '123'
    # 1. 按核心分组
    core_tasks = {}
    for _ni, _st, _ct, _ai in _dl:
        if _ai not in core_tasks:
            core_tasks[_ai] = []
        core_tasks[_ai].append((_ni, _st, _ct))

    # 2. 颜色方案
    core_palette = ['#f7f1de', '#81b19c', '#3498db', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c', '#34495e']
    core_ids = sorted(core_tasks.keys())
    core_to_color = {cid: core_palette[i % len(core_palette)] for i, cid in enumerate(core_ids)}

    # 3. 生成bar
    fig = go.Figure()
    bar_height = 0.50   # 设置纵坐标宽度
    for core in core_ids:
        y_val = f"Core {core}"
        color = core_to_color[core]
        for _ni, _st, _ct in core_tasks[core]:
            if _ct <= 0:
                continue  # 跳过执行时间为0的任务
            fig.add_trace(go.Bar(
                x=[_ct],
                y=[y_val],
                base=[_st],
                orientation='h',
                marker_color=color,
                marker_line_color='black',
                marker_line_width=1,    # 每个节点线宽粗
                text=f"{_ni}({_ct})",
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(color='black', size=16, family='Arial'),
                hovertext=f"Task {_ni} (执行时间{_ct})",
                hoverinfo='text',
                width=bar_height
            ))

    # 4. 布局美化，背景色灰色
    fig.update_layout(
        barmode='stack',
        title=f"Gantt: {_title}",
        xaxis_title='Time',
        yaxis=dict(
            categoryorder='array',
            categoryarray=[f"Core {cid}" for cid in core_ids],
            showline=True,
            linecolor='black',
            linewidth=2,
            gridcolor='black',
            gridwidth=0.5
        ),
        xaxis=dict(
            showline=True,
            linecolor='black',
            linewidth=2,
            gridcolor='black',
            gridwidth=0.5
        ),
        showlegend=False,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        bargap=0.3  # 行间距
    )

    return fig
    # 5. 保存为png
    # if not os.path.exists(_file):
    #     os.makedirs(_file)
    # if solver_name:
    #     out_png = os.path.join(_file, f"{_rd.graph['ID']}_{solver_name}.png")
    # else:
    #     out_png = os.path.join(_file, f"{_rd.graph['ID']}.png")
    # pio.write_image(fig, out_png, format='png')
    # print(f"Gantt图已保存到: {out_png}")

# (5) Schedule table Output (json) 
def Schedule_Tab_Output(_rd, _dl:list, _file:str, solver_name:str=""):
    filename = f"{_rd.graph['ID']}_{solver_name}.json" if solver_name else f"{_rd.graph['ID']}.json"
    with open(f"{_file}/{filename}", "w", encoding="utf-8") as _f:
        json.dump({_n: {'s': _s, 'c': _c, 'a': _a} for _n, _s, _c, _a in _dl}, _f, indent=4, ensure_ascii=False)

import glob
if __name__ == "__main__":
    for __fp in glob.glob(os.path.join( os.path.dirname(os.path.abspath(__file__)) , "*.json")):
        print("--------------------------------")
        print(__fp)
        _td = Dag_Json_Input(__fp)
        dag_topology_initial(_td)
        print(_td.graph)
        DAG_Fig_Output(_td, os.path.dirname(__fp))

# 1. Output DAG Fig
# DAG_Fig_Output(_td, "/home/fyj/Project/TG-RT-System/Data/Odata/DAGs")
# 1. Output Gantt Fig
# Gantt_Fig_Output(_td, _dl, "/home/fyj/Project/TG-RT-System/Data/Odata/Gantt", f"z3_min")
# gantt_data = [(n, bt, ft - bt, a) for item in _dl if len(item) == 9 for n, w, b, a, p, rt, bt, ft, et in [item]]
# table_data = [(n, bt, et, a) for item in _dl if len(item) == 9 for n, w, b, a, p, rt, bt, ft, et in [item]]
# Gantt_Fig_Output(_td, gantt_data, os.path.join(_rp, "Odata/Gantt"), f"z3_max")
# Schedule_Tab_Output(_td, table_data, os.path.join(_rp, "Odata/Table"), f"z3_max")
