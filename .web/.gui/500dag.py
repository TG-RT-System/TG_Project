import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import math
import pandas as pd


plt.rcParams['font.family'] = 'YouYuan'
plt.rcParams['font.sans-serif']= ['Microsoft YaHei']  # 使用微软雅黑的字体
# matplotlib.rcParams['font.size'] = 20
plt.style.use('classic') # 画板主题风格
plt.figure(figsize=(9, 6))
plt.title("exam_data")  # 标题
plt.grid()  # 网格线
plt.xlabel('length')
plt.ylabel('width')
plt.axis([0, 300, 0, 250])


ax = plt.gca()
ax.spines['bottom'].set_position(('data', 0))
ax.spines['top'].set_color('none')
ax.spines['left'].set_position(('data', 0))
ax.spines['right'].set_color('none')

#####################
temp_data = pd.read_csv('./dag_data.csv', index_col=None, na_values=["NA"])
for row in temp_data.index:
    dag_length = temp_data.loc[row]['length']
    dag_width = temp_data.loc[row]['width']
    if dag_width == 1 or dag_width == 1:
        continue
    plt.scatter(x=dag_length, y=dag_width)  # 散点图


x = np.arange(0, 300, 1)
y1 = np.power(x, 0.85)
y2 = np.power(x, 1.15)
plt.plot(x, y1, 'r-')
plt.plot(x, y2, 'g-')
plt.show()

