import pandas as pd
#调用随机森林模型
from sklearn.ensemble import RandomForestClassifier


#加载csv文件test
#df = pd.read_csv("E:/PythonProject/Kaggle/Data/titanic/train.csv")

#显示前5行数据
#print(df.head(5))
#=====success!

#1.加载训练集，测试集

train_data = pd.read_csv("E:/PythonProject/Kaggle/Data/titanic/train.csv")
test_data = pd.read_csv("E:/PythonProject/Kaggle/Data/titanic/test.csv")

women = train_data.loc[train_data.Sex =='female']['Survived']
rate_women = sum(women)/len(women)
#print(women)

#2.加载模型（回归模型）
y = train_data['Survived']
features = ["Pclass", "Sex", "SibSp", "Parch"]
x = pd.get_dummies(train_data[features])

x_test = pd.get_dummies(test_data[features])

#3.训练
model = RandomForestClassifier(n_estimators=100,max_depth=5,random_state=1)

model.fit(x,y)

predictions = model.predict(x_test)

#4.输出结果

output = pd.DataFrame({'PassengerId':test_data.PassengerId,'Survived':predictions})

print(output)

#5.保存到csv

output.to_csv("E:/PythonProject/Kaggle/Titanic/runs/predictions.csv",index=False)
