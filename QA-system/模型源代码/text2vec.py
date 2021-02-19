# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 20:24:21 2021

@author: Cai Luoshan

Sentence to Vector: feature extraction encoding
"""

#原始问句输入路径
Qsentence_file = 'data/Question.txt'
#问句特征向量输出路径
Qfeatures_file = 'data/Q_features.npy'

sentences = open(Qsentence_file, 'r') #tuple类型
Sentences = list(sentences)


'''==========================sklearn(词袋模型+TF-IDF)==============================
from sklearn.feature_extraction.text import CountVectorizer
count_vec = CountVectorizer()
Vectors_1 = count_vec.fit_transform(Sentences).toarray()
#单纯地统计词频，得到一个句子向量，非常稀疏，感觉无法对一个句子和另一个句子进行比较，维度都不一样？'''

'''========================Bert模型库=============================='''
from bert_serving.client import BertClient
bert_client = BertClient()
Vectors_2 = []
for idx,sentence in enumerate(Sentences):
    Vectors_2.append(bert_client.encode([sentence])) #对每个句子进行特征提取，维度为768
import numpy as np
features = np.array(Vectors_2)
np.save(Qfeatures_file,features)

'''==========================word2vec=============================
from gensim.models import Word2Vec
import numpy as np
dim = 300
#预训练词向量模型
model = Word2Vec(Sentences, sg=1, size=dim,  window=5,  min_count=0,  negative=3, sample=0.001, hs=1, workers=4)
model.save("data/word2vec.model")
#构建文本数据集的特征向量:调用模型索引词向量获取样本中每个词的词向量，直接相加
def Get_Feature(sentences, word_vec, dim):
    m = len(sentences)
    feature = np.zeros((m,dim))
    for i,sentence in enumerate(sentences):
        for w in sentence:
            feature[i,:] += word_vec[w]
    return feature
model = Word2Vec.load("data/word2vec.model")
word_vec = model.wv
Vectors_3 = Get_Feature(Sentences,word_vec,dim)
np.save(Qfeatures_file,Vectors_3)'''