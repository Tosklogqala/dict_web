# 导入:
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker

from ..tools import myTools

# 创建对象的基类:
dbmodel = declarative_base()

# hanzi
# 	+---zgchn pl.
#	|
#	+---sgchn pl. xiaoyun
#	|
#	+---pychn pl. xiaoyun
#	|
#	+---jpn
#	|    +---jpwuhan pl. xiaoyun
#	|
#	+---kor
#	|    +---kryinxun pl. xiaoyun
#	|
#	+---vnm
#	     +---vnyin pl. xiaoyun


class hanzi(dbmodel):
    # 表的名字:
    __tablename__ = 'hanzi'

    # 表的结构:
    id = Column(Integer,primary_key=True,autoincrement=True)
    zi = Column(String(1),nullable=False,unique=True)
    code = Column(String)										#unicode编码
    zg = relationship("zgchn", back_populates="hanzi")			#中古广韵
    sg = relationship("sgchn", back_populates="hanzi")			#上古音系（郑张）
    py = relationship("pychn", back_populates="hanzi")			#普语拼音
    jpn_id = Column(Integer)									#日语
    kr = relationship("kor", back_populates="hanzi")			#韩语
    vn = relationship("vnm", back_populates="hanzi")			#越南

    def __repr__(self):
        return "<hanzi(id='%s', zi='%s')>" % (self.id, self.zi)

class zgchn(dbmodel):
	__tablename__ = 'zgchn'

	id = Column(Integer, primary_key=True)
	mean = Column(String)
	sheng = Column(String(1))		#声母
	yun = Column(String(1))			#韵母（平声的韵字）
	diao = Column(String(1))		#声调
	deng = Column(String(2))		#等（三A）
	hu = Column(String(1))			#呼（开合）
	xiaoyun = Column(String(1))		#小韵
	she = Column(String(1))			#摄
	yunmu = Column(String(1))		#韵目（带声调的韵）
	fanqie_1 = Column(String(1))	#反切上字
	fanqie_2 = Column(String(1))	#反切下字
	zgzz = Column(String)			#中古郑张
	zgys = Column(String)			#中古严实
	infer_pinyin = Column(String)	#推导现代音

	hanzi_zi = Column(String(1),ForeignKey('hanzi.zi'))
	hanzi = relationship("hanzi", back_populates="zg")

	def __repr__(self):
		return "<zgchn(hanzi_zi='%s', zgys='%s')>" % (self.hanzi_zi, self.zgys)

class sgchn(dbmodel):
	__tablename__ = 'sgchn'

	id = Column(Integer, primary_key=True)
	shengfu = Column(String(1))								#声符
	yunbu = Column(String(1))								#韵部
	sgzz = Column(String)									#上古郑张
	xiaoyun = Column(String(1))								#对应中古韵

	hanzi_zi = Column(String(1),ForeignKey('hanzi.zi'))
	hanzi = relationship("hanzi", back_populates="sg")

	def __repr__(self):
		return "<sgchn(hanzi_zi='%s', sgzz='%s')>" % (self.hanzi_zi, self.sgzz)

class pychn(dbmodel):
	__tablename__ = 'pychn'

	id = Column(Integer, primary_key=True)
	pinyin = Column(String)
	xiaoyun = Column(String(1))	

	hanzi_zi = Column(String(1),ForeignKey('hanzi.zi'))
	hanzi = relationship("hanzi", back_populates="py")

	def __repr__(self):
		return "<pychn(hanzi_zi='%s', pinyin='%s')>" % (self.hanzi_zi, self.pinyin)

class jpn(dbmodel):
	__tablename__ = 'jpn'

	id = Column(Integer, primary_key=True)
	tang = Column(String)									#唐
	guan = Column(String)									#惯
	wuhan = relationship('jpwuhan', back_populates='jp')	#吴汉
	often = Column(String)									#常用音训
	xun = Column(String)									#训，连写
	mingfu= Column(String)									#名付读音
	mean = Column(String)									#义，连写
	hanzi = relationship("hanzi",backref="jp", foreign_keys=[hanzi.jpn_id],primaryjoin='hanzi.jpn_id == jpn.id')
	hanzi_zi = Column(String)	#数据库中有的汉字
	all_zi = Column(String)		#字典条目下的所有汉字

	# hanzi = relationship("hanzi",primaryjoin='hanzi.jpn_id == jpn.id',backref='jp')

	def __repr__(self):
		return "<jpn(tang='%s')>" % (self.tang)

class jpwuhan(dbmodel):
	__tablename__ = 'jpwuhan'

	id = Column(Integer, primary_key=True)
	zxw = Column(String)								#为了查询和分析而转写
	zxh = Column(String)
	zxw_h=Column(String)								#zxw和zxh是今天的实际读音，zxw_h和zxh_h是也许存在的历史音
	zxh_h=Column(String)
	wu = Column(String)									#吴
	han = Column(String)								#汉
	yun = Column(String)								#韵，资料中有
	xiaoyun = Column(String)							#对应小韵，程序处理

	jpn_id =  Column(Integer,ForeignKey('jpn.id'))
	jp = relationship('jpn', back_populates='wuhan')

	def __repr__(self):
		return "<jpwuhan(jpn_id='%s',wu='%s',han='%s')>" % (self.jpn_id,self.wu,self.han)

class kor(dbmodel):
	__tablename__ = 'kor'

	id = Column(Integer, primary_key=True)
	yinxun = relationship('kryinxun', back_populates='kr')	#音训，naver音训成对出现
	mean = Column(String)

	hanzi_zi = Column(String(1),ForeignKey('hanzi.zi'))
	hanzi = relationship("hanzi", back_populates="kr")

	def __repr__(self):
		return "<kor(hanzi_zi='%s')>" % (self.hanzi_zi)

class kryinxun(dbmodel):
	__tablename__ = 'kryinxun'

	id = Column(Integer, primary_key=True)
	zxy = Column(String)						#转写对音
	yin = Column(String)						#对音
	liu = Column(String)						#流音规则下的韩语实际读音
	xun = Column(String)
	xiaoyun = Column(String)
	hanzi_zi = Column(String)

	kor_id =  Column(Integer,ForeignKey('kor.id'))
	# kor_id =  Column(String,ForeignKey('kor.hanzi_zi'))
	kr = relationship('kor', back_populates='yinxun')

	def __repr__(self):
		return "<kryinxun(kor_id='%s')>" % (self.kor_id)

class vnm(dbmodel):
	__tablename__ = 'vnm'

	id = Column(Integer, primary_key=True)
	yin = relationship('vnyin',back_populates='vn')
	mean = Column(String)

	hanzi_zi = Column(String(1),ForeignKey('hanzi.zi'))
	hanzi = relationship("hanzi", back_populates="vn")

	def __repr__(self):
		return "<vnm(hanzi_zi='%s')>" % (self.hanzi_zi)

class vnyin(dbmodel):
	__tablename__ = 'vnyin'

	id = Column(Integer, primary_key=True)
	yin = Column(String)
	xiaoyun = Column(String)

	vnm_id =  Column(Integer,ForeignKey('vnm.id'))
	vn = relationship('vnm', back_populates='yin')

	def __repr__(self):
		return "<vnyin(vnm_id='%s')>" % (self.vnm_id)

def initDB(path):
	loc = myTools.SQL_URL.rfind("\\")
	if myTools.hasFile(path[0:loc],path[loc+1:]):
		return
	# newstr = myTools.SQL_URL.replace('\\','\\\\')
	# print(myTools.SQL_URL)
	try:
		# engine = create_engine('sqlite:///D:\\Progress\\githubCode\\dict_web\\data')
		engine = create_engine("sqlite:///"+path,encoding='utf8', convert_unicode=True)
		dbmodel.metadata.create_all(engine)
	except Exception as e:
		print(e)

def getSession(path):
	engine = create_engine("sqlite:///"+path,encoding='utf8', convert_unicode=True)
	DBSession = sessionmaker(bind=engine)
	return DBSession()