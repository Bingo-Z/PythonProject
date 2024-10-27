import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_profiling as pp
#0.查看数据格式
df = pd.read_csv("E:/PythonProject/Kaggle/Data/housePrise/train.csv")
#   查看前5行
# print(df.head(5))
#==================================================================
#    Id  MSSubClass MSZoning  ...  SaleType  SaleCondition SalePrice
# 0   1          60       RL  ...        WD         Normal    208500
# 1   2          20       RL  ...        WD         Normal    181500
# 2   3          60       RL  ...        WD         Normal    223500
# 3   4          70       RL  ...        WD        Abnorml    140000
# 4   5          60       RL  ...        WD         Normal    250000
#==================================================================
#1.加载数据
train_data = pd.read_csv("E:/PythonProject/Kaggle/Data/housePrise/train.csv")
test_data = pd.read_csv("E:/PythonProject/Kaggle/Data/housePrise/test.csv")

#2.查看数据类型并进行数据处理
# 2.1查看所有特征因子，即列名
#print(train_data.columns,len(train_data.columns))
#   or
#print(train_data.info())
#发现type有object，int64，float64，所以有一个任务是统一数据类型


# #从数据表格中选择数字列
# numeric_df = train_data.select_dtypes(include=['int64','float64'])
# #计算数字各变量数据相关性的热力图即热力矩阵
# corr_mat = numeric_df.corr()
# #展示热力矩阵
# f,ax = plt.subplots(figsize=(12,9))
# #使用 Seaborn 库中的 heatmap 函数来绘制热图
# sns.heatmap(corr_mat,vmax=.8,square = True,annot=True,fmt=".1f")
# #plt中文
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.suptitle("相关特征热图")
# plt.xlabel("特征")
# plt.ylabel("特征")
#plt.show()

# 使用第三方工具来查看
profile = pp.ProfileReport(train_data)
profile.to_file("output_train.html")
profile = pp.ProfileReport(test_data)
profile.to_file("output_test.html")
#计算特征矩阵
corr_mat = train_data.select_dtypes(include=['int64','float64']).corr()
#设置矩阵大小和plt画布大小
sns.set(font_scale=1.3)
plt.figure(figsize=(11, 8))
#选择与“销售价格”相关度高于0.5的特性
top_corr = corr_mat.index[abs(corr_mat['SalePrice'])>0.5]
#绘制特征热图
sns.heatmap(train_data[top_corr].corr(),annot=True,cmap="YlGnBu")
#plt画布
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.suptitle("相关特征热图")
plt.xlabel("特征")
plt.ylabel("特征")
plt.show()
#   为数据绘制散点图，以去除异常数据
