import matplotlib.pyplot as plt
import Core as Core

""" 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。
一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

# Dag_color_list = {"M1_S1_C1": {0: "#BFE0E1",
#                                1: "#54D5DB"},
#                   "M1_S2_C1": {0: "#CFB4E1",
#                                1: "#B667DB",
#                                2: "#886BF0"},
#                   "M1_S1_C2": {0: "#E1B2E0",
#                                1: "#DB47D7"},
#                   "M1_S2_C2": {0: "#BED0A4",
#                                1: "#6EC700",
#                                2: "#00DB84"},
#                   "M2_S1_C1": {0: "#D9B89D",
#                                1: "darkorange"},
#                   "M2_S2_C1": {0: "#C2D2F2",
#                                1: "#5A84DB",
#                                2: "#2807E6"},
#                   "M2_S3_C1": {0: "#E6D5B8",
#                                1: "#E6DB10",
#                                2: "#EDC00C",
#                                3: "#D68A00",
#                                4: "#ED740C",
#                                5: "#E3400B",
#                                6: "#F70800"},
#                   }
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


color_dict = {
    0: '#1b9e77',
    1: '#d95f02',
    2: '#7570b3',
    3: '#e7298a'
}

Dag_color_list = {"M1_S1_C1": {0: "#D8D8D8",
                               1: "#D8D8D8"},
                  "M1_S2_C1": {0: "#b3e2cd",
                               1: "#b3e2cd",
                               2: "#b3e2cd"},
                  "M1_S1_C2": {0: "#fdcdac",
                               1: "#fdcdac"},
                  "M1_S2_C2": {0: "#fdcdac",
                               1: "#fdcdac",
                               2: "#fdcdac"},
                  "M2_S1_C1": {0: "#fdcdac",
                               1: "#fdcdac"},
                  "M2_S2_C1": {0: "#cbd5e8",
                               1: "#cbd5e8",
                               2: "#cbd5e8"},
                  "M2_S3_C1": {0: "#f4cae4",
                               1: "#f4cae4",
                               2: "#f4cae4",
                               3: "#f4cae4",
                               4: "#f4cae4",
                               5: "#f4cae4",
                               6: "#f4cae4"},
                  }


def show_dag_and_makespan(Core_Data_List, makespan_res, ax, xtikck_type, font_size):
    core_channel = 0
    core_name_list = []
    core_y_location_list = []
    xtick_size = 20
    ax.ticklabel_format(style='plain')

    # plt.ylabel("core-list", fontdict={'family': 'Times New Roman', 'size': 16})
    # makespan_res = self.get_makespan(Core_Data_List)

    # 'best': 0,  # 'upper right': 1,  # 'upper left': 2,  # 'lower left': 3,  # 'lower right': 4,  # 'right': 5,
    # 'center left': 6,     # 'center right': 7,    # 'lower center': 8,    # 'upper center': 9,    # 'center': 10,

    # 0: '#1b9e77', # 1: '#d95f02', # 2: '#7570b3', # 3: '#e7298a'

    temp_obj_list = [plt.scatter(0, 0, marker="s", color='#d95f02'), plt.scatter(0, 0, marker="s", color='#7570b3'), plt.scatter(0, 0, marker="s", color='#e7298a')]
    Flow_ID_List = ['DAG_1', 'DAG_2', 'DAG_3']
    plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', prop={'family': 'Times New Roman', 'size': xtick_size})   # plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', title=running_type, prop={'family': 'Times New Roman', 'size': 32})

    for x in Core_Data_List:
        core_name_list.append(x.Core_ID)
        for y in x.Core_Running_Task:
            if y['node'][1]['Node_ID'] in ['Job_29.1', 'Job_0']:
                continue
            # 默认 tick
            barh_width = y['end_time'] - y['start_time']
            barh_left = y['start_time']
            text_left = y['start_time'] + (y['end_time'] - y['start_time']) / 2

            if xtikck_type == 'TICK':
                barh_width = barh_width
                barh_left  = barh_left
                text_left  = text_left
                plt.xlabel("time-axis_(tick)", fontdict={'family': 'Times New Roman', 'size': xtick_size})
            elif xtikck_type == 'MS':
                barh_width = barh_width / 2260000
                barh_left  = barh_left  / 2260000
                text_left  = text_left  / 2260000
                plt.xlabel("time-axis_(ms)", fontdict={'family': 'Times New Roman', 'size': xtick_size})
            elif xtikck_type == 'US':
                barh_width = barh_width / 2260
                barh_left  = barh_left  / 2260
                text_left  = text_left  / 2260
                plt.xlabel("time-axis_(us)", fontdict={'family': 'Times New Roman', 'size': xtick_size})
            elif xtikck_type == 'NS':
                barh_width = barh_width / 2.260
                barh_left  = barh_left  / 2.260
                text_left  = text_left  / 2.260
                plt.xlabel("time-axis_(ns)", fontdict={'family': 'Times New Roman', 'size': xtick_size})
            ax.barh(y=core_channel, width=barh_width, height=1, left=barh_left, color=color_dict[y['node'][1]['Criticality']], edgecolor='gray')
            ax.text(y=core_channel, x=text_left, s='{0}'.format(y['node'][1]['Node_ID']), fontsize=font_size, family='Times New Roman', ha='center', va='center')

                # color_lable = Dag_color_list[y['dag_ID']][y["node"][1]["Flow_Num"]]
            # if y['node'][1]['Node_ID'].endswith('Job_29.1') or y['node'][1]['Node_ID'].endswith('Job_0'):
            #     ax.barh(y=core_channel * 1, width=3000, height=1, left=y['start_time'],
            #              color='white', edgecolor='white')
            # else:
            # dag_x.graph['Criticality']
        core_y_location_list.append(core_channel * 1)
        core_channel += 1
    temp_obj_list = []
    Flow_ID_List = []
    # 右上标记
    # for dag_id in Dag_ID_List:
    #     for flow_num, dag_flow_color in Dag_color_list[dag_id].items():
    #         if flow_num > 0:
    #             temp_obj_list.append(plt.scatter(-100000, 0, marker="s", color=dag_flow_color))
    #             Flow_ID_List.append("{0}".format(dag_id, flow_num))
        # temp_obj_list.append(plt.scatter(-100000, 0, marker="s", color=Dag_color_list[dag_id][0]))
        # Flow_ID_List.append("{0}_Other".format(dag_id))

    # font = font_manager.FontProperties(size=font_size)
    # plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', prop={'family': 'Times New Roman', 'size': 16})

    plt.yticks(core_y_location_list, core_name_list, fontproperties='Times New Roman', size=font_size)  # 设置y刻度:用文字来显示刻度
    # plt.xticks((0, makespan_res * 1.2), rotation=30)
    plt.xticks(fontproperties='Times New Roman', size=xtick_size)
    # plt.xticks(np.arange(makespan_res))
    if xtikck_type == 'TICK':
        plt.xlim(xmin=0, xmax=makespan_res * 1)
    elif xtikck_type == 'NS':
        plt.xlim(xmin=0, xmax=makespan_res / 2.260)
    # plt.xlim(xmin=0, xmax=makespan_res * 3)


def draw(d, node_name, start_time, end_time, processor, dag_name, core_num, filename, make_span, ax, Dag_ID_List=None):
    plt.cla()
    cores = [Core.Core(f'core_{i + 1}') for i in range(core_num)]
    node_ids = list(d.nodes)[:-1]
    for key, (node, start, end, p) in enumerate(zip(node_name, start_time, end_time, processor)):
        if node == 'S' or node == 'E':
            continue
        if Dag_ID_List is not None:
            dag_id = node[:8]
            nodeN = node[9:]
            cores[p].Insert_Task_Info(dag_id,
                                      node=(1, {'Node_ID': f'{nodeN}',
                                                'Flow_Num': d.nodes[f"{node_ids[key]}"]['flow_num']}),
                                      start_time=start,
                                      end_time=end
                                      )
        else:
            cores[p].Insert_Task_Info(dag_name,
                                      node=(1, {'Node_ID': f'{node}',
                                                'Flow_Num': d.nodes[str(key + 1)]['flow_num']}),
                                      start_time=start,
                                      end_time=end
                                      )

    if Dag_ID_List is not None:
        pass
    else:
        Dag_ID_List = [dag_name]

    show_dag_and_makespan(Dag_ID_List, cores, None, make_span, {}, 14, ax)
    # plt.show()


if __name__ == "__main__":
    Dag_ID_List = ['M1_S1_C1']
    core1 = Core.Core('c1')
    core1.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_0', 'Flow_Num': 0}), start_time=0, end_time=1000)
    core2 = Core.Core('c2')
    core2.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_1', 'Flow_Num': 0}), start_time=0, end_time=1000)
    core3 = Core.Core('c3')
    core3.Insert_Task_Info('M1_S1_C1', node=(1, {'Node_ID': 'job_2', 'Flow_Num': 1}), start_time=0, end_time=1000)
    show_dag_and_makespan(Dag_ID_List, [core1, core2, core3], None, 2000, {}, 14)
