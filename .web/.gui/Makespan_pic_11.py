import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import Core

""" 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

# Dag_color_list = {  "M1_S1_C1":     "silver",
#                     "M1_S2_C1":     "lightcoral",
#                     "M1_S1_C2":     "darkorange",
#                     "M1_S2_C2":     "lawngreen",
#                     "M2_S1_C1":     "lightseagreen",
#                     "M2_S2_C1":     "cornflowerblue",
#                     "M2_S3_C1":     "plum",
#                     "M2_S1_C2":     "pink",
#                     "M2_S2_C2":     "fuchsia",
#                     "M2_S3_C2":     "greenyellow",
#                     "C6_F6_T1_F0":  "lawngreen",
#                     "C6_F6_T1_F1":  "palevioletred",
#                     "C6_F6_T1_F2":  "royalblue",
#                     "C6_F6_T1_F3":  "blueviolet",
#                     "C6_F6_T1_F4":  "olive",
#                     "C6_F6_T1_F5":  "dodgerblue",
#                     "C6_F6_T2":     "indianred",
#                     "C6_F6_T3":     "tomato",
#                     "C6_F6_T4":     "green",
#                     'DAG_1':        "green",
#                     'DAG_2':        "indianred",
#                     'DAG_3':        "dodgerblue"}

# Dag_color_list = {  "M1_S1_C1":     {0:"silver",            1:"lawngreen"},
#                     "M1_S2_C1":     {0:"lightcoral",        1:"palevioletred",      2:"royalblue"},
#                     "M1_S1_C2":     {0:"silver",            1:"lawngreen"},                             #{0:
#                     "M1_S2_C2":     {0:"lightcoral",        1:"palevioletred",      2:"royalblue"},     #{0:
#                     "M2_S1_C1":     {0:"lightseagreen",     1:"darkorange"},
#                     "M2_S2_C1":     {0:"cornflowerblue",    1:"lawngreen",           2:"blueviolet"},
#                     "M2_S3_C1":     {0:"plum",              1:"pink",                2:"fuchsia",       3:"olive",
#                                      4:"dodgerblue",        5: "indianred",          6:"tomato"},
#                     "M2_S1_C2":     {0:"lightseagreen",     1:"darkorange"},
#                     "M2_S2_C2":     {0:"cornflowerblue",    1:"lawngreen",           2:"blueviolet"},
#                     "M2_S3_C2":     {0:"plum",              1:"pink",                2:"fuchsia",       3:"olive",
#                                      4:"dodgerblue",        5: "indianred",          6:"tomato"}
#                     }
Dag_color_list = {"M1_S1_C1": {0: "#BFE0E1",
                               1: "#54D5DB"},
                  "M1_S2_C1": {0: "#CFB4E1",
                               1: "#B667DB",
                               2: "#886BF0"},
                  "M1_S1_C2": {0: "#E1B2E0",
                               1: "#DB47D7"},
                  "M1_S2_C2": {0: "#BED0A4",
                               1: "#6EC700",
                               2: "#00DB84"},
                  "M2_S1_C1": {0: "#D9B89D",
                               1: "darkorange"},
                  "M2_S2_C1": {0: "#C2D2F2",
                               1: "#5A84DB",
                               2: "#2807E6"},
                  "M2_S3_C1": {0: "#E6D5B8",
                               1: "#E6DB10",
                               2: "#EDC00C",
                               3: "#D68A00",
                               4: "#ED740C",
                               5: "#E3400B",
                               6: "#F70800"},
                  }

def show_dag_and_makespan(Dag_ID_List, Core_Data_List, DAG_dict, makespan_res, param_dict, font_size ):
    plt.clf()
    plt.cla()
    # plt.figure(num=None, figsize=(256, 6), dpi=80, facecolor='w', edgecolor='k')
    core_channel = 0
    core_name_list = []
    core_y_location_list = []
    plt.xlabel("time-axis")
    plt.ylabel("core-list")
    # makespan_res = self.get_makespan(Core_Data_List)
    for x in Core_Data_List:
        core_name_list.append(x.Core_ID)
        for y in x.Core_Running_Task:
            color_lable = Dag_color_list[y['dag_ID']][y["node"][1]["Flow_Num"]]
            plt.barh(y=core_channel * 3, width=y['end_time'] - y['start_time'], height=2, left=y['start_time'], color=color_lable, edgecolor='gray')
            plt.text(x=y['start_time'] + (y['end_time']-y['start_time']) / 2, y=core_channel * 3, s='{0}'.format( y['node'][1]['Node_ID']+'/' )[4:-1], fontsize=font_size)
                     # s='{0}'.format((y['node'])), fontsize=font_size)

        core_y_location_list.append(core_channel * 3)
        core_channel += 1
    temp_obj_list = []
    Flow_ID_List = []
    for dag_id in Dag_ID_List:
        for flow_num, dag_flow_color in Dag_color_list[dag_id].items():
            temp_obj_list.append( plt.scatter(0, 0, marker="s", color=dag_flow_color) )
            Flow_ID_List.append( "{0}_Flow{1}".format(dag_id, flow_num) )

    # temp_obj_list = [plt.scatter(0, 0, marker="s", color=Dag_color_list[dag_id]) for dag_id in Dag_ID_List]
    font = font_manager.FontProperties(size=font_size)
    # plt.legend(temp_obj_list, Dag_ID_List, loc='upper right', prop=font)
    plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', prop=font)
    plt.yticks(core_y_location_list, core_name_list)  # 设置y刻度:用文字来显示刻度
    # plt.xticks((0, makespan_res * 1.2), rotation=30)
    # plt.xticks(np.arange(makespan_res))
    plt.xlim(xmin=0, xmax=makespan_res*1.15)
    plt.title("makespan:{0}={1:.4f}ms".format(makespan_res, makespan_res / 2260000), fontsize=font_size, color="black", weight="light", ha='left', x=0)
    # plt.savefig('./fig/{0}_{1}_{2}_{3}.png'.format(param_dict["Running_Type"],param_dict["Core_Num"],param_dict["Arrive_Time"],param_dict["DAG_Set_ID"]))
    plt.show()

"""
def show_dag_and_makespan(Dag_ID_List, Core_Data_List, DAG_dict, makespan_res, font_size ):
    # plt.figure(num=None, figsize=(256, 6), dpi=80, facecolor='w', edgecolor='k')
    core_channel = 0
    core_name_list = []
    core_y_location_list = []
    plt.xlabel("time-axis")
    plt.ylabel("core-list")
    # makespan_res = self.get_makespan(Core_Data_List)
    for x in Core_Data_List:
        core_name_list.append(x.Core_ID)
        for y in x.Core_Running_Task:
            plt.barh(y=core_channel * 3, width=y['end_time'] - y['start_time'], height=2, left=y['start_time'], color=Dag_color_list[y['dag_ID']], edgecolor='gray')
            plt.text(x=y['start_time'] + (y['end_time']-y['start_time']) / 2, y=core_channel * 3, s='{0}'.format( y['node'][1]['Node_ID']+'/' )[4:-1], fontsize=font_size)
                     # s='{0}'.format((y['node'])), fontsize=font_size)

        core_y_location_list.append(core_channel * 3)
        core_channel += 1
    temp_obj_list = [plt.scatter(0, 0, marker="s", color=Dag_color_list[dag_id]) for dag_id in Dag_ID_List]
    font = font_manager.FontProperties(size=font_size)
    plt.legend(temp_obj_list, Dag_ID_List, loc='upper right', prop=font)
    plt.yticks(core_y_location_list, core_name_list)  # 设置y刻度:用文字来显示刻度

    plt.title("makespan:{0}={1:.4f}ms".format(makespan_res, makespan_res / 2260000), fontsize=font_size, color="black", weight="light", ha='left', x=0)
    # plt.show()
"""

    # def show_dag_and_makespan(self, Core_Data_List):
    #     figure(num=None, figsize=(256, 6), dpi=80, facecolor='w', edgecolor='k')
    #     core_channel = 0
    #     font_size = 5
    #     core_name_list = []
    #     core_y_location_list = []
    #     plt.xlabel("time-axis")
    #     plt.ylabel("core-list")
    #     makespan_res = self.get_makespan(Core_Data_List)
    #     for x in Core_Data_List:
    #         core_name_list.append(x.Core_ID)
    #         for y in x.Core_Running_Task:
    #             plt.barh(y=core_channel * 3, width=y['end_time']-y['start_time'], height=2,
    #                      left=y['start_time'], color=Dag_color_list[y['dag_ID']], edgecolor='gray')
    #             plt.text(x=y['start_time'] + y['node'][1]['WCET'] / 2, y=core_channel * 3,
    #                      s='{0}'.format((y['node'][1]['Node_ID'] + '/')[4:-1]), fontsize=makespan_res/100000)
    #         core_y_location_list.append(core_channel * 3)
    #         core_channel += 1
    #     temp_obj_list = []
    #     temp_dag_id_list = []
    #     for x in self.Dag_List:
    #         temp_dag_id_list.append( x.graph['DAG_ID'] )
    #         temp_obj_list.append( plt.scatter(0, 0, marker="s", color=Dag_color_list[x.graph['DAG_ID']]) )
    #     font = font_manager.FontProperties(size=makespan_res/200000)
    #     plt.legend(temp_obj_list, temp_dag_id_list, loc='upper right', prop=font)
    #     plt.yticks(core_y_location_list, core_name_list)            # 设置y刻度:用文字来显示刻度
    #
    #     plt.title("makespan:{0}={1:.4f}ms".format(makespan_res, makespan_res/2260000),
    #         fontsize=font_size, color="black", weight="light", ha='left', x=0)
    #     plt.show()


if __name__ == "__main__":
    Dag_ID_List = ['DAG_1', 'DAG_2', 'DAG_3']
    core1 = Core.Core('c1')
    core1.Insert_Task_Info('DAG_1', node=(1, {'Node_ID': 'job_0'}), start_time=0, end_time=1000)
    core2 = Core.Core('c2')
    core2.Insert_Task_Info('DAG_2', node=(1, {'Node_ID': 'job_1'}), start_time=0, end_time=1000)
    core3 = Core.Core('c3')
    core3.Insert_Task_Info('DAG_3', node=(1, {'Node_ID': 'job_2'}), start_time=0, end_time=1000)
    show_dag_and_makespan(Dag_ID_List, [core1, core2, core3], makespan_res=2000)

