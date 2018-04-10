from os import path
import jieba.analyse as analyse
import jieba
jieba.load_userdict("/Users/alisa/Desktop/实训/关键词抽取/测试/userdict.txt")

text_path = '/Users/alisa/Desktop/实训/关键词抽取/测试/jieba分词测试.txt'

text = open(path.join(text_path)).read()
seg_list1 = jieba.cut(text, cut_all=False)



stopwords_path = '/Users/alisa/Desktop/实训/关键词抽取/中文停用词.txt'

def jiebaclearText(text):
    mywordlist=[]
    seg_list = jieba.cut(text, cut_all=False)
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
    return ' '.join(mywordlist)

text1 = jiebaclearText(text)
#print(" ".join(seg_list1))
#print(text1)

test_sent = (
"李小福是创新办主任也是云计算方面的专家; 什么是八一双鹿\n"
"例如我输入一个带“韩玉赏鉴”的标题，在自定义词库中也增加了此词为N类\n"
"「台中」正確應該不會被切開。mac上可分出「石墨烯」；此時又可以分出來凱特琳了。"
)

words = jieba.cut(test_sent)
print('/'.join(words))
#李小福/是/创新/办/主任/也/是/云/计算/方面/的/专家/;/ /什么/是/八/一双/鹿/
#/例如/我/输入/一个/带/“/韩玉/赏鉴/”/的/标题/，/在/自定义词/库中/也/增加/了/此/词为/N/类/
#/「/台/中/」/正確/應該/不會/被/切開/。/mac/上/可/分出/「/石墨/烯/」/；/此時/又/可以/分出/來凱/特琳/了/。

