import re
line="30天安利鹿晗# 情人节快乐，好像想要玩偶的人比较多，带话题并艾特@M鹿M  ，抽一人送一只鹿五岁[女孩儿][女孩儿][女孩儿] ​​​,转发理由"
cl_line=re.sub("\[.+\]","",line)
print(cl_line)