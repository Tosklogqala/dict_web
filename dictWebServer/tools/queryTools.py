# coding=utf-8
from ..dbModel import dbmodel
from . import myTools as tl
import json
import re

import datetime
# import sys
# import io
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# __all__ = ['queryTools']

class queryTools(object):
    # __instance = None

    # def __new__(cls, *args, **kwargs):
    #     if cls.__instance is None:
    #         cls.__instance = super(queryTools, cls).__new__(cls, *args, **kwargs)
    #     return cls.__instance

    def __init__(self):
        self._time=0
        self.entryPerPage=20
        self.searchZi=""
        self.opt=""
        self.origin=False # 日語歷史假名遣 韓語頭部流音不保留 則為True

    def danHanzi(self,zi):
        if len(zi)<1 or len(zi)>1:
            return -1,[]

        session = dbmodel.getSession(tl.SQL_URL)
        zilist = session.query(dbmodel.hanzi).filter(dbmodel.hanzi.zi==zi).all()

        err = 0
        if len(zilist)==1:
            err = 1
            results = self.parseAZi(zilist[0])
        else:
            self.searchZi = zi
            self.opt = "hanzi"
            results = self.parseFromZiList(zilist)

        session.close()
        return err,results

    def queryList(self,page,maxfunc,queryfunc):
        session = dbmodel.getSession(tl.SQL_URL)
        total = maxfunc(session)
        totalpage = int(total/self.entryPerPage)+1
        if page>totalpage:
            return -2,[],totalpage
        offset = (page-1)*self.entryPerPage
        zglist = queryfunc(session,offset)
        zilist = []
        # if makelist == "":
        [zilist.append(entry.hanzi) for entry in zglist if not entry.hanzi in zilist]
        # else:
        #     if makelist == "kor":
        #         [zilist.append(entry.kr.hanzi) for entry in zglist if not entry.kr.hanzi in zilist]
        #     elif makelist == "jpn":
        #         for entry in zglist:
        #             for hz in entry.jp.hanzi:
        #                 if not hz in zilist:
        #                     zilist.append(hz)

        results = self.parseFromZiList(zilist)
        session.close()
        return 0,results,totalpage

    def queryListForeign(self,page,maxfunc1,maxfunc2,queryfunc1,queryfunc2,makelist=""):
        session = dbmodel.getSession(tl.SQL_URL)

        total = maxfunc1(session)
        if total==0:
            total = maxfunc2(session)
            if total == 0:
                return -3,[],1
            else:
                self.origin = True

        totalpage = int(total/self.entryPerPage)+1
        if page>totalpage:
            return -2,[],totalpage
        offset = (page-1)*self.entryPerPage

        zglist = []
        if self.origin:
            zglist = queryfunc2(session,offset)
        else:
            zglist = queryfunc1(session,offset)

        zilist = []

        if makelist == "kor":
            [zilist.append(entry.kr.hanzi) for entry in zglist if not entry.kr.hanzi in zilist]
        elif makelist == "jpn":
            for entry in zglist:
                for hz in entry.jp.hanzi:
                    if not hz in zilist:
                        zilist.append(hz)

        results = self.parseFromZiList(zilist)
        session.close()
        return 0,results,totalpage

    def danSheng(self,zi,page):
        if len(zi)<1 or len(zi)>1:
            return -1,[],1

        self.searchZi = zi
        self.opt = "sheng"

        err,results,totalpage = self.queryList(page,
            lambda x:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.sheng==zi).count(),
            lambda x,y:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.sheng==zi).order_by(dbmodel.zgchn.hanzi_zi).offset(y).limit(self.entryPerPage+1)
            )

        return err,results,totalpage

    def danYun(self,zi,page):
        if len(zi)<1 or len(zi)>1:
            return -1,[],1

        self.searchZi = zi
        self.opt = "yun"

        err,results,totalpage = self.queryList(page,
            lambda x:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.yun==zi).count(),
            lambda x,y:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.yun==zi).order_by(dbmodel.zgchn.hanzi_zi).offset(y).limit(self.entryPerPage+1)
            )

        return err,results,totalpage

    def danXiaoyun(self,zi,page):
        if len(zi)<1 or len(zi)>1:
            return -1,[],1

        self.searchZi = zi
        self.opt = "xiaoyun"

        err,results,totalpage = self.queryList(page,
            lambda x:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.xiaoyun==zi).count(),
            lambda x,y:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.xiaoyun==zi).order_by(dbmodel.zgchn.hanzi_zi).offset(y).limit(self.entryPerPage+1)
            )

        return err,results,totalpage

    def danZgys(self,zi,page):
        check = re.findall("[a-zA-Z\-]+",zi)
        if len(check) < 1 or check[0] != zi:
            return -1,[],1

        self.searchZi = zi
        self.opt = "zgys"

        pipei = zi
        pipei = pipei.replace("-","%")

        err,results,totalpage = self.queryList(page,
            lambda x:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.zgys.like(pipei)).count(),
            lambda x,y:x.query(dbmodel.zgchn).filter(dbmodel.zgchn.zgys.like(pipei)).order_by(dbmodel.zgchn.hanzi_zi).offset(y).limit(self.entryPerPage+1)
            )

        return err,results,totalpage

    def danPinyin(self,zi,page):
        check = re.findall("[a-zA-Z1-4\-]+",zi)
        if len(check) < 1 or check[0] != zi:
            return -1,[],1

        self.searchZi = zi.replace("-","")
        self.opt = "pychn"

        pipei = zi
        pipei = pipei.replace("-","%")
        diao = re.findall("[1-4]",pipei)
        if len(diao) > 1:
            return -1,[],1
        if len(diao)==0:
            pipei += "_"

        err,results,totalpage = self.queryList(page,
            lambda x:x.query(dbmodel.pychn).filter(dbmodel.pychn.pinyin.like(pipei)).count(),
            lambda x,y:x.query(dbmodel.pychn).filter(dbmodel.pychn.pinyin.like(pipei)).order_by(dbmodel.pychn.hanzi_zi).offset(y).limit(self.entryPerPage+1)
            )

        return err,results,totalpage

    def danJpn(self,zi,page,wh):
        pipei = ""
        check1 = re.findall("[a-zA-Z\-]+",zi)
        if len(check1)==1 and check1[0] == zi:
            pipei = zi
        else:
            check2 = re.findall("[ア-ンあ-ん]+",zi)
            if len(check2)==1 and check2[0] == zi:
                pipei = tl.jToR(zi)
            else:
                return -1,[],1

        pipei = pipei.replace("-","%")

        self.searchZi = pipei.replace("%","")
        self.opt = "jpn" + wh

        err = 0
        if wh == "wu":
            err,results,totalpage = self.queryListForeign(page,
                lambda x:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxw.like(pipei)).count(),
                lambda x:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxw_h.like(pipei)).count(),
                lambda x,y:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxw.like(pipei)).order_by(dbmodel.jpwuhan.jpn_id).offset(y).limit(self.entryPerPage+1),
                lambda x,y:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxw_h.like(pipei)).order_by(dbmodel.jpwuhan.jpn_id).offset(y).limit(self.entryPerPage+1),
                "jpn"
                )
        else:
            err,results,totalpage = self.queryListForeign(page,
                lambda x:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxh.like(pipei)).count(),
                lambda x:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxh_h.like(pipei)).count(),
                lambda x,y:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxh.like(pipei)).order_by(dbmodel.jpwuhan.jpn_id).offset(y).limit(self.entryPerPage+1),
                lambda x,y:x.query(dbmodel.jpwuhan).filter(dbmodel.jpwuhan.zxh_h.like(pipei)).order_by(dbmodel.jpwuhan.jpn_id).offset(y).limit(self.entryPerPage+1),
                "jpn"
                )

        return err,results,totalpage

    def danKor(self,zi,page):
        pipei = ""
        check1 = re.findall("[a-zA-Z\-]+",zi)
        if len(check1)==1 and check1[0] == zi:
            pipei = zi
        else:
            check2 = re.findall("[가-힣ㄱ-ㅣ]+",zi)
            if len(check2)==1 and len(check2[0])==1:
                pipei = tl.hToR(check2[0])
            else:
                return -1,[],1

            if zi.find("-")==0:
                pipei = "-" + pipei
            elif zi.find("-")>0:
                pipei = pipei + "-"

        pipei = pipei.replace("-","%")

        self.searchZi = pipei.replace("%","")
        self.opt = "kor"

        err,results,totalpage = self.queryListForeign(page,
            lambda x:x.query(dbmodel.kryinxun).filter(dbmodel.kryinxun.zxy.like(pipei)).count(),
            lambda x:x.query(dbmodel.kryinxun).filter(dbmodel.kryinxun.liu.like(pipei)).count(),
            lambda x,y:x.query(dbmodel.kryinxun).filter(dbmodel.kryinxun.zxy.like(pipei)).order_by(dbmodel.kryinxun.hanzi_zi).offset(y).limit(self.entryPerPage+1),
            lambda x,y:x.query(dbmodel.kryinxun).filter(dbmodel.kryinxun.liu.like(pipei)).order_by(dbmodel.kryinxun.hanzi_zi).offset(y).limit(self.entryPerPage+1),
            "kor"
            )

        return err,results,totalpage

    def danVnm(self,zi,page):
        pass

    def parseFromZiList(self,zilist):
        results = []
        for one in zilist:
            # if not "zg" in one.keys():
            #     continue
            resultOfZi=[]
            for zgy in one.zg:
                if self.opt=="xiaoyun" and self.searchZi!=zgy.xiaoyun:
                    continue
                if self.opt=="sheng" and self.searchZi!=zgy.sheng:
                    continue
                if self.opt=="yun" and self.searchZi!=zgy.yun:
                    continue
                if self.opt=="zgys":
                    _t = self.searchZi.replace("-","")
                    if zgy.zgys.find(_t) < 0:
                        continue    

                line={}
                if len(resultOfZi)==0:
                    line['zi']='<a href="/dan?zi='+one.zi+'&opt=hanzi">'+one.zi+'</a>'
                    line['_zi']=one.zi
                else:
                    line['zi']=""
                    line['_zi']=""

                line['xiaoyun'] = '<a href="/dan?zi='+zgy.xiaoyun+'&opt=xiaoyun">'+zgy.xiaoyun+'</a>'
                line['_xiaoyun']= zgy.xiaoyun
                line['fanqie']  = zgy.fanqie_1+zgy.fanqie_2
                line['sheng']   = zgy.sheng
                line['yun']     = zgy.yun
                line['diao']    = zgy.diao
                line['deng']    = zgy.deng
                line['hu']      = zgy.hu
                line['she']     = zgy.she
                line['zgzz']    = zgy.zgzz
                line['zgys']    = zgy.zgys

                resultOfZi.append(line)

            if len(one.sg)>0:
                self.langAddToColumn(one.sg,resultOfZi,self.addSg,one.zi)

            if len(one.py)>0:
                self.langAddToColumn(one.py,resultOfZi,self.addPy,one.zi)

            if one.jpn_id != None:
                self.langAddToColumn(one.jp.wuhan,resultOfZi,self.addJp,one.zi)

            if len(one.kr)>0:
                self.langAddToColumn(one.kr[0].yinxun,resultOfZi,self.addKr,one.zi)

            if len(one.vn)>0:
                self.langAddToColumn(one.vn[0].yin,resultOfZi,self.addVn,one.zi)

            [results.append(y) for y in resultOfZi]

        return results

    def langAddToColumn(self,lang,dic,func,zi):
        size = len(dic)
    # 若不存在中古韻，建立新的行来填写本语言信息
        if size == 0:
            line={}
            line['zi']='<a href="/dan?zi='+zi+'&opt=hanzi">'+zi+'</a>'
            line['_zi']=zi
            for entry in lang:
                func(entry,line)
            dic.append(line)
    # 若只有一個中古韻，則顯示在一行。（也许上古多于一行时，应建立新的行？）
        elif size==1:
            for entry in lang:
                #填在第一行而不匹配当行中古韵的读音，用特殊字体标识
                if '_xiaoyun' in dic[0].keys():
                    if entry.xiaoyun and entry.xiaoyun.find(dic[0]['_xiaoyun'])>=0:
                        func(entry,dic[0])
                    else:
                        # 若本条目未記錄小韻，則顯示本条目。
                        # 若已記錄小韻，卻找不到同小韻的中古條目，則認為此條目不屬於所查詢的結果
                        if self.opt=="sheng" or self.opt=="yun" or self.opt=="xiaoyun" or self.opt=="zgys":
                            if entry.xiaoyun=="" or entry.xiaoyun is None:
                                func(entry,dic[0],False)
                        else:
                            func(entry,dic[0],False)
                else:
                    func(entry,dic[0])
        elif size>1:
    # 若存在多个中古韻，則能匹配的填在對應的後面。
            for entry in lang:
                found=False
                for x in range(0,size):
                    if '_xiaoyun' in dic[x].keys():
                        if entry.xiaoyun and entry.xiaoyun.find(dic[x]['_xiaoyun'])>=0:
                            func(entry,dic[x])
                            found=True
                            break
    # 若不能匹配到中古韻。則填在第一行。
                #填在第一行而不匹配当行中古韵的读音，用特殊字体标识
                if not found:
                    if self.opt=="sheng" or self.opt=="yun" or self.opt=="xiaoyun" or self.opt=="zgys":
                        if entry.xiaoyun=="" or entry.xiaoyun is None:
                            func(entry,dic[0],False)
                    else:
                        func(entry,dic[0],False)

    def addSg(self,entry,ary,bold=True):
        self.safeAppend('shengfu',entry.shengfu,ary)
        self.safeAppend('yunbu',entry.yunbu,ary)
        self.safeAppend('sgzz',entry.sgzz,ary)

    def addPy(self,entry,ary,bold=True):
        if bold==True:
            self.safeAppend('pinyin',entry.pinyin,ary)
        else:
            self.safeAppend('pinyin',"<b class='f'>"+entry.pinyin+"</b>",ary)

    def addJp(self,entry,ary,bold=True):
        done = ""
        if self.opt == "jpnwu":
            if self.origin:
                if entry.zxw_h.find(self.searchZi)>=0:
                    self.safeAppend('wu',"<b class='h'>"+entry.wu+"</b>",ary)
                    done = "wu"
            else:
                if entry.zxw.find(self.searchZi)>=0:
                    self.safeAppend('wu',"<b class='h'>"+entry.wu+"</b>",ary)
                    done = "wu"

        if self.opt == "jpnhan":
            if self.origin:
                if entry.zxh_h.find(self.searchZi)>=0:
                    self.safeAppend('han',"<b class='h'>"+entry.han+"</b>",ary)
                    done = "han"
            else:
                if entry.zxh.find(self.searchZi)>=0:
                    self.safeAppend('han',"<b class='h'>"+entry.han+"</b>",ary)
                    done = "han"

        if bold==True:
            if done != "wu":
                self.safeAppend('wu',entry.wu,ary)
            if done != "han":
                self.safeAppend('han',entry.han,ary)
        else:
            if done != "wu":
                self.safeAppend('wu',"<b class='f'>"+entry.wu+"</b>",ary)
            if done != "han":
                self.safeAppend('han',"<b class='f'>"+entry.han+"</b>",ary)

    def addKr(self,entry,ary,bold=True):
        ky=""
        if entry.liu == "":
            ky=entry.yin
        else:
            ky=entry.yin+"("+entry.liu+")"

        if self.opt == "kor":
            if self.origin:
                if entry.liu.find(self.searchZi)>=0:
                    self.safeAppend('kr',"<b class='h'>"+ky+"</b>",ary)
                    return
            else:
                if entry.zxy.find(self.searchZi)>=0:
                    self.safeAppend('kr',"<b class='h'>"+ky+"</b>",ary)  
                    return

        self.safeAppend('kr',ky,ary)

    def addVn(self,entry,ary,bold=True):
        self.safeAppend('vn',entry.yin,ary)

    def testTimeStart(self):
        self._time = datetime.datetime.now().microsecond

    def testTimePrint(self):
        _delta = datetime.datetime.now().microsecond - self._time
        self._time = datetime.datetime.now().microsecond
        print("%d"%(_delta))

    @staticmethod
    def safeAppend(dst,src,dic):
        if dst in dic.keys() and dic[dst]!="":
            dic[dst] = dic[dst] + "," + src
        else:
            dic[dst] = src

    # 顯示單個漢字的頁面
    @staticmethod
    def parseAZi(azi):
        result = {}
        result["zi"] = azi.zi
        result["sg"] = azi.sg
        result["zg"] = azi.zg
        result["py"] = azi.py

        result["jp"] = {}
        if azi.jp is not None:
            if not azi.jp.tang == "":
                result["jp"]["tang"] = azi.jp.tang
            if not azi.jp.guan == "":
                result["jp"]["guan"] = azi.jp.guan
            if not azi.jp.often == "":
                result["jp"]["often"] = azi.jp.often
            if not azi.jp.xun == "":
                result["jp"]["xun"] = azi.jp.xun
            if not azi.jp.mingfu == "":
                result["jp"]["mingfu"] = azi.jp.mingfu
            if not azi.jp.mean == "":
                tmp = azi.jp.mean.strip()
                for i in range(2,20):
                    tmp.replace("%d."%i,"\n")
                result["jp"]["mean"] = tmp.split("\n")
            result["jp"]["wuhan"] = azi.jp.wuhan

        result["kr"] = {}
        if len(azi.kr) > 0 :
            result["kr"]["mean"] = json.loads(azi.kr[0].mean)
            result["kr"]["yinxun"]=azi.kr[0].yinxun

        result["vn"] = {}
        if len(azi.vn) > 0 :
            result["vn"]["mean"] = azi.vn[0].mean
            result["vn"]["yin"] = azi.vn[0].yin     

        return result