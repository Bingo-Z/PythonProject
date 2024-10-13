#爬虫
#1、程序模拟浏览器
#
from urllib.request import urlopen

url = "http://www.baidu.com"
res = urlopen(url)

#print(res.read().decode("utf-8"))

with open ("mybaidu.html",mode='w',encoding='utf-8') as f:
    f.write(res.read().decode("utf-8"))
print("over")
