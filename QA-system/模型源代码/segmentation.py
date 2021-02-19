# encoding=utf-8
import jieba
import json

#获取停用词列表
def stopword_list():
    stopwords = [line.strip() for line in open('data/stopword.txt', encoding='utf-8').readlines()]
    return stopwords

terms = {'1届': '一届', '2届': '二届', '3届': '三届', '4届': '四届', 
        '5届': '五届', '6届': '六届', '7届': '七届', '8届': '八届', 
        '9届': '九届', '10届': '十届', '11届': '十一届', '12届': '十二届', 
        '13届': '十三届', '14届': '十四届', '15届': '十五届', '16届': '十六届', 
        '17届': '十七届', '18届': '十八届', '19届': '十九届', '20届': '二十届', 
        '21届': '二十一届', '22届': '二十二届', '23届': '二十三届', '24届': '二十四届', 
        '25届': '二十五届'}
#对文本中的所有句子进行分词
def segmentation(strs, outputfile):
    sentence_list = []
    stopwords = stopword_list()
    jieba.load_userdict("data/dict.txt")  # 自定义词典
    #snum = 0
    for str in strs:
        for term in terms:
            if term in str:
                str.replace(term, terms[term])
        seg_list = jieba.lcut(str,cut_all=False)     #对一个句子分词
        for w in seg_list[::-1]:                      #过滤助词,介词和停用词
            if w in stopwords:
                seg_list.remove(w)
                continue
        for w in seg_list:
            outputfile.write("%s " %w)
        sentence_list.append(seg_list)                #形成分词后的句子列表
    return sentence_list

def create_index(sentence_list):
    key_word = {}
    for i in range(len(sentence_list)):
        for item in sentence_list[i]:
            if item in key_word:
                if i not in key_word[item]:
                    key_word[item].append(i)
            else:
                key_word[item] = [i]
    with open('data/index_table.json', 'w') as j:
        json.dump(key_word, j)

#训练集问句输入路径
Q_file = 'data/Question.txt'
#分好词的问句输出路径
Qseg_file = 'data/QuestionSeg.txt'
#对训练集进行分词
raw_Q = open(Q_file, 'r', encoding='utf-8')
Out_Q = open(Qseg_file, 'w', encoding='utf-8')
seg_list = segmentation(raw_Q, Out_Q) 
create_index(seg_list)
raw_Q.close()
Out_Q.close()
