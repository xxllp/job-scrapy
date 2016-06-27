#coding=utf-8
###爬取一些国外IT的电子书和介绍，支持文件下载。希望能够检索和评论，类似豆瓣.国内的书相对比较烂一般
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import requests,re,pyquery ,json
from pyquery import PyQuery as pq
import csv
def download_file(url, filename):
      local_filename = filename
      # NOTE the stream=True parameter
      r = requests.get(url, stream=True)
      with open(local_filename, 'wb') as f:
          for chunk in r.iter_content(chunk_size=1024):
              if chunk: # filter out keep-alive new chunks
                  f.write(chunk)
                  f.flush()
      return local_filename

def get_ebook(url):

 #url="http://www.allitebooks.com/"
 content=requests.get(url).content
 books=[pq(e).attr.href for e in pq(content)("#main-content .entry-title a")]
 print books
 for book_url in books:
    content=pq(requests.get(book_url).content)
    book_name=content(".single-title").text()
    book_basic=[pq(e).text() for e in content(".book-detail dd")]
    book_desc=content(".entry-content p").text()
    book_down=content(".download-links a").attr.href
    book_img=content(".wp-post-image").attr.src
    print book_url
    print book_name
    print book_desc
    print book_basic
    print book_down
    #download_file(book_down,u"d:/工作/pdf/%s.pdf"%(book_name))
    yield book_name,book_img,book_desc,book_down,book_url,book_basic[0],book_basic[1],book_basic[2],book_basic[3],book_basic[7]

def all_book():
    filename=file('ebook.csv', 'wb')
    writer=csv.writer( filename)
    writer.writerow(["name","img","desc","down","url","author","ibsn","year","page","category"])
    for i in range(1,608):
        url="http://www.allitebooks.com/page/%d/"%(i)
        for e in get_ebook(url):
            print list(e)
            writer.writerow(tuple(e))
    filename.close()
all_book()


###网站API有限制，而且需要分类抓取也是够了。如何比较全面的爬取站内信息，而且能动态更新
content=requests.get("http://it-ebooks-api.info/v1/search/mysql").content
print content
for d in json.loads(content).get("Books"):
    print d.get("ID")
    book_content=requests.get("http://it-ebooks-api.info/v1/book/%s"%(d.get("ID"))).content
    print book_content