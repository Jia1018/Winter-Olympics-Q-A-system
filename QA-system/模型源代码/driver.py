from json import dumps
from shell import print_answer
import xlrd
import os
import jieba
import xlwt

questions_num = 1733
data = xlrd.open_workbook('test/test.xlsx')
table = data.sheets()[0]
if os.path.exists("测试集result.json"):
    os.remove("测试集result.json")
f = open('测试集result.json', 'a+')

with open('data/Question.txt','r', encoding='utf-8') as fin:
    Questions = fin.readlines()
writebook = xlwt.Workbook()     #打开一个excel
sheet = writebook.add_sheet('test')     #在打开的excel中添加一个sheet
for i in range(questions_num):
    tmp_question = table.cell(i+1, 0).value
    ans,result_id = print_answer(tmp_question)
    sheet.write(i,0,Questions[result_id])    #写入excel，i行0列
    dic = {'question': tmp_question, 'answer': ans}
    js = dumps(dic, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
    print(js, file=f)
writebook.save('data/compare.xls')
f.close()