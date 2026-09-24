#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import numpy as np
import seaborn as sns
import multiprocessing
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import copy

ROOT_ADDR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_ADDR)

from DAG_Model import *
from Static_Scheduler import *
from Dynamic_Scheduler import *


def __exam(_td, _ta):
    _WS = WorkStation(copy.deepcopy(_td), copy.deepcopy(_ta))

    return max([_rx['ft'] for _rx in _WS.run()])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Opt Frame')

    parser.add_argument('-e', '--en', type=int, required=True, 
                            help='The number of experimental tests')
    parser.add_argument('-a', '--arch', type=str, required=True, 
                            help='Input the Arch json file address')
    parser.add_argument('-id', '--idata', type=str, required=True, 
                            help='Iterative data file input address')
    parser.add_argument('-rd', '--rdag', type=str, required=True, 
                            help='Input the Original DAG json file address')
    parser.add_argument('-pd', '--pdag', type=str, required=True, 
                            help='Input the Optimized  DAG json file address')
    parser.add_argument('-od', '--odata', type=str, required=True, 
                            help='Output the result fig address')

    args = parser.parse_args()

    _fig, _axs = plt.subplots(1, 3, figsize=(24, 6))

    _en = args.en

    # 处理相对路径：如果不是绝对路径，则相对于项目根目录
    rdag_path = args.rdag if os.path.isabs(args.rdag) else os.path.join(ROOT_ADDR, args.rdag)
    pdag_path = args.pdag if os.path.isabs(args.pdag) else os.path.join(ROOT_ADDR, args.pdag)
    arch_path = args.arch if os.path.isabs(args.arch) else os.path.join(ROOT_ADDR, args.arch)
    idata_path = args.idata if os.path.isabs(args.idata) else os.path.join(ROOT_ADDR, args.idata)

    _rd = Dag_Json_Input(rdag_path)
    _pd = Dag_Json_Input(pdag_path)
    _ta = Arch_Json_Input(arch_path)
    _idf = pd.read_csv(idata_path)
    
    with multiprocessing.Pool(processes=os.cpu_count()) as _pool:
        _ms_ori = list( _pool.starmap(__exam, [(_rd, _ta) for _ in range(_en)]) )
        _ms_opt = list( _pool.starmap(__exam, [(_pd, _ta) for _ in range(_en)]) )

    print(f"Ori:")
    print(f"\tMax:{max(_ms_ori):.2f}")
    print(f"\tMin:{min(_ms_ori):.2f}")
    print(f"\tStd:{np.std(_ms_ori):.2f}")
    print(f"\tAvg:{np.mean(_ms_ori):.2f}")

    print(f"Opt:")
    print(f"\tMax:{max(_ms_opt):.2f}")
    print(f"\tMin:{min(_ms_opt):.2f}")
    print(f"\tStd:{np.std(_ms_opt):.2f}")
    print(f"\tAvg:{np.mean(_ms_opt):.2f}")

    # axs[0].set_ylim(500000, 4000000)
    sns.lineplot(y=_ms_ori, x=range(_en), ax=_axs[0])

    # axs[1].set_ylim(500000, 4000000)
    sns.lineplot(y=_ms_opt, x=range(_en), ax=_axs[1])

    _sdd = list(_idf['opt_fit'])
    sns.lineplot( x = list(range(1, len(_sdd) + 1)), y = _sdd, ax=_axs[2] )

    # 处理输出文件路径：如果不是绝对路径，则相对于当前工作目录
    odata_path = args.odata if os.path.isabs(args.odata) else os.path.join(os.getcwd(), args.odata)
    odata_dir = os.path.dirname(odata_path)
    
    # 确保输出目录存在
    os.makedirs(odata_dir, exist_ok=True)
    
    plt.savefig(odata_path)
    print(f"结果图表已保存到: {odata_path}")
