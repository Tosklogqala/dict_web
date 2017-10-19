import urllib.parse
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


from bs4 import BeautifulSoup
import requests

# from myTools import myTools

# help(myTools)
# print(myTools.getMd5Str("1"))

# print(urllib.parse.quote("https://itunes.apple.com/jp/app//id1296713868?l=zh&ls=1&mt=8"))
# print(urllib.parse.quote("电池管理者"))
# print(urllib.parse.unquote("%E7%94%B5%E6%B1%A0%E7%AE%A1%E7%90%86%E8%80%85"))
try:
	# print(b'\\u3014'.decode("unicode-escape"))
	# zi = '蝨'.encode("unicode-escape").decode("ascii")
	# s = zi.replace('\\u','')
	zi = '麤'
	ma = zi.encode("unicode-escape")
	if zi>='\4e00' and zi<='\u9fff' :
		print(ma)
	else:
		print("not hanzi")
except Exception as e:
	print(e)
# print("あ".encode(encoding='utf-8'));
# print("".encode(encoding='ascii'))

# "[蟲/𧎪]也"
# print("[蟲/𧎪]也".encode(encoding='unicode-escape',errors='replace'))
# astr = b'[\\u87f2/\\000U273aa]\\u4e5f'
# print(astr.decode('unicode-escape','replace'))

# 获取当前目录 sys.path[0]或sys.argv[0]  ?os.getcwd()
# print(sys.path[0])
# 获取本文件路径 os.path.realpath(__file__)
# print(os.path.realpath(__file__))

# response = requests.get("http://ytenx.org/kyonh/dzih/945/")
# soup = BeautifulSoup(response.text,"html.parser")
# print(soup.body.text)


# ucode = "東".encode('unicode-escape').decode('ascii')
# num = str.split(ucode,'u')

# print("{0}".format(num[1]))