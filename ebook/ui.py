#coding=utf-8
###简单的图书列表和检索，需要支持很多
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, render_template, request
import csv
from searchofbook import search

app = Flask(__name__)
reader=csv.reader(open("ebook.csv","r"))

###关键字匹配搜索。容易出现隔断的情况
#http://127.0.0.1:5000/?key=Python
@app.route('/')
#@app.route('/<string:keywords>/')
def list():
    msg=[]
    key=request.args.get("key")
    print key
    for item in reader:
        if unicode(key).upper() in unicode(item[0]).upper():
           msg.append([unicode(item[0]),unicode(item[1]),unicode(item[2])])
    print msg
    return render_template('main.html', msg=msg)


#
@app.route('/demo/')
def list1():
    msg=[["1","2","3"]]

    # for m in msg:
    #     print m[0],m[1]
    return render_template('main.html', msg=msg)

#/search/?key=java
@app.route('/search/')
def rearch():
    key=request.args.get("key")
    print key
    result=search(key)
    print result
    return render_template('search.html', result=result)

if __name__=='__main__':
  app.run(debug=True)
  #app.debug=True