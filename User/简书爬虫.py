#coding=utf-8
##爬取简述站内信息，补充用户,详情页需要翻页.无需登录，速度比较一般
import re,time
import pyquery,time
from pybloom import BloomFilter

##爬取单个页面的内容,对于页面中粉丝数不足的可以提前筛选掉,需要获取数量
def get_detail(url):
     pq=pyquery.PyQuery(url)
     pic=[pq(e).attr.src for e in pq(".users li > a img")]
     followings=[re.findall("/users/(.*)",pq(e).attr.href)[0] for e in pq(".users li h4 a ")]
     name=[e.text for e in pq(".users li h4 a ")]
     return pic,followings,name

##获取某个user的follows或者fans，翻页比较多，还存在一些企业号对应的关注。只看粉丝列表
def get_follow(userid):
     pics=[]
     followings=[]
     names=[]
     ###有些用户界面不存在直接pass
     try :
      pq=pyquery.PyQuery("http://www.jianshu.com/users/%s/latest_articles"%(userid))
      stat=pq(".user-stats li b").text().split(" ")
      n1=int(stat[0])/10
      n2=int(stat[1])/10  if int(stat[1]) %10==0 else int(stat[1])/10+1
      print n1,n2
     except Exception as e:
      print e
      n2=0
     # if n1>0:
     #  for i in range(1,n1+1):
     #   url="http://www.jianshu.com/users/%s/following?page=%d"%(userid,i)
     #   pic,following,name=get_detail(url)
     #   pics.extend(pic)
     #   followings.extend(following)
     #   names.extend(name)
     if n2>0:
      for i in range(1,min(n2,200)+1):
       url="http://www.jianshu.com/users/%s/followers?page=%d"%(userid,i)
       print url
       time.sleep(0.5)
       try:
          pic,following,name=get_detail(url)
       except Exception as e:
          pic,following,name=[],[],[]
       pics.extend(pic)
       followings.extend(following)
       names.extend(name)
     return pics,followings,names

#初始化现有的用户id,主要为了判断遍历的用户是否爬取过，用bloomFilter
def user_init():
    import re
    users = BloomFilter(10000000, 0.001)
    f= open(u"D:/工作/数据美化/data/简书用户id1.txt")
    for line in f:
        users.add(line.strip())
    return users

###深度爬取,主要问题就是无法中断，因为一直在爬取，可以添加数量

def get_all(init_id,f,f1,f2):
###init_users为操作的user集合(爬虫队列)，all为所有的已爬取的user集合
    init_users=set()
    init_users.add(init_id)
    all_users=user_init()
    while len(init_users)>0:
        u=init_users.pop()
        print(u)
        if u not in all_users:

          file=open(f,"a")
          file1=open(f1,"a")
          file2=open(f2,"a")
          all_users.add(u)
          #time.sleep(3)
          pics,followings,names=get_follow(u)
          print pics
          print followings
          for pic,id,name in zip(pics,followings,names):
              ##如果新用户不在消息中，且不是老用户，添加
              if id not in all_users and  id not in init_users:
               init_users.add(id)
               file.write(pic+"\n")
               file1.write(name.encode("utf-8")+"\n")
               file2.write(id+"\n")
          file.close()
          file1.close()
          file2.close()

# pics,followings,names= get_follow("f59fa3849810")
# print pics
# print followings
# print names
get_all("49f7ed6bc050",u"D:/工作/数据美化/data/简书用户照片1.txt",u"D:/工作/数据美化/data/简书用户名1.txt",u"D:/工作/数据美化/data/简书用户id1.txt")

