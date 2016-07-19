#coding=utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
###爬取公司的面试评价，对自己找工作会有点帮助.拉钩的数据基本都是有对应的api服务的
####先爬取公司的基本信息，再爬取其评价信息
import requests,json,math


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

###获取拉钩的企业所有数据,因为不知道数量，所以只能测试
def get_company(page=300):
    gongsi="http://www.lagou.com/gongsi/0-0-0.json"
    for i in range(1,page+1):
     content=requests.post(gongsi,data={'first':'false','pn':i,'sortField':'2','havemark':'0'}).content
     print content
     try:
       data=json.loads(content).get("result")
       for d in data:
          yield d
     except Exception as e :
       print e

# company=get_company(page=313)
# with open("company.json","wb") as w:
#     for com in company:
#      w.writelines(json.dumps(com)+"\n")


file=open("company.json",'r')
w=open("comments.json","wb")
for d in file.readlines():
        d=json.loads(d)
        interviewRemarkNum=d.get("interviewRemarkNum")
        companyId=d.get("companyId")
        num=int(math.ceil(interviewRemarkNum/16))
        print d.get("companyLabels")
        print d.get("companyId")
        print d.get("companyShortName")
        for  n in range(1,num+1):
           for i in getcompany_comment(companyId,pageNo=n):
              print i
              w.write(json.dumps(i)+"\n")

file.close()
w.close()


###新增，获取每个公司下面的职位信息，对职位介绍提取关键字和推荐
