# 工具介绍

本工具旨在计算静态调度的最优解。

任务$\tau_x$被定义为多元组，各任务具唯一的ID（TASK_ID / TASK_INDEX）：

$$\tau_x=\{T_x,~D_x,~G_x~=~(V_x,~E_x)\}$$

其中：

<!-- 任务的周期类型Periodically:
  - 'PERIODIC'：周期任务；
  - 'SPORADIC'：零星任务；
  - 'APERIODIC'：非周期任务(只运行一次) -->


- $T_x$：周期任务的周期或循环时间（period）。
<!-- 零散任务的最小到达间隔时间。 -->
<!-- - $R$: DAG的执行周期; -->


- $D_x$：任务的相对截止时间，满足 $D_x \leq T_x$。
<!-- （constrained relative deadline） -->

<!-- - 实时类型Real_Time:- 'HRT'：硬实时;  - 'SRT'：软实时;  - 'FRT'：固实时; -->


<!-- - Priority(Prio) : DAG的优先级(越小等级越高); -->


<!-- - 偏移量/相位/起始时间 : 第一个任务的到达时间（默认为0）-->


- $G_x=(V_x,~E_x)$：有向无环图（DAG），描述任务内部的依赖关系，一个DAG具有一个唯一的DAG_ID（DAG_INDEX）：

  - $V_x$：DAG的结点集合，每个结点$v_i \in V_x$代表一个<!-- 不可抢占的 -->串行执行单元。各结点$v_i$具有唯一的ID（NODE_ID / NODE_INDEX）。

  - $E_x \subseteq V_x \times V_x$：DAG的有向边集合，表示结点间的依赖关系。

<!-- JOB\_ID -->

## 1. 输入文件

示例输入文件位于Idata文件夹中，用于确定任务与处理器模型。

### 1.1 DAG数据（json）

- ID: 表示任务的ID；

- T: 表示任务的周期；

- D: 表示任务的截止时间；

- G: 表示DAG；
  - V: 表示DAG的结点集合；
    - ID: 表示结点的ID；

    - W:  表示任务的WCET。
    <!-- "WCET/BCET/ACET——WCET：Max/Min/Ave/Std"（执行时间） -->

    <!-- - Pr: 结点的优先级（Priority）。 -->

    <!-- - Succ: 结点的后继结点集合。 -->

    <!-- GROUP_ID -->

    <!-- FLOW_ID -->

    <!-- Start_Time/OFFSET -->

  - E: 表示DAG的有向边集合；


### 1.2 处理器数据（json）
一个处理器（Processor）拥有特定数量的资源，其中，每个核心具有唯一的ID （CORE_ID / CORE_INDEX）。
<!--（core，内存，缓存等）-->

- ID: 表示核心的ID;

<!-- - CORE_ID :           e.g. '1_1'  "CORE_ID" -->
<!-- - Core_Type）:        e.g. 'Cortex-M3'； -->
<!-- - Core_Status         更新core状态为BUSY/IDLE -->


## 2. 输出文件
示例输出文件位于Odata文件夹中。

### 2.1 调度表数据 json
每个元素为一个结点及其对应的调度数据：包括：
- $s$：结点的起始时间(start_time);

- $c$：结点的执行时间(execution_time);

- $a$：结点运行的核心的ID;

<!-- - $f$：结点的结束时间(finish_time); -->

<!-- - Core_Running_Task:  the running log about this core (sch list)
  - r:    arrive_time,
  - f:    finish_time,
  - e:    end_time-->

### 2.2 DAG图 png
以图的形式介绍DAG的相关数据。

<!-- DAG 的分析参数：一个客户首先申请服务。在对应服务时间完成后结束并离开工作站。获取DAG的并行度和关键路径长度。

"s_max",
"s_min",
"s_ave",
"s_std",
"r_max",
"r_min",
"r_ave",
"r_std",
"id",
"od",
"w",
DAG_volume(DAG_vol) = sum(WCET_list)-->


### 2.3 Gantt图 png
以图的形式绘制调度表中各任务的执行情况。

## 3. 源代码
工具的源代码在Main.py中，直接运行即可。运行结束会打印求解器的运行结果，包括DAG调度的makespan以及求解所用的时间开销。代码中关键函数介绍如下：

### 3.1 Dag_Json_Input(_file:str):
- 函数介绍：该函数可将以Json文件存储的DAG数据读取到程序中；

- 输入参数：
  - _file：表示输入的DAG数据文件（json）的存储地址；

- 输出结果：函数将输出文件（json）中存储的DAG数据；




### 3.2 Processor_Json_Input(_file:str):
- 函数介绍：该函数可将以Json文件存储的处理器数据读取到程序中；

- 输入参数：
  - _file：表示输入的处理器数据文件（json）的存储地址；

- 输出结果：函数将输出文件（json）中存储的处理器数据；

### 3.3 DAG_Fig_Output(_rd, _file:str):
- 函数介绍：该函数可将DAG数据以png格式输出存储到指定地址；

- 输入参数：
  - _rd：表示待输出的目标DAG；

  - _file：表示输出文件的存储地址；

- 输出结果：函数将在指定的存储地址中，输出DAG图；


### 3.4 Gantt_Fig_Output(_rd, _dl:list, _file:str):
- 函数介绍：该函数可将根特图以png格式输出存储到指定地址；

- 输入参数：
  - _rd：表示待输出的目标DAG；
  
  - _dl：表示DAG的调度表；

  - _file：表示输出文件的存储地址；

- 输出结果：函数将在指定的存储地址中，输出DAG最优调度的根特图；


### 3.5 Schedule_Tab_Output(_rd, _dl:list, _file:str):
- 函数介绍：该函数可将调度表以json格式输出存储到指定地址；

- 输入参数：
  - _rd：表示待输出的目标DAG；
  
  - _dl：表示DAG的调度表；

  - _file：表示输出文件的存储地址；

- 输出结果：函数将在指定的存储地址中，输出一个json格式的调度表；


### 3.6 DAG_Opt_Solver(_td, _pd):
- 函数介绍：该函数可根据任务和处理器参数计算调度的最优解；

- 输入参数：
  - _td：表示待求解的目标DAG；

  - _pd：表示处理器相关数据（核心数量）；

- 输出结果：函数将判断是否有解，如果有解则返回调度表，否则返回None；
