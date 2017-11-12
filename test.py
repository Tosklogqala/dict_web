# coding=utf-8
import urllib.parse
import os
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import myTools

from bs4 import BeautifulSoup
import requests

from makeData import getzdic
from dbModel import dbmodel

import re

# from myTools import myTools

# help(myTools)
# print(myTools.getMd5Str("1"))

# print(urllib.parse.quote("https://itunes.apple.com/jp/app//id1296713868?l=zh&ls=1&mt=8"))
# print(urllib.parse.quote("电池管理者"))
# print(urllib.parse.unquote("%E7%94%B5%E6%B1%A0%E7%AE%A1%E7%90%86%E8%80%85"))
# try:
	# print(b'\\u3014'.decode("unicode-escape"))
	# zi = '蝨'.encode("unicode-escape").decode("ascii")
	# s = zi.replace('\\u','')
# 	zi = '麤'
# 	ma = zi.encode("unicode-escape")
# 	if zi>='\4e00' and zi<='\u9fff' :
# 		print(ma)
# 	else:
# 		print("not hanzi")
# except Exception as e:
# 	print(e)
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

# zi = "즤"
# print(myTools.rToH(myTools.hToR(zi)))
# dui = []
# for i,h in enumerate(myTools.f['h']):
# 	if myTools.f['r'][i] == "":
# 		continue
# 	dui.append([h,myTools.f['r'][i]])
# for i,h in enumerate(myTools.m['h']):
# 	if myTools.m['r'][i] == "":
# 		continue
# 	dui.append([h,myTools.m['r'][i]])
# for i,h in enumerate(myTools.l['h']):
# 	if myTools.l['r'][i] == "":
# 		continue
# 	dui.append([h,myTools.l['r'][i]])
# nd = []
# [nd.append(i) for i in dui if not i in nd]
# nd.sort(key=lambda x:ord(x[0]))

# sc = {'h':[],'r':[]}
# for one in nd:
# 	sc['h'].append(one[0])
# 	sc['r'].append(one[1])
# print(sc)

# for zi in allzimu:
# 	print(hex(ord(zi)))
# print(myTools.rToH(myTools.hToR(zi)))

# ma = "마"
# mae= "매"
# ga = "가"
# gae= "개"
# gga= "까"
# print("start:"+hex(ord(ga))+";distanceOfVowel:"+(ord(gae)-ord(ga))+";distanceOfConsonant:"+(ord(gga)-ord(ga)))
# print("start:%s;distanceOfVowel:%d;distanceOfConsonant:%d"%(hex(ord(ga)),(ord(gae)-ord(ga)),(ord(gga)-ord(ga))))
# print("%d"%((ord(gae)-0xac00)/28))
# num = str.split(ucode,'u')

# print("{0}".format(num[1]))

# a = ""
# print(a.encode("unicode-escape").decode("ascii").replace("\\U",""))
# print(myTools.SQL_URL)

# getzdic.getApinyin('天','5929')

# http://www.zdic.net/sousuo?q=天

# dbmodel.initDB(myTools.SQL_URL)
# session=dbmodel.getSession(myTools.SQL_URL)

# session.add(dbmodel.kryinxun(zxy='jeong'))
# session.commit()

# s = "뵙고 청할 곡"
# print(s[s.rfind(" ")+1:])


# a = "办"
# print(a.encode('gbk'))
# s = "一"
# print(s.encode("EUC-JP"))
# kwpy = open('kwpy.txt','w',encoding='utf-8')
# with open('kw.txt','rb') as fp:
# 	while True:
# 		text = fp.readline()
# 		if text:
# 			kwpy.write(text.decode("EUC-JP",errors='replace'))
# 		else:
# 			break
# kwpy.close()
# fp = open('kwpy.txt','w',encoding='utf-8')
# fp.write(text)

# print(b'\xad\xa1'.decode("EUC-JP"))
# s = "【鞏固】キョウコ"
# PATTERN=u'[\u30a2-\u30f3]+'
# pattern = re.compile(PATTERN)
# print(pattern.findall(s))
# print(re.findall(u'[\u30a2-\u30f3]+',s))

# print(hex(ord(s)))
# s = "ギ"
# print(hex(ord(s)))
# s = "キ"
# print(hex(ord(s)))
# s = "ン"
# print(hex(ord(s)))

# s = "unicode=1e0a sfadfas unicode=d04f"
# print(re.findall("(?<=unicode=)....",s))
# print(re.findall("(?<=unicode=)[a-zA-Z0-9]+",s))

# s="1 ヨ(wu)(han)<a href=>(上)語</a>, <a href=>(去)御</a>"

# print(re.findall(u'...(?=wu)',s))

# s = "<div id='yindu'>《音読み》\n[w:0xa464]オ(ヲ)(han), ウ(wu)<a href=>(去)遇(暮)</a>　汚と同音。\n[w:0xa465]アク(wu)(han)<a href=>(入)薬(鐸)</a>　悪と同音。\n《ピンイン》([n:0xa23e])\n</div>"
# s = "《音読み》\n[w:0xa464]キ(クヰ)(wu)(han)<a href=>(去)[w:0xb02b](至)</a>\n[w:0xa465]カイ(クヮイ)(han), ケ(クヱ)(wu)<a href=>(去)卦(怪)</a>\n《ピンイン》(ku[n:0xa161]i)"
# print(re.findall(u'([\u30a2-\u30f3]{1,6}\([\u30a2-\u30f3]{0,6}\))(\([\(wuhantg\)]{1,20}\))',s))
# print(re.findall('([ア-ン]{0,5},{0,5}[ア-ン]{1,5}\({0,1}[ア-ン]{0,5}\){0,1})(\([wuhantg\)\(]*\))',s))
# result = s.split("\n")
# print(result)
# for one in result:
# 	if one.find("《")<0:
# 		print("one:"+one)
# 		a = re.findall(u'([\u30a2-\u30f3]{1,6}\([\u30a2-\u30f3]{0,6}\))(\([\(wuhantg\)]{1,20}\))',one)
# 		b = re.findall('<a href=>(.*)</a>',one)
# 		for f in a:
# 			# print(f[0]+";"+f[1])
# 			print(len(f))
# 		print(b)

# s = "平上入(去)卦(怪)(去)[w:0xb02b](至)"
# print(re.findall(u'[\u2E80-\u4e09\u4e0b-\u5164\u5166-\u53ba\u53bc-\u5e72\u5e74-\u9FFF]',s))


# print("入".encode("unicode-escape"))

# print(chr(int("4e00", base=16)))
# def cuyin(two):
# 	if len(two.group(0))!= 2:
# 		return two
# 	else:
# 		return two.group(0)[1]+two.group(0)[1]
# s = "keqkyoku"
# print(re.sub('q[a-z]',cuyin,s))

# import csv
# #打开文件，用with打开可以不用去特意关闭file了，python3不支持file()打开文件，只能用open()
# with open("orthography_jp.tsv","r",encoding='utf-8') as fp:
# 	# text = fp.read()
# 	# text = text.replace("\t",",")
# 	# print(text)
# 	kata=[]
# 	hira=[]
# 	roma=[]

# 	tmp =[]
# 	read = csv.reader(fp)
# 	for i in read:
# 		dui=i[0].split("\t")
# 		tmp.append(dui)

# 	tmp.sort(key=lambda x:4-len(x[2]))
# 	for j in tmp:
# 		kata.append(j[1])
# 		hira.append(j[0])
# 		roma.append(j[2])

# 	dic=[kata,hira,roma]

# 	print(dic)


s = "(2.2)"
s.replace("2","1")
s.replace("1","3")
print(s)
# print(myTools.jToR(s))
# print(re.findall("\d\.",s))
# print(s.find("[ア-ン]"))

# print(myTools.jToR("クヱ"))

# j = [
# ['ア', 'イ', 'ウ', 'エ', 'オ', 'ヤ', 'ユ', 'ヨ', 'カ', 'キ', 'ク', 'ケ', 'コ', 'キャ', 'キュ', 'キョ', 'サ', 'シ', 'ス', 'セ', 'ソ', 'シャ', 'シュ', 'ショ', 'タ', 'チ', 'ツ', 'テ', 'ト', 'チャ', 'チュ', 'チョ', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ニャ', 'ニュ', 'ニョ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ', 'ヒャ', 'ヒュ', 'ヒョ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ミャ', 'ミュ', 'ミョ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'リャ', 'リュ', 'リョ', 'ワ', 'ヰ', 'ヱ', 'ヲ', 'ヰャ', 'ヰュ', 'ヰョ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'ギャ', 'ギュ', 'ギョ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'ジャ', 'ジュ', 'ジョ', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド', 'ヂャ', 'ヂュ', 'ヂョ', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'ビャ', 'ビュ', 'ビョ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'ピャ', 'ピュ', 'ピョ', 'クヮ', 'クヰ', 'クヱ', 'クヲ', 'グヮ', 'グヰ', 'グヱ', 'グヲ', 'グヰャ', 'グヰュ', 'グヰョ', 'ン', 'ッ'], 
# ['あ', 'い', 'う', 'え', 'お', 'や', 'ゆ', 'よ', 'か', 'き', 'く', 'け', 'こ', 'きゃ', 'きゅ', 'きょ', 'さ', 'し', 'す', 'せ', 'そ', 'しゃ', 'しゅ', 'しょ', 'た', 'ち', 'つ', 'て', 'と', 'ちゃ', 'ちゅ', 'ちょ', 'な', 'に', 'ぬ', 'ね', 'の', 'にゃ', 'にゅ', 'にょ', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ひゃ', 'ひゅ', 'ひょ', 'ま', 'み', 'む', 'め', 'も', 'みゃ', 'みゅ', 'みょ', 'ら', 'り', 'る', 'れ', 'ろ', 'りゃ', 'りゅ', 'りょ', 'わ', 'ゐ', 'ゑ', 'を', 'ゐゃ', 'ゐゅ', 'ゐょ', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'ぎゃ', 'ぎゅ', 'ぎょ', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'じゃ', 'じゅ', 'じょ', 'だ', 'ぢ', 'づ', 'で', 'ど', 'ぢゃ', 'ぢゅ', 'ぢょ', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'びゃ', 'びゅ', 'びょ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'ぴゃ', 'ぴゅ', 'ぴょ', 'くゎ', 'くゐ', 'くゑ', 'くを', 'くゐゃ', 'くゐゅ', 'くゐょ', 'ぐゎ', 'ぐゐ', 'ぐゑ', 'ぐを', 'ぐゐゃ', 'ぐゐゅ', 'ぐゐょ', 'ん', 'っ'], 
# ['a', 'i', 'u', 'e', 'o', 'ya', 'yu', 'yo', 'ka', 'ki', 'ku', 'ke', 'ko', 'kya', 'kyu', 'kyo', 'sa', 'si', 'su', 'se', 'so', 'sya', 'syu', 'syo', 'ta', 'ti', 'tu', 'te', 'to', 'tya', 'tyu', 'tyo', 'na', 'ni', 'nu', 'ne', 'no', 'nya', 'nyu', 'nyo', 'ha', 'hi', 'hu', 'he', 'ho', 'hya', 'hyu', 'hyo', 'ma', 'mi', 'mu', 'me', 'mo', 'mya', 'myu', 'myo', 'ra', 'ri', 'ru', 're', 'ro', 'rya', 'ryu', 'ryo', 'wa', 'wi', 'we', 'wo', 'wya', 'wyu', 'wyo', 'ga', 'gi', 'gu', 'ge', 'go', 'gya', 'gyu', 'gyo', 'za', 'zi', 'zu', 'ze', 'zo', 'zya', 'zyu', 'zyo', 'da', 'di', 'du', 'de', 'do', 'dya', 'dyu', 'dyo', 'ba', 'bi', 'bu', 'be', 'bo', 'bya', 'byu', 'byo', 'pa', 'pi', 'pu', 'pe', 'po', 'pya', 'pyu', 'pyo', 'kwa', 'kwi', 'kwe', 'kwo', 'kwya', 'kwyu', 'kwyo', 'gwa', 'gwi', 'gwe', 'gwo', 'gwya', 'gwyu', 'gwyo', 'n', 'q']]

# yunmus=['東', '董', '送', '屋', '冬', '湩', '宋', '沃', '鍾', '腫', '用', '燭', '江', '講', '絳', '覺', '之', '止', '志', '微', '尾', '未', '魚', '語', '御', '虞', '麌', '遇', '模', '姥', '暮', '齊', '薺', '霽', '泰', '佳', '蟹', '卦', '皆', '駭', '怪', '夬', '灰', '賄', '隊', '咍', '海', '代', '廢', '諄', '準', '稕', '術', '臻', '櫬', '櫛', '文', '吻', '問', '物', '欣', '隱', '焮', '迄', '元', '阮', '願', '月', '魂', '混', '慁', '沒', '痕', '很', '恨', '麧', '寒', '旱', '翰', '曷', '桓', '緩', '換', '末', '刪', '潸', '諫', '黠', '山', '產', '襇', '鎋', '先', '銑', '霰', '屑', '蕭', '篠', '嘯', '肴', '巧', '效', '豪', '晧', '号', '歌', '哿', '箇', '戈', '果', '過', '麻', '馬', '禡', '陽', '養', '漾', '藥', '唐', '蕩', '宕', '鐸', '庚', '梗', '映', '陌', '耕', '耿', '諍', '麥', '清', '靜', '勁', '昔', '青', '迥', '徑', '錫', '蒸', '拯', '證', '職', '登', '等', '嶝', '德', '尤', '有', '宥', '侯', '厚', '候', '幽', '黝', '幼', '覃', '感', '勘', '合', '談', '敢', '闞', '盍', '添', '忝', '怗', '咸', '豏', '陷', '洽', '銜', '檻', '鑑', '狎', '嚴', '儼', '釅', '業', '凡', '梵', '范', '乏']
# chongnius=['支', '紙', '寘', '支', '紙', '寘', '脂', '旨', '至', '脂', '旨', '至', '祭', '祭', '眞', '軫', '震', '質', '眞', '軫', '震', '質', '仙', '獮', '線', '薛', '仙', '獮', '線', '薛', '宵', '小', '笑', '宵', '小', '笑', '侵', '寑', '沁', '緝', '侵', '寑', '沁', '緝', '鹽', '琰', '豔', '葉', '鹽', '琰', '豔', '葉']

# founds1=['湩', '咍', '稕', '櫬', '焮', '慁', '麧', '產', '襇', '鎋', '哿', '禡', '德', '闞', '怗', '豏', '釅']
# founds2=['寘', '寘', '獮', '獮', '寑', '寑', '琰', '豔', '琰', '豔']

# founds3=['脂', '旨', '至', '祭', '眞', '仙', '線', '薛', '宵', '小', '笑', '鹽']
# founds4=['隱', '沒', '效', '麥', '靜', '陷', '嚴', '范']
# with open("kwpy",'r',encoding='utf-8') as fp:
# 	text = fp.read()
# 	for one in chongnius:
# 		if text.find(")"+one+"</a>") < 0 and text.find("("+one+")")<0:
# 			founds3.append(one)

# print(founds3)

#[['[w:0xa75a]', '僀'], ['[w:0xa934]', '勏'], ['[w:0xa961]', '卙'], ['[w:0xab40]', '嗁'], ['[w:0xad68]', '墊'], ['[w:0xad64]', '墁'], ['[w:0xb044]', '屢'], ['[w:0xb443]', '懟'], ['[w:0xb826]', '暵'], ['[w:0xa977]', '歴'], ['[w:0xa977]', '厯'], ['[w:0xbd21]', '淊'], ['[w:0xbd5f]', '滊'], ['[w:0xc04c]', '猅'], ['[w:0xc148]', '珽'], ['[w:0xc545]', '碰'], ['[w:0xc575]', '礿'], ['[w:0xc57a]', '祋'], ['[w:0xc625]', '祫'], ['[w:0xc623]', '祧'], ['[w:0xc62d]', '禑'], ['[w:0xc632]', '禘'], ['[w:0xc62e]', '禓'], ['[w:0xc868]', '穀'], ['[w:0xc868]', '糓'], ['[w:0xc952]', '緃'], ['[w:0xc966]', '緺'], ['[w:0xcc2d]', '臬'], ['[w:0xcf64]', '虚'], ['[w:0xcf64]', '虗'], ['[w:0xcf69]', '虡'], ['[w:0xc427]', '視'], ['[w:0xc427]', '眎'], ['[w:0xd347]', '誯'], ['[w:0xd363]', '謑'], ['[w:0xd467]', '賿'], ['[w:0xd67e]', '逭'], ['[w:0xd755]', '郎'], ['[w:0xd755]', '郒'], ['[w:0xd757]', '郫'], ['[w:0xda2f]', '錴'], ['[w:0xe23b]', '黆']]
#[  '[w:0xe333]', '[w:0xe458]', '[w:0xa53f]', '[w:0xa546]', '[w:0xe456]']

#['[w:0xe44a]','陽'],['[w:0xe44b]','陰']
#['[w:0xe450]','巽'],['[w:0xe44c]','乾'],['[w:0xe44d]','兌'],['[w:0xe453]','坤'],['[w:0xe44f]','震'],['[w:0xe451]','坎'],['[w:0xe452]','艮'],['[w:0xe44e]','離']
#['[w:0xa538]','ǚ'],['[w:0xa536]','ǜ'],['[w:0xa537]','ǘ']
#['[n:0xa174]','ó']['[n:0xa16a]','é']
#[w:0xa53c][w:0xa540][w:0xa53d][w:0xa542][w:0xa53b] #IPA
#[n:0xa254][n:0xa34c] #IPA
#['[w:0xa433]','ヰ']，['[w:0xa434]','ヱ']
#['[w:0xe34c]','yao']#瑤的右边
#['[w:0xe454]','']#淮南子 堕形
#['[w:0xe335]','']#包耳旁
#['[w:0xe334]','']#方框旁
#['[w:0xa53a]', '[w:0xe336]','[w:0xe32e]','[w:0xe455]', '[w:0xe34e]','[w:0xe347]','[w:0xe332]','[w:0xe33e]','[w:0xe349]','[w:0xe448]','[w:0xe343]','[w:0xe34b]',
#'[w:0xa531]','[w:0xe34d]','[w:0xe348]','[w:0xe340]','[w:0xe457]', '[w:0xa532]','[w:0xe449]',]