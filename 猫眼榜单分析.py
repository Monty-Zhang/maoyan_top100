'''
    Author: Monty
    Date: 2019-07-17
    Function: 分析猫眼榜单数据
    Version: 1.0
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file_path = 'Download/maoyantop100.csv'

with open(file_path, 'r', encoding='utf-8') as f:
    data = pd.read_csv(f, usecols=['title','star','releasetime','score'])

# 将releasetime列拆分，分成发行时间和发行国家两列
# expand=True可以将一列分为多列，如果为False则在一列中表示为列表
transform = data['releasetime'].str.rstrip(')').str.split('(', expand=True)

data['releasetime'] = transform[0]
data['country'] = transform[1]

# 将star列进行拆分，用于统计出现次数最多的演员
stars = data['star'].str.split(',', expand=True)
data['star'] = stars[0]
data['star2'] = stars[1]
data['star3'] = stars[2]

transformed_data = data.reindex(columns=['title','star','star2','star3','releasetime','country','score'])

# 统计所有演员在榜单中出现的次数
star_count = pd.value_counts(np.concatenate((transformed_data['star'],transformed_data['star2'],transformed_data['star3'])))
print('出现3次以上演员名单：')
print(star_count[star_count>=3])
print('--'*50)

# 统计演员组合出现的次数
# 首先查看是否有主演完全一样的电影
star_duplicated = transformed_data[['star','star2','star3']].duplicated()
print('三人组合入榜名单：')
print(transformed_data[star_duplicated])
print('--'*50)

# 将这三部电影剔除后查看演员两两组合出现的次数，这里使用笨办法，手工将演员配对
data_without_duplicated = transformed_data.drop_duplicates(['star','star2','star3'])
star_combin1 = data_without_duplicated['star'] + data_without_duplicated['star2']
star_combin2 = data_without_duplicated['star'] + data_without_duplicated['star3']
star_combin3 = data_without_duplicated['star2'] + data_without_duplicated['star3']
star_combin_count = pd.value_counts(np.concatenate([star_combin1, star_combin2, star_combin3]))
print('双人搭档出现大于1次名单：')
print(star_combin_count[star_combin_count>1])
print('--'*50)

# 统计电影年份的出现次数
# 表中的releasetime是str格式，将其转化为datetime格式
transformed_data['releasetime'] = pd.to_datetime(transformed_data['releasetime'])
year_count = transformed_data['releasetime'].value_counts().resample('AS').count().to_period('Y')
print('年度电影数量5部以上名单：')
print(year_count[year_count>=5].sort_values(ascending=False))
print('--'*50)

# 统计国家出现次数
# 改数据缺失值较多，没什么统计价值
country_count = transformed_data['country'].value_counts()
print('国家电影出现3次以上名单：')
print(country_count[country_count>=3])
print('--'*50)

# 查看score的分布
score_count = transformed_data['score'].value_counts().sort_index(ascending=False)
fig, axs = plt.subplots(1,1)
axs.set_yticks(range(1,30,2))
score_count.plot.bar(ax=axs, color='g')
plt.show()

