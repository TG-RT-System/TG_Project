import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
# 密度图

colore_dict = {'SELF_D_improve':   "#f4cae4",
               'HE_improve':       "#D8D8D8",
               'WCET_improve':     "#b3e2cd",
               'HEET_improve':     "#fdcdac"}

with pd.ExcelFile("../Data/result_data_ori_4_5.xlsx") as data:
    all_sheet_names = data.sheet_names
    df = pd.read_excel(data, all_sheet_names[0], index_col=None, na_values=["NA"])
    DAG_list = []
    Jitter_Rate_list = [0.1, 0.3, 0.5]
    Flow_num_list = [4, 5]
    for Jitter_Rate in Jitter_Rate_list:
        plt.figure()
        for items_k, items_v in colore_dict.items():
            # sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'].isin(Flow_num_list)), items_k], color=items_v)
            sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate), items_k], color=items_v)
        # Decoration
        plt.title('flow:{0}——jiter:{1}'.format(Flow_num_list, Jitter_Rate), fontsize=12)
        colore_id = [items_k for items_k, items_v in colore_dict.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 8})
        plt.show()
        # plt.savefig('./3_31/F-{0}_J-{1}.png'.format(Flow_num_list, Jitter_Rate))
        # print( 'flow:{0}——jiter：{1}'.format(Flow_num_list, Jitter_Rate) )
