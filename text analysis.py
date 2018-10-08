# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 21:35:56 2018

@author: lenovo
"""

from io import StringIO
from io import open
import csv
import re 
import jieba
import jieba.posseg
from gensim import corpora,models,similarities,summarization
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
mpl.rcParams['axes.unicode_minus']=False #用来正常显示负号
mpl.rc('xtick', labelsize=16) #设置坐标轴刻度显示大小
mpl.rc('ytick', labelsize=16) 
font_size=25

def wordcount(str1):
    # 文章字符串前期处理
    count_dict = {}
    # 如果字典里有该单词则加1，否则添加入字典
    for str in str1:
        if str in count_dict.keys():
            count_dict[str] = count_dict[str] + 1
        else:
            count_dict[str] = 1
    #按照词频从高到低排列
    count_list=dict(sorted(count_dict.items(),key=lambda x:x[1],reverse=True))
    #删除超过百分之25
    #[i for i in count_dict.values()]
    return(count_list)

#投入产出的经营范围
csvFile = open('投入产出分类解释.csv','r', encoding='UTF-8') # 设置newline，否则两行之间会空一行
reader = csv.reader(csvFile)
touru_class = []
jingyingfanwei = []
daima_class = []
i=1
for line in reader:
    if i>=3:
        touru = ''
        jingying = ''
        touru_class.append(touru.join(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]',line[1])))
        daima_class.append(line[0])
        rawjingying = jingying.join(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]',line[2]))
        segs = jieba.posseg.cut(rawjingying)
        l = [] 
        for seg in segs:
            if seg.flag == 'n':
                l.append(seg.word)
        jingyingfanwei.append(l)
    i += 1
#统计词频

#删除'指'
deleteName = ['指']
index = 1
for stock in jingyingfanwei:
    for cell in stock:
        if cell in deleteName:
            stock.remove(cell)
    index += 1
    print(index)
    

l = []
for i in jingyingfanwei:
    l.extend(i)
countStocks_touru = wordcount(l)
countStocks_touru.items()
  
dictionary = corpora.Dictionary(jingyingfanwei) ##获取词袋
corpus = [dictionary.doc2bow(title) for title in jingyingfanwei]
doc_test_vec = [dictionary.doc2bow(title) for title in allStock]
tfidf = models.TfidfModel(corpus)
tfidf_vectors = tfidf[corpus]
indexStock = similarities.MatrixSimilarity(tfidf_vectors)
sim = indexStock[tfidf[doc_test_vec]]
class_touru = np.argmax(sim,axis=1)
#分类
stock_class_2 = []
for i in class_touru:
    stock_class_2.append(daima_class[i])    
#二级分类转一级
csvFile = open('分类细则.csv','r', encoding='GBK') # 设置newline，否则两行之间会空一行
reader = csv.reader(csvFile,delimiter='\t')   
class_1 =[]
class_2 = []  
for line in reader:
    class_1.append(line[0])
    class_2.append(line[1])
    
#分类匹配
touru_class_21 = []
for obj in stock_class_2:
    index_1 = [i for i,j in enumerate(class_2) if j==obj]
    raw_info = class_1[index_1[0]]
    aft_info = ''
    aft_info = aft_info.join(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]',raw_info))
    touru_class_21.append(aft_info)
    
with open('余弦相似度分类股票_2.csv','w',newline='',encoding='utf-8') as csvfile: 
    writer = csv.writer(csvfile,delimiter=',')
    #先写入列名
    writer.writerow(["股票代码","投入产出分类"])
    for i in range(len(touru_class_21)):
        writer.writerow([Stockname[i+1],touru_class_21[i]])

# figure 1        
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
count_class21 = wordcount(touru_class_21)
values = (list(count_class21.values()))
rects=plt.bar(range(len(values)), values)
index = range(42)
plt.xticks(index,  count_class21.keys())
tickx = ax.get_xticklabels()
#ticky = ax2.get_yticklabels()
ax.set_xticklabels(range(42),fontsize=16)#,rotation=90

# CSV
List_class = list(count_class21.keys())
List_num = list(count_class21.values())
with open('分类结果.csv','w',newline='',encoding='utf-8') as csvfile: 
    writer = csv.writer(csvfile,delimiter=',')
    writer.writerow(["行业","分类数量"])
    for i in range(len(count_class21)):
        writer.writerow([List_class[i],List_num[i]])
        

# figure histgoram of firms       
words = []
for stock in allStock:
    words.append(len(stock))
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
ax.hist(words,rwidth=0.6,bins=50)
# ax.hist(wordcount(touru_class_21),rwidth=0.6,bins=50)