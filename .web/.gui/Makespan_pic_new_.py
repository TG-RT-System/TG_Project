import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import Core as Core

""" 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

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
                  "M2_S1_C2": {0: "#D9B89D",
                               1: "darkorange"},
                  "M2_S2_C2": {0: "#C2D2F2",
                               1: "#5A84DB",
                               2: "#2807E6"},
                  "M2_S3_C2": {0: "#E6D5B8",
                               1: "#E6DB10",
                               2: "#EDC00C",
                               3: "#D68A00",
                               4: "#ED740C",
                               5: "#E3400B",
                               6: "#F70800"},

                  }

# Dag_color_list = {"M1_S1_C1": {0: "#D8D8D8",
#                                1: "#b3e2cd"},
#                   "M1_S2_C1": {0: "#D8D8D8",
#                                1: "#fdcdac",
#                                2: "#cbd5e8"},
#                   "M1_S1_C2": {0: "#D8D8D8",
#                                1: "#b3e2cd"},
#                   "M1_S2_C2": {0: "#D8D8D8",
#                                1: "#fdcdac",
#                                2: "#cbd5e8"},
#                   "M2_S1_C1": {0: "#D8D8D8",
#                                1: "#b3e2cd"},
#                   "M2_S2_C1": {0: "#D8D8D8",
#                                1: "#fdcdac",
#                                2: "#cbd5e8"},
#                   "M2_S3_C1": {0: "#D8D8D8",
#                                1: "#b3e2cd",
#                                2: "#fdcdac",
#                                3: "#cbd5e8",
#                                4: "#f4cae4",
#                                5: "#e6f5c9",
#                                6: "#fff2ae"},
#                   }

def show_dag_and_makespan(Dag_ID_List, Core_Data_List, font_size):
    plt.clf()
    plt.cla()
    core_channel = 0
    core_name_list = []
    core_y_location_list = []
    # plt.xlabel("time-axis", fontdict={'family': 'Times New Roman', 'size': 16})
    plt.ylabel("core-list", fontdict={'family': 'Times New Roman', 'size': 16})
    # makespan_res = self.get_makespan(Core_Data_List)
    for x in Core_Data_List:
        core_name_list.append(x.Core_ID)
        for y in x.Core_Running_Task:
            color_lable = Dag_color_list[y['dag_ID']][y["node"][1]["Flow_Num"]]

            if (y['node'][1]['Node_ID'] != 'Job_29.1') and (y['node'][1]['Node_ID'] != 'Job_0'):
                plt.barh(y=core_channel * 1, width=y['end_time'] - y['start_time'], height=1, left=y['start_time'],
                         color=color_lable, edgecolor='gray')
                plt.text(x=y['start_time'] + (y['end_time'] - y['start_time']) / 2, y=core_channel,
                         s='{0}'.format(y['node'][1]['Node_ID'] + '/')[4:-1], fontsize=font_size,
                         family='Times New Roman', ha='center', va='center')

        core_y_location_list.append(core_channel * 1)
        core_channel += 1
    temp_obj_list = []
    Flow_ID_List = []
    # 右上标记
    for dag_id in Dag_ID_List:
        for flow_num, dag_flow_color in Dag_color_list[dag_id].items():
            if flow_num > 0:
                temp_obj_list.append(plt.scatter(-100000, 0, marker="s", color=dag_flow_color))
                Flow_ID_List.append("{0}_Flow{1}".format(dag_id, flow_num))
        temp_obj_list.append(plt.scatter(-100000, 0, marker="s", color=Dag_color_list[dag_id][0]))
        Flow_ID_List.append("{0}_Other".format(dag_id))

    font = font_manager.FontProperties(size=font_size)
    plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', prop={'family': 'Times New Roman', 'size': 16})
    plt.yticks(core_y_location_list, core_name_list, fontproperties='Times New Roman', size=16)  # 设置y刻度:用文字来显示刻度
    # plt.xticks((0, makespan_res * 1.2), rotation=30)
    plt.xticks(fontproperties='Times New Roman', size=16)
    # plt.xticks(np.arange(makespan_res))
    # plt.xlim(xmin=0, xmax=makespan_res * 1.2)
    plt.xlim(xmin=0, xmax=2260000)
    plt.show()

if __name__ == "__main__":
    Dag_ID_List = ['M1_S1_C1']
    core1 = Core.Core('c1')
    core1.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_0', 'Flow_Num': 0}), start_time=0, end_time=1000)
    core2 = Core.Core('c2')
    core2.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_1', 'Flow_Num': 0}), start_time=0, end_time=1000)
    core3 = Core.Core('c3')
    core3.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_2', 'Flow_Num': 1}), start_time=0, end_time=1000)
    show_dag_and_makespan(Dag_ID_List, [core1, core2, core3], None, 2000, {}, 14)
