#coding=utf-8
###公司数量为1000个，对其进行清洗，做些简单的统计分析。对标签进行统计，可视化结果(词云)
####主要看到的标签就是五险一金和带薪年假,岗位
import json,csv,sys
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

company=pd.read_csv(ur"C:/Users/Administrator/PycharmProjects/留影/job-scrapy/Job/company.csv",sep=",")
labels=set()
all=[]
###分为公司标签和其他标签，但是标签很多
for l in company.otherLabels:
     try:
      split_labels=[e.decode("utf-8") for e in l.split(",")]
     except Exception as e:
        split_labels=[]
     labels=labels.union(set(split_labels))
     all.extend(split_labels)
for label in labels:
        print label

print len(labels),len(all)
##需要统计词频来看。
freq = {k:all.count(k) for k in set(all)}.items()
print freq

masks = np.array(Image.open("aa.jpg"))

wordcloud = WordCloud(font_path=r'c:\windows\fonts\simsun.ttc',mask=masks).generate_from_frequencies(freq)

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
import matplotlib
f=matplotlib.font_manager.FontProperties(fname='/usr/share/fonts/cjkunifonts-ukai/ukai.ttc')

plt.imshow(wordcloud)
plt.axis("off")
plt.show()
# take relative word frequencies into account, lower max_font_size
# wordcloud = WordCloud(font_path=r'c:\windows\fonts\simsun.ttc',background_color="white",max_font_size=40, relative_scaling=.5,mask=masks).generate_from_frequencies(freq)
#
# plt.figure()
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.show()




