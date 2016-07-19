#coding=utf-8
###将json格式的数据拿出来写到csv文件里面
import json,csv,sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')
###将json转数据框
file=open("company.json",'r')
w=csv.writer(open("company.csv","ab+"))
data=pd.DataFrame(columns=["city","industryField","finaceStage","companyName","score","createTime","companyId","companyLabels","positionNum","searchScore","otherLabels"])
w.writerow(["city","industryField","finaceStage","companyName","score","createTime","companyId","companyLabels","positionNum","searchScore","otherLabels"])
#csv=open("company.json","wb")
for d in file.readlines():
        d=json.loads(d)
        city=d.get("city")
        industryField=d.get("industryField")
        finaceStage=d.get("finaceStage")
        companyName=d.get("companyName")
        score=d.get("score")
        createTime=d.get("createTime")
        companyId=d.get("companyId")
        companyLabels=d.get("companyLabels")
        positionNum=d.get("positionNum")
        searchScore=d.get("searchScore")
        otherLabels=d.get("otherLabels")
        line=[city,industryField,finaceStage,companyName,score,createTime,companyId,companyLabels,positionNum,searchScore,otherLabels]
        w.writerow(line)


file=open("comments.json",'r')
w=csv.writer(open("comments.csv","ab+"))
w.writerow(["companyName","companyId","userId","isInterview","positionName","createTime","tags","comprehensiveScore","companyScore","interviewerScore","describeScore","content"])
#csv=open("company.json","wb")
for d in file.readlines():
        d=json.loads(d)
        companyName=d.get("companyName")
        companyId=d.get("companyId")
        userId=d.get("userId")
        isInterview=d.get("isInterview")
        positionName=d.get("positionName")
        createTime=d.get("createTime")
        tags=d.get("tags")
        comprehensiveScore=d.get("comprehensiveScore")
        companyScore=d.get("companyScore")
        interviewerScore=d.get("interviewerScore")
        describeScore=d.get("describeScore")
        content=d.get("content")
        line=[companyName,companyId,userId,isInterview,positionName,createTime,tags,comprehensiveScore,companyScore,interviewerScore,describeScore,content]
        w.writerow(line)
