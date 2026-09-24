import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi

# 密度图

colore_dict = { 'SELF_S_improve':   "#f4cae4",
                'HE_improve':       "#D8D8D8",
                'WCET_improve':     "#b3e2cd",
                'HEET_improve':     "#fdcdac"}

colore_dict_1_1 = {0.1: "red",
                   0.3: "green",
                   0.5: "blue"}

colore_dict_2_1 = {'SELF_D_improve':   "red",
                   'SELF_S_improve':   "green"}

colore_dict_2_2 = {'SELF_D_improve':   "red",
                   'HE_improve':       "green",
                   'WCET_improve':     "blue",
                   'HEET_improve':     "yellow"}


# sns.kdeplot((df.loc[:, 'SELF_S_improve'] - df.loc[:, 'SELF_D_improve'] )/ df.loc[:, 'SELF_S_improve'], color="")
with pd.ExcelFile("../Data/result_data_ori_4_5.xlsx") as data:
    all_sheet_names = data.sheet_names
    df = pd.read_excel(data, all_sheet_names[0], index_col=None, na_values=["NA"])
    DAG_list = []
    # """
    # ############## (1.1) 静态算法与基线_分  ################
    """
    plt.figure(figsize=(20, 10))
    for items_k, items_v in colore_dict_1_1.items():
        sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == items_k), 'SELF_S_improve'], color=items_v)
    plt.grid(True)
    colore_id = [items_k for items_k, items_v in colore_dict_1_1.items()]
    colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict_1_1[items_id]) for items_id in colore_id]
    colore_id = [f'jitter:{100 * c_id}%' for c_id in colore_id]
    plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 16})

    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[2].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[2].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[2].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

    print(f'JITTER_10_improve_10:{100 * len( df.loc[(df["Jitter_Rate"] == 0.1) & (df["SELF_S_improve"] > 0.1)]) / len(df.loc[(df["Jitter_Rate"] == 0.1)])}')
    print(f'JITTER_10_improve_15:{100 * len( df.loc[(df["Jitter_Rate"] == 0.1) & (df["SELF_S_improve"] > 0.15)]) / len(df.loc[(df["Jitter_Rate"] == 0.1)])}')

    print(f'JITTER_30_improve_10:{100 * len( df.loc[(df["Jitter_Rate"] == 0.3) & (df["SELF_S_improve"] > 0.1)]) / len(df.loc[(df["Jitter_Rate"] == 0.3)])}')
    print(f'JITTER_30_improve_15:{100 * len( df.loc[(df["Jitter_Rate"] == 0.3) & (df["SELF_S_improve"] > 0.15)]) / len(df.loc[(df["Jitter_Rate"] == 0.3)])}')

    print(f'JITTER_50_improve_10:{100 * len( df.loc[(df["Jitter_Rate"] == 0.5) & (df["SELF_S_improve"] > 0.1)]) / len(df.loc[(df["Jitter_Rate"] == 0.5)])}')
    print(f'JITTER_50_improve_15:{100 * len( df.loc[(df["Jitter_Rate"] == 0.5) & (df["SELF_S_improve"] > 0.15)]) / len(df.loc[(df["Jitter_Rate"] == 0.5)])}')

    plt.savefig('./3_31/(1_1)S_Huawei-{0}.png'.format(0))
    plt.close()
    """

    # ############## (1.2) 静态算法与基线_总  ################
    """
    plt.figure(figsize=(20, 10))
    sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red')
    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")
    print(f'improve_10:{100 * len(df.loc[(df["SELF_S_improve"] > 0.10)]) / len(df.index)}')
    print(f'improve_15:{100 * len(df.loc[(df["SELF_S_improve"] > 0.15)]) / len(df.index)}')
    plt.grid(True)
    plt.savefig('./3_31/(1_2)S_Huawei-{0}.png'.format(0))
    plt.close()
    """

    """
    # ############## (2.1) 动静态算法对比  ################
    plt.figure(figsize=(20, 10))
    for items_k, items_v in colore_dict_2_1.items():
        sns.kdeplot(100 * df.loc[:, items_k], color=items_v)
    plt.grid(True)
    colore_id = [items_k for items_k, items_v in colore_dict_2_1.items()]
    colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict_2_1[items_id]) for items_id in colore_id]
    plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 16})

    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[0].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

    # 获取概率密度最大值的位置
    max_idx = np.argmax(sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[1])
    x_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[0][max_idx]
    y_max = sns.kdeplot(100 * df.loc[:, 'SELF_S_improve'], color='red').get_lines()[1].get_data()[1][max_idx]
    # 显示结果
    print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

    print(f'SELF_S_improve:{len(df.loc[(df["SELF_S_improve"] > 0.15)]) / len(df.index)}')
    print(f'SELF_D_improve:{len(df.loc[(df["SELF_D_improve"] > 0.15)]) / len(df.index)}')

    plt.savefig('./3_31/(2_1)SD-{0}.png'.format(0))
    # plt.show()
    plt.close()
    """

    # """
    # ############## (2.2) 业界算法对比  ################
    for jitter in [0.1, 0.3, 0.5]:
        plt.figure(figsize=(20, 10))
        for key, (items_k, items_v) in enumerate(colore_dict_2_2.items()):
            sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v)
            print(f'model_{items_k}__Jitter_{jitter}_improve_10:{100 * len(df.loc[(df["Jitter_Rate"] == jitter) & (df[items_k] > 0.10)]) / len(df.loc[(df["Jitter_Rate"] == jitter)])}')
            print(f'model_{items_k}__Jitter_{jitter}_improve_15:{100 * len(df.loc[(df["Jitter_Rate"] == jitter) & (df[items_k] > 0.15)]) / len(df.loc[(df["Jitter_Rate"] == jitter)])}')
            # 获取概率密度最大值的位置
        max_idx = np.argmax(sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[0].get_data()[1])
        x_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[0].get_data()[0][max_idx]
        y_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[0].get_data()[1][max_idx]
        print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

        max_idx = np.argmax(sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[1].get_data()[1])
        x_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[1].get_data()[0][max_idx]
        y_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[1].get_data()[1][max_idx]
        print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

        max_idx = np.argmax(sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[2].get_data()[1])
        x_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[2].get_data()[0][max_idx]
        y_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[2].get_data()[1][max_idx]
        print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

        max_idx = np.argmax(sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[3].get_data()[1])
        x_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[3].get_data()[0][max_idx]
        y_max = sns.kdeplot(100 * df.loc[(df['Jitter_Rate'] == jitter), items_k], color=items_v).get_lines()[3].get_data()[1][max_idx]
        print(f"The maximum density is {y_max:.4f} at x = {x_max:.4f}")

        plt.grid(True)
        colore_id = [items_k for items_k, items_v in colore_dict_2_2.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict_2_2[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 16})
        plt.savefig('./3_31/(2_2)Industry_J-{0}.png'.format(jitter))
        plt.show()
        plt.close()
    # """
    """
    jitter_rate_list = [0.1, 0.3, 0.5]

    for Jitter_Rate in jitter_rate_list:
        plt.figure()
        for items_k, items_v in colore_dict.items():
            sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate), items_k], color=items_v)
        # Decoration
        plt.title('jiter:{0}'.format(Jitter_Rate), fontsize=12)
        colore_id = [items_k for items_k, items_v in colore_dict.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 8})
        plt.show()
    """
    """
    flow_num_list = range(3, 11)
    for Jitter_Rate in jitter_rate_list:
        # for Flow_num in flow_num_list:
        plt.figure()
        for items_k, items_v in colore_dict.items():
            sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate), items_k], color=items_v)
        # Decoration
        # plt.title('flow:{0}——jiter:{1}'.format(Flow_num, Jitter_Rate), fontsize=12)
        colore_id = [items_k for items_k, items_v in colore_dict.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 8})
        plt.show()
        # plt.savefig('./3_31/J-{0}.png'.format(Jitter_Rate))
        # print( 'flow:{0}——jiter：{1}'.format(Flow_num, Jitter_Rate) )
    """
    # """
    """
    jitter_rate_list = [0.1, 0.3, 0.5]
    # flow_num_list = range(3, 11)
    for Jitter_Rate in jitter_rate_list:
        # for Flow_num in flow_num_list:
        plt.figure()
        for items_k, items_v in colore_dict.items():
            sns.kdeplot(df.loc[(df['Jitter_Rate'] == Jitter_Rate) & (df['Flow_num'] == Flow_num), items_k], color=items_v)
        # Decoration
        plt.title('flow:{0}——jiter:{1}'.format(Flow_num, Jitter_Rate), fontsize=12)
        colore_id = [items_k for items_k, items_v in colore_dict.items()]
        colore_list = [plt.scatter(0, 0, marker="s", color=colore_dict[items_id]) for items_id in colore_id]
        plt.legend(colore_list, colore_id, loc='upper right', title='', prop={'family': 'Times New Roman', 'size': 8})
        plt.savefig('./3_31/F-{0}_J-{1}.png'.format(Flow_num, Jitter_Rate))
        print( 'flow:{0}——jiter：{1}'.format(Flow_num, Jitter_Rate) )
    """