#coding=utf-8
###字段搜索统计，现在数据还不全
from whoosh import fields, index, qparser
from whoosh.qparser import MultifieldParser
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

reader=csv.reader(open("ebook.csv","r"))

schema = fields.Schema(name=fields.TEXT(stored=True),
                       author=fields.TEXT(),
                        desc=fields.TEXT(),
                       )
#ix = index.create_in("indexdir", schema)
ix = index.open_dir("indexdir",schema=schema)
# w=ix.writer()
# for item in reader:
#        if item[0]!='name':
#          print item
#          w.add_document(name=unicode(item[0]),author=unicode(item[5]),desc=unicode(item[2]))
# w.commit()

###单个字段查询,注意默认的返回数量为10
with ix.searcher() as s:
    qp = MultifieldParser(["name","author","desc"], ix.schema)
    q = qp.parse("spark")

with ix.searcher() as s:
    results = s.search(q, limit=200)
    print results
    for e in results:
        print e.fields()

def search(keyword):
    result=[]
    ix = index.open_dir("indexdir",schema=schema)

    qp = qparser.QueryParser("name", ix.schema)
    q = qp.parse(keyword)

    with ix.searcher() as s:
     results = s.search(q, limit=200)
     for e in results:
        result.extend(e.values())
    return  result