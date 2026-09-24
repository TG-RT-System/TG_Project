import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
# 密度图

colore_dict = { 'SELF_S_improve':   "#f4cae4",
                'HE_improve':       "#D8D8D8",
                'WCET_improve':     "#b3e2cd",
                'HEET_improve':     "#fdcdac"}

colore_dd = {
    0.1: "#f4cae4",
    0.3: "#D8D8D8",
    0.5: "#b3e2cd"
}

with pd.ExcelFile("../Data/result_data_ori.xlsx") as data:
    all_sheet_names = data.sheet_names
    df = pd.read_excel(data, all_sheet_names[0], index_col=None, na_values=["NA"])
    DAG_list = []
    Jitter_Rate_list = [0.1, 0.3, 0.5]
    # for Flow_num_list in combinations(items, 5):
    #     print(Flow_num_list)

    for max_flow_num in range(4, 11):
        Flow_num_list = range(max_flow_num-1, max_flow_num)
        plt.figure()
        plt.grid(True)
        for Jitter_Rate in Jitter_Rate_list:
            CC = (df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'HE_2019'] -
                  df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'SELF_S']) \
                 / df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'HE_2019']
            # CC = (df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'HEFT'] -
            #       df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'SELF_S']) \
            #      / df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), 'HEFT']
            sns.kdeplot(CC, color=colore_dd[Jitter_Rate])
        # for items_k, items_v in colore_dict.items():
        #     sns.kdeplot(200 * df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), items_k], color=items_v)
        # Decoration
        plt.title('flow:{0}'.format(max_flow_num), fontsize=12)
        colore_id = [items_k for items_k, items_v in colore_dd.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dd[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 8})

        plt.show()
        plt.savefig('./3_31/Max-{0}.png'.format(max_flow_num, Jitter_Rate))
        # print( 'flow:{0}——jiter：{1}'.format(Flow_num_list, Jitter_Rate) )
        plt.close()
