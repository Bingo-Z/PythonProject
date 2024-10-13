#requests包的学习

#安装request ==pip install requests

import requests

url = "https://www.sogou.com/web?query=周杰伦"

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
res = requests.get(url,headers=headers)

print(res.text)