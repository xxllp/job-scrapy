#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
###爬取公司的面试评价，对自己找工作会有点帮助.拉钩的数据基本都是有对应的api服务的
####先爬取公司的基本信息，再爬取其评价信息
import requests,json,math
from __future__ import division

def getcompany_comment(companyId,pageNo=1,pageSize=16):
    url="http://www.lagou.com/gongsi/searchInterviewExperiences.json"
    content=requests.post(url,data={'companyId':companyId,'pageSize':pageSize,'pageNo':pageNo}).content
    print content
    try:
     data=json.loads(content).get("content").get("data").get("page").get("result")
     for d in data:
          yield d
    except Exception as e :
         print e
#getcompany_comment(13809)
file=open("aa.txt",'wb')
gongsi="http://www.lagou.com/gongsi/0-0-0.json"
content=requests.post(gongsi,data={'first':'false','pn':'1','sortField':'2','havemark':'0'}).content
print content
try:
    data=json.loads(content).get("result")
    for d in data:
        #print dict(d).keys()
        interviewRemarkNum=d.get("interviewRemarkNum")
        companyId=d.get("companyId")
        num=math.ceil(interviewRemarkNum/16)
        print d.get("companyLabels")
        print d.get("companyId")
        print d.get("companyShortName")
        for  n in range(1,num+1):
           for i in getcompany_comment(companyId,pageNo=n):
              print i
              file.write(i.get("companyName")+u":"+i.get("content"))
except Exception as e :
    print e
file.close()
