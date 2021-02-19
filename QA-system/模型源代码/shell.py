from get_result import *
import jieba
from bert_serving.client import BertClient
bert_client = BertClient()
'''from gensim.models import Word2Vec'''
import json

test_Qfile = open('data/test_Question.txt','w')

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

def print_answer(question):
    question_seg=segmentation([question], test_Qfile)   #segmentation把它分成关键词组
    question_vector=bert_client.encode([question])      #vectorize函数得到特征向量
    found=0
    #读取倒排序索引
    with open('data/index_table.json','r',encoding='utf-8') as fp:
        transfer_list = json.load(fp)
    #看看是否有相同的关键词
    for item in question_seg[0]:
        if item in transfer_list:#.keys()
            found=1
    #如果相同的关键词都没有那就肯定没有答案了
    if found==0:
        print('暂时寻找不到答案')
        return "NAN",0
    else:
        result_id=get_result_id(question_seg[0],question_vector,transfer_list)
        answer = find_answer(result_id)  
        '''print("答案是：" + answer)
        print(result_id)'''
        return answer,result_id   
    

if __name__ == '__main__':
    while True:
        sentence1 = input('请输入您需要问的冬奥会问题(输入quit退出)：\n')
        if sentence1 == 'quit':
            break
        else:
            answer,result_id = print_answer(sentence1)
