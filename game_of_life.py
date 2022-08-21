import random
import time

def getround(list,i,j):
    sum=0
    for a in range(i-1,i+2):
        for b in range(j-1,j+2):
            if( 0<=a<10 and 0<=b<10 and list[a][b]=='#' and (a!=i or b!=j)):
                sum=sum+1

    if sum==2: return 1
    elif sum==3: return 2
    else: return 0

list=[]
for i in range(10):
    list_temp=[]
    for j in range(10):
        if(random.random()<0.8):
            list_temp.append('#')
        else:
            list_temp.append(' ')
    list.append(list_temp)
for i in range(10):
    for j in range(10):
        print(list[i][j],end='  ')
    print()
print('___________________________________-')


while(1):
    time.sleep(0.1)
    newlist=[]
    for i in range(10):
        newlist_temp=[]
        for j in range(10):
            judge=getround(list,i,j)
            if(judge==1):
                newlist_temp.append('#')
            elif(judge==2):
                newlist_temp.append(list[i][j])
            else: newlist_temp.append(' ')
        newlist.append(newlist_temp)
    list = newlist
    for i in range(10):
        for j in range(10):
            print(list[i][j], end='  ')
        print()
    print('___________________________________')











