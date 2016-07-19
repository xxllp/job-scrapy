#coding=utf-8
import json,csv,sys
import pandas as pd
###评论超过11w，从文本中分析情感和对岗位公司的打分等。难易程度等。
import jieba
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud

comment=pd.read_table(ur"C:/Users/Administrator/PycharmProjects/留影/job-scrapy/Job/tags.csv")
#print comment.head()
labels=set()
all=[]
for l in comment['﻿tags']:
    print [e.strip('[]').strip('\"').decode("utf-8") for e in l.split(",")]
    try:
      split_labels=[e.strip('[]').strip('\"').decode("utf-8") for e in l.split(",")]
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


plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.show()