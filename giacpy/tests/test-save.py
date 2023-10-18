from sys import path
path.insert(0,'/home/fred/giacpy/build/lib.linux-x86_64-2.7')
#path.append('/home/fred/giacpy/build/lib.linux-x86_64-3.2')
from giacpy import *
a=giac('1111111111111112+2')
#write=giac('write')
#read=giac('read')
#giac('tmp:=%s'%a.__str__())
#write('"tutu.txt",tmp')
#import io
x,y,z=giac('x,y,z')
a=(x+y+z+2)**15+1
aa=(a*(a+1)).normal()

#with io.open('tutu2.txt', 'wb') as file:
#    #file.write(a.__str__().decode())
#    file.write(a.__str__())
#print("fin")
#with io.open('tutu2.txt', 'r') as file2:
#    b=Pygen(file2.read())
#    #b=0
#(a-b).ratnormal()
aa.save("tutusave.giacpy")
b=loadgiacgen("tutusave.giacpy")
print(b.factor().nops())
print(((b/a-2).factor()))


####################################################################
from tempfile import NamedTemporaryFile
F1=NamedTemporaryFile()
#tests: n=30 -> file size 3.2M
#       n=40 -> file size 12M (save 1s, load 2s)
#       n=60 -> file size 63M (save 6s, load 10s)
#       n=80 -> file size 212M (sur macbook save 19s, load 30s RAM during load: 1.5G?)
#       n=90 -> file size 350M (sur serveur save 43s, load 60s RAM during load: 2G?)
#       n=110-> file size 828M (sur serveur save 93s, load 123s RAM during load 4.6G?)

n=20
l1=giac('seq(ratnormal((x+y+z+2)**k),k=20..%s)'%(n))
from time import time
t=time()
print("saving l1")
l1.save(F1.name)
l1=0
print("done: time (s): ", time()-t)
k=raw_input("espace pour continuer : ")
print("loading l1")
t=time()
l1=loadgiacgen(F1.name)
print("done. time (s): ", time()-t)
for k in l1:
    print k.factor()

k=raw_input("espace entree pour effacer F1 : ")
F1.close()

#F1.close()
