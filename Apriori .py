##Apriori algorithm implement   目的是找出最终频繁集合
## 1、最终频繁集合
    #  k=1,计算每组元素出现频数，淘汰最小的那个（可以用集合的差进行描述）
    #  对新的集合内元素完成全连接操作，然后继续求出新集合每个元素频数，再进行淘汰
## 2、置信度与关联规则
    #   可能需要对以前各个集合内元素出现频数进行存储，然后对最终频繁集合每个非空子集进行拆解并求出置信度。
    #   按照之前定下来的置信度进行筛选，先查表，如果没有的话就当场计算
class Apriori:
    num,confidence=0,0  ##数据集个数以及最小置信度
    ##choose_set->去掉最小置信度集合->连接构造新集合交给present->choose_set=present
    choose_set=[]  ##集合列表，用于每一轮得到新的项集
    DATA=[]  ##集合列表，用于容纳初始值
    present=[] ##集合列表，用于临时存储choose_set里面的值
    cache=dict()##用于存储已经计算过的项集对于的支持度
    finalset=[]  ##储存最终频繁集合

    def __init__(self,path,confidence):

        f=open(path)
        chooseset = set()
        for line in f:
            temp=set(line.strip().split())
            chooseset=chooseset.union(temp)
            self.DATA.append(temp)
            self.num=self.num+1
        self.confidence=confidence
        print(self.DATA)
        for item in chooseset:
            self.choose_set.append(set(item))  ##产生一个一个子集

        self.iterate()
        self.print_confidence()

    def iterate(self):  ##多轮迭代得到最终频繁项集

        k,flag=2,1
        while flag:            ##选择淘汰
            tempval,idx=1,0
            listt,dellist=[],[]
            tempset=set()
            for sett in self.choose_set:
                addval = 0
                for sets in self.DATA:
                    if sets.intersection(sett)==sett:
                        addval+=1/self.num
                listt.append([addval,idx])
                self.cache[frozenset]=addval
                #self.cache.update(frozenset(sett),addval)
                idx+=1
            print('k={}时self.choose_set={}'.format(k,self.choose_set))
            for val in listt:
                tempval=min(tempval,val[0])
            for val in listt:
                if val[0]==tempval:
                    dellist.append(val[1])
            dellist.sort()
            dellist.reverse()
            for delidx in dellist:
                tempset=self.choose_set[delidx]
                self.choose_set.pop(delidx)

            for set1 in self.choose_set:
                for set2 in self.choose_set:
                    unionset=set1.union(set2)
                    if len(unionset)==k:
                        for item in self.present:
                            if item==unionset:
                                self.present.remove(item)
                        self.present.append(unionset)  #有可能重复

            self.choose_set=self.present.copy()
            self.present.clear()
            k+=1
            if len(self.choose_set)==0:
                flag=0
                print('最终频繁集合为:',tempset)
                self.finalset=list(tempset)


    def print_confidence(self):  ##输出>最小置信度的互补子集置信度
        n=len(self.finalset)
        for i in range(1,2**n):
            comb=[]
            for j in range(n):
                if (i>>j)%2==1:
                    comb.append(self.finalset[j])
            comb1=[j for j in self.finalset if j not in comb]
            set1=frozenset(comb)
            set2=frozenset(comb1)
            if set1 in self.cache.keys():
                val1=self.cache[set1]
            else:
                val1=0
                for sets in self.DATA:
                    if set1==set1.intersection(sets):
                        val1+=1/self.num
            if set2 in self.cache.keys():
                val2=self.cache[set2]
            else:
                val2=0
                for sets in self.DATA:
                    if set2==set2.intersection(sets):
                        val2+=1/self.num
            if val1/val2>=self.confidence:
                print('互补子集X:',set1,' 互补子集Y:',set2,'正则化:',val1/val2)


if __name__=='__main__': ##程序入口
    path='D:\Desktop\data.txt'
    apr=Apriori(path,0.6)
