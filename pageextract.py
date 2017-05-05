#coding=utf-8
'''
 规则的url 模版自动生成，wrapper 抽取内容
 根据标题和文本分布定义正文所在的区域
'''
from bs4 import BeautifulSoup,Comment,Doctype
import re, requests
from dateutil.parser import parse
from datetime import datetime


def getDate(text):
    datereg=["20\d{2}-\d{1,2}-\d{1,2}","20\d{2}/\d{1,2}/\d{1,2}","20\d{2}\.\d{1,2}\.\d{1,2}","1\d{1}-\d{1,2}-\d{1,2}"]
    dates = []
    if len(re.findall("20\d{2}-\d{1,2}-\d{1,2}", text))>0:

        dates.extend(re.findall("20\d{2}-\d{1,2}-\d{1,2}", text))

    if len(re.findall(ur"20\d{2}年\d{1,2}月\d{1,2}日?", text))>0:
        for e in re.findall(ur"20\d{2}年\d{1,2}月\d{1,2}日?", text):
            y, m, d=re.findall("\d+",e)
            # print y, m, d
            # print parse(y+'-'+m+'-'+d)
            dates.extend([y+'-'+m+'-'+d])
    if len(re.findall("20\d{2}/\d{1,2}/\d{1,2}", text)) > 0:
        dates.extend(re.findall("20\d{2}/\d{1,2}/\d{1,2}", text))
    if len(re.findall("20\d{2}\.\d{1,2}\.\d{1,2}",text)) > 0:
        dates.extend(re.findall("20\d{2}\.\d{1,2}\.\d{1,2}", text))
    if len(re.findall("1\d{1}-\d{1,2}-\d{1,2}", text)) > 0:
        dates.extend(["20"+e for e in re.findall("1\d{1}-\d{1,2}-\d{1,2}", text)])
    if len(dates) > 0:
        ds = []
        for e in set(dates):
            try:
                e = datetime.strftime(parse(e), "%Y-%m-%d")
                ds.append(e)
            except Exception:
                pass
        return ds

    return []

content=requests.get("http://www.forestry.gov.cn/main/424/content-973768.html").content

s=BeautifulSoup(content,"lxml")
[ss.extract() for ss in s('style')]
[ss.extract() for ss in s('script')]
[ss.extract() for ss in s('a')]
comments = s.findAll(text=lambda text:isinstance(text, Comment))
[comment.extract() for comment in comments]
doctypes = s.findAll(text=lambda text:isinstance(text, Doctype))
[doctype.extract() for doctype in doctypes]
#s.prettify()
s=s.find("body")
head= s.find(text=u"积极推进天然林保护工程　让“生态”和“民生”两条腿走路" )
print(head.parent)
#print head.parent["class"]
#print head.parent["id"]
midtext=head.find_parent(["table","div"]).find_parent(["table","div"])
print unicode(midtext)
date=getDate(unicode(midtext))
print date
for e in  midtext.findAll(text=lambda text:text is not None and text !="\n"):
        print e




