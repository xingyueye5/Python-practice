## 记0星价值为1
## 忽略草的价值,2、3一草，4二草，5二、三草(>=0.396用二草），6三、四草（>=0.35用三草），7四草，8五、六草（>=0.22用五草），9六、S草（>=0.135用六）
## 10S、SS草（>=0.125用S），11SS、SSS草（>=0.116用SS)，12SSS、SSR草(>=0.107用SSS)
p_0=[1.000,1.000,0.968,0.686,0.495,0.396,0.319,0.264,0.220,0.135,0.125,0.116,0.107]
p_1=[0.880,0.792,0.550,0.403,0.330,0.264,0.212,0.132,0.045,0.046,0.043,0.0398]
p_2=[0.608,0.429,0.242,0.201,0.132,0.106,0.060,0.022,0.018,0.017,0.0157]
leaf= {1:1.2,2:1.4,3:1.7,4:2.0,5:2.4,6:2.7,'s':3.0,'ss':3.4,'sss':3.7,'ssr':4.0}
leaf_star=[1,1,1.2,1.2,1.4,1.4,1.7,2,2.4,2.7,3,3.4,3.7,4]
comb=['a','aa','ab','ac','aaa','aab','abb','aac','acc','abc','b','bb','bc','bbb','bbc','bcc']

class update:
    def __init__(self):
        self.value={0:1,1:2,2:3.136,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0,13:0}
        self.choice={0:'a',1:'b',2:'',3:'',4:'',5:'',6:'',7:'',8:'',9:'',10:'',11:'',12:''}
        self.tempval=[]  ##用来装临时Tn值


    def update(self,star): ##star>=2,返回加了四叶草的概率值
        res=[]
        res_leaf=[]
        self.tempval=[]
        for items in comb:
            (p,flag,val)=(0,0,0)
            for s in items:
                if s=='a':
                    p+=p_0[star]/3
                    val+=self.value[star]
                elif s=='b':
                    p+=p_1[star-1]/3
                    val+=self.value[star-1]
                elif s=='c':
                    p+=p_2[star-2]/3
                    val+=self.value[star-2]
                if flag==0:
                    p=p*3
                    flag=1
            res.append(p)
            self.tempval.append(val)
        (p,p_plus)=(leaf_star[star],leaf_star[star+1])
        for item in res:
            if (star==5 and item<0.396) or (star==6 and item<0.35) or (star==8 and item<0.22) or (star==9 and item<0.135) or(star==10 and item<0.125) or(star==11 and item<0.116)or(star==12 and item<0.107):
                temp=item*p_plus
            else:
                temp=item*p
            if temp>1:
                temp=1
            res_leaf.append(temp)
        return res_leaf


    def choose(self,p,star):  ##我们根据各种选择的概率表选择需要的强化方案并得到价值表
        (index,value)=(0,9999999999)
        if star<=5:
            for i in range(len(p)):
                v=self.tempval[i]/p[i]+self.value[star]
                if v<value:
                    value=v
                    index=i
        else:
            for i in range(len(p)):
                v=(self.value[star]+self.tempval[i]-(1-p[i])*self.value[star-1])/p[i]
                if v<value:
                    value=v
                    index=i
        self.value[star+1]=v
        self.choice[star]=comb[index]


if __name__=='__main__':
    my_update=update()
    for i in range(2,13):
        temp=my_update.update(i)
        print(i, '->', i + 1, ' possibilities=')
        for j in range(len(temp)):
            print(comb[j],':',temp[j])
        print()
        my_update.choose(my_update.update(i),i)
    print('final values: ',my_update.value)
    print('final choices: ',my_update.choice)





