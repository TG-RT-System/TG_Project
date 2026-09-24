import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 密度图

# colore_dict = { 'SELF_D_improve':   '#5F9EA0',
#                 'SELF_S_improve':   "#f4cae4",
#                 'HE_improve':       "#D8D8D8",
#                 'WCET_improve':     "#b3e2cd",
#                 'HEET_improve':     "#fdcdac"}

colore_dict = { 'SELF_D_improve':   'red',
                'SELF_S_improve':   'green',}

with pd.ExcelFile("../Data/result_data_ori.xlsx") as data:
    all_sheet_names = data.sheet_names
    df = pd.read_excel(data, all_sheet_names[0], index_col=None, na_values=["NA"])
    DAG_list = []

    jitter_rate_list = [0.1, 0.3, 0.5]
    # flow_num_list = range(3, 4)
    for Jitter_Rate in jitter_rate_list:
        # for Flow_num in flow_num_list:
        plt.figure()
        for items_k, items_v in colore_dict.items():
            ret_max = sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate), items_k] * 100, color=items_v)

        x0 = ret_max.lines[0].get_xdata()  # Get the x data of the distribution
        y0 = ret_max.lines[0].get_ydata()  # Get the y data of the distribution

        x1 = ret_max.lines[1].get_xdata()  # Get the x data of the distribution
        y1 = ret_max.lines[1].get_ydata()  # Get the y data of the distribution

        print(f"line0:---x:{x0[np.argmax(y0)]}---y:{y0[np.argmax(y0)]}")
        print(f"line1:---x:{x1[np.argmax(y1)]}---y:{y1[np.argmax(y1)]}")

        tcd_m = df.loc[df['Jitter_Rate'] == Jitter_Rate, 'SELF_D_improve'].size
        tcd_10_z = df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['SELF_D_improve'] > 0.1), 'SELF_D_improve'].size
        tcd_15_z = df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['SELF_D_improve'] > 0.15), 'SELF_D_improve'].size
        print(f'DY----10% upon {100 * tcd_10_z / tcd_m }----15% upon {100 * tcd_15_z / tcd_m }')
        tcs_m = df.loc[(df['Jitter_Rate'] == Jitter_Rate), 'SELF_S_improve'].size
        tcs_10_z = df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['SELF_S_improve'] > 0.1), 'SELF_S_improve'].size
        tcs_15_z = df.loc[(df['Jitter_Rate'] == Jitter_Rate)  & (df['SELF_S_improve'] > 0.15), 'SELF_S_improve'].size
        print(f'ST--10% upon {100 * tcs_10_z / tcs_m }----15% upon {100 * tcs_15_z / tcs_m }')

        # Decoration
        plt.title('jiter:{0}'.format(Jitter_Rate), fontsize=12)
        plt.grid(True)

        colore_id = [items_k for items_k, items_v in colore_dict.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict[items_id]) for items_id in colore_id]

        plt.legend(colore_list, colore_id, loc='upper right', title='',
                   prop={'family': 'Times New Roman', 'size': 12})

        plt.show()


    # colore_list = [plt.scatter(0, 0, marker="s", color='green'),  plt.scatter(0, 0, marker="s", color='red')]
    # colore_id = ['FP', 'LP']

    # plt.show()

