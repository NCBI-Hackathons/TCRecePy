from time import time
from tcrecepy.distances import *
t1=time()

s1="CASSGATGREKFF"
s2="CASSGTTFREKFF"

weights=[1]*13

for ii in range(0,10000000):
    #TMP=sigmoid(np.dot(weights, np.fromiter(blosum62_score(s1,s2),int)))
    TMP=blosum62_distance([s1], [s2], weights=weights, allowed_gaps=0)

t2=time()

print (t2-t1)
