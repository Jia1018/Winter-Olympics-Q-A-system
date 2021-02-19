import numpy as np
import jieba

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

#获取专用名词列表
def specialword_list():
    specialwords = [line.strip() for line in open('data/specialword.txt', encoding='utf-8').readlines()]
    return specialwords

def try_divide(x, y, val=0.0):
    """
    算除法的函数
    """
    if y != 0.0:
        val = float(x) / y
    return val

def cosine_distance(v1, v2):
    """
    计算余弦距离
    """
    up = float(np.sum(v1 * v2))
    down = np.linalg.norm(v1) * np.linalg.norm(v2)
    return try_divide(up, down)


def get_score(vector_1,vector_2,dis_type):
    '''
    计算两个句子匹配度的函数
    ----------
    vector_1和vector_2是两个要比对的句子的特征向量 
    dis_type 是选择计算距离的方法（有很多种，可以根据效果调试）

    '''
    if dis_type==1:
        result=cosine_distance(vector_1,vector_2)
    #其它的距离计算函数还没加上去，我会再去找找
    
    return result

Qfeatures_file = 'data/Q_features.npy'
def get_result_id(question_sentence,question_vector,transfer_list):
    '''
    比对得到最大相似度的句子的id的函数
    ----------
    question_sentence 是对提问的句子进行jieba分词得到的元素为关键词的list组
    question_vector 是进一步处理后的特征向量
    transfer_list 是关键词和句子之间建立索引的字典
    '''
    Qset_vector = np.load(Qfeatures_file)
    q_vector = np.array(question_vector)
    max_similarity=0
    result_id=0
    super_key_num=0
    max_super_key_num=0
    list_for_contract=[]
    with open('data/QuestionSeg.txt', 'r', encoding='utf-8') as fin:
        seg_Q = fin.readlines()  
    for item in question_sentence:#对于提问的句子中的每一个关键词
        if item not in transfer_list:
            continue    
        for idx in transfer_list[item]:#对于关键词对应的句子
            #idx_to_sentence_list是把训练集的idx转换成关键词句子的数组
            seg_sentence = seg_Q[idx].split()
            super_key_num=0
            if item in seg_sentence:
                #specialwords是从存人名、时间、地点的文件里读出来的list
                specialwords = specialword_list()
                if item in specialwords:
                    super_key_num+=1
            if super_key_num>=max_super_key_num:
                if super_key_num>max_super_key_num:
                    max_super_key_num=super_key_num
                    list_for_contract=[]    #存在更大的就清空list
                list_for_contract.append(idx)#存下来人名地名时间匹配数最多的句子的id

    for idx in list_for_contract:
        score=get_score(Qset_vector[idx],q_vector,1)
        #逐个比对得到最大的相似值及其id
        if score>max_similarity:
            max_similarity=score
            result_id=idx
    
    #匹配度太低就抛弃掉
    if max_similarity < 0.8:
        result_id=-1
    
    '''for item in question_sentence:#对于提问的句子中的每一个关键词
        for idx in transfer_list[item.word]:#对于关键词对应的句子
            score=get_score(Qset_vector[idx],q_vector,1)
            #逐个比对得到最大的相似值及其id
            if score>max_similarity:
                max_similarity=score
                result_id=idx'''
    
    return result_id

def find_answer(result_id):
    # 打开文件
    #data = xlrd.open_workbook('标注数据1.xlsx')
    if result_id==-1:
        print("暂时没有合适的答案")
    else:
        with open('data/Answer.txt','r', encoding='gbk') as fin:
            Answers = fin.readlines()

    # 通过文件名获得工作表,获取工作表1
    #table = data.sheet_by_name('工作表1')

        # 获取某个单元格的值，答案在(id,B)单元格处
        answer = Answers[result_id] 
        return answer           
            
        