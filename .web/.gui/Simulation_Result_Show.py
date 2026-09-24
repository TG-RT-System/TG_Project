import matplotlib.pyplot as plt
import Core as Core

""" 一个处理器（Processor），拥有特定数量的资源（core，内存，缓存等）。一个客户首先申请服务。在对应服务时间完成后结束并离开工作站 """

color_dict = {0: '#1b9e77', 1: '#d95f02', 2: '#7570b3', 3: '#e7298a'}

Dag_color_list = {"M1_S1_C1": {0: "#D8D8D8", 1: "#D8D8D8"},
                  "M1_S2_C1": {0: "#b3e2cd", 1: "#b3e2cd", 2: "#b3e2cd"},
                  "M1_S1_C2": {0: "#fdcdac", 1: "#fdcdac"},
                  "M1_S2_C2": {0: "#fdcdac", 1: "#fdcdac", 2: "#fdcdac"},
                  "M2_S1_C1": {0: "#fdcdac", 1: "#fdcdac"},
                  "M2_S2_C1": {0: "#cbd5e8", 1: "#cbd5e8", 2: "#cbd5e8"},
                  "M2_S3_C1": {0: "#f4cae4", 1: "#f4cae4", 2: "#f4cae4", 3: "#f4cae4", 4: "#f4cae4", 5: "#f4cae4"}}


def show_dag_and_makespan(Core_Data_List, ax_obj, font_size):
    makespan_res = max([Core_Data_x.last_finish_time for Core_Data_x in Core_Data_List])
    core_name_list = []
    core_y_location_list = []
    ax_obj.ticklabel_format(style='plain')
    for core_id, x in enumerate(Core_Data_List):
        core_name_list.append(x.Core_ID)
        core_y_location_list.append(core_id * 1)
        for y in x.Core_Running_Task:
            color_lable = color_dict[y['dag_ID']]
            barh_width = y['end_time'] - y['start_time']
            barh_start = y['start_time']
            node_id = y['node'][1]['Node_ID']  # name = (y['node'][1]['Node_ID'] + '/')[4:-1]
            # if y['node'][1]['Node_ID'].endswith('Job_29.1') or y['node'][1]['Node_ID'].endswith('Job_0'):
            if node_id in ['Job_29.1', 'Job_0']:
                continue
            ax_obj.barh(y=core_id * 1, width=barh_width, height=1, left=barh_start, color=color_lable, edgecolor='gray')
            ax_obj.text(x=barh_start + barh_width / 2, y=core_id, s='{0}'.format(node_id), fontsize=font_size,
                        family='Times New Roman', ha='center', va='center')
    plt.yticks(core_y_location_list, core_name_list, fontproperties='Times New Roman', size=font_size)  # 设置y刻度:用文字来显示刻度
    plt.xticks(fontproperties='Times New Roman', size=font_size)
    plt.xlim(xmin=0, xmax=makespan_res * 1)

    # 右上标记
    # temp_obj_list = []
    # Flow_ID_List = []
    # for dag_id in Dag_ID_List:
    #     for flow_num, dag_flow_color in Dag_color_list[dag_id].items():
    #         if flow_num > 0:
    #             temp_obj_list.append(plt.scatter(-100000, 0, marker="s", color=dag_flow_color))
    #             Flow_ID_List.append("{0}".format(dag_id, flow_num))
    # font = font_manager.FontProperties(size=font_size)
    # plt.legend(temp_obj_list, Flow_ID_List, loc='upper right', prop={'family': 'Times New Roman', 'size': 16})


if __name__ == "__main__":
    Dag_ID_List = ['M1_S1_C1']
    core_num = 3
    Core_Data_List = [Core.Core_Obj(f'core_{i + 1}') for i in range(core_num)]

    core0 = Core_Data_List[0]
    core0.Insert_Task_Info(2, dag_NUM=1, node=[1, {'Node_ID': '1'}], start_time=0,    end_time=100)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[2, {'Node_ID': '2'}], start_time=100,  end_time=200)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[3, {'Node_ID': '3'}], start_time=200,  end_time=300)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[4, {'Node_ID': '4'}], start_time=300,  end_time=400)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[5, {'Node_ID': '5'}], start_time=600,  end_time=700)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[6, {'Node_ID': '6'}], start_time=700,  end_time=800)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[7, {'Node_ID': '7'}], start_time=800,  end_time=900)
    core0.Insert_Task_Info(2, dag_NUM=1, node=[8, {'Node_ID': '8'}], start_time=1000, end_time=1200)

    core1 = Core_Data_List[1]
    core1.Insert_Task_Info(0, dag_NUM=1, node=[1, {'Node_ID': '1'}], start_time=0,    end_time=100)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[2, {'Node_ID': '2'}], start_time=100,  end_time=200)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[3, {'Node_ID': '3'}], start_time=200,  end_time=300)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[4, {'Node_ID': '4'}], start_time=300,  end_time=400)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[5, {'Node_ID': '5'}], start_time=600,  end_time=700)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[6, {'Node_ID': '6'}], start_time=700,  end_time=800)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[7, {'Node_ID': '7'}], start_time=800,  end_time=900)
    core1.Insert_Task_Info(0, dag_NUM=1, node=[8, {'Node_ID': '8'}], start_time=1000, end_time=1200)

    core2 = Core_Data_List[2]
    core2.Insert_Task_Info(1, dag_NUM=1, node=[1, {'Node_ID': '1'}], start_time=0,    end_time=100)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[2, {'Node_ID': '2'}], start_time=100,  end_time=200)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[3, {'Node_ID': '3'}], start_time=200,  end_time=300)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[4, {'Node_ID': '4'}], start_time=300,  end_time=400)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[5, {'Node_ID': '5'}], start_time=600,  end_time=700)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[6, {'Node_ID': '6'}], start_time=700,  end_time=800)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[7, {'Node_ID': '7'}], start_time=800,  end_time=900)
    core2.Insert_Task_Info(1, dag_NUM=1, node=[8, {'Node_ID': '8'}], start_time=1000, end_time=1200)

    makespan = max([Core_Data_x.last_finish_time for Core_Data_x in Core_Data_List])
    FontSize = 14
    plt.xlabel("time-axis", fontdict={'family': 'Times New Roman', 'size': 16})
    plt.ylabel("core-list", fontdict={'family': 'Times New Roman', 'size': 16})

    for exam_id in range(1, 3):  # range(1,3) = [1,2,3) = [1,2]
        ax = plt.subplot(2, 1, exam_id)
        show_dag_and_makespan(Core_Data_List=Core_Data_List, ax_obj=ax, font_size=FontSize)
        ax.set_title("Makespan:{0}={1}ms\n Workload:{2}".format(makespan, makespan / 2260000, 0), fontsize=FontSize,
                     fontproperties='Times New Roman', color="black", weight="light", ha='left', x=0)

    plt.show()
