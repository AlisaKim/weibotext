import  pandas as pd
import numpy as np
a=np.array([0,0,1,1,2,20,0,4,0,3])
print(a)
b=[1,2,3,4,5,6,7,8,9,10]
d=pd.DataFrame(a,index=b,columns=list('c'))
print(d)
#print(d[d.c!=0])
#print(d[d!=0])
