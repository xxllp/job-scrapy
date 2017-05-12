#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
'''
 规则的url 模版自动生成，wrapper 抽取内容
 根据标题和文本分布定义正文所在的区域

 过滤掉标题前和正文后的附带内容和中间的部分不需要的东西

存在问题：选择的区域太小或者太大，正文中包含链接。从上往下找title，如果找到则不在分割
'''
from bs4 import BeautifulSoup,Comment,Doctype
from pyquery import PyQuery as p
import re, requests
from dateutil.parser import parse
from datetime import datetime
import pymysql
import logging
from urlparse import urlparse,urljoin
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
}

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='d:/tmp/zw.log',
                    encode="utf-8",
                    filemode='a')

def getDate(text):
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

# 直接对bs 对象获取文本中时间
def bgetDate(s):
    dateitem=s.find(text=lambda text:len(getDate(text))>0)
    if dateitem :
      date=getDate(unicode(dateitem))[0]
    else :
       date=""
    return dateitem,date
'''
修改标题统一为h3
'''

def pathparse(html,url):
    for img in [e.attr.src for e in p(html)("img").items()]:
        newimg=urljoin(url,img)
        html=html.replace(img,newimg)
    return  html



##如何删除中间 和末尾的多余信息
## 标题如果还有问题，可以用网页的标题进行强化
###目前的正文定温还是容易出错
def pagedetail(url,title):
    print(url)
    #logging.info(str(url))
    content=requests.get(url,headers=headers).content
    s=BeautifulSoup(content,"lxml")
    # pagetitle=s.find("head")
    # print pagetitle
    # 过滤一些无用信息
    [ss.extract() for ss in s('style')]
    [ss.extract() for ss in s('script')]
    comments = s.findAll(text=lambda text:isinstance(text, Comment))
    [comment.extract() for comment in comments]
    doctypes = s.findAll(text=lambda text:isinstance(text, Doctype))
    [doctype.extract() for doctype in doctypes]

    if s is None :
        return ("","","","")

    # 获取标题的位置
    sc=s.find("body")
    #print sc

    # if sc("a"):
    #    [ss.extract()  for ss in sc('a')]
    midtext=[e for e in sc.descendants if title in unicode(e) and u"。" in unicode(e)][-1]
    print midtext
    head= midtext.find(text=lambda text:title in text and ">" not in text and text.parent.name<>'title'and text.parent.name<>'a')


    print(head.parent)
    head.parent.name = "h1"

    ###递归删除head前面的内容
    # pa=head.parent
    # while pa:
    #     pas=pa.find_previous_siblings()
    #     if len(pas)>0:
    #        [ss.extract() for ss in pas]
    #     pa=pa.parent
    #print head.parent["class"]
    #print head.parent["id"]
    # midtext=head.find_parent(["table","div"]).find_parent(["table","div"])
    # if midtext is None:
    #    midtext=head.find_parent(["table","div"])
    #print midtext
    dateitem,date=bgetDate(midtext)

    print date
    #[ss.parent.extract()  for ss in s('a')]
    ##删除标题和正文中间内容

    # if dateitem:
    #
    #   if max([ e in dateitem.parent.find_previous_siblings() for e in head.parents ])>0:
    #        dateitem.parent.extract()
    #   else:
    #
    #        dateitem.parent.parent.extract()
    # cishu=s.find(text=lambda text:u"阅读" in text or u"浏览次数" in text or u'浏览数' in text  or u"次数" in text or u"点击次数" in text or u"访问次数" in text or u"点击" in text or  u"来源" in text or u"作者" in text or u"日期" in text
    #              or u"时间" in text)
    # if cishu:
    #     if head.parent in cishu.parent.find_previous_siblings():
    #        cishu.parent.extract()
    #     else:
    #        cishu.parent.parent.extract()

    # if len(cishu)>0:
    #  [ss.extract() for ss in cishu]
     # for c in cishu:
     #
     #     [ss.extract() for ss in c.parent  if c.parent is not None ]
    midtext=[e for e in midtext.descendants if  u"。" in unicode(e) and title not  in unicode(e)][0]

    # tail=sc.find(text=lambda text:u"上一篇" in text or u"下一篇" in text or u"上一条" in text or u"下一条" in text or u"上一页" in text or u"下一页" in text or u'分享到' in text or u'分享至' in text or u'没有了' in text or u'相关新闻' in text or u'相关文章' in text  or
    #                              u'相关信息' in text or u'相关报道' in text or ">>" in text or u'打印' in text  or u'关闭' in text)
    # print tail
    # tails=[]
    # if tail:
    #
    #     if head.parent in tail.parent.find_previous_siblings():
    #         pa=tail.parent
    #         pas=pa.find_next_siblings()
    #         #pa.extract()
    #         tails.append(pa)
    #         tails.extend(pas)
    #     else:
    #         pa=tail.parent.parent
    #         pas=pa.find_next_siblings()
    #         #pa.extract()
    #         tails.append(pa)
    #         tails.extend(pas)
    # ##删除结尾内容
    #     while pa.name<>'body':
    #           #[ss.extract() for ss in pas]
    #           pa=pa.parent
    #           if pa:
    #              pas=pa.find_next_siblings()
    #              tails.extend(pas)
    #
    #     print tails
    #     [ss.extract() for ss in tails]
        # while pa:
        #    pas=pa.find_next_siblings()
        #    print pas
        #
        #    if len(pas)>0:
        #       [ss.extract() for ss in pas]
        #    pa=pa.parent


    # if len(tail)>0:
    #   [ss.extract() for ss in tail]
      # for t in tail:
      #   [ss.extract() for ss in t.parent if t.parent is not None ]
    head.parent.extract()

    #midtext=head.find_parent(["table","div"]).find_parent(["table","div"])
    ##删除正文后无关内容
    midtext= BeautifulSoup(re.subn("<\?.*>","",unicode(midtext))[0],"lxml").find("body")


    text="\n".join([e for e in midtext.findAll(text=lambda text:text is not None and text !="\n")]).strip()
    print text
    return (unicode(head).strip(),date,text,pathparse(unicode(midtext),url))


'''
测试哪里存在问题
'''
def test():

    con=pymysql.connect(host="crawl.v5time.net",user="tfdata",port=3366,password="tfdatapw",database="datazf",charset='utf8')

    cur = con.cursor()
    cur.execute("select distinct pageurl,title from zfurl where sdate>'2017-05-09'and length(title)>10 order by sdate")
    for u in cur.fetchall():
        title=u[1].strip().replace(u"・","")
        print  title
        pageurl=u[0]
        if len(title)>10:
             pagedetail(pageurl,title[1:7])

def isIn(base,url):
    base=urlparse(base).netloc
    url=urlparse(url).netloc
    if base ==url:
        return True
    else :
        return False

def pagedetailextract(tb="zfurl"):
    con=pymysql.connect(host="crawl.v5time.net",user="tfdata",port=3366,password="tfdatapw",database="datazf",charset='utf8')

    cur = con.cursor()
    #select distinct pageurl from parsepage a where not exists (select pageurl from pagedetail b where a.pageurl=b.pageurl)

    cur.execute('''
    select distinct a.pageurl,a.url,a.title from {} a
 where  pageurl not like "%/" and
    pageurl not like "%cn"  and pageurl not like "%com"  and pageurl not like "%org"
    and pageurl not like "%net" and pageurl not like "%pdf" and pageurl not like "%JPG" and pageurl not like "%login%" and  pageurl not like "%doc" and
   sdate >= '2017-05-12 00:00:00' and sdate <= '2017-05-13 00:00:00'and  not exists (select pageurl from pagedetail1 b where a.pageurl=b.pageurl)

 '''.format(tb))

    for u in cur.fetchall():
        try:
            url = u[0]
            title=u[2].replace(" ","").replace("・","").replace("·","")
            print title
            if  len(title)<6:
                continue
            if  u"标题" in title:
                continue
            base=u[1]
            print url
            if isIn(base,url):
                (title,date,contents,pcontents)=pagedetail(url,title[0:4])
                tt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("insert into pagedetail1(pageurl,title,content,pdate,edate,pcontent) values ('{}','{}','{}','{}','{}','{}')".format(url, title, pymysql.escape_string(contents), date,tt,pymysql.escape_string(pcontents)))
                con.commit()
            else:
                print 1111
                pass
        except Exception as e :
             print(e)
             # con = pymysql.connect(host="crawl.v5time.net",user="tfdata",port=3366,password="tfdatapw",database="datazf",charset='utf8')
             # cur = con.cursor()
             # cur.execute(sql)
             # con .commit()
             # con.close()

    con.close()

if __name__ == '__main__':
    # title=u"·长风乡召开文明创建工作部署会议".replace(u"·","")
    # print  title
    # (title,date,contents,pcontents)=pagedetail("http://www.taihe.gov.cn/content/detail/59102d0e7f8b9aa31fac7cd7.html","肖口镇：“五聚焦”扎实推进基层党组织标准化建设")
    # con=pymysql.connect(host="crawl.v5time.net",user="tfdata",port=3366,password="tfdatapw",database="datazf",charset='utf8')
    #
    # cur = con.cursor()
    # cur.execute("insert into pagedetail1(pageurl,title,content,pdate,edate,pcontent) values ('{}','{}','{}','{}','{}','{}')".format("http://www.taihe.gov.cn/content/detail/59102d0e7f8b9aa31fac7cd7.html", title, pymysql.escape_string(contents), date,"",pymysql.escape_string(pcontents)))
    # con.commit()
    # con.close()
    #pagedetail("http://wtxg.es.gov.cn/gbys/201705/t20170505_386224.html","红土：进一步推进“户户通”工程建设工作")
    #pagedetail("http://bjhdw.cn/showarticle.asp?ArticleID=2848","广东省公布水路运输“十三五”规划研究")
    pagedetail("http://www.cdrb.com.cn/html/2017-05/05/content_68897.htm","2017年“熊猫杯”国际青年足球锦标赛5月中旬在蓉开赛 ")
    #pagedetailextract()
    # pagedetailextract("zfurl_gd")
    # pagedetailextract("zfurl_zj")
    # pagedetailextract("zfurl_shanxi")
    # pagedetailextract("zfurl_bj")
    # pagedetailextract("zfurl_hubei")
    # pagedetailextract("zfurl_hebei")
    # pagedetailextract("zfurl_sc")
    # pagedetailextract("zfurl_sh")
    # pagedetailextract("zfurl_yunnan")





