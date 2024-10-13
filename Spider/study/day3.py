#豆瓣简单爬虫
import requests

url = "https://movie.douban.com/j/chart/top_list"

#重新封装url里的参数
param ={
    "type": "24",
    "interval_id": "100:90",
    "action": "",
    "start":" 0",
    "limit": "20",
}
head = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",

}


res = requests.get(url,params = param,headers=head)
print(res.json())
res.close()