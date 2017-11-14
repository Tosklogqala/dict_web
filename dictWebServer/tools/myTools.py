# coding=utf-8
from bs4 import BeautifulSoup
import requests

import hashlib
import re
import os
import sys
import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

YTENX_GY_NAME = 'ytenx_gy_xiaoyun_{0}'
YTENX_SG_NAME = 'ytenx_sg_zibiao_{0}'

# 现在这个路径与调用的py所在的路径有关。以后要改成myTools所在的路径
PROJ_PATH = os.path.split(os.path.realpath(__file__))[0] 

# ZDIC_PATH = os.path.join(PROJ_PATH,"zdic")

# YTENX_PATH = os.path.join(PROJ_PATH,"ytenx")
# YTENX_GY_PATH = os.path.join(YTENX_PATH,"gy")
# YTENX_SG_PATH = os.path.join(YTENX_PATH,"sg")

# NAVER_PATH = os.path.join(PROJ_PATH,"naver")
# HANVIET_PATH =os.path.join(PROJ_PATH,"hanviet")

# EB_PATH = PROJ_PATH

SQL_URL = ""+os.path.join(PROJ_PATH,"..","data","cl.db")

# class myTools():
	# @staticmethod
def getUniStr(hanzi):
	coded = hanzi.encode("unicode-escape").decode("ascii")
	# if hanzi>='\4e00' and hanzi<='\u9fff' :
	if coded.find('U')>0:
		return coded.replace('\\U','')
	else:
		return coded.replace('\\u','')
	# else:
	# 	return '0'


def getMd5Str(_str):
	hs = hashlib.md5()
	hs.update(_str.encode('utf-8'))
	return hs.hexdigest()

	# @staticmethod
def hasFile(root,fileName):
	# print("myTools.hasFile("+root+","+fileName+")")
	for f in os.listdir(root):
		# if os.path.isfile(f) :
		if f==fileName:
			# print("found")
			return True
	# print("opseo")
	return False

	# @staticmethod
def hasDict(root,dictName):
	for f in os.listdir(root):
		if not os.path.isfile(f) :
			if f==dictName:
				return True
	return False


def writeResWeb(dictName,fileName,resWeb=""):
	if hasFile(dictName,fileName):
		return

	newfile = os.path.join(dictName,fileName)
	try:
		fp = open(newfile,'w',encoding='utf-8')
		fp.write(resWeb)
	except Exception as e:
		print(e)
		os.remove(newfile)
	finally:
		fp.close()

# first
f = {
'h':['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
'r':['g','gg','n','d','dd','r','m','b','bb','s','ss','','j','jj','ch','k','t','p','h']}
# mid
m = {
'h':['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅗ','ㅘ','ㅙ','ㅚ','ㅛ','ㅜ','ㅝ','ㅞ','ㅟ','ㅠ','ㅡ','ㅢ','ㅣ'],
'r':['a','ae','ya','yae','eo','e','yeo','ye','o','wa','wae','oe','yo','u','wo','we','wi','yu','eu','eui','i']}
# last
l = {
'h':['','ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ'],
'r':['','g','gg','gs','n','nj','nh','d','l','lg','lm','lb','ls','lt','lp','lh','m','b','bs','s','ss','ng','j','ch','k','t','p','h']}
# single character
sc= {
'h': ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ', 'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'],
'r': ['g', 'gg', 'gs', 'n', 'nj', 'nh', 'd', 'dd', 'r', 'l', 'lg', 'lm', 'lb', 'ls', 'lt', 'lp', 'lh', 'm', 'b', 'bb', 'bs', 's', 'ss', 'ng', 'j', 'jj', 'ch', 'k', 't', 'p', 'h', 'a', 'ae', 'ya', 'yae', 'eo', 'e', 'yeo', 'ye', 'o', 'wa', 'wae', 'oe', 'yo', 'u', 'wo', 'we', 'wi', 'yu', 'eu', 'eui', 'i']}

hangulStart=0xac00
dofc=588 	#21*28 起始辅音间的距离
dofv=28		#		元音间的距离

def hToR(hangul):
	if ord(hangul) >= hangulStart:
		repos = ord(hangul)-hangulStart
		hc = f['h'][int(repos/dofc)]
		rc = f['r'][int(repos/dofc)]

		hv = m['h'][int(repos%dofc/dofv)]
		rv = m['r'][int(repos%dofc/dofv)]

		ht = l['h'][int(repos%dofc%dofv)]
		rt = l['r'][int(repos%dofc%dofv)]

		return rc+rv+rt
	else:
		return sc['r'][sc['h'].index(hangul)]

def rToH(roman):
	print(roman)
	nc=11
	nv=0
	nt=0

	result = re.findall("[aeiouwy]+",roman)
	# print(result)
	if len(result)<1:
		result_h = sc['h'][sc['r'].index(roman)]
		return result_h
		# pass
	else:
		vowel = result[0]
		nv=m['r'].index(vowel)

		cs = str.split(roman,vowel)
		# print(cs)
		nc=f['r'].index(cs[0])
		nt=l['r'].index(cs[1])
		return chr(nc*dofc+nv*dofv+nt+hangulStart)

j = [
['クヰャ', 'クヰュ', 'クヰョ', 'グヰャ', 'グヰュ', 'グヰョ', 'キャ', 'キュ', 'キョ', 'シャ', 'シュ', 'ショ', 'チャ', 'チュ', 'チョ', 'ニャ', 'ニュ', 'ニョ', 'ヒャ', 'ヒュ', 'ヒョ', 'ミャ', 'ミュ', 'ミョ', 'リャ', 'リュ', 'リョ', 'ヰャ', 'ヰュ', 'ヰョ', 'ギャ', 'ギュ', 'ギョ', 'ジャ', 'ジュ', 'ジョ', 'ヂャ', 'ヂュ', 'ヂョ', 'ビャ', 'ビュ', 'ビョ', 'ピャ', 'ピュ', 'ピョ', 'クヮ', 'クヰ', 'クヱ', 'クヲ', 'グヮ', 'グヰ', 'グヱ', 'グヲ', 'ヤ', 'ユ', 'ヨ', 'カ', 'キ', 'ク', 'ケ', 'コ', 'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ', 'ツ', 'テ', 'ト', 'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ', 'マ', 'ミ', 'ム', 'メ', 'モ', 'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヰ', 'ヱ', 'ヲ', 'ガ', 'ギ', 'グ', 'ゲ', 'ゴ', 'ザ', 'ジ', 'ズ', 'ゼ', 'ゾ', 'ダ', 'ヂ', 'ヅ', 'デ', 'ド', 'バ', 'ビ', 'ブ', 'ベ', 'ボ', 'パ', 'ピ', 'プ', 'ペ', 'ポ', 'ア', 'イ', 'ウ', 'エ', 'オ', 'ン', 'ッ'],
['くゐゃ', 'くゐゅ', 'くゐょ', 'ぐゐゃ', 'ぐゐゅ', 'ぐゐょ', 'きゃ', 'きゅ', 'きょ', 'しゃ', 'しゅ', 'しょ', 'ちゃ', 'ちゅ', 'ちょ', 'にゃ', 'にゅ', 'にょ', 'ひゃ', 'ひゅ', 'ひょ', 'みゃ', 'みゅ', 'みょ', 'りゃ', 'りゅ', 'りょ', 'ゐゃ', 'ゐゅ', 'ゐょ', 'ぎゃ', 'ぎゅ', 'ぎょ', 'じゃ', 'じゅ', 'じょ', 'ぢゃ', 'ぢゅ', 'ぢょ', 'びゃ', 'びゅ', 'びょ', 'ぴゃ', 'ぴゅ', 'ぴょ', 'くゎ', 'くゐ', 'くゑ', 'くを', 'ぐゎ', 'ぐゐ', 'ぐゑ', 'ぐを', 'や', 'ゆ', 'よ', 'か', 'き', 'く', 'け', 'こ', 'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と', 'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ', 'ま', 'み', 'む', 'め', 'も', 'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'ゐ', 'ゑ', 'を', 'が', 'ぎ', 'ぐ', 'げ', 'ご', 'ざ', 'じ', 'ず', 'ぜ', 'ぞ', 'だ', 'ぢ', 'づ', 'で', 'ど', 'ば', 'び', 'ぶ', 'べ', 'ぼ', 'ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ', 'あ', 'い', 'う', 'え', 'お', 'ん', 'っ'], 
['kwya', 'kwyu', 'kwyo', 'gwya', 'gwyu', 'gwyo', 'kya', 'kyu', 'kyo', 'sya', 'syu', 'syo', 'tya', 'tyu', 'tyo', 'nya', 'nyu', 'nyo', 'hya', 'hyu', 'hyo', 'mya', 'myu', 'myo', 'rya', 'ryu', 'ryo', 'wya', 'wyu', 'wyo', 'gya', 'gyu', 'gyo', 'zya', 'zyu', 'zyo', 'dya', 'dyu', 'dyo', 'bya', 'byu', 'byo', 'pya', 'pyu', 'pyo', 'kwa', 'kwi', 'kwe', 'kwo', 'gwa', 'gwi', 'gwe', 'gwo', 'ya', 'yu', 'yo', 'ka', 'ki', 'ku', 'ke', 'ko', 'sa', 'si', 'su', 'se', 'so', 'ta', 'ti', 'tu', 'te', 'to', 'na', 'ni', 'nu', 'ne', 'no', 'ha', 'hi', 'hu', 'he', 'ho', 'ma', 'mi', 'mu', 'me', 'mo', 'ra', 'ri', 'ru', 're', 'ro', 'wa', 'wi', 'we', 'wo', 'ga', 'gi', 'gu', 'ge', 'go', 'za', 'zi', 'zu', 'ze', 'zo', 'da', 'di', 'du', 'de', 'do', 'ba', 'bi', 'bu', 'be', 'bo', 'pa', 'pi', 'pu', 'pe', 'po', 'a', 'i', 'u', 'e', 'o', 'n', 'q']]
def jToR(kana):
	for i,tmp in enumerate(j[0]):
		kana = kana.replace(tmp,j[2][i])

	return kana