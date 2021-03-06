import numpy as np
import re
import pandas as pd
import jieba
from scipy.sparse import coo_matrix
from sklearn.linear_model import LogisticRegression


url_jiebaDict = "/Users/alisa/Desktop/实训/关键词抽取/p_userdict.txt"
jieba.load_userdict(url_jiebaDict)
stopwords_path = "/Users/alisa/Desktop/实训/关键词抽取/中文停用词.txt"

def main():
    url_data="/Users/alisa/Desktop/实训/关键词抽取/weibo_10usr.csv"
    dt=pd.read_csv(url_data)
    ur = dt.ix[:, ['uid', 'text']]
    id1=dt.ix[:,'uid']
    id2=list(set(id1))

    for id_now in id2:
        try:
            #分词 传入数据框，用户id，停用词路径；传出word_dict，usr_word，target_list
            (word_dict,usr_word,target_list)= cutWord(ur,id_now)
            #把词转成数字
            word_map=word2num(word_dict)
            #把用户{编号:{词：次数}}的字典中的词用word_map中的数字对应
            usr_word_matrix=usrword2num(word_map,usr_word)
            #构造稀疏矩阵
            lens=len(word_dict)
            x=sparseMatrix(usr_word_matrix,lens)
            #L1LR特征选择
            name=word_dict.keys()
            L1LR=LogisticRegression(penalty="l1", C=0.1)
            L1LR.fit(x, target_list)
            ceof=np.array(L1LR.coef_)
            d_ceof=pd.DataFrame(ceof.reshape(len(ceof[0,:]),1),index=name,columns=list('c'))
            d_hotword=d_ceof[d_ceof.c>0].sort_values(ascending = False,by='c')
        except Exception:
            continue
        else:
            print(id_now,":")
            print(d_hotword.index)

    #分词函数
def cutWord(ur,id_now):
    word_dict={} #用于保存去重的关键词
    usr_word = {} #用于保存每个用户的关键词及其数量
    target_list = [] #用于保存模型的y值：是否为目标用户
    i = 0 #文本顺序索引（会排除空值）

    for ur_row in range(0, len(ur)):
        text=ur.iloc[ur_row]['text']
        id=ur.iloc[ur_row]['uid']
        mywordlist=[]

        try:
            text_cl_emoticons=re.sub("\[.+\]","",text) #去除表情文字
            text_cl = re.sub("[0-9\[\"\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\.\<\>\/\?\~\！\@\#\\\&\*\%\，\~\~\：\。\……\【\】\？\《\》\；]", "", text_cl_emoticons)
        except TypeError:
            continue
        #print(text_cl) #去重英文、数字、特殊符号后的文本
        seg_list = jieba.cut(text_cl, cut_all=False)
        liststr="/".join(seg_list)
        f_stop=open(stopwords_path)
        try:
            f_stop_text = f_stop.read()
        finally:
            f_stop.close()
        f_stop_seg_list = f_stop_text.split('\n')
        for myword in liststr.split('/'):

            if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
                mywordlist.append(myword)
                if(word_dict.__contains__(myword)):
                    word_dict[myword]=word_dict[myword]+1
                else:
                    word_dict[myword]=1
        usr_word[i]=mywordlist #每个用户的词
        i=i+1
        #构建用户target向量
        if(id==id_now): target_list.append(1)
        else: target_list.append(0)
    return (word_dict,usr_word,target_list)

#把词对应到数字
def word2num(word_dict):
    word_list=word_dict.keys()
    word_map={}
    index=0
    #world_list的index对应矩阵的列
    for word in word_list:
        word_map[word]=index
        index+=1
    return word_map

#用户词转数字
def usrword2num(word_map,usr_word):
    usr_word_matrix={}
    k=0
    for k,v in usr_word.items():
        row={}#统计词频用
        newWorld={}  # 是否是新词
        for myword in v:
            if(word_map.__contains__(myword)):
                if(newWorld.__contains__(myword)==False):
                    row[word_map[myword]]=1
                    newWorld[myword]=1
                else:
                    row[word_map[myword]]+=1
                # print(word_map[myword]," ;")


        usr_word_matrix[k]=row
        k+=1
    return usr_word_matrix;

#稀疏矩阵
def sparseMatrix(usr_word_matrix,lens):
# arr_row:usr_word_matrix的key(要循环该row的长度)
# arr_colum:usr_word_matrix的value中的key
# arr_data:usr_word_matrix的value中的value
    arr_row=[]
    arr_col=[]
    arr_data=[]
    row_line=0
    for row in usr_word_matrix:
        for col_data in usr_word_matrix[row]:
            arr_row.append(row)
            arr_col.append(col_data)
            arr_data.append(usr_word_matrix[row][col_data])
        row_line+=1
    row=np.array(arr_row)
    col=np.array(arr_col)
    data=np.array(arr_data)
    sm=coo_matrix((data,(row,col)), shape=(row_line,lens)).todense()
    return sm




if __name__ == '__main__':
    main()