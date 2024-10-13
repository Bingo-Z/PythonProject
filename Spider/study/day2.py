import time

import requests

url = "https://fanyi.baidu.com/sug"

s = input("请输入要翻译的词语：")
str = {
    "kw": s
}

ua =  {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
ck = {
    "cookie":"BAIDUID_BFESS=B9C4249284C73BC974FAC5FAC1026596:FG=1","user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
res = requests.post(url,headers=ck,data=str)

#test
print(res.text)
print(res.json())